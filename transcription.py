# ✅ transcription.py (lightweight & CPU-friendly)
import whisper
import os
import pandas as pd

# Load lightweight Whisper model (CPU-friendly)
model = whisper.load_model("base")  # Avoids GPU issues

def transcribe_audio_chunks(chunk_folder, output_csv="transcriptions.csv"):
    results = []
    files = sorted([f for f in os.listdir(chunk_folder) if f.endswith((".wav", ".mp3"))])

    for idx, file in enumerate(files):
        file_path = os.path.join(chunk_folder, file)
        print(f"🔠 Transcribing {file_path} ...")
        result = model.transcribe(file_path)
        results.append({
            "chunk_id": idx,
            "file_name": file,
            "transcription": result["text"].strip()
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"✅ Transcriptions saved to {output_csv}")
