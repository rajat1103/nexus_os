from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.services.brain import store_memory, retrieve_memory
from app.services.llm import get_llm_response

load_dotenv()

app = FastAPI(title="NEXUS OS")

class MemoryRequest(BaseModel):
    content: str
    category: str = "general"

class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"system_status": "active", "version": "0.1.0"}

@app.post("/learn")
async def learn_new_information(memory: MemoryRequest):
    try:
        result = store_memory(memory.content, memory.category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_nexus(request: ChatRequest):
    try:
        search_results = retrieve_memory(request.query)
        
        context_text = ""
        if search_results["documents"]:
            context_text = "\n".join(search_results["documents"][0])
        
        ai_response = get_llm_response(request.query, context_text)
        
        return {
            "response": ai_response,
            "source_context": search_results["documents"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)