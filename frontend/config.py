"""
Configuration and styling for the SoundCheck Streamlit Frontend
"""

import streamlit as st

# App Configuration
APP_CONFIG = {
    "page_title": "SoundCheck - Hearing Test",
    "page_icon": "🔊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Test Configuration
TEST_CONFIG = {
    "frequencies": [500, 1000, 2000, 3000, 4000, 6000, 8000],
    "tone_duration": 2.0,
    "tone_volume": 0.6,
    "instructions": {
        "setup": """
        ### 🎧 Test Setup Instructions
        
        **Before starting the hearing test:**
        
        1. **Use headphones or earbuds** for accurate results
        2. **Find a quiet environment** with minimal background noise
        3. **Adjust your volume** to a comfortable level
        4. **Sit comfortably** and focus on the test
        
        **During the test:**
        - You will hear tones at different frequencies
        - Click "Yes, I heard it" if you can hear the tone
        - Click "No, I didn't hear it" if you cannot hear the tone
        - Be honest with your responses for accurate results
        """,
        "test": """
        ### 🔊 Listen carefully and respond honestly
        
        Click the play button to hear a tone, then indicate whether you heard it or not.
        """,
        "results": """
        ### 📊 Your Hearing Test Results
        
        Based on your responses, our AI model has analyzed your hearing profile.
        Remember: This is a screening tool, not a medical diagnosis.
        """
    }
}

# Styling and CSS
def load_css():
    """Load custom CSS styling"""
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333;
        line-height: 1.6;
    }
    
    .success-card {
        background: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }

    .warning-card {
        background: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }

    .error-card {
        background: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }

    /* Recommendations styling */
    .recommendations-card {
        background: white;
        border: 1px solid #e9ecef;
        border-left: 4px solid #28a745;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .recommendations-card ul {
        margin: 0;
        padding-left: 1.5rem;
    }

    .recommendations-card li {
        margin-bottom: 0.8rem;
        color: #333;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Audio button styling */
    .audio-button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .audio-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 20px;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Frequency display */
    .frequency-display {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin: 1rem 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Results styling */
    .result-category {
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-size: 1.5rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .category-normal {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
    }
    
    .category-mild {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: #212529;
    }
    
    .category-moderate {
        background: linear-gradient(135deg, #fd7e14, #dc3545);
        color: white;
    }
    
    .category-severe {
        background: linear-gradient(135deg, #dc3545, #6f42c1);
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .frequency-display {
            font-size: 2rem;
        }
        
        .result-category {
            font-size: 1.2rem;
            padding: 1.5rem;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #667eea);
    }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Create the app header"""
    st.markdown("""
    <div class="app-header fade-in">
        <div class="app-title">🔊 SoundCheck</div>
        <div class="app-subtitle">AI-Powered Hearing Test & Analysis</div>
    </div>
    """, unsafe_allow_html=True)

def create_info_card(content: str, card_type: str = "info"):
    """Create an information card"""
    card_class = f"info-card {card_type}-card"
    st.markdown(f"""
    <div class="{card_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(value: str, label: str):
    """Create a metric display card"""
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar(current: int, total: int):
    """Create a custom progress bar"""
    percentage = (current / total) * 100
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%"></div>
    </div>
    <p style="text-align: center; margin-top: 0.5rem;">
        Progress: {current}/{total} frequencies tested ({percentage:.0f}%)
    </p>
    """, unsafe_allow_html=True)

def create_frequency_display(frequency: int):
    """Create a frequency display"""
    st.markdown(f"""
    <div class="frequency-display pulse">
        {frequency} Hz
    </div>
    """, unsafe_allow_html=True)

def create_result_category_display(category: str):
    """Create a result category display"""
    category_class = f"category-{category.lower()}"
    st.markdown(f"""
    <div class="result-category {category_class} fade-in">
        {category} Hearing
    </div>
    """, unsafe_allow_html=True)

# Color schemes
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2", 
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Icons
ICONS = {
    "sound": "🔊",
    "headphones": "🎧",
    "check": "✅",
    "cross": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "chart": "📊",
    "medical": "🏥",
    "brain": "🧠",
    "ear": "👂"
}
