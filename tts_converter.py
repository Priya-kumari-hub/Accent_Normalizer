async def convert_texts_to_indian_accent(texts, output_dir, voice="en-IN-NeerjaNeural"):
    os.makedirs(output_dir, exist_ok=True)
    for idx, text in enumerate(texts):
        output_path = os.path.join(output_dir, f"line_{idx+1}.mp3")
        try:
            communicate = edge_tts.Communicate(text=text, voice=voice)
            await communicate.save(output_path)
        except Exception as e:
            print(f"Error in TTS at line {idx+1}: {e}")
def attach_audio_to_video(video_path, new_audio_path, output_path):
    video = VideoFileClip(video_path)
    video = video.set_audio(AudioFileClip(new_audio_path))
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')
