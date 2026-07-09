"""
Assignment 3: The Analytics Engine
Weeks 5-6: Backend Logic & Performance Metrics Computation

This module computes performance metrics from fitness tracker data:
- Distance calculations using Haversine formula
- Dynamic split times (pace per kilometer)
- Heart Rate zones breakdown
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from math import radians, sin, cos, sqrt, atan2


class AnalyticsEngine:
    """Compute performance metrics from fitness tracking data."""

    # Heart Rate Zones (standard percentages of max HR)
    # Assuming max HR = 220 - age (for age 25 = 195 bpm)
    MAX_HR = 195
    HR_ZONES = {
        'Zone 1': (0.50 * MAX_HR, 0.60 * MAX_HR),    # Recovery: 98-117 bpm
        'Zone 2': (0.60 * MAX_HR, 0.70 * MAX_HR),    # Aerobic: 117-137 bpm
        'Zone 3': (0.70 * MAX_HR, 0.80 * MAX_HR),    # Tempo: 137-156 bpm
        'Zone 4': (0.80 * MAX_HR, 0.90 * MAX_HR),    # Threshold: 156-176 bpm
        'Zone 5': (0.90 * MAX_HR, 1.00 * MAX_HR),    # Maximum: 176-195 bpm
    }

    def __init__(self, max_hr: int = 195):
        """
        Initialize analytics engine.

        Args:
            max_hr: Maximum heart rate (default: 195 for age 25)
        """
        self.MAX_HR = max_hr
        self._update_hr_zones()

    def _update_hr_zones(self):
        """Update HR zones based on max heart rate."""
        self.HR_ZONES = {
            'Zone 1': (0.50 * self.MAX_HR, 0.60 * self.MAX_HR),
            'Zone 2': (0.60 * self.MAX_HR, 0.70 * self.MAX_HR),
            'Zone 3': (0.70 * self.MAX_HR, 0.80 * self.MAX_HR),
            'Zone 4': (0.80 * self.MAX_HR, 0.90 * self.MAX_HR),
            'Zone 5': (0.90 * self.MAX_HR, 1.00 * self.MAX_HR),
        }

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula.

        Args:
            lat1, lon1: First coordinate (latitude, longitude)
            lat2, lon2: Second coordinate (latitude, longitude)

        Returns:
            Distance in kilometers
        """
        # Earth's radius in kilometers
        R = 6371.0

        # Convert degrees to radians
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def calculate_cumulative_distance(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate cumulative distance from GPS coordinates.

        Args:
            df: DataFrame with 'latitude' and 'longitude' columns

        Returns:
            DataFrame with added 'segment_distance' and 'cumulative_distance' columns
        """
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            raise ValueError("DataFrame must contain 'latitude' and 'longitude' columns")

        # Calculate distance for each segment
        distances = []
        for i in range(len(df)):
            if i == 0:
                distances.append(0.0)
            else:
                dist = self.haversine_distance(
                    df.iloc[i-1]['latitude'],
                    df.iloc[i-1]['longitude'],
                    df.iloc[i]['latitude'],
                    df.iloc[i]['longitude']
                )
                distances.append(dist)

        df['segment_distance'] = distances
        df['cumulative_distance'] = df['segment_distance'].cumsum()

        return df

    def calculate_split_times(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Calculate kilometer split times (pace per kilometer).

        Args:
            df: DataFrame with 'time' and 'cumulative_distance' columns

        Returns:
            List of split dictionaries with kilometer, time, and pace
        """
        if 'time' not in df.columns or 'cumulative_distance' not in df.columns:
            raise ValueError("DataFrame must contain 'time' and 'cumulative_distance' columns")

        # Convert time column to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df['time']):
            df['time'] = pd.to_datetime(df['time'])

        splits = []
        start_time = df.iloc[0]['time']
        total_distance = df.iloc[-1]['cumulative_distance']

        # Calculate splits for each kilometer
        for km in range(1, int(total_distance) + 1):
            # Find the point closest to this kilometer mark
            km_idx = (df['cumulative_distance'] - km).abs().idxmin()

            if km_idx in df.index:
                km_time = df.loc[km_idx, 'time']
                elapsed_seconds = (km_time - start_time).total_seconds()

                # Calculate pace for this specific kilometer
                if km == 1:
                    km_start_idx = 0
                else:
                    km_start_idx = (df['cumulative_distance'] - (km - 1)).abs().idxmin()

                km_start_time = df.iloc[km_start_idx]['time']
                km_elapsed = (km_time - km_start_time).total_seconds()

                # Convert to min:sec per km
                pace_minutes = int(km_elapsed // 60)
                pace_seconds = int(km_elapsed % 60)

                splits.append({
                    'kilometer': km,
                    'time': f"{int(elapsed_seconds // 3600):02d}:{int((elapsed_seconds % 3600) // 60):02d}:{int(elapsed_seconds % 60):02d}",
                    'pace': f"{pace_minutes}:{pace_seconds:02d}",
                    'pace_seconds': km_elapsed
                })

        return splits

    def calculate_hr_zones(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Calculate heart rate zones breakdown.

        Args:
            df: DataFrame with 'heart_rate' and 'time' columns

        Returns:
            Dictionary with time spent in each HR zone
        """
        if 'heart_rate' not in df.columns:
            raise ValueError("DataFrame must contain 'heart_rate' column")

        # Convert time column to datetime if present
        if 'time' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['time']):
            df['time'] = pd.to_datetime(df['time'])

        # Calculate time intervals (time between consecutive points)
        if 'time' in df.columns and len(df) > 1:
            time_diffs = df['time'].diff().dt.total_seconds().fillna(0)
        else:
            # If no time column, assume 1 second intervals
            time_diffs = pd.Series([1.0] * len(df))

        # Classify each heart rate reading into zones
        zone_times = {zone: 0.0 for zone in self.HR_ZONES.keys()}

        for idx, hr in enumerate(df['heart_rate']):
            if pd.isna(hr):
                continue

            for zone_name, (min_hr, max_hr) in self.HR_ZONES.items():
                if min_hr <= hr < max_hr or (zone_name == 'Zone 5' and hr >= min_hr):
                    zone_times[zone_name] += time_diffs.iloc[idx]
                    break

        # Calculate percentages and format output
        total_time = sum(zone_times.values())
        zone_breakdown = {}

        for zone_name, seconds in zone_times.items():
            percentage = (seconds / total_time * 100) if total_time > 0 else 0
            minutes = int(seconds // 60)
            secs = int(seconds % 60)

            zone_breakdown[zone_name] = {
                'time_seconds': seconds,
                'time_formatted': f"{minutes}:{secs:02d}",
                'percentage': round(percentage, 1),
                'hr_range': f"{int(self.HR_ZONES[zone_name][0])}-{int(self.HR_ZONES[zone_name][1])} bpm"
            }

        return zone_breakdown

    def calculate_pace(self, distance_km: float, time_seconds: float) -> str:
        """
        Calculate pace in min:sec per kilometer.

        Args:
            distance_km: Distance in kilometers
            time_seconds: Time in seconds

        Returns:
            Pace string in format "M:SS"
        """
        if distance_km <= 0:
            return "0:00"

        pace_seconds = time_seconds / distance_km
        minutes = int(pace_seconds // 60)
        seconds = int(pace_seconds % 60)

        return f"{minutes}:{seconds:02d}"

    def apply_rolling_average(self, df: pd.DataFrame, column: str, window: int = 5) -> pd.DataFrame:
        """
        Apply rolling average to smooth noisy data.

        Args:
            df: DataFrame
            column: Column name to smooth
            window: Rolling window size (default: 5)

        Returns:
            DataFrame with smoothed column added as '{column}_smoothed'
        """
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")

        df[f'{column}_smoothed'] = df[column].rolling(window=window, min_periods=1).mean()
        return df

    def analyze_activity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Complete activity analysis pipeline.

        Args:
            df: DataFrame with GPS and heart rate data

        Returns:
            Comprehensive analytics dictionary
        """
        results = {
            'status': 'success',
            'metrics': {}
        }

        try:
            # Calculate distances
            if 'latitude' in df.columns and 'longitude' in df.columns:
                df = self.calculate_cumulative_distance(df)
                total_distance = df.iloc[-1]['cumulative_distance']
                results['metrics']['total_distance_km'] = round(total_distance, 2)

                # Calculate split times if time data available
                if 'time' in df.columns:
                    splits = self.calculate_split_times(df)
                    results['metrics']['split_times'] = splits

                    # Overall pace
                    start_time = pd.to_datetime(df.iloc[0]['time'])
                    end_time = pd.to_datetime(df.iloc[-1]['time'])
                    total_seconds = (end_time - start_time).total_seconds()
                    overall_pace = self.calculate_pace(total_distance, total_seconds)
                    results['metrics']['overall_pace'] = overall_pace
                    results['metrics']['total_time'] = f"{int(total_seconds // 3600):02d}:{int((total_seconds % 3600) // 60):02d}:{int(total_seconds % 60):02d}"

            # Heart rate analysis
            if 'heart_rate' in df.columns:
                hr_zones = self.calculate_hr_zones(df)
                results['metrics']['hr_zones'] = hr_zones

                # Basic HR stats
                results['metrics']['avg_heart_rate'] = round(df['heart_rate'].mean(), 1)
                results['metrics']['max_heart_rate'] = int(df['heart_rate'].max())
                results['metrics']['min_heart_rate'] = int(df['heart_rate'].min())

            # Elevation analysis if available
            if 'elevation' in df.columns:
                elevation_gain = df['elevation'].diff().clip(lower=0).sum()
                results['metrics']['elevation_gain_m'] = round(elevation_gain, 1)

            return results

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error analyzing activity: {str(e)}",
                'metrics': {}
            }

    def print_analytics_report(self, results: Dict[str, Any]):
        """Print formatted analytics report."""
        print("\n" + "="*60)
        print("ANALYTICS ENGINE REPORT")
        print("="*60)

        if results['status'] == 'error':
            print(f"❌ ERROR: {results['message']}")
            return

        metrics = results['metrics']

        if 'total_distance_km' in metrics:
            print(f"\n📏 DISTANCE METRICS")
            print(f"  • Total Distance: {metrics['total_distance_km']} km")

            if 'total_time' in metrics:
                print(f"  • Total Time: {metrics['total_time']}")
                print(f"  • Overall Pace: {metrics['overall_pace']} /km")

        if 'split_times' in metrics:
            print(f"\n⏱️  SPLIT TIMES (per kilometer)")
            for split in metrics['split_times']:
                print(f"  • KM {split['kilometer']}: {split['pace']} /km (elapsed: {split['time']})")

        if 'hr_zones' in metrics:
            print(f"\n❤️  HEART RATE ANALYSIS")
            print(f"  • Average HR: {metrics['avg_heart_rate']} bpm")
            print(f"  • Min HR: {metrics['min_heart_rate']} bpm")
            print(f"  • Max HR: {metrics['max_heart_rate']} bpm")
            print(f"\n  HR Zone Breakdown:")
            for zone, data in metrics['hr_zones'].items():
                print(f"    {zone} ({data['hr_range']}): {data['time_formatted']} ({data['percentage']}%)")

        if 'elevation_gain_m' in metrics:
            print(f"\n⛰️  ELEVATION")
            print(f"  • Total Gain: {metrics['elevation_gain_m']} meters")

        print("="*60 + "\n")


def main():
    """Demo function showing usage of AnalyticsEngine."""
    print("Analytics Engine - Assignment 3")
    print("This module computes performance metrics from fitness data\n")

    # Create sample data
    sample_data = {
        'time': pd.date_range('2026-01-15 08:00:00', periods=50, freq='30s'),
        'latitude': np.linspace(40.7128, 40.7228, 50) + np.random.normal(0, 0.0001, 50),
        'longitude': np.linspace(-74.0060, -73.9960, 50) + np.random.normal(0, 0.0001, 50),
        'elevation': np.linspace(10, 50, 50) + np.random.normal(0, 2, 50),
        'heart_rate': np.clip(np.random.normal(145, 15, 50), 100, 190)
    }

    df = pd.DataFrame(sample_data)

    # Initialize engine
    engine = AnalyticsEngine(max_hr=195)

    # Run analysis
    print("Running activity analysis on sample data...")
    results = engine.analyze_activity(df)
    engine.print_analytics_report(results)

    # Demonstrate individual functions
    print("\n" + "="*60)
    print("ADDITIONAL ANALYSIS")
    print("="*60)

    # Apply rolling average to heart rate
    df = engine.apply_rolling_average(df, 'heart_rate', window=5)
    print(f"\n✅ Applied rolling average to heart rate data")
    print(f"   Original HR variance: {df['heart_rate'].var():.2f}")
    print(f"   Smoothed HR variance: {df['heart_rate_smoothed'].var():.2f}")

    print("\n✅ Analytics engine ready for integration")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
