# Fitness Tracking Dashboard - Complete Project

**8-Week Frontend & Data Engineering Project**

A comprehensive fitness tracking dashboard that processes GPS and heart rate data to provide detailed athletic performance analytics.

## 📚 Project Structure

```
SoC_2026/
├── Assignment_1/          # Week 1-2: Static Frontend Shell
│   ├── index.html
│   └── Screenshot.png
│
├── Assignment_2/          # Week 3-4: Data Ingestion
│   ├── ingest.py
│   ├── requirements.txt
│   └── README.md
│
├── Assignment_3/          # Week 5-6: Analytics Engine
│   ├── analytics.py
│   ├── requirements.txt
│   └── README.md
│
├── Assignment_4/          # Week 7-8: Interactive Web App
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md             # This file
```

## 🎯 Project Overview

This project builds a complete fitness analytics pipeline through four progressive assignments:

### ✅ Assignment 1: The Static Shell
**Technologies**: HTML, CSS, TailwindCSS, Lucide Icons

A beautiful dark-themed dashboard interface with:
- Responsive sidebar with file upload placeholder
- Metric cards for distance, pace, and heart rate
- Navigation menu
- Modern, professional UI design

**[View Assignment 1 →](Assignment_1/)**

---

### ✅ Assignment 2: The Data Sanitizer
**Technologies**: Python, Pandas, GPXpy

Data ingestion module that handles:
- CSV, JSON, and GPX file formats
- Missing data detection and handling
- Timestamp normalization (YYYY-MM-DD HH:MM:SS)
- GPS coordinate validation
- Comprehensive error handling

**[View Assignment 2 →](Assignment_2/)**

---

### ✅ Assignment 3: The Analytics Engine
**Technologies**: Python, Pandas, NumPy

Core computational engine featuring:
- **Haversine formula** for accurate distance calculation
- **Dynamic split times** (pace per kilometer)
- **Heart Rate zones** (Zone 1-5 classification)
- **Rolling averages** for data smoothing
- **Elevation analysis**

**[View Assignment 3 →](Assignment_3/)**

---

### ✅ Assignment 4: The Live Launch
**Technologies**: Streamlit, Plotly, Python

Interactive web application with:
- File upload interface
- Real-time data processing
- Interactive visualizations (distance, pace, HR zones, elevation)
- Dark theme matching Assignment 1
- Responsive dashboard layout

**[View Assignment 4 →](Assignment_4/)**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or download this project**
   ```bash
   cd SoC_2026
   ```

2. **Install all dependencies**
   ```bash
   # For Assignments 2, 3, 4
   pip install pandas numpy gpxpy streamlit plotly
   ```

   Or install per assignment:
   ```bash
   cd Assignment_2
   pip install -r requirements.txt

   cd ../Assignment_3
   pip install -r requirements.txt

   cd ../Assignment_4
   pip install -r requirements.txt
   ```

### Running the Applications

#### Assignment 1 (Static HTML)
```bash
cd Assignment_1
# Open index.html in your web browser
start index.html  # Windows
# or
open index.html   # macOS
# or
xdg-open index.html  # Linux
```

#### Assignment 2 (Data Ingestion Demo)
```bash
cd Assignment_2
python ingest.py
```

#### Assignment 3 (Analytics Demo)
```bash
cd Assignment_3
python analytics.py
```

#### Assignment 4 (Full Web Application)
```bash
cd Assignment_4
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

---

## 📊 Features

### Data Processing
- ✅ Support for CSV, JSON, and GPX formats
- ✅ Automatic data cleaning and validation
- ✅ Missing data imputation
- ✅ Timestamp standardization

### Analytics
- ✅ GPS-based distance calculation (Haversine formula)
- ✅ Per-kilometer split times
- ✅ Average pace computation
- ✅ Heart rate zone analysis (5 zones)
- ✅ Elevation gain tracking
- ✅ Data smoothing (rolling averages)

### Visualization
- ✅ Interactive distance over time chart
- ✅ Split times bar chart
- ✅ Heart rate zone distribution (pie chart)
- ✅ Heart rate over time with zone markers
- ✅ Elevation profile
- ✅ Responsive metrics dashboard

---

## 📖 Learning Path

### Week 1-2: Frontend Foundations
- HTML structure and semantic markup
- CSS layout (Flexbox, Grid)
- Responsive design principles
- Dark theme implementation
- TailwindCSS utility classes

### Week 3-4: Data Engineering
- File I/O operations
- Pandas DataFrame manipulation
- Data cleaning techniques
- JSON parsing and normalization
- GPX/XML parsing
- Error handling and validation

### Week 5-6: Backend Logic
- Mathematical computations (Haversine)
- Time-series data processing
- Statistical analysis
- Algorithm implementation
- Performance optimization

### Week 7-8: Web Application Development
- Streamlit framework
- Interactive visualizations with Plotly
- State management
- User input handling
- Full-stack integration

---

## 🧪 Testing with Sample Data

### Create Sample CSV
```python
import pandas as pd

data = {
    'time': pd.date_range('2026-01-15 08:00:00', periods=50, freq='30s'),
    'latitude': [40.7128 + i*0.0001 for i in range(50)],
    'longitude': [-74.0060 + i*0.0001 for i in range(50)],
    'elevation': [10 + i*0.5 for i in range(50)],
    'heart_rate': [120 + (i % 20) for i in range(50)]
}

