"""Tests for data utilities."""

import pytest
from pathlib import Path
from src.utils.data import (
    load_sample_articles,
    load_articles_by_category,
    get_available_categories,
    validate_text,
    clean_text,
    chunk_text
)


class TestLoadSampleArticles:
    """Tests for loading sample articles."""
    
    def test_load_default_path(self, project_root):
        """Test loading from default path."""
        titles, contents, categories = load_sample_articles()
        
        assert isinstance(titles, list)
        assert isinstance(contents, list)
        assert isinstance(categories, list)
        
        assert len(titles) > 0
        assert len(contents) > 0
        assert len(categories) > 0
        
        # All lists should have same length
        assert len(titles) == len(contents) == len(categories)
    
    def test_all_fields_valid(self):
        """Test that all loaded fields are valid."""
        titles, contents, categories = load_sample_articles()
        
        # All titles should be non-empty strings
        assert all(isinstance(t, str) and len(t) > 0 for t in titles)
        
        # All contents should be non-empty strings
        assert all(isinstance(c, str) and len(c) > 0 for c in contents)
        
        # All categories should be non-empty strings
        assert all(isinstance(cat, str) and len(cat) > 0 for cat in categories)
    
    def test_nonexistent_path(self):
        """Test with non-existent CSV path."""
        with pytest.raises(FileNotFoundError):
            load_sample_articles("nonexistent_file.csv")


class TestLoadArticlesByCategory:
    """Tests for loading articles by category."""
    
    def test_filter_by_category(self):
        """Test filtering by a specific category."""
        # First get available categories
        categories = get_available_categories()
        
        if len(categories) > 0:
            first_category = categories[0]
            titles, contents = load_articles_by_category(first_category)
            
            assert len(titles) > 0
            assert len(contents) > 0
            assert len(titles) == len(contents)
    
    def test_nonexistent_category(self):
        """Test with non-existent category."""
        titles, contents = load_articles_by_category("NonexistentCategory123")
        
        # Should return empty lists
        assert len(titles) == 0
        assert len(contents) == 0


class TestGetAvailableCategories:
    """Tests for getting available categories."""
    
    def test_get_categories(self):
        """Test getting list of categories."""
        categories = get_available_categories()
        
        assert isinstance(categories, list)
        assert len(categories) > 0
        
        # Should be unique
        assert len(categories) == len(set(categories))
        
        # Should be sorted
        assert categories == sorted(categories)
    
    def test_categories_match_data(self):
        """Test that categories match actual data."""
        categories = get_available_categories()
        _, _, all_categories = load_sample_articles()
        
        unique_data_categories = set(all_categories)
        
        assert set(categories) == unique_data_categories


class TestValidateText:
    """Tests for text validation."""
    
    def test_valid_text(self, sample_text):
        """Test with valid text."""
        assert validate_text(sample_text) is True
    
    def test_empty_string(self):
        """Test with empty string."""
        assert validate_text("") is False
    
    def test_whitespace_only(self):
        """Test with whitespace only."""
        assert validate_text("   ") is False
    
    def test_too_short(self):
        """Test with text that's too short."""
        assert validate_text("Only five words here okay") is False
    
    def test_minimum_length(self):
        """Test text with exactly minimum words."""
        text = "One two three four five six seven eight nine ten"
        assert validate_text(text) is True
    
    def test_non_string(self, sample_text_invalid):
        """Test with non-string input."""
        assert validate_text(sample_text_invalid["non_string"]) is False


class TestCleanText:
    """Tests for text cleaning."""
    
    def test_remove_extra_whitespace(self):
        """Test removing extra whitespace."""
        text = "This   has    extra    spaces"
        cleaned = clean_text(text)
        
        assert "  " not in cleaned
        assert cleaned == "This has extra spaces"
    
    def test_strip_leading_trailing(self):
        """Test stripping leading and trailing whitespace."""
        text = "   Text with spaces   "
        cleaned = clean_text(text)
        
        assert cleaned == "Text with spaces"
    
    def test_newlines_and_tabs(self):
        """Test with newlines and tabs."""
        text = "Text\nwith\nnewlines\tand\ttabs"
        cleaned = clean_text(text)
        
        assert "\n" not in cleaned
        assert "\t" not in cleaned
        assert cleaned == "Text with newlines and tabs"
    
    def test_already_clean(self):
        """Test with already clean text."""
        text = "This is clean text."
        cleaned = clean_text(text)
        
        assert cleaned == text
    
    def test_empty_string(self):
        """Test with empty string."""
        cleaned = clean_text("")
        assert cleaned == ""


class TestChunkText:
    """Tests for text chunking."""
    
    def test_short_text_no_chunking(self):
        """Test that short text isn't chunked."""
        text = "Short text with only a few words here"
        chunks = chunk_text(text, max_chunk_size=100)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_long_text_chunking(self):
        """Test that long text is chunked."""
        # Create text with 1000 words
        text = " ".join(["word"] * 1000)
        chunks = chunk_text(text, max_chunk_size=100)
        
        assert len(chunks) > 1
        
        # Each chunk should be <= max_chunk_size words
        for chunk in chunks[:-1]:  # Except possibly the last
            words = chunk.split()
            assert len(words) <= 100
    
    def test_chunk_size_parameter(self):
        """Test different chunk sizes."""
        text = " ".join(["word"] * 500)
        
        chunks_100 = chunk_text(text, max_chunk_size=100)
        chunks_200 = chunk_text(text, max_chunk_size=200)
        
        # Smaller chunk size should create more chunks
        assert len(chunks_100) > len(chunks_200)
    
    def test_all_words_preserved(self):
        """Test that all words are preserved in chunks."""
        text = " ".join([f"word{i}" for i in range(250)])
        chunks = chunk_text(text, max_chunk_size=100)
        
        # Reconstruct text from chunks
        reconstructed = " ".join(chunks)
        
        assert reconstructed == text
    
    def test_empty_text(self):
        """Test with empty text."""
        chunks = chunk_text("", max_chunk_size=100)
        
        assert len(chunks) == 1
        assert chunks[0] == ""


def test_full_data_pipeline():
    """Integration test for full data loading and processing pipeline."""
    # Load articles
    titles, contents, categories = load_sample_articles()
    
    assert len(titles) > 0
    
    # Get first article
    first_content = contents[0]
    
    # Validate
    assert validate_text(first_content)
    
    # Clean
    cleaned = clean_text(first_content)
    assert len(cleaned) > 0
    
    # Chunk if needed
    chunks = chunk_text(cleaned, max_chunk_size=100)
    assert len(chunks) > 0
    
    # Each chunk should be valid
    for chunk in chunks:
        assert isinstance(chunk, str)
        assert len(chunk) > 0


def test_category_filtering_accuracy():
    """Test that category filtering is accurate."""
    categories = get_available_categories()
    
    for category in categories:
        titles, contents = load_articles_by_category(category)
        
        # Verify by loading all and manually filtering
        all_titles, all_contents, all_cats = load_sample_articles()
        
        expected_count = all_cats.count(category)
        assert len(titles) == expected_count
