import whisper
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    print(f"🔠 Transcribing {audio_path} ...")
    result = model.transcribe(audio_path)
    return result["text"].strip()
