# SoundCheck Backend API

FastAPI-based REST API server for the SoundCheck hearing test application. Handles audio generation, machine learning analysis, and real-time hearing assessment processing.

## Overview

The backend serves as the core processing engine for hearing tests, providing:
- Pure tone audio generation for frequency testing
- ML-powered hearing loss classification
- Real-time analysis with confidence scoring
- Privacy-focused local data processing

## Architecture

```
Client Request → FastAPI Router → Business Logic → ML Model → JSON Response
```

### Core Components
- **FastAPI Application** (main.py): REST API server with automatic documentation
- **ML Model** (utils.py): Logistic regression classifier for hearing loss analysis
- **Data Models** (models.py): Pydantic schemas for request/response validation
- **Server Startup** (start_server.py): Uvicorn server configuration

## Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Quick Start
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python start_server.py
```

### Verification
- Server: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Reference

### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "SoundCheck API is running",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Generate Audio
```http
POST /generate-audio
Content-Type: application/json

{
  "frequency": 1000,
  "duration": 3.0,
  "sample_rate": 22050
}
```
**Response:** Binary audio data (WAV format)

### Analyze Hearing
```http
POST /analyze-hearing
Content-Type: application/json

{
  "responses": [
    {"frequency": 500, "heard": true},
    {"frequency": 1000, "heard": true},
    {"frequency": 2000, "heard": false}
  ],
  "age": 35,
  "gender": "Male"
}
```
**Response:**
```json
{
  "category": "Mild Hearing Loss",
  "confidence_score": 0.85,
  "risk_level": "Low",
  "pta_score": 25.5,
  "recommendations": ["Consider follow-up with audiologist"]
}
```

## Machine Learning Model

### Model Specifications
- **Algorithm**: Logistic Regression with L2 regularization
- **Training Data**: Audiometric patterns from clinical datasets
- **Features**: Frequency response patterns, demographic data
- **Performance**: 99%+ accuracy on validation set

### Classification Categories
1. **Normal Hearing** (0-25 dB HL)
2. **Mild Hearing Loss** (26-40 dB HL)
3. **Moderate Hearing Loss** (41-70 dB HL)
4. **Severe Hearing Loss** (71+ dB HL)

## Development

### Development Server
```bash
# Start with auto-reload
python start_server.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with interactive docs
# Visit http://localhost:8000/docs
```

### Code Structure
```
backend/
├── main.py                 # FastAPI application and routes
├── models.py              # Pydantic data models
├── utils.py               # ML model and utility functions
├── start_server.py        # Server startup configuration
├── requirements.txt       # Python dependencies
└── hearing_loss_model.pkl # Trained ML model file
```

## Configuration

### Server Settings
```python
# start_server.py
HOST = "0.0.0.0"
PORT = 8000
RELOAD = True  # Development only
```

### Model Parameters
```python
# utils.py
SAMPLE_RATE = 22050
TONE_DURATION = 3.0
CONFIDENCE_THRESHOLD = 0.7
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

3. **Model Loading Error**
   - Ensure hearing_loss_model.pkl exists
   - Check file permissions
   - Verify scikit-learn version compatibility

### Performance
- Lightweight ML model for real-time processing
- Efficient audio generation algorithms
- Fast response times (<100ms typical)

## Security & Privacy
- No persistent data storage
- All processing happens in memory
- Local-only ML model inference
- Input validation with Pydantic models

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
