# Assignment 4: The Live Launch

**Weeks 7-8: Interactive Visualization**

## Overview

This assignment deploys a fully functional, interactive web application that combines data ingestion (Assignment 2) and analytics (Assignment 3) into a beautiful, dark-themed fitness tracking dashboard.

## Features

- ✅ **File Upload**: Drag-and-drop interface for CSV, JSON, and GPX files
- ✅ **Real-time Processing**: Instant data sanitization and analytics
- ✅ **Interactive Charts**: Plotly visualizations with zoom, pan, and hover
- ✅ **Dark Theme**: Matches the static shell from Assignment 1
- ✅ **Responsive Layout**: Works on desktop and mobile
- ✅ **Comprehensive Metrics**: Distance, pace, HR zones, elevation

## Installation

```bash
cd Assignment_4
pip install -r requirements.txt
```

## Running the Application

### Start the Streamlit server:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Alternative command:

```bash
python -m streamlit run app.py
```

## Application Structure

```
Assignment_4/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Features Breakdown

### 📁 File Upload
- Supports CSV, JSON, and GPX formats
- Drag-and-drop interface
- Automatic file type detection
- Error handling for empty or corrupted files

### 📊 Dashboard Metrics
Real-time metrics cards showing:
- Total distance (km)
- Average pace (min:sec/km)
- Average heart rate (bpm)
- Total activity time

### 📈 Interactive Visualizations

1. **Cumulative Distance Over Time**
   - Line chart with fill
   - Shows distance progression throughout activity

2. **Split Times by Kilometer**
   - Color-coded bar chart
   - Displays pace for each kilometer
   - Hover for detailed information

3. **Heart Rate Over Time**
   - Raw and smoothed HR data
   - Zone reference lines
   - Rolling average visualization

4. **Heart Rate Zone Distribution**
   - Pie chart showing time in each zone
   - Color-coded by intensity
   - Percentage and time breakdown

5. **Elevation Profile**
   - Shows terrain changes
   - Distance vs elevation plot

### ⚙️ Settings
- Configurable maximum heart rate
- Adjusts HR zone calculations dynamically

### 📋 Data Quality Report
- Total rows processed
- Missing data points
- Corrupted data points
- Time range of activity

### 🔍 Raw Data Viewer
- Expandable section with full dataset
- Searchable and sortable table

## Integration with Previous Assignments

The application seamlessly integrates:

```python
# Assignment 2: Data Ingestion
from Assignment_2.ingest import DataSanitizer

# Assignment 3: Analytics
from Assignment_3.analytics import AnalyticsEngine

# Workflow:
# 1. User uploads file
# 2. DataSanitizer processes and cleans data
# 3. AnalyticsEngine computes metrics
# 4. Streamlit displays results interactively
```

## UI/UX Design

### Color Palette (Dark Theme)
- **Background**: `#0f172a` (slate-950)
- **Cards**: `#1e293b` (slate-900)
- **Borders**: `#334155` (slate-800)
- **Text**: `#f1f5f9` (slate-50)
- **Accent**: `#3b82f6` (blue-500)

### Typography
- **Headings**: Bold, tracking-tight
- **Metrics**: Extra-bold, large font
- **Labels**: Uppercase, letter-spacing

## Usage Example

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Upload your fitness data**:
   - Click "Browse files" in the sidebar
   - Select a `.csv`, `.json`, or `.gpx` file

3. **Process the data**:
   - Click "🔄 Process Data" button
   - Wait for sanitization and analytics

4. **Explore your metrics**:
   - View key metrics at the top
   - Scroll through interactive charts
   - Check data quality report
   - Inspect raw data

## Sample Data

For testing, you can:
1. Use the demo data generator from Assignment 2
2. Download sample GPX files from [GPX Resources](https://www.topografix.com/gpx_resources.asp)
3. Export data from fitness apps (Strava, Garmin Connect, etc.)

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Import Errors
Make sure you're running from the `Assignment_4` directory, or the parent directories are in your Python path.

## Assignment Requirements ✅

1. ✅ Loads model/analytics engine successfully
2. ✅ File uploader for activity data
3. ✅ Backend resizes/processes uploaded data
4. ✅ Displays comprehensive metrics with confidence
5. ✅ Clean, dark-themed UI matching Assignment 1
6. ✅ Error handling prevents crashes on empty files

## Performance Optimizations

- Session state caching for processed data
- Lazy loading of visualizations
- Efficient data processing with pandas
- Plotly's GPU-accelerated rendering

## Future Enhancements

Possible improvements for extended learning:
- Export processed data as CSV/JSON
- Compare multiple activities
- Training plan recommendations
- Integration with fitness APIs (Strava, Garmin)
- User authentication and data persistence
- Mobile-responsive improvements
- Real-time GPS tracking

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repository and deploy

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)

---

**Congratulations!** You've completed the full pipeline from static UI → data processing → analytics → live web app! 🎉
