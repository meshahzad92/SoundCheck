"""
Utility functions for the SoundCheck Hearing Test API
"""

import numpy as np
import pandas as pd
from scipy import signal
from pydub import AudioSegment
from pydub.generators import Sine
import base64
import io
import joblib
import os
from typing import List, Dict, Tuple, Optional
from models import FrequencyResponse, HearingCategory, FrequencyThreshold
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages the ML model loading and predictions"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.metadata = None
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model and artifacts"""
        try:
            # Load model metadata
            metadata_path = os.path.join(self.model_dir, "model_metadata.joblib")
            if os.path.exists(metadata_path):
                self.metadata = joblib.load(metadata_path)
                logger.info(f"Loaded model metadata: {self.metadata['model_name']}")
            
            # Load the model
            model_name = self.metadata['model_name'].lower() if self.metadata else "logisticregression"
            model_path = os.path.join(self.model_dir, f"hearing_classifier_{model_name}.joblib")
            
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info(f"Loaded model from: {model_path}")
            else:
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # Load scaler if it exists
            scaler_path = os.path.join(self.model_dir, "scaler.joblib")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info("Loaded scaler")
            
            # Load feature names
            feature_path = os.path.join(self.model_dir, "feature_names.joblib")
            if os.path.exists(feature_path):
                self.feature_names = joblib.load(feature_path)
                logger.info(f"Loaded feature names: {self.feature_names}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is properly loaded"""
        return self.model is not None and self.feature_names is not None
    
    def predict(self, features: Dict[str, float]) -> Tuple[str, float]:
        """Make prediction using the loaded model"""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")
        
        # Create feature vector in the correct order
        feature_vector = []
        for feature_name in self.feature_names:
            # Extract frequency from feature name (e.g., "500_avg" -> 500)
            freq = feature_name.replace("_avg", "")
            if freq in features:
                feature_vector.append(features[freq])
            else:
                # Use a default threshold if frequency not tested
                feature_vector.append(25.0)  # Normal hearing threshold
        
        # Convert to numpy array and reshape
        X = np.array(feature_vector).reshape(1, -1)
        
        # Scale if scaler is available
        if self.scaler:
            X = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        
        # Get confidence score
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.8  # Default confidence for models without probability
        
        return prediction, confidence

class AudioGenerator:
    """Generates audio tones for hearing tests"""
    
    @staticmethod
    def generate_sine_tone(frequency: int, duration: float, volume: float = 0.5, 
                          sample_rate: int = 44100) -> AudioSegment:
        """Generate a sine wave tone"""
        try:
            # Generate sine wave using pydub
            tone = Sine(frequency).to_audio_segment(duration=int(duration * 1000))
            
            # Adjust volume (pydub uses dB, convert from 0-1 scale)
            volume_db = 20 * np.log10(max(volume, 0.001))  # Avoid log(0)
            tone = tone + volume_db
            
            return tone
        except Exception as e:
            logger.error(f"Error generating tone: {e}")
            raise
    
    @staticmethod
    def tone_to_base64(tone: AudioSegment, format: str = "wav") -> str:
        """Convert audio tone to base64 string"""
        try:
            # Export to bytes
            buffer = io.BytesIO()
            tone.export(buffer, format=format)
            audio_bytes = buffer.getvalue()
            
            # Encode to base64
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            return base64_audio
        except Exception as e:
            logger.error(f"Error converting tone to base64: {e}")
            raise

class HearingAnalyzer:
    """Analyzes hearing test results"""
    
    @staticmethod
    def estimate_thresholds(responses: List[FrequencyResponse]) -> Dict[str, float]:
        """Estimate hearing thresholds from yes/no responses"""
        thresholds = {}
        
        for response in responses:
            freq_str = str(response.frequency)
            
            if response.heard:
                # If heard, threshold is likely below 25 dB (normal)
                thresholds[freq_str] = 20.0
            else:
                # If not heard, threshold is likely above 25 dB
                # Use frequency-dependent estimation
                if response.frequency <= 1000:
                    thresholds[freq_str] = 35.0  # Mild loss
                elif response.frequency <= 4000:
                    thresholds[freq_str] = 40.0  # Mild to moderate
                else:
                    thresholds[freq_str] = 45.0  # High frequency loss common
        
        return thresholds
    
    @staticmethod
    def calculate_pta(thresholds: Dict[str, float]) -> float:
        """Calculate Pure-Tone Average (PTA) from thresholds"""
        # Use standard PTA frequencies: 500, 1000, 2000, 4000 Hz
        pta_frequencies = ['500', '1000', '2000', '4000']
        pta_values = []
        
        for freq in pta_frequencies:
            if freq in thresholds:
                pta_values.append(thresholds[freq])
        
        if pta_values:
            return sum(pta_values) / len(pta_values)
        else:
            # Fallback: use all available frequencies
            if thresholds:
                return sum(thresholds.values()) / len(thresholds)
            else:
                return 25.0  # Default normal threshold
    
    @staticmethod
    def get_recommendations(category: str, pta: float) -> List[str]:
        """Get health recommendations based on hearing category"""
        recommendations = []
        
        if category == "Normal":
            recommendations = [
                "Your hearing appears to be within normal limits.",
                "Continue to protect your hearing from loud noises.",
                "Consider annual hearing checks if you're over 50.",
                "Use ear protection in noisy environments."
            ]
        elif category == "Mild":
            recommendations = [
                "You may have mild hearing loss.",
                "Consider consulting an audiologist for a comprehensive evaluation.",
                "You might benefit from hearing aids in certain situations.",
                "Protect your hearing from further damage."
            ]
        elif category == "Moderate":
            recommendations = [
                "You appear to have moderate hearing loss.",
                "We strongly recommend seeing an audiologist.",
                "Hearing aids would likely be beneficial.",
                "Consider communication strategies and assistive devices."
            ]
        elif category in ["Severe", "Profound"]:
            recommendations = [
                "You appear to have significant hearing loss.",
                "Please consult an audiologist or ENT specialist immediately.",
                "You may benefit from hearing aids or cochlear implants.",
                "Consider learning sign language or other communication methods."
            ]
        
        recommendations.append("Note: This is a screening test, not a diagnostic evaluation.")
        return recommendations
    
    @staticmethod
    def assess_risk_level(category: str, age: Optional[int] = None, pta: Optional[float] = None,
                         frequencies_not_heard: Optional[int] = None, total_frequencies: int = 7) -> str:
        """Assess risk level based on frequency response - simplified logic"""

        # Calculate frequencies heard
        frequencies_heard = total_frequencies - (frequencies_not_heard or 0)

        # Simple rule-based risk assessment based on user requirements:
        # - No voices heard = High risk (Red)
        # - All voices heard = Low risk (Green)
        # - More than 2 voices heard = Medium risk (Yellow)
        # - 2 or fewer voices heard = High risk (Red)

        if frequencies_heard == 0:
            return "High"  # No voices heard - High risk (Red)
        elif frequencies_heard == total_frequencies:
            return "Low"   # All voices heard - Low risk (Green)
        elif frequencies_heard > 2:
            return "Medium"  # More than 2 voices heard - Medium risk (Yellow)
        else:
            return "High"    # 2 or fewer voices heard - High risk (Red)

# Global model manager instance
model_manager = ModelManager()

def get_model_manager() -> ModelManager:
    """Get the global model manager instance"""
    return model_manager
