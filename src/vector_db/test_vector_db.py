"""
Test script for vector database functionality.
"""
import sys
from pathlib import Path
import logging

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

def test_vector_db():
    """Test vector database functionality with sample queries."""
    try:
        # Initialize managers
        embedding_manager = EmbeddingManager()
        vector_db_manager = VectorDBManager()
        
        # Test queries in English
        english_queries = [
            "What is a Green Card?",
            "How can I apply for a Green Card?",
            "What are the requirements for a Green Card?"
        ]
        
        # Test queries in Mandarin
        mandarin_queries = [
            "什么是绿卡？",
            "如何申请绿卡？",
            "绿卡的要求是什么？"
        ]
        
        # Test English queries
        logger.info("\nTesting English queries:")
        for query in english_queries:
            logger.info(f"\nQuery: {query}")
            embedding = embedding_manager.get_embedding(query)
            results = vector_db_manager.search_similar(embedding, n_results=2)
            
            for result in results:
                logger.info(f"Document ID: {result['id']}")
                logger.info(f"Question: {result['question']}")
                logger.info(f"Answer: {result['answer']}")
                logger.info(f"Distance: {result['distance']:.4f}")
                logger.info("---")
        
        # Test Mandarin queries
        logger.info("\nTesting Mandarin queries:")
        for query in mandarin_queries:
            logger.info(f"\nQuery: {query}")
            embedding = embedding_manager.get_embedding(query)
            results = vector_db_manager.search_similar(
                embedding,
                n_results=2,
                where={"language": "mandarin"}
            )
            
            for result in results:
                logger.info(f"Document ID: {result['id']}")
                logger.info(f"Question: {result['question']}")
                logger.info(f"Answer: {result['answer']}")
                logger.info(f"Distance: {result['distance']:.4f}")
                logger.info("---")
        
        logger.info("\nVector database testing completed successfully")
        
    except Exception as e:
        logger.error(f"Error testing vector database: {str(e)}")
        raise

if __name__ == "__main__":
    test_vector_db() 