"""
Test the caching functionality.
"""
import pytest
from unittest.mock import Mock, patch
from src.api.cache_manager import CacheManager

@pytest.fixture
def cache_manager():
    """Create a cache manager with mocked Redis."""
    with patch('redis.from_url') as mock_redis:
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_redis.return_value = mock_client
        return CacheManager()

@pytest.fixture
def memory_cache_manager():
    """Create a cache manager that falls back to in-memory cache."""
    with patch('redis.from_url') as mock_redis:
        mock_redis.side_effect = Exception("Redis not available")
        return CacheManager()

def test_cache_key_generation(cache_manager):
    """Test cache key generation."""
    key1 = cache_manager._generate_cache_key("What is EB-2?", "en")
    key2 = cache_manager._generate_cache_key("what is eb-2?", "en")
    key3 = cache_manager._generate_cache_key("What is EB-2?", "zh")
    
    # Same question and language should generate same key
    assert key1 == key2
    # Different language should generate different key
    assert key1 != key3

def test_cache_set_and_get(cache_manager):
    """Test setting and getting from cache."""
    question = "What documents do I need for EB-2?"
    response = {"content": "Test answer", "model": "gpt-3.5-turbo", "usage": {"total_tokens": 100}}
    
    # Test set
    success = cache_manager.set(question, response, "en")
    assert success is True
    
    # Test get
    cached_response = cache_manager.get(question, "en")
    assert cached_response == response

def test_cache_miss(cache_manager):
    """Test cache miss scenario."""
    question = "What documents do I need for EB-2?"
    cached_response = cache_manager.get(question, "en")
    assert cached_response is None

def test_memory_cache_fallback(memory_cache_manager):
    """Test in-memory cache fallback when Redis is not available."""
    question = "What documents do I need for EB-2?"
    response = {"content": "Test answer", "model": "gpt-3.5-turbo", "usage": {"total_tokens": 100}}
    
    # Test set
    success = memory_cache_manager.set(question, response, "en")
    assert success is True
    
    # Test get
    cached_response = memory_cache_manager.get(question, "en")
    assert cached_response == response

def test_cache_delete(cache_manager):
    """Test cache deletion."""
    question = "What documents do I need for EB-2?"
    response = {"content": "Test answer", "model": "gpt-3.5-turbo", "usage": {"total_tokens": 100}}
    
    # Set cache
    cache_manager.set(question, response, "en")
    
    # Verify it's cached
    assert cache_manager.get(question, "en") == response
    
    # Delete cache
    success = cache_manager.delete(question, "en")
    assert success is True
    
    # Verify it's deleted
    assert cache_manager.get(question, "en") is None

def test_cache_clear_all(cache_manager):
    """Test clearing all cache."""
    question1 = "What documents do I need for EB-2?"
    question2 = "How do I apply for permanent residence?"
    response = {"content": "Test answer", "model": "gpt-3.5-turbo", "usage": {"total_tokens": 100}}
    
    # Set multiple cache entries
    cache_manager.set(question1, response, "en")
    cache_manager.set(question2, response, "en")
    
    # Clear all cache
    success = cache_manager.clear_all()
    assert success is True
    
    # Verify all cache is cleared
    assert cache_manager.get(question1, "en") is None
    assert cache_manager.get(question2, "en") is None 