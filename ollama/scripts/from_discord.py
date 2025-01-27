import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

try:
    print("Starting document loading...")
    loader = TextLoader("./data/cars.csv", encoding='utf-8')  
    print("Loader created successfully")
    
    documents = loader.load()
    print(f"Documents loaded successfully. Number of documents: {len(documents)}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size
        chunk_overlap=100,  # less overlap
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )
    
    docs = text_splitter.split_documents(documents)
    print(f"Number of chunks: {len(docs)}")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': True}
    )

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./code_knowledge"
    )
    vector_store.persist()

    llm = Ollama(model="qwen2.5-coder:3b")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    query = "How do I create a basic GUI in AHKv2?"
    result = qa_chain({"query": query})
    print("\nResponse:", result['result'])

except Exception as e:
    print(f"Error occurred: {str(e)}")
    import traceback
    print(f"Full traceback: {traceback.format_exc()}")