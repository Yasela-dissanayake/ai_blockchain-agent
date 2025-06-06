from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3.1")
response = model.invoke("What is the capital of Sri Lanka?")
print(response.content)