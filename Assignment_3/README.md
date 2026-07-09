# Assignment 3: The Analytics Engine

**Weeks 5-6: Backend Logic & Performance Metrics Computation**

## Overview

This assignment builds the computational core that transforms raw GPS and heart rate data into meaningful athletic performance metrics.

## Features

- ✅ **Distance Calculation**: Haversine formula for accurate GPS-based distance
- ✅ **Split Times**: Dynamic pace calculation per kilometer
- ✅ **Heart Rate Zones**: Classify time spent in Zones 1-5
- ✅ **Pace Calculations**: Convert time/distance to min:sec per km
- ✅ **Rolling Averages**: Smooth noisy GPS and HR data
- ✅ **Elevation Analysis**: Calculate total elevation gain

## Installation

```bash
cd Assignment_3
pip install -r requirements.txt
```

## Usage

### Basic Analysis

```python
from analytics import AnalyticsEngine
import pandas as pd

# Initialize engine (adjust max_hr for your age: 220 - age)
engine = AnalyticsEngine(max_hr=195)

# Load your data (from Assignment 2)
df = pd.read_csv('your_activity_data.csv')

# Run complete analysis
results = engine.analyze_activity(df)
engine.print_analytics_report(results)
```

### Individual Metric Calculations

```python
# Calculate cumulative distance
df = engine.calculate_cumulative_distance(df)
print(f"Total distance: {df.iloc[-1]['cumulative_distance']:.2f} km")

# Get split times
splits = engine.calculate_split_times(df)
for split in splits:
    print(f"KM {split['kilometer']}: {split['pace']} /km")

# Analyze heart rate zones
hr_zones = engine.calculate_hr_zones(df)
for zone, data in hr_zones.items():
    print(f"{zone}: {data['time_formatted']} ({data['percentage']}%)")

# Smooth noisy data
df = engine.apply_rolling_average(df, 'heart_rate', window=5)
```

### Run the Demo

```bash
python analytics.py
```

## Mathematical Implementations

### 1. Haversine Formula

Calculates great-circle distance between two GPS coordinates:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1-a))
distance = R × c
```

Where R = 6371 km (Earth's radius)

### 2. Pace Calculation

```
pace (min/km) = total_time_seconds / distance_km / 60
```

### 3. Heart Rate Zones

Based on percentage of maximum heart rate (220 - age):

- **Zone 1 (Recovery)**: 50-60% of max HR
- **Zone 2 (Aerobic)**: 60-70% of max HR
- **Zone 3 (Tempo)**: 70-80% of max HR
- **Zone 4 (Threshold)**: 80-90% of max HR
- **Zone 5 (Maximum)**: 90-100% of max HR

### 4. Rolling Average

Smooths noisy data using a sliding window:

```python
smoothed_value[i] = mean(values[i-window:i+window])
```

## Output Structure

The `analyze_activity()` method returns:

```python
{
    'status': 'success' | 'error',
    'metrics': {
        'total_distance_km': float,
        'total_time': 'HH:MM:SS',
        'overall_pace': 'M:SS',
        'split_times': [
            {
                'kilometer': int,
                'time': 'HH:MM:SS',
                'pace': 'M:SS',
                'pace_seconds': float
            },
            ...
        ],
        'hr_zones': {
            'Zone 1': {
                'time_seconds': float,
                'time_formatted': 'MM:SS',
                'percentage': float,
                'hr_range': 'min-max bpm'
            },
            ...
        },
        'avg_heart_rate': float,
        'max_heart_rate': int,
        'min_heart_rate': int,
        'elevation_gain_m': float
    }
}
```

## Validation Against Marathon Splits

The calculations are designed to match real-world marathon performance. For example:

- **42.195 km** in **3:48:00** = **5:24 /km** average pace ✅
- Individual km splits match cumulative time accurately
- Floating-point precision ensures no rounding errors accumulate

## Integration with Previous Assignments

```python
# Complete pipeline from Assignment 2 → Assignment 3
from Assignment_2.ingest import DataSanitizer
from Assignment_3.analytics import AnalyticsEngine

# Step 1: Ingest data
sanitizer = DataSanitizer()
result = sanitizer.ingest_file('activity.gpx')

# Step 2: Analyze metrics
engine = AnalyticsEngine()
analysis = engine.analyze_activity(result['data'])
engine.print_analytics_report(analysis)
```

## Assignment Requirements ✅

1. ✅ Cumulative distance computed using Haversine formula
2. ✅ Dynamic split times (pace per kilometer)
3. ✅ Heart Rate zones breakdown (Zone 1-5 classification)
4. ✅ Clean JSON/dictionary output (no visualization needed)
5. ✅ Floating-point calculations match marathon splits

## Next Steps

The computed metrics will be visualized in Assignment 4 using interactive charts and a web interface with Streamlit.
