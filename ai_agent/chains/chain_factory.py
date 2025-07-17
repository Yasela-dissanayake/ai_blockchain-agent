from langchain_ollama import ChatOllama
from ai_blockchain.ai_agent.retrievers.embed_and_retrieve import build_blockchain_retriever
from langchain.chains import RetrievalQA

def build_blockchain_qa_chain():
    llm = ChatOllama(model="llama3.1")
    retriever = build_blockchain_retriever()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
