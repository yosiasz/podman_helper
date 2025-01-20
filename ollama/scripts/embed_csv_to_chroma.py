import pandas as pd
import ollama
import chromadb

# Initialize ChromaDB client
#client = chromadb.Client()
chroma_path = './chroma_persistent_storage/'
client = chromadb.PersistentClient(chroma_path)
# Create a ChromaDB collection for storing embeddings
collection_name = "csv_embeddings_chroma"
collection = client.get_or_create_collection(collection_name)


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('./data/cars.csv')

# Initialize Ollama client (assuming Ollama is installed and running)
ollama_client = ollama

# Function to generate embeddings using Ollama
def get_embeddings(text):
    response = ollama_client.embed('llama3.2',text)
    #print('embedding', response)
    return response['embeddings']

# Iterate through rows in the DataFrame and generate embeddings
for index, row in df.iterrows():
    # Extract the text from the CSV (assuming a column 'text')
    text = row['text']  # Modify if your CSV has a different structure
    
    # Generate embedding for the text
    embedding = get_embeddings(text)
    try:
    # Store the embedding and metadata in ChromaDB
        collection.add(
            ids=[index],
            embeddings=[embedding],
            metadatas=[{'row_index': index, 'text': text}],
            documents=[text]
        )
    except Exception as e:
        print("An error occurred:", str(e))


print("CSV data successfully embedded into ChromaDB.")
