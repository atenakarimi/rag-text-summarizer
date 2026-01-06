"""
Download required models for the application.
This script ensures all models are available before starting the app.
"""

import sys
import os

def download_models():
    """Download all required NLP models."""
    print("=" * 60)
    print("Downloading required models...")
    print("=" * 60)
    
    # 1. NLTK Data
    try:
        print("\n[1/3] Downloading NLTK data...")
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✓ NLTK data downloaded successfully")
    except Exception as e:
        print(f"✗ NLTK download failed: {e}")
        return False
    
    # 2. Spacy Model
    try:
        print("\n[2/3] Downloading spaCy model...")
        import spacy
        try:
            # Try to load model
            nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model already installed")
        except OSError:
            # Download if not found
            print("Downloading en_core_web_sm (this may take a moment)...")
            os.system("python -m pip install -q https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl")
            print("✓ spaCy model downloaded successfully")
    except Exception as e:
        print(f"✗ spaCy download failed: {e}")
        print("Note: The app can still run with limited functionality")
    
    # 3. Sentence Transformers
    try:
        print("\n[3/3] Downloading sentence-transformers model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Sentence transformers model downloaded successfully")
    except Exception as e:
        print(f"✗ Sentence transformers download failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All models downloaded successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = download_models()
    sys.exit(0 if success else 1)
