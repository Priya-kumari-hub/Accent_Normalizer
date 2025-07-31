
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks

def extract_audio_from_video(video_path, output_audio_path="full_audio.wav"):
    print(f"🎬 Extracting audio from {video_path}")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path)
    print(f"✅ Audio saved to {output_audio_path}")
    return output_audio_path

def split_audio(audio_path, chunk_length_ms=20000, output_folder="chunks"):
    print(f"✂️ Splitting audio into {chunk_length_ms / 1000} second chunks")
    os.makedirs(output_folder, exist_ok=True)
    audio = AudioSegment.from_file(audio_path)
    chunks = make_chunks(audio, chunk_length_ms)

    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.join(output_folder, f"chunk_{i+1}.wav")
        chunk.export(chunk_name, format="wav")
        chunk_paths.append(chunk_name)
        print(f"✅ Saved: {chunk_name}")

    return chunk_paths

def merge_audio_with_video(original_video_path, tts_audio_path, output_path="static/final_output.mp4"):
    print(f"🔄 Merging {tts_audio_path} with {original_video_path}")
    video = VideoFileClip(original_video_path)
    new_audio = AudioFileClip(tts_audio_path)

    final_duration = min(video.duration, new_audio.duration)
    new_audio = new_audio.subclip(0, final_duration)
    video = video.subclip(0, final_duration)

    final_video = video.set_audio(new_audio)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"✅ Final video saved at: {output_path}")
    return output_path
