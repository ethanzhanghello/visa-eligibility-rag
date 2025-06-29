"""
Configuration management for the Green Card RAG Helper.
"""
import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DatabaseConfig:
    """Database configuration."""
    collection_name: str = "green-card-faq"
    persist_dir: str = "chroma_db"
    similarity_threshold: float = 0.5
    max_results: int = 3

@dataclass
class LLMConfig:
    """LLM configuration."""
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    api_key: Optional[str] = None

@dataclass
class ConfidenceConfig:
    """Confidence scoring configuration."""
    threshold: float = 0.7
    context_weight: float = 0.4
    source_weight: float = 0.3
    length_weight: float = 0.2
    terms_weight: float = 0.1

@dataclass
class APIConfig:
    """API configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    workers: int = 1
    rate_limit_window: int = 60
    rate_limit_max_requests: int = 100

@dataclass
class CacheConfig:
    """Cache configuration."""
    enabled: bool = True
    ttl: int = 3600  # 1 hour
    max_size: int = 1000
    redis_url: Optional[str] = None

@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None

@dataclass
class SecurityConfig:
    """Security configuration."""
    cors_origins: list = None
    trusted_hosts: list = None
    api_key_header: Optional[str] = None
    enable_rate_limiting: bool = True

class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.llm = LLMConfig()
        self.confidence = ConfidenceConfig()
        self.api = APIConfig()
        self.cache = CacheConfig()
        self.logging = LoggingConfig()
        self.security = SecurityConfig()
        
        self._load_from_environment()
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        
        # Database
        self.database.collection_name = os.getenv("DB_COLLECTION_NAME", self.database.collection_name)
        self.database.persist_dir = os.getenv("DB_PERSIST_DIR", self.database.persist_dir)
        self.database.similarity_threshold = float(os.getenv("DB_SIMILARITY_THRESHOLD", self.database.similarity_threshold))
        self.database.max_results = int(os.getenv("DB_MAX_RESULTS", self.database.max_results))
        
        # LLM
        self.llm.model_name = os.getenv("LLM_MODEL_NAME", self.llm.model_name)
        self.llm.temperature = float(os.getenv("LLM_TEMPERATURE", self.llm.temperature))
        self.llm.max_tokens = int(os.getenv("LLM_MAX_TOKENS", self.llm.max_tokens))
        self.llm.api_key = os.getenv("OPENAI_API_KEY")
        
        # Confidence
        self.confidence.threshold = float(os.getenv("CONFIDENCE_THRESHOLD", self.confidence.threshold))
        self.confidence.context_weight = float(os.getenv("CONFIDENCE_CONTEXT_WEIGHT", self.confidence.context_weight))
        self.confidence.source_weight = float(os.getenv("CONFIDENCE_SOURCE_WEIGHT", self.confidence.source_weight))
        self.confidence.length_weight = float(os.getenv("CONFIDENCE_LENGTH_WEIGHT", self.confidence.length_weight))
        self.confidence.terms_weight = float(os.getenv("CONFIDENCE_TERMS_WEIGHT", self.confidence.terms_weight))
        
        # API
        self.api.host = os.getenv("API_HOST", self.api.host)
        self.api.port = int(os.getenv("API_PORT", self.api.port))
        self.api.reload = os.getenv("API_RELOAD", "true").lower() == "true"
        self.api.workers = int(os.getenv("API_WORKERS", self.api.workers))
        self.api.rate_limit_window = int(os.getenv("API_RATE_LIMIT_WINDOW", self.api.rate_limit_window))
        self.api.rate_limit_max_requests = int(os.getenv("API_RATE_LIMIT_MAX_REQUESTS", self.api.rate_limit_max_requests))
        
        # Cache
        self.cache.enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.cache.ttl = int(os.getenv("CACHE_TTL", self.cache.ttl))
        self.cache.max_size = int(os.getenv("CACHE_MAX_SIZE", self.cache.max_size))
        self.cache.redis_url = os.getenv("REDIS_URL")
        
        # Logging
        self.logging.level = os.getenv("LOG_LEVEL", self.logging.level)
        self.logging.format = os.getenv("LOG_FORMAT", self.logging.format)
        self.logging.file = os.getenv("LOG_FILE")
        
        # Security
        cors_origins = os.getenv("CORS_ORIGINS")
        if cors_origins:
            self.security.cors_origins = [origin.strip() for origin in cors_origins.split(",")]
        
        trusted_hosts = os.getenv("TRUSTED_HOSTS")
        if trusted_hosts:
            self.security.trusted_hosts = [host.strip() for host in trusted_hosts.split(",")]
        
        self.security.api_key_header = os.getenv("API_KEY_HEADER")
        self.security.enable_rate_limiting = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    
    def validate(self) -> list:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate required settings
        if not self.llm.api_key:
            errors.append("OPENAI_API_KEY environment variable is required")
        
        # Validate numeric ranges
        if not (0.0 <= self.confidence.threshold <= 1.0):
            errors.append("CONFIDENCE_THRESHOLD must be between 0.0 and 1.0")
        
        if not (0.0 <= self.llm.temperature <= 2.0):
            errors.append("LLM_TEMPERATURE must be between 0.0 and 2.0")
        
        if self.llm.max_tokens <= 0:
            errors.append("LLM_MAX_TOKENS must be positive")
        
        if self.api.port <= 0 or self.api.port > 65535:
            errors.append("API_PORT must be between 1 and 65535")
        
        # Validate file paths
        if self.logging.file:
            log_path = Path(self.logging.file)
            if not log_path.parent.exists():
                errors.append(f"Log file directory does not exist: {log_path.parent}")
        
        return errors
    
    def get_database_path(self) -> str:
        """Get the full path to the database directory."""
        project_root = Path(__file__).parent.parent
        return str(project_root / self.database.persist_dir)
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            "database": {
                "collection_name": self.database.collection_name,
                "persist_dir": self.database.persist_dir,
                "similarity_threshold": self.database.similarity_threshold,
                "max_results": self.database.max_results
            },
            "llm": {
                "model_name": self.llm.model_name,
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens,
                "api_key_set": bool(self.llm.api_key)
            },
            "confidence": {
                "threshold": self.confidence.threshold,
                "context_weight": self.confidence.context_weight,
                "source_weight": self.confidence.source_weight,
                "length_weight": self.confidence.length_weight,
                "terms_weight": self.confidence.terms_weight
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "reload": self.api.reload,
                "workers": self.api.workers,
                "rate_limit_window": self.api.rate_limit_window,
                "rate_limit_max_requests": self.api.rate_limit_max_requests
            },
            "cache": {
                "enabled": self.cache.enabled,
                "ttl": self.cache.ttl,
                "max_size": self.cache.max_size,
                "redis_url_set": bool(self.cache.redis_url)
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
                "file": self.logging.file
            },
            "security": {
                "cors_origins": self.security.cors_origins,
                "trusted_hosts": self.security.trusted_hosts,
                "api_key_header_set": bool(self.security.api_key_header),
                "enable_rate_limiting": self.security.enable_rate_limiting
            }
        }

# Global configuration instance
config = Config() 