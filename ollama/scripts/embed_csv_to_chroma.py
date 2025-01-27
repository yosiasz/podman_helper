import uuid
import pandas as pd
import ollama
import chromadb
from transformers import AutoTokenizer, AutoModel
import torch

# Initialize ChromaDB client
chroma_path = './chroma_persistent_storage/'
client = chromadb.PersistentClient(chroma_path)

#client = chromadb.Client()
# Create a ChromaDB collection for storing embeddings
collection_name = "nanu_nanu_neyi"
collection = client.get_or_create_collection(collection_name)


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('./data/cars.csv')

# Initialize Ollama client (assuming Ollama is installed and running)
ollama_client = ollama

# Load the model and tokenizer (for text embeddings)
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to generate embeddings for texts
def generate_embeddings(texts):
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
        #print('embeddings', embeddings)
    return embeddings.numpy()

# Function to generate embeddings using Ollama
def get_embeddings(text):
    response = ollama_client.embed('llama3.2',text)
    #print('embedding', response)
    return response['embeddings']

id = 0
# Iterate through rows in the DataFrame and generate embeddings
for index, row in df.iterrows():
    id += 1
    # Extract the text from the CSV (assuming a column 'text')
    text = row['text']  # Modify if your CSV has a different structure
    
    # Generate embedding for the text
    #embedding = get_embeddings(text)
    embedding = get_embeddings(text)
    unique_id = str(uuid.uuid4()) 
    try:
    # Store the embedding and metadata in ChromaDB
        collection.add(
            ids=[unique_id],
            embeddings=[embedding],
            metadatas=[{'row_index': index, 'text': text}],
            documents=[text]
        )
    except Exception as e:
        print("An error occurred:", str(e))


print("CSV data successfully embedded into ChromaDB.")

def retrieve_from_chroma(query, k=3):
    query_embedding = generate_embeddings([query])[0]
    
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    print('retrieve_from_chroma results', results)
    return results['documents']

# Function to generate an answer using Ollama
def generate_answer_with_ollama(query, context):
    input_text = f"Question: {query}\nContext: {context}"
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": input_text}])
    return response['text']

# Example query
query = "What did the fox do?"
retrieved_docs = retrieve_from_chroma(query)

#print(retrieved_docs)
# Combine the retrieved documents into a single context
#context = " ".join(retrieved_docs)

# Generate the final answer with Ollama
#answer = generate_answer_with_ollama(query, context)
#print(f"Answer: {answer}")