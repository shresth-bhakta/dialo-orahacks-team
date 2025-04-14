import torch
import ollama
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import inflect
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
class RealTimeTTS:
    def __init__(self, tts_model="microsoft/speecht5_tts", llm_model="llama3.2"):
        # Load TTS model
        self.synthesiser = pipeline("text-to-speech", tts_model)
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(self.embeddings_dataset[7040]["xvector"]).unsqueeze(0)
        self.data = pd.read_csv('orders.csv', encoding='latin1')
        # Set up Ollama model name
        self.llm_model = llm_model
        self.p = inflect.engine()
    def get_order_id_from_user(self):
        while True:
            try:
                order_id = int(input("What is the order ID of the product? "))
                return order_id
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    def get_context_from_df(self, order_id):
        try:
            result = self.data.query(f'Order_ID == {order_id}')
            if result.empty:
                raise ValueError("Order ID not found.")
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    def get_contextualized_query(self, prompt):
        order_id = self.get_order_id_from_user()
        context_data = self.get_context_from_df(order_id).to_dict(orient='records')[0]
        contextualized_query = f"You are customer care agent,and give the answer to '{prompt}' only using {', '.join(map(str, context_data.values()))}, such that there can be an answer within these sentences? Find the related data and provide the answer. Additionally, if the answer contains digits, please convert them to single digit words.(e.g., 1 to One, 2 to Two,0 to zero and ignore +,- etc.),Do not give more extra information more than user asked ."
        return contextualized_query
    # def get_llm_response(self, prompt):
    #     response = ollama.chat(model=self.llm_model, messages=[{"role": "user", "content": prompt}])
    #     return response["message"]["content"]
    def get_llm_response(self, prompt):
        response = ollama.chat(model=self.llm_model, messages=[{"role": "user", "content": prompt}])
        text = response["message"]["content"]
        # Convert numeric digits to words
        import re
        numbers = re.findall(r'\d', text)
        for num in numbers:
            text = text.replace(num, self.p.number_to_words(num))
        return text
    def inference(self, text):
        speech = self.synthesiser(text, forward_params={"speaker_embeddings": self.speaker_embedding})
        return speech
    def save_audio(self, speech, filename):
        sf.write(filename, speech["audio"], samplerate=speech["sampling_rate"])
    def run_real_time_tts(self, prompt, filename):
        contextualized_query = self.get_contextualized_query(prompt)
        print(f"Contextualized Query: {contextualized_query}")
        text = self.get_llm_response(contextualized_query)
        print(f"LLM Response: {text}")
        speech = self.inference(text)
        self.save_audio(speech, filename)
# Example Usage
# tts_system = RealTimeTTS()
# tts_system.run_real_time_tts("What are products I order?", "speech.wav")