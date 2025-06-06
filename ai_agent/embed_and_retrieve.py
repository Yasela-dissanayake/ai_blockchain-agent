from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from chunked_loader import load_all_chunks

def build_vector_store():
    chunks = load_all_chunks()
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever()

