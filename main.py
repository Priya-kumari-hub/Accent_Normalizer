import os
from video_audio_utils import extract_audio_from_video, split_audio, merge_audio_with_video
from transcription import transcribe_audio_chunks
from tts_converter import convert_texts_to_speech

# Configuration
VIDEO_PATH = "input_video.mp4"                          # Input video file path
FULL_AUDIO_PATH = "full_audio.wav"                      # Audio extracted from video
CHUNK_FOLDER = "chunks"                                 # Folder to save audio chunks
TRANSCRIPTION_CSV = "transcriptions.csv"                # Where transcriptions are saved
TTS_OUTPUT_PATH = "tts_outputs/indian_accent_audio.wav" # Path to save generated Indian-accent audio
FINAL_VIDEO_PATH = "static/final_output.mp4"            # Final video output path
CHUNK_DURATION_MS = 60000                               # 60 seconds per chunk

def main():
    print("🚀 Starting Indian Accent Conversion Pipeline")

    # Step 1: Extract audio from video
    extract_audio_from_video(VIDEO_PATH, FULL_AUDIO_PATH)

    # Step 2: Split audio into manageable chunks
    chunk_paths = split_audio(FULL_AUDIO_PATH, CHUNK_DURATION_MS, CHUNK_FOLDER)

    # Step 3: Transcribe each audio chunk using Whisper
    transcribe_audio_chunks(CHUNK_FOLDER, TRANSCRIPTION_CSV)

    # Step 4: Generate Indian-accented speech using TTS
    convert_texts_to_speech(TRANSCRIPTION_CSV, TTS_OUTPUT_PATH)

    # Step 5: Merge generated audio with original video
    merge_audio_with_video(VIDEO_PATH, TTS_OUTPUT_PATH, FINAL_VIDEO_PATH)

    print("✅ All done! Final output saved at:", FINAL_VIDEO_PATH)

if __name__ == "__main__":
    main()
