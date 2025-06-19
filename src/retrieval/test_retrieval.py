"""
Test the retrieval pipeline functionality.
"""
import pytest
from src.retrieval.retrieval_manager import RetrievalManager

@pytest.fixture(scope="module")
def retrieval_manager():
    return RetrievalManager()

def test_process_query_english(retrieval_manager):
    query = "What documents do I need for EB-2 application?"
    results = retrieval_manager.process_query(query, language='en', top_k=2)
    assert isinstance(results, list)
    assert len(results) <= 2
    for result in results:
        assert 'document' in result and 'metadata' in result

def test_process_query_mandarin(retrieval_manager):
    query = "我需要哪些文件来申请 EB-2？"
    results = retrieval_manager.process_query(query, language='zh', top_k=2)
    assert isinstance(results, list)
    assert len(results) <= 2
    for result in results:
        assert 'document' in result and 'metadata' in result

def test_process_query_auto_language(retrieval_manager):
    query = "我需要哪些文件来申请 EB-2？"
    results = retrieval_manager.process_query(query, top_k=2)
    assert isinstance(results, list)
    assert len(results) <= 2
    for result in results:
        assert 'document' in result and 'metadata' in result

def test_process_query_empty(retrieval_manager):
    with pytest.raises(ValueError):
        retrieval_manager.process_query("", language='en')

def test_detect_language_empty(retrieval_manager):
    with pytest.raises(ValueError):
        retrieval_manager.detect_language("")

def test_get_context(retrieval_manager):
    # Use a real query to get results, then test context generation
    query = "What documents do I need for EB-2 application?"
    results = retrieval_manager.process_query(query, language='en', top_k=1)
    context = retrieval_manager.get_context(results)
    assert isinstance(context, str)
    assert context.startswith("Q: ")

def test_retrieval_pipeline():
    """Test the retrieval pipeline with sample queries."""
    print("Initializing RetrievalManager...")
    manager = RetrievalManager()
    
    # Test queries in English
    english_queries = [
        "What documents do I need for EB-2 application?",
        "How do I apply for permanent residence?",
        "What are the requirements for naturalization?"
    ]
    
    print("\nTesting English queries:")
    for query in english_queries:
        print(f"\nQuery: {query}")
        results = manager.process_query(query, language='en', top_k=3)
        context = manager.get_context(results)
        print("\nContext:")
        print(context)
    
    # Test queries in Mandarin
    mandarin_queries = [
        "我需要哪些文件来申请 EB-2？",
        "如何申请永久居留权？",
        "入籍有什么要求？"
    ]
    
    print("\nTesting Mandarin queries:")
    for query in mandarin_queries:
        print(f"\nQuery: {query}")
        results = manager.process_query(query, language='zh', top_k=3)
        context = manager.get_context(results)
        print("\nContext:")
        print(context)
    
    # Test automatic language detection
    print("\nTesting automatic language detection:")
    mixed_queries = [
        "What documents do I need for EB-2 application?",
        "我需要哪些文件来申请 EB-2？"
    ]
    
    for query in mixed_queries:
        print(f"\nQuery: {query}")
        results = manager.process_query(query, top_k=3)
        context = manager.get_context(results)
        print("\nContext:")
        print(context)

if __name__ == "__main__":
    test_retrieval_pipeline() 