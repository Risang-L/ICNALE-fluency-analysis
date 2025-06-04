import os
import whisper
import pandas as pd

# === Settings ===
AUDIO_DIR = "data/wav"
MODEL_SIZE = "base"  # Change to "small", "medium" if needed
OUTPUT_CSV = "data/segment_level_analysis.csv"

# === Load Whisper model ===
print(f"[INFO] Loading Whisper model: {MODEL_SIZE}")
model = whisper.load_model(MODEL_SIZE)

# === Store results here ===
all_segments = []

# === Loop through audio files ===
for filename in sorted(os.listdir(AUDIO_DIR)):
    if not filename.endswith(".wav"):
        continue

    # Remove file extension
    speaker_id = filename.replace(".wav", "")

    # Extract country code (second element after splitting by "_")
    parts = speaker_id.split("_")
    country = parts[1] if len(parts) > 1 else "UNK"

    print(f"[INFO] Transcribing {filename}")
    result = model.transcribe(os.path.join(AUDIO_DIR, filename))

    previous_end = 0.0  # For pause calculation

    for i, seg in enumerate(result["segments"]):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        word_count = len(text.split())
        duration = end - start
        wps = word_count / duration if duration > 0 else 0
        pause = start - previous_end if i > 0 else 0.0

        all_segments.append({
            "speaker_id": speaker_id,
            "country": country,
            "segment_id": i + 1,
            "start": start,
            "end": end,
            "duration": duration,
            "words": word_count,
            "wps": round(wps, 3),
            "pause_before": round(pause, 3),
            "text": text
        })

        previous_end = end

# === Convert to DataFrame and save ===
df = pd.DataFrame(all_segments)
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print(f"\n✅ Saved segment-level data to: {OUTPUT_CSV}")
print(df.head())
