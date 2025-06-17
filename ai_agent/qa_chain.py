
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from python_scripts.vehicle_registry_interaction import get_vehicle_owner


from langchain_ollama import ChatOllama
# from embed_and_retrieve import build_vector_store
from ai_agent.embed_and_retrieve import build_vector_store

from langchain.chains import RetrievalQA
from ai_agent.logger import log_query
from ai_agent.access_control import check_permission
from ai_agent.embed_and_retrieve import build_blockchain_retriever
# from python_scripts.vehicle_registry_interaction import get_vehicle_owner

# retriever = build_vector_store()
retriever = build_blockchain_retriever()
qa_chain = RetrievalQA.from_chain_type(
llm=ChatOllama(model="llama3.1"),
retriever=retriever,
return_source_documents=False
)

print("before hadnle_query")
def handle_query(query):
    """
    Intelligently handle the query by analyzing its intent.
    """

    print("inside hadnle_query -start")    

    # Use the AI model to analyze the query
    response = qa_chain.invoke({"query": query})
    result = response["result"]

    print("query response ",result)

    # Check if the query is related to vehicle ownership
    if "vehicle" in query.lower() or "owner" in query.lower():
        print("inside if start")
        # Extract vehicle ID intelligently (e.g., using regex or NLP tools)
        import re
        match = re.search(r"vehicle\s+(\w+)", query.lower())
        if match:
            print("inside match")
            vehicle_id = match.group(1)
            return get_vehicle_owner(vehicle_id)

    print("inside hadnle_query -end")
    # If not related to vehicle ownership, return the general result
    return result


# Example usage
user_id = "test_user_1"
check_permission(user_id, "vehicle")

query = "How many vehicles does Yasela Dissanayake owns?"
result = handle_query(query)
print("final result ",result)

log_query(user_id, query, result)