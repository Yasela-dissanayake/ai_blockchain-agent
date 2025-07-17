# ai_agent/chains/qa_chain.py
import sys
import os
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from ai_agent.tools.tools import blockchain_tool, search_tool
from ai_agent.logger import log_query
from ai_agent.access_control import check_permission

class QAChain:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.1")
        self.agent = initialize_agent(
            tools=[blockchain_tool, search_tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=1
        )
        self.explanation_steps = []

    def run(self, query, user_id="default_user"):
        """
        Run QA chain and return both answer and explanation trace
        """
        self.explanation_steps = []
        
        # Step 1: Log query receipt
        self.explanation_steps.append(f"Received query: {query}")
        
        # Step 2: Check permissions
        try:
            entity_type = self._extract_entity_type(query)
            check_permission(user_id, entity_type)
            self.explanation_steps.append(f"Permission check passed for entity type: {entity_type}")
        except Exception as e:
            self.explanation_steps.append(f"Permission check failed: {str(e)}")
            return "Access denied", "\n".join(self.explanation_steps)
        
        # Step 3: Process query through agent
        self.explanation_steps.append("Processing query through blockchain agent...")
        try:
            result = self.agent.run(query)
            self.explanation_steps.append(f"Agent successfully retrieved result from blockchain")
        except Exception as e:
            self.explanation_steps.append(f"Error during agent processing: {str(e)}")
            result = "Unable to process query due to error"
        
        # Step 4: Log the interaction
        log_query(user_id, query, result)
        self.explanation_steps.append("Query and result logged for audit trail")
        
        # Combine explanation steps
        explanation = "\n".join(self.explanation_steps)
        
        return result, explanation
    
    def _extract_entity_type(self, query):
        """Extract entity type from query for permission checking"""
        query_lower = query.lower()
        if "vehicle" in query_lower or "car" in query_lower:
            return "vehicle"
        elif "land" in query_lower or "property" in query_lower:
            return "land"
        else:
            return "general"
    
    def handle_query(self, query, user_id="default_user"):
        """Backward compatibility method"""
        answer, _ = self.run(query, user_id)
        return answer

def handle_query(query):
    """Legacy function for backward compatibility"""
    qa_chain = QAChain()
    return qa_chain.handle_query(query)

if __name__ == "__main__":
    # Example usage
    qa_chain = QAChain()
    user_id = "test_user_1"
    
    try:
        check_permission(user_id, "vehicle")
        query = "Who is the owner of the vehicle VH002?"
        
        result, explanation = qa_chain.run(query, user_id)
        print("Final result:", result)
        print("\nExplanation trace:")
        print(explanation)
    except Exception as e:
        print(f"Error: {e}")
