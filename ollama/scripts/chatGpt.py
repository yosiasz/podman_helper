import pandas as pd
import ollama
import chromadb
#from chromadb.config import Settings
#from chromadb.utils import embedding_functions

# Step 1: Read the CSV file
csv_file_path = "./data/cars.csv"
df = pd.read_csv(csv_file_path)

# Make sure you have a column containing text data to generate embeddings
# For example, let's assume the text column is named 'text'
texts = df['text'].tolist()

# Step 2: Generate embeddings using Ollama
# Create a function to use Ollama to generate embeddings
def generate_embeddings(texts):
    embeddings = []
    for text in texts:
        #embedding = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": text}])
        embedding = ollama.embed(model="llama3.2",input=text)
        print('momomo',embedding)
        #embeddings.append(embedding['embeddings'])
    return embeddings

# Generate embeddings
embeddings = generate_embeddings(texts)

# Step 3: Set up ChromaDB to store embeddings
# Configure ChromaDB settings
#client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
# Initialize ChromaDB client
chroma_path = './chroma_persistent_storage/'
client = chromadb.PersistentClient(chroma_path)

#client = chromadb.Client()
# Create a ChromaDB collection for storing embeddings
collection_name = "nanu_nanu_neyi"
collection = client.get_or_create_collection(collection_name)

# Add documents with embeddings to the collection
for idx, embedding in enumerate(embeddings):
    collection.add(
        documents=[texts[idx]],
        metadatas=[{"index": idx}],
        embeddings=[embedding]
    )

print("Embeddings successfully created and stored in ChromaDB.")
