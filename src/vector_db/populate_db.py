import sys
from pathlib import Path
import logging
import numpy as np

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from vector_db.vector_db_manager import VectorDBManager
from embeddings.embedding_utils import EmbeddingManager
from utils.validation import load_and_validate_knowledge_base

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
        logger.info("Initializing managers...")
        embedding_manager = EmbeddingManager()
        vector_db_manager = VectorDBManager()

        # Load and validate FAQs
        logger.info("Loading FAQs...")
        faq_path = Path(__file__).parent.parent / 'data' / 'knowledge-base' / 'faqs.json'
        faqs = load_and_validate_knowledge_base(str(faq_path))

        # Generate embeddings for each FAQ
        logger.info("Generating embeddings...")
        embeddings = []
        for faq in faqs:
            # Combine question and answer for better context
            text = f"{faq['question']} {faq['answer']}"
            embedding = embedding_manager.get_embedding(text)
            embeddings.append(embedding)

        # Add documents to vector database
        logger.info("Adding documents to vector database...")
        vector_db_manager.add_documents(faqs, embeddings)

        logger.info("Successfully populated vector database")
        return True

    except Exception as e:
        logger.error(f"Failed to populate vector database: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        populate_vector_db()
    except Exception as e:
        logger.error(f"Failed to populate vector database: {str(e)}")
        sys.exit(1) 