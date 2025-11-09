from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
import sys

# Load environment variables
load_dotenv()

API_KEY = os.getenv("Eleven_Labs_Api_Key")
if not API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY not set in environment")

client = ElevenLabs(api_key=API_KEY)

# Get input file from command line
if len(sys.argv) < 2:
    raise ValueError("No input file provided. Usage: python tts_eleven.py <file_path>")

INPUT_FILE = sys.argv[1]

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"File not found: {INPUT_FILE}")

# Read text from file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    raise ValueError(f"No text found in {INPUT_FILE}")

print(f"🔊 Converting text from: {INPUT_FILE}")

# Convert text to speech
audio_stream = client.text_to_speech.convert(
    text=text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # Change voice if you want
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Play audio
print("Playing audio… 🎧")
play(audio_stream)

print("✅ Done!")
