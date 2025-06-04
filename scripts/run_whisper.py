import os
import whisper

# Load the Whisper model (use "base" or "small" to start; larger models need more RAM/VRAM)
model = whisper.load_model("base")  # options: "tiny", "base", "small", "medium", "large"

INPUT_DIR = "data/wav"
OUTPUT_DIR = "data/whisper_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through all WAV files
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".wav"):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename.replace(".wav", ".txt"))

        # Skip if already transcribed
        if os.path.exists(output_path):
            print(f"[SKIP] {filename} already transcribed.")
            continue

        print(f"[INFO] Transcribing: {filename}")
        result = model.transcribe(input_path)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"[DONE] Saved transcription → {output_path}")
