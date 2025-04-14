const socket = io("http://localhost:5001");
let isRecording = false;

const micBtn = document.getElementById("micBtn");
const chatBox = document.getElementById("chat");

micBtn.addEventListener("click", () => {
    if (!isRecording) {
        socket.emit("start_recording");
        micBtn.textContent = "🛑 Stop Recording";
        micBtn.classList.remove("btn-danger");
        micBtn.classList.add("btn-secondary");
    } else {
        socket.emit("stop_recording");
        micBtn.textContent = "🎙️ Start Recording";
        micBtn.classList.remove("btn-secondary");
        micBtn.classList.add("btn-danger");
    }
    isRecording = !isRecording;
});

socket.on("status", (data) => {
    console.log("Status:", data.message);
});

// socket.on("audio", (data) => {
//     const audio = new Audio(data.audio_file);
//     audio.play().catch(error => {
//         console.error("Audio playback failed:", error);
//     });
// });

socket.on("audio", (data) => {
    // Add timestamp to bypass browser cache
    const audioUrl = `${data.audio_file}?t=${Date.now()}`;
    const audio = new Audio(audioUrl);
    audio.play().catch(error => {
        console.error("Audio playback failed:", error);
    });
});


socket.on("transcription", (data) => {
    const msg = document.createElement("div");
    msg.className = "user-msg";
    msg.textContent = `🗣️ You: ${data.text}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("llm_response", (data) => {
    const msg = document.createElement("div");
    msg.className = "llm-msg";
    msg.textContent = `🤖 LLM: ${data.response}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("error", (data) => {
    alert("Error: " + data.message);
});
