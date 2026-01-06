"""
Evaluation metrics for text summarization quality assessment.

This module provides metrics to evaluate and compare different summarization approaches.
"""

from typing import Dict
import re
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


def calculate_compression_ratio(original: str, summary: str) -> float:
    """
    Calculate compression ratio (summary length / original length).
    
    Args:
        original: Original text
        summary: Summary text
        
    Returns:
        Compression ratio (0 to 1)
    """
    if not original or not summary:
        return 0.0
    
    original_words = len(word_tokenize(original))
    summary_words = len(word_tokenize(summary))
    
    return summary_words / original_words if original_words > 0 else 0.0


def calculate_sentence_count(text: str) -> int:
    """
    Count the number of sentences in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of sentences
    """
    if not text or not text.strip():
        return 0
    return len(sent_tokenize(text))


def calculate_word_count(text: str) -> int:
    """
    Count the number of words in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of words
    """
    if not text or not text.strip():
        return 0
    return len(word_tokenize(text))


def calculate_average_sentence_length(text: str) -> float:
    """
    Calculate average sentence length in words.
    
    Args:
        text: Input text
        
    Returns:
        Average sentence length
    """
    if not text or not text.strip():
        return 0.0
    
    sentences = sent_tokenize(text)
    if not sentences:
        return 0.0
    
    total_words = sum(len(word_tokenize(sent)) for sent in sentences)
    return total_words / len(sentences)


def calculate_metrics(original: str, summary: str) -> Dict[str, float]:
    """
    Calculate comprehensive metrics for a summary.
    
    Args:
        original: Original text
        summary: Summary text
        
    Returns:
        Dictionary with various metrics
    """
    metrics = {
        "compression_ratio": calculate_compression_ratio(original, summary),
        "original_sentences": calculate_sentence_count(original),
        "summary_sentences": calculate_sentence_count(summary),
        "original_words": calculate_word_count(original),
        "summary_words": calculate_word_count(summary),
        "original_avg_sentence_length": calculate_average_sentence_length(original),
        "summary_avg_sentence_length": calculate_average_sentence_length(summary)
    }
    
    return metrics


def format_metrics(metrics: Dict[str, float]) -> str:
    """
    Format metrics dictionary as a readable string.
    
    Args:
        metrics: Metrics dictionary
        
    Returns:
        Formatted string
    """
    lines = [
        f"Compression Ratio: {metrics['compression_ratio']:.2%}",
        f"Sentences: {metrics['original_sentences']} → {metrics['summary_sentences']}",
        f"Words: {metrics['original_words']} → {metrics['summary_words']}",
        f"Avg Sentence Length: {metrics['original_avg_sentence_length']:.1f} → {metrics['summary_avg_sentence_length']:.1f}"
    ]
    return "\n".join(lines)
