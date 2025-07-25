# SoundCheck Frontend

Professional Streamlit web application for the SoundCheck hearing test system. Provides an intuitive interface for conducting ML-powered hearing assessments with real-time analysis and educational features.

## Overview

The frontend serves as the user interface for the SoundCheck hearing test system, featuring:
- Professional hearing test interface with guided workflow
- Real-time ML-powered analysis and results visualization
- Educational hearing loss simulator with pre-processed audio samples
- Responsive design with clean, modern styling
- Downloadable test reports and comprehensive results display

## Architecture

```
User Interface (Streamlit) → API Client → Backend API → ML Analysis → Results Display
```

### Core Components
- **Main Application** (app.py): Primary Streamlit interface and navigation
- **API Client** (utils.py): Backend communication and data processing
- **Configuration** (config.py): Styling, themes, and application settings
- **Hearing Loss Simulator** (hearing_loss_simulator.py): Educational audio simulation feature

## Installation & Setup

### Prerequisites
- Python 3.8+
- Backend API running on http://localhost:8000
- Modern web browser with audio support

### Quick Start
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pip install -r requirements.txt

# Start the application
streamlit run app.py --server.port 8502
```

### Verification
- Application: http://localhost:8502
- Backend connection status shown in sidebar
- Audio playback test available in hearing loss simulator

## Application Features

### 1. Home Page
- Welcome interface with user information collection (age, gender)
- Backend connection status indicator
- Navigation to hearing test and hearing loss simulator
- Clean, professional design with ML-powered branding

### 2. Hearing Test Flow
- **Guided Testing**: Step-by-step frequency testing (500Hz - 8000Hz)
- **Audio Playback**: Real-time pure tone generation via backend API
- **Progress Tracking**: Visual progress indicators and frequency status
- **Response Collection**: Simple Yes/No interface for each frequency
- **Navigation**: Dynamic navigation showing current test state

### 3. Results Display
- **ML Analysis**: Hearing loss classification with confidence scoring
- **Visual Reports**: Audiogram charts and frequency response visualization
- **Recommendations**: Personalized health recommendations based on results
- **Export Options**: Downloadable CSV reports with test data
- **Navigation**: Results shown within hearing test context

### 4. Hearing Loss Simulator
- **Educational Tool**: Experience different types of hearing loss
- **Pre-processed Audio**: Instant playback of hearing loss simulations
- **Multiple Types**: Mild, moderate, high-frequency, and severe hearing loss
- **Sample Audio**: Uses JFK Moon Speech for realistic demonstration

## Navigation System

### Dynamic Navigation
The application uses a context-aware navigation system:

**Home State**: `["Home", "Hearing Loss Simulator"]`
- Clean interface with only essential options
- No test-related navigation when not testing

**Test Active State**: `["Home", "Hearing Test", "Hearing Loss Simulator"]`
- Appears when hearing test is started
- "Hearing Test" option shows current test progress
- Results are displayed within "Hearing Test" context

### Navigation Behavior
- **Representational**: Shows which section you're currently in
- **Context-Aware**: Options change based on application state
- **User-Friendly**: "Finish" button returns to clean home state

## Technical Implementation

### Code Structure
```
frontend/
├── app.py                              # Main Streamlit application
├── utils.py                           # API client and utility functions
├── config.py                          # Styling and configuration
├── hearing_loss_simulator.py          # Educational simulation feature
├── generate_hearing_loss_samples.py   # Audio preprocessing script
├── requirements.txt                   # Python dependencies
├── Sample.mp3                         # Original sample audio
├── Sample_mild.mp3                    # Pre-processed mild hearing loss
├── Sample_moderate.mp3                # Pre-processed moderate hearing loss
├── Sample_high_freq.mp3               # Pre-processed high-frequency loss
└── Sample_severe.mp3                  # Pre-processed severe hearing loss
```

### Key Technologies
- **Streamlit**: Web application framework
- **Requests**: HTTP client for backend API communication
- **Plotly**: Interactive data visualizations
- **Librosa**: Audio processing for hearing loss simulation
- **NumPy/SciPy**: Audio signal processing
- **Pandas**: Data manipulation and CSV export

### Session Management
- **Test State**: Tracks current frequency, responses, and progress
- **Navigation State**: Manages page routing and context
- **User Data**: Stores age, gender, and test results
- **Audio Cache**: Caches generated audio for performance

## Configuration

### Application Settings
```python
# config.py
APP_CONFIG = {
    "title": "SoundCheck",
    "subtitle": "ML-Powered Hearing Test & Analysis",
    "theme": "professional"
}

TEST_CONFIG = {
    "frequencies": [500, 1000, 2000, 3000, 4000, 8000],
    "tone_duration": 3.0,
    "sample_rate": 22050
}
```

### API Configuration
```python
# utils.py
API_BASE_URL = "http://localhost:8000"  # Backend server URL
REQUEST_TIMEOUT = 30  # Request timeout in seconds
```

### Styling Customization
The application uses custom CSS for professional styling:
- Gradient headers and backgrounds
- Responsive design for mobile devices
- Professional color scheme
- Interactive hover effects

## Development

### Running in Development Mode
```bash
# Start with auto-reload
streamlit run app.py --server.port 8502

# With debug mode
streamlit run app.py --server.port 8502 --logger.level debug
```

### Adding New Features
1. **New Pages**: Add functions to app.py and update navigation
2. **API Endpoints**: Extend APIClient class in utils.py
3. **Styling**: Update config.py for new visual elements
4. **Audio Features**: Extend hearing_loss_simulator.py

### Testing
- **Manual Testing**: Use the web interface
- **API Testing**: Verify backend connectivity
- **Audio Testing**: Test with different browsers and devices
- **Responsive Testing**: Check mobile and tablet layouts

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   ```
   ⚠️ Backend server is not running
   ```
   **Solution**: Ensure backend server is running on http://localhost:8000

2. **Audio File Loading Error**
   ```
   ❌ Error loading sample audio: No such file or directory
   ```
   **Solution**: Verify Sample*.mp3 files exist in frontend directory

3. **Navigation Issues**
   - **Problem**: Navigation doesn't update when changing pages
   - **Solution**: Check session state management and page routing logic

4. **Hearing Loss Simulator Issues**
   - **Problem**: Pre-processed audio files not found
   - **Solution**: Run `python generate_hearing_loss_samples.py` to create audio files

### Performance Optimization
- Pre-processed audio files for instant playback
- Session state caching for improved responsiveness
- Efficient API communication with proper error handling
- Lightweight ML model integration

## Browser Compatibility
- **Chrome/Chromium**: Full support with audio playback
- **Firefox**: Full support with audio playback
- **Safari**: Full support with audio playback
- **Edge**: Full support with audio playback
- **Mobile**: Responsive design, audio support varies

## Security & Privacy
- **Local Processing**: All data processing happens locally
- **No Data Storage**: No persistent storage of user data
- **API Security**: Secure communication with backend
- **Input Validation**: Proper sanitization of user inputs

## Contributing
1. Follow Streamlit best practices
2. Maintain clean separation of concerns (app.py, utils.py, config.py)
3. Test across different browsers and devices
4. Update documentation for new features
5. Ensure responsive design principles
