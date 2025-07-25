"""
Utility functions for the SoundCheck Streamlit Frontend
"""

import streamlit as st
import requests
import base64
import io
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Tuple, Any
import time
from datetime import datetime

# API Configuration
#API_BASE_URL = "http://localhost:8000"
API_BASE_URL = "https://soundcheck-2qak.onrender.com"

class APIClient:
    """Client for communicating with the SoundCheck backend API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the backend API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the ML model"""
        try:
            response = self.session.get(f"{self.base_url}/model/info", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def generate_audio(self, frequency: int, duration: float = 1.0, 
                      volume: float = 0.5) -> Dict[str, Any]:
        """Generate audio tone for hearing test"""
        try:
            payload = {
                "frequency": frequency,
                "duration": duration,
                "volume": volume,
                "sample_rate": 44100
            }
            response = self.session.post(
                f"{self.base_url}/audio/generate", 
                json=payload, 
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_hearing_test(self, user_info: Dict[str, Any], 
                           frequency_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze hearing test results"""
        try:
            payload = {
                "user_info": user_info,
                "frequency_responses": frequency_responses,
                "test_id": f"test_{int(time.time())}"
            }
            response = self.session.post(
                f"{self.base_url}/test/analyze", 
                json=payload, 
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_test_frequencies(self) -> Dict[str, Any]:
        """Get standard test frequencies"""
        try:
            response = self.session.get(f"{self.base_url}/test/frequencies", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_hearing_categories(self) -> Dict[str, Any]:
        """Get hearing loss categories"""
        try:
            response = self.session.get(f"{self.base_url}/categories", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class AudioPlayer:
    """Handles audio playback in Streamlit"""
    
    @staticmethod
    def play_audio_from_base64(audio_data: str, autoplay: bool = False) -> None:
        """Play audio from base64 data"""
        try:
            import base64
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(audio_data)
            # Use Streamlit's native audio component
            st.audio(audio_bytes, format='audio/wav', autoplay=autoplay)
        except Exception as e:
            st.error(f"Error playing audio: {e}")
    
    @staticmethod
    def create_audio_button(frequency: int, api_client: APIClient) -> bool:
        """Create a button that plays audio when clicked"""
        button_key = f"play_{frequency}hz"
        
        if st.button(f"🔊 Play {frequency} Hz", key=button_key, use_container_width=True):
            with st.spinner(f"Generating {frequency} Hz tone..."):
                audio_response = api_client.generate_audio(frequency)
                
                if audio_response.get("success"):
                    AudioPlayer.play_audio_from_base64(
                        audio_response["audio_data"], 
                        autoplay=True
                    )
                    return True
                else:
                    st.error(f"Failed to generate audio: {audio_response.get('error', 'Unknown error')}")
                    return False
        return False

class DataVisualizer:
    """Creates visualizations for hearing test results"""
    
    @staticmethod
    def create_audiogram(frequency_responses: List[Dict[str, Any]], 
                        predicted_thresholds: Optional[Dict[str, float]] = None) -> go.Figure:
        """Create an audiogram visualization"""
        frequencies = [r["frequency"] for r in frequency_responses]
        heard_status = [r["heard"] for r in frequency_responses]
        
        # Estimate thresholds based on responses
        thresholds = []
        for response in frequency_responses:
            if response["heard"]:
                thresholds.append(20)  # Normal hearing
            else:
                # Estimate based on frequency
                if response["frequency"] <= 1000:
                    thresholds.append(35)
                elif response["frequency"] <= 4000:
                    thresholds.append(40)
                else:
                    thresholds.append(45)
        
        # Create the plot
        fig = go.Figure()
        
        # Add threshold line
        fig.add_trace(go.Scatter(
            x=frequencies,
            y=thresholds,
            mode='lines+markers',
            name='Estimated Thresholds',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        # Add normal hearing reference
        fig.add_hline(y=25, line_dash="dash", line_color="green", 
                     annotation_text="Normal Hearing Threshold (25 dB)")
        
        # Customize layout
        fig.update_layout(
            title=dict(
                text="🎧 Hearing Test Results - Audiogram",
                font=dict(size=22, color='white', family='Arial Black'),
                x=0.5,
                y=0.95
            ),
            xaxis_title="Frequency (Hz)",
            yaxis_title="Hearing Threshold (dB HL)",
            yaxis=dict(
                autorange="reversed",  # Invert y-axis (audiogram convention)
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=12, color='white'),
                title_font=dict(size=14, color='white')
            ),
            xaxis=dict(
                type="log",  # Log scale for frequencies
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=12, color='white'),
                title_font=dict(size=14, color='white')
            ),
            template="plotly_dark",
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=80, b=60, l=60, r=40),
            showlegend=True,
            legend=dict(
                font=dict(color='white', size=12),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(255,255,255,0.3)',
                borderwidth=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_frequency_response_chart(frequency_responses: List[Dict[str, Any]]) -> go.Figure:
        """Create a frequency response chart"""
        if not frequency_responses:
            # Return empty chart if no data
            fig = go.Figure()
            fig.update_layout(
                title="No data available",
                template="plotly_dark",
                height=450
            )
            return fig

        frequencies = [r["frequency"] for r in frequency_responses]
        heard = [1 if r["heard"] else 0 for r in frequency_responses]
        colors = ['#28a745' if h else '#dc3545' for h in heard]
        
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=frequencies,
            y=heard,
            marker_color=colors,
            text=['✓ Heard' if h else '✗ Not Heard' for h in heard],
            textposition='auto',
            textfont=dict(size=14, color='white', family='Arial Black'),
            marker=dict(
                line=dict(color='rgba(255,255,255,0.3)', width=2),
                opacity=0.9
            ),
            hovertemplate='<b>%{x} Hz</b><br>%{text}<br><extra></extra>',
            width=0.6,
            name='Response'
        ))

        fig.update_layout(
            title=dict(
                text="🎵 Frequency Response Summary",
                font=dict(size=22, color='white', family='Arial Black'),
                x=0.5,
                y=0.95
            ),
            xaxis_title="Frequency (Hz)",
            yaxis_title="Response",
            yaxis=dict(
                tickvals=[0, 1],
                ticktext=['Not Heard', 'Heard'],
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=12, color='white'),
                range=[-0.1, 1.1]  # Ensure proper range
            ),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=12, color='white'),
                title_font=dict(size=14, color='white'),
                type='category'  # Ensure frequencies are treated as categories
            ),
            template="plotly_dark",
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=80, b=60, l=60, r=40),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_risk_gauge(risk_level: str, confidence: float) -> go.Figure:
        """Create a risk level gauge"""
        risk_values = {"Low": 1, "Medium": 2, "High": 3}
        risk_colors = {"Low": "green", "Medium": "yellow", "High": "red"}
        
        value = risk_values.get(risk_level, 1)
        color = risk_colors.get(risk_level, "green")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Risk Level: {risk_level}"},
            gauge={
                'axis': {'range': [None, 3]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 1], 'color': "lightgreen"},
                    {'range': [1, 2], 'color': "lightyellow"},
                    {'range': [2, 3], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 2.5
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig

class SessionManager:
    """Manages Streamlit session state"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        if 'test_started' not in st.session_state:
            st.session_state.test_started = False
        
        if 'current_frequency_index' not in st.session_state:
            st.session_state.current_frequency_index = 0
        
        if 'frequency_responses' not in st.session_state:
            st.session_state.frequency_responses = []
        
        if 'test_completed' not in st.session_state:
            st.session_state.test_completed = False
        
        if 'test_results' not in st.session_state:
            st.session_state.test_results = None
        
        if 'user_info' not in st.session_state:
            st.session_state.user_info = {}
    
    @staticmethod
    def reset_test():
        """Reset the hearing test"""
        st.session_state.test_started = False
        st.session_state.current_frequency_index = 0
        st.session_state.frequency_responses = []
        st.session_state.test_completed = False
        st.session_state.test_results = None
        # Clear audio played tracking
        if 'audio_played_for_frequency' in st.session_state:
            st.session_state.audio_played_for_frequency = {}
    
    @staticmethod
    def save_response(frequency: int, heard: bool):
        """Save a frequency response"""
        response = {"frequency": frequency, "heard": heard}
        
        # Check if response already exists for this frequency
        existing_index = None
        for i, r in enumerate(st.session_state.frequency_responses):
            if r["frequency"] == frequency:
                existing_index = i
                break
        
        if existing_index is not None:
            st.session_state.frequency_responses[existing_index] = response
        else:
            st.session_state.frequency_responses.append(response)

def format_recommendations(recommendations: List[str]) -> str:
    """Format recommendations as HTML with better visibility"""
    if not recommendations:
        return "<p style='color: #6c757d; font-style: italic;'>No specific recommendations available.</p>"

    formatted = "<div style='background: white; padding: 1rem; border-radius: 8px;'><ul style='margin: 0; padding-left: 1.5rem;'>"
    for rec in recommendations:
        formatted += f"<li style='margin-bottom: 0.5rem; color: #333; line-height: 1.5;'>{rec}</li>"
    formatted += "</ul></div>"

    return formatted

def get_category_color(category: str) -> str:
    """Get color for hearing category"""
    colors = {
        "Normal": "#28a745",      # Green
        "Mild": "#ffc107",        # Yellow
        "Moderate": "#fd7e14",    # Orange
        "Severe": "#dc3545",      # Red
        "Profound": "#6f42c1"     # Purple
    }
    return colors.get(category, "#6c757d")  # Default gray

def format_confidence(confidence: float) -> str:
    """Format confidence score as percentage"""
    return f"{confidence * 100:.1f}%"
