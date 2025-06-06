from langchain_ollama import ChatOllama
from embed_and_retrieve import build_vector_store
from langchain.chains import RetrievalQA
from logger import log_query

retriever = build_vector_store()
qa_chain = RetrievalQA.from_chain_type(
llm=ChatOllama(model="llama3.1"),
retriever=retriever,
return_source_documents=False
)


user_id = "test_user_1"
query = "Who owns land LD002?"
response = qa_chain.invoke({"query": query})
print(response["result"])
log_query(user_id, query, response["result"])

