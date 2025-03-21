import nltk
from nltk.tokenize import sent_tokenize
import csv
nltk.download('punkt_tab')
# Load the text file
with open('output.txt', 'r') as f:
    text = f.read()

# Split the text into sentences
sentences = sent_tokenize(text)

# Initialize an empty list to store the contextual blocks
context_blocks = []

# Iterate through the sentences and group them into blocks
block = []
for sentence in sentences:
    if sentence.endswith('.'):  # Assuming paragraphs end with a period
        block.append(sentence)
        context_blocks.append(block)
        block = []
    else:
        block.append(sentence)

# Handle the last block if it doesn't end with a period
if block:
    context_blocks.append(block)

# Open the CSV file for writing
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Index', 'Body'])

    # Write each contextual block to the CSV file
    for i, block in enumerate(context_blocks):
        body = ' '.join(block)
        writer.writerow([i, body])