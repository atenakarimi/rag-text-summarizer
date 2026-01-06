"""
Data loading and validation utilities.

This module provides functions for loading articles, validating text,
and preprocessing data for summarization.
"""

from typing import List, Tuple, Optional
import pandas as pd
from pathlib import Path
import re


def load_sample_articles(csv_path: Optional[str] = None) -> Tuple[List[str], List[str], List[str]]:
    """
    Load sample articles from CSV file.
    
    Args:
        csv_path: Path to CSV file. If None, uses default data/sample_articles.csv
        
    Returns:
        Tuple of (titles, contents, categories)
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV is improperly formatted
    """
    if csv_path is None:
        # Get path relative to project root
        project_root = Path(__file__).parent.parent.parent
        csv_path = project_root / "data" / "sample_articles.csv"
    else:
        csv_path = Path(csv_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")
    
    if df.empty:
        raise ValueError("CSV file is empty")
    
    required_columns = ["title", "content", "category"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"CSV must have a '{col}' column")
    
    titles = df["title"].dropna().tolist()
    contents = df["content"].dropna().tolist()
    categories = df["category"].dropna().tolist()
    
    if not titles or not contents:
        raise ValueError("No valid articles found in CSV")
    
    return titles, contents, categories


def load_articles_by_category(category: str, csv_path: Optional[str] = None) -> Tuple[List[str], List[str]]:
    """
    Load articles filtered by category.
    
    Args:
        category: Category to filter by
        csv_path: Path to CSV file
        
    Returns:
        Tuple of (titles, contents) for the specified category
    """
    titles, contents, categories = load_sample_articles(csv_path)
    
    filtered_titles = []
    filtered_contents = []
    
    for title, content, cat in zip(titles, contents, categories):
        if cat == category:
            filtered_titles.append(title)
            filtered_contents.append(content)
    
    return filtered_titles, filtered_contents


def get_available_categories(csv_path: Optional[str] = None) -> List[str]:
    """
    Get list of available article categories.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of unique categories
    """
    _, _, categories = load_sample_articles(csv_path)
    return sorted(list(set(categories)))


def validate_text(text: str) -> bool:
    """
    Validate that text is suitable for summarization.
    
    Args:
        text: Input text to validate
        
    Returns:
        True if text is valid, False otherwise
    """
    if not isinstance(text, str):
        return False
    
    text = text.strip()
    
    if not text:
        return False
    
    # Minimum 10 words for meaningful summarization
    words = text.split()
    if len(words) < 10:
        return False
    
    return True


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text string
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def chunk_text(text: str, max_chunk_size: int = 500) -> List[str]:
    """
    Split long text into smaller chunks for processing.
    
    Args:
        text: Text to chunk
        max_chunk_size: Maximum words per chunk
        
    Returns:
        List of text chunks
    """
    words = text.split()
    
    if len(words) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        
        if len(current_chunk) >= max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    
    # Add remaining words
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
