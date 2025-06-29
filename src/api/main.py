"""
Main FastAPI application for the Green Card RAG Helper.
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from typing import Dict, Any, Optional
import os
import time
from datetime import datetime
import json

# Import managers
from src.retrieval.retrieval_manager import RetrievalManager
from src.api.confidence_manager import ConfidenceManager
from src.api.question_tracker import QuestionTracker
from src.api.faq_integration import FAQIntegrationManager
from src.api.models import QueryRequest, QueryResponse, HealthResponse, ExpertReviewRequest
from src.config import config
from src.utils.validation import validate_question_input, validate_expert_review, sanitize_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_WINDOW = config.api.rate_limit_window
RATE_LIMIT_MAX_REQUESTS = config.api.rate_limit_max_requests

# Simple in-memory rate limiting
request_counts = {}

def check_rate_limit(request: Request):
    """Check rate limit for the client."""
    global request_counts
    
    if not config.security.enable_rate_limiting:
        return
        
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old entries
    request_counts = {ip: (count, timestamp) for ip, (count, timestamp) in request_counts.items() 
                     if current_time - timestamp < RATE_LIMIT_WINDOW}
    
    if client_ip in request_counts:
        count, timestamp = request_counts[client_ip]
        if current_time - timestamp < RATE_LIMIT_WINDOW and count >= RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        request_counts[client_ip] = (count + 1, timestamp)
    else:
        request_counts[client_ip] = (1, current_time)

def validate_configuration():
    """Validate configuration on startup."""
    logger.info("Validating configuration...")
    errors = config.validate()
    
    if errors:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        raise ValueError("Configuration validation failed. Please check your environment variables.")
    
    logger.info("Configuration validation passed")

# Initialize FastAPI app
app = FastAPI(
    title="Green Card RAG Helper API",
    description="Bilingual immigration assistant with expert review system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.security.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if config.security.trusted_hosts:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=config.security.trusted_hosts
    )

# Validate configuration on startup
@app.on_event("startup")
async def startup_event():
    """Validate configuration and initialize managers on startup."""
    try:
        validate_configuration()
        
        # Initialize managers
        global retrieval_manager, confidence_manager, question_tracker, faq_integration, llm_manager
        
        retrieval_manager = RetrievalManager()
        confidence_manager = ConfidenceManager()
        question_tracker = QuestionTracker()
        faq_integration = FAQIntegrationManager()
        
        # Use real LLM manager if API key is available, otherwise use mock
        if config.llm.api_key:  # Enable real LLM
            from src.llm.llm_manager import LLMManager
            llm_manager = LLMManager()
            # Test LLM connection
            if not llm_manager.test_connection():
                logger.warning("LLM connection test failed, falling back to mock manager")
                llm_manager = MockLLMManager()
        else:
            llm_manager = MockLLMManager()
        
        logger.info("All managers initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

# Initialize managers (will be set in startup_event)
retrieval_manager = None
confidence_manager = None
question_tracker = None
faq_integration = None
llm_manager = None

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
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get mock config summary."""
        return {
            "model_name": self.model_name,
            "temperature": config.llm.temperature,
            "max_tokens": config.llm.max_tokens,
            "api_key_set": False
        }

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    # Check if managers are initialized
    managers_healthy = all([
        retrieval_manager is not None,
        confidence_manager is not None,
        question_tracker is not None,
        faq_integration is not None,
        llm_manager is not None
    ])
    
    status = "healthy" if managers_healthy else "unhealthy"
    message = "Green Card RAG Helper API is running" if managers_healthy else "API is not fully initialized"
    
    return HealthResponse(
        status=status,
        message=message,
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.get("/config")
def get_config():
    """Get current configuration (without sensitive data)."""
    return config.to_dict()

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: Request, query_request: QueryRequest):
    """Main query endpoint for processing immigration questions."""
    try:
        # Check rate limit
        check_rate_limit(request)
        
        # Validate and sanitize input
        is_valid, validation_errors = validate_question_input(query_request.question, query_request.language)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid input: {'; '.join(validation_errors)}")
        
        # Sanitize the question
        sanitized_question = sanitize_text(query_request.question)
        
        logger.info(f"Processing query: {sanitized_question[:50]}... (language: {query_request.language})")
        
        # Process query through retrieval system
        retrieval_results = retrieval_manager.process_query(sanitized_question, query_request.language)
        
        if not retrieval_results:
            # No relevant context found
            response = QueryResponse(
                answer="I'm sorry, I couldn't find specific information about your question in our immigration database. Please try rephrasing your question or consult with an immigration attorney for specific legal advice.",
                confidence={
                    "score": 0.0,
                    "level": "low",
                    "context_relevance": 0.0,
                    "source_quality": 0.0,
                    "response_length": 0,
                    "contains_immigration_terms": False,
                    "flagged_for_review": True
                },
                model=llm_manager.model_name,
                cached=False
            )
        else:
            # Generate context from retrieval results
            context = retrieval_manager.get_context(retrieval_results)
            
            # Generate response using LLM
            llm_response = llm_manager.generate_response(context, sanitized_question)
            
            # Calculate confidence score
            confidence_metrics = confidence_manager.calculate_confidence(
                sanitized_question, llm_response["content"], context, query_request.language
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
                question_tracker.track_question(sanitized_question, query_request.language, confidence_info["score"])
            
            response = QueryResponse(
                answer=llm_response["content"],
                confidence=confidence_info,
                model=llm_response["model"],
                usage=llm_response["usage"],
                cached=False
            )
        
        return response
        
    except HTTPException:
        raise
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
def submit_expert_review(request: Request, review_request: ExpertReviewRequest):
    """Submit an expert review for a question."""
    try:
        # Check rate limit
        check_rate_limit(request)
        
        # Validate expert review data
        review_data = {
            "question_id": review_request.question_id,
            "expert_answer": review_request.expert_answer,
            "expert_sources": review_request.expert_sources,
            "expert_credentials": review_request.expert_credentials,
            "confidence_level": review_request.confidence_level,
            "notes": review_request.notes
        }
        
        is_valid, validation_errors = validate_expert_review(review_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid expert review: {'; '.join(validation_errors)}")
        
        # Sanitize inputs
        sanitized_answer = sanitize_text(review_request.expert_answer)
        sanitized_credentials = sanitize_text(review_request.expert_credentials)
        sanitized_notes = sanitize_text(review_request.notes) if review_request.notes else ""
        
        result = question_tracker.submit_expert_review(
            review_request.question_id, 
            sanitized_answer, 
            review_request.expert_sources, 
            sanitized_credentials, 
            review_request.confidence_level, 
            sanitized_notes
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error submitting expert review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/faq/pending-integrations")
def get_pending_integrations():
    """Get questions pending FAQ integration."""
    try:
        pending = faq_integration.get_pending_integrations()
        return {"pending_integrations": pending}
    except Exception as e:
        logger.exception(f"Error getting pending integrations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/faq/integrate/{question_id}")
def integrate_to_faq(question_id: str):
    """Integrate a question into the FAQ database."""
    try:
        # Validate question_id format
        if not question_id or not question_id.strip():
            raise HTTPException(status_code=400, detail="Question ID is required")
        
        result = faq_integration.integrate_question(question_id)
        return result
    except Exception as e:
        logger.exception(f"Error integrating to FAQ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/cache/stats")
def get_cache_stats():
    """Get cache statistics."""
    try:
        # This would be implemented with your cache manager
        return {"cache_stats": "Not implemented yet"}
    except Exception as e:
        logger.exception(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/system/info")
def get_system_info():
    """Get system information and configuration summary."""
    try:
        return {
            "version": "1.0.0",
            "config": config.to_dict(),
            "managers": {
                "retrieval": retrieval_manager is not None,
                "confidence": confidence_manager is not None,
                "question_tracker": question_tracker is not None,
                "faq_integration": faq_integration is not None,
                "llm": llm_manager is not None
            },
            "llm_config": llm_manager.get_config_summary() if llm_manager else None,
            "confidence_config": confidence_manager.get_config_summary() if confidence_manager else None
        }
    except Exception as e:
        logger.exception(f"Error getting system info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors."""
    return {"error": "Endpoint not found", "path": request.url.path}

@app.exception_handler(429)
async def rate_limit_handler(request: Request, exc: HTTPException):
    """Handle rate limit errors."""
    return {"error": "Rate limit exceeded", "retry_after": RATE_LIMIT_WINDOW}

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {exc.detail}")
    return {"error": "Internal server error", "message": "Please try again later"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
        workers=config.api.workers
    ) 