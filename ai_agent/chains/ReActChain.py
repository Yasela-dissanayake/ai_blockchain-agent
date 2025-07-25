
## Removed langchain_ollama import (Ollama no longer used)
from ai_agent.logger import log_query
from ai_agent.access_control import check_permission
import re

class ReActChain:
    def __init__(self):
        # Move imports here to avoid circular import errors
        from ai_agent.retrievers.blockchain_loader import BlockchainRetriever
        from ai_agent.tools.tools import search_tool
        self.retriever = BlockchainRetriever()
        self.tools = [search_tool]
        
    def run(self, query, user_id="default_user"):
        """
        ReAct reasoning loop: Reason → Act → Observe → Reason
        """
        explanation_steps = []
        
        # Step 1: Reason about the query
        explanation_steps.append(f"Query received: {query}")
        explanation_steps.append("Reasoning: Analyzing query to determine required actions...")
        
        # Determine what type of query this is
        query_type = self._analyze_query(query)
        explanation_steps.append(f"Query type identified: {query_type}")
        
        # Step 2: Plan actions
        if query_type == "vehicle_ownership":
            explanation_steps.append("Planning: Need to retrieve vehicle ownership data from blockchain")
            action_plan = "retrieve_vehicle_data"
        elif query_type == "general_search":
            explanation_steps.append("Planning: Need to search for general information")
            action_plan = "search_general"
        else:
            explanation_steps.append("Planning: Default to vehicle data retrieval")
            action_plan = "retrieve_vehicle_data"
        
        # Step 3: Act - Execute the planned action
        explanation_steps.append(f"Action: Executing {action_plan}")
        
        try:
            if action_plan == "retrieve_vehicle_data":
                # Use retriever to get vehicle data
                documents = self.retriever.retrieve(query)
                if documents:
                    answer = self._format_vehicle_answer(documents[0])
                    explanation_steps.append(f"Observation: Successfully retrieved vehicle data")
                else:
                    answer = "No vehicle data found for the specified query."
                    explanation_steps.append("Observation: No matching vehicle data found")
            elif action_plan == "search_general":
                # Use search tool for general queries
                answer = self.tools[0].run(query)
                explanation_steps.append("Observation: Retrieved answer using search tool")
            else:
                answer = "Action plan not recognized."
                explanation_steps.append("Observation: No valid action plan executed")
                
        except Exception as e:
            answer = f"Error processing query: {str(e)}"
            explanation_steps.append(f"Observation: Error occurred - {str(e)}")
        
        # Step 4: Final reasoning
        explanation_steps.append("Final reasoning: Synthesizing answer based on retrieved information")
        
        # Log the interaction
        log_query(user_id, query, answer)
        explanation_steps.append("Action: Logged query and response for audit trail")
        
        explanation = "\n".join(explanation_steps)
        return answer, explanation
    
    def _analyze_query(self, query):
        """Analyze query to determine type"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["owner", "owns", "vehicle", "car"]):
            return "vehicle_ownership"
        elif any(word in query_lower for word in ["search", "find", "look"]):
            return "general_search"
        else:
            return "vehicle_ownership"
    
    def _format_vehicle_answer(self, document):
        """Format vehicle document into readable answer"""
        content = document.page_content
        metadata = document.metadata
        
        # Extract owner information
        owner_match = re.search(r'Owner:\s*(.+)', content)
        reg_match = re.search(r'Registration Number:\s*(.+)', content)
        
        if owner_match and reg_match:
            owner = owner_match.group(1).strip()
            reg_num = reg_match.group(1).strip()
            return f"The owner of vehicle {reg_num} is {owner}."
        else:
            return "Vehicle ownership information could not be determined."

if __name__ == "__main__":
    # Test ReAct chain
    react_chain = ReActChain()
    answer, explanation = react_chain.run("Who owns VH001?")
    print("Answer:", answer)
    print("\nExplanation trace:")
    print(explanation)
