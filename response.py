from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

# Load .env
load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Read text from file
INPUT_FILE = "input.txt"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read().strip()

print(f"Loaded text from {INPUT_FILE} ✅")

# Convert text to speech
audio_stream = client.text_to_speech.convert(
    text=text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # Change voice if you want
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Join streaming chunks
audio_bytes = b"".join(chunk for chunk in audio_stream)

# Play result
print("Playing audio… 🎧")
play(audio_bytes)
