#!/usr/bin/env python3
"""
Simple test script to verify the API can start and run.
"""

import requests
import time
import subprocess
import sys
import os

def test_api_startup():
    """Test if the API can start and respond."""
    print("Testing API startup...")
    
    # Try to import the app
    try:
        from src.api.main import app
        print("✅ API imports successfully")
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False
    
    # Try to start the server
    try:
        import uvicorn
        print("Starting server...")
        
        # Start server in background
        process = subprocess.Popen([
            sys.executable, "-c", 
            "import uvicorn; from src.api.main import app; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error')"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ API server is running and responding")
                process.terminate()
                return True
            else:
                print(f"❌ API responded with status {response.status_code}")
                process.terminate()
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ API server not responding: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

if __name__ == "__main__":
    success = test_api_startup()
    sys.exit(0 if success else 1) 