"""
Vector-based retrieval module using FAISS for efficient similarity search.

This module implements semantic search over document collections using
dense vector representations and FAISS indexing.
"""

from typing import List, Tuple, Optional
import numpy as np
import faiss
from .embeddings import EmbeddingModel


class VectorRetriever:
    """
    FAISS-based vector retriever for semantic search.
    
    Stores document embeddings in a FAISS index and retrieves
    the most semantically similar documents to a query.
    """
    
    def __init__(self, embedding_model: EmbeddingModel):
        """
        Initialize the retriever.
        
        Args:
            embedding_model: Loaded embedding model
        """
        self.embedding_model = embedding_model
        self.index = None
        self.documents = []
        self.metadata = []
        
    def build_index(self, documents: List[str], metadata: Optional[List[dict]] = None) -> None:
        """
        Build FAISS index from documents.
        
        Args:
            documents: List of text documents
            metadata: Optional list of metadata dicts for each document
        """
        if not documents:
            raise ValueError("Cannot build index from empty document list")
        
        print(f"Building index for {len(documents)} documents...")
        
        # Store documents and metadata
        self.documents = documents
        self.metadata = metadata if metadata else [{} for _ in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.embed_batch(documents, show_progress=True)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"Index built successfully with {self.index.ntotal} vectors")
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[str, float, dict]]:
        """
        Retrieve most similar documents to query.
        
        Args:
            query: Query text
            top_k: Number of documents to retrieve
            
        Returns:
            List of tuples (document, similarity_score, metadata)
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Generate query embedding
        query_embedding = self.embedding_model.embed_text(query)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        # Search index
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.documents)))
        
        # Prepare results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                # Convert L2 distance to similarity score (0-1, higher is better)
                similarity = 1 / (1 + dist)
                results.append((
                    self.documents[idx],
                    float(similarity),
                    self.metadata[idx]
                ))
        
        return results
    
    def get_index_stats(self) -> dict:
        """
        Get statistics about the index.
        
        Returns:
            Dictionary with index statistics
        """
        if self.index is None:
            return {"status": "not_built"}
        
        return {
            "status": "ready",
            "num_vectors": self.index.ntotal,
            "dimension": self.index.d,
            "num_documents": len(self.documents)
        }


def create_retriever(embedding_model: EmbeddingModel, documents: List[str], 
                    metadata: Optional[List[dict]] = None) -> VectorRetriever:
    """
    Factory function to create and build a vector retriever.
    
    Args:
        embedding_model: Loaded embedding model
        documents: Documents to index
        metadata: Optional metadata for documents
        
    Returns:
        Ready-to-use VectorRetriever instance
    """
    retriever = VectorRetriever(embedding_model)
    retriever.build_index(documents, metadata)
    return retriever
