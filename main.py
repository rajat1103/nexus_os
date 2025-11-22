from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import get_vector_client

app = FastAPI(title="NEXUS OS")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"system_status": "active", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/db-check")
async def database_health():
    try:
        client = get_vector_client()
        heartbeat = client.heartbeat()
        return {"database_status": "connected", "heartbeat": heartbeat}
    except Exception as e:
        return {"database_status": "error", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)