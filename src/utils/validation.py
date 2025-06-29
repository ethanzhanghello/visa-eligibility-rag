"""
Validation utilities for the Green Card RAG Helper.
"""
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error."""
    pass

def validate_faq_data(faq_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate FAQ data structure and content.
    
    Args:
        faq_data: FAQ data dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required top-level keys
    required_keys = ['faqs']
    for key in required_keys:
        if key not in faq_data:
            errors.append(f"Missing required key: {key}")
    
    if 'faqs' not in faq_data:
        return False, errors
    
    # Validate each FAQ entry
    for i, faq in enumerate(faq_data['faqs']):
        faq_errors = validate_faq_entry(faq, i)
        errors.extend(faq_errors)
    
    return len(errors) == 0, errors

def validate_faq_entry(faq: Dict[str, Any], index: int) -> List[str]:
    """
    Validate a single FAQ entry.
    
    Args:
        faq: FAQ entry dictionary
        index: Index of the FAQ entry
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Required fields
    required_fields = ['id', 'language', 'question', 'answer']
    for field in required_fields:
        if field not in faq:
            errors.append(f"FAQ {index}: Missing required field '{field}'")
            continue
        
        if not faq[field]:
            errors.append(f"FAQ {index}: Field '{field}' cannot be empty")
    
    # Validate language
    if 'language' in faq:
        valid_languages = ['en', 'zh']
        if faq['language'] not in valid_languages:
            errors.append(f"FAQ {index}: Invalid language '{faq['language']}'. Must be one of: {valid_languages}")
    
    # Validate content length
    if 'question' in faq and len(faq['question']) > 500:
        errors.append(f"FAQ {index}: Question too long ({len(faq['question'])} chars, max 500)")
    
    if 'answer' in faq and len(faq['answer']) > 2000:
        errors.append(f"FAQ {index}: Answer too long ({len(faq['answer'])} chars, max 2000)")
    
    # Validate ID format
    if 'id' in faq:
        if not re.match(r'^[a-z0-9-]+$', faq['id']):
            errors.append(f"FAQ {index}: Invalid ID format '{faq['id']}'. Use lowercase letters, numbers, and hyphens only")
    
    return errors

def validate_question_input(question: str, language: str) -> Tuple[bool, List[str]]:
    """
    Validate user question input.
    
    Args:
        question: User's question
        language: Language code
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check question length
    if not question or not question.strip():
        errors.append("Question cannot be empty")
    elif len(question.strip()) > 1000:
        errors.append("Question too long (max 1000 characters)")
    elif len(question.strip()) < 3:
        errors.append("Question too short (min 3 characters)")
    
    # Check for suspicious content
    suspicious_patterns = [
        r'<script',
        r'javascript:',
        r'data:text/html',
        r'vbscript:',
        r'onload=',
        r'onerror='
    ]
    
    question_lower = question.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, question_lower):
            errors.append("Question contains potentially harmful content")
            break
    
    # Validate language
    valid_languages = ['en', 'zh', 'auto']
    if language not in valid_languages:
        errors.append(f"Invalid language '{language}'. Must be one of: {valid_languages}")
    
    return len(errors) == 0, errors

def validate_expert_review(review_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate expert review submission.
    
    Args:
        review_data: Expert review data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    required_fields = ['question_id', 'expert_answer', 'expert_credentials']
    for field in required_fields:
        if field not in review_data or not review_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate answer length
    if 'expert_answer' in review_data:
        answer = review_data['expert_answer']
        if len(answer) < 10:
            errors.append("Expert answer too short (min 10 characters)")
        elif len(answer) > 5000:
            errors.append("Expert answer too long (max 5000 characters)")
    
    # Validate credentials
    if 'expert_credentials' in review_data:
        credentials = review_data['expert_credentials']
        if len(credentials) < 5:
            errors.append("Expert credentials too short (min 5 characters)")
        elif len(credentials) > 200:
            errors.append("Expert credentials too long (max 200 characters)")
    
    # Validate sources
    if 'expert_sources' in review_data:
        sources = review_data['expert_sources']
        if isinstance(sources, list):
            for i, source in enumerate(sources):
                if not re.match(r'^https?://', source):
                    errors.append(f"Source {i+1} must be a valid URL")
        else:
            errors.append("Expert sources must be a list")
    
    # Validate confidence level
    if 'confidence_level' in review_data:
        valid_levels = ['high', 'medium', 'low']
        if review_data['confidence_level'] not in valid_levels:
            errors.append(f"Invalid confidence level. Must be one of: {valid_levels}")
    
    return len(errors) == 0, errors

def sanitize_text(text: str) -> str:
    """
    Sanitize text input to prevent injection attacks.
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def validate_embedding_data(embedding_data: List[float]) -> bool:
    """
    Validate embedding vector data.
    
    Args:
        embedding_data: List of embedding values
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(embedding_data, list):
        return False
    
    if len(embedding_data) == 0:
        return False
    
    # Check for NaN or infinite values
    for value in embedding_data:
        if not isinstance(value, (int, float)):
            return False
        if not (float('-inf') < value < float('inf')):
            return False
    
    return True

def validate_api_response(response_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate API response structure.
    
    Args:
        response_data: API response data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    required_fields = ['answer', 'confidence', 'model']
    for field in required_fields:
        if field not in response_data:
            errors.append(f"Missing required response field: {field}")
    
    # Validate confidence structure
    if 'confidence' in response_data:
        confidence = response_data['confidence']
        if not isinstance(confidence, dict):
            errors.append("Confidence must be a dictionary")
        else:
            required_confidence_fields = ['score', 'level']
            for field in required_confidence_fields:
                if field not in confidence:
                    errors.append(f"Missing confidence field: {field}")
    
    # Validate model field
    if 'model' in response_data and not response_data['model']:
        errors.append("Model field cannot be empty")
    
    return len(errors) == 0, errors

def log_validation_errors(errors: List[str], context: str = ""):
    """
    Log validation errors.
    
    Args:
        errors: List of validation errors
        context: Context for the validation
    """
    if errors:
        error_msg = f"Validation errors {context}: " + "; ".join(errors)
        logger.warning(error_msg) 