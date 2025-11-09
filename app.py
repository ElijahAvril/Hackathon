# tts_test.py
from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play  # correct import in 1.5.0

# Load API key
load_dotenv()
api_key = os.getenv("Eleven_Labs_Api_Key")
if not api_key:
    raise ValueError("API key not found in .env")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

# Read text from input.txt
text_file_path = "input.txt"
if not os.path.exists(text_file_path):
    raise FileNotFoundError(f"{text_file_path} not found")

with open(text_file_path, "r", encoding="utf-8") as f:
    text_to_speak = f.read()

# Generate audio using default voice "alloy"
voice = client.get_default_voice()  # works in 1.5.0
audio = voice.generate(text=text_to_speak)

# Play the audio
play(audio)

# Optionally, save to file
with open("output.wav", "wb") as f:
    f.write(audio)

print("Audio generated, saved as output.wav, and played successfully!")
