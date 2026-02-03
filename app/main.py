from fastapi import FastAPI
from app.routes import trace
from app.database.session import engine, Base  # Import engine and Base
from app.models import models  # IMPORTANT: You MUST import your models here

# This line is the "Magic Trigger"
# It tells SQLAlchemy to look at everything inherited from Base and create it
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Supply Chain Backend")

# Include routes
app.include_router(trace.router)

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
