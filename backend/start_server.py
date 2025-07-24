#!/usr/bin/env python3
"""
Startup script for the SoundCheck API server
"""

import uvicorn
import sys
import os

def main():
    """Start the FastAPI server"""
    print("Starting SoundCheck API Server...")
    print("=" * 50)
    
    # Check if model files exist
    model_dir = "models"
    required_files = [
        "hearing_classifier_logisticregression.joblib",
        "scaler.joblib", 
        "feature_names.joblib",
        "model_metadata.joblib"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(model_dir, file)):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing model files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease run 'python train_model.py' first to train the model.")
        sys.exit(1)
    
    print("✅ All model files found")
    print("🚀 Starting server on http://localhost:8000")
    print("📚 API documentation available at http://localhost:8000/docs")
    print("🔄 Server will auto-reload on code changes")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
