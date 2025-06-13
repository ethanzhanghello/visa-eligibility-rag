"""
Script to populate the vector database with FAQ embeddings.
"""
import sys
from pathlib import Path
import logging
import numpy as np
import json

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.embeddings.embedding_utils import EmbeddingManager
from src.vector_db.vector_db_manager import VectorDBManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def populate_vector_db():
    """Populate the vector database with FAQ embeddings."""
    try:
        # Initialize managers
        embedding_manager = EmbeddingManager()
        vector_db_manager = VectorDBManager()
        
        # Load FAQs
        faq_path = Path(project_root) / "src" / "data" / "knowledge-base" / "faqs.json"
        if not faq_path.exists():
            raise FileNotFoundError(f"FAQ file not found at {faq_path}")
            
        with open(faq_path, 'r', encoding='utf-8') as f:
            faqs = json.load(f)["faqs"]
        
        # Generate embeddings and add to vector DB
        for faq in faqs:
            # Combine question and answer for better context
            text = f"{faq['question']} {faq['answer']}"
            embedding = embedding_manager.get_embedding(text)
            
            # Add to vector DB
            vector_db_manager.add_documents(
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    'id': faq['id'],
                    'question': faq['question'],
                    'answer': faq['answer'],
                    'language': faq['language']
                }]
            )
            
        logger.info("Successfully populated vector database with FAQ embeddings")
        
    except Exception as e:
        logger.error(f"Error populating vector database: {str(e)}")
        raise

if __name__ == "__main__":
    populate_vector_db() 