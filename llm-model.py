from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama


# Define a prompt template for the chatbot
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a knowledgable , resourceful and experienced Q&A specialist. Please respond to the questions"),
        ("user","Question:{question}")
    ]
)

# Initialize the Ollama model
llm=Ollama(model="llama3.2")

# Create a chain that combines the prompt and the Ollama model
chain=prompt|llm

prompt = input("Hey!!!How can I help you \n")
# Invoke the chain with the input text and display the output
response = chain.invoke({"question":prompt})

print(response)