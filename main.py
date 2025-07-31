
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os, shutil, uuid, subprocess
from video_audio_utils import extract_audio_from_video, merge_audio_with_video
from transcription import transcribe_audio
from tts_converter import convert_text_to_indian_accent

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "✅ API running. Use /docs to test."}

@app.post("/convert")
async def convert(video: UploadFile = File(...), gender: str = Form("female")):
    file_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    return await process(video_path, gender, file_id)

async def process(video_path, gender, file_id):
    audio_path = extract_audio_from_video(video_path)
    text = transcribe_audio(audio_path)
    tts_path = os.path.join("tts_outputs", f"{file_id}.mp3")
    convert_text_to_indian_accent(text, tts_path, gender)
    final_path = os.path.join("static", f"{file_id}.mp4")
    merge_audio_with_video(video_path, tts_path, final_path)
    return FileResponse(final_path, media_type="video/mp4", filename="converted.mp4")
