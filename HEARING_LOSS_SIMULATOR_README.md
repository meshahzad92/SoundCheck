# 🎧 Hearing Loss Simulator - User Guide

## Overview

The **Hearing Loss Simulator** is a new feature in SoundCheck that allows users to experience how different types of hearing loss affect audio perception. This educational tool applies digital signal processing filters to simulate various hearing impairments.

## 🚀 How to Access

1. **Start the Application**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   python start_server.py

   # Terminal 2 - Frontend
   cd frontend
   source venv/bin/activate
   streamlit run app.py
   ```

2. **Navigate to the Simulator**:
   - Open your browser to `http://localhost:8501`
   - Use the **sidebar navigation** to select "Hearing Loss Simulator"
   - Or click the "Try Hearing Loss Simulator" button on the home page

## 🎵 Features

### Audio Source Options

**1. Generate Sample Audio**
- Click "Generate Sample Audio" to create a test audio clip
- Contains multiple frequency components (440Hz to 8000Hz)
- Designed to demonstrate hearing loss effects clearly
- No additional files needed

**2. Upload Your Own Audio**
- Supports: WAV, MP3, FLAC, M4A formats
- Automatically trimmed to 10 seconds for performance
- Best results with speech or music containing various frequencies

### Hearing Loss Types

**🔇 Mild Hearing Loss**
- Reduces mid-frequencies (1000-4000 Hz)
- Affects speech clarity
- Common in early hearing loss stages

**🔇 High-Frequency Loss (Presbycusis)**
- Removes frequencies above 4000 Hz
- Most common age-related hearing loss
- Affects consonant sounds, alarms, birds

**🔇 Moderate Hearing Loss**
- Reduces both low and high frequencies
- Significant impact on speech understanding
- May require hearing aids

**🔇 Severe Hearing Loss**
- Major frequency reduction (keeps only 500-2000 Hz)
- Difficulty with most sounds and speech
- Typically requires assistive devices

## 🎛️ How to Use

1. **Choose Audio Source**:
   - Select "Generate Sample Audio" for quick testing
   - Or "Upload Your Own Audio" for personal files

2. **Play Original Audio**:
   - Listen to the unfiltered audio first
   - Adjust your volume to a comfortable level

3. **Experience Hearing Loss**:
   - Click any hearing loss simulation button
   - Compare the filtered audio to the original
   - Try different types to understand various impairments

4. **Analyze Results** (Optional):
   - Expand "Spectrogram Comparison" to see visual analysis
   - Shows frequency content differences
   - Helps understand which frequencies are affected

5. **Download Simulated Audio**:
   - Use the download button to save filtered audio
   - Share with others for educational purposes

## 🔧 Technical Details

### Audio Processing
- **Sample Rate**: 22,050 Hz (default)
- **Filters**: Butterworth digital filters
- **Processing**: Real-time audio filtering using scipy.signal
- **Normalization**: Prevents audio clipping

### Filter Specifications
- **Mild Loss**: Bandstop filter (1000-4000 Hz), 70% volume
- **High-Freq Loss**: Lowpass filter (4000 Hz cutoff)
- **Moderate Loss**: Highpass (500 Hz) + Lowpass (3000 Hz), 50% volume
- **Severe Loss**: Narrow band (500-2000 Hz), 30% volume

### Dependencies
- **Required**: scipy, numpy, plotly, streamlit
- **Optional**: librosa (for file upload), soundfile (for audio conversion)
- **Fallback**: Generate sample audio works without optional dependencies

## 🎯 Educational Use Cases

### For Healthcare Professionals
- Demonstrate hearing loss effects to patients
- Educational tool for audiology training
- Patient empathy building

### For Developers
- Understanding accessibility requirements
- Audio application testing
- Hearing aid algorithm development

### For General Users
- Learn about hearing loss types
- Understand family members' hearing difficulties
- Awareness and empathy building

## 🛠️ Troubleshooting

### Common Issues

**"soundfile not available" Warning**
- Feature still works with generated audio
- Install soundfile: `pip install soundfile`
- Only affects audio download functionality

**"librosa not available" Warning**
- Can't upload custom audio files
- Use "Generate Sample Audio" instead
- Install librosa: `pip install librosa`

**Audio Not Playing**
- Check browser audio permissions
- Ensure speakers/headphones are connected
- Try refreshing the page

**Poor Audio Quality**
- Use headphones for best experience
- Ensure quiet environment
- Check volume levels

### Performance Tips
- Use shorter audio clips (< 10 seconds)
- Generate sample audio for faster processing
- Close other browser tabs if experiencing lag

## 🔬 Behind the Scenes

The simulator uses **digital signal processing** techniques:

1. **Audio Loading**: Converts uploaded files to numpy arrays
2. **Filter Design**: Creates Butterworth filters for specific frequency ranges
3. **Signal Processing**: Applies filters using scipy.signal.lfilter
4. **Visualization**: Generates spectrograms using librosa and plotly
5. **Audio Export**: Converts processed audio back to playable format

This provides a realistic simulation of how hearing loss affects audio perception, helping users understand the challenges faced by people with hearing impairments.

## 📚 Further Reading

- [Understanding Hearing Loss Types](https://www.nidcd.nih.gov/health/hearing-loss)
- [Presbycusis (Age-Related Hearing Loss)](https://www.nidcd.nih.gov/health/age-related-hearing-loss)
- [Digital Signal Processing for Audio](https://en.wikipedia.org/wiki/Audio_signal_processing)

---

**Note**: This simulator is for educational purposes only and should not be used for medical diagnosis. Consult a healthcare professional for hearing concerns.
