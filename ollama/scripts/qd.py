import uuid
from qdrant_client import QdrantClient, models
import ollama

COLLECTION_NAME = "NicheApplications"

# Initialize Ollama client
ollama_client = ollama.Client(host="localhost")

# Initialize Qdrant client
qclient = QdrantClient(host="localhost", port=6333)
""" qclient = QdrantClient(
    "https://8f998521-eea1-41e6-9534-9c83e87e2533.eu-central-1-0.aws.cloud.qdrant.io:6333",
    api_key="J_LwwZmXd-Sj6G458O1TtMKIAudevJOELnzyy28TJagwic-KtBXk-A",
) """

# Create a collection if it doesn't already exist
if not qclient.collection_exists(COLLECTION_NAME):
    qclient.create_collection(
        collection_name=COLLECTION_NAME
    )

# Text to embed
text = "Ollama excels in niche applications with specific embeddings"

def store_chunks_in_qdrantdb(chunks):
    # Loop through the chunks, embed each one and store in qdrant
    for i, chunk in enumerate(chunks):
        # Get the embedding for the current chunk
        embedding = embed_text_with_ollama(chunk)
        
        unique_id = str(uuid.uuid4()) 
        # Add the chunk and its metadata to the collection
        # Upload the vectors to the collection along with the original text as payload
        qclient.upsert(
            collection_name=COLLECTION_NAME,
            points=[models.PointStruct(id=i, vector=embedding, payload={"text": chunk})],
        )

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
    # Generate embeddings

    response = ollama.embeddings(
        #model='nomic-embed-text',
        model="llama3.2",
        prompt=chunk,
    )

    embeddings = response["embedding"]

    return embeddings

# Main function to process the large text file and store in ChromaDB
def process_large_text_file(file_path):
    # Step 1: Read the file
    text = read_file(file_path)

    # Step 2: Chunk the text
    chunks = chunk_text(text, chunk_size=500)  # Adjust chunk_size as needed

    # Step 3: Store the chunks and embeddings in ChromaDB
    store_chunks_in_qdrantdb(chunks)

    print("Text has been chunked, embedded, and stored in ChromaDB.")

# Run the process for your text file
file_path = "./data/wiki.txt"  # Replace with your file path
process_large_text_file(file_path)