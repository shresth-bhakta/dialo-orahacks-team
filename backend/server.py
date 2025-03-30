# import torch
# import soundfile as sf
# import numpy as np
# import io
# from flask import Flask
# from flask_socketio import SocketIO, emit
# from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
# from datasets import load_dataset
# from pydub import AudioSegment

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# @app.route("/")
# def home():
#     return "Flask-SocketIO Server is Running!"


# # Load Llama Model
# LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
# model = AutoModelForCausalLM.from_pretrained(LLM_MODEL, torch_dtype=torch.float16, device_map="auto")
# text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# # Load TTS Model
# TTS_MODEL = "microsoft/speecht5_tts"
# tts = pipeline("text-to-speech", TTS_MODEL)
# embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
# speaker_embedding = torch.tensor(embeddings_dataset[7040]["xvector"]).unsqueeze(0)

# @socketio.on("generate_speech")
# def handle_generate_speech(data):
#     """Handles the text input, generates LLM response, converts it to speech, and streams it."""
#     prompt = data.get("text", "")
#     print(f"Received Prompt: {prompt}")

#     # Generate response from Llama 2
#     response = text_generator(prompt, max_length=150, do_sample=True, temperature=0.2)
#     generated_text = response[0]["generated_text"]
#     print(f"Generated Text: {generated_text}")

#     # Convert text to speech
#     speech = tts(generated_text, forward_params={"speaker_embeddings": speaker_embedding})

#     # Convert raw numpy array to audio data
#     audio_data = speech["audio"]
#     sample_rate = speech["sampling_rate"]

#     # Convert numpy array to WAV format using Pydub
#     audio_segment = AudioSegment(
#         audio_data.astype("float32").tobytes(),
#         frame_rate=sample_rate,
#         sample_width=2,
#         channels=1
#     )

#     # Stream audio in small chunks
#     chunk_size = 1024  # Adjust for smoother playback
#     buffer = io.BytesIO()
#     audio_segment.export(buffer, format="wav")
#     buffer.seek(0)

#     while chunk := buffer.read(chunk_size):
#         socketio.emit("audio_chunk", {"chunk": chunk})

#     socketio.emit("audio_end")  # Signal completion
#     print("Streaming complete.")

# if __name__ == "__main__":
#     socketio.run(app, host="0.0.0.0", port=5001, debug=True)

import torch
import soundfile as sf
import numpy as np
import io
import ollama
from flask import Flask
from flask_socketio import SocketIO, emit
from transformers import pipeline
from datasets import load_dataset
from pydub import AudioSegment

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return "Flask-SocketIO Server is Running!"

# Load TTS Model
TTS_MODEL = "microsoft/speecht5_tts"
tts = pipeline("text-to-speech", TTS_MODEL)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7040]["xvector"]).unsqueeze(0)

@socketio.on("generate_speech")
def handle_generate_speech(data):
    """Handles the text input, generates LLM response, converts it to speech, and streams it."""
    prompt = data.get("text", "")
    print(f"Received Prompt: {prompt}")

    # Generate response from Ollama LLM
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    generated_text = response["message"]["content"]
    print(f"Generated Text: {generated_text}")

    # Convert text to speech
    speech = tts(generated_text, forward_params={"speaker_embeddings": speaker_embedding})

    # Convert raw numpy array to audio data
    audio_data = speech["audio"]
    sample_rate = speech["sampling_rate"]

    # Convert numpy array to WAV format using Pydub
    audio_segment = AudioSegment(
        audio_data.astype("float32").tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )

    # Stream audio in small chunks
    chunk_size = 1024  # Adjust for smoother playback
    buffer = io.BytesIO()
    audio_segment.export(buffer, format="wav")
    buffer.seek(0)

    while chunk := buffer.read(chunk_size):
        socketio.emit("audio_chunk", {"chunk": chunk})

    socketio.emit("audio_end")  # Signal completion
    print("Streaming complete.")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
