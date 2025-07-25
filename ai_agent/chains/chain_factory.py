from langchain_ollama import ChatOllama
from ai_agent.retrievers.embed_and_retrieve import build_blockchain_retriever
from langchain.chains import RetrievalQA

def build_blockchain_qa_chain():
    llm = ChatOllama(model="llama3.1")
    retriever = build_blockchain_retriever()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

def get_chain(chain_name="qa_chain"):
    """
    Factory function to create different types of chains
    Note: Import QAChain locally to avoid circular imports
    """
    if chain_name == "legacy_qa":
        return build_blockchain_qa_chain()
    elif chain_name == "qa_chain":
        # Import locally to avoid circular import
        from ai_agent.chains.qa_chain import QAChain
        return QAChain()
    else:
        # Default to legacy for now
        return build_blockchain_qa_chain()

if __name__ == "__main__":
    # Test the factory
    chain = get_chain("legacy_qa")
    result = chain.run("Who owns vehicle VH002?")
    print("Answer:", result)
