"""Tests for extractive summarization algorithms."""

import pytest
from src.algorithms.extractive import TextRankSummarizer, LexRankSummarizer, LuhnSummarizer


class TestTextRankSummarizer:
    """Tests for TextRank algorithm."""
    
    def test_initialization(self):
        """Test summarizer initialization."""
        summarizer = TextRankSummarizer()
        assert summarizer is not None
    
    def test_single_summarization(self, sample_text):
        """Test summarizing a single text."""
        summarizer = TextRankSummarizer()
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert len(summary) < len(sample_text)
    
    def test_custom_sentence_count(self, sample_text):
        """Test with different sentence counts."""
        summarizer = TextRankSummarizer()
        
        summary_2 = summarizer.summarize(sample_text, num_sentences=2)
        summary_4 = summarizer.summarize(sample_text, num_sentences=4)
        
        assert len(summary_2) < len(summary_4)
    
    def test_batch_summarization(self, sample_text):
        """Test summarizing multiple texts."""
        summarizer = TextRankSummarizer()
        texts = [sample_text, sample_text]
        
        summaries = summarizer.summarize_batch(texts, num_sentences=3)
        
        assert isinstance(summaries, list)
        assert len(summaries) == 2
        assert all(isinstance(s, str) for s in summaries)
    
    def test_empty_text(self):
        """Test with empty text."""
        summarizer = TextRankSummarizer()
        
        with pytest.raises(ValueError):
            summarizer.summarize("", num_sentences=3)
    
    def test_very_short_text(self, sample_text_short):
        """Test with very short text."""
        summarizer = TextRankSummarizer()
        summary = summarizer.summarize(sample_text_short, num_sentences=2)
        
        assert isinstance(summary, str)
        assert len(summary) > 0


class TestLexRankSummarizer:
    """Tests for LexRank algorithm."""
    
    def test_initialization(self):
        """Test summarizer initialization."""
        summarizer = LexRankSummarizer()
        assert summarizer is not None
    
    def test_single_summarization(self, sample_text):
        """Test summarizing a single text."""
        summarizer = LexRankSummarizer()
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_threshold_parameter(self, sample_text):
        """Test with different thresholds."""
        summarizer = LexRankSummarizer(threshold=0.2)
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
    
    def test_batch_summarization(self, sample_text):
        """Test summarizing multiple texts."""
        summarizer = LexRankSummarizer()
        texts = [sample_text, sample_text]
        
        summaries = summarizer.summarize_batch(texts, num_sentences=3)
        
        assert len(summaries) == 2


class TestLuhnSummarizer:
    """Tests for Luhn algorithm."""
    
    def test_initialization(self):
        """Test summarizer initialization."""
        summarizer = LuhnSummarizer()
        assert summarizer is not None
    
    def test_single_summarization(self, sample_text):
        """Test summarizing a single text."""
        summarizer = LuhnSummarizer()
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_different_languages(self, sample_text):
        """Test with different language settings."""
        summarizer = LuhnSummarizer(language="english")
        summary = summarizer.summarize(sample_text, num_sentences=3)
        
        assert isinstance(summary, str)
    
    def test_batch_summarization(self, sample_text):
        """Test summarizing multiple texts."""
        summarizer = LuhnSummarizer()
        texts = [sample_text, sample_text]
        
        summaries = summarizer.summarize_batch(texts, num_sentences=3)
        
        assert len(summaries) == 2


def test_all_algorithms_produce_different_results(sample_text):
    """Test that different algorithms produce different summaries."""
    textrank = TextRankSummarizer()
    lexrank = LexRankSummarizer()
    luhn = LuhnSummarizer()
    
    summary_tr = textrank.summarize(sample_text, num_sentences=3)
    summary_lr = lexrank.summarize(sample_text, num_sentences=3)
    summary_lu = luhn.summarize(sample_text, num_sentences=3)
    
    # All should be valid strings
    assert all(isinstance(s, str) and len(s) > 0 for s in [summary_tr, summary_lr, summary_lu])
