# Assignment 2: The Data Sanitizer

**Weeks 3-4: Data Engineering & File Ingestion**

## Overview

This assignment focuses on reading, cleaning, and organizing fitness tracker data from various formats.

## Features

- ✅ Support for CSV, JSON, and GPX file formats
- ✅ Handles missing data points gracefully (NaN values)
- ✅ Detects and reports corrupted GPS coordinates
- ✅ Converts timestamps to uniform `YYYY-MM-DD HH:MM:SS` format
- ✅ Comprehensive error handling with clean error messages
- ✅ Detailed ingestion statistics report

## Installation

```bash
cd Assignment_2
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from ingest import DataSanitizer

sanitizer = DataSanitizer()
result = sanitizer.ingest_file('your_activity_data.gpx')
sanitizer.print_report(result)
```

### Run the Demo

```bash
python ingest.py
```

## Data Formats Supported

### CSV Format
- Automatically detects timestamp and GPS columns
- Handles missing numeric values with forward/backward fill
- Removes rows with missing GPS coordinates

### JSON Format
- Supports nested JSON structures
- Handles wrapped data (e.g., `{"activities": [...]}`)
- Automatically flattens nested dictionaries

### GPX Format
- Parses track points with GPS coordinates
- Extracts elevation data
- Interpolates missing elevation values

## Output Structure

The `ingest_file()` method returns a dictionary with:

```python
{
    'status': 'success' | 'error',
    'message': 'Human-readable status message',
    'data': pandas.DataFrame | None,
    'stats': {
        'total_rows': int,
        'missing_data_points': int,
        'corrupted_data_points': int,
        'start_timestamp': 'YYYY-MM-DD HH:MM:SS',
        'end_timestamp': 'YYYY-MM-DD HH:MM:SS',
        'file_type': 'CSV' | 'JSON' | 'GPX'
    }
}
```

## Testing with Sample Data

You can download sample fitness data from:
- [Kaggle Running Dataset](https://www.kaggle.com/datasets/girardi69/running-training-log)
- [GPX Sample Files](https://www.topografix.com/gpx_resources.asp)

Place the downloaded file in the `Assignment_2` folder and run:

```bash
python ingest.py
```

## Assignment Requirements ✅

1. ✅ Reads files and outputs a cleanly structured DataFrame
2. ✅ Shows total rows processed
3. ✅ Reports missing/corrupted data points (NaN, missing GPS)
4. ✅ Converts timestamps to uniform `YYYY-MM-DD HH:MM:SS` format
5. ✅ Handles edge cases (empty files don't crash, shows clean error message)

## Next Steps

The cleaned data from this module will be used in Assignment 3 for computing performance metrics like:
- Distance calculations using the Haversine formula
- Split times and pace analysis
- Heart rate zone classification
