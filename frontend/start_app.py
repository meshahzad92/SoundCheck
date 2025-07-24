#!/usr/bin/env python3
"""
Startup script for the SoundCheck Streamlit Frontend
"""

import subprocess
import sys
import os
import requests
import time

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Start the Streamlit application"""
    print("Starting SoundCheck Frontend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the frontend directory.")
        sys.exit(1)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected.")
        print("   Consider activating the virtual environment: source venv/bin/activate")
    
    # Check backend connection
    print("🔍 Checking backend connection...")
    if check_backend():
        print("✅ Backend is running and healthy")
    else:
        print("⚠️  Backend not detected at http://localhost:8000")
        print("   Please start the backend server first:")
        print("   cd ../backend && python start_server.py")
        print("\n   The frontend will still start, but functionality will be limited.")
        
        # Wait a moment for user to read
        time.sleep(3)
    
    print("\n🚀 Starting Streamlit application...")
    print("📱 Frontend will be available at: http://localhost:8501")
    print("🔄 Application will auto-reload on code changes")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([
            "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except FileNotFoundError:
        print("❌ Error: Streamlit not found. Please install it:")
        print("   pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
