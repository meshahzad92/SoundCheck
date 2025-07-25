"""
Simulated Hearing Loss Module
Implements audio filtering to simulate different types of hearing loss
"""

import streamlit as st
import numpy as np
import io
import time
from scipy.signal import butter, lfilter, freqz
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Try to import optional dependencies
try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False
    st.warning("⚠️ soundfile not available. Some features may be limited.")

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    st.warning("⚠️ librosa not available. Some features may be limited.")

class HearingLossSimulator:
    """Class to simulate different types of hearing loss on audio files"""
    
    def __init__(self):
        self.sample_rate = 22050  # Default sample rate
        
    def butter_bandstop(self, lowcut, highcut, fs, order=5):
        """Create a bandstop (notch) filter"""
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        
        # Ensure frequencies are within valid range
        low = max(0.01, min(low, 0.99))
        high = max(0.01, min(high, 0.99))
        
        if low >= high:
            # If invalid range, create a simple lowpass filter
            b, a = butter(order, high, btype='low')
        else:
            b, a = butter(order, [low, high], btype='bandstop')
        return b, a
    
    def butter_lowpass(self, cutoff, fs, order=5):
        """Create a lowpass filter"""
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        normal_cutoff = max(0.01, min(normal_cutoff, 0.99))
        b, a = butter(order, normal_cutoff, btype='low')
        return b, a
    
    def butter_highpass(self, cutoff, fs, order=5):
        """Create a highpass filter"""
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        normal_cutoff = max(0.01, min(normal_cutoff, 0.99))
        b, a = butter(order, normal_cutoff, btype='high')
        return b, a
    
    def apply_filter(self, data, filter_coeffs):
        """Apply filter to audio data"""
        b, a = filter_coeffs
        filtered_data = lfilter(b, a, data)
        return filtered_data
    
    def simulate_mild_hearing_loss(self, audio, sr):
        """Simulate mild hearing loss by reducing mid frequencies"""
        # Reduce frequencies between 1000-4000 Hz (speech range)
        b, a = self.butter_bandstop(1000, 4000, sr, order=3)
        filtered_audio = self.apply_filter(audio, (b, a))
        
        # Apply slight volume reduction
        filtered_audio = filtered_audio * 0.7
        return filtered_audio
    
    def simulate_high_frequency_loss(self, audio, sr):
        """Simulate high-frequency hearing loss (presbycusis)"""
        # Remove frequencies above 4000 Hz
        b, a = self.butter_lowpass(4000, sr, order=6)
        filtered_audio = self.apply_filter(audio, (b, a))
        
        # Apply additional attenuation to higher frequencies
        b2, a2 = self.butter_lowpass(6000, sr, order=3)
        filtered_audio = self.apply_filter(filtered_audio, (b2, a2))
        
        return filtered_audio
    
    def simulate_moderate_hearing_loss(self, audio, sr):
        """Simulate moderate hearing loss across multiple frequency bands"""
        # Reduce low frequencies (below 500 Hz)
        b1, a1 = self.butter_highpass(500, sr, order=2)
        filtered_audio = self.apply_filter(audio, (b1, a1))
        
        # Reduce high frequencies (above 3000 Hz)
        b2, a2 = self.butter_lowpass(3000, sr, order=4)
        filtered_audio = self.apply_filter(filtered_audio, (b2, a2))
        
        # Apply volume reduction
        filtered_audio = filtered_audio * 0.5
        return filtered_audio
    
    def simulate_severe_hearing_loss(self, audio, sr):
        """Simulate severe hearing loss with significant frequency reduction"""
        # Keep only narrow frequency band (500-2000 Hz)
        b1, a1 = self.butter_highpass(500, sr, order=3)
        filtered_audio = self.apply_filter(audio, (b1, a1))
        
        b2, a2 = self.butter_lowpass(2000, sr, order=5)
        filtered_audio = self.apply_filter(filtered_audio, (b2, a2))
        
        # Significant volume reduction
        filtered_audio = filtered_audio * 0.3
        return filtered_audio
    
    def convert_to_wav_bytes(self, audio_data, sample_rate):
        """Convert audio data to WAV bytes for Streamlit audio player"""
        if not HAS_SOUNDFILE:
            st.error("❌ soundfile library is required for audio conversion")
            return None

        wav_bytes = io.BytesIO()
        sf.write(wav_bytes, audio_data, sample_rate, format='WAV')
        wav_bytes.seek(0)
        return wav_bytes
    
    def create_frequency_response_plot(self, filter_coeffs, sr, title):
        """Create frequency response plot for the filter"""
        b, a = filter_coeffs
        w, h = freqz(b, a, worN=8000)
        frequencies = w * sr / (2 * np.pi)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=frequencies,
            y=20 * np.log10(abs(h)),
            mode='lines',
            name='Frequency Response',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title=f'Frequency Response - {title}',
            xaxis_title='Frequency (Hz)',
            yaxis_title='Magnitude (dB)',
            xaxis_type='log',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_spectrogram_comparison(self, original_audio, filtered_audio, sr, title):
        """Create spectrogram comparison between original and filtered audio"""
        if not HAS_LIBROSA:
            st.error("❌ librosa library is required for spectrogram analysis")
            return None

        # Compute spectrograms
        D_orig = librosa.amplitude_to_db(np.abs(librosa.stft(original_audio)), ref=np.max)
        D_filt = librosa.amplitude_to_db(np.abs(librosa.stft(filtered_audio)), ref=np.max)
        
        # Create subplot
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Original Audio', f'{title}'),
            shared_yaxes=True
        )
        
        # Time and frequency axes
        times = librosa.frames_to_time(np.arange(D_orig.shape[1]), sr=sr)
        freqs = librosa.fft_frequencies(sr=sr)
        
        # Add spectrograms
        fig.add_trace(
            go.Heatmap(z=D_orig, x=times, y=freqs, colorscale='Viridis', showscale=False),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Heatmap(z=D_filt, x=times, y=freqs, colorscale='Viridis', showscale=True),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f'Spectrogram Comparison - {title}',
            height=500,
            yaxis_title='Frequency (Hz)'
        )
        
        return fig
    
    def normalize_audio(self, audio_data):
        """Normalize audio to prevent clipping"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data

    def load_sample_audio(self, file_path="frontend/Sample.mp3"):
        """Load the sample audio file"""
        if not HAS_LIBROSA:
            raise ImportError("librosa library is required for audio file loading")

        try:
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            # Limit duration to 10 seconds for performance
            if len(audio_data) > sample_rate * 10:
                audio_data = audio_data[:sample_rate * 10]

            audio_data = self.normalize_audio(audio_data)
            return audio_data, sample_rate
        except Exception as e:
            raise Exception(f"Error loading audio file: {str(e)}")

    def generate_sample_audio(self, duration=3.0, sr=22050):
        """Generate a sample audio clip with multiple frequency components"""
        t = np.linspace(0, duration, int(sr * duration), False)

        # Create a complex audio signal with multiple frequency components
        # Speech-like frequencies
        audio = (
            0.3 * np.sin(2 * np.pi * 440 * t) +      # A4 note
            0.2 * np.sin(2 * np.pi * 880 * t) +      # A5 note
            0.15 * np.sin(2 * np.pi * 1320 * t) +    # E6 note
            0.1 * np.sin(2 * np.pi * 2640 * t) +     # E7 note
            0.05 * np.sin(2 * np.pi * 5280 * t) +    # E8 note
            0.02 * np.sin(2 * np.pi * 8000 * t)      # High frequency
        )

        # Add some envelope to make it more natural
        envelope = np.exp(-t * 0.5)  # Exponential decay
        audio = audio * envelope

        # Add some noise for realism
        noise = 0.01 * np.random.randn(len(audio))
        audio = audio + noise

        return self.normalize_audio(audio), sr


def show_hearing_loss_simulator():
    """Main function to display the hearing loss simulator page"""
    st.title("🎧 Hearing Loss Simulator")
    st.markdown("---")

    # Introduction
    st.markdown("""
    ### What is Simulated Hearing Loss?

    This tool allows you to experience how audio sounds with different types of hearing loss.
    We apply digital filters to normal audio to simulate:

    - **High-frequency hearing loss** (presbycusis) - common with aging
    - **Mild hearing loss** - affects speech frequencies
    - **Moderate hearing loss** - broader frequency reduction
    - **Severe hearing loss** - significant hearing impairment

    This helps build empathy and understanding of hearing difficulties.
    """)

    simulator = HearingLossSimulator()

    # Audio source selection
    st.markdown("### 🎵 Audio Source")
    audio_source = st.radio(
        "Choose audio source:",
        ["Play Audio", "Upload Your Own Audio"],
        help="You can use our sample audio or upload your own audio file"
    )

    audio_data = None
    sample_rate = None

    if audio_source == "Play Audio":
        if st.button("🎼 Play Audio", use_container_width=True):
            with st.spinner("Loading sample audio..."):
                try:
                    # Load the sample audio file using the new method
                    audio_data, sample_rate = simulator.load_sample_audio()
                    st.session_state.original_audio = audio_data
                    st.session_state.sample_rate = sample_rate
                    st.success("✅ Sample audio loaded!")
                except Exception as e:
                    st.error(f"❌ Error loading sample audio: {str(e)}")

        if 'original_audio' in st.session_state:
            audio_data = st.session_state.original_audio
            sample_rate = st.session_state.sample_rate

    else:  # Upload Your Own Audio
        uploaded_file = st.file_uploader(
            "Upload an audio file",
            type=['wav', 'mp3', 'flac', 'm4a'],
            help="Supported formats: WAV, MP3, FLAC, M4A"
        )

        if uploaded_file is not None:
            if not HAS_LIBROSA:
                st.error("❌ librosa library is required for audio file loading. Please use the 'Generate Sample Audio' option instead.")
            else:
                try:
                    with st.spinner("Loading audio file..."):
                        audio_data, sample_rate = librosa.load(uploaded_file, sr=None)
                        # Limit duration to 10 seconds for performance
                        if len(audio_data) > sample_rate * 10:
                            audio_data = audio_data[:sample_rate * 10]
                            st.info("ℹ️ Audio trimmed to 10 seconds for performance")

                        audio_data = simulator.normalize_audio(audio_data)
                        st.session_state.original_audio = audio_data
                        st.session_state.sample_rate = sample_rate
                        st.success("✅ Audio file loaded successfully!")
                except Exception as e:
                    st.error(f"❌ Error loading audio file: {str(e)}")

    # Show audio controls if we have audio data
    if audio_data is not None and sample_rate is not None:
        st.markdown("### 🎧 Audio Playback & Simulation")

        # Original audio
        st.markdown("#### 🔊 Original Audio")
        original_wav = simulator.convert_to_wav_bytes(audio_data, sample_rate)
        st.audio(original_wav, format='audio/wav')

        # Simulation options
        st.markdown("#### 🎛️ Hearing Loss Simulations")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔇 Mild Hearing Loss", use_container_width=True):
                with st.spinner("Applying mild hearing loss filter..."):
                    filtered_audio = simulator.simulate_mild_hearing_loss(audio_data, sample_rate)
                    filtered_wav = simulator.convert_to_wav_bytes(filtered_audio, sample_rate)
                    st.audio(filtered_wav, format='audio/wav')
                    st.session_state.last_filtered = ('mild', filtered_audio)

            if st.button("🔇 Moderate Hearing Loss", use_container_width=True):
                with st.spinner("Applying moderate hearing loss filter..."):
                    filtered_audio = simulator.simulate_moderate_hearing_loss(audio_data, sample_rate)
                    filtered_wav = simulator.convert_to_wav_bytes(filtered_audio, sample_rate)
                    st.audio(filtered_wav, format='audio/wav')
                    st.session_state.last_filtered = ('moderate', filtered_audio)

        with col2:
            if st.button("🔇 High-Frequency Loss", use_container_width=True):
                with st.spinner("Applying high-frequency hearing loss filter..."):
                    filtered_audio = simulator.simulate_high_frequency_loss(audio_data, sample_rate)
                    filtered_wav = simulator.convert_to_wav_bytes(filtered_audio, sample_rate)
                    st.audio(filtered_wav, format='audio/wav')
                    st.session_state.last_filtered = ('high_freq', filtered_audio)

            if st.button("🔇 Severe Hearing Loss", use_container_width=True):
                with st.spinner("Applying severe hearing loss filter..."):
                    filtered_audio = simulator.simulate_severe_hearing_loss(audio_data, sample_rate)
                    filtered_wav = simulator.convert_to_wav_bytes(filtered_audio, sample_rate)
                    st.audio(filtered_wav, format='audio/wav')
                    st.session_state.last_filtered = ('severe', filtered_audio)

        # Show visualizations if we have filtered audio
        if 'last_filtered' in st.session_state:
            filter_type, filtered_audio = st.session_state.last_filtered

            st.markdown("### 📊 Audio Analysis")

            # Show spectrogram comparison
            with st.expander("🔍 Spectrogram Comparison", expanded=False):
                try:
                    fig = simulator.create_spectrogram_comparison(
                        audio_data, filtered_audio, sample_rate,
                        filter_type.replace('_', ' ').title() + " Hearing Loss"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating spectrogram: {str(e)}")

        # Download options
        st.markdown("### 💾 Download Options")
        if 'last_filtered' in st.session_state:
            filter_type, filtered_audio = st.session_state.last_filtered

            # Convert to downloadable format
            download_wav = simulator.convert_to_wav_bytes(filtered_audio, sample_rate)

            st.download_button(
                label=f"📥 Download {filter_type.replace('_', ' ').title()} Hearing Loss Audio",
                data=download_wav.getvalue(),
                file_name=f"hearing_loss_{filter_type}_{int(time.time())}.wav",
                mime="audio/wav",
                use_container_width=True
            )

    # Educational content
    st.markdown("---")
    st.markdown("### 📚 Understanding Hearing Loss Types")

    with st.expander("🔍 Learn More About Hearing Loss", expanded=False):
        st.markdown("""
        #### Types of Hearing Loss Simulated:

        **🔸 Mild Hearing Loss**
        - Affects speech frequencies (1000-4000 Hz)
        - Difficulty hearing soft sounds and some speech
        - Common in early stages of hearing loss

        **🔸 High-Frequency Hearing Loss (Presbycusis)**
        - Affects frequencies above 4000 Hz
        - Most common type, especially with aging
        - Difficulty hearing consonants, birds, alarms

        **🔸 Moderate Hearing Loss**
        - Affects both low and high frequencies
        - Significant impact on speech understanding
        - May require hearing aids

        **🔸 Severe Hearing Loss**
        - Major reduction across frequency spectrum
        - Difficulty with most sounds and speech
        - Typically requires hearing aids or assistive devices

        #### Technical Implementation:
        - Uses digital signal processing with Butterworth filters
        - Simulates frequency-specific attenuation
        - Applies realistic volume reduction
        - Maintains audio quality while demonstrating hearing loss effects
        """)


if __name__ == "__main__":
    show_hearing_loss_simulator()
