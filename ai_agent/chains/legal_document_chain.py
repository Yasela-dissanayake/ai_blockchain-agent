from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from ai_agent.retrievers.chunked_loader import load_all_chunks
from ai_agent.logger import log_query

class LegalDocumentChain:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        self.llm = OllamaLLM(model="llama3.1")
        self.vector_store = None
        self.qa_chain = None
        self._build_legal_qa_chain()
    
    def _build_legal_qa_chain(self):
        """Build QA chain specifically for legal documents"""
        print("Building legal document chain...")
        
        # Load only legal documents
        chunks = load_all_chunks(include_legal=True)
        legal_chunks = [c for c in chunks if c.metadata.get('source_type') == 'legal_document']
        
        if not legal_chunks:
            print("No legal documents found. Check your PDF files in legal_docs/")
            return
        
        # Create vector store from legal documents
        self.vector_store = FAISS.from_documents(legal_chunks, self.embeddings)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        
        # Legal-specific prompt template
        legal_prompt = PromptTemplate(
            template="""You are a legal expert specializing in Sri Lankan Motor Traffic Law. 
Use the following legal documents to answer the question accurately and professionally.

Legal Documents:
{context}

Question: {question}

Provide a comprehensive legal answer that includes:
1. Direct answer to the question
2. Relevant legal sections or requirements
3. Step-by-step procedures if applicable
4. Any penalties or consequences
5. Legal citations from the documents

Answer:""",
            input_variables=["context", "question"]
        )
        
        # Create RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": legal_prompt}
        )
        
        print(f"Legal document chain built with {len(legal_chunks)} legal chunks")
    
    def run(self, query, user_id="default_user"):
        """Process legal document queries"""
        if not self.qa_chain:
            return "Legal document chain not available. Check PDF files.", "Chain initialization failed"
        
        try:
            # Query the legal documents
            result = self.qa_chain({"query": query})
            answer = result["result"]
            source_docs = result["source_documents"]
            
            # Create explanation showing which documents were used
            explanation = f"Legal Analysis Steps:\n"
            explanation += f"1. Query: {query}\n"
            explanation += f"2. Retrieved {len(source_docs)} relevant legal documents\n"
            explanation += f"3. Generated legal opinion based on:\n"
            
            for i, doc in enumerate(source_docs[:2], 1):
                doc_type = doc.metadata.get('document_category', 'legal_document')
                explanation += f"   - {doc_type}: {doc.page_content[:100]}...\n"
            
            explanation += f"4. Provided comprehensive legal guidance"
            
            # Add legal disclaimer
            answer += "\n\n⚖️ Legal Disclaimer: This guidance is based on available legal documents. For specific legal matters, consult with qualified legal counsel or the Department of Motor Traffic."
            
            # Log the query
            log_query(user_id, query, answer)
            
            return answer, explanation
            
        except Exception as e:
            error_msg = f"Error processing legal query: {str(e)}"
            return error_msg, f"Legal document chain error: {str(e)}"

# For testing
if __name__ == "__main__":
    chain = LegalDocumentChain()
    
    test_queries = [
        "What are the requirements to register a new vehicle in Sri Lanka?",
        "What documents do I need for MTA 6 form?",
        "What are the penalties for late vehicle registration?",
        "How do I resolve a vehicle ownership dispute?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        answer, explanation = chain.run(query)
        print(f"Answer: {answer[:200]}...")
        print(f"Explanation: {explanation}")
        print("-" * 80)
