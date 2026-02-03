

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
