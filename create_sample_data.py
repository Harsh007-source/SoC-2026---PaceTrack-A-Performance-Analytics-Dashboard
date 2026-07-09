"""
Helper script to generate sample fitness tracking data for testing.
Creates CSV, JSON, and GPX files with realistic running data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path


def create_sample_csv(output_path: str = "sample_run.csv", distance_km: float = 5.0):
    """
    Create a sample CSV file with running data.

    Args:
        output_path: Path to save the CSV file
        distance_km: Total distance for the run
    """
    # Generate timestamps (1 point every 5 seconds)
    num_points = int(distance_km * 1000 / 10)  # ~10 meters per point
    start_time = datetime(2026, 1, 15, 8, 0, 0)
    timestamps = [start_time + timedelta(seconds=5*i) for i in range(num_points)]

    # Generate GPS coordinates (simulate a running route)
    start_lat, start_lon = 40.7128, -74.0060  # Starting point (NYC)
    latitudes = []
    longitudes = []

    for i in range(num_points):
        # Add some variation to make it realistic
        lat_offset = i * 0.00009 + np.random.normal(0, 0.00001)
        lon_offset = i * 0.00009 + np.random.normal(0, 0.00001)
        latitudes.append(start_lat + lat_offset)
        longitudes.append(start_lon + lon_offset)

    # Generate elevation (simulate some hills)
    elevations = 10 + 30 * np.sin(np.linspace(0, 2*np.pi, num_points)) + np.random.normal(0, 2, num_points)

    # Generate heart rate (realistic running HR)
    # Start around 100, ramp up to 150-160, then maintain
    hr_base = np.concatenate([
        np.linspace(100, 155, num_points // 4),  # Warm up
        np.random.normal(155, 8, num_points // 2),  # Steady state
        np.linspace(155, 120, num_points // 4),  # Cool down
    ])
    heart_rates = np.clip(hr_base[:num_points], 90, 180).astype(int)

    # Create DataFrame
    df = pd.DataFrame({
        'time': timestamps,
        'latitude': latitudes,
        'longitude': longitudes,
        'elevation': elevations,
        'heart_rate': heart_rates
    })

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"[OK] Created sample CSV: {output_path}")
    print(f"   - {len(df)} data points")
    print(f"   - ~{distance_km:.1f} km route")
    print(f"   - Duration: {len(df) * 5 / 60:.1f} minutes")

    return df


def create_sample_json(output_path: str = "sample_run.json", distance_km: float = 5.0):
    """
    Create a sample JSON file with running data.

    Args:
        output_path: Path to save the JSON file
        distance_km: Total distance for the run
    """
    # Generate similar data as CSV
    num_points = int(distance_km * 1000 / 10)
    start_time = datetime(2026, 1, 15, 8, 0, 0)

    activities = []

    for i in range(num_points):
        timestamp = start_time + timedelta(seconds=5*i)
        lat = 40.7128 + i * 0.00009 + np.random.normal(0, 0.00001)
        lon = -74.0060 + i * 0.00009 + np.random.normal(0, 0.00001)
        elevation = 10 + 30 * np.sin(i * 2 * np.pi / num_points) + np.random.normal(0, 2)

        # Heart rate simulation
        if i < num_points // 4:
            hr = int(100 + (i / (num_points // 4)) * 55)
        elif i > 3 * num_points // 4:
            hr = int(155 - ((i - 3*num_points//4) / (num_points // 4)) * 35)
        else:
            hr = int(np.random.normal(155, 8))

        hr = np.clip(hr, 90, 180)

        activities.append({
            'timestamp': timestamp.isoformat(),
            'location': {
                'latitude': float(lat),
                'longitude': float(lon)
            },
            'elevation': float(elevation),
            'metrics': {
                'heart_rate': int(hr)
            }
        })

    # Wrap in standard JSON structure
    data = {
        'activity_type': 'running',
        'date': start_time.strftime('%Y-%m-%d'),
        'data': activities
    }

    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"[OK] Created sample JSON: {output_path}")
    print(f"   - {len(activities)} data points")
    print(f"   - ~{distance_km:.1f} km route")

    return data


def create_sample_gpx(output_path: str = "sample_run.gpx", distance_km: float = 5.0):
    """
    Create a sample GPX file with running data.

    Args:
        output_path: Path to save the GPX file
        distance_km: Total distance for the run
    """
    num_points = int(distance_km * 1000 / 10)
    start_time = datetime(2026, 1, 15, 8, 0, 0)

    gpx_content = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="SampleDataGenerator"
     xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <name>Sample Running Activity</name>
    <time>''' + start_time.isoformat() + '''</time>
  </metadata>
  <trk>
    <name>Sample Run</name>
    <type>running</type>
    <trkseg>
'''

    for i in range(num_points):
        timestamp = start_time + timedelta(seconds=5*i)
        lat = 40.7128 + i * 0.00009 + np.random.normal(0, 0.00001)
        lon = -74.0060 + i * 0.00009 + np.random.normal(0, 0.00001)
        elevation = 10 + 30 * np.sin(i * 2 * np.pi / num_points) + np.random.normal(0, 2)

        gpx_content += f'''      <trkpt lat="{lat:.7f}" lon="{lon:.7f}">
        <ele>{elevation:.2f}</ele>
        <time>{timestamp.isoformat()}</time>
      </trkpt>
'''

    gpx_content += '''    </trkseg>
  </trk>
</gpx>'''

    # Save to GPX
    with open(output_path, 'w') as f:
        f.write(gpx_content)

    print(f"[OK] Created sample GPX: {output_path}")
    print(f"   - {num_points} track points")
    print(f"   - ~{distance_km:.1f} km route")

    return gpx_content


def create_all_samples(distance_km: float = 5.0):
    """Create all three sample file types."""
    print("\n" + "="*60)
    print("SAMPLE DATA GENERATOR")
    print("="*60 + "\n")

    # Create sample files
    create_sample_csv("sample_run.csv", distance_km)
    print()
    create_sample_json("sample_run.json", distance_km)
    print()
    create_sample_gpx("sample_run.gpx", distance_km)

    print("\n" + "="*60)
    print("[OK] All sample files created successfully!")
    print("\nYou can now use these files to test:")
    print("  - Assignment 2: python ingest.py")
    print("  - Assignment 3: python analytics.py")
    print("  - Assignment 4: streamlit run app.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate sample fitness tracking data")
    parser.add_argument(
        '--distance',
        type=float,
        default=5.0,
        help='Total distance in kilometers (default: 5.0)'
    )
    parser.add_argument(
        '--format',
        choices=['csv', 'json', 'gpx', 'all'],
        default='all',
        help='File format to generate (default: all)'
    )

    args = parser.parse_args()

    if args.format == 'all':
        create_all_samples(args.distance)
    elif args.format == 'csv':
        create_sample_csv(distance_km=args.distance)
    elif args.format == 'json':
        create_sample_json(distance_km=args.distance)
    elif args.format == 'gpx':
        create_sample_gpx(distance_km=args.distance)
