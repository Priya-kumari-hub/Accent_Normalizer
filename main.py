# ✅ main.py (optimized for short videos, avoids chunking and GPU usage)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import shutil
import uuid
import subprocess
import pandas as pd

try:
    from moviepy.editor import VideoFileClip
    print("✅ moviepy.editor import successful.")
except Exception as e:
    print("❌ MoviePy import failed:", e)

from video_audio_utils import extract_audio_from_video, merge_audio_with_video
from transcription import transcribe_audio
from tts_converter import convert_text_to_indian_accent

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "✅ Accent Normalizer API is running. Use /docs to upload a video or YouTube URL."}

@app.post("/convert")
async def convert_video_to_indian_accent(
    video: UploadFile = File(...),
    gender: str = Form("female")
):
    file_id = str(uuid.uuid4())
    input_video_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")
    with open(input_video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    return await process_pipeline(input_video_path, gender, file_id)

@app.post("/convert-url")
async def convert_video_from_youtube_url(
    url: str = Form(...),
    gender: str = Form("female")
):
    file_id = str(uuid.uuid4())
    input_video_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    command = ["yt-dlp", "-f", "bestaudio+bestvideo", "--merge-output-format", "mp4", "-o", input_video_path, url]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return {"error": "❌ Failed to download or merge YouTube video. Please check the URL."}
    return await process_pipeline(input_video_path, gender, file_id)

async def process_pipeline(input_video_path, gender, file_id):
    if not os.path.exists(input_video_path):
        return {"error": f"❌ File not found at {input_video_path}"}

    print(f"🎮 Extracting audio from {input_video_path}")
    audio_path = extract_audio_from_video(input_video_path)

    text = transcribe_audio(audio_path)
    print("✅ Transcription:", text)

    tts_path = os.path.join("tts_outputs", "chunk_0.mp3")
    convert_text_to_indian_accent(text, tts_path, gender)

    final_output_path = os.path.join("static", f"{file_id}_output.mp4")
    merge_audio_with_video(input_video_path, tts_path, final_output_path)

    return FileResponse(final_output_path, media_type="video/mp4", filename="converted_video.mp4")
