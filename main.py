from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import shutil
import uuid
import subprocess
import pandas as pd

from video_audio_utils import extract_audio_from_video, split_audio, merge_audio_with_video
from transcription import transcribe_audio_chunks
from tts_converter import convert_transcriptions_to_indian_accent

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
    filename = f"{file_id}.mp4"
    input_video_path = os.path.join(UPLOAD_DIR, filename)

    # Ensure uploads dir exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # yt-dlp download
    command = [
        "yt-dlp",
        "-f", "bestaudio+bestvideo",
        "--merge-output-format", "mp4",
        "-o", input_video_path,
        url
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return {"error": "❌ Failed to download or merge YouTube video. Please check the URL."}

    return await process_pipeline(input_video_path, gender, file_id)

async def process_pipeline(input_video_path, gender, file_id):
    if not os.path.exists(input_video_path):
        return {"error": f"❌ File not found at {input_video_path}"}

    print(f"🎬 Extracting audio from {input_video_path}")
    audio_path = extract_audio_from_video(input_video_path)

    chunk_paths = split_audio(audio_path, output_folder="chunks")
    transcribe_audio_chunks("chunks", output_csv="transcriptions.csv")

    df = pd.read_csv("transcriptions.csv")
    convert_transcriptions_to_indian_accent(df, "tts_outputs", gender=gender)

    final_output_path = os.path.join("static", f"{file_id}_output.mp4")
    merge_audio_with_video(input_video_path, os.path.join("tts_outputs", "combined_audio.mp3"), final_output_path)

    return FileResponse(final_output_path, media_type="video/mp4", filename="converted_video.mp4")
