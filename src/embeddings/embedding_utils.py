import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-base"):
        """Initialize the embedding manager with the specified model."""
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.metadata = None
        self.load_embeddings()
    
    def load_embeddings(self):
        """Load the pre-generated embeddings and metadata."""
        base_dir = Path(__file__).parent / 'generated'
        embeddings_path = base_dir / 'embeddings.npy'
        metadata_path = base_dir / 'metadata.json'
        
        if not embeddings_path.exists() or not metadata_path.exists():
            raise FileNotFoundError("Embeddings not found. Please generate them first.")
        
        self.embeddings = np.load(embeddings_path)
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a given text."""
        return self.model.encode(text, normalize_embeddings=True)
    
    def find_similar_faqs(self, query: str, top_k: int = 5) -> List[Dict]:
        """Find the most similar FAQs to the query."""
        # Generate embedding for the query
        query_embedding = self.get_embedding(query)
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding)
        
        # Get top-k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return the corresponding FAQs with their similarity scores
        results = []
        for idx in top_indices:
            faq = self.metadata['faqs'][idx]
            results.append({
                'faq': faq,
                'similarity_score': float(similarities[idx])
            })
        
        return results
    
    def find_similar_faqs_by_language(self, query: str, language: str, top_k: int = 5) -> List[Dict]:
        """Find the most similar FAQs to the query in a specific language."""
        # Generate embedding for the query
        query_embedding = self.get_embedding(query)
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding)
        
        # Filter by language and get top-k results
        language_indices = [i for i, faq in enumerate(self.metadata['faqs']) 
                          if faq['language'] == language]
        language_similarities = similarities[language_indices]
        top_indices = np.argsort(language_similarities)[-top_k:][::-1]
        
        # Return the corresponding FAQs with their similarity scores
        results = []
        for idx in top_indices:
            original_idx = language_indices[idx]
            faq = self.metadata['faqs'][original_idx]
            results.append({
                'faq': faq,
                'similarity_score': float(language_similarities[idx])
            })
        
        return results 