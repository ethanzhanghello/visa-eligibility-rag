"""
Retrieval manager for handling user queries and finding relevant documents.
"""
import logging
from typing import List, Dict, Any, Optional
from langdetect import detect
import numpy as np

from src.embeddings.embedding_utils import EmbeddingManager
from src.vector_db.vector_db_manager import VectorDBManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RetrievalManager:
    """Manager class for handling the retrieval pipeline."""
    
    def __init__(self):
        """Initialize the retrieval manager."""
        try:
            logger.info("Initializing RetrievalManager")
            self.embedding_manager = EmbeddingManager()
            self.vector_db_manager = VectorDBManager()
        except Exception as e:
            logger.exception(f"Failed to initialize RetrievalManager: {str(e)}")
            raise
    
    def normalize_language(self, lang: str) -> str:
        """Normalize language codes to match those in the database ('en', 'zh')."""
        lang = lang.lower()
        if lang.startswith('zh'):
            return 'zh'
        if lang.startswith('en'):
            return 'en'
        # Default to English if not recognized
        return 'en'

    def detect_language(self, text: str) -> str:
        """Detect the language of the input text.
        
        Args:
            text (str): Input text to detect language for.
            
        Returns:
            str: Two-letter language code (e.g., 'en', 'zh').
        """
        try:
            if not text.strip():
                raise ValueError("Input text cannot be empty")
            
            lang = detect(text)
            norm_lang = self.normalize_language(lang)
            logger.info(f"Detected language: {lang} (normalized: {norm_lang})")
            return norm_lang
            
        except Exception as e:
            logger.exception(f"Failed to detect language: {str(e)}")
            raise
    
    def process_query(
        self,
        query: str,
        language: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Process a user query and return relevant documents.
        
        Args:
            query (str): User query text.
            language (Optional[str]): Optional language code. If not provided, will be detected.
            top_k (int): Number of results to return.
            
        Returns:
            List[Dict[str, Any]]: List of relevant documents with metadata.
        """
        try:
            if not query.strip():
                raise ValueError("Query cannot be empty")
            
            # Detect language if not provided
            if language is None:
                language = self.detect_language(query)
            else:
                language = self.normalize_language(language)
            
            logger.info(f"Processing query in {language}: {query}")
            
            # Generate embedding for the query in the same format as stored documents
            formatted_query = f"Q: {query}\nA:"
            query_embedding = self.embedding_manager.get_embedding(formatted_query)
            
            # Search vector database
            results = self.vector_db_manager.search_similar(
                query_embedding=query_embedding,
                n_results=top_k,
                where={"language": language} if language else None
            )
            
            logger.info(f"Found {len(results)} relevant documents")
            return results
            
        except Exception as e:
            logger.exception(f"Failed to process query: {str(e)}")
            raise
    
    def get_context(self, results: List[Dict[str, Any]]) -> str:
        """Generate a context string from retrieved results.
        
        Args:
            results (List[Dict[str, Any]]): List of relevant documents with metadata.
            
        Returns:
            str: Concatenated context string.
        """
        context_parts = []
        for result in results:
            # Use metadata fields for question and answer
            question = result['metadata'].get('question', '')
            answer = result['metadata'].get('answer', '')
            context_parts.append(f"Q: {question}\nA: {answer}")
        return "\n\n".join(context_parts) 