import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import faiss
import os

class SemanticSearch:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.model = None
        self.index = None
        self.embeddings_file = 'embeddings.npy'


    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def preprocess_data(self):
        def extract(txt):
            return txt.strip()

        self.df['Body'] = self.df['Body'].apply(lambda x: extract(x))

    def load_model(self):
        self.model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
        #self.model = SentenceTransformer('Salesforce/SFR-Embedding-Mistral')

    def load_embeddings(self):
        if os.path.exists(self.embeddings_file):
            self.df['Embeddings'] = np.load(self.embeddings_file, allow_pickle=True)
        else:
            self.compute_embeddings()
            np.save(self.embeddings_file, self.df['Embeddings'])

    def compute_embeddings(self):
        self.df['Embeddings'] = self.df['Body'].apply(lambda x: self.model.encode([x])[0])

    def create_faiss_index(self):
        body_texts = self.df["Body"].tolist()
        body_embeddings = self.model.encode(body_texts)
        self.index = faiss.IndexFlatL2(body_embeddings.shape[1])
        self.index.add(body_embeddings)
        faiss.write_index(self.index, 'index_body_texts')

    def load_faiss_index(self):
        self.index = faiss.read_index('index_body_texts')

    def search(self, query):
        query_vector = self.model.encode([query])
        k = 5
        top_k = self.index.search(query_vector, k)  # top3 only
        body_texts = self.df["Body"].tolist()
        return [body_texts[_id] for _id in top_k[1].tolist()[0]]

    def run_search(self, query):
        self.load_data()
        self.preprocess_data()
        self.load_model()
        self.compute_embeddings()
        self.create_faiss_index()
        self.load_faiss_index()
        results = self.search(query)
        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in body texts:\n")
        for r in enumerate(results, start=1):
            print(f"{r[0]}). {r[1]}")
    def ask_repeated_questions(self):
        while True:
            query = input("Enter your question (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            results = self.search(query)
            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop 5 most similar sentences in body texts:\n")
            for r in enumerate(results, start=1):
                print(f"{r[0]}). {r[1]}")

# Usage
# semantic_search = SemanticSearch('output.csv')
# #semantic_search.run_search('What is college name?')
# semantic_search.load_data()
# semantic_search.preprocess_data()
# semantic_search.load_model()
# semantic_search.load_embeddings()
# semantic_search.create_faiss_index()
# semantic_search.load_faiss_index()
# semantic_search.ask_repeated_questions()

