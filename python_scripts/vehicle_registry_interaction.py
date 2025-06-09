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

print(get_vehicle_owner(1))