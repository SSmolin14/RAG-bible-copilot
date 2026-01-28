from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from typing import List
from app.core.rag_pipeline import BibleCopilot
from app.config import Config

app = FastAPI(title="Bible Copilot API")

# Allow your React app to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG engine once when the server starts
copilot = BibleCopilot(
    api_key=Config.GEMINI_API_KEY, 
    mode=Config.VECTOR_STORE_TYPE
)

# Define what the incoming request looks like
class QueryRequest(BaseModel):
    question: str

# Define what the outgoing response looks like
class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
def read_root():
    return {"status": "Bible Copilot API is online", "model_type": Config.LLM_TYPE}

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        # Use our existing logic
        result = copilot.ask(request.question)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))