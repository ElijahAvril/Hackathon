from flask import Flask, render_template, request, jsonify
import whisper
from pydub import AudioSegment
import uuid
import os

app = Flask(__name__)
model = whisper.load_model("base")  # you can change to "small" or "medium"

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

    return jsonify({"transcript": text})

if __name__ == "__main__":
    app.run(debug=True)
