let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");
const statusText = document.getElementById("status");
const userText = document.getElementById("userText");
const playback = document.getElementById("playback");
const chatLog = document.getElementById("chatLog");

startBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = handleStop;

    mediaRecorder.start();
    statusText.textContent = "Recording...";
    startBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    statusText.textContent = "Processing...";
    startBtn.disabled = false;
    stopBtn.disabled = true;
};

function handleStop() {
    // Make audio playable
    const blob = new Blob(audioChunks, { type: "audio/webm" });
    const audioURL = URL.createObjectURL(blob);
    playback.src = audioURL;

    // Send to server for transcription
    sendAudio(blob);
}

async function sendAudio(blob) {
    const formData = new FormData();
    formData.append("audio", blob, "audio.webm");

    const response = await fetch("/process", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    userText.textContent = data.transcript;
    statusText.textContent = "Done!";

    addToChatLog(data.transcript);
}

function addToChatLog(text) {
    const msg = document.createElement("div");
    msg.className = "msg";
    msg.textContent = text;
    chatLog.appendChild(msg);

    // auto scroll to newest message
    chatLog.scrollTop = chatLog.scrollHeight;
}
