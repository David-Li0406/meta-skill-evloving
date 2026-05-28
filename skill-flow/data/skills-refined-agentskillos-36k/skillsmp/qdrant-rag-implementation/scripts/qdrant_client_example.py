"""
Qdrant Client Configuration and Usage Example
This script demonstrates proper Qdrant client setup with error handling and async compatibility.
"""

import os
import logging
from typing import List, Dict, Any
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    doc_path: str
    embedding: List[float]
    metadata: Dict[str, Any] = {}

class VectorStore:
    def __init__(self, 
                 collection_name: str = "default_collection", 
                 timeout: int = 30, 
                 grpc_port: int = 6334, 
                 prefer_grpc: bool = True):
        """
        Initialize the vector store with Qdrant client.

        Args:
            collection_name: Name of the Qdrant collection to use
            timeout: Timeout for Qdrant API requests in seconds
            grpc_port: gRPC port for Qdrant communication
            prefer_grpc: Whether to prefer gRPC communication (faster than HTTP)
        """
        try:
            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")

            if not qdrant_url or not qdrant_api_key:
                raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment variables")

            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                timeout=timeout,
                grpc_port=grpc_port,
                prefer_grpc=prefer_grpc
            )
            self.collection_name = collection_name
            self.timeout = timeout

            # Create or verify the collection exists
            self._ensure_collection_exists()
        except Exception as e:
            logging.error(f"Failed to initialize Qdrant client: {e}")
            raise

    def check_connection(self):
        """
        Check if the Qdrant connection is working.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to get collections to verify connection
            # Note: get_collections doesn't accept timeout parameter, but uses the client's global timeout
            collections = self.client.get_collections()
            logging.info("Qdrant connection test succeeded")
            return True
        except Exception as e:
            logging.error(f"Qdrant connection test failed: {e}")
            return False

    def _ensure_collection_exists(self):
        """
        Ensure the Qdrant collection exists with proper configuration.
        """
        try:
            # Check if collection exists
            # Note: get_collections doesn't accept timeout parameter, but uses the client's global timeout
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            collection_exists = self.collection_name in collection_names
            
            if not collection_exists:
                # Create collection with 384-dimensional vectors and cosine similarity
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
                    timeout=self.timeout
                )
                logging.info(f"Created Qdrant collection '{self.collection_name}' with 384-dim vectors and cosine similarity")
            else:
                # Verify collection configuration matches expected settings
                # Note: get_collection doesn't accept timeout parameter, but uses the client's global timeout
                collection_info = self.client.get_collection(
                    collection_name=self.collection_name
                )
                
                expected_size = 384
                expected_distance = Distance.COSINE
                
                # Check if vector configuration matches expectations
                if hasattr(collection_info.config.params, 'vectors'):
                    vec_params = collection_info.config.params.vectors
                    if hasattr(vec_params, 'size') and vec_params.size != expected_size:
                        logging.warning(f"Collection '{self.collection_name}' has unexpected vector size: {vec_params.size}, expected: {expected_size}")
                    if hasattr(vec_params, 'distance') and vec_params.distance != expected_distance:
                        logging.warning(f"Collection '{self.collection_name}' has unexpected distance metric: {vec_params.distance}, expected: {expected_distance}")
                
                logging.info(f"Qdrant collection '{self.collection_name}' already exists with proper configuration")
        except Exception as e:
            logging.error(f"Failed to create or verify Qdrant collection: {e}")
            raise

    def validate_embedding_dimensions(self, embedding: List[float]) -> bool:
        """Validate that the embedding has the correct dimensions for this collection."""
        expected_size = 384  # As configured in the collection
        if len(embedding) != expected_size:
            raise ValueError(f"Embedding dimension mismatch: got {len(embedding)}, expected {expected_size}")
        return True

    def store_document_chunk(self, chunk: DocumentChunk) -> bool:
        """
        Store a document chunk in the vector database.

        Args:
            chunk: DocumentChunk object containing content and embedding

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate embedding dimensions
            self.validate_embedding_dimensions(chunk.embedding)
            
            # Ensure chunk_id is a proper integer or UUID
            # Convert string IDs to integer if possible, otherwise generate an integer ID
            try:
                point_id = int(chunk.chunk_id) if chunk.chunk_id.isdigit() else hash(chunk.chunk_id) % (10**9)
            except (ValueError, AttributeError):
                # Fallback to hash of content
                import hashlib
                point_id = int(hashlib.md5(chunk.content.encode()).hexdigest(), 16) % (10**9)
            
            # Prepare the point for Qdrant
            points = [
                models.PointStruct(
                    id=point_id,
                    vector=chunk.embedding,
                    payload={
                        "content": chunk.content,
                        "doc_path": chunk.doc_path,
                        "metadata": chunk.metadata
                    }
                )
            ]

            # Upload the point to Qdrant
            # Note: upsert doesn't accept timeout parameter, but uses the client's global timeout
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            return True
        except Exception as e:
            logging.error(f"Failed to store document chunk: {e}")
            return False

    def store_document_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """
        Store multiple document chunks in the vector database using batch operations.

        Args:
            chunks: List of DocumentChunk objects to store

        Returns:
            True if successful, False otherwise
        """
        try:
            if not chunks:
                logging.warning("No chunks to store")
                return True
            
            # Validate all embeddings have correct dimensions
            for chunk in chunks:
                self.validate_embedding_dimensions(chunk.embedding)
            
            # Prepare the points for Qdrant
            points = []
            for chunk in chunks:
                # Ensure chunk_id is a proper integer or UUID
                try:
                    point_id = int(chunk.chunk_id) if chunk.chunk_id.isdigit() else hash(chunk.chunk_id) % (10**9)
                except (ValueError, AttributeError):
                    # Fallback to hash of content
                    import hashlib
                    point_id = int(hashlib.md5(chunk.content.encode()).hexdigest(), 16) % (10**9)
                
                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=chunk.embedding,
                        payload={
                            "content": chunk.content,
                            "doc_path": chunk.doc_path,
                            "metadata": chunk.metadata
                        }
                    )
                )

            # Upload the points to Qdrant in batches for better performance
            batch_size = 64  # Recommended batch size for performance
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                # Note: upsert doesn't accept timeout parameter, but uses the client's global timeout
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
            
            logging.info(f"Successfully stored {len(chunks)} document chunks in batch")
            return True
        except Exception as e:
            logging.error(f"Failed to store document chunks: {e}")
            return False

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar document chunks based on the query embedding.

        Args:
            query_embedding: 384-dimensional embedding vector to search for
            limit: Maximum number of results to return

        Returns:
            List of documents with similarity scores
        """
        try:
            # Validate embedding dimensions
            self.validate_embedding_dimensions(query_embedding)
            
            # Perform the search in Qdrant with timeout
            # Use query_points method which is the new universal method for searching
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit,
                timeout=self.timeout
            )

            # Format the results
            results = []
            for result in search_results.points:
                results.append({
                    "content": result.payload["content"],
                    "doc_path": result.payload["doc_path"],
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score
                })

            return results
        except Exception as e:
            logging.error(f"Failed to search in vector store: {e}")
            return []

    def delete_collection(self) -> bool:
        """
        Delete the entire collection (useful for re-indexing).

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name, timeout=self.timeout)
            logging.info(f"Deleted Qdrant collection '{self.collection_name}'")
            return True
        except Exception as e:
            logging.error(f"Failed to delete collection: {e}")
            return False

    def count_documents(self) -> int:
        """
        Count the total number of documents in the collection.

        Returns:
            Total number of documents in the collection
        """
        try:
            # Note: get_collection doesn't accept timeout parameter, but uses the client's global timeout
            collection_info = self.client.get_collection(
                collection_name=self.collection_name
            )
            return collection_info.points_count
        except Exception as e:
            logging.error(f"Failed to count documents in collection: {e}")
            return 0

    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the Qdrant instance.

        Returns:
            Health status information
        """
        try:
            # Use info() method which provides version and other information about the instance
            # Note: info() doesn't accept timeout parameter, but uses the client's global timeout
            info = self.client.info()
            return {
                "status": "healthy",
                "version": getattr(info, 'version', 'unknown'),
                "commit": getattr(info, 'commit', 'unknown')
            }
        except Exception as e:
            logging.error(f"Qdrant health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

# Example usage
if __name__ == "__main__":
    # Example usage - requires environment variables to be set
    # os.environ["QDRANT_URL"] = "your_qdrant_url"
    # os.environ["QDRANT_API_KEY"] = "your_api_key"
    
    try:
        # Initialize vector store
        vector_store = VectorStore(collection_name="test_collection", timeout=30)
        
        # Test connection
        if vector_store.check_connection():
            print("Qdrant connection successful!")
            
            # Test health check
            health = vector_store.health_check()
            print(f"Health check: {health}")
            
            # Test document storage
            test_chunk = DocumentChunk(
                chunk_id="1",
                content="This is a test document for Qdrant integration.",
                doc_path="test/path.txt",
                embedding=[0.1] * 384  # 384-dimensional vector
            )
            
            if vector_store.store_document_chunk(test_chunk):
                print("Document stored successfully!")
                
                # Test search
                results = vector_store.search([0.1] * 384, limit=5)
                print(f"Search returned {len(results)} results")
                
                # Test document count
                count = vector_store.count_documents()
                print(f"Total documents in collection: {count}")
            
            # Clean up
            vector_store.delete_collection()
            print("Test collection cleaned up")
        else:
            print("Failed to connect to Qdrant")
    except Exception as e:
        print(f"Error in example: {e}")