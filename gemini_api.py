import sys
import subprocess
from datetime import datetime
import os
from typing import List, Dict
import dotenv
from google import genai
from google.genai import types

dotenv.load_dotenv()

GEMINI_KEY = os.getenv("Gemini_Api_Key")
if not GEMINI_KEY:
    raise RuntimeError("Gemini_Api_Key not set in environment")

client = genai.Client(api_key=GEMINI_KEY)
MODEL_NAME = "gemini-2.5-flash"

history = []


def _build_prompt(history: List[Dict[str, str]]):
    """Convert message history to a string format"""
    lines = ["System: You are a helpful assistant."]
    for msg in history:
        role = msg["role"].capitalize()
        content = msg["content"]
        lines.append(f"{role}: {content}")
    lines.append("Assistant:")
    return "\n".join(lines)


def generate_reply(user_text: str) -> str:
    """Send text to Gemini and return its response."""
    history.append({"role": "user", "content": user_text})
    prompt = _build_prompt(history)

    config = types.GenerateContentConfig(max_output_tokens=800)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config=config
    )

    ai_text = response.text.strip() if response and response.text else "I could not generate a response."

    # Save AI reply to a new file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"response_{timestamp}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ai_text)

    print(f"✅ Saved AI response to {output_file}")

    # Send to text-to-speech converter
    try:
        subprocess.run(["python", "response.py", output_file], check=True)
        print("🎤 Sent response to TTS successfully")
    except Exception as e:
        print(f"⚠ Error sending to TTS: {e}")

    return output_file


def reply_from_file(input_file: str) -> str:
    """Read the user's text file and generate AI response."""
    with open(input_file, "r", encoding="utf-8") as f:
        user_text = f.read().strip()
    return generate_reply(user_text)