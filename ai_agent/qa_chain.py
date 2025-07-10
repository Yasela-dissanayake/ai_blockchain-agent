import sys
import os
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools.tavily_search.tool import TavilySearchResults

from ai_agent.tools import blockchain_tool,search_tool
from ai_agent.logger import log_query
from ai_agent.access_control import check_permission

llm = ChatOllama(model="llama3.1")

agent = initialize_agent(
    tools=[blockchain_tool, search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

def handle_query(query):
    return agent.run(query)

# Example usage
user_id = "test_user_1"
check_permission(user_id, "vehicle")

query = "Who is the owner of the vehicle VH002?"
result = handle_query(query)
print("final result", result)

log_query(user_id, query, result)
