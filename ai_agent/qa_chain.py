from langchain_ollama import ChatOllama
from embed_and_retrieve import build_vector_store
from langchain.chains import RetrievalQA


retriever = build_vector_store()
qa_chain = RetrievalQA.from_chain_type(
llm=ChatOllama(model="llama3.1"),
retriever=retriever,
return_source_documents=False
)

question = "Who owns land LD002?"
response = qa_chain.invoke({"query": question})
print(response["result"])