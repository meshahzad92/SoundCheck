# SoundCheck - ML-Powered Hearing Test Application

SoundCheck is a comprehensive hearing assessment application that combines machine learning analysis with an intuitive web interface. The system provides professional-grade hearing tests, real-time analysis, and educational hearing loss simulation.

## Project Overview

### Architecture
The application follows a client-server architecture:
- **Backend**: FastAPI-based REST API server handling audio processing and ML analysis
- **Frontend**: Streamlit web application providing the user interface
- **ML Model**: Logistic regression model trained on audiometric data for hearing loss classification

### Key Features
- Professional hearing test with multiple frequency assessment (500Hz - 8000Hz)
- Real-time ML-powered analysis with confidence scoring
- Hearing loss simulation for educational purposes
- Downloadable test reports
- Privacy-focused design (all data processing is local)

## Quick Start

### Prerequisites
- Python 3.12 or higher
- Virtual environment (recommended)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SoundCheck
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Start the backend server**
   ```bash
   cd backend
   python main.py
   ```
   The backend will be available at `http://localhost:8000`

5. **Start the frontend application** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py --server.port 8502
   ```
   The frontend will be available at `http://localhost:8502`

## Application Flow

### 1. User Journey
```
Home Page → Start Test → Frequency Testing → ML Analysis → Results → Download Report
     ↓
Hearing Loss Simulator (Educational Feature)
```

### 2. Technical Flow
```
Frontend (Streamlit) → API Calls → Backend (FastAPI) → ML Model → Response → Frontend Display
```

### 3. Test Process
1. **User Information**: Age and gender collection for personalized analysis
2. **Frequency Testing**: Sequential testing of 6 frequencies (500Hz, 1000Hz, 2000Hz, 3000Hz, 4000Hz, 8000Hz)
3. **Audio Generation**: Backend generates calibrated pure tones
4. **Response Collection**: User indicates whether they can hear each frequency
5. **ML Analysis**: Logistic regression model analyzes response patterns
6. **Results Generation**: Classification, confidence score, and recommendations

## Project Structure

```
SoundCheck/
├── README.md                 # This file
├── train_model.ipynb          # Model training
├── backend/                 # Backend API server
│   ├── README.md           # Backend-specific documentation
│   ├── requirements.txt    # Backend dependencies
│   ├── main.py            # FastAPI application
│   ├── models.py          # Data models and schemas
│   ├── utils.py           # ML model and utilities
│   └── hearing_loss_model.pkl  # Trained ML model
└── frontend/               # Frontend web application
    ├── README.md          # Frontend-specific documentation
    ├── requirements.txt   # Frontend dependencies
    ├── app.py            # Main Streamlit application
    ├── config.py         # Configuration and styling
    ├── utils.py          # Utility functions and API client
    ├── hearing_loss_simulator.py  # Hearing loss simulation
    ├── Sample*.mp3       # Pre-processed audio samples
    └── generate_hearing_loss_samples.py  # Audio preprocessing script
```

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /health` - Health check endpoint
- `POST /generate-audio` - Generate pure tone audio for testing
- `POST /analyze-hearing` - Analyze hearing test results using ML model
- `GET /` - API documentation and status

## Machine Learning Model

### Model Details
- **Algorithm**: Logistic Regression
- **Features**: Frequency response patterns, age, gender
- **Output**: Hearing loss category, confidence score, risk level
- **Accuracy**: 99%+ on test data

### Categories
- Normal Hearing
- Mild Hearing Loss
- Moderate Hearing Loss
- Severe Hearing Loss

## Development

### Backend Development
```bash
cd backend
python main.py
# Server runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Frontend Development
```bash
cd frontend
streamlit run app.py --server.port 8502
# Application runs on http://localhost:8502
```

### Testing
- Backend API can be tested using the interactive docs at `/docs`
- Frontend features can be tested through the web interface
- Audio samples are pre-generated for consistent testing

## Configuration

### Backend Configuration
- Server host/port settings in `main.py`
- ML model parameters in `utils.py`
- API response models in `models.py`

### Frontend Configuration
- Styling and themes in `config.py`
- API endpoints in `utils.py`
- Test parameters and frequencies in configuration constants

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure backend server is running on port 8000
   - Check firewall settings
   - Verify virtual environment activation

2. **Audio Playback Issues**
   - Ensure browser supports audio playback
   - Check system audio settings
   - Verify librosa installation for audio processing

3. **Missing Dependencies**
   - Reinstall requirements: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Ensure virtual environment is activated

### Performance Optimization
- Audio samples are pre-processed for faster loading
- ML model is lightweight for real-time analysis
- Frontend uses caching for improved responsiveness

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

## Support

For technical support or questions:
- Check the troubleshooting section above
- Review the backend and frontend README files for specific details
- Ensure all dependencies are properly installed
- Verify that both backend and frontend servers are running
