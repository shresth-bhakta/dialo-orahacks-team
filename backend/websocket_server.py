from flask import Flask
from flask_socketio import SocketIO, emit
import ollama
import whisper
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import asyncio
from edge_tts import Communicate
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load Whisper model for STT
stt_model = whisper.load_model("base")

# Function to record audio until silence is detected
def record_until_silence(samplerate=16000, silence_duration=1.5, max_duration=15):
    print("Listening... Speak now!")
    audio_data = []
    silence_start = None
    start_time = time.time()

    while time.time() - start_time < max_duration:
        frame = sd.rec(int(samplerate * 0.5), samplerate=samplerate, channels=1, dtype="int16")  # 0.5 sec chunks
        sd.wait()
        audio_data.extend(frame)

        # Check if last frames are silent
        amplitude = np.abs(np.array(frame, dtype=np.int16))
        if np.mean(amplitude) < 500:  # Silence threshold
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > silence_duration:
                print("Silence detected. Stopping recording.")
                break
        else:
            silence_start = None  # Reset if speech resumes

    return np.array(audio_data, dtype=np.int16)

# Save recorded audio as WAV
def save_wav(filename, audio_data, samplerate=16000):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

# WebSocket event for speech processing
@socketio.on("speech")
def handle_speech(data):
    print("received websocket connection")
    audio_data = record_until_silence()

    # Save audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        save_wav(temp_audio.name, audio_data)
        temp_filename = temp_audio.name

    # Convert speech to text
    result = stt_model.transcribe(temp_filename)
    os.remove(temp_filename)  # Cleanup
    transcription = result["text"]

    # Emit full transcribed text back to client
    emit("transcription", {"text": transcription})

    # *** FIX: Only send final query to LLM once user stops speaking ***
    if transcription.strip():
        llm_response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": transcription}])
        response_text = llm_response["message"]["content"]

        # Emit LLM response
        emit("llm_response", {"response": response_text})

        # Convert LLM response to speech
        asyncio.run(text_to_speech(response_text))

# Convert text to speech
async def text_to_speech(text):
    audio_output = "output.mp3"
    communicate = Communicate(text, "en-US-JennyNeural")
    await communicate.save(audio_output)

    # Emit audio file
    socketio.emit("audio", {"audio_file": audio_output})

# Start server
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)


