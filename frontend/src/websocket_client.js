import { io } from "socket.io-client";

const socket = io("http://localhost:5001");

// Event: On connection
socket.on("connect", () => {
  console.log("Connected to the server!");
  socket.emit("speech", { duration: 5 }); // Send event to server
});

// Event: On disconnection
socket.on("disconnect", () => {
  console.log("Disconnected from the server!");
});

// Event: On transcription received
socket.on("transcription", (data) => {
  console.log("User said:", data.text);
});

// Event: On LLM response received
socket.on("llm_response", (data) => {
  console.log("Llama Model Response:", data.response);
});

// Event: On audio received
socket.on("audio", (data) => {
  console.log("Playing:", data.audio_file);
});

export default socket;
