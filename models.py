import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from datasets import load_dataset
import soundfile as sf

class RealTimeTTS:
    def __init__(self, 
                 tts_model="microsoft/speecht5_tts", 
                 llm_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):  # Mistral model
        # Load TTS model
        self.synthesiser = pipeline("text-to-speech", tts_model)
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(self.embeddings_dataset[1000]["xvector"]).unsqueeze(0)


        # Load model and tokenizer
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
        self.model = AutoModelForCausalLM.from_pretrained(
            llm_model, 
            torch_dtype=torch.float16, 
            device_map="auto",  # Auto-assigns to GPU if available
            offload_folder="./offload"
        )
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def get_llm_response(self, prompt):
        response = self.generator(prompt, max_length=150, do_sample=True, temperature=0.3)
        return response[0]["generated_text"]

    def inference(self, text):
        speech = self.synthesiser(text, forward_params={"speaker_embeddings": self.speaker_embedding})
        return speech

    def save_audio(self, speech, filename):
        sf.write(filename, speech["audio"], samplerate=speech["sampling_rate"])

    def run_real_time_tts(self, prompt, filename):
        text = self.get_llm_response(prompt)
        print(f"LLM Response: {text}")
        speech = self.inference(text)
        self.save_audio(speech, filename)

# Example Usage
tts_system = RealTimeTTS()
tts_system.run_real_time_tts("Hi", "speech.wav")
