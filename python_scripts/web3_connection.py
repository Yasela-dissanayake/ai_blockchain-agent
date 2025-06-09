from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to the Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))

# Check connection
assert w3.is_connected(), "Failed to connect to Web3 provider"
print("Connected to Web3 provider successfully!")