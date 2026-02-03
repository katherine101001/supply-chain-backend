import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool  # <--- 新增这个导入

# 1. 加载环境变量
# Render 上没有 .env 文件，load_dotenv() 会自动跳过并读取系统设置
load_dotenv()

# 2. 读取变量
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# 数据库链接 (确保 Render 后台的 Key 是 DB_URL)
DB_URL = os.getenv("DB_URL") 

# 3. 创建 Engine (针对 Supabase 的关键改动)
# 如果你使用的是 Supabase 的连接池 (端口 6543)，
# 必须添加 poolclass=NullPool，否则连接会经常断开。
if DB_URL and "6543" in DB_URL:
    engine = create_engine(DB_URL, poolclass=NullPool)
else:
    engine = create_engine(DB_URL)

# 调试日志
if DB_URL:
    print(f"✅ DB Config loaded for host: {DB_URL.split('@')[-1].split('/')[0]}")