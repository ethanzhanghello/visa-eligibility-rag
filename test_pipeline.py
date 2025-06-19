"""
Test the entire RAG pipeline.
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.embeddings.embedding_utils import EmbeddingManager
from src.vector_db.vector_db_manager import VectorDBManager
from src.retrieval.retrieval_manager import RetrievalManager
from src.llm.llm_manager import LLMManager

def test_pipeline():
    """Test the entire RAG pipeline."""
    print("Testing the RAG pipeline...")
    
    # Initialize managers
    print("\n1. Initializing managers...")
    embedding_manager = EmbeddingManager()
    vector_db_manager = VectorDBManager()
    retrieval_manager = RetrievalManager()
    llm_manager = LLMManager()
    
    # Test queries
    test_queries = [
        "What documents do I need for EB-2 application?",
        "我需要哪些文件来申请 EB-2？",
        "How do I apply for permanent residence?",
        "如何申请永久居留权？"
    ]
    
    print("\n2. Testing queries...")
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Test language detection
        lang = retrieval_manager.detect_language(query)
        print(f"Detected language: {lang}")
        
        # Test query processing
        results = retrieval_manager.process_query(query, top_k=3)
        print(f"Found {len(results)} relevant documents")
        
        # Test context generation
        context = retrieval_manager.get_context(results)
        print("\nContext:")
        print(context)
        
        # Generate LLM response
        print("\nGenerating response...")
        try:
            response = llm_manager.generate_response(context, query)
            print("\nResponse:")
            print(response["content"])
            print(f"\nTokens used: {response['usage']['total_tokens']}")
        except Exception as e:
            print(f"Failed to generate response: {str(e)}")
        
        print("-" * 80)

if __name__ == "__main__":
    test_pipeline() 