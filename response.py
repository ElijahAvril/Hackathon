import sys
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

def main():
    # Ensure we got a filename argument
    if len(sys.argv) < 2:
        print("Usage: python response.py <textfile>")
        return

    text_file = sys.argv[1]

    # Read the incoming text file
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    print(f"Received text from {text_file} ✅")

    # Load ElevenLabs key
    load_dotenv()
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    # Generate speech
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Combine chunks
    audio_bytes = b"".join(chunk for chunk in audio_stream)

    # Play audio
    print("Playing response audio… 🎧")
    play(audio_bytes)

if __name__ == "__main__":
    main()
