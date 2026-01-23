from fastapi import FastAPI
from app.routes import trace

app = FastAPI(title="Supply Chain Backend")

# Include routes
app.include_router(trace.router)

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
