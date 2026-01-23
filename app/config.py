import os
from dotenv import load_dotenv

# Load .env from project root
root_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=root_env_path, override=True)

# ---- Read environment variables ----
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
CHAIN_ID = int(os.getenv("CHAIN_ID", 11155111))
DB_URL = os.getenv("DB_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Optional sanity check
print("Config loaded. DB_URL:", DB_URL)
