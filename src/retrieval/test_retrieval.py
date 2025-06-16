"""
Test the retrieval pipeline functionality.
"""
from retrieval_manager import RetrievalManager

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