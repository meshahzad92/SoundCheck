"""
Pydantic models for the SoundCheck Hearing Test API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class HearingCategory(str, Enum):
    """Hearing loss categories based on WHO classification"""
    NORMAL = "Normal"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    PROFOUND = "Profound"

class FrequencyResponse(BaseModel):
    """Response for a single frequency test"""
    frequency: int = Field(..., description="Frequency in Hz (e.g., 500, 1000, 2000)")
    heard: bool = Field(..., description="Whether the user heard the tone")
    threshold: Optional[float] = Field(None, description="Estimated threshold in dB HL")

class UserInfo(BaseModel):
    """User demographic information"""
    age: Optional[int] = Field(None, ge=1, le=120, description="User's age")
    gender: Optional[str] = Field(None, description="User's gender (Male/Female)")
    
class HearingTestRequest(BaseModel):
    """Request model for hearing test submission"""
    user_info: UserInfo
    frequency_responses: List[FrequencyResponse] = Field(
        ..., 
        description="List of frequency test responses",
        min_items=1
    )
    test_id: Optional[str] = Field(None, description="Unique test identifier")

class HearingTestResult(BaseModel):
    """Result of hearing test analysis"""
    predicted_category: HearingCategory
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Model confidence (0-1)")
    pta_score: float = Field(..., description="Pure-tone average in dB HL")
    frequency_analysis: Dict[str, Any] = Field(..., description="Per-frequency analysis")
    recommendations: List[str] = Field(..., description="Health recommendations")
    risk_level: str = Field(..., description="Risk assessment (Low/Medium/High)")

class HearingTestResponse(BaseModel):
    """Complete response for hearing test"""
    success: bool
    message: str
    test_id: str
    result: Optional[HearingTestResult] = None
    error_details: Optional[str] = None

class AudioGenerationRequest(BaseModel):
    """Request for generating audio tone"""
    frequency: int = Field(..., ge=20, le=20000, description="Frequency in Hz")
    duration: float = Field(1.0, ge=0.1, le=10.0, description="Duration in seconds")
    volume: float = Field(0.5, ge=0.0, le=1.0, description="Volume level (0-1)")
    sample_rate: int = Field(44100, description="Sample rate in Hz")

class AudioResponse(BaseModel):
    """Response for audio generation"""
    success: bool
    message: str
    audio_data: Optional[str] = Field(None, description="Base64 encoded audio data")
    content_type: str = Field("audio/wav", description="Audio MIME type")

class HealthStatus(BaseModel):
    """API health status"""
    status: str
    timestamp: str
    model_loaded: bool
    version: str

class ModelInfo(BaseModel):
    """Information about the ML model"""
    model_name: str
    accuracy: float
    feature_names: List[str]
    classes: List[str]
    training_date: str
    
class FrequencyThreshold(BaseModel):
    """Threshold estimation for a frequency"""
    frequency: int
    estimated_threshold: float
    confidence: float
    
class TestStatistics(BaseModel):
    """Statistics about the hearing test"""
    total_frequencies_tested: int
    frequencies_heard: int
    hearing_percentage: float
    average_threshold: float
    worst_frequency: Optional[int] = None
    best_frequency: Optional[int] = None
