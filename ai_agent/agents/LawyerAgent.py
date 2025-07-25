from ai_agent.chains.chain_factory import get_chain
from ai_agent.logger import log_query

class LawyerAgent:
    def __init__(self, chain_name="qa_chain"):
        """
        Initialize the AI Agent with a chosen chain orchestrator.
        """
        self.chain = get_chain(chain_name)

    def handle_query(self, query, user_id="default_user"):
        """
        Main entry point to process user queries.
        1) Pass the query to chain orchestrator.
        2) Receive answer + explanation trace.
        """
        print(f"Received query: {query}")
        
        # Check if chain has run method (new chains) or just call it directly (legacy)
        if hasattr(self.chain, 'run') and callable(getattr(self.chain, 'run')):
            # New chain structure with explanation

            chain = self._select_chain(query)
            answer, explanation = chain.run(query, user_id)

            # answer, explanation = self.chain.run(query, user_id)
            print(f"Answer: {answer}")
            print(f"Explanation: {explanation}")
            return answer, explanation
        else:
            # Legacy chain structure
            answer = self.chain.run(query)
            print(f"Answer: {answer}")
            log_query(user_id, query, answer)
            return answer, "Legacy chain used - no explanation trace available"
        
    def _select_chain(self, query):
        # Basic example: choose chain based on keywords
        query_lower = query.lower()
        if 'history' in query_lower or 'report' in query_lower:
            from ai_agent.chains.ReActChain import ReActChain
            return ReActChain()
        else:
            from ai_agent.chains.qa_chain import QAChain
            return QAChain()

if __name__ == "__main__":
    # Simple test run
    agent = LawyerAgent()
    user_id = "test_user_1"
    query = input("Enter your query: ")
    # query = "What is the price of Zotye z100 in Sri Lanka?"
    
    try:
        answer, explanation = agent.handle_query(query, user_id)
        print("\n=== FINAL RESULTS ===")
        print("Answer:", answer)
        print("Explanation:", explanation)
    except Exception as e:
        print(f"Error: {e}")
