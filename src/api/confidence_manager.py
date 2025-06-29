import hashlib
import logging
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from src.api.models import ConfidenceMetrics, ConfidenceLevel, LowConfidenceQuestion, QuestionFrequency
from src.config import config

logger = logging.getLogger(__name__)

class ConfidenceManager:
    def __init__(self, confidence_threshold: Optional[float] = None):
        """
        Initialize confidence manager.
        
        Args:
            confidence_threshold: Threshold below which questions are flagged for expert review.
                                 If None, uses config default.
        """
        self.confidence_threshold = confidence_threshold or config.confidence.threshold
        self.immigration_terms = [
            "visa", "green card", "immigration", "USCIS", "form", "petition",
            "permanent resident", "citizenship", "naturalization", "asylum",
            "refugee", "work permit", "adjustment of status", "consular processing",
            "priority date", "visa bulletin", "labor certification", "affidavit of support",
            "medical examination", "police certificate", "birth certificate", "marriage certificate",
            "divorce decree", "tax returns", "employment authorization", "re-entry permit",
            "conditional residence", "removal of conditions", "waiver", "inadmissibility",
            "deportation", "removal proceedings", "immigration court", "appeal"
        ]
        
        # Chinese immigration terms
        self.chinese_immigration_terms = [
            "签证", "绿卡", "移民", "永久居民", "公民身份", "归化", "庇护", "难民",
            "工作许可", "身份调整", "领事处理", "优先日期", "签证公告", "劳工认证",
            "经济担保", "体检", "警察证明", "出生证明", "结婚证", "离婚判决",
            "纳税申报", "就业授权", "再入境许可", "条件性居留", "解除条件",
            "豁免", "不可入境", "驱逐出境", "驱逐程序", "移民法庭", "上诉"
        ]
    
    def calculate_confidence(self, question: str, response: str, context: str, language: str = "en") -> ConfidenceMetrics:
        """
        Calculate confidence score for a response.
        
        Args:
            question: User's question
            response: Generated response
            context: Retrieved context
            language: Language of the question
            
        Returns:
            ConfidenceMetrics object with detailed confidence analysis
        """
        # Calculate individual confidence factors
        context_relevance = self._calculate_context_relevance(question, context, language)
        source_quality = self._calculate_source_quality(context)
        response_length = len(response)
        contains_immigration_terms = self._check_immigration_terms(response, language)
        
        # Calculate overall confidence score using config weights
        confidence_score = self._calculate_overall_confidence(
            context_relevance, source_quality, response_length, contains_immigration_terms
        )
        
        return ConfidenceMetrics(
            question=question,
            language=language,
            confidence_score=confidence_score,
            context_relevance=context_relevance,
            source_quality=source_quality,
            response_length=response_length,
            contains_immigration_terms=contains_immigration_terms
        )
    
    def _calculate_context_relevance(self, question: str, context: str, language: str) -> float:
        """Calculate how relevant the retrieved context is to the question."""
        if not context or not question:
            return 0.0
        
        # Normalize text for comparison
        question_lower = question.lower().strip()
        context_lower = context.lower().strip()
        
        # Count overlapping words
        question_words = set(re.findall(r'\w+', question_lower))
        context_words = set(re.findall(r'\w+', context_lower))
        
        if not question_words:
            return 0.0
        
        overlap = len(question_words.intersection(context_words))
        relevance = overlap / len(question_words)
        
        # Boost relevance if immigration terms are present
        immigration_terms = self.immigration_terms if language == "en" else self.chinese_immigration_terms
        immigration_overlap = len(set(immigration_terms).intersection(question_words))
        relevance += immigration_overlap * 0.1
        
        return min(relevance, 1.0)
    
    def _calculate_source_quality(self, context: str) -> float:
        """Calculate quality score of the source context."""
        if not context:
            return 0.0
        
        quality_score = 0.5  # Base score
        
        # Boost score for longer, more detailed responses
        if len(context) > 200:
            quality_score += 0.2
        
        # Boost score for structured responses (numbered lists, etc.)
        if re.search(r'\d+\.', context) or re.search(r'[A-Z]\.', context):
            quality_score += 0.1
        
        # Boost score for official terminology
        official_terms = ["USCIS", "Form", "Department of State", "immigration law"]
        for term in official_terms:
            if term.lower() in context.lower():
                quality_score += 0.1
        
        return min(quality_score, 1.0)
    
    def _check_immigration_terms(self, response: str, language: str) -> bool:
        """Check if response contains immigration-related terms."""
        response_lower = response.lower()
        terms = self.immigration_terms if language == "en" else self.chinese_immigration_terms
        
        for term in terms:
            if term.lower() in response_lower:
                return True
        return False
    
    def _calculate_overall_confidence(self, context_relevance: float, source_quality: float, 
                                    response_length: int, contains_immigration_terms: bool) -> float:
        """Calculate overall confidence score using config weights."""
        # Use config weights for weighted combination
        confidence = (
            context_relevance * config.confidence.context_weight +
            source_quality * config.confidence.source_weight +
            min(response_length / 500, 1.0) * config.confidence.length_weight +
            (config.confidence.terms_weight if contains_immigration_terms else 0.0)
        )
        
        return min(confidence, 1.0)
    
    def get_confidence_level(self, confidence_score: float) -> ConfidenceLevel:
        """Convert confidence score to confidence level."""
        if confidence_score >= 0.8:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def should_flag_for_review(self, confidence_score: float) -> bool:
        """Determine if a question should be flagged for expert review."""
        return confidence_score < self.confidence_threshold
    
    def generate_question_hash(self, question: str, language: str) -> str:
        """Generate a unique hash for a question."""
        normalized = f"{question.strip().lower()}:{language}"
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current confidence configuration."""
        return {
            "threshold": self.confidence_threshold,
            "weights": {
                "context": config.confidence.context_weight,
                "source": config.confidence.source_weight,
                "length": config.confidence.length_weight,
                "terms": config.confidence.terms_weight
            },
            "immigration_terms_count": {
                "english": len(self.immigration_terms),
                "chinese": len(self.chinese_immigration_terms)
            }
        } 