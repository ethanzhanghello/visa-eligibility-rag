from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ReviewStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class LowConfidenceQuestion(BaseModel):
    id: Optional[str] = None
    question: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(..., regex="^(en|zh|auto)$")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    frequency_count: int = Field(default=1, ge=1)
    first_asked: datetime = Field(default_factory=datetime.now)
    last_asked: datetime = Field(default_factory=datetime.now)
    status: ReviewStatus = Field(default=ReviewStatus.PENDING)
    expert_reviewer: Optional[str] = None
    expert_answer: Optional[str] = None
    expert_sources: Optional[List[str]] = None
    expert_credentials: Optional[str] = None
    review_date: Optional[datetime] = None
    audit_trail: List[Dict[str, Any]] = Field(default_factory=list)

class ExpertReviewRequest(BaseModel):
    question_id: str
    expert_answer: str = Field(..., min_length=1, max_length=5000)
    expert_sources: List[str] = Field(..., min_items=1)
    expert_credentials: str = Field(..., min_length=1)
    confidence_level: ConfidenceLevel
    notes: Optional[str] = None

class ExpertReviewResponse(BaseModel):
    question_id: str
    status: ReviewStatus
    expert_answer: str
    expert_sources: List[str]
    expert_credentials: str
    review_date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None

class QuestionFrequency(BaseModel):
    question_hash: str
    question: str
    language: str
    frequency_count: int = Field(default=1, ge=1)
    first_seen: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    average_confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class ConfidenceMetrics(BaseModel):
    question: str
    language: str
    confidence_score: float
    context_relevance: float
    source_quality: float
    response_length: int
    contains_immigration_terms: bool
    timestamp: datetime = Field(default_factory=datetime.now) 