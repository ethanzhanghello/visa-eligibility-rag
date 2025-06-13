import sys
from pathlib import Path
import logging

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from vector_db.vector_db_manager import VectorDBManager
from embeddings.embedding_utils import EmbeddingManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_vector_db():
    """Test the vector database functionality."""
    try:
        # Initialize managers
        logger.info("Initializing managers...")
        embedding_manager = EmbeddingManager()
        vector_db_manager = VectorDBManager()

        # Test queries in English
        english_queries = [
            "What is a Green Card?",
            "How do I apply for permanent residence?",
            "What are the eligibility categories for a Green Card?",
            "What documents do I need for the application?",
            "How long does the process take?"
        ]

        # Test queries in Mandarin
        mandarin_queries = [
            "什么是绿卡？",
            "如何申请永久居留权？",
            "绿卡的资格类别有哪些？",
            "申请需要哪些文件？",
            "处理时间需要多久？"
        ]

        # Test English queries
        logger.info("\nTesting English queries:")
        for query in english_queries:
            logger.info(f"\nQuery: {query}")
            # Generate embedding for query
            query_embedding = embedding_manager.get_embedding(query)
            
            # Search for similar documents
            results = vector_db_manager.search_similar(
                query_embedding,
                n_results=3,
                language="en"
            )
            
            # Display results
            for result in results:
                logger.info(f"ID: {result['id']}")
                logger.info(f"Question: {result['metadata']['question']}")
                logger.info(f"Answer: {result['answer']}")
                logger.info(f"Distance: {result['distance']}")
                logger.info("---")

        # Test Mandarin queries
        logger.info("\nTesting Mandarin queries:")
        for query in mandarin_queries:
            logger.info(f"\nQuery: {query}")
            # Generate embedding for query
            query_embedding = embedding_manager.get_embedding(query)
            
            # Search for similar documents
            results = vector_db_manager.search_similar(
                query_embedding,
                n_results=3,
                language="zh"
            )
            
            # Display results
            for result in results:
                logger.info(f"ID: {result['id']}")
                logger.info(f"Question: {result['metadata']['question']}")
                logger.info(f"Answer: {result['answer']}")
                logger.info(f"Distance: {result['distance']}")
                logger.info("---")

        logger.info("Successfully completed vector database tests")
        return True

    except Exception as e:
        logger.error(f"Failed to test vector database: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        test_vector_db()
    except Exception as e:
        logger.error(f"Failed to test vector database: {str(e)}")
        sys.exit(1) 