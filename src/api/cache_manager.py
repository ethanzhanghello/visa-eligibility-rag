import json
import hashlib
import redis
import logging
from typing import Optional, Dict, Any
from datetime import timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379", default_ttl: int = 3600):
        """
        Initialize cache manager with Redis connection.
        
        Args:
            redis_url: Redis connection URL
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self.default_ttl = default_ttl
        try:
            self.redis_client = redis.from_url(redis_url)
            # Test connection
            self.redis_client.ping()
            logger.info("Successfully connected to Redis cache")
        except redis.ConnectionError:
            logger.warning("Redis not available, falling back to in-memory cache")
            self.redis_client = None
            self._memory_cache = {}
    
    def _generate_cache_key(self, question: str, language: str = None) -> str:
        """Generate a unique cache key for a query."""
        # Normalize the question and create a hash
        normalized_question = question.strip().lower()
        cache_string = f"{normalized_question}:{language or 'auto'}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, question: str, language: str = None) -> Optional[Dict[str, Any]]:
        """Retrieve cached response for a question."""
        cache_key = self._generate_cache_key(question, language)
        
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    logger.info(f"Cache hit for question: {question[:50]}...")
                    return json.loads(cached_data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        else:
            # Fallback to in-memory cache
            if cache_key in self._memory_cache:
                logger.info(f"Memory cache hit for question: {question[:50]}...")
                return self._memory_cache[cache_key]
        
        logger.info(f"Cache miss for question: {question[:50]}...")
        return None
    
    def set(self, question: str, response: Dict[str, Any], language: str = None, ttl: int = None) -> bool:
        """Cache a response for a question."""
        cache_key = self._generate_cache_key(question, language)
        ttl = ttl or self.default_ttl
        
        try:
            if self.redis_client:
                self.redis_client.setex(cache_key, ttl, json.dumps(response))
                logger.info(f"Cached response for question: {question[:50]}...")
            else:
                # Fallback to in-memory cache
                self._memory_cache[cache_key] = response
                logger.info(f"Memory cached response for question: {question[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, question: str, language: str = None) -> bool:
        """Delete cached response for a question."""
        cache_key = self._generate_cache_key(question, language)
        
        try:
            if self.redis_client:
                self.redis_client.delete(cache_key)
            else:
                self._memory_cache.pop(cache_key, None)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all cached responses."""
        try:
            if self.redis_client:
                self.redis_client.flushdb()
            else:
                self._memory_cache.clear()
            logger.info("Cache cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False 