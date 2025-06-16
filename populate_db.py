"""
Script to populate the vector database with FAQ data.
"""
import json
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.embeddings.embedding_utils import EmbeddingManager
from src.vector_db.vector_db_manager import VectorDBManager

def populate_database():
    """Populate the vector database with FAQ data."""
    print("Loading FAQ data...")
    
    # Load FAQ data
    faq_path = Path(__file__).parent / "src" / "data" / "knowledge-base" / "faqs.json"
    with open(faq_path, 'r', encoding='utf-8') as f:
        faq_data = json.load(f)
    
    # Initialize managers
    print("Initializing managers...")
    embedding_manager = EmbeddingManager()
    vector_db_manager = VectorDBManager()
    
    # Process FAQs
    print("Processing FAQs...")
    documents = []
    embeddings = []
    metadatas = []
    
    for faq in faq_data['faqs']:
        # Concatenate question and answer for embedding and storage
        qa_text = f"Q: {faq['question']}\nA: {faq['answer']}"
        embedding = embedding_manager.get_embedding(qa_text)
        unique_id = f"{faq['id']}_{faq['language']}"
        documents.append(qa_text)
        embeddings.append(embedding)
        metadatas.append({
            'id': unique_id,
            'base_id': faq['id'],
            'language': faq['language'],
            'question': faq['question'],
            'answer': faq['answer']
        })
    
    # Add to vector database
    print(f"Adding {len(documents)} documents to vector database...")
    success = vector_db_manager.add_documents(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    if success:
        print("Successfully populated vector database!")
    else:
        print("Failed to populate vector database.")

if __name__ == "__main__":
    populate_database() 