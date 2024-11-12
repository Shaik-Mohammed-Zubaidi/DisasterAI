# Disaster recovery
import requests
from dotenv import load_dotenv
import os
import re


# to implement later
# query_counter = 0

load_dotenv()


# Define the data directory for local files
data_folder = './rag_data'

def load_documents():

    # Function to load content from all text files in a directory recursively
    def load_files_from_folder(folder_path):
        documents = []
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            return documents

        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.endswith('.txt'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        documents.append(file_content)
                        print(f"Loaded content from {file_path}")
        return documents

    # Load documents from the root folder recursively
    try:
        documents = load_files_from_folder(data_folder)
        print(f"Total documents loaded: {len(documents)}", documents)
    except Exception as e:
        print(f"Error loading documents: {e}")

    print(f"Loaded {len(documents)} documents")
    return documents



### RAG pipeline

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load SentenceTransformer model for FAISS
print("Loading SentenceTransformer model...")
# model = SentenceTransformer('Alibaba-NLP/gte-base-en-v1.5', trust_remote_code=True)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("SentenceTransformer Model loaded successfully.")


# # Check if MPS is available, otherwise default to CPU
# device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
# print(f"Using device: {device}")

# # Rank-BERT model and tokenizer for reranking (using a smaller model for compatibility)
# rank_bert_model_name = "castorini/monobert-base-msmarco"
# rank_bert_model = AutoModelForSequenceClassification.from_pretrained(rank_bert_model_name).to(device)
# rank_bert_tokenizer = AutoTokenizer.from_pretrained(rank_bert_model_name)

# Rank-BERT model and tokenizer for reranking
rank_bert_model = AutoModelForSequenceClassification.from_pretrained("castorini/monobert-large-msmarco-finetune-only")
rank_bert_tokenizer = AutoTokenizer.from_pretrained("castorini/monobert-large-msmarco-finetune-only")

# T5 model and tokenizer for answer generation (using T5-base for compatibility)
t5_model_name = "t5-large"
t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name)
t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name)

print("Models loaded successfully.")

def get_answer_rag(query, documents):
    # Convert documents to embeddings
    print("Converting documents to embeddings...")
    document_embeddings = model.encode(documents, normalize_embeddings=True)
    # print(document_embeddings)
    print("Documents converted to embeddings.")

    # Initialize FAISS index
    d = document_embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(np.array(document_embeddings))

    # Function to rerank documents using Rank-BERT
    def rerank_with_rank_bert(query, retrieved_docs):
        inputs = []
        for doc in retrieved_docs:
            inputs.append(rank_bert_tokenizer.encode_plus(query, doc, return_tensors='pt', truncation=True))

        scores = []
        with torch.no_grad():
            for input_data in inputs:
                outputs = rank_bert_model(**input_data)
                score = outputs.logits[0][1].item()  # Assuming binary classification for ranking
                scores.append(score)
        print("Reranking complete.")
        doc_scores = list(zip(retrieved_docs, scores))
        ranked_docs = sorted(doc_scores, key=lambda x: x[1], reverse=True)
        return [doc for doc, score in ranked_docs]

    # Function to generate an answer using T5 model
    def generate_answer_with_t5(query, context):
        print("Generating answer...")
        prompt = f"QUESTION: {query}, CONTEXT: {context}"
        inputs = t5_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = t5_model.generate(inputs.input_ids, max_length=300, num_beams=10, early_stopping=True)
        return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Function to extract phone numbers from text
    def extract_phone_numbers(text):
        # Regex pattern for phone numbers (adjust as needed for different formats)
        phone_pattern = r'\(?\b\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phone_numbers = list(set(re.findall(phone_pattern, text)))
        return " ".join(phone_numbers)

    # RAG pipeline with FAISS, reranking, and T5 model
    def rag_pipeline(query):
        # Step 1: Retrieve relevant documents from FAISS
        query_embedding = model.encode([query])
        D, I = index.search(query_embedding, k=5)  # Retrieve top 5 documents
        
        retrieved_docs = [documents[i] for i in I[0]]
        print("Documents retrieved.")

        # Step 2: Rerank using Rank-BERT
        reranked_docs = rerank_with_rank_bert(query, retrieved_docs)

        # Step 3: Generate an answer using T5
        context = " ".join(reranked_docs)  # Joining reranked docs as context
        answer = generate_answer_with_t5(query, context)
        phone_numbers = extract_phone_numbers(answer)
        print("Answer generated.", phone_numbers, answer)
        if("number" in query):
            return phone_numbers
        return answer

    # Test the pipeline with the query
    answer = rag_pipeline(query)
    print(f"Answer: {answer}")

    # Save the query and answer to a text file
    # folder_name = './query_answers'
    folder_name = os.path.join(data_folder, 'query_answers')
    os.makedirs(folder_name, exist_ok=True)

    # Define the filename
    filename = os.path.join(folder_name, f"{query}_query_answer.txt")

    # Save the query and answer to the text file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Query: {query}\n\n")
        file.write(f"Answer: {answer}\n")

    print(f"Query and answer saved to {filename}")
    return answer
