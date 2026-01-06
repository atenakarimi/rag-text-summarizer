"""
Statistical text summarization using TF-IDF and frequency-based approaches.

This module implements statistical methods for extractive summarization based on
term frequency and sentence scoring.
"""

from typing import List, Dict
import re
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)


class StatisticalSummarizer:
    """
    Statistical summarization using TF-IDF and word frequency.
    
    Scores sentences based on the importance of words they contain,
    measured using TF-IDF or word frequency statistics.
    """
    
    def __init__(self, method: str = "tfidf"):
        """
        Initialize the statistical summarizer.
        
        Args:
            method: Method to use ('tfidf' or 'frequency')
        """
        self.method = method.lower()
        self.stop_words = set(stopwords.words('english'))
        
    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove special characters and extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def _calculate_sentence_scores_tfidf(self, sentences: List[str]) -> Dict[int, float]:
        """
        Calculate sentence scores using TF-IDF.
        
        Args:
            sentences: List of sentences
            
        Returns:
            Dictionary mapping sentence index to score
        """
        if not sentences:
            return {}
        
        # Create TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words='english')
        
        try:
            tfidf_matrix = vectorizer.fit_transform(sentences)
        except ValueError:
            # Handle case where all sentences are stop words
            return {i: 0.0 for i in range(len(sentences))}
        
        # Sum TF-IDF scores for each sentence
        sentence_scores = {}
        for i in range(len(sentences)):
            sentence_scores[i] = np.sum(tfidf_matrix[i].toarray())
        
        return sentence_scores
    
    def _calculate_sentence_scores_frequency(self, text: str, sentences: List[str]) -> Dict[int, float]:
        """
        Calculate sentence scores using word frequency.
        
        Args:
            text: Full text
            sentences: List of sentences
            
        Returns:
            Dictionary mapping sentence index to score
        """
        # Tokenize and remove stop words
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        # Calculate word frequencies
        word_freq = Counter(words)
        
        # Normalize frequencies
        max_freq = max(word_freq.values()) if word_freq else 1
        word_freq = {word: freq / max_freq for word, freq in word_freq.items()}
        
        # Score each sentence
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            words = [word for word in words if word.isalnum() and word not in self.stop_words]
            
            # Sum word frequencies
            score = sum(word_freq.get(word, 0) for word in words)
            sentence_scores[i] = score
        
        return sentence_scores
    
    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """
        Generate statistical summary of the text.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences in the summary
            
        Returns:
            Summary as a string
        """
        if not text or not text.strip():
            return ""
        
        # Preprocess
        text = self._preprocess_text(text)
        
        # Split into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Calculate scores
        if self.method == "tfidf":
            sentence_scores = self._calculate_sentence_scores_tfidf(sentences)
        else:
            sentence_scores = self._calculate_sentence_scores_frequency(text, sentences)
        
        # Select top sentences
        top_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        
        # Sort by original order
        top_indices = sorted(top_indices)
        
        # Create summary
        summary = " ".join([sentences[i] for i in top_indices])
        
        return summary
    
    def summarize_batch(self, texts: List[str], num_sentences: int = 3) -> List[str]:
        """
        Summarize multiple texts.
        
        Args:
            texts: List of input texts
            num_sentences: Number of sentences per summary
            
        Returns:
            List of summaries
        """
        return [self.summarize(text, num_sentences) for text in texts]


def get_available_methods() -> List[str]:
    """
    Get list of available statistical methods.
    
    Returns:
        List of method names
    """
    return ["tfidf", "frequency"]


def create_summarizer(method: str = "tfidf") -> StatisticalSummarizer:
    """
    Factory function to create a statistical summarizer.
    
    Args:
        method: Method to use
        
    Returns:
        Configured StatisticalSummarizer instance
    """
    return StatisticalSummarizer(method=method)
