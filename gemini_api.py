
import os
from typing import List, Dict
import dotenv
from google import genai
from google.genai import types



dotenv.load_dotenv()

GEMINI_KEY = os.getenv("Gemini_Api_Key")
if not GEMINI_KEY:
    raise RuntimeError("Gemini_Api_Key not set in environment")

# configure gemini
client = genai.Client(api_key=GEMINI_KEY)

# choose model (change if you have different access)
MODEL_NAME = "gemini-2.5-flash"
history = []


def _build_prompt(user_text: str, history: List[Dict[str, str]], target_lang: str | None) -> str:
    """
    Build a single string prompt for Gemini from history + current user text.
    We prefix with a system line to instruct language.
    """
    if target_lang:
        system_line = f"System: You are a helpful assistant. Always reply in {target_lang}."
    else:
        system_line = "System: You are a helpful multilingual assistant."

    lines = [system_line]
    for msg in history:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    lines.append(f"User: {user_text}")
    lines.append("Assistant:")
    return "\n".join(lines)

def generate_reply(
    user_text: str,
    history: List[Dict[str, str]] | None = None,
    target_lang: str | None = None,
    max_tokens: int = 800
) -> str:
    if history is None:
        history = []
    history.append({"role": "user", "content": user_text})
    prompt = _build_prompt(user_text, history, target_lang)

    config = types.GenerateContentConfig(
        max_output_tokens = max_tokens
    )

    # Create the request using the new SDK
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config=config
    )

    # Extract text safely
    if response and response.text:
        return response.text.strip()
    else:
        return "I'm sorry, I couldn't generate a response."


if __name__ == "__main__":
    # Simple test
    user_input = "Hello, how are you?"
    reply = generate_reply(user_input,history)
    print(reply)
    reply2 = generate_reply("What is currently in your context?", history)
    print(reply2)