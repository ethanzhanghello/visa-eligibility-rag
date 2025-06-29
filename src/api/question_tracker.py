import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.api.models import (
    LowConfidenceQuestion, QuestionFrequency, ReviewStatus, 
    ExpertReviewRequest, ExpertReviewResponse
)
from src.api.confidence_manager import ConfidenceManager

logger = logging.getLogger(__name__)

class QuestionTracker:
    def __init__(self, storage_file: str = "low_confidence_questions.json"):
        """
        Initialize question tracker.
        
        Args:
            storage_file: File to store low-confidence questions
        """
        self.storage_file = storage_file
        self.confidence_manager = ConfidenceManager()
        self.questions: Dict[str, LowConfidenceQuestion] = {}
        self.frequency_tracker: Dict[str, QuestionFrequency] = {}
        self._load_data()
    
    def _load_data(self):
        """Load existing data from storage file."""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = {
                    qid: LowConfidenceQuestion(**q) 
                    for qid, q in data.get('questions', {}).items()
                }
                self.frequency_tracker = {
                    qhash: QuestionFrequency(**f) 
                    for qhash, f in data.get('frequency', {}).items()
                }
            logger.info(f"Loaded {len(self.questions)} questions and {len(self.frequency_tracker)} frequency records")
        except FileNotFoundError:
            logger.info("No existing data found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def _save_data(self):
        """Save data to storage file."""
        try:
            data = {
                'questions': {
                    qid: q.model_dump() for qid, q in self.questions.items()
                },
                'frequency': {
                    qhash: f.model_dump() for qhash, f in self.frequency_tracker.items()
                }
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def track_question(self, question: str, language: str, confidence_score: float) -> Optional[str]:
        """
        Track a low-confidence question.
        
        Args:
            question: The question asked
            language: Language of the question
            confidence_score: Confidence score of the response
            
        Returns:
            Question ID if flagged for review, None otherwise
        """
        if not self.confidence_manager.should_flag_for_review(confidence_score):
            return None
        
        question_hash = self.confidence_manager.generate_question_hash(question, language)
        now = datetime.now()
        
        # Update frequency tracking
        if question_hash in self.frequency_tracker:
            freq = self.frequency_tracker[question_hash]
            freq.frequency_count += 1
            freq.last_seen = now.isoformat()
            freq.average_confidence = (
                (freq.average_confidence * (freq.frequency_count - 1) + confidence_score) 
                / freq.frequency_count
            )
        else:
            self.frequency_tracker[question_hash] = QuestionFrequency(
                question_hash=question_hash,
                question=question,
                language=language,
                frequency_count=1,
                first_seen=now.isoformat(),
                last_seen=now.isoformat(),
                average_confidence=confidence_score
            )
        
        # Check if we already have this question in our tracking
        existing_question_id = None
        for qid, q in self.questions.items():
            if q.question == question and q.language == language:
                existing_question_id = qid
                break
        
        if existing_question_id:
            # Update existing question
            existing = self.questions[existing_question_id]
            existing.frequency_count += 1
            existing.last_asked = now.isoformat()
            existing.audit_trail.append({
                "action": "repeated_question",
                "timestamp": now.isoformat(),
                "confidence_score": confidence_score,
                "frequency_count": existing.frequency_count
            })
            self._save_data()
            logger.info(f"Updated existing low-confidence question: {existing_question_id}")
            return existing_question_id
        else:
            # Create new question entry
            question_id = f"q_{len(self.questions) + 1}_{question_hash[:8]}"
            self.questions[question_id] = LowConfidenceQuestion(
                id=question_id,
                question=question,
                language=language,
                confidence_score=confidence_score,
                frequency_count=1,
                first_asked=now.isoformat(),
                last_asked=now.isoformat(),
                status=ReviewStatus.PENDING,
                audit_trail=[{
                    "action": "flagged_for_review",
                    "timestamp": now.isoformat(),
                    "confidence_score": confidence_score,
                    "frequency_count": 1
                }]
            )
            self._save_data()
            logger.info(f"New low-confidence question flagged: {question_id}")
            return question_id
    
    def get_pending_questions(self, limit: int = 50) -> List[LowConfidenceQuestion]:
        """Get questions pending expert review, prioritized by frequency."""
        pending = [
            q for q in self.questions.values() 
            if q.status == ReviewStatus.PENDING
        ]
        
        # Sort by frequency count (descending) and then by first asked (ascending)
        pending.sort(key=lambda x: (-x.frequency_count, x.first_asked))
        
        return pending[:limit]
    
    def get_question_by_id(self, question_id: str) -> Optional[LowConfidenceQuestion]:
        """Get a specific question by ID."""
        return self.questions.get(question_id)
    
    def update_question_status(self, question_id: str, status: ReviewStatus, 
                             expert_reviewer: Optional[str] = None) -> bool:
        """Update the status of a question."""
        if question_id not in self.questions:
            return False
        
        question = self.questions[question_id]
        question.status = status
        if expert_reviewer:
            question.expert_reviewer = expert_reviewer
        
        question.audit_trail.append({
            "action": "status_update",
            "timestamp": datetime.now().isoformat(),
            "new_status": status,
            "expert_reviewer": expert_reviewer
        })
        
        self._save_data()
        logger.info(f"Updated question {question_id} status to {status}")
        return True
    
    def add_expert_review(self, review_request: ExpertReviewRequest) -> bool:
        """Add expert review to a question."""
        if review_request.question_id not in self.questions:
            return False
        
        question = self.questions[review_request.question_id]
        question.expert_answer = review_request.expert_answer
        question.expert_sources = review_request.expert_sources
        question.expert_credentials = review_request.expert_credentials
        question.review_date = datetime.now().isoformat()
        question.status = ReviewStatus.APPROVED
        
        question.audit_trail.append({
            "action": "expert_review",
            "timestamp": datetime.now().isoformat(),
            "expert_credentials": review_request.expert_credentials,
            "confidence_level": review_request.confidence_level,
            "notes": review_request.notes
        })
        
        self._save_data()
        logger.info(f"Added expert review to question {review_request.question_id}")
        return True
    
    def get_frequency_stats(self) -> Dict[str, Any]:
        """Get statistics about question frequency."""
        total_questions = len(self.questions)
        pending_questions = len([q for q in self.questions.values() if q.status == ReviewStatus.PENDING])
        reviewed_questions = len([q for q in self.questions.values() if q.status == ReviewStatus.APPROVED])
        
        # Top 5 most frequent questions
        top_frequent = sorted(
            self.questions.values(), 
            key=lambda x: x.frequency_count, 
            reverse=True
        )[:5]
        
        return {
            "total_questions": total_questions,
            "pending_questions": pending_questions,
            "reviewed_questions": reviewed_questions,
            "top_frequent_questions": [
                {
                    "id": q.id,
                    "question": q.question[:100] + "..." if len(q.question) > 100 else q.question,
                    "frequency": q.frequency_count,
                    "status": q.status
                }
                for q in top_frequent
            ]
        } 