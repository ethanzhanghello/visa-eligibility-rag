from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.retrieval.retrieval_manager import RetrievalManager
from src.llm.llm_manager import LLMManager
from src.api.cache_manager import CacheManager
from src.api.confidence_manager import ConfidenceManager
from src.api.question_tracker import QuestionTracker

app = FastAPI()

retrieval_manager = RetrievalManager()
llm_manager = LLMManager()
cache_manager = CacheManager()
confidence_manager = ConfidenceManager()
question_tracker = QuestionTracker()

class QueryRequest(BaseModel):
    question: str
    language: str = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/cache/clear")
def clear_cache():
    """Clear all cached responses."""
    try:
        success = cache_manager.clear_all()
        if success:
            return {"message": "Cache cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear cache")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache clear error: {str(e)}")

@app.get("/cache/stats")
def cache_stats():
    """Get cache statistics."""
    try:
        if cache_manager.redis_client:
            # Redis stats
            info = cache_manager.redis_client.info()
            return {
                "type": "redis",
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        else:
            # In-memory cache stats
            return {
                "type": "memory",
                "cached_items": len(cache_manager._memory_cache),
                "fallback_mode": True
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache stats error: {str(e)}")

@app.post("/query")
def query(request: QueryRequest):
    try:
        # Check cache first
        cached_response = cache_manager.get(request.question, request.language)
        if cached_response:
            return {
                "answer": cached_response["content"], 
                "model": cached_response["model"], 
                "usage": cached_response["usage"], 
                "cached": True,
                "confidence": {
                    "score": 1.0,
                    "level": "high",
                    "cached_response": True
                }
            }
        
        # Process query if not cached
        lang = request.language or retrieval_manager.detect_language(request.question)
        results = retrieval_manager.process_query(request.question, top_k=3)
        context = retrieval_manager.get_context(results)
        response = llm_manager.generate_response(context, request.question)
        
        # Calculate confidence
        confidence_metrics = confidence_manager.calculate_confidence(
            question=request.question,
            response=response["content"],
            context=context,
            language=lang
        )
        
        # Track low-confidence questions
        flagged_question_id = question_tracker.track_question(
            question=request.question,
            language=lang,
            confidence_score=confidence_metrics.confidence_score
        )
        
        # Cache the response
        cache_manager.set(request.question, response, request.language)
        
        return {
            "answer": response["content"], 
            "model": response["model"], 
            "usage": response["usage"], 
            "cached": False,
            "confidence": {
                "score": confidence_metrics.confidence_score,
                "level": confidence_manager.get_confidence_level(confidence_metrics.confidence_score),
                "context_relevance": confidence_metrics.context_relevance,
                "source_quality": confidence_metrics.source_quality,
                "contains_immigration_terms": confidence_metrics.contains_immigration_terms,
                "flagged_for_review": flagged_question_id is not None,
                "question_id": flagged_question_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}") 