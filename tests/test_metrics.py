"""Tests for metrics module."""

import pytest
from src.algorithms.metrics import (
    compression_ratio,
    word_count,
    sentence_count,
    average_sentence_length
)


class TestCompressionRatio:
    """Tests for compression ratio calculation."""
    
    def test_basic_compression(self):
        """Test basic compression ratio calculation."""
        original = "This is a long text with many words and sentences."
        summary = "This is short."
        
        ratio = compression_ratio(original, summary)
        
        assert 0 < ratio < 1
        assert isinstance(ratio, float)
    
    def test_no_compression(self):
        """Test when summary equals original."""
        text = "Same text."
        ratio = compression_ratio(text, text)
        
        assert ratio == 1.0
    
    def test_high_compression(self):
        """Test high compression scenario."""
        original = "This is a very long text. " * 10
        summary = "Short summary."
        
        ratio = compression_ratio(original, summary)
        
        assert ratio < 0.2
    
    def test_empty_original(self):
        """Test with empty original text."""
        with pytest.raises(ValueError):
            compression_ratio("", "summary")
    
    def test_empty_summary(self):
        """Test with empty summary."""
        ratio = compression_ratio("original text", "")
        assert ratio == 0.0


class TestWordCount:
    """Tests for word counting."""
    
    def test_basic_counting(self):
        """Test basic word counting."""
        text = "This is a test with five words."
        count = word_count(text)
        
        assert count == 7
    
    def test_with_punctuation(self):
        """Test word counting with punctuation."""
        text = "Hello, world! How are you?"
        count = word_count(text)
        
        assert count == 5
    
    def test_with_extra_spaces(self):
        """Test with multiple spaces."""
        text = "Word    with    extra    spaces."
        count = word_count(text)
        
        assert count == 4
    
    def test_empty_text(self):
        """Test with empty text."""
        assert word_count("") == 0
    
    def test_whitespace_only(self):
        """Test with whitespace only."""
        assert word_count("   ") == 0
    
    def test_single_word(self):
        """Test with single word."""
        assert word_count("Hello") == 1


class TestSentenceCount:
    """Tests for sentence counting."""
    
    def test_basic_counting(self):
        """Test basic sentence counting."""
        text = "First sentence. Second sentence. Third sentence."
        count = sentence_count(text)
        
        assert count == 3
    
    def test_with_question_marks(self):
        """Test with question marks."""
        text = "Is this working? Yes it is! Great."
        count = sentence_count(text)
        
        assert count == 3
    
    def test_with_exclamation(self):
        """Test with exclamation marks."""
        text = "Hello! How are you! I am fine!"
        count = sentence_count(text)
        
        assert count == 3
    
    def test_empty_text(self):
        """Test with empty text."""
        assert sentence_count("") == 0
    
    def test_no_punctuation(self):
        """Test text without sentence terminators."""
        text = "Just a fragment"
        count = sentence_count(text)
        
        assert count >= 1
    
    def test_multiple_terminators(self):
        """Test with multiple terminators."""
        text = "Really?! Yes... Maybe."
        count = sentence_count(text)
        
        assert count >= 2


class TestAverageSentenceLength:
    """Tests for average sentence length calculation."""
    
    def test_basic_calculation(self):
        """Test basic average calculation."""
        text = "Short one. This is longer sentence. Three."
        avg = average_sentence_length(text)
        
        assert avg > 0
        assert isinstance(avg, float)
    
    def test_uniform_sentences(self):
        """Test with uniform sentence lengths."""
        text = "Five words in here. Five words in here."
        avg = average_sentence_length(text)
        
        # Average should be around 4 words
        assert 3 < avg < 5
    
    def test_single_sentence(self):
        """Test with single sentence."""
        text = "This is a single sentence with seven words."
        avg = average_sentence_length(text)
        
        assert avg == word_count(text)
    
    def test_empty_text(self):
        """Test with empty text."""
        with pytest.raises(ValueError):
            average_sentence_length("")


def test_metrics_consistency(sample_text):
    """Test that metrics are consistent with each other."""
    words = word_count(sample_text)
    sentences = sentence_count(sample_text)
    avg_length = average_sentence_length(sample_text)
    
    # Average length should be roughly words / sentences
    calculated_avg = words / sentences if sentences > 0 else 0
    
    assert abs(avg_length - calculated_avg) < 2  # Allow some tolerance


def test_compression_ratio_on_real_summary(sample_text):
    """Test compression ratio with actual summarization."""
    # Simulate a summary (first two sentences)
    sentences = sample_text.split('.')[:2]
    summary = '.'.join(sentences) + '.'
    
    ratio = compression_ratio(sample_text, summary)
    
    assert 0 < ratio < 1
    assert ratio < 0.5  # Should be compressed by more than half
