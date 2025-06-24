#!/usr/bin/env python3
"""
Simple API test that bypasses LLM initialization.
"""

import requests
import time
import subprocess
import sys
import os

def create_simple_app():
    """Create a simple FastAPI app for testing."""
    from fastapi import FastAPI
    
    app = FastAPI(title="Test API")
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "message": "API is running"}
    
    @app.get("/test")
    def test_endpoint():
        return {"message": "Test endpoint working"}
    
    return app

def test_simple_api():
    """Test a simple API without LLM dependencies."""
    print("Testing simple API...")
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except Exception as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        app = create_simple_app()
        print("✅ Simple app created successfully")
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False
    
    # Start server in background
    try:
        process = subprocess.Popen([
            sys.executable, "-c", 
            "import uvicorn; from simple_api_test import create_simple_app; app = create_simple_app(); uvicorn.run(app, host='127.0.0.1', port=8001, log_level='error')"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get("http://127.0.0.1:8001/health", timeout=5)
            if response.status_code == 200:
                print("✅ Simple API server is running and responding")
                print(f"Response: {response.json()}")
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
    success = test_simple_api()
    sys.exit(0 if success else 1) 