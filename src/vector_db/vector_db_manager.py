import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import json
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorDBManager:
    def __init__(self, collection_name: str = "green-card-faq"):
        """Initialize the vector database manager."""
        try:
            logger.info(f"Initializing VectorDBManager with collection: {collection_name}")
            self.client = chromadb.Client(Settings(
                persist_directory=str(Path(__file__).parent / "chroma_db")
            ))
            self.collection_name = collection_name
            self.collection = self._get_or_create_collection()
        except Exception as e:
            logger.error(f"Failed to initialize VectorDBManager: {str(e)}")
            raise

    def _get_or_create_collection(self):
        """Get existing collection or create a new one."""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(self.collection_name)
            logger.info(f"Retrieved existing collection: {self.collection_name}")
            return collection
        except ValueError:
            # Create new collection if it doesn't exist
            logger.info(f"Creating new collection: {self.collection_name}")
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Green Card FAQ embeddings"}
            )

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[np.ndarray]) -> None:
        """Add documents and their embeddings to the collection."""
        try:
            if not documents or not embeddings:
                raise ValueError("Documents and embeddings cannot be empty")
            if len(documents) != len(embeddings):
                raise ValueError("Number of documents must match number of embeddings")

            # Prepare data for batch insertion
            ids = [doc["id"] for doc in documents]
            texts = [doc["answer"] for doc in documents]
            metadatas = [{
                "language": doc["language"],
                "question": doc["question"]
            } for doc in documents]

            # Add documents to collection
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas,
                embeddings=[embedding.tolist() for embedding in embeddings]
            )
            logger.info(f"Successfully added {len(documents)} documents to collection")
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise

    def search_similar(self, query_embedding: np.ndarray, n_results: int = 5, 
                      language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for similar documents using an embedding."""
        try:
            # Prepare where clause for language filter
            where = {"language": language} if language else None

            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results,
                where=where
            )

            # Format results
            formatted_results = []
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "answer": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })

            logger.info(f"Found {len(formatted_results)} similar documents")
            return formatted_results
        except Exception as e:
            logger.error(f"Failed to search similar documents: {str(e)}")
            raise

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by its ID."""
        try:
            result = self.collection.get(ids=[doc_id])
            if not result["ids"]:
                return None

            return {
                "id": result["ids"][0],
                "answer": result["documents"][0],
                "metadata": result["metadatas"][0]
            }
        except Exception as e:
            logger.error(f"Failed to get document: {str(e)}")
            raise

    def delete_document(self, doc_id: str) -> None:
        """Delete a document by its ID."""
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Successfully deleted document: {doc_id}")
        except Exception as e:
            logger.error(f"Failed to delete document: {str(e)}")
            raise

    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        try:
            self.collection.delete(where={})
            logger.info("Successfully cleared collection")
        except Exception as e:
            logger.error(f"Failed to clear collection: {str(e)}")
            raise 