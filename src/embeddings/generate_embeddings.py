import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import logging
from typing import List, Dict, Any
import sys

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from utils.validation import load_and_validate_knowledge_base, ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_embeddings() -> None:
    """Generate embeddings for all FAQs in the knowledge base."""
    try:
        # Load and validate FAQs
        faq_path = Path(__file__).parent.parent / 'data' / 'knowledge-base' / 'faqs.json'
        logger.info(f"Loading FAQs from {faq_path}")
        faqs = load_and_validate_knowledge_base(str(faq_path))
        
        # Load the model
        logger.info("Loading multilingual E5 model...")
        try:
            model = SentenceTransformer("intfloat/multilingual-e5-base")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
        
        # Prepare texts for embedding
        logger.info("Preparing texts for embedding...")
        texts = []
        for faq in faqs:
            text = f"{faq['question']} {faq['answer']}"
            texts.append(text)
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(texts)} texts...")
        try:
            embeddings = model.encode(texts, normalize_embeddings=True)
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise
        
        # Create output directory
        output_dir = Path(__file__).parent / 'generated'
        output_dir.mkdir(exist_ok=True)
        
        # Save embeddings
        embeddings_path = output_dir / 'embeddings.npy'
        logger.info(f"Saving embeddings to {embeddings_path}")
        try:
            np.save(embeddings_path, embeddings)
        except Exception as e:
            logger.error(f"Failed to save embeddings: {str(e)}")
            raise
        
        # Save metadata
        metadata_path = output_dir / 'metadata.json'
        logger.info(f"Saving metadata to {metadata_path}")
        metadata = {
            'faqs': faqs,
            'embedding_dimensions': embeddings.shape[1]
        }
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metadata: {str(e)}")
            raise
        
        logger.info("Successfully completed embedding generation")
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        generate_embeddings()
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {str(e)}")
        sys.exit(1) 