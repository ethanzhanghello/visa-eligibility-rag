#!/usr/bin/env python3
"""
Startup script for Green Card RAG Helper UI
"""
import subprocess
import sys
import time
import requests
import os

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🌍 Green Card RAG Helper - UI Startup")
    print("=" * 50)
    
    # Check if API is running
    print("🔍 Checking API server...")
    if not check_api_health():
        print("❌ API server is not running!")
        print("\nPlease start the API server first:")
        print("   python3 start_server.py")
        print("\nThen run this UI again.")
        return
    
    print("✅ API server is running")
    
    # Check if streamlit is available
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found!")
        print("\nPlease install streamlit:")
        print("   pip install streamlit")
        return
    
    # Start the UI
    print("\n🚀 Starting UI...")
    print("📱 UI will be available at: http://localhost:8501")
    print("🔗 API is available at: http://localhost:8000")
    print("\nPress Ctrl+C to stop the UI")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "simple_ui.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 UI stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting UI: {e}")

if __name__ == "__main__":
    main() 