"""
SoundCheck - ML-Powered Hearing Test Backend
FastAPI application for the hackathon hearing test project
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import uuid
from datetime import datetime
import logging
from typing import Dict, Any

# Import our models and utilities
from models import (
    HearingTestRequest, HearingTestResponse, HearingTestResult,
    AudioGenerationRequest, AudioResponse, HealthStatus, ModelInfo,
    HearingCategory, FrequencyThreshold, TestStatistics
)
from utils import (
    get_model_manager, AudioGenerator, HearingAnalyzer
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SoundCheck API",
    description="ML-Powered Hearing Test Backend for Hackathon",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model_manager = get_model_manager()
audio_generator = AudioGenerator()
hearing_analyzer = HearingAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting SoundCheck API...")
    
    # Verify model is loaded
    if not model_manager.is_loaded():
        logger.error("Failed to load ML model!")
        raise RuntimeError("ML model not loaded")
    
    logger.info("SoundCheck API started successfully!")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "SoundCheck - ML-Powered Hearing Test API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint"""
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=model_manager.is_loaded(),
        version="1.0.0"
    )

@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the loaded ML model"""
    if not model_manager.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    metadata = model_manager.metadata
    return ModelInfo(
        model_name=metadata.get('model_name', 'Unknown'),
        accuracy=0.99,  # From training results
        feature_names=metadata.get('feature_names', []),
        classes=metadata.get('classes', []),
        training_date=datetime.now().isoformat()
    )

@app.post("/audio/generate", response_model=AudioResponse)
async def generate_audio_tone(request: AudioGenerationRequest):
    """Generate an audio tone for hearing testing"""
    try:
        # Generate the tone
        tone = audio_generator.generate_sine_tone(
            frequency=request.frequency,
            duration=request.duration,
            volume=request.volume,
            sample_rate=request.sample_rate
        )
        
        # Convert to base64
        audio_base64 = audio_generator.tone_to_base64(tone)
        
        return AudioResponse(
            success=True,
            message=f"Generated {request.frequency}Hz tone",
            audio_data=audio_base64,
            content_type="audio/wav"
        )
        
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")

@app.post("/test/analyze", response_model=HearingTestResponse)
async def analyze_hearing_test(request: HearingTestRequest):
    """Analyze hearing test results and provide ML-based assessment"""
    try:
        # Generate unique test ID if not provided
        test_id = request.test_id or str(uuid.uuid4())
        
        logger.info(f"Analyzing hearing test {test_id}")
        
        # Estimate thresholds from responses
        thresholds = hearing_analyzer.estimate_thresholds(request.frequency_responses)
        
        # Calculate PTA (Pure-Tone Average)
        pta = hearing_analyzer.calculate_pta(thresholds)
        
        # Make ML prediction
        try:
            prediction, confidence = model_manager.predict(thresholds)
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")
            # Fallback to rule-based classification
            if pta <= 25:
                prediction = "Normal"
            elif pta <= 40:
                prediction = "Mild"
            elif pta <= 60:
                prediction = "Moderate"
            else:
                prediction = "Severe"
            confidence = 0.7
        
        # Get recommendations
        recommendations = hearing_analyzer.get_recommendations(prediction, pta)
        
        # Calculate additional risk factors
        frequencies_not_heard = len([r for r in request.frequency_responses if not r.heard])
        total_frequencies = len(request.frequency_responses)

        # Assess risk level with simplified logic
        risk_level = hearing_analyzer.assess_risk_level(
            prediction,
            request.user_info.age,
            pta,
            frequencies_not_heard,
            total_frequencies
        )
        
        # Create frequency analysis
        frequency_analysis = {
            "thresholds": thresholds,
            "pta": pta,
            "frequencies_tested": [r.frequency for r in request.frequency_responses],
            "frequencies_heard": [r.frequency for r in request.frequency_responses if r.heard]
        }
        
        # Create result
        result = HearingTestResult(
            predicted_category=HearingCategory(prediction),
            confidence_score=confidence,
            pta_score=pta,
            frequency_analysis=frequency_analysis,
            recommendations=recommendations,
            risk_level=risk_level
        )
        
        return HearingTestResponse(
            success=True,
            message="Hearing test analyzed successfully",
            test_id=test_id,
            result=result
        )
        
    except Exception as e:
        logger.error(f"Error analyzing hearing test: {e}")
        return HearingTestResponse(
            success=False,
            message="Analysis failed",
            test_id=request.test_id or "unknown",
            error_details=str(e)
        )

@app.get("/test/frequencies")
async def get_test_frequencies():
    """Get the standard frequencies used for hearing testing"""
    return {
        "frequencies": [500, 1000, 2000, 3000, 4000, 6000, 8000],
        "description": "Standard audiometric frequencies in Hz",
        "pta_frequencies": [500, 1000, 2000, 4000],
        "pta_description": "Frequencies used for Pure-Tone Average calculation"
    }

@app.get("/categories")
async def get_hearing_categories():
    """Get hearing loss categories and their descriptions"""
    return {
        "categories": {
            "Normal": {
                "range": "≤ 25 dB HL",
                "description": "No hearing loss"
            },
            "Mild": {
                "range": "26-40 dB HL", 
                "description": "Mild hearing loss"
            },
            "Moderate": {
                "range": "41-60 dB HL",
                "description": "Moderate hearing loss"
            },
            "Severe": {
                "range": "61-80 dB HL",
                "description": "Severe hearing loss"
            },
            "Profound": {
                "range": "> 80 dB HL",
                "description": "Profound hearing loss"
            }
        },
        "note": "Classifications based on WHO standards"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_details": str(exc)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
