"""Tests for statistical summarization algorithms."""

import pytest
from src.algorithms.statistical import TFIDFSummarizer, FrequencySummarizer


class TestTFIDFSummarizer:
    """Tests for TF-IDF algorithm."""
    
    def test_initialization(self):
        """Test summarizer initialization."""
        summarizer = TFIDFSummarizer()
        assert summarizer is not None
    
    def test_single_summarization(self, sample_text):
        """Test summarizing a single text."""
        summarizer = TFIDFSummarizer()
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert len(summary) < len(sample_text)
    
    def test_custom_sentence_count(self, sample_text):
        """Test with different sentence counts."""
        summarizer = TFIDFSummarizer()
        
        summary_2 = summarizer.summarize(sample_text, num_sentences=2)
        summary_4 = summarizer.summarize(sample_text, num_sentences=4)
        
        # More sentences should result in longer summary
        assert len(summary_2) < len(summary_4)
    
    def test_batch_summarization(self, sample_text):
        """Test summarizing multiple texts."""
        summarizer = TFIDFSummarizer()
        texts = [sample_text, sample_text]
        
        summaries = summarizer.summarize_batch(texts, num_sentences=3)
        
        assert isinstance(summaries, list)
        assert len(summaries) == 2
        assert all(isinstance(s, str) for s in summaries)
    
    def test_empty_text(self):
        """Test with empty text."""
        summarizer = TFIDFSummarizer()
        
        with pytest.raises(ValueError):
            summarizer.summarize("", num_sentences=3)
    
    def test_sentence_preservation(self, sample_text):
        """Test that output contains complete sentences."""
        summarizer = TFIDFSummarizer()
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        # Summary should end with proper punctuation
        assert summary.strip()[-1] in ['.', '!', '?']


class TestFrequencySummarizer:
    """Tests for frequency-based algorithm."""
    
    def test_initialization(self):
        """Test summarizer initialization."""
        summarizer = FrequencySummarizer()
        assert summarizer is not None
    
    def test_single_summarization(self, sample_text):
        """Test summarizing a single text."""
        summarizer = FrequencySummarizer()
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_custom_parameters(self, sample_text):
        """Test with custom stopwords and parameters."""
        summarizer = FrequencySummarizer(stopwords=["the", "is", "and"])
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
    
    def test_batch_summarization(self, sample_text):
        """Test summarizing multiple texts."""
        summarizer = FrequencySummarizer()
        texts = [sample_text, sample_text]
        
        summaries = summarizer.summarize_batch(texts, num_sentences=3)
        
        assert len(summaries) == 2
    
    def test_different_sentence_counts(self, sample_text):
        """Test with various sentence counts."""
        summarizer = FrequencySummarizer()
        
        summary_1 = summarizer.summarize(sample_text, num_sentences=1)
        summary_3 = summarizer.summarize(sample_text, num_sentences=3)
        summary_5 = summarizer.summarize(sample_text, num_sentences=5)
        
        # Check increasing length
        assert len(summary_1) < len(summary_3) < len(summary_5)


def test_statistical_methods_comparison(sample_text):
    """Test that statistical methods produce valid summaries."""
    tfidf = TFIDFSummarizer()
    freq = FrequencySummarizer()
    
    summary_tfidf = tfidf.summarize(sample_text, num_sentences=3)
    summary_freq = freq.summarize(sample_text, num_sentences=3)
    
    # Both should produce valid strings
    assert isinstance(summary_tfidf, str) and len(summary_tfidf) > 0
    assert isinstance(summary_freq, str) and len(summary_freq) > 0
    
    # Both should be shorter than original
    assert len(summary_tfidf) < len(sample_text)
    assert len(summary_freq) < len(sample_text)


def test_tfidf_with_single_sentence():
    """Test TF-IDF with single sentence text."""
    text = "This is a single sentence text."
    summarizer = TFIDFSummarizer()
    
    summary = summarizer.summarize(text, num_sentences=1)
    assert len(summary) > 0


def test_frequency_with_repeated_words():
    """Test frequency summarizer with highly repeated words."""
    text = """
    AI is powerful. AI is transformative. AI is innovative.
    Machine learning uses AI. Deep learning uses AI.
    AI will change the world. AI is the future.
    """
    
    summarizer = FrequencySummarizer()
    summary = summarizer.summarize(text, num_sentences=3)
    
    assert isinstance(summary, str)
    assert "AI" in summary  # Most frequent word should appear
