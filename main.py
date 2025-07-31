from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import shutil
import uuid

from video_audio_utils import extract_audio_from_video, split_audio, merge_audio_with_video

from transcription import transcribe_audio_chunks
from tts_converter import convert_to_indian_accent

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/convert")
async def convert_video_to_indian_accent(
    video: UploadFile = File(...),
    gender: str = Form("female")  # Accept "male" or "female" input
):
    # Save uploaded video
    file_id = str(uuid.uuid4())
    input_video_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")
    
    with open(input_video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # Step 1: Extract audio
    audio_path = extract_audio_from_video(input_video_path)

    # Step 2: Split audio
    split_audio_to_chunks(audio_path, "chunks")

    # Step 3: Transcribe
    transcribe_audio_chunks("chunks", output_csv="transcriptions.csv")

    # Step 4: TTS conversion (with gendered voice)
    convert_transcriptions_to_indian_accent("transcriptions.csv", "tts_outputs", gender=gender)

    # Step 5: Merge new audio with original video
    final_output_path = os.path.join("static", f"{file_id}_output.mp4")
    merge_audio_with_video(input_video_path, os.path.join("tts_outputs", "combined_audio.mp3"), final_output_path)

    return FileResponse(final_output_path, media_type="video/mp4", filename="converted_video.mp4")
