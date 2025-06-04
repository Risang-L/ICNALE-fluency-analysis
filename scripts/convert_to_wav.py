import os
from pydub import AudioSegment

# Set your input/output directories
INPUT_DIR = "data/mp3"
OUTPUT_DIR = "data/wav"

# Make sure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through all .mp3 files in the input folder
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".mp3"):
        mp3_path = os.path.join(INPUT_DIR, filename)
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        wav_path = os.path.join(OUTPUT_DIR, wav_filename)

        # Load MP3 and export as mono 16kHz WAV
        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(wav_path, format="wav")

        print(f"Converted: {filename} → {wav_filename}")
