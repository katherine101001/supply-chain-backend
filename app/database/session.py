from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.config import DB_URL  

# 根据是否连接 Supabase 的连接池来选择合适的 Engine 配置
# 如果你的 DB_URL 包含了 6543 端口，说明你用了 Supabase 的 Transaction Pooler
if DB_URL and "6543" in DB_URL:
    # 关键：连接池模式下必须禁用 SQLAlchemy 本地的连接池 (NullPool)
    # 否则会和 Supabase 的连接池起冲突，导致连接失效
    engine = create_engine(DB_URL, poolclass=NullPool, echo=True)
else:
    # 如果是普通连接 (5432端口)，则使用默认配置
    engine = create_engine(DB_URL, echo=True)

# Create SQLAlchemy engine
engine = create_engine(DB_URL, echo=True)  # echo=True prints SQL statements, useful for debugging

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for ORM models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
