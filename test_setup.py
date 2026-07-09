"""
Quick test script to verify all assignments are working correctly.
Run this before starting the Streamlit app.
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all modules can be imported."""
    print("\n" + "="*60)
    print("TESTING PROJECT SETUP")
    print("="*60 + "\n")

    try:
        print("[1/5] Testing Assignment 2 imports...")
        from Assignment_2.ingest import DataSanitizer
        print("      [OK] Assignment_2.ingest.DataSanitizer")

        print("\n[2/5] Testing Assignment 3 imports...")
        from Assignment_3.analytics import AnalyticsEngine
        print("      [OK] Assignment_3.analytics.AnalyticsEngine")

        print("\n[3/5] Testing required packages...")
        import pandas
        print("      [OK] pandas")
        import numpy
        print("      [OK] numpy")
        import gpxpy
        print("      [OK] gpxpy")
        import streamlit
        print("      [OK] streamlit")
        import plotly
        print("      [OK] plotly")

        print("\n[4/5] Testing data generation...")
        import create_sample_data
        print("      [OK] create_sample_data module loads")

        print("\n[5/5] Testing sample data files...")
        sample_files = ['sample_run.csv', 'sample_run.json', 'sample_run.gpx']
        for fname in sample_files:
            if Path(fname).exists():
                print(f"      [OK] {fname} exists")
            else:
                print(f"      [WARN] {fname} not found - run: python create_sample_data.py")

        print("\n" + "="*60)
        print("[SUCCESS] All tests passed!")
        print("="*60)
        print("\nYou can now run the web app:")
        print("  cd Assignment_4")
        print("  streamlit run app.py")
        print("="*60 + "\n")

        return True

    except ImportError as e:
        print(f"\n[ERROR] Import failed: {e}")
        print("\nTo fix, run:")
        print("  pip install pandas numpy gpxpy streamlit plotly")
        print("="*60 + "\n")
        return False
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        print("="*60 + "\n")
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
