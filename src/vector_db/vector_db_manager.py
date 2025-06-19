"""
Vector database manager for handling ChromaDB operations.
"""
import chromadb
import numpy as np
import logging
from typing import List, Dict, Any, Optional
from chromadb.config import Settings
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorDBManager:
    """Manager class for handling ChromaDB operations."""
    
    _instance = None
    _client = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VectorDBManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, collection_name: str = "green-card-faq"):
        """Initialize the vector database manager.
        
        Args:
            collection_name (str): Name of the collection to use.
        """
        if hasattr(self, 'initialized'):
            return
            
        self.collection_name = collection_name
        try:
            # Set persistent directory for ChromaDB
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            persist_dir = os.path.join(project_root, "chroma_db")
            
            # Create persistent directory if it doesn't exist
            os.makedirs(persist_dir, exist_ok=True)
            
            # Initialize persistent client if not already initialized
            if VectorDBManager._client is None:
                VectorDBManager._client = chromadb.PersistentClient(path=persist_dir)
            
            self.client = VectorDBManager._client
            logger.info(f"Initializing VectorDBManager with collection: {collection_name} (persistent at {persist_dir})")
            
            # Get or create collection
            self.collection = self._get_or_create_collection()
            self.initialized = True
            
        except Exception as e:
            logger.exception(f"Failed to initialize VectorDBManager: {str(e)}")
            raise
    
    def _get_or_create_collection(self):
        """Get an existing collection or create a new one."""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(self.collection_name)
            logger.info(f"Retrieved existing collection: {self.collection_name}")
            return collection
        except Exception:
            # Create new collection if it doesn't exist
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Green Card FAQ collection"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
            return collection
    
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[np.ndarray],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """Add documents to the collection.
        
        Args:
            documents (List[str]): List of document texts.
            embeddings (List[np.ndarray]): List of document embeddings.
            metadatas (Optional[List[Dict[str, Any]]]): List of metadata dictionaries.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not documents or not embeddings:
            logger.error("No documents or embeddings provided")
            return False
            
        if len(documents) != len(embeddings):
            logger.error("Number of documents does not match number of embeddings")
            return False
            
        try:
            # Convert numpy arrays to lists for ChromaDB
            embeddings_list = [emb.tolist() for emb in embeddings]
            
            # Generate IDs if not provided in metadata
            if metadatas is None:
                metadatas = [{"id": str(i)} for i in range(len(documents))]
            ids = [meta["id"] for meta in metadatas]
            
            # Add documents to collection
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings_list,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully added {len(documents)} documents to collection")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to add documents: {str(e)}")
            return False
    
    def search_similar(
        self,
        query_embedding: np.ndarray,
        n_results: int = 3,
        where: Optional[Dict] = None,
        similarity_threshold: float = 0.5  # Lowered from default
    ) -> List[Dict[str, Any]]:
        """Search for similar documents in the collection.
        
        Args:
            query_embedding (np.ndarray): Query embedding vector.
            n_results (int): Number of results to return.
            where (Optional[Dict]): Filter conditions.
            similarity_threshold (float): Minimum similarity score to include a result.
            
        Returns:
            List[Dict[str, Any]]: List of similar documents with metadata.
        """
        try:
            # Log collection state
            doc_count = self.collection.count()
            logger.info(f"Collection state: {doc_count} documents")
            
            if doc_count == 0:
                logger.warning("Collection is empty. No documents to search.")
                return []
            
            # Convert query embedding to list format
            query_embedding_list = query_embedding.tolist()
            
            # Perform the search
            results = self.collection.query(
                query_embeddings=[query_embedding_list],
                n_results=n_results,
                where=where
            )
            
            # Log raw results for debugging
            logger.debug(f"Raw query results: {results}")
            
            if not results or not results.get('documents') or not results['documents'][0]:
                logger.warning("No results found in query response")
                return []
            
            # Debug: Print a few examples of stored documents and their embeddings
            logger.info("Example stored documents and their embeddings:")
            if 'embeddings' in results and results['embeddings'] and results['embeddings'][0]:
                for i, (doc, emb) in enumerate(zip(results['documents'][0][:2], results['embeddings'][0][:2])):
                    logger.info(f"Document {i}: {doc}")
                    logger.info(f"Embedding {i}: {emb[:5]}...")  # Print first 5 elements
            else:
                for i, doc in enumerate(results['documents'][0][:2]):
                    logger.info(f"Document {i}: {doc}")
            
            # Filter results by similarity threshold
            filtered_results = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                similarity = 1 - distance  # Convert distance to similarity
                if similarity >= similarity_threshold:
                    filtered_results.append({
                        'document': doc,
                        'metadata': metadata,
                        'similarity': similarity
                    })
            
            logger.info(f"Found {len(filtered_results)} similar documents")
            return filtered_results
            
        except Exception as e:
            logger.exception(f"Failed to search similar documents: {str(e)}")
            return []
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID.
        
        Args:
            doc_id (str): Document ID.
            
        Returns:
            Optional[Dict[str, Any]]: Document with metadata if found, None otherwise.
        """
        try:
            result = self.collection.get(ids=[doc_id])
            if not result['ids']:
                return None
                
            return {
                'id': result['ids'][0],
                'question': result['metadatas'][0].get('question', ''),
                'answer': result['metadatas'][0].get('answer', '')
            }
            
        except Exception as e:
            logger.exception(f"Failed to get document: {str(e)}")
            return None
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID.
        
        Args:
            doc_id (str): Document ID.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Successfully deleted document: {doc_id}")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to delete document: {str(e)}")
            return False
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.collection.delete(where={})
            logger.info("Successfully cleared collection")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to clear collection: {str(e)}")
            return False 