from typing import Dict, List, Any
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_language_code(language: str) -> bool:
    """Validate if the language code is supported."""
    supported_languages = ['en', 'zh']
    if language not in supported_languages:
        raise ValidationError(f"Unsupported language code: {language}. Supported languages: {supported_languages}")
    return True

def validate_faq_structure(faq: Dict[str, Any]) -> bool:
    """Validate the structure of a single FAQ entry."""
    required_fields = ['id', 'language', 'question', 'answer']
    
    # Check for required fields
    for field in required_fields:
        if field not in faq:
            raise ValidationError(f"Missing required field '{field}' in FAQ entry")
    
    # Validate field types
    if not isinstance(faq['id'], str):
        raise ValidationError(f"FAQ ID must be a string, got {type(faq['id'])}")
    if not isinstance(faq['language'], str):
        raise ValidationError(f"Language must be a string, got {type(faq['language'])}")
    if not isinstance(faq['question'], str):
        raise ValidationError(f"Question must be a string, got {type(faq['question'])}")
    if not isinstance(faq['answer'], str):
        raise ValidationError(f"Answer must be a string, got {type(faq['answer'])}")
    
    # Validate content
    if not faq['question'].strip():
        raise ValidationError("Question cannot be empty")
    if not faq['answer'].strip():
        raise ValidationError("Answer cannot be empty")
    
    # Validate language code
    validate_language_code(faq['language'])
    
    return True

def validate_knowledge_base(faqs: List[Dict[str, Any]]) -> bool:
    """Validate the entire knowledge base."""
    if not isinstance(faqs, list):
        raise ValidationError(f"Knowledge base must be a list, got {type(faqs)}")
    
    if not faqs:
        raise ValidationError("Knowledge base cannot be empty")
    
    # Check for duplicate IDs
    ids = set()
    for faq in faqs:
        if faq['id'] in ids:
            raise ValidationError(f"Duplicate FAQ ID found: {faq['id']}")
        ids.add(faq['id'])
        validate_faq_structure(faq)
    
    return True

def load_and_validate_knowledge_base(file_path: str) -> List[Dict[str, Any]]:
    """Load and validate the knowledge base from a JSON file."""
    try:
        path = Path(file_path)
        if not path.exists():
            raise ValidationError(f"Knowledge base file not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON format: {str(e)}")
        
        if 'faqs' not in data:
            raise ValidationError("Missing 'faqs' key in knowledge base file")
        
        validate_knowledge_base(data['faqs'])
        logger.info(f"Successfully validated knowledge base with {len(data['faqs'])} FAQs")
        return data['faqs']
    
    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        raise 