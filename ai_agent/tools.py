from langchain.agents import Tool
from ai_agent.chain_factory import build_blockchain_qa_chain
from langchain_community.tools.tavily_search.tool import TavilySearchResults

qa_chain = build_blockchain_qa_chain()

blockchain_tool = Tool(
    name="BlockchainVehicleSearch",
    func=qa_chain.run,
    description=(
        "Searches vehicle registration details from the blockchain. "
        "Use this for questions like 'who owns Zotye Z100?' or 'how many Mitsubishi cars are registered?'"
    )
)


search_tool = TavilySearchResults(
    name="SriLankaSearch",
    description="Searches the internet with a focus on Sri Lanka. Use it to answer questions like 'price of used Zotye Z100 in Sri Lanka'",
    k=3  # top 3 results
)
