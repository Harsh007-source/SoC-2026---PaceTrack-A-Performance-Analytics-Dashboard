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

