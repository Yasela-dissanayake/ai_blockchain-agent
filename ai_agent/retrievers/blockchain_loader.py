from langchain.schema import Document
from python_scripts.vehicle_registry_interaction import get_vehicle_owner, get_all_vehicles, get_vehicle_details
import json
import re

class BlockchainRetriever:
    def __init__(self):
        self.cache = {}
    
    def retrieve(self, query: str):
        """
        Given a natural language query, retrieve matching blockchain data.
        Return list of relevant text chunks or records.
        """
        # Extract vehicle registration number from query
        vehicle_id = self._extract_vehicle_id(query)
        
        if vehicle_id:
            # Load specific vehicle data
            document = load_single_vehicle_from_blockchain(vehicle_id)
            return [document] if document else []
        else:
            # Load all vehicle data for general queries
            return load_vehicle_data_from_blockchain()
    
    def _extract_vehicle_id(self, query):
        """Extract vehicle ID/registration number from query"""
        # Look for patterns like VH001, AB-9436, etc.
        patterns = [
            r'VH\d+',  # VH001, VH002, etc.
            r'[A-Z]{2}-\d+',  # AB-9436, etc.
            r'[A-Z]{2}\d+',  # AB9436, etc.
            r'\b[A-Z0-9]{4,}\b'  # General alphanumeric patterns
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.upper())
            if match:
                return match.group()
        return None

def load_vehicle_data_from_blockchain():
    """
    Load vehicle data from blockchain and convert to LangChain Document format
    """
    try:
        # Get all vehicles from blockchain
        vehicles = get_all_vehicles()
        documents = []
        
        for vehicle in vehicles:
            # Convert vehicle data to text format similar to CSV
            vehicle_text = f"""
Registration Number: {vehicle.get('registration_number', 'N/A')}
Owner: {vehicle.get('owner', 'N/A')}
Make: {vehicle.get('make', 'N/A')}
Model: {vehicle.get('model', 'N/A')}
Status: Active
"""
            
            # Create LangChain Document
            doc = Document(
                page_content=vehicle_text.strip(),
                metadata={
                    "source": "blockchain",
                    "registration_number": vehicle.get('registration_number'),
                    "vehicle_id": vehicle.get('registration_number'),
                    "owner": vehicle.get('owner'),
                    "type": "vehicle_registry"
                }
            )
            documents.append(doc)
        
        return documents
    
    except Exception as e:
        print(f"Error loading vehicle data from blockchain: {e}")
        return []

def load_single_vehicle_from_blockchain(registration_number):
    """
    Load a single vehicle's data from blockchain
    """
    try:
        vehicle = get_vehicle_details(registration_number)
        if vehicle:
            vehicle_text = f"""
Registration Number: {vehicle.get('registration_number', 'N/A')}
Owner: {vehicle.get('owner', 'N/A')}
Make: {vehicle.get('make', 'N/A')}
Model: {vehicle.get('model', 'N/A')}
Status: Active
"""
            
            return Document(
                page_content=vehicle_text.strip(),
                metadata={
                    "source": "blockchain",
                    "registration_number": vehicle.get('registration_number'),
                    "vehicle_id": vehicle.get('registration_number'),
                    "owner": vehicle.get('owner'),
                    "type": "vehicle_registry"
                }
            )
    except Exception as e:
        print(f"Error loading vehicle {registration_number} from blockchain: {e}")
        return None

# Backward compatibility functions
def load_blockchain_data():
    """Legacy function for backward compatibility"""
    return load_vehicle_data_from_blockchain()

if __name__ == "__main__":
    # Test the retriever
    retriever = BlockchainRetriever()
    
    # Test specific vehicle query
    results = retriever.retrieve("Who owns vehicle VH002?")
    print("Specific vehicle query results:")
    for doc in results:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")
    
    # Test general query
    results = retriever.retrieve("Show me all vehicles")
    print(f"\nGeneral query returned {len(results)} documents")
