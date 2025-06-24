from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.retrieval.retrieval_manager import RetrievalManager
from src.llm.llm_manager import LLMManager
from src.api.cache_manager import CacheManager

app = FastAPI()

retrieval_manager = RetrievalManager()
llm_manager = LLMManager()
cache_manager = CacheManager()

class QueryRequest(BaseModel):
    question: str
    language: str = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(request: QueryRequest):
    try:
        lang = request.language or retrieval_manager.detect_language(request.question)
        results = retrieval_manager.process_query(request.question, top_k=3)
        context = retrieval_manager.get_context(results)
        response = llm_manager.generate_response(context, request.question)
        return {"answer": response["content"], "model": response["model"], "usage": response["usage"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}") 