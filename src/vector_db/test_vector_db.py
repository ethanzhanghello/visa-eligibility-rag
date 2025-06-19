"""
Test script for vector database functionality.
"""
import sys
from pathlib import Path
import logging
import pytest
import numpy as np
from src.embeddings.embedding_utils import EmbeddingManager
from src.vector_db.vector_db_manager import VectorDBManager

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def embedding_manager():
    return EmbeddingManager()

@pytest.fixture(scope="module")
def vector_db_manager():
    return VectorDBManager()

def test_add_documents_and_search(vector_db_manager, embedding_manager):
    text = "Test document for vector db."
    embedding = embedding_manager.get_embedding(text)
    doc_id = "test-doc-1"
    metadata = {"id": doc_id, "question": "Test Q", "answer": "Test A", "language": "en"}
    # Add document
    result = vector_db_manager.add_documents([text], [embedding], [metadata])
    assert result is True
    # Search for the document
    results = vector_db_manager.search_similar(embedding, n_results=1)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert 'document' in results[0] and 'metadata' in results[0]

def test_add_documents_mismatched_lengths(vector_db_manager):
    # Should fail if documents and embeddings lengths do not match
    result = vector_db_manager.add_documents(["doc1"], [np.zeros(10), np.zeros(10)])
    assert result is False

def test_add_documents_empty(vector_db_manager):
    # Should fail if no documents or embeddings
    result = vector_db_manager.add_documents([], [])
    assert result is False

def test_search_similar_empty_collection():
    # Create a new collection to ensure it's empty
    db = VectorDBManager(collection_name="empty-test-collection")
    embedding = np.zeros(768)
    results = db.search_similar(embedding, n_results=1)
    assert results == []

def test_search_similar_invalid_embedding(vector_db_manager):
    # Should handle invalid embedding shape gracefully
    with pytest.raises(Exception):
        vector_db_manager.search_similar(np.array([1, 2, 3]), n_results=1)

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