
import os, asyncio
from edge_tts import Communicate

def convert_text_to_indian_accent(text, output_path, gender="female"):
    voice = {"female": "en-IN-NeerjaNeural", "male": "en-IN-PrabhatNeural"}.get(gender, "en-IN-NeerjaNeural")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    async def run():
        communicate = Communicate(text, voice)
        await communicate.save(output_path)
    asyncio.run(run())
