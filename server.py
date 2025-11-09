from gemini_api import reply_from_file

from flask import Flask, render_template, request, jsonify
import whisper
from pydub import AudioSegment
import uuid
import os
import subprocess


app = Flask(__name__)
model = whisper.load_model("base")  # you can change to "small" or "medium"
GEMINI_SCRIPT = "gemini_api.py"
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_audio():
    file = request.files["audio"]
    temp_name = f"temp_{uuid.uuid4()}.webm"
    file.save(temp_name)

    wav_path = temp_name.replace(".webm", ".wav")
    AudioSegment.from_file(temp_name).export(wav_path, format="wav")

    result = model.transcribe(wav_path)
    text = result["text"]

    os.remove(temp_name)
    os.remove(wav_path)


    input_file = f"user_input_{uuid.uuid4()}.txt"
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(text)
 
     # *** Generate the AI reply ***
    ai_reply = reply_from_file(input_file)
    print(f"Transcript type: {type(text)}, value: {text}")
    print(f"AI reply type: {type(ai_reply)}, value: {ai_reply}")

    return jsonify({"transcript": text, "ai_reply": ai_reply})


if __name__ == "__main__":
    app.run(debug=True)
