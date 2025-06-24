"""
Test the low-confidence question detection and expert review system.
"""
import pytest
import tempfile
import json
from unittest.mock import Mock, patch
from datetime import datetime
from src.api.confidence_manager import ConfidenceManager
from src.api.question_tracker import QuestionTracker
from src.api.faq_integration import FAQIntegrationManager
from src.api.models import (
    ConfidenceLevel, ReviewStatus, ExpertReviewRequest, 
    LowConfidenceQuestion, QuestionFrequency
)

@pytest.fixture
def confidence_manager():
    """Create a confidence manager for testing."""
    return ConfidenceManager(confidence_threshold=0.7)

@pytest.fixture
def temp_storage_file():
    """Create a temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"questions": {}, "frequency": {}}, f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    import os
    os.unlink(temp_file)

@pytest.fixture
def question_tracker(temp_storage_file):
    """Create a question tracker with temporary storage."""
    return QuestionTracker(storage_file=temp_storage_file)

@pytest.fixture
def faq_integration():
    """Create a FAQ integration manager for testing."""
    return FAQIntegrationManager()

def test_confidence_calculation(confidence_manager):
    """Test confidence score calculation."""
    question = "What documents do I need for EB-2 visa?"
    response = "For EB-2 visa, you need: 1) Valid passport, 2) Birth certificate, 3) Form I-140 approval, 4) Medical examination results, 5) Police certificates."
    context = "EB-2 visa requirements include Form I-140, medical examination, and police certificates."
    
    metrics = confidence_manager.calculate_confidence(question, response, context, "en")
    
    assert 0.0 <= metrics.confidence_score <= 1.0
    assert 0.0 <= metrics.context_relevance <= 1.0
    assert 0.0 <= metrics.source_quality <= 1.0
    assert metrics.contains_immigration_terms is True
    assert metrics.response_length > 0

def test_confidence_level_classification(confidence_manager):
    """Test confidence level classification."""
    assert confidence_manager.get_confidence_level(0.9) == ConfidenceLevel.HIGH
    assert confidence_manager.get_confidence_level(0.7) == ConfidenceLevel.MEDIUM
    assert confidence_manager.get_confidence_level(0.5) == ConfidenceLevel.LOW

def test_question_flagging(confidence_manager):
    """Test if questions are flagged for review based on confidence threshold."""
    assert confidence_manager.should_flag_for_review(0.5) is True  # Below threshold
    assert confidence_manager.should_flag_for_review(0.8) is False  # Above threshold

def test_question_hash_generation(confidence_manager):
    """Test question hash generation."""
    hash1 = confidence_manager.generate_question_hash("What is EB-2?", "en")
    hash2 = confidence_manager.generate_question_hash("what is eb-2?", "en")
    hash3 = confidence_manager.generate_question_hash("What is EB-2?", "zh")
    
    assert hash1 == hash2  # Same question, same language
    assert hash1 != hash3  # Same question, different language

def test_question_tracking(question_tracker):
    """Test question tracking functionality."""
    question = "What documents do I need for EB-2?"
    language = "en"
    confidence_score = 0.5  # Low confidence
    
    # Track the question
    question_id = question_tracker.track_question(question, language, confidence_score)
    
    assert question_id is not None
    assert question_id in question_tracker.questions
    
    # Check that the question was stored correctly
    stored_question = question_tracker.questions[question_id]
    assert stored_question.question == question
    assert stored_question.language == language
    assert stored_question.confidence_score == confidence_score
    assert stored_question.status == ReviewStatus.PENDING

def test_question_frequency_tracking(question_tracker):
    """Test that question frequency is tracked correctly."""
    question = "What documents do I need for EB-2?"
    language = "en"
    
    # Track the same question multiple times
    question_id1 = question_tracker.track_question(question, language, 0.5)
    question_id2 = question_tracker.track_question(question, language, 0.6)
    
    # Should be the same question ID
    assert question_id1 == question_id2
    
    # Check frequency count
    stored_question = question_tracker.questions[question_id1]
    assert stored_question.frequency_count == 2

def test_pending_questions_retrieval(question_tracker):
    """Test retrieval of pending questions."""
    # Add some test questions
    question_tracker.track_question("Question 1", "en", 0.5)
    question_tracker.track_question("Question 2", "en", 0.6)
    question_tracker.track_question("Question 3", "en", 0.7)
    
    pending = question_tracker.get_pending_questions()
    
    assert len(pending) >= 2  # At least 2 should be pending (low confidence)
    assert all(q.status == ReviewStatus.PENDING for q in pending)

def test_expert_review_submission(question_tracker):
    """Test expert review submission."""
    # First track a question
    question_id = question_tracker.track_question("Test question", "en", 0.5)
    
    # Submit expert review
    review_request = ExpertReviewRequest(
        question_id=question_id,
        expert_answer="This is the expert answer with proper sources.",
        expert_sources=["uscis.gov/forms", "immigration.gov"],
        expert_credentials="Immigration Attorney, 10+ years experience",
        confidence_level=ConfidenceLevel.HIGH,
        notes="This is a common question that needs clear guidance."
    )
    
    success = question_tracker.add_expert_review(review_request)
    assert success is True
    
    # Check that the question was updated
    question = question_tracker.get_question_by_id(question_id)
    assert question.status == ReviewStatus.APPROVED
    assert question.expert_answer == review_request.expert_answer
    assert question.expert_sources == review_request.expert_sources
    assert question.expert_credentials == review_request.expert_credentials

def test_faq_integration_validation(faq_integration):
    """Test FAQ integration validation."""
    # Create a mock question for validation testing
    mock_question = LowConfidenceQuestion(
        id="test_question",
        question="What documents do I need for EB-2?",
        language="en",
        confidence_score=0.5,
        frequency_count=3,
        expert_answer="You need Form I-140, medical examination, and police certificates.",
        expert_sources=["uscis.gov/forms/i-140", "state.gov/visa"],
        expert_credentials="Immigration Attorney",
        status=ReviewStatus.APPROVED
    )
    
    # Mock the question tracker to return our test question
    with patch.object(faq_integration.question_tracker, 'get_question_by_id', return_value=mock_question):
        validation = faq_integration.validate_expert_review("test_question")
        
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0
        assert "official government sources" not in [w.lower() for w in validation["warnings"]]

def test_faq_integration_validation_with_issues(faq_integration):
    """Test FAQ integration validation with potential issues."""
    # Create a mock question with issues
    mock_question = LowConfidenceQuestion(
        id="test_question_bad",
        question="What is the weather like?",
        language="en",
        confidence_score=0.5,
        frequency_count=1,
        expert_answer="It depends on the location.",
        expert_sources=["weather.com"],
        expert_credentials="",
        status=ReviewStatus.APPROVED
    )
    
    # Mock the question tracker to return our test question
    with patch.object(faq_integration.question_tracker, 'get_question_by_id', return_value=mock_question):
        validation = faq_integration.validate_expert_review("test_question_bad")
        
        assert validation["valid"] is True  # Still valid but with warnings
        assert len(validation["warnings"]) > 0
        assert any("official government sources" in w.lower() for w in validation["warnings"])
        assert any("immigration-related" in w.lower() for w in validation["warnings"])

def test_chinese_immigration_terms(confidence_manager):
    """Test confidence calculation with Chinese immigration terms."""
    question = "我需要哪些文件来申请 EB-2？"
    response = "申请 EB-2 需要：1）有效护照，2）出生证明，3）I-140 表格批准，4）体检结果，5）警察证明。"
    context = "EB-2 签证要求包括 I-140 表格、体检和警察证明。"
    
    metrics = confidence_manager.calculate_confidence(question, response, context, "zh")
    
    assert metrics.contains_immigration_terms is True
    assert 0.0 <= metrics.confidence_score <= 1.0

def test_confidence_threshold_configuration():
    """Test that confidence threshold can be configured."""
    high_threshold_manager = ConfidenceManager(confidence_threshold=0.9)
    low_threshold_manager = ConfidenceManager(confidence_threshold=0.3)
    
    # Same confidence score should be flagged differently
    confidence_score = 0.5
    assert high_threshold_manager.should_flag_for_review(confidence_score) is True
    assert low_threshold_manager.should_flag_for_review(confidence_score) is False 