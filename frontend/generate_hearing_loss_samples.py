#!/usr/bin/env python3
"""
Script to pre-generate hearing loss audio samples
This creates the 4 different hearing loss versions of the sample audio
so they can be loaded instantly without processing delays.
"""

import numpy as np
from scipy.signal import butter, lfilter
import librosa
import soundfile as sf
import os

class HearingLossProcessor:
    """Processes audio to simulate different types of hearing loss"""
    
    def butter_lowpass(self, cutoff, fs, order=5):
        """Create a Butterworth low-pass filter"""
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a
    
    def butter_highpass(self, cutoff, fs, order=5):
        """Create a Butterworth high-pass filter"""
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a
    
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        """Create a Butterworth band-pass filter"""
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a
    
    def apply_filter(self, audio, filter_coeffs):
        """Apply filter to audio signal"""
        b, a = filter_coeffs
        return lfilter(b, a, audio)
    
    def normalize_audio(self, audio_data):
        """Normalize audio to prevent clipping"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data
    
    def simulate_mild_hearing_loss(self, audio, sr):
        """Simulate mild hearing loss - slight high frequency reduction"""
        # Reduce frequencies above 4000 Hz by 20%
        b, a = self.butter_lowpass(4000, sr, order=3)
        filtered_audio = self.apply_filter(audio, (b, a))
        
        # Mix with original (80% original, 20% filtered)
        result = 0.8 * audio + 0.2 * filtered_audio
        return self.normalize_audio(result)
    
    def simulate_moderate_hearing_loss(self, audio, sr):
        """Simulate moderate hearing loss - more significant frequency reduction"""
        # Reduce frequencies above 3000 Hz by 50%
        b, a = self.butter_lowpass(3000, sr, order=4)
        filtered_audio = self.apply_filter(audio, (b, a))
        
        # Mix with original (60% original, 40% filtered)
        result = 0.6 * audio + 0.4 * filtered_audio
        return self.normalize_audio(result)
    
    def simulate_high_frequency_loss(self, audio, sr):
        """Simulate high-frequency hearing loss (presbycusis)"""
        # Remove frequencies above 4000 Hz
        b, a = self.butter_lowpass(4000, sr, order=6)
        filtered_audio = self.apply_filter(audio, (b, a))
        
        # Apply additional attenuation to higher frequencies
        b2, a2 = self.butter_lowpass(6000, sr, order=3)
        filtered_audio = self.apply_filter(filtered_audio, (b2, a2))
        
        return self.normalize_audio(filtered_audio)
    
    def simulate_severe_hearing_loss(self, audio, sr):
        """Simulate severe hearing loss - significant frequency and volume reduction"""
        # Heavily filter frequencies above 2000 Hz
        b, a = self.butter_lowpass(2000, sr, order=6)
        filtered_audio = self.apply_filter(audio, (b, a))
        
        # Reduce overall volume by 40%
        filtered_audio = filtered_audio * 0.6
        
        # Add some distortion to simulate recruitment
        filtered_audio = np.tanh(filtered_audio * 2) * 0.5
        
        return self.normalize_audio(filtered_audio)

def generate_hearing_loss_samples():
    """Generate all hearing loss variations of the sample audio"""
    
    # File paths
    input_file = "Sample.mp3"
    output_files = {
        "mild": "Sample_mild.mp3",
        "moderate": "Sample_moderate.mp3", 
        "high_freq": "Sample_high_freq.mp3",
        "severe": "Sample_severe.mp3"
    }
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        print("Please make sure Sample.mp3 is in the frontend directory.")
        return
    
    print(f"🎵 Loading original audio: {input_file}")
    
    try:
        # Load the original audio
        audio_data, sample_rate = librosa.load(input_file, sr=None)
        
        # Limit duration to 10 seconds for performance
        if len(audio_data) > sample_rate * 10:
            audio_data = audio_data[:sample_rate * 10]
            print("ℹ️ Audio trimmed to 10 seconds")
        
        print(f"✅ Loaded audio: {len(audio_data)/sample_rate:.1f}s at {sample_rate}Hz")
        
        # Initialize processor
        processor = HearingLossProcessor()
        
        # Generate each hearing loss variation
        hearing_loss_functions = {
            "mild": processor.simulate_mild_hearing_loss,
            "moderate": processor.simulate_moderate_hearing_loss,
            "high_freq": processor.simulate_high_frequency_loss,
            "severe": processor.simulate_severe_hearing_loss
        }
        
        for loss_type, output_file in output_files.items():
            print(f"🔄 Generating {loss_type} hearing loss...")
            
            # Apply hearing loss simulation
            processed_audio = hearing_loss_functions[loss_type](audio_data, sample_rate)
            
            # Save the processed audio
            sf.write(output_file, processed_audio, sample_rate, format='MP3')
            print(f"✅ Saved: {output_file}")
        
        print("\n🎉 All hearing loss samples generated successfully!")
        print("\nGenerated files:")
        for loss_type, output_file in output_files.items():
            if os.path.exists(output_file):
                print(f"  ✅ {output_file} ({loss_type} hearing loss)")
            else:
                print(f"  ❌ {output_file} (failed)")
                
    except Exception as e:
        print(f"❌ Error processing audio: {str(e)}")

if __name__ == "__main__":
    generate_hearing_loss_samples()
