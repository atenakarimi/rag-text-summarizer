"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return """
    Artificial intelligence is revolutionizing many industries. Machine learning algorithms
    can now process vast amounts of data. Deep learning models achieve remarkable accuracy.
    Natural language processing enables computers to understand human language. Computer vision
    systems can recognize objects and faces. AI is transforming healthcare, finance, and transportation.
    The future of AI holds great promise and challenges.
    """


@pytest.fixture
def sample_text_short():
    """Short text that might cause issues."""
    return "This is a very short text with only a few words here."


@pytest.fixture
def sample_text_invalid():
    """Invalid text samples."""
    return {
        "empty": "",
        "whitespace": "   ",
        "too_short": "Only five words here",
        "non_string": 12345
    }


@pytest.fixture
def sample_articles():
    """Sample articles for testing."""
    return [
        {
            "title": "AI in Healthcare",
            "content": "Artificial intelligence is transforming healthcare. Machine learning helps diagnose diseases. Deep learning analyzes medical images. AI improves patient outcomes.",
            "category": "AI/ML"
        },
        {
            "title": "Quantum Computing",
            "content": "Quantum computers use quantum mechanics. They can solve complex problems. Quantum algorithms are revolutionary. The technology is still developing.",
            "category": "Quantum Computing"
        },
        {
            "title": "Cybersecurity Trends",
            "content": "Cybersecurity threats are evolving. Organizations need robust defenses. AI helps detect anomalies. Zero-trust architecture is becoming standard.",
            "category": "Cybersecurity"
        }
    ]


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent
