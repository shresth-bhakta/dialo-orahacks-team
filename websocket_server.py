# from flask import Flask
# from flask_socketio import SocketIO, emit
# import ollama
# import whisper
# import sounddevice as sd
# import numpy as np
# import wave
# import tempfile
# import os
# import asyncio
# from edge_tts import Communicate
# import time

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Load Whisper model for STT
# stt_model = whisper.load_model("base.en")

# # Function to record audio until silence is detected
# def record_until_silence(samplerate=16000, silence_duration=2, max_duration=15):
#     print("Listening... Speak now!")
#     audio_data = []
#     silence_start = None
#     start_time = time.time()

#     while time.time() - start_time < max_duration:
#         frame = sd.rec(int(samplerate * 0.5), samplerate=samplerate, channels=1, dtype="int16")  # 0.5 sec chunks
#         sd.wait()
#         audio_data.extend(frame)

#         # Check if last frames are silent
#         amplitude = np.abs(np.array(frame, dtype=np.int16))
#         if np.mean(amplitude) < 500:  # Silence threshold
#             if silence_start is None:
#                 silence_start = time.time()
#             elif time.time() - silence_start > silence_duration:
#                 print("Silence detected. Stopping recording.")
#                 break
#         else:
#             silence_start = None  # Reset if speech resumes

#     return np.array(audio_data, dtype=np.int16)

# # Save recorded audio as WAV
# def save_wav(filename, audio_data, samplerate=16000):
#     with wave.open(filename, "wb") as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(2)
#         wf.setframerate(samplerate)
#         wf.writeframes(audio_data.tobytes())

# # WebSocket event for speech processing
# @socketio.on("speech")
# def handle_speech(data):
#     print("received websocket connection")
#     audio_data = record_until_silence()

#     # Save audio to temp file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#         save_wav(temp_audio.name, audio_data)
#         temp_filename = temp_audio.name

#     # Convert speech to text
#     result = stt_model.transcribe(temp_filename)
#     os.remove(temp_filename)  # Cleanup
#     transcription = result["text"]

#     # Emit full transcribed text back to client
#     emit("transcription", {"text": transcription})

#     # *** FIX: Only send final query to LLM once user stops speaking ***
#     if transcription.strip():
#         llm_response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": transcription}])
#         response_text = llm_response["message"]["content"]

#         # Emit LLM response
#         emit("llm_response", {"response": response_text})

#         # Convert LLM response to speech
#         asyncio.run(text_to_speech(response_text))

# # Convert text to speech
# async def text_to_speech(text):
#     audio_output = "output.mp3"
#     communicate = Communicate(text, "en-US-JennyNeural")
#     await communicate.save(audio_output)

#     # Emit audio file
#     socketio.emit("audio", {"audio_file": audio_output})

# # Start server
# if __name__ == "__main__":
#     socketio.run(app, host="0.0.0.0", port=5001, debug=True)


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
import threading
from faiss_check import SemanticSearch

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load Whisper model
stt_model = whisper.load_model("medium")

# Globals
recording_buffer = []
is_recording = False



def get_contextualized_query(prompt):
        # order_id = self.get_order_id_from_user()
        semantic_search = SemanticSearch('Orders.csv')
        context_data = semantic_search.run_search(prompt)
        # contextualized_query = f"You are customer care agent,and give the answer to '{prompt}' only using {', '.join(map(str, context_data.values()))}, such that there can be an answer within these sentences? Find the related data and provide the answer. Additionally, if the answer contains digits, please convert them to single digit words.(e.g., 1 to One, 2 to Two,0 to zero and ignore +,- etc.),Do not give more extra information more than user asked ."
        
        return context_data
        # else : return {', '.join(map(str, context_data.values()))}

# Background recording function
def background_recording():
    global is_recording, recording_buffer
    print("🎙️ Recording started (float32)...")

    samplerate = 16000
    recording_buffer = []

    while is_recording:
        frame = sd.rec(int(samplerate * 0.5), samplerate=samplerate, channels=1, dtype="float32")
        sd.wait()
        recording_buffer.extend(frame)

    print("🛑 Recording stopped.")

# Normalize and convert to float32
def normalize_and_convert(audio):
    audio_np = np.array(audio, dtype=np.float32)
    max_val = np.max(np.abs(audio_np), initial=1)
    if max_val > 0:
        audio_np /= max_val
    return audio_np

# Save WAV
def save_wav(filename, audio_data, samplerate=16000):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

# SocketIO: Start Recording
@socketio.on("start_recording")
def handle_start_recording():
    global is_recording, recording_buffer
    if is_recording:
        return emit("status", {"message": "Already recording!"})
    
    is_recording = True
    recording_buffer = []
    threading.Thread(target=background_recording, daemon=True).start()
    emit("status", {"message": "Recording started."})

# SocketIO: Stop Recording
@socketio.on("stop_recording")
def handle_stop_recording():
    global is_recording, recording_buffer
    if not is_recording:
        return emit("status", {"message": "Recording was not started."})

    is_recording = False
    emit("status", {"message": "Recording stopped. Processing..."})

    # Convert buffer to numpy array
    audio_np = np.array(recording_buffer, dtype=np.float32).flatten()

    # Directly pass to Whisper
    try:
        result = stt_model.transcribe(audio_np, language='en', fp16=False)  # Use fp16=False for better CPU support
        transcription = result["text"].strip()
        emit("transcription", {"text": transcription})
    except Exception as e:
        emit("error", {"message": f"Transcription failed: {e}"})
        return


    
    # Query LLM if transcription exists
    if transcription:
        new_prompt = get_contextualized_query(transcription)
        if(new_prompt.length() == 0) : 
            query = f"You are customer care agent,and give the answer to '{transcription}'  and ask user to provide order id as he has not provided, such that there can be an answer within these sentences?"
            llm_response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": query}])
            response_text = llm_response["message"]["content"]
            emit("llm_response", {"response": response_text})
            asyncio.run(text_to_speech(response_text))
        else:
            contextualized_query = f"You are customer care agent,and give the answer to '{transcription}' only using {new_prompt}, such that there can be an answer within these sentences? Find the related data and provide the answer. Additionally, if the answer contains digits, please convert them to single digit words.(e.g., 1 to One, 2 to Two,0 to zero and ignore +,- etc.),Do not give more extra information more than user asked ."
            llm_response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": contextualized_query}])
            response_text = llm_response["message"]["content"]
            # response = ollama.chat(model=self.llm_model, messages=[{"role": "user", "content": prompt}])
            # response_text = response["message"]["content"]
            emit("llm_response", {"response": response_text})
            asyncio.run(text_to_speech(response_text))
    

          
            
            
# TTS with edge-tts
async def text_to_speech(text):
    audio_output = "output.mp3"
    communicate = Communicate(text, "en-US-JennyNeural")
    await communicate.save(audio_output)

    # Send audio to client
    socketio.emit("audio", {"audio_file": audio_output})

# Start server
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)





