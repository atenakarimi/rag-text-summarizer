"""
Document embedding module for RAG pipeline.

This module handles converting text documents into vector embeddings
for semantic search and retrieval.
"""

from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    """
    Wrapper for sentence embedding model.
    
    Uses sentence-transformers to create dense vector representations
    of text for semantic similarity and retrieval.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: HuggingFace model name (default: all-MiniLM-L6-v2, ~80MB)
        """
        self.model_name = model_name
        self.model = None
        
    def load_model(self) -> None:
        """Load the embedding model."""
        print(f"Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        print("Embedding model loaded successfully")
        
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_batch(self, texts: List[str], show_progress: bool = False) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            show_progress: Whether to show progress bar
            
        Returns:
            2D numpy array of embeddings (num_texts x embedding_dim)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=show_progress
        )
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Embedding dimension
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        return self.model.get_sentence_embedding_dimension()


def create_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingModel:
    """
    Factory function to create and load an embedding model.
    
    Args:
        model_name: Model name
        
    Returns:
        Loaded EmbeddingModel instance
    """
    model = EmbeddingModel(model_name=model_name)
    model.load_model()
    return model
