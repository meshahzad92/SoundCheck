"""
SoundCheck - AI-Powered Hearing Test Streamlit Application
Professional, clean, and attractive frontend for the hearing test system
"""

import streamlit as st
import time
from datetime import datetime
import pandas as pd

# Import our custom modules
from utils import (
    APIClient, AudioPlayer, DataVisualizer, SessionManager,
    format_recommendations, get_category_color, format_confidence
)
from config import (
    APP_CONFIG, TEST_CONFIG, load_css, create_header, create_info_card,
    create_metric_card, create_progress_bar, create_frequency_display,
    create_result_category_display, ICONS
)
from hearing_loss_simulator import show_hearing_loss_simulator

# Configure the Streamlit page
st.set_page_config(**APP_CONFIG)

# Load custom CSS
load_css()

# Initialize session state
SessionManager.initialize_session()

# Initialize API client
@st.cache_resource
def get_api_client():
    return APIClient()

api_client = get_api_client()

def check_backend_connection():
    """Check if backend is available"""
    health = api_client.health_check()
    return health.get("status") == "healthy"

def show_welcome_page():
    """Display the welcome page"""
    create_header()
    
    # Check backend connection
    if not check_backend_connection():
        create_info_card("""
        <h3>⚠️ Backend Connection Issue</h3>
        <p>Cannot connect to the SoundCheck backend API. Please ensure:</p>
        <ul>
            <li>The backend server is running on <code>http://localhost:8000</code></li>
            <li>Run <code>python start_server.py</code> in the backend directory</li>
        </ul>
        """, "error")
        return
    
    # Welcome content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to SoundCheck! 👋")
        
        st.markdown("""
        **SoundCheck** is an ML-powered hearing test application that uses machine learning 
        to analyze your hearing profile and provide personalized recommendations.
        
        ### What makes SoundCheck special?
        
        - 🧠 **ML-Powered Analysis**: Uses trained machine learning models for accurate assessment
        - 🔊 **Professional Audio Testing**: Generates precise pure-tone audio signals
        - 📊 **Detailed Results**: Comprehensive analysis with visualizations
        - 🏥 **Health Recommendations**: Personalized advice based on your results
        - 🔒 **Privacy First**: All processing happens locally, no data shared or exposed
        """)
        
        # User information form
        st.markdown("### Tell us about yourself")
        
        col_age, col_gender = st.columns(2)
        with col_age:
            age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
        with col_gender:
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        
        st.session_state.user_info = {"age": age, "gender": gender}
        
        # Start test button
        if st.button("🎧 Start Hearing Test", type="primary", use_container_width=True):
            st.session_state.test_started = True
            st.rerun()

        # Feature promotion
        st.markdown("---")
        st.markdown("### 🎵 New Feature: Hearing Loss Simulator")
        st.markdown("""
        Experience how different types of hearing loss affect audio perception.
        Our simulator applies digital filters to demonstrate:
        - High-frequency hearing loss (presbycusis)
        - Mild to severe hearing impairment
        - Real-time audio processing with visualizations
        """)

        if st.button("🎧 Try Hearing Loss Simulator", use_container_width=True):
            # Set the page state to navigate to hearing loss simulator
            st.session_state.current_page = "Hearing Loss Simulator"
            st.rerun()
    
    with col2:
        # Quick Instructions - improved visibility
        st.markdown("### 📋 Quick Instructions")

        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            <h4 style="color: white; margin-top: 0; margin-bottom: 1rem;">🎧 Before Starting:</h4>
            <div style="margin-bottom: 0.8rem;">
                <strong>1. Use headphones or earbuds</strong><br>
                <small style="opacity: 0.9;">For accurate results</small>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <strong>2. Find a quiet environment</strong><br>
                <small style="opacity: 0.9;">Minimize background noise</small>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <strong>3. Adjust your volume</strong><br>
                <small style="opacity: 0.9;">To a comfortable level</small>
            </div>
            <div style="margin-bottom: 0;">
                <strong>4. Focus and be honest</strong><br>
                <small style="opacity: 0.9;">With your responses</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_hearing_test():
    """Display the hearing test interface"""
    create_header()
    
    frequencies = TEST_CONFIG["frequencies"]
    current_index = st.session_state.current_frequency_index
    
    if current_index >= len(frequencies):
        # Test completed
        st.session_state.test_completed = True
        st.rerun()
        return
    
    current_frequency = frequencies[current_index]
    
    # Progress bar
    create_progress_bar(current_index + 1, len(frequencies))
    
    # Test instructions - improved
    st.markdown("""
    <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 2rem; border-radius: 15px; margin: 1.5rem 0; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
        <h2 style="color: white; margin-top: 0; margin-bottom: 1rem;">🔊 Listen Carefully</h2>
        <p style="font-size: 1.2rem; margin-bottom: 1rem; opacity: 0.95;">
            Click the <strong>Play</strong> button below to hear a tone at <strong>{} Hz</strong>
        </p>
        <p style="font-size: 1rem; margin-bottom: 0; opacity: 0.9;">
            Then honestly indicate whether you heard it or not
        </p>
    </div>
    """.format(current_frequency), unsafe_allow_html=True)
    
    # Main test interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Frequency display
        create_frequency_display(current_frequency)
        
        # Audio player
        st.markdown("### 🔊 Audio Test")
        
        # Play button
        if st.button(f"▶️ Play {current_frequency} Hz Tone", 
                    type="primary", use_container_width=True):
            with st.spinner("Generating audio..."):
                audio_response = api_client.generate_audio(
                    frequency=current_frequency,
                    duration=TEST_CONFIG["tone_duration"],
                    volume=TEST_CONFIG["tone_volume"]
                )
                
                if audio_response.get("success"):
                    AudioPlayer.play_audio_from_base64(
                        audio_response["audio_data"], 
                        autoplay=True
                    )
                    st.success("🔊 Audio playing! Listen carefully...")
                else:
                    st.error(f"Failed to generate audio: {audio_response.get('error')}")
        
        st.markdown("---")
        
        # Response buttons
        st.markdown("### Did you hear the tone?")
        
        col_yes, col_no = st.columns(2)
        
        with col_yes:
            if st.button("✅ Yes, I heard it", use_container_width=True, type="primary"):
                SessionManager.save_response(current_frequency, True)
                st.session_state.current_frequency_index += 1
                st.success("Response recorded!")
                time.sleep(0.5)
                st.rerun()
        
        with col_no:
            if st.button("❌ No, I didn't hear it", use_container_width=True):
                SessionManager.save_response(current_frequency, False)
                st.session_state.current_frequency_index += 1
                st.success("Response recorded!")
                time.sleep(0.5)
                st.rerun()
    
    # Sidebar with progress
    with st.sidebar:
        st.markdown("### Test Progress")
        
        # Show completed frequencies
        for i, freq in enumerate(frequencies):
            if i < current_index:
                response = next((r for r in st.session_state.frequency_responses 
                               if r["frequency"] == freq), None)
                if response:
                    status = "✅ Heard" if response["heard"] else "❌ Not heard"
                    st.markdown(f"**{freq} Hz**: {status}")
            elif i == current_index:
                st.markdown(f"**{freq} Hz**: 🔄 Current")
            else:
                st.markdown(f"**{freq} Hz**: ⏳ Pending")
        
        # Reset button
        if st.button("🔄 Restart Test"):
            SessionManager.reset_test()
            st.rerun()

