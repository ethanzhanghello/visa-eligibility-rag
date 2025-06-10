import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os

def load_faqs():
    """Load FAQs from the knowledge base."""
    faq_path = Path(__file__).parent.parent / 'data' / 'knowledge-base' / 'faqs.json'
    with open(faq_path, 'r', encoding='utf-8') as f:
        return json.load(f)['faqs']

def generate_embeddings():
    """Generate embeddings for all FAQs using the multilingual E5 model."""
    # Load the model
    print("Loading the multilingual E5 model...")
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    
    # Load FAQs
    print("Loading FAQs...")
    faqs = load_faqs()
    
    # Prepare texts for embedding
    texts = []
    for faq in faqs:
        # Combine question and answer for better context
        text = f"{faq['question']} {faq['answer']}"
        texts.append(text)
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(texts, normalize_embeddings=True)
    
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent / 'generated'
    output_dir.mkdir(exist_ok=True)
    
    # Save embeddings
    print("Saving embeddings...")
    np.save(output_dir / 'embeddings.npy', embeddings)
    
    # Save metadata (mapping between embeddings and FAQs)
    metadata = {
        'faqs': faqs,
        'embedding_dimensions': embeddings.shape[1]
    }
    with open(output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(embeddings)} embeddings with {embeddings.shape[1]} dimensions each")
    print(f"Saved embeddings to {output_dir / 'embeddings.npy'}")
    print(f"Saved metadata to {output_dir / 'metadata.json'}")

if __name__ == "__main__":
    generate_embeddings() 