# SoundCheck Backend - ML-Powered Hearing Test API

This is the backend API for the SoundCheck hearing test application, built for the hackathon challenge. It provides ML-powered hearing loss classification based on NHANES audiometry data.

## Features

- **ML-Powered Analysis**: Uses trained scikit-learn models (Logistic Regression, Random Forest, Decision Tree) for hearing loss classification
- **Audio Generation**: Generates pure-tone audio files for hearing testing
- **RESTful API**: FastAPI-based REST API with automatic documentation
- **Real-time Processing**: Analyzes hearing test results in real-time
- **WHO Classification**: Uses WHO hearing loss categories (Normal, Mild, Moderate, Severe, Profound)
- **Health Recommendations**: Provides personalized recommendations based on results

## Project Structure

```
backend/
├── main.py                 # FastAPI application
├── models.py              # Pydantic data models
├── utils.py               # Utility functions and ML model management
├── train_model.py         # ML model training script
├── test_api.py           # API testing script
├── start_server.py       # Server startup script
├── requirements.txt      # Python dependencies
├── AUX_J.xpt            # NHANES audiometry dataset
├── models/              # Trained ML models directory
│   ├── hearing_classifier_logisticregression.joblib
│   ├── scaler.joblib
│   ├── feature_names.joblib
│   └── model_metadata.joblib
└── venv/               # Python virtual environment
```

## Setup Instructions

### 1. Prerequisites
- Python 3.12
- Virtual environment (venv)

### 2. Installation

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (already done)
pip install -r requirements.txt

# Train the ML model (already done)
python train_model.py
```

### 3. Start the Server

```bash
# Method 1: Using the startup script
python start_server.py

# Method 2: Direct uvicorn command
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with basic info
- `GET /health` - Health check and system status
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Model Information

- `GET /model/info` - Get ML model information and metadata

### Audio Generation

- `POST /audio/generate` - Generate pure-tone audio for testing
  ```json
  {
    "frequency": 1000,
    "duration": 1.0,
    "volume": 0.5,
    "sample_rate": 44100
  }
  ```

### Hearing Test Analysis

- `POST /test/analyze` - Analyze hearing test results
  ```json
  {
    "user_info": {
      "age": 35,
      "gender": "Male"
    },
    "frequency_responses": [
      {"frequency": 500, "heard": true},
      {"frequency": 1000, "heard": true},
      {"frequency": 2000, "heard": false}
    ]
  }
  ```

### Reference Data

- `GET /test/frequencies` - Get standard audiometric frequencies
- `GET /categories` - Get hearing loss categories and descriptions

## ML Model Details

### Training Data
- **Source**: NHANES Audiometry Dataset (AUX_J.xpt)
- **Records**: 2,520 clean records after preprocessing
- **Features**: 7 frequency thresholds (500Hz - 8000Hz)
- **Target**: WHO hearing loss categories

### Model Performance
- **Best Model**: Logistic Regression
- **Accuracy**: 99.01%
- **Features**: Average hearing thresholds across left/right ears
- **Preprocessing**: StandardScaler for feature normalization

### Classification Categories
- **Normal**: ≤ 25 dB HL
- **Mild**: 26-40 dB HL  
- **Moderate**: 41-60 dB HL
- **Severe**: 61-80 dB HL
- **Profound**: > 80 dB HL

## Technical Stack

- **Framework**: FastAPI 0.116.1
- **ML Library**: scikit-learn 1.7.1
- **Data Processing**: pandas 2.3.1, numpy 2.3.1
- **Audio Processing**: pydub 0.25.1, scipy 1.16.0
- **Data Loading**: pyreadstat 1.3.0 (for NHANES .xpt files)
- **Server**: uvicorn 0.35.0

## Development

### Code Structure

- **main.py**: FastAPI application with all endpoints
- **models.py**: Pydantic models for request/response validation
- **utils.py**: Core business logic including:
  - `ModelManager`: ML model loading and prediction
  - `AudioGenerator`: Pure-tone audio generation
  - `HearingAnalyzer`: Hearing test analysis and recommendations

### Adding New Features

1. Add new Pydantic models to `models.py`
2. Implement business logic in `utils.py`
3. Add new endpoints to `main.py`
4. Update tests in `test_api.py`

## Deployment

The backend is designed to be easily deployable to:
- **Local Development**: `python start_server.py`
- **Docker**: Can be containerized with a simple Dockerfile
- **Cloud Platforms**: Heroku, Railway, Render, etc.
- **Serverless**: Can be adapted for AWS Lambda, Vercel, etc.

## Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

Tests cover:
- Health checks
- Model loading
- Audio generation
- Hearing test analysis
- All API endpoints

## Notes

- This is a **screening tool**, not a diagnostic medical device
- Results should not replace professional audiological evaluation
- The model is trained on NHANES data and may not generalize to all populations
- Audio testing requires proper headphones/speakers for accurate results

## Hackathon Compliance

✅ **No LLM APIs**: Uses only scikit-learn models trained from scratch  
✅ **Own ML Models**: Trained on NHANES audiometry data  
✅ **Transparent**: All code and training process is open source  
✅ **Functional**: Complete working API with audio generation and analysis  
✅ **Real Problem**: Addresses early hearing loss detection and awareness
