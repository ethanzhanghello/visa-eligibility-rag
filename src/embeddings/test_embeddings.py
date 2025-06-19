import pytest
from embedding_utils import EmbeddingManager
import numpy as np

@pytest.fixture(scope="module")
def embedding_manager():
    return EmbeddingManager()

def test_get_embedding_valid(embedding_manager):
    text = "What is a Green Card?"
    embedding = embedding_manager.get_embedding(text)
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[0] > 0

def test_get_embedding_empty(embedding_manager):
    with pytest.raises(ValueError):
        embedding_manager.get_embedding("")

def test_find_similar_faqs_valid(embedding_manager):
    query = "What is a Green Card?"
    results = embedding_manager.find_similar_faqs(query, top_k=2)
    assert isinstance(results, list)
    assert len(results) == 2
    for result in results:
        assert 'faq' in result and 'similarity_score' in result

def test_find_similar_faqs_empty_query(embedding_manager):
    with pytest.raises(ValueError):
        embedding_manager.find_similar_faqs("", top_k=2)

def test_find_similar_faqs_by_language_valid(embedding_manager):
    query = "什么是绿卡？"
    results = embedding_manager.find_similar_faqs_by_language(query, 'zh', top_k=2)
    assert isinstance(results, list)
    assert len(results) <= 2
    for result in results:
        assert 'faq' in result and 'similarity_score' in result

def test_find_similar_faqs_by_language_invalid_lang(embedding_manager):
    query = "What is a Green Card?"
    results = embedding_manager.find_similar_faqs_by_language(query, 'xx', top_k=2)
    assert results == []

def test_find_similar_faqs_by_language_empty_query(embedding_manager):
    with pytest.raises(ValueError):
        embedding_manager.find_similar_faqs_by_language("", 'en', top_k=2)

def test_embedding_system():
    """Test the embedding system with sample queries."""
    print("Initializing EmbeddingManager...")
    manager = EmbeddingManager()
    
    # Test queries in English
    english_queries = [
        "What is a Green Card?",
        "How do I apply for permanent residence?",
        "What are the requirements for naturalization?",
        "Can I work in the US with a Green Card?",
        "How long does the Green Card process take?"
    ]
    
    print("\nTesting English queries:")
    for query in english_queries:
        print(f"\nQuery: {query}")
        results = manager.find_similar_faqs_by_language(query, 'en', top_k=3)
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (Score: {result['similarity_score']:.4f}):")
            print(f"Question: {result['faq']['question']}")
            print(f"Answer: {result['faq']['answer']}")
    
    # Test queries in Mandarin
    mandarin_queries = [
        "什么是绿卡？",
        "如何申请永久居留权？",
        "入籍有什么要求？",
        "持有绿卡可以在美国工作吗？",
        "绿卡处理需要多长时间？"
    ]
    
    print("\nTesting Mandarin queries:")
    for query in mandarin_queries:
        print(f"\nQuery: {query}")
        results = manager.find_similar_faqs_by_language(query, 'zh', top_k=3)
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (Score: {result['similarity_score']:.4f}):")
            print(f"Question: {result['faq']['question']}")
            print(f"Answer: {result['faq']['answer']}")

if __name__ == "__main__":
    test_embedding_system() 