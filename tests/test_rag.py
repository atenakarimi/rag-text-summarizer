"""Tests for RAG pipeline components."""

import pytest
import numpy as np
from src.rag.embeddings import EmbeddingModel
from src.rag.retrieval import VectorRetriever
from src.rag.pipeline import RAGPipeline


class TestEmbeddingModel:
    """Tests for embedding model."""
    
    def test_initialization(self):
        """Test model initialization."""
        model = EmbeddingModel()
        assert model is not None
        assert model.model is not None
    
    def test_embed_single_text(self):
        """Test embedding a single text."""
        model = EmbeddingModel()
        text = "This is a test sentence."
        
        embedding = model.embed_text(text)
        
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape[0] == 384  # all-MiniLM-L6-v2 dimension
    
    def test_embed_batch(self):
        """Test embedding multiple texts."""
        model = EmbeddingModel()
        texts = ["First text.", "Second text.", "Third text."]
        
        embeddings = model.embed_batch(texts)
        
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (3, 384)
    
    def test_empty_text(self):
        """Test with empty text."""
        model = EmbeddingModel()
        
        with pytest.raises(ValueError):
            model.embed_text("")
    
    def test_embedding_consistency(self):
        """Test that same text produces same embedding."""
        model = EmbeddingModel()
        text = "Consistent text."
        
        emb1 = model.embed_text(text)
        emb2 = model.embed_text(text)
        
        # Should be very similar (allowing for minor numerical differences)
        assert np.allclose(emb1, emb2, rtol=1e-5)
    
    def test_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings."""
        model = EmbeddingModel()
        text1 = "Artificial intelligence."
        text2 = "Quantum computing."
        
        emb1 = model.embed_text(text1)
        emb2 = model.embed_text(text2)
        
        # Should be different
        assert not np.allclose(emb1, emb2, rtol=0.1)


class TestVectorRetriever:
    """Tests for vector retrieval."""
    
    def test_initialization(self):
        """Test retriever initialization."""
        retriever = VectorRetriever()
        assert retriever is not None
    
    def test_build_index(self, sample_articles):
        """Test building index from articles."""
        retriever = VectorRetriever()
        
        texts = [doc["content"] for doc in sample_articles]
        retriever.build_index(texts, sample_articles)
        
        assert retriever.index is not None
        assert len(retriever.documents) == len(sample_articles)
    
    def test_retrieve_relevant_docs(self, sample_articles):
        """Test retrieving relevant documents."""
        retriever = VectorRetriever()
        
        texts = [doc["content"] for doc in sample_articles]
        retriever.build_index(texts, sample_articles)
        
        query = "Tell me about artificial intelligence in healthcare"
        results, scores = retriever.retrieve(query, top_k=2)
        
        assert len(results) == 2
        assert len(scores) == 2
        assert all(isinstance(doc, dict) for doc in results)
        assert all(isinstance(score, (int, float)) for score in scores)
    
    def test_retrieve_ordering(self, sample_articles):
        """Test that results are ordered by relevance."""
        retriever = VectorRetriever()
        
        texts = [doc["content"] for doc in sample_articles]
        retriever.build_index(texts, sample_articles)
        
        query = "quantum computing algorithms"
        results, scores = retriever.retrieve(query, top_k=3)
        
        # Scores should be in descending order (more relevant first)
        assert scores[0] >= scores[1] >= scores[2]
    
    def test_empty_index(self):
        """Test retrieving from empty index."""
        retriever = VectorRetriever()
        
        with pytest.raises((ValueError, AttributeError)):
            retriever.retrieve("query", top_k=1)
    
    def test_top_k_parameter(self, sample_articles):
        """Test different top_k values."""
        retriever = VectorRetriever()
        
        texts = [doc["content"] for doc in sample_articles]
        retriever.build_index(texts, sample_articles)
        
        query = "technology"
        
        results_1, _ = retriever.retrieve(query, top_k=1)
        results_2, _ = retriever.retrieve(query, top_k=2)
        
        assert len(results_1) == 1
        assert len(results_2) == 2


class TestRAGPipeline:
    """Tests for RAG pipeline."""
    
    def test_initialization(self):
        """Test pipeline initialization."""
        pipeline = RAGPipeline()
        assert pipeline is not None
    
    def test_index_documents(self, sample_articles):
        """Test indexing documents."""
        pipeline = RAGPipeline()
        pipeline.index_documents(sample_articles)
        
        assert len(pipeline.documents) == len(sample_articles)
    
    def test_query_and_summarize(self, sample_articles):
        """Test full query and summarization."""
        pipeline = RAGPipeline()
        pipeline.index_documents(sample_articles)
        
        result = pipeline.query_and_summarize(
            query="artificial intelligence healthcare",
            top_k=2,
            num_sentences=2,
            method="extractive"
        )
        
        assert "retrieved_docs" in result
        assert "similarity_scores" in result
        assert "summary" in result
        
        assert len(result["retrieved_docs"]) == 2
        assert len(result["similarity_scores"]) == 2
        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0
    
    def test_query_with_statistical_method(self, sample_articles):
        """Test query with statistical summarization."""
        pipeline = RAGPipeline()
        pipeline.index_documents(sample_articles)
        
        result = pipeline.query_and_summarize(
            query="quantum",
            top_k=1,
            num_sentences=2,
            method="statistical"
        )
        
        assert isinstance(result["summary"], str)
    
    def test_compare_methods(self, sample_text):
        """Test method comparison."""
        pipeline = RAGPipeline()
        
        result = pipeline.compare_methods(sample_text, num_sentences=3)
        
        assert "extractive" in result
        assert "statistical" in result
        
        assert isinstance(result["extractive"], str)
        assert isinstance(result["statistical"], str)
        assert len(result["extractive"]) > 0
        assert len(result["statistical"]) > 0
    
    def test_invalid_method(self, sample_articles):
        """Test with invalid summarization method."""
        pipeline = RAGPipeline()
        pipeline.index_documents(sample_articles)
        
        with pytest.raises(ValueError):
            pipeline.query_and_summarize(
                query="test",
                top_k=1,
                num_sentences=2,
                method="invalid_method"
            )
    
    def test_empty_query(self, sample_articles):
        """Test with empty query."""
        pipeline = RAGPipeline()
        pipeline.index_documents(sample_articles)
        
        with pytest.raises(ValueError):
            pipeline.query_and_summarize(
                query="",
                top_k=1,
                num_sentences=2
            )


def test_full_rag_workflow(sample_articles):
    """Integration test for full RAG workflow."""
    # Initialize pipeline
    pipeline = RAGPipeline()
    
    # Index documents
    pipeline.index_documents(sample_articles)
    
    # Query and summarize
    result = pipeline.query_and_summarize(
        query="What are the latest developments in AI?",
        top_k=2,
        num_sentences=3,
        method="extractive"
    )
    
    # Verify all components worked
    assert len(result["retrieved_docs"]) > 0
    assert len(result["summary"]) > 0
    assert all(score > 0 for score in result["similarity_scores"])
    
    # Verify retrieved docs are relevant
    ai_mentioned = any("AI" in doc["content"] or "intelligence" in doc["content"].lower() 
                       for doc in result["retrieved_docs"])
    assert ai_mentioned
