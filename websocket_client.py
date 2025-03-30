import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server!")
    sio.emit("speech", {"duration": 5})  # Send event to server

@sio.event
def disconnect():
    print("Disconnected from the server!")

@sio.on("transcription")
def on_transcription(data):
    print("User said:", data["text"])

@sio.on("llm_response")
def on_llm_response(data):
    print("Llama Model Response:", data["response"])

@sio.on("audio")
def on_audio(data):
    print("Playing:", data["audio_file"])

try:
    sio.connect("http://localhost:5001")
    print("Successfully connected!")
except Exception as e:
    print("Connection failed:", e)

sio.wait()  # Keeps the connection open for receiving responses


