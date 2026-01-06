"""
RAG pipeline orchestration module.

This module combines retrieval and summarization to implement
Retrieval-Augmented Generation for targeted summarization.
"""

from typing import List, Dict, Tuple
from .embeddings import EmbeddingModel, create_embedding_model
from .retrieval import VectorRetriever, create_retriever
from ..algorithms.extractive import ExtractiveSummarizer
from ..algorithms.statistical import StatisticalSummarizer


class RAGPipeline:
    """
    Complete RAG pipeline for query-based summarization.
    
    Combines semantic retrieval with extractive summarization to
    generate summaries focused on specific topics or queries.
    """
    
    def __init__(self, embedding_model: EmbeddingModel):
        """
        Initialize RAG pipeline.
        
        Args:
            embedding_model: Loaded embedding model
        """
        self.embedding_model = embedding_model
        self.retriever = None
        self.extractive_summarizer = ExtractiveSummarizer(algorithm="textrank")
        self.statistical_summarizer = StatisticalSummarizer(method="tfidf")
        
    def index_documents(self, documents: List[str], metadata: List[dict] = None) -> None:
        """
        Index documents for retrieval.
        
        Args:
            documents: List of documents to index
            metadata: Optional metadata for each document
        """
        self.retriever = create_retriever(self.embedding_model, documents, metadata)
    
    def query_and_summarize(self, query: str, top_k: int = 5, 
                           num_sentences: int = 3,
                           summarization_method: str = "extractive") -> Dict:
        """
        Retrieve relevant documents and generate summary.
        
        Args:
            query: Query text
            top_k: Number of documents to retrieve
            num_sentences: Number of sentences in summary
            summarization_method: 'extractive' or 'statistical'
            
        Returns:
            Dictionary with retrieved documents, scores, and summary
        """
        if self.retriever is None:
            raise ValueError("Documents not indexed. Call index_documents() first.")
        
        # Retrieve relevant documents
        results = self.retriever.retrieve(query, top_k)
        
        # Combine retrieved documents
        retrieved_texts = [doc for doc, _, _ in results]
        combined_text = " ".join(retrieved_texts)
        
        # Generate summary
        if summarization_method == "extractive":
            summary = self.extractive_summarizer.summarize(combined_text, num_sentences)
        else:
            summary = self.statistical_summarizer.summarize(combined_text, num_sentences)
        
        return {
            "query": query,
            "retrieved_documents": [
                {
                    "text": doc,
                    "similarity": score,
                    "metadata": meta
                }
                for doc, score, meta in results
            ],
            "summary": summary,
            "num_retrieved": len(results)
        }
    
    def compare_methods(self, query: str, top_k: int = 5, 
                       num_sentences: int = 3) -> Dict:
        """
        Compare different summarization methods on retrieved documents.
        
        Args:
            query: Query text
            top_k: Number of documents to retrieve
            num_sentences: Number of sentences in summaries
            
        Returns:
            Dictionary with summaries from different methods
        """
        if self.retriever is None:
            raise ValueError("Documents not indexed. Call index_documents() first.")
        
        # Retrieve documents
        results = self.retriever.retrieve(query, top_k)
        retrieved_texts = [doc for doc, _, _ in results]
        combined_text = " ".join(retrieved_texts)
        
        # Generate summaries with different methods
        extractive_summary = self.extractive_summarizer.summarize(combined_text, num_sentences)
        statistical_summary = self.statistical_summarizer.summarize(combined_text, num_sentences)
        
        return {
            "query": query,
            "retrieved_count": len(results),
            "retrieval_scores": [score for _, score, _ in results],
            "summaries": {
                "extractive": extractive_summary,
                "statistical": statistical_summary
            },
            "retrieved_documents": [
                {
                    "text": doc,
                    "similarity": score,
                    "metadata": meta
                }
                for doc, score, meta in results
            ]
        }


def create_rag_pipeline(model_name: str = "all-MiniLM-L6-v2") -> RAGPipeline:
    """
    Factory function to create a complete RAG pipeline.
    
    Args:
        model_name: Embedding model name
        
    Returns:
        Initialized RAGPipeline instance
    """
    embedding_model = create_embedding_model(model_name)
    return RAGPipeline(embedding_model)
