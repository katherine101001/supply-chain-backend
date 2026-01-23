import pandas as pd
from web3 import Web3
from app.config import SEPOLIA_RPC_URL, CONTRACT_ADDRESS
import json

# Load CSV
csv_path = "app/scripts/supply_chain_data.csv"
df = pd.read_csv(csv_path)

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
# acct = w3.eth.account.from_key(PRIVATE_KEY)

# Load ABI
with open("app/scripts/SupplyChainRegistry.json") as f:
    abi = json.load(f)

contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
contract = w3.eth.contract(address=contract_address, abi=abi)

# Place the verification snippet here
for sku in df["SKU"]:
    try:
        product_type, location, status, record_hash = contract.functions.getProduct(sku).call()
        print(f"{sku} ✅ Found:")
        print("  Type:", product_type)
        print("  Location:", location)
        print("  Status:", status)
        print("  Record hash:", record_hash.hex())
    except Exception:
        print(f"{sku} ❌ Not found on blockchain")