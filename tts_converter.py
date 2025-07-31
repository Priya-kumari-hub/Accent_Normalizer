# ✅ tts_converter.py (efficient and uses edge-tts)
def convert_transcriptions_to_indian_accent(df, output_folder="tts_outputs", gender="female"):
    import os
    import asyncio
    from edge_tts import Communicate

    voice_map = {
        "female": "en-IN-NeerjaNeural",
        "male": "en-IN-PrabhatNeural"
    }
    voice = voice_map.get(gender, "en-IN-NeerjaNeural")

    os.makedirs(output_folder, exist_ok=True)

    async def run_tts():
        for idx, row in df.iterrows():
            text = row["transcription"]
            output_path = os.path.join(output_folder, f"chunk_{idx}.mp3")
            print(f"🎤 Generating TTS for: {output_path}")
            communicate = Communicate(text, voice)
            await communicate.save(output_path)

    asyncio.run(run_tts())
