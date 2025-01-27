import ollama
import chromadb
from chromadb.config import Settings
import os

collection_name = "simply_red"
chroma_path = './chroma_persistent_storage/'
chroma_client = chromadb.PersistentClient(chroma_path)
#settings=Settings(chroma_server_http_port=5677)
#chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name=collection_name)

def ingest_syslog(doc_path):
    with open(doc_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    return text_content

ingest_syslog('./data/wiki.txt')

collection.add(
    documents=["this is juicy gossip of the recent marriage of querrn", "this is an attempt to embed into the family"],
    metadatas=[{"souce":"mysource"}, {"souce":"mysource"}],
    ids=["898989","687676"]
)


results = collection.query(
    query_texts=["ethiopia"],
    n_results=2,
    include=['distances','metadatas','documents']
    )

print(results)