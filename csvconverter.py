import PyPDF2
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize


nltk.download('punkt')

def pdf_to_csv(pdf_path, output_csv):


    
    with open(pdf_path, 'rb') as pdf_file:
        
        pdf_reader = PyPDF2.PdfReader(pdf_file)

       
        sentences = []

        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
           
            sentences.extend(sent_tokenize(text))

    
    df = pd.DataFrame({'body': sentences})

    
    df.to_csv(output_csv, index=True, index_label='index')

if __name__ == "__main__":
    pdf_path = 'input.pdf'
    output_csv = 'output2.csv'

    pdf_to_csv(pdf_path, output_csv)
    print("PDF converted to CSV successfully!")