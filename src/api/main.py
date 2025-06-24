"""
Main FastAPI application for the Green Card RAG Helper.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, Any, Optional
import os

# Import managers
from src.retrieval.retrieval_manager import RetrievalManager
from src.api.confidence_manager import ConfidenceManager
from src.api.question_tracker import QuestionTracker
from src.api.faq_integration import FAQIntegrationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Green Card RAG Helper API",
    description="Bilingual immigration assistant with expert review system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
try:
    retrieval_manager = RetrievalManager()
    confidence_manager = ConfidenceManager()
    question_tracker = QuestionTracker()
    faq_integration = FAQIntegrationManager()
    logger.info("All managers initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize managers: {e}")
    raise

# Mock LLM manager for testing
class MockLLMManager:
    """Mock LLM manager for testing without OpenAI API."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        logger.info(f"Initialized MockLLMManager with model: {model_name}")
    
    def generate_response(self, context: str, user_input: str, **kwargs) -> Dict[str, Any]:
        """Generate a mock response for testing."""
        return {
            "content": f"Mock response for: {user_input}. Based on context: {context[:100]}...",
            "model": self.model_name,
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150
            }
        }

# Use mock LLM manager for now
llm_manager = MockLLMManager()

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Green Card RAG Helper API is running",
        "version": "1.0.0"
    }

@app.post("/query")
def query_endpoint(request: Dict[str, Any]):
    """Main query endpoint for processing immigration questions."""
    try:
        question = request.get("question", "").strip()
        language = request.get("language", "auto")
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        logger.info(f"Processing query: {question[:50]}... (language: {language})")
        
        # Process query through retrieval system
        retrieval_results = retrieval_manager.process_query(question, language)
        
        if not retrieval_results:
            # No relevant context found
            response = {
                "answer": "I'm sorry, I couldn't find specific information about your question in our immigration database. Please try rephrasing your question or consult with an immigration attorney for specific legal advice.",
                "confidence": {
                    "score": 0.0,
                    "level": "low",
                    "context_relevance": 0.0,
                    "source_quality": 0.0,
                    "response_length": 0,
                    "contains_immigration_terms": False,
                    "flagged_for_review": True
                },
                "model": llm_manager.model_name,
                "cached": False
            }
        else:
            # Generate context from retrieval results
            context = retrieval_manager.get_context(retrieval_results)
            
            # Generate response using LLM
            llm_response = llm_manager.generate_response(context, question)
            
            # Calculate confidence score
            confidence_metrics = confidence_manager.calculate_confidence(
                question, llm_response["content"], context, language
            )
            
            # Convert to dictionary and add additional fields
            confidence_info = {
                "score": confidence_metrics.confidence_score,
                "level": confidence_manager.get_confidence_level(confidence_metrics.confidence_score).value,
                "context_relevance": confidence_metrics.context_relevance,
                "source_quality": confidence_metrics.source_quality,
                "response_length": confidence_metrics.response_length,
                "contains_immigration_terms": confidence_metrics.contains_immigration_terms,
                "flagged_for_review": confidence_manager.should_flag_for_review(confidence_metrics.confidence_score)
            }
            
            # Track question if confidence is low
            if confidence_info["flagged_for_review"]:
                question_tracker.track_question(question, language, confidence_info["score"])
            
            response = {
                "answer": llm_response["content"],
                "confidence": confidence_info,
                "model": llm_response["model"],
                "usage": llm_response["usage"],
                "cached": False
            }
        
        return response
        
    except Exception as e:
        logger.exception(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/expert/pending-questions")
def get_pending_questions():
    """Get questions pending expert review."""
    try:
        pending = question_tracker.get_pending_questions()
        return {"pending_questions": pending}
    except Exception as e:
        logger.exception(f"Error getting pending questions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/expert/stats")
def get_expert_stats():
    """Get expert review statistics."""
    try:
        stats = question_tracker.get_frequency_stats()
        return {
            "question_statistics": stats,
            "confidence_threshold": confidence_manager.confidence_threshold,
            "system_info": {
                "total_questions_tracked": len(question_tracker.questions),
                "frequency_records": len(question_tracker.frequency_tracker)
            }
        }
    except Exception as e:
        logger.exception(f"Error getting expert stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/expert/review")
def submit_expert_review(request: Dict[str, Any]):
    """Submit an expert review for a question."""
    try:
        question_id = request.get("question_id")
        expert_answer = request.get("expert_answer")
        expert_sources = request.get("expert_sources", [])
        expert_credentials = request.get("expert_credentials")
        confidence_level = request.get("confidence_level", "medium")
        notes = request.get("notes", "")
        
        if not all([question_id, expert_answer, expert_credentials]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        result = question_tracker.submit_expert_review(
            question_id, expert_answer, expert_sources, 
            expert_credentials, confidence_level, notes
        )
        
        return result
        
    except Exception as e:
        logger.exception(f"Error submitting expert review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/faq/pending-integrations")
def get_pending_integrations():
    """Get questions ready for FAQ integration."""
    try:
        pending = faq_integration.get_pending_integrations()
        return {"pending_integrations": pending}
    except Exception as e:
        logger.exception(f"Error getting pending integrations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/faq/integrate/{question_id}")
def integrate_to_faq(question_id: str):
    """Integrate an expert-reviewed question into the FAQ database."""
    try:
        result = faq_integration.integrate_question(question_id)
        return result
    except Exception as e:
        logger.exception(f"Error integrating to FAQ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/cache/stats")
def get_cache_stats():
    """Get cache statistics."""
    try:
        # Mock cache stats for now
        return {
            "type": "memory",
            "cached_items": 0,
            "hit_rate": 0.0
        }
    except Exception as e:
        logger.exception(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 