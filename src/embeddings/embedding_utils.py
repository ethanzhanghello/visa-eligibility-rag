import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from sentence_transformers import SentenceTransformer
import logging
from ..utils.validation import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-base"):
        """Initialize the embedding manager with a specified model."""
        try:
            logger.info(f"Initializing EmbeddingManager with model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.embeddings = None
            self.metadata = None
            self.load_embeddings()
        except Exception as e:
            logger.error(f"Failed to initialize EmbeddingManager: {str(e)}")
            raise
    
    def load_embeddings(self) -> None:
        """Load pre-generated embeddings and metadata."""
        try:
            base_path = Path(__file__).parent / 'generated'
            
            # Load embeddings
            embeddings_path = base_path / 'embeddings.npy'
            logger.info(f"Loading embeddings from {embeddings_path}")
            if not embeddings_path.exists():
                raise FileNotFoundError(f"Embeddings file not found: {embeddings_path}")
            self.embeddings = np.load(embeddings_path)
            
            # Load metadata
            metadata_path = base_path / 'metadata.json'
            logger.info(f"Loading metadata from {metadata_path}")
            if not metadata_path.exists():
                raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            
            # Validate metadata structure
            if 'faqs' not in self.metadata:
                raise ValidationError("Missing 'faqs' key in metadata")
            if 'embedding_dimensions' not in self.metadata:
                raise ValidationError("Missing 'embedding_dimensions' key in metadata")
            
            logger.info(f"Successfully loaded {len(self.metadata['faqs'])} FAQs and their embeddings")
            
        except Exception as e:
            logger.error(f"Failed to load embeddings: {str(e)}")
            raise
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a given text."""
        try:
            if not text.strip():
                raise ValueError("Input text cannot be empty")
            
            logger.debug(f"Generating embedding for text: {text[:100]}...")
            embedding = self.model.encode(text, normalize_embeddings=True)
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise
    
    def find_similar_faqs(self, query: str, top_k: int = 5) -> List[Dict]:
        """Find similar FAQs based on a query."""
        try:
            if not query.strip():
                raise ValueError("Query cannot be empty")
            if top_k < 1:
                raise ValueError("top_k must be at least 1")
            
            logger.info(f"Finding similar FAQs for query: {query[:100]}...")
            
            # Generate embedding for the query
            query_embedding = self.get_embedding(query)
            
            # Calculate cosine similarity
            similarities = np.dot(self.embeddings, query_embedding)
            
            # Get top-k results
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # Prepare results
            results = []
            for idx in top_indices:
                results.append({
                    'faq': self.metadata['faqs'][idx],
                    'similarity_score': float(similarities[idx])
                })
            
            logger.info(f"Found {len(results)} similar FAQs")
            return results
            
        except Exception as e:
            logger.error(f"Failed to find similar FAQs: {str(e)}")
            raise
    
    def find_similar_faqs_by_language(self, query: str, language: str, top_k: int = 5) -> List[Dict]:
        """Find similar FAQs in a specific language."""
        try:
            if not query.strip():
                raise ValueError("Query cannot be empty")
            if not language.strip():
                raise ValueError("Language cannot be empty")
            if top_k < 1:
                raise ValueError("top_k must be at least 1")
            
            logger.info(f"Finding similar FAQs in {language} for query: {query[:100]}...")
            
            # Generate embedding for the query
            query_embedding = self.get_embedding(query)
            
            # Calculate cosine similarity
            similarities = np.dot(self.embeddings, query_embedding)
            
            # Filter by language and get top-k results
            language_indices = [i for i, faq in enumerate(self.metadata['faqs']) 
                              if faq['language'] == language]
            
            if not language_indices:
                logger.warning(f"No FAQs found for language: {language}")
                return []
            
            # Get similarities for the specified language
            language_similarities = similarities[language_indices]
            
            # Get top-k results
            top_k = min(top_k, len(language_indices))
            top_indices = np.argsort(language_similarities)[-top_k:][::-1]
            
            # Prepare results
            results = []
            for idx in top_indices:
                original_idx = language_indices[idx]
                results.append({
                    'faq': self.metadata['faqs'][original_idx],
                    'similarity_score': float(language_similarities[idx])
                })
            
            logger.info(f"Found {len(results)} similar FAQs in {language}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to find similar FAQs by language: {str(e)}")
            raise 