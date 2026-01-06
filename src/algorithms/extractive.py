"""
Extractive text summarization using TextRank and other graph-based algorithms.

This module implements extractive summarization techniques that select the most
important sentences from the original text without modification.
"""

from typing import List, Optional
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class ExtractiveSummarizer:
    """
    Extractive summarization using graph-based algorithms.
    
    Supports multiple algorithms:
    - TextRank: Based on PageRank, identifies important sentences
    - LexRank: Graph-based approach using sentence similarity
    - Luhn: Statistical approach based on significant word frequency
    """
    
    def __init__(self, algorithm: str = "textrank"):
        """
        Initialize the extractive summarizer.
        
        Args:
            algorithm: Algorithm to use ('textrank', 'lexrank', or 'luhn')
        """
        self.algorithm = algorithm.lower()
        self.summarizer = self._get_summarizer()
        
    def _get_summarizer(self):
        """Get the appropriate summarizer based on algorithm choice."""
        if self.algorithm == "textrank":
            return TextRankSummarizer()
        elif self.algorithm == "lexrank":
            return LexRankSummarizer()
        elif self.algorithm == "luhn":
            return LuhnSummarizer()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
    
    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """
        Generate extractive summary of the text.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences in the summary
            
        Returns:
            Summary as a string
        """
        if not text or not text.strip():
            return ""
        
        # Parse the text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        # Generate summary
        summary_sentences = self.summarizer(parser.document, num_sentences)
        
        # Combine sentences into text
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        
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


def get_available_algorithms() -> List[str]:
    """
    Get list of available extractive summarization algorithms.
    
    Returns:
        List of algorithm names
    """
    return ["textrank", "lexrank", "luhn"]


def create_summarizer(algorithm: str = "textrank") -> ExtractiveSummarizer:
    """
    Factory function to create an extractive summarizer.
    
    Args:
        algorithm: Algorithm to use
        
    Returns:
        Configured ExtractiveSummarizer instance
    """
    return ExtractiveSummarizer(algorithm=algorithm)
