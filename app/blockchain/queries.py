# from web3 import Web3
# from app.config import SEPOLIA_RPC_URL, CONTRACT_ADDRESS
# import json

# # Connect to blockchain
# w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

# with open("app/scripts/SupplyChainRegistry.json") as f:
#     abi = json.load(f)
#     if isinstance(abi, dict) and 'abi' in abi:
#         abi = abi['abi']

# contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# def get_onchain_recordHash(sku: str) -> str:
#     """Return the on-chain recordHash for a given SKU as hex string."""
#     try:
#         product = contract.functions.getProduct(sku).call()
#         return product[3].hex()  # recordHash stored on-chain
#     except Exception:
#         return None

from web3 import Web3
from app.config import SEPOLIA_RPC_URL, CONTRACT_ADDRESS
import json
from typing import Optional

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

with open("app/scripts/SupplyChainRegistry.json") as f:
    abi = json.load(f)
    if isinstance(abi, dict) and 'abi' in abi:
        abi = abi['abi']

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def get_onchain_recordHash(sku: str) -> Optional[str]:
    """Return the on-chain recordHash for a given SKU as hex string."""
    try:
        product = contract.functions.getProduct(sku).call()
        return product[3].hex()  # recordHash stored on-chain
    except Exception:
        return None

def verify_tx_on_chain(tx_hash: str) -> bool:
    """Return True if transaction succeeded on-chain."""
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        return receipt.status == 1
    except Exception:
        return False
