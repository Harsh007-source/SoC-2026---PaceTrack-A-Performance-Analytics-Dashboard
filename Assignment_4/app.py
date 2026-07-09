"""
Assignment 4: The Live Launch
Weeks 7-8: Interactive Visualization

Streamlit web application that combines data ingestion and analytics
into an interactive fitness tracking dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add parent directories to path to import previous assignments
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Assignment_2.ingest import DataSanitizer
from Assignment_3.analytics import AnalyticsEngine


# Page configuration
st.set_page_config(
    page_title="PulseAnalytics - Fitness Dashboard",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme matching Assignment 1
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .stMetric label {
        color: #94a3b8 !important;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-size: 2rem;
        font-weight: 800;
    }
    h1 {
        color: #f1f5f9;
        font-weight: 800;
    }
    h2, h3 {
        color: #f1f5f9;
    }
    .uploadedFile {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'sanitizer_result' not in st.session_state:
        st.session_state.sanitizer_result = None
    if 'analytics_result' not in st.session_state:
        st.session_state.analytics_result = None


def plot_distance_over_time(df: pd.DataFrame):
    """Create interactive distance over time plot."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['cumulative_distance'],
        mode='lines',
        name='Distance',
        line=dict(color='#3b82f6', width=3),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))

    fig.update_layout(
        title="Cumulative Distance Over Time",
        xaxis_title="Time Point",
        yaxis_title="Distance (km)",
        template="plotly_dark",
        hovermode='x unified',
        height=400
    )

    return fig


def plot_split_times(splits: list):
    """Create bar chart for kilometer split times."""
    kms = [s['kilometer'] for s in splits]
    pace_seconds = [s['pace_seconds'] for s in splits]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=kms,
        y=pace_seconds,
        text=[s['pace'] for s in splits],
        textposition='auto',
        marker=dict(
            color=pace_seconds,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Seconds")
        ),
        hovertemplate='<b>KM %{x}</b><br>Pace: %{text}/km<extra></extra>'
    ))

    fig.update_layout(
        title="Split Times by Kilometer",
        xaxis_title="Kilometer",
        yaxis_title="Pace (seconds)",
        template="plotly_dark",
        height=400
    )

    return fig


def plot_heart_rate_zones(hr_zones: dict):
    """Create pie chart for heart rate zones."""
    zones = list(hr_zones.keys())
    percentages = [hr_zones[zone]['percentage'] for zone in zones]

    colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6']

    fig = go.Figure(data=[go.Pie(
        labels=zones,
        values=percentages,
        hole=.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<br>%{text}<extra></extra>',
        text=[hr_zones[zone]['time_formatted'] for zone in zones]
    )])

    fig.update_layout(
        title="Heart Rate Zone Distribution",
        template="plotly_dark",
        height=400
    )

    return fig


def plot_heart_rate_over_time(df: pd.DataFrame):
    """Create heart rate over time plot with smoothed line."""
    fig = go.Figure()

    # Raw heart rate
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['heart_rate'],
        mode='lines',
        name='Raw HR',
        line=dict(color='#ef4444', width=1),
        opacity=0.3
    ))

    # Smoothed heart rate if available
    if 'heart_rate_smoothed' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['heart_rate_smoothed'],
            mode='lines',
            name='Smoothed HR',
            line=dict(color='#ef4444', width=3)
        ))

    # Add zone reference lines
    engine = AnalyticsEngine()
    for zone_name, (min_hr, max_hr) in engine.HR_ZONES.items():
        fig.add_hline(
            y=min_hr,
            line_dash="dash",
            line_color="gray",
            opacity=0.3,
            annotation_text=zone_name,
            annotation_position="right"
        )

    fig.update_layout(
        title="Heart Rate Over Time",
        xaxis_title="Time Point",
        yaxis_title="Heart Rate (bpm)",
        template="plotly_dark",
        hovermode='x unified',
        height=400
    )

    return fig


def plot_elevation_profile(df: pd.DataFrame):
    """Create elevation profile plot."""
    if 'elevation' not in df.columns or 'cumulative_distance' not in df.columns:
        return None

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['cumulative_distance'],
        y=df['elevation'],
        mode='lines',
        name='Elevation',
        line=dict(color='#10b981', width=2),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))

    fig.update_layout(
        title="Elevation Profile",
        xaxis_title="Distance (km)",
        yaxis_title="Elevation (m)",
        template="plotly_dark",
        hovermode='x unified',
        height=400
    )

    return fig


