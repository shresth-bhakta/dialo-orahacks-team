// const express = require("express");
// const http = require("http");
// const socketIo = require("socket.io");
// const fs = require("fs");
// const path = require("path");
// const record = require("node-record-lpcm16");
// const wav = require("wav");
// const { Communicate } = require("edge-tts");
// const temp = require("temp");
// const os = require("os");
// const whisper = require("whisper");  // Import the whisper package

// const app = express();
// const server = http.createServer(app);
// const io = socketIo(server, { cors: { origin: "*" } });

// // Record audio until silence is detected
// function recordUntilSilence(samplerate = 16000, silenceDuration = 1.5, maxDuration = 15) {
//   return new Promise((resolve, reject) => {
//     console.log("Listening... Speak now!");

//     let audioData = [];
//     let silenceStart = null;
//     let startTime = Date.now();

//     const recorder = record.start({
//       sampleRateHertz: samplerate,
//       channels: 1,
//       audioType: "wav",
//     });

//     recorder.on("data", (chunk) => {
//       audioData.push(chunk);
//       const amplitude = Math.abs(chunk.readInt16LE(0)); // Check for silence

//       if (amplitude < 500) {
//         if (silenceStart === null) {
//           silenceStart = Date.now();
//         } else if ((Date.now() - silenceStart) > silenceDuration * 1000) {
//           console.log("Silence detected. Stopping recording.");
//           recorder.stop();
//           resolve(Buffer.concat(audioData)); // Resolve with the audio data
//         }
//       } else {
//         silenceStart = null;
//       }

//       // Stop if max duration is reached
//       if (Date.now() - startTime >= maxDuration * 1000) {
//         recorder.stop();
//         resolve(Buffer.concat(audioData));
//       }
//     });

//     recorder.on("error", (err) => {
//       reject(err);
//     });
//   });
// }

// // Save the recorded audio as a WAV file
// function saveWav(filename, audioData) {
//   return new Promise((resolve, reject) => {
//     const fileStream = fs.createWriteStream(filename);
//     const wavEncoder = new wav.Writer({
//       sampleRate: 16000,
//       channels: 1,
//       bitDepth: 16,
//     });

//     fileStream.on("finish", resolve);
//     fileStream.on("error", reject);

//     wavEncoder.pipe(fileStream);
//     wavEncoder.write(audioData);
//     wavEncoder.end();
//   });
// }

// // WebSocket event to handle speech processing
// io.on("connection", (socket) => {
//   console.log("WebSocket connection established");

//   socket.on("speech", async (data) => {
//     console.log("Received speech data");

//     try {
//       // Record audio from the user
//       const audioData = await recordUntilSilence();
//       const tempAudioFile = path.join(os.tmpdir(), "audio.wav");

//       // Save the recorded audio
//       await saveWav(tempAudioFile, audioData);

//       // Convert speech to text using Whisper
//       const transcriptionResult = await whisper.transcribe(tempAudioFile);  // Use whisper package to transcribe the audio
//       const transcription = transcriptionResult.text;

//       // Cleanup the temp audio file
//       fs.unlinkSync(tempAudioFile);

//       // Emit the transcription back to the client
//       socket.emit("transcription", { text: transcription });

//       // Process the transcription with an LLM (e.g., Ollama)
//       if (transcription.trim()) {
//         const llmResponse = await fetch("http://localhost:5001/chat", {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify({ model: "llama3.2", messages: [{ role: "user", content: transcription }] }),
//         });
//         const llmData = await llmResponse.json();
//         const responseText = llmData.message.content;

//         // Emit the LLM response back to the client
//         socket.emit("llm_response", { response: responseText });

//         // Convert the LLM response to speech
//         await textToSpeech(responseText, socket);
//       }
//     } catch (error) {
//       console.error("Error processing speech:", error);
//     }
//   });
// });

// // Convert text to speech using Edge TTS
// async function textToSpeech(text, socket) {
//   try {
//     const audioOutputPath = path.join(os.tmpdir(), "output.mp3");
//     const communicate = new Communicate(text, "en-US-JennyNeural");

//     await communicate.save(audioOutputPath);

//     // Emit the audio file back to the client
//     socket.emit("audio", { audio_file: audioOutputPath });
//   } catch (error) {
//     console.error("Error generating speech:", error);
//   }
// }

// // Start the server
// server.listen(5001, () => {
//   console.log("Server running on http://localhost:5001");
// });



const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const fs = require("fs");
const path = require("path");
const whisper = require("@openai/whisper-stt-browser"); // Placeholder for Whisper integration
const { exec } = require("child_process");

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

// Placeholder for Whisper model loading
const sttModel = "tiny.en"; // Replace with actual model loading logic

// Function to simulate recording audio until silence
const recordUntilSilence = () => {
  console.log("Simulating audio recording...");
  return Buffer.from("dummy_audio_data"); // Replace with actual audio data
};

// Function to save audio as a WAV file
const saveWav = (filename, audioData) => {
  fs.writeFileSync(filename, audioData);
};

// WebSocket event for speech processing
io.on("connection", (socket) => {
  console.log("Client connected!");

  socket.on("speech", async (data) => {
    console.log("Speech event received!");

    // Simulate recording audio
    const audioData = recordUntilSilence();

    // Save audio to a temporary file
    const tempFilename = path.join(__dirname, "temp_audio.wav");
    saveWav(tempFilename, audioData);

    // Simulate speech-to-text transcription
    const transcription = "Simulated transcription"; // Replace with actual transcription logic
    console.log("Transcription:", transcription);

    // Emit transcription back to the client
    socket.emit("transcription", { text: transcription });

    // Simulate LLM response
    const llmResponse = "Simulated LLM response"; // Replace with actual LLM logic
    console.log("LLM Response:", llmResponse);

    // Emit LLM response back to the client
    socket.emit("llm_response", { response: llmResponse });

    // Simulate text-to-speech conversion
    const audioFile = path.join(__dirname, "response_audio.wav");
    exec(`echo "Simulated TTS audio" > ${audioFile}`); // Replace with actual TTS logic

    // Emit audio file back to the client
    socket.emit("audio", { audio_file: audioFile });

    // Cleanup temporary files
    fs.unlinkSync(tempFilename);
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected!");
  });
});

// Start the server
const PORT = 5001;
server.listen(PORT, () => {
  console.log(`WebSocket server running on http://localhost:${PORT}`);
});
