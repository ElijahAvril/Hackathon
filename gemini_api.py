import sys
import subprocess
from datetime import datetime
import os
from typing import List, Dict
import dotenv
from google import genai
from google.genai import types

# Load environment variables
dotenv.load_dotenv()

GEMINI_KEY = os.getenv("Gemini_Api_Key")
if not GEMINI_KEY:
    raise RuntimeError("Gemini_Api_Key not set in environment")  

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_KEY)
MODEL_NAME = "gemini-2.5-flash"

history = []

def _build_prompt(history: List[Dict[str, str]], language: str) -> str:
    """Convert message history to a string format and enforce target language"""
    lines = [
        "System: You are a helpful multilingual assistant.",
        f"System: Mainly reply in {language}."
    ]
    for msg in history:
        role = msg["role"].capitalize()
        content = msg["content"]
        lines.append(f"{role}: {content}")
    lines.append("Assistant:")
    return "\n".join(lines)

def generate_reply(user_text: str, language: str = "en") -> str:
    """Send text to Gemini, save AI response, and convert it to speech"""
    history.append({"role": "user", "content": user_text})
    prompt = _build_prompt(history, language)

    config = types.GenerateContentConfig(max_output_tokens=800)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config=config
    )

    ai_text = response.text.strip() if response and response.text else "I could not generate a response."

    # Save AI reply to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"response_{timestamp}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ai_text)

    print(f"✅ Saved AI response to {output_file}")

    # Send to TTS
    try:
        subprocess.run(["python", "response.py", output_file], check=True)
        print("🎤 Sent response to TTS successfully")
    except Exception as e:
        print(f"⚠ Error sending to TTS: {e}")
    finally:
        os.remove(output_file)

    return ai_text

def reply_from_file(input_file: str, language: str) -> str:
    """Read user's text and generate reply in selected language"""
    with open(input_file, "r", encoding="utf-8") as f:
        user_text = f.read().strip()
    return generate_reply(user_text, language)