def main():
    """Main Streamlit application."""
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### 🏃 PulseAnalytics")
        st.markdown("**The Live Launch** - Assignment 4")
        st.markdown("---")

        st.markdown("#### Import Data")
        uploaded_file = st.file_uploader(
            "Upload your fitness data",
            type=['csv', 'json', 'gpx'],
            help="Supported formats: CSV, JSON, GPX"
        )

        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = Path(f"temp_{uploaded_file.name}")
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            if st.button("🔄 Process Data", type="primary"):
                with st.spinner("Processing file..."):
                    # Data sanitization
                    sanitizer = DataSanitizer()
                    sanitizer_result = sanitizer.ingest_file(temp_path)
                    st.session_state.sanitizer_result = sanitizer_result

                    if sanitizer_result['status'] == 'success':
                        st.session_state.data = sanitizer_result['data']

                        # Analytics
                        engine = AnalyticsEngine(max_hr=195)
                        analytics_result = engine.analyze_activity(st.session_state.data)
                        st.session_state.analytics_result = analytics_result

                        # Apply rolling average
                        if 'heart_rate' in st.session_state.data.columns:
                            st.session_state.data = engine.apply_rolling_average(
                                st.session_state.data,
                                'heart_rate',
                                window=5
                            )

                        st.success("✅ Data processed successfully!")
                    else:
                        st.error(f"❌ {sanitizer_result['message']}")

                # Clean up temp file
                temp_path.unlink(missing_ok=True)

        st.markdown("---")
        st.markdown("#### Settings")
        max_hr = st.number_input(
            "Max Heart Rate",
            min_value=150,
            max_value=220,
            value=195,
            help="Enter your maximum heart rate (220 - age)"
        )

        st.markdown("---")
        st.markdown("#### Navigation")
        st.markdown("📊 Dashboard")
        st.markdown("📈 History *(coming soon)*")
        st.markdown("⚙️ Settings *(coming soon)*")

    # Main content
    st.title("🏃 Performance Overview")

    if st.session_state.data is None:
        # Welcome screen
        st.markdown("""
        ### Welcome to PulseAnalytics!

        Upload your fitness tracking data to get started:
        - 📁 Supported formats: **CSV, JSON, GPX**
        - 📊 View comprehensive analytics
        - 📈 Interactive visualizations
        - ❤️ Heart rate zone analysis

        Use the sidebar to upload your file and begin analysis.
        """)

        # Show example metrics (static shell from Assignment 1)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Total Distance",
                value="42.2 km",
                delta="+12% from last week"
            )

        with col2:
            st.metric(
                label="Average Pace",
                value="5:24 /km",
                delta="-0:15 seconds"
            )

        with col3:
            st.metric(
                label="Heart Rate",
                value="142 bpm",
                delta="Steady baseline"
            )

        st.info("👆 Upload a file to see your real data here!")

    else:
        # Display processed data
        stats = st.session_state.sanitizer_result['stats']
        metrics = st.session_state.analytics_result['metrics']

        # Data quality indicators
        st.markdown(f"**Status:** ✅ Frontend Engine Ready | **File Type:** {stats['file_type']} | **Data Points:** {stats['total_rows']}")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if 'total_distance_km' in metrics:
                st.metric(
                    label="Total Distance",
                    value=f"{metrics['total_distance_km']} km"
                )
            else:
                st.metric(label="Total Distance", value="N/A")

        with col2:
            if 'overall_pace' in metrics:
                st.metric(
                    label="Average Pace",
                    value=f"{metrics['overall_pace']} /km"
                )
            else:
                st.metric(label="Average Pace", value="N/A")

        with col3:
            if 'avg_heart_rate' in metrics:
                st.metric(
                    label="Avg Heart Rate",
                    value=f"{metrics['avg_heart_rate']} bpm"
                )
            else:
                st.metric(label="Avg Heart Rate", value="N/A")

        with col4:
            if 'total_time' in metrics:
                st.metric(
                    label="Total Time",
                    value=metrics['total_time']
                )
            else:
                st.metric(label="Total Time", value="N/A")

        # Visualizations
        st.markdown("---")

        # Distance and elevation
        if 'cumulative_distance' in st.session_state.data.columns:
            col1, col2 = st.columns(2)

            with col1:
                fig_distance = plot_distance_over_time(st.session_state.data)
                st.plotly_chart(fig_distance, use_container_width=True)

            with col2:
                fig_elevation = plot_elevation_profile(st.session_state.data)
                if fig_elevation:
                    st.plotly_chart(fig_elevation, use_container_width=True)
                else:
                    st.info("No elevation data available")

        # Split times
        if 'split_times' in metrics:
            st.markdown("### ⏱️ Split Times Analysis")
            fig_splits = plot_split_times(metrics['split_times'])
            st.plotly_chart(fig_splits, use_container_width=True)

            # Split times table
            with st.expander("📋 View Detailed Split Times"):
                splits_df = pd.DataFrame(metrics['split_times'])
                st.dataframe(splits_df, use_container_width=True)

        # Heart rate analysis
        if 'heart_rate' in st.session_state.data.columns:
            st.markdown("### ❤️ Heart Rate Analysis")

            col1, col2 = st.columns(2)

            with col1:
                fig_hr = plot_heart_rate_over_time(st.session_state.data)
                st.plotly_chart(fig_hr, use_container_width=True)

            with col2:
                if 'hr_zones' in metrics:
                    fig_hr_zones = plot_heart_rate_zones(metrics['hr_zones'])
                    st.plotly_chart(fig_hr_zones, use_container_width=True)

        # Data quality report
        with st.expander("📊 Data Quality Report"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Rows Processed", stats['total_rows'])

            with col2:
                st.metric("Missing Data Points", stats['missing_data_points'])

            with col3:
                st.metric("Corrupted Data Points", stats['corrupted_data_points'])

            if stats['start_timestamp'] and stats['end_timestamp']:
                st.markdown(f"**Time Range:** {stats['start_timestamp']} to {stats['end_timestamp']}")

        # Raw data viewer
        with st.expander("🔍 View Raw Data"):
            st.dataframe(st.session_state.data, use_container_width=True)


if __name__ == "__main__":
    main()
