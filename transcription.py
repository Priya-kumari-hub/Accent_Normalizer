# transcription.py

import whisper
import os
import pandas as pd

# Load Whisper model (use "base", "small", "medium", or "large" as per your setup)
model = whisper.load_model("base")  # change to "medium" if GPU and speed needed

def transcribe_audio_chunks(chunk_folder, output_csv="transcriptions.csv"):
    results = []
    files = sorted([f for f in os.listdir(chunk_folder) if f.endswith(".wav") or f.endswith(".mp3")])
    
    for idx, file in enumerate(files):
        file_path = os.path.join(chunk_folder, file)
        print(f"🔠 Transcribing {file_path} ...")
        result = model.transcribe(file_path)
        results.append({
            "chunk_id": idx,
            "file_name": file,
            "transcription": result["text"]
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"✅ Transcriptions saved to {output_csv}")
