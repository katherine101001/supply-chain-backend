# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text
# from web3 import Web3

# # Load .env from project root
# root_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# load_dotenv(dotenv_path=root_env_path, override=True)

# # ---- Read variables ----
# SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
# CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
# CHAIN_ID = int(os.getenv("CHAIN_ID"))
# DB_URL = os.getenv("DB_URL")
# PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# print("Loaded .env variables successfully.")
# print(f"DB_URL read: {DB_URL}")  # debug


# # ---- Test MySQL connection ----
# try:
#     engine = create_engine(DB_URL)
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT 1"))
#         print("✅ MySQL connection successful:", result.fetchone())
# except Exception as e:
#     print("❌ MySQL connection failed:", e)

# # ---- Test Sepolia connection ----
# try:
#     w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
#     if w3.is_connected():
#         print("✅ Sepolia connection successful!")
#         acct = w3.eth.account.from_key(PRIVATE_KEY)
#         balance = w3.eth.get_balance(acct.address)
#         print(f"Wallet address: {acct.address}")
#         print(f"Wallet balance (in wei): {balance}")
#     else:
#         print("❌ Sepolia connection failed")
# except Exception as e:
#     print("❌ Error connecting to Sepolia:", e)

from sqlalchemy import create_engine, text
from web3 import Web3
from app.config import DB_URL, SEPOLIA_RPC_URL, PRIVATE_KEY

# ---- Test MySQL connection ----
try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ MySQL connection successful:", result.fetchone())
except Exception as e:
    print("❌ MySQL connection failed:", e)

# ---- Test Sepolia connection ----
try:
    w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    if w3.is_connected():
        print("✅ Sepolia connection successful!")
        acct = w3.eth.account.from_key(PRIVATE_KEY)
        balance = w3.eth.get_balance(acct.address)
        print(f"Wallet address: {acct.address}")
        print(f"Wallet balance (in wei): {balance}")
    else:
        print("❌ Sepolia connection failed")
except Exception as e:
    print("❌ Error connecting to Sepolia:", e)
