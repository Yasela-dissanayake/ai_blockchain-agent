from web3 import Web3
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to the Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))
assert w3.is_connected(), "Failed to connect to Web3 provider"
print("Connected to Web3 provider successfully!")

# Load ABI
with open("abi/VehicleRegistry.json") as f:
    abi = json.load(f)["abi"]

# Connect to the VehicleRegistry contract
vehicle_contract = w3.eth.contract(
    address=Web3.to_checksum_address("0x28234bcb8625184d8bd1a3bdfbaa787ccd73e57d"),
    abi=abi
)
# Example: Call a function from the contract
print("Contract connected successfully!")

def get_vehicle_owner(land_id):
    return vehicle_contract.functions.getVehicleOwner(land_id).call()

# print(get_vehicle_owner("VH001"))

def get_all_vehicles():
    """
    Get all vehicles from the blockchain
    """
    try:
        contract = vehicle_contract
        
        # Method 1: If you upgrade to the improved contract
        try:
            registration_numbers = contract.functions.getAllRegistrationNumbers().call()
        except:
            # Method 2: Fallback for current contract - use known registration numbers
            registration_numbers = get_known_registration_numbers()
        
        vehicles = []
        for reg_num in registration_numbers:
            vehicle_data = get_vehicle_details(reg_num)
            if vehicle_data and vehicle_data.get('owner'):
                vehicles.append(vehicle_data)
        
        print(f"Retrieved {len(vehicles)} vehicles from blockchain")
        return vehicles
        
    except Exception as e:
        print(f"Error getting all vehicles: {e}")
        return []

def get_vehicle_details(registration_number):
    """
    Get detailed vehicle information from blockchain
    """
    try:
        contract = vehicle_contract
        
        # Method 1: If you upgrade to the improved contract
        try:
            vehicle_data = contract.functions.getVehicleDetails(registration_number).call()
            reg_num, owner, make, model = vehicle_data
        except:
            # Method 2: Fallback for current contract - use the public mapping
            vehicle_data = contract.functions.vehicles(registration_number).call()
            reg_num, owner, make, model = vehicle_data
        
        # Only return data if the vehicle exists (has an owner)
        if owner and owner.strip():
            return {
                'registration_number': reg_num,
                'vehicle_id': reg_num,  # Using registration number as vehicle ID
                'owner': owner,
                'make': make,
                'model': model,
                'status': 'Active'
            }
        else:
            return None
            
    except Exception as e:
        print(f"Error getting vehicle details for {registration_number}: {e}")
        return None

def get_known_registration_numbers():
    """
    Fallback function to get known registration numbers
    Replace this with your actual data or implement event querying
    """
    # Option 1: Hardcoded list (replace with your actual registration numbers)
    return ["VH001", "VH002", "VH003", "VH004", "VH005"]
    
    # Option 2: Read from a file
    # try:
    #     with open('known_vehicles.txt', 'r') as f:
    #         return [line.strip() for line in f.readlines()]
    # except:
    #     return []

def get_vehicle_count():
    """
    Get total number of registered vehicles
    """
    try:
        contract = vehicle_contract
        
        # If you upgrade to improved contract
        try:
            return contract.functions.getVehicleCount().call()
        except:
            # Fallback - count known vehicles
            return len(get_known_registration_numbers())
            
    except Exception as e:
        print(f"Error getting vehicle count: {e}")
        return 0

def vehicle_exists(registration_number):
    """
    Check if a vehicle exists in the registry
    """
    try:
        contract = vehicle_contract
        
        # If you upgrade to improved contract
        try:
            return contract.functions.vehicleExists(registration_number).call()
        except:
            # Fallback - check if owner exists
            owner = contract.functions.getVehicleOwner(registration_number).call()
            return owner and owner.strip() != ""
            
    except Exception as e:
        print(f"Error checking if vehicle exists: {e}")
        return False

# Example usage and testing functions
def test_blockchain_integration():
    """
    Test function to verify blockchain integration works
    """
    print("Testing blockchain integration...")
    
    # Test getting all vehicles
    print("\n1. Getting all vehicles:")
    vehicles = get_all_vehicles()
    for vehicle in vehicles:
        print(f"   - {vehicle['registration_number']}: {vehicle['owner']} ({vehicle['make']} {vehicle['model']})")
    
    # Test getting specific vehicle
    print("\n2. Getting specific vehicle details:")
    if vehicles:
        reg_num = vehicles[0]['registration_number']
        details = get_vehicle_details(reg_num)
        print(f"   Vehicle {reg_num}: {details}")
    
    # Test vehicle count
    print(f"\n3. Total vehicles: {get_vehicle_count()}")
    
    return len(vehicles) > 0

    def get_next_vehicle(reg_num):
        """
        Get the next vehicle in the registration chain
        """
        try:
            return vehicle_contract.functions.getNextVehicle(reg_num).call()
        except Exception as e:
            print(f"Error getting next vehicle after {reg_num}: {e}")
            return None

    def get_previous_vehicle(reg_num):
        """
        Get the previous vehicle in the registration chain
        """
        try:
            return vehicle_contract.functions.getPreviousVehicle(reg_num).call()
        except Exception as e:
            print(f"Error getting previous vehicle before {reg_num}: {e}")
            return None

    def get_first_vehicle():
        """
        Get the first vehicle registered
        """
        try:
            return vehicle_contract.functions.getFirstVehicle().call()
        except Exception as e:
            print(f"Error getting first vehicle: {e}")
            return None

    def get_last_vehicle():
        """
        Get the most recently registered vehicle
        """
        try:
            return vehicle_contract.functions.getLastVehicle().call()
        except Exception as e:
            print(f"Error getting last vehicle: {e}")
            return None


if __name__ == "__main__":
    # Test the integration
    success = test_blockchain_integration()
    if success:
        print("\n✅ Blockchain integration test passed!")
    else:
        print("\n❌ Blockchain integration test failed!")