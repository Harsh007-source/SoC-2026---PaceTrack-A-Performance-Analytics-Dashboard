"""
Assignment 2: The Data Sanitizer
Weeks 3-4: Data Engineering & File Ingestion

This module handles reading, cleaning, and organizing fitness tracker data.
Supports: CSV, JSON, and GPX files.
"""

import pandas as pd
import json
import gpxpy
import gpxpy.gpx
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Union


class DataSanitizer:
    """Handle ingestion and sanitization of fitness tracking data."""

    def __init__(self):
        self.stats = {
            'total_rows': 0,
            'missing_data_points': 0,
            'corrupted_data_points': 0,
            'start_timestamp': None,
            'end_timestamp': None,
            'file_type': None
        }

    def ingest_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Main ingestion method that routes to appropriate parser.

        Args:
            file_path: Path to the data file

        Returns:
            Dictionary containing cleaned data and statistics
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.stat().st_size == 0:
            return self._handle_empty_file(file_path)

        suffix = file_path.suffix.lower()

        if suffix == '.csv':
            return self._ingest_csv(file_path)
        elif suffix == '.json':
            return self._ingest_json(file_path)
        elif suffix == '.gpx':
            return self._ingest_gpx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}. Supported: .csv, .json, .gpx")

    def _handle_empty_file(self, file_path: Path) -> Dict[str, Any]:
        """Handle empty file gracefully."""
        return {
            'status': 'error',
            'message': f'File is empty: {file_path.name}',
            'data': None,
            'stats': self.stats
        }

    def _ingest_csv(self, file_path: Path) -> Dict[str, Any]:
        """Ingest and clean CSV fitness data."""
        try:
            df = pd.read_csv(file_path)
            self.stats['file_type'] = 'CSV'
            self.stats['total_rows'] = len(df)

            # Handle missing values
            missing_count = df.isnull().sum().sum()
            self.stats['missing_data_points'] = int(missing_count)

            # Try to identify timestamp columns
            timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]

            if timestamp_cols:
                df = self._sanitize_timestamps(df, timestamp_cols[0])

            # Fill missing numeric values with forward fill, then backward fill
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            df[numeric_cols] = df[numeric_cols].ffill().bfill()

            # Handle GPS coordinates if present
            if 'latitude' in df.columns and 'longitude' in df.columns:
                corrupted_gps = ((df['latitude'].isnull()) | (df['longitude'].isnull())).sum()
                self.stats['corrupted_data_points'] += int(corrupted_gps)
                # Remove rows with missing GPS coordinates
                df = df.dropna(subset=['latitude', 'longitude'])

            return {
                'status': 'success',
                'message': f'Successfully processed {len(df)} rows from CSV',
                'data': df,
                'stats': self.stats
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing CSV: {str(e)}',
                'data': None,
                'stats': self.stats
            }

    def _ingest_json(self, file_path: Path) -> Dict[str, Any]:
        """Ingest and clean JSON fitness data."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self.stats['file_type'] = 'JSON'

            # Handle nested JSON structures
            if isinstance(data, list):
                df = pd.json_normalize(data)
            elif isinstance(data, dict):
                # Check if data is wrapped in a key
                if 'activities' in data:
                    df = pd.json_normalize(data['activities'])
                elif 'data' in data:
                    df = pd.json_normalize(data['data'])
                else:
                    df = pd.json_normalize([data])
            else:
                raise ValueError("Unsupported JSON structure")

            self.stats['total_rows'] = len(df)

            # Handle missing values
            missing_count = df.isnull().sum().sum()
            self.stats['missing_data_points'] = int(missing_count)

            # Try to identify timestamp columns
            timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]

            if timestamp_cols:
                df = self._sanitize_timestamps(df, timestamp_cols[0])

            return {
                'status': 'success',
                'message': f'Successfully processed {len(df)} rows from JSON',
                'data': df,
                'stats': self.stats
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing JSON: {str(e)}',
                'data': None,
                'stats': self.stats
            }

    def _ingest_gpx(self, file_path: Path) -> Dict[str, Any]:
        """Ingest and clean GPX fitness data."""
        try:
            with open(file_path, 'r') as f:
                gpx = gpxpy.parse(f)

            self.stats['file_type'] = 'GPX'

            # Extract track points
            points_data = []

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        point_dict = {
                            'latitude': point.latitude,
                            'longitude': point.longitude,
                            'elevation': point.elevation,
                            'time': point.time
                        }
                        points_data.append(point_dict)

            if not points_data:
                return {
                    'status': 'error',
                    'message': 'No track points found in GPX file',
                    'data': None,
                    'stats': self.stats
                }

            df = pd.DataFrame(points_data)
            self.stats['total_rows'] = len(df)

            # Handle missing GPS coordinates
            missing_coords = ((df['latitude'].isnull()) | (df['longitude'].isnull())).sum()
            self.stats['corrupted_data_points'] = int(missing_coords)

            # Remove rows with missing coordinates
            df = df.dropna(subset=['latitude', 'longitude'])

            # Handle missing elevation
            missing_elevation = df['elevation'].isnull().sum()
            self.stats['missing_data_points'] = int(missing_elevation)

            # Fill missing elevation with interpolation
            df['elevation'] = df['elevation'].interpolate(method='linear')

            # Sanitize timestamps
            if 'time' in df.columns:
                df = self._sanitize_timestamps(df, 'time')

            return {
                'status': 'success',
                'message': f'Successfully processed {len(df)} track points from GPX',
                'data': df,
                'stats': self.stats
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing GPX: {str(e)}',
                'data': None,
                'stats': self.stats
            }

    def _sanitize_timestamps(self, df: pd.DataFrame, time_column: str) -> pd.DataFrame:
        """Convert timestamps to uniform YYYY-MM-DD HH:MM:SS format."""
        try:
            # Convert to datetime
            df[time_column] = pd.to_datetime(df[time_column], errors='coerce')

            # Count corrupted timestamps
            corrupted_times = df[time_column].isnull().sum()
            self.stats['corrupted_data_points'] += int(corrupted_times)

            # Remove rows with corrupted timestamps
            df = df.dropna(subset=[time_column])

            if len(df) > 0:
                # Set start and end timestamps
                self.stats['start_timestamp'] = df[time_column].min().strftime('%Y-%m-%d %H:%M:%S')
                self.stats['end_timestamp'] = df[time_column].max().strftime('%Y-%m-%d %H:%M:%S')

                # Format timestamp column
                df[time_column] = df[time_column].dt.strftime('%Y-%m-%d %H:%M:%S')

            return df

        except Exception as e:
            print(f"Warning: Could not sanitize timestamps: {str(e)}")
            return df

    def print_report(self, result: Dict[str, Any]):
        """Print a formatted ingestion report."""
        print("\n" + "="*60)
        print("DATA SANITIZER REPORT")
        print("="*60)

        if result['status'] == 'error':
            print(f"[ERROR]: {result['message']}")
            return

        print(f"[OK] Status: {result['message']}")
        print("\nStatistics:")
        print(f"  • File Type: {result['stats']['file_type']}")
        print(f"  • Total Rows Processed: {result['stats']['total_rows']}")
        print(f"  • Missing Data Points: {result['stats']['missing_data_points']}")
        print(f"  • Corrupted Data Points: {result['stats']['corrupted_data_points']}")

        if result['stats']['start_timestamp']:
            print(f"\nTimestamp Range:")
            print(f"  • Start: {result['stats']['start_timestamp']}")
            print(f"  • End:   {result['stats']['end_timestamp']}")

        print("\nData Preview:")
        if result['data'] is not None:
            print(result['data'].head(5).to_string())

        print("="*60 + "\n")


def main():
    """Demo function showing usage of DataSanitizer."""
    sanitizer = DataSanitizer()

    # Example usage - replace with actual file path
    print("Data Sanitizer - Assignment 2")
    print("Place your fitness data file in the Assignment_2 folder")
    print("Supported formats: .csv, .json, .gpx")

    # Check for sample files in the directory
    sample_files = list(Path('.').glob('*.csv')) + list(Path('.').glob('*.json')) + list(Path('.').glob('*.gpx'))

    if sample_files:
        print(f"\nFound sample file(s): {[f.name for f in sample_files]}")
        for file in sample_files:
            result = sanitizer.ingest_file(file)
            sanitizer.print_report(result)
    else:
        print("\nNo sample files found. Creating a demo...")
        # Create a demo CSV
        demo_data = {
            'time': ['2026-01-15 08:00:00', '2026-01-15 08:05:00', '2026-01-15 08:10:00'],
            'latitude': [40.7128, 40.7130, 40.7135],
            'longitude': [-74.0060, -74.0058, -74.0055],
            'heart_rate': [120, 135, 142]
        }
        demo_df = pd.DataFrame(demo_data)
        demo_df.to_csv('sample_activity.csv', index=False)
        print("Created sample_activity.csv for demonstration")

        result = sanitizer.ingest_file('sample_activity.csv')
        sanitizer.print_report(result)


if __name__ == "__main__":
    main()
