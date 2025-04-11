# import socketio

# sio = socketio.Client()

# @sio.event
# def connect():
#     print("Connected to the server!")
#     sio.emit("speech", {"duration": 5})  # Send event to server

# @sio.event
# def disconnect():
#     print("Disconnected from the server!")

# @sio.on("transcription")
# def on_transcription(data):
#     print("User said:", data["text"])

# @sio.on("llm_response")
# def on_llm_response(data):
#     print("Llama Model Response:", data["response"])

# @sio.on("audio")
# def on_audio(data):
#     print("Playing:", data["audio_file"])

# try:
#     sio.connect("http://localhost:5001")
#     print("Successfully connected!")
# except Exception as e:
#     print("Connection failed:", e)

# sio.wait()  # Keeps the connection open for receiving responses


import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to the server!")

    # Step 1: Start recording
    print("🎤 Starting recording...")
    sio.emit("start_recording")

    # Simulate user speaking for a while, then stop
    time.sleep(10)  # Wait for 10 seconds (you can replace with input() or a button trigger)

    # Step 2: Stop recording
    print("🛑 Stopping recording...")
    sio.emit("stop_recording")

@sio.event
def disconnect():
    print("🔌 Disconnected from the server!")

@sio.on("status")   #not useful for the connection
def on_status(data):
    print("ℹ️ Server Status:", data["message"])

@sio.on("transcription")
def on_transcription(data):
    print("📝 User said:", data["text"])

@sio.on("llm_response")
def on_llm_response(data):
    print("🤖 LLM Response:", data["response"])

@sio.on("audio")
def on_audio(data):
    print("🔊 Playing:", data["audio_file"])
  # You can use a media player to play this

try:
    sio.connect("http://localhost:5001")
except Exception as e:
    print("❌ Connection failed:", e)

sio.wait()  # Keep the connection open