df = pd.DataFrame(data)
df.to_csv('sample_run.csv', index=False)
```

### Download Real Data
- **Kaggle**: [Running Training Log Dataset](https://www.kaggle.com/datasets/girardi69/running-training-log)
- **GPX Samples**: [TopGrafix GPX Resources](https://www.topografix.com/gpx_resources.asp)
- **Strava**: Export your activities as GPX

---

## 💡 Key Concepts Learned

### Frontend
- Semantic HTML5
- Modern CSS (Flexbox, Grid, Custom Properties)
- Responsive design patterns
- Component-based thinking

### Data Engineering
- Data validation and sanitization
- File format handling
- Missing data strategies
- Error handling patterns

### Algorithms & Math
- Haversine formula (great-circle distance)
- Rolling window calculations
- Time-series analysis
- Zone-based classification

### Web Development
- Streamlit reactive programming
- State management
- Interactive visualization
- User experience design

---

## 🔧 Troubleshooting

### Common Issues

**ImportError: No module named 'pandas'**
```bash
pip install pandas numpy gpxpy streamlit plotly
```

**Streamlit port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Cannot import from Assignment_2/Assignment_3**
```bash
# Make sure you're running from Assignment_4 directory
cd Assignment_4
streamlit run app.py
```

**Empty file error**
- Ensure your data file is not empty
- Check file format matches extension (.csv, .json, .gpx)

---

## 📈 Project Statistics

- **Total Lines of Code**: ~1,500+
- **Technologies Used**: 8+ (HTML, CSS, JavaScript, Python, Pandas, NumPy, Streamlit, Plotly)
- **File Formats Supported**: 3 (CSV, JSON, GPX)
- **Visualization Types**: 5 (Line, Bar, Pie, Scatter, Area)
- **Core Algorithms**: 4 (Haversine, Split Times, HR Zones, Rolling Average)

---

## 🎓 Skills Demonstrated

### Technical Skills
- Frontend development (HTML/CSS)
- Python programming
- Data manipulation (Pandas)
- Mathematical computations (NumPy)
- Web framework (Streamlit)
- Data visualization (Plotly)
- File I/O and parsing
- Error handling

### Software Engineering
- Modular code design
- Clean code principles
- Documentation
- Version control (implied)
- Testing and validation
- User experience focus

### Domain Knowledge
- GPS coordinate systems
- Heart rate training zones
- Fitness metrics and pace calculations
- Geospatial distance algorithms

---

## 🚀 Future Enhancements

Potential extensions for continued learning:

### Features
- [ ] Multiple activity comparison
- [ ] Training plan recommendations
- [ ] Export processed data
- [ ] Activity history and trends
- [ ] Goal setting and tracking
- [ ] Social sharing

### Technical
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication
- [ ] API integration (Strava, Garmin)
- [ ] Real-time GPS tracking
- [ ] Mobile app (React Native)
- [ ] Cloud deployment (AWS, Azure, GCP)

### Analytics
- [ ] Machine learning predictions
- [ ] Anomaly detection
- [ ] Performance trends
- [ ] Recovery recommendations
- [ ] Injury risk assessment

---

## 📚 Resources & References

### Documentation
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [GPXpy Documentation](https://github.com/tkrajina/gpxpy)

### Learning Resources
- [MDN Web Docs (HTML/CSS)](https://developer.mozilla.org/)
- [TailwindCSS](https://tailwindcss.com/docs)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

### Datasets
- [Kaggle Fitness Datasets](https://www.kaggle.com/datasets?search=running)
- [GPX Sample Files](https://www.topografix.com/gpx_resources.asp)

---

## 📝 Assignment Checklist

### Assignment 1: The Static Shell ✅
- [x] Dark-mode theme
- [x] Sidebar with file upload
- [x] Three metric cards (Distance, Pace, HR)
- [x] Responsive layout
- [x] Clean component structure

### Assignment 2: The Data Sanitizer ✅
- [x] Read CSV, JSON, GPX files
- [x] Output clean DataFrame
- [x] Report total rows processed
- [x] Handle missing/corrupted data
- [x] Uniform timestamp format (YYYY-MM-DD HH:MM:SS)
- [x] Graceful error handling

### Assignment 3: The Analytics Engine ✅
- [x] Cumulative distance (Haversine formula)
- [x] Dynamic split times per kilometer
- [x] Heart Rate zones (Zone 1-5)
- [x] Clean JSON/dict output
- [x] Accurate floating-point calculations

### Assignment 4: The Live Launch ✅
- [x] Streamlit file uploader
- [x] Load and process uploaded data
- [x] Display comprehensive metrics
- [x] Interactive visualizations
- [x] Dark theme UI
- [x] Error handling (no crashes on empty files)

---

## 👨‍💻 Author

**Project**: Fitness Tracking Dashboard  
**Timeline**: 8 Weeks (Completed)  
**Technologies**: Python, Streamlit, Pandas, NumPy, Plotly, HTML, CSS

---

## 📜 License

This project is created for educational purposes as part of the SoC 2026 program.

---

## 🎉 Congratulations!

You've successfully built a complete fitness analytics pipeline from scratch, covering:
- ✅ Frontend design and development
- ✅ Data engineering and ETL
- ✅ Backend algorithms and analytics
- ✅ Full-stack web application deployment

This project demonstrates real-world software engineering skills applicable to:
- Data science roles
- Full-stack development positions
- Sports analytics companies
- Health tech startups
- Wearable technology firms

**Keep building!** 🚀
