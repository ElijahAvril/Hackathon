import os
import requests
import tempfile
from pathlib import Path
import dotenv 
dotenv.load_dotenv()

ELEVEN_KEY = os.getenv("Eleven_Labs_Api_Key")
DEFAULT_VOICE = os.getenv("ELEVEN_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # replace with a voice you have

if not ELEVEN_KEY:
    raise RuntimeError("Eleven_Labs_Api_Key not found in environment")

ELEVEN_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{}"

def text_to_speech_bytes(text: str, voice_id: str | None = None, model_id: str = "eleven_multilingual_v2", stability: float = 0.4, similarity_boost: float = 0.75) -> bytes:
    """
    Returns raw audio bytes (mp3) for text using ElevenLabs.
    """
    vid = voice_id or DEFAULT_VOICE
    url = ELEVEN_TTS_URL.format(vid)

    headers = {
        "xi-api-key": ELEVEN_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }

    resp = requests.post(url, headers=headers, json=payload, stream=True)
    if resp.status_code not in (200, 201):
        # forward message for debugging
        raise RuntimeError(f"ElevenLabs TTS failed: {resp.status_code} {resp.text}")
    

    return resp.content
