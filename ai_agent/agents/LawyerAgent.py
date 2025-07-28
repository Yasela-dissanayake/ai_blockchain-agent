# ai_agent/agents/LawyerAgent.py
from ai_agent.chains.chain_factory import get_chain
from ai_agent.logger import log_query
from ai_agent.classifiers.query_classifier import IntelligentQueryClassifier

class LawyerAgent:
    def __init__(self, chain_name="qa_chain"):
        """
        Initialize the AI Agent with intelligent query classification.
        """
        self.default_chain = get_chain(chain_name)
        self.classifier = IntelligentQueryClassifier()

    def handle_query(self, query, user_id="default_user"):
        """
        Main entry point to process user queries with intelligent routing.
        1) Classify the query to determine the appropriate chain
        2) Route to the selected chain
        3) Return answer and explanation trace
        """
        print(f"Received query: {query}")
        
        # Intelligent chain selection
        chain = self._select_chain_intelligently(query)
        
        # Process query through selected chain
        if hasattr(chain, 'run') and callable(getattr(chain, 'run')):
            answer, explanation = chain.run(query, user_id)
            print(f"Answer: {answer}")
            print(f"Explanation: {explanation}")
            return answer, explanation
        else:
            # Legacy chain structure fallback
            answer = chain.run(query)
            print(f"Answer: {answer}")
            log_query(user_id, query, answer)
            return answer, "Legacy chain used - no explanation trace available"

    def _select_chain_intelligently(self, query):
        """
        Intelligent chain selection based on query analysis with detailed logging
        """
        # Get detailed classification with confidence and reasoning
        classification_result = self.classifier.classify_with_confidence(query)
        
        query_type = classification_result['classification']
        confidence = classification_result['confidence']
        reasoning = classification_result['reasoning']
        
        # Log the decision process
        print(f"Query classification: {query_type}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Reasoning: {', '.join(reasoning)}")
        
        # Route to appropriate chain based on classification
        if query_type == 'blockchain':
            from ai_agent.chains.ReActChain import ReActChain
            print("→ Routing to ReActChain for blockchain-specific query")
            print("  ReActChain will provide detailed reasoning and blockchain data retrieval")
            return ReActChain()
        else:
            from ai_agent.chains.qa_chain import QAChain
            print("→ Routing to QAChain for general query")
            print("  QAChain will handle web search and general information retrieval")
            return QAChain()
    
    def _legacy_select_chain(self, query):
        """
        Legacy chain selection method (kept for backward compatibility)
        """
        query_lower = query.lower()
        if 'history' in query_lower or 'report' in query_lower:
            from ai_agent.chains.ReActChain import ReActChain
            return ReActChain()
        else:
            from ai_agent.chains.qa_chain import QAChain
            return QAChain()
    
    def get_classification_info(self, query):
        """
        Public method to get classification information without processing the query
        """
        return self.classifier.classify_with_confidence(query)
    
    def set_classification_mode(self, use_intelligent=True):
        """
        Toggle between intelligent and legacy classification modes
        """
        self.use_intelligent_classification = use_intelligent
        mode = "intelligent" if use_intelligent else "legacy"
        print(f"Classification mode set to: {mode}")

if __name__ == "__main__":
    # Enhanced test run with classification demonstration
    agent = LawyerAgent()
    user_id = "test_user_1"
    
    # Test queries to demonstrate intelligent classification
    test_queries = [
        "Who owns vehicle VH001?",
        "What is the price of Honda Civic 2019 in Sri Lanka?",
        "Show me the ownership history of land LD005",
        "How to register a new vehicle?",
        "Transfer ownership of VH003 to John Smith"
    ]
    
    print("=== INTELLIGENT QUERY CLASSIFICATION DEMO ===\n")
    
    for test_query in test_queries:
        print(f"Test Query: '{test_query}'")
        classification_info = agent.get_classification_info(test_query)
        print(f"Classification: {classification_info['classification']}")
        print(f"Confidence: {classification_info['confidence']:.2f}")
        print(f"Reasoning: {', '.join(classification_info['reasoning'])}")
        print("-" * 50)
    
    print("\n=== INTERACTIVE MODE ===")
    
    try:
        query = input("Enter your query: ")
        answer, explanation = agent.handle_query(query, user_id)
        
        print("\n=== FINAL RESULTS ===")
        print("Answer:", answer)
        print("\nExplanation:", explanation)
        
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nSession terminated by user.")
