# ✅ tts_converter.py (short-video optimized, no DataFrame needed)
import os
import asyncio
from edge_tts import Communicate

def convert_text_to_indian_accent(text, output_path="tts_outputs/chunk_0.mp3", gender="female"):
    voice_map = {
        "female": "en-IN-NeerjaNeural",
        "male": "en-IN-PrabhatNeural"
    }
    voice = voice_map.get(gender, "en-IN-NeerjaNeural")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    async def run():
        print(f"🎤 Generating TTS: {output_path}")
        communicate = Communicate(text, voice)
        await communicate.save(output_path)

    asyncio.run(run())
