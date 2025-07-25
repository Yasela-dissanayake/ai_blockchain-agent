# ai_agent/tools/tools.py
from langchain.tools import Tool
from ai_agent.retrievers.blockchain_loader import load_vehicle_data_from_blockchain, load_single_vehicle_from_blockchain
from python_scripts.vehicle_registry_interaction import get_vehicle_owner, get_all_vehicles, get_vehicle_details
import re
from langchain_community.tools.tavily_search.tool import TavilySearchResults


def blockchain_query_handler(query):
    """
    Handle blockchain queries without importing chain_factory
    """
    try:
        # Extract vehicle ID from query
        vehicle_id = extract_vehicle_id(query)
        
        if vehicle_id:
            # Get specific vehicle data
            vehicle = get_vehicle_details(vehicle_id)
            if vehicle:
                return f"Vehicle {vehicle_id} is owned by {vehicle.get('owner', 'Unknown')}"
            else:
                return f"No vehicle found with ID {vehicle_id}"
        else:
            # Get all vehicles for general queries
            vehicles = get_all_vehicles()
            return f"Found {len(vehicles)} vehicles in the registry"
    except Exception as e:
        return f"Error querying blockchain: {str(e)}"

def extract_vehicle_id(query):
    """Extract vehicle ID from query"""
    patterns = [
        r'VH\d+',
        r'[A-Z]{2}-\d+',
        r'[A-Z]{2}\d+',
        r'\b[A-Z0-9]{4,}\b'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query.upper())
        if match:
            return match.group()
    return None

def search_handler(query):
    """Handle general search queries"""
    return f"Search functionality for: {query}"


search_tool = TavilySearchResults()


# Create tools
blockchain_tool = Tool(
    name="blockchain_query",
    description="Query blockchain for vehicle information",
    func=blockchain_query_handler
)

# search_tool = TavilySearch(
#     max_results=5,
#     topic="general",
#     include_answer=True,          # Tries to include a direct answer
#     include_raw_content=False,
#     include_images=False,
#     include_image_descriptions=False,
#     search_depth="basic"
# )
