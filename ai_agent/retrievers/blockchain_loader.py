from langchain.schema import Document
from python_scripts.vehicle_registry_interaction import get_vehicle_owner, get_all_vehicles, get_vehicle_details
import json

def load_vehicle_data_from_blockchain():
    """
    Load vehicle data from blockchain and convert to LangChain Document format
    """
    try:
        # Get all vehicles from blockchain
        vehicles = get_all_vehicles()  # You'll need to implement this function
        
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
                    "vehicle_id": vehicle.get('registration_number'),  # Using reg number as ID
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