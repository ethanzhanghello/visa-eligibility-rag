"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import re

class ConfidenceLevel(str, Enum):
    """Confidence level enumeration."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ReviewStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")
    language: str = Field(default="auto", description="Language code (en, zh, auto)")
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()
    
    @validator('language')
    def validate_language(cls, v):
        valid_languages = ['en', 'zh', 'auto']
        if v not in valid_languages:
            raise ValueError(f"Language must be one of: {valid_languages}")
        return v

class LowConfidenceQuestion(BaseModel):
    """Model for low confidence questions."""
    id: str
    question: str
    language: str
    confidence_score: float
    frequency_count: int
    first_asked: str
    last_asked: str
    status: str
    expert_reviewer: Optional[str] = None
    expert_answer: Optional[str] = None
    expert_sources: Optional[List[str]] = None
    expert_credentials: Optional[str] = None
    review_date: Optional[str] = None
    audit_trail: List[Dict[str, Any]] = []

class ExpertReviewRequest(BaseModel):
    """Request model for expert review submission."""
    question_id: str = Field(..., description="ID of the question to review")
    expert_answer: str = Field(..., min_length=10, max_length=5000, description="Expert's answer")
    expert_sources: List[str] = Field(default=[], description="List of source URLs")
    expert_credentials: str = Field(..., min_length=5, max_length=200, description="Expert's credentials")
    confidence_level: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM, description="Expert's confidence level")
    notes: Optional[str] = Field(default="", max_length=1000, description="Additional notes")
    
    @validator('expert_sources')
    def validate_sources(cls, v):
        for source in v:
            if not re.match(r'^https?://', source):
                raise ValueError("Sources must be valid URLs")
        return v

class ExpertReviewResponse(BaseModel):
    question_id: str
    status: ReviewStatus
    expert_answer: str
    expert_sources: List[str]
    expert_credentials: str
    review_date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None

class QuestionFrequency(BaseModel):
    """Model for question frequency tracking."""
    question_hash: str
    question: str
    language: str
    frequency_count: int
    first_seen: str
    last_seen: str
    average_confidence: float

class ConfidenceMetrics(BaseModel):
    """Confidence metrics model."""
    question: str
    language: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    context_relevance: float = Field(..., ge=0.0, le=1.0)
    source_quality: float = Field(..., ge=0.0, le=1.0)
    response_length: int = Field(..., ge=0)
    contains_immigration_terms: bool

class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    answer: str
    confidence: Dict[str, Any]
    model: str
    usage: Optional[Dict[str, int]] = None
    cached: bool = False

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str
    version: str
    timestamp: str 