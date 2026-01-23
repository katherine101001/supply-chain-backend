# app/database/test_db.py
from app.database.session import engine, Base
from sqlalchemy import text

# Test raw SQL
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("✅ Database raw SQL test:", result.fetchone())

# Optional: test metadata creation (if you define models later)
# Base.metadata.create_all(bind=engine)
print("✅ Engine works, ready for ORM models.")
