from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from ai_blockchain.ai_agent.retrievers.chunked_loader import load_all_chunks
from ai_blockchain.ai_agent.retrievers.blockchain_loader import load_vehicle_data_from_blockchain

# def build_vector_store():
#     chunks = load_all_chunks()
#     embeddings = OllamaEmbeddings(model="mxbai-embed-large")
#     vectorstore = FAISS.from_documents(chunks, embeddings)
#     return vectorstore.as_retriever()

def build_vector_store(use_blockchain=True):
    """
    Build vector store from blockchain or CSV data
    """
    print(f"Building vector store using {'blockchain' if use_blockchain else 'CSV'} data...")
    
    # chunks = load_all_chunks(use_blockchain=use_blockchain)
    chunks = load_vehicle_data_from_blockchain()
    
    if not chunks:
        print("No data chunks loaded. Check your data source.")
        return None
    
    # embeddings = OllamaEmbeddings(model="llama2:7b")
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    print(f"Vector store built with {len(chunks)} chunks")
    return vectorstore.as_retriever()

def build_blockchain_retriever():
    """
    Convenience function to build retriever specifically from blockchain data
    """
    return build_vector_store(use_blockchain=True)

def build_csv_retriever():
    """
    Convenience function to build retriever from CSV data (for testing/fallback)
    """
    return build_vector_store(use_blockchain=False)