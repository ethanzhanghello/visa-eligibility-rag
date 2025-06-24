#!/usr/bin/env python3
"""
Launcher script for the Green Card RAG Helper UI.
"""

import subprocess
import sys
import time
import requests
import os

def check_api_server():
    """Check if the API server is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import requests
        import pandas
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

def main():
    print("🌍 Green Card RAG Helper UI Launcher")
    print("=" * 50)
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("❌ Missing dependencies. Please run: pip install -r requirements.txt")
        sys.exit(1)
    print("✅ Dependencies OK")
    
    # Check API server
    print("Checking API server...")
    if not check_api_server():
        print("❌ API server is not running!")
        print("Please start the API server first:")
        print("  uvicorn src.api.main:app --reload")
        print("\nThen run this launcher again.")
        sys.exit(1)
    print("✅ API server is running")
    
    # Launch UI
    print("Launching UI...")
    print("The UI will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the UI")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "ui/app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 UI stopped by user")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 