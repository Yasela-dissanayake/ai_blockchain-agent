# ai_agent/agents/LawyerAgent.py

from ai_agent.chains.chain_factory import get_chain
from ai_agent.logger import get_logger

logger = get_logger(__name__)

class LawyerAgent:
    def __init__(self, chain_name="qa_chain"):
        """
        Initialize the AI Agent with a chosen chain orchestrator.
        """
        self.chain = get_chain(chain_name)

    def handle_query(self, query):
        """
        Main entry point to process user queries.
        1) Pass the query to chain orchestrator.
        2) Receive answer + explanation trace.
        """
        logger.info(f"Received query: {query}")
        answer, explanation = self.chain.run(query)
        logger.info(f"Answer: {answer}")
        return answer, explanation

if __name__ == "__main__":
    # Simple test run
    agent = LawyerAgent()
    query = "Who owns vehicle AB-9436?"
    answer, explanation = agent.handle_query(query)
    print("Answer:", answer)
    print("Explanation trace:", explanation)
