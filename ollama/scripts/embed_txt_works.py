import uuid
import requests
import chromadb
import ollama


# Initialize ChromaDB client
#chroma_path = './chroma_storage/'
#client = chromadb.PersistentClient(chroma_path)
client = chromadb.Client()

# Create a ChromaDB collection for storing embeddings
collection_name = "garifuna"
#lient.delete_collection("nanu_nanu_neyi")
collection = client.get_or_create_collection(collection_name)

# Function to read a text file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to chunk the text into manageable pieces (e.g., by character count)
def chunk_text(text, chunk_size=10):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

def embed_text_with_ollama(chunk):
    response = ollama.embeddings(
    model='nomic-embed-text',
    prompt=chunk,
    )

    embedding = response["embedding"]

    return embedding
    
# Function to embed text using Ollama's API (assumes Ollama is running locally)
def embed_text_with_ollama_v1(chunk):
    url = "http://localhost:11434/v1/embeddings"  # Ollama API endpoint
    headers = {"Content-Type": "application/json"}
    data = {"text": chunk, "model": "nomic-embed-text"}  # You can change the model name if needed

    response = requests.post(url, json=data, headers=headers)
    print('JUMBO', response)
    if response.status_code == 200:
        return response.json()['embedding']
    else:
        raise Exception(f"Error during embedding: {response.text}")

# Function to store text chunks and their embeddings in ChromaDB
def store_chunks_in_chromadb(chunks):
    # Loop through the chunks, embed each one and store in ChromaDB
    for i, chunk in enumerate(chunks):
        # Get the embedding for the current chunk
        embedding = embed_text_with_ollama(chunk)
        
        unique_id = str(uuid.uuid4()) 
        # Add the chunk and its metadata to the collection
        collection.add(
            ids=[unique_id],
            documents=[chunk],               # The chunk text
            metadatas=[{"chunk_index": i}],   # Optional metadata (e.g., index)
            embeddings=[embedding]            # The embedding vector
        )

# Main function to process the large text file and store in ChromaDB
def process_large_text_file(file_path):
    # Step 1: Read the file
    text = read_file(file_path)

    # Step 2: Chunk the text
    chunks = chunk_text(text, chunk_size=500)  # Adjust chunk_size as needed

    # Step 3: Store the chunks and embeddings in ChromaDB
    store_chunks_in_chromadb(chunks)

    print("Text has been chunked, embedded, and stored in ChromaDB.")

# Run the process for your text file
file_path = "./data/wiki.txt"  # Replace with your file path
process_large_text_file(file_path)

"""
 errors: Embedding dimension 384 does not match collection dimensionality 768 
    needed to cleanup db?
    need new persistence folder?
"""
results = collection.query(
    query_texts=["Julius"],
    n_results=10,
    include=['distances','metadatas','documents']
    )
print(results)