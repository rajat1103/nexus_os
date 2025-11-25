from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.database import get_vector_client
from app.services.brain import store_memory

app = FastAPI(title="NEXUS OS")

class MemoryRequest(BaseModel):
    content: str
    category: str = "general"

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

@app.post("/learn")
async def learn_new_information(memory: MemoryRequest):
    try:
        result = store_memory(memory.content, memory.category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)