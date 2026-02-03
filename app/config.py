# import os
# from dotenv import load_dotenv

# # Load .env from project root
# root_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
# load_dotenv(dotenv_path=root_env_path, override=True)

# # ---- Read environment variables ----
# SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
# CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
# CHAIN_ID = int(os.getenv("CHAIN_ID", 11155111))
# DB_URL = os.getenv("DB_URL")
# PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# # Optional sanity check
# print("Config loaded. DB_URL:", DB_URL)

import os
from dotenv import load_dotenv

# 1. 尝试加载 .env 文件（仅用于本地开发）
# 使用 find_dotenv() 会更智能，它会自动往上找文件
root_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(root_env_path):
    load_dotenv(dotenv_path=root_env_path, override=True)
else:
    # 如果找不到文件（比如在 Render 上），它会直接读取系统环境变量
    load_dotenv() 

# 2. 读取变量
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# 注意：从 os.getenv 拿到的都是字符串，CHAIN_ID 需要转成 int
chain_id_raw = os.getenv("CHAIN_ID")
CHAIN_ID = int(chain_id_raw) if chain_id_raw else 11155111

DB_URL = os.getenv("DB_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# 3. 调试日志（重要！）
# 在 Render 的 Logs 里你会看到这一行。
# 注意：做生意时不要 print 完整的 DB_URL（包含密码）和 PRIVATE_KEY
if DB_URL:
    print(f"✅ Config loaded. DB Host: {DB_URL.split('@')[-1]}") 
else:
    print("❌ Error: DB_URL not found in environment variables!")