def show_results():
    """Display the test results"""
    create_header()
    
    if not st.session_state.frequency_responses:
        st.error("No test data available. Please take the test first.")
        return
    
    # Analyze results
    with st.spinner("🧠 Analyzing your hearing profile with AI..."):
        analysis_result = api_client.analyze_hearing_test(
            user_info=st.session_state.user_info,
            frequency_responses=st.session_state.frequency_responses
        )
    
    if not analysis_result.get("success"):
        st.error(f"Analysis failed: {analysis_result.get('error', 'Unknown error')}")
        return
    
    result = analysis_result["result"]
    st.session_state.test_results = result
    
    # Clean, professional results header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 2.2rem; margin-bottom: 0.5rem;">🎯 Your Hearing Analysis</h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;">AI-powered assessment complete</p>
    </div>
    """, unsafe_allow_html=True)

    # Category result - more compact and professional
    category = result["predicted_category"]
    category_colors = {
        "Normal": "#28a745",
        "Mild": "#ffc107",
        "Moderate": "#fd7e14",
        "Severe": "#dc3545",
        "Profound": "#6f42c1"
    }
    category_color = category_colors.get(category, "#6c757d")

    # Main result card - more compact
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {category_color}, {category_color}dd);
                color: white; padding: 1.5rem; border-radius: 12px; text-align: center;
                margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.3rem;">
            {category} Hearing
        </div>
        <div style="font-size: 0.95rem; opacity: 0.9;">
            Classification Result
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics in a single row - dark theme
    col_pta, col_conf, col_risk = st.columns(3)

    with col_pta:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1.2rem; border-radius: 10px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px);">
            <div style="font-size: 1.8rem; font-weight: bold; color: #667eea; margin-bottom: 0.3rem;">
                {result['pta_score']:.1f} dB
            </div>
            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.9); text-transform: uppercase; letter-spacing: 1px;">
                PTA Score
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_conf:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1.2rem; border-radius: 10px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px);">
            <div style="font-size: 1.8rem; font-weight: bold; color: #28a745; margin-bottom: 0.3rem;">
                {format_confidence(result['confidence_score'])}
            </div>
            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.9); text-transform: uppercase; letter-spacing: 1px;">
                Confidence
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_risk:
        risk_colors = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}
        risk_color = risk_colors.get(result['risk_level'], "#6c757d")

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1.2rem; border-radius: 10px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px);">
            <div style="font-size: 1.8rem; font-weight: bold; color: {risk_color}; margin-bottom: 0.3rem;">
                {result['risk_level']}
            </div>
            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.9); text-transform: uppercase; letter-spacing: 1px;">
                Risk Level
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Test Summary - compact and professional
    st.markdown("### 📈 Test Summary")
    total_freq = len(st.session_state.frequency_responses)
    heard_freq = sum(1 for r in st.session_state.frequency_responses if r["heard"])

    col_summary1, col_summary2 = st.columns(2)

    with col_summary1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 1.5rem; font-weight: bold; color: #667eea; margin-bottom: 0.3rem;">
                {heard_freq}/{total_freq}
            </div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">
                Frequencies Heard
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_summary2:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 1.5rem; font-weight: bold; color: #28a745; margin-bottom: 0.3rem;">
                {(heard_freq/total_freq)*100:.0f}%
            </div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">
                Success Rate
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Visualizations section
    st.markdown("### 📊 Detailed Analysis")

    # Tabs for better organization
    tab1, tab2 = st.tabs(["📈 Audiogram", "🎵 Frequency Response"])

    with tab1:
        audiogram = DataVisualizer.create_audiogram(st.session_state.frequency_responses)
        st.plotly_chart(audiogram, use_container_width=True)

    with tab2:
        freq_chart = DataVisualizer.create_frequency_response_chart(
            st.session_state.frequency_responses
        )
        st.plotly_chart(freq_chart, use_container_width=True)

    # Health Recommendations - clean and professional
    st.markdown("### 🏥 Health Recommendations")

    recommendations = result.get("recommendations", [])
    if recommendations:
        # Clean recommendations without white box
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div style="background: rgba(40, 167, 69, 0.1); padding: 0.8rem; border-radius: 8px;
                        border-left: 4px solid #28a745; margin: 0.5rem 0;">
                <span style="color: rgba(255,255,255,0.9); font-size: 0.95rem;">
                    <strong>{i}.</strong> {rec}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No specific recommendations available.")
    
    # Action buttons
    col_new, col_download = st.columns(2)
    
    with col_new:
        if st.button("🔄 Take New Test", type="primary", use_container_width=True):
            SessionManager.reset_test()
            st.rerun()
    
    with col_download:
        # Create downloadable report
        report_data = {
            "Test Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Category": category,
            "PTA Score": f"{result['pta_score']:.1f} dB HL",
            "Confidence": format_confidence(result['confidence_score']),
            "Risk Level": result['risk_level'],
            "Frequencies Tested": total_freq,
            "Frequencies Heard": heard_freq
        }
        
        report_df = pd.DataFrame([report_data])
        csv = report_df.to_csv(index=False)
        
        st.download_button(
            label="📄 Download Report",
            data=csv,
            file_name=f"hearing_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

def main():
    """Main application logic"""
    
    # Initialize current_page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")

        if st.session_state.test_completed:
            options = ["Results", "Hearing Loss Simulator", "New Test"]
            current_index = 0 if st.session_state.current_page == "Results" else (1 if st.session_state.current_page == "Hearing Loss Simulator" else 0)
            page = st.radio("Go to:", options, index=current_index)
            if page == "New Test":
                SessionManager.reset_test()
                st.session_state.current_page = "Home"
                st.rerun()
            else:
                st.session_state.current_page = page
        elif st.session_state.test_started:
            options = ["Hearing Test", "Hearing Loss Simulator", "Home"]
            current_index = 0 if st.session_state.current_page == "Hearing Test" else (1 if st.session_state.current_page == "Hearing Loss Simulator" else 2)
            page = st.radio("Go to:", options, index=current_index)
            if page == "Home":
                SessionManager.reset_test()
                st.session_state.current_page = "Home"
                st.rerun()
            else:
                st.session_state.current_page = page
        else:
            options = ["Home", "Hearing Loss Simulator"]
            current_index = 0 if st.session_state.current_page == "Home" else 1
            page = st.radio("Go to:", options, index=current_index)
            st.session_state.current_page = page
        
        # About section
        st.markdown("---")
        st.markdown("### About SoundCheck")
        st.markdown("""
        **Version**: 1.0.0 \n
        **Model**: Logistic Regression \n
        **Accuracy**: 99.01% \n
        **Data**: NHANES Audiometry \n
        """)

        # Deploy section
        st.markdown("---")
        st.markdown("### 🚀 Deploy")
        if st.button("Deploy to Streamlit Cloud", use_container_width=True):
            st.info("""
            To deploy this app to Streamlit Cloud:

            1. Push your code to GitHub
            2. Go to [share.streamlit.io](https://share.streamlit.io)
            3. Connect your GitHub repository
            4. Select the main branch and `frontend/app.py`
            5. Click Deploy!

            **Note**: Make sure to set up environment variables for the backend API URL.
            """)

        # Removed the warning notice as requested
    
    # Main content routing
    if st.session_state.current_page == "Hearing Loss Simulator":
        show_hearing_loss_simulator()
    elif st.session_state.test_completed and st.session_state.current_page == "Results":
        show_results()
    elif st.session_state.test_started and st.session_state.current_page == "Hearing Test":
        show_hearing_test()
    else:
        show_welcome_page()

if __name__ == "__main__":
    main()
