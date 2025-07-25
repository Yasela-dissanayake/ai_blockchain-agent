import sys
import os
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from ai_agent.tools.tools import blockchain_tool, search_tool
from ai_agent.logger import log_query
from ai_agent.access_control import check_permission

class QAChain:
    def __init__(self,max_iterations=2):
        self.llm = ChatOllama(model="llama3.1")
        self.agent = initialize_agent(
            tools=[blockchain_tool, search_tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=max_iterations
        )
        self.max_iterations = max_iterations
        self.explanation_steps = []

    def is_output_satisfactory(self, output):
        """Simple dynamic check, customize per use case."""
        if output is None:
            return False
        key_phrases = ["owner", "ownership", "title report", "registered", "transferred"]  # extend as needed
        output_lower = str(output).lower()
        return any(phrase in output_lower for phrase in key_phrases)


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
        
        outputs = []
        explanations = []
        for i in range(1, self.max_iterations + 1):
            self.explanation_steps.append(f"Step {i}: Processing query through blockchain agent...")
            try:
                result = self.agent.run(query)
                self.explanation_steps.append(f"Agent output at step {i}: {result}")
            except Exception as e:
                self.explanation_steps.append(f"Error during agent processing at step {i}: {str(e)}")
                result = "Unable to process query due to error"
            outputs.append(result)
            explanations.append("\n".join(self.explanation_steps))
            # Early stopping if satisfactory answer found
            if self.is_output_satisfactory(result):
                log_query(user_id, query, result)
                self.explanation_steps.append("Stopping early: satisfactory answer found.")
                return result, "\n".join(self.explanation_steps)
            
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

# Legacy function for backward compatibility
def handle_query(query):
    qa_chain = QAChain()
    return qa_chain.handle_query(query)

if __name__ == "__main__":
    # Example usage
    qa_chain = QAChain()
    user_id = "test_user_1"
    
    try:
        # query = "What is the price of Zotye z100 in Sri Lanka?"
        query = input("Enter your query: ")
        result, explanation = qa_chain.run(query, user_id)
        print("Final result:", result)
        print("\nExplanation trace:")
        print(explanation)
    except Exception as e:
        print(f"Error: {e}")
