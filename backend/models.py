# import torch
# from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
# from datasets import load_dataset
# import soundfile as sf

# class RealTimeTTS:
#     def __init__(self, 
#                  tts_model="microsoft/speecht5_tts", 
# #                 llm_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):  # Mistral model
#                 llm_model="meta-llama/Llama-3.2-1B"):
#         # Load TTS model
#         self.synthesiser = pipeline("text-to-speech", tts_model)
#         self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
#         self.speaker_embedding = torch.tensor(self.embeddings_dataset[1000]["xvector"]).unsqueeze(0)


#         # Load model and tokenizer
#         quantization_config = BitsAndBytesConfig(load_in_4bit=True)
#         self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
#         self.model = AutoModelForCausalLM.from_pretrained(
#             llm_model, 
#             torch_dtype=torch.float16, 
#             device_map="auto",  # Auto-assigns to GPU if available
#             offload_folder="./offload"
#         )
#         self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

#     def get_llm_response(self, prompt):
#         response = self.generator(prompt, max_length=150, do_sample=True, temperature=0.3)
#         return response[0]["generated_text"]

#     def inference(self, text):
#         speech = self.synthesiser(text, forward_params={"speaker_embeddings": self.speaker_embedding})
#         return speech

#     def save_audio(self, speech, filename):
#         sf.write(filename, speech["audio"], samplerate=speech["sampling_rate"])

#     def run_real_time_tts(self, prompt, filename):
#         text = self.get_llm_response(prompt)
#         print(f"LLM Response: {text}")
#         speech = self.inference(text)
#         self.save_audio(speech, filename)

# # Example Usage
# tts_system = RealTimeTTS()
# tts_system.run_real_time_tts("Hi", "speech.wav")

import torch
import ollama
from transformers import pipeline
from datasets import load_dataset
from faiss_check import SemanticSearch
import soundfile as sf

class RealTimeTTS:
    def __init__(self, tts_model="microsoft/speecht5_tts", llm_model="llama3.2",faiss_model_path='output.csv'):
        # Load TTS model
        self.synthesiser = pipeline("text-to-speech", tts_model)
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(self.embeddings_dataset[7040]["xvector"]).unsqueeze(0)

        # Set up Ollama model name
        self.llm_model = llm_model
        self.faiss_model = SemanticSearch(faiss_model_path)
    
    def get_context_texts(self, prompt):
        self.faiss_model.load_data()
        self.faiss_model.preprocess_data()
        self.faiss_model.load_model()
        self.faiss_model.load_embeddings()
        self.faiss_model.create_faiss_index()
        self.faiss_model.load_faiss_index()
        context_texts = self.faiss_model.search(prompt)
        return context_texts[:3]


    # def get_llm_response(self, prompt):
    #     response = ollama.chat(model=self.llm_model, messages=[{"role": "user", "content": prompt}])
    #     return response["message"]["content"]

    def get_llm_response(self, prompt, context_texts):
        combined_prompt = f"{prompt}\n{context_texts[0]}\n{context_texts[1]}\n{context_texts[2]}"
        response = self.generator(combined_prompt, max_length=200)
        return response[0]['generated_text']


    def inference(self, text):
        speech = self.synthesiser(text, forward_params={"speaker_embeddings": self.speaker_embedding})
        return speech

    def save_audio(self, speech, filename):
        sf.write(filename, speech["audio"], samplerate=speech["sampling_rate"])

    def save_conversation(self, conversation_history, filename):
        with open(filename, 'w') as f:
            for turn in conversation_history:
                f.write(turn + '\n')

    # def run_real_time_tts(self, prompt, filename):
    #     text = self.get_llm_response(prompt)
    #     print(f"LLM Response: {text}")
    #     speech = self.inference(text)
    #     self.save_audio(speech, filename)

    def run_real_time_tts(self, prompt, filename):
        conversation_history = []
        while True:
            context_texts = self.get_context_texts(prompt)
            llm_response = self.get_llm_response(prompt, context_texts)
            conversation_history.append(f"User: {prompt}")
            conversation_history.append(f"LLM Response: {llm_response}")
            print(f"Context Texts: {context_texts}")
            print(f"LLM Response: {llm_response}")
            speech = self.inference(llm_response)
            self.save_audio(speech, filename)
            prompt = input("Enter next prompt (or 'quit' to exit): ")
            if prompt.lower() == 'quit':
                break
        self.save_conversation(conversation_history, 'conversation.txt')


# Example Usage
tts_system = RealTimeTTS()
tts_system.run_real_time_tts("What are the advantages of doing yoga daily,limit your answer in 90 words", "speech.wav")