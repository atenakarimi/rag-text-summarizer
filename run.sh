#!/bin/bash

# RAG Text Summarizer - Quick Start Script
# This script sets up and runs the application

set -e  # Exit on error

echo "=========================================="
echo " RAG Text Summarizer - Quick Start"
echo "=========================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✓ Docker detected"
    
    echo ""
    echo "Choose your option:"
    echo "1) Run with Docker (recommended)"
    echo "2) Run locally with Python"
    read -p "Enter choice [1-2]: " choice
    
    case $choice in
        1)
            echo ""
            echo "Building Docker image..."
            docker-compose build
            
            echo ""
            echo "Starting application..."
            docker-compose up -d
            
            echo ""
            echo "✓ Application is starting!"
            echo "  URL: http://localhost:8501"
            echo ""
            echo "To view logs: docker-compose logs -f"
            echo "To stop: docker-compose down"
            ;;
        2)
            run_local
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
else
    echo "✗ Docker not found. Running locally..."
    run_local
fi

function run_local() {
    echo ""
    echo "Setting up Python environment..."
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        echo "✗ Python 3 not found. Please install Python 3.9+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "✓ Python $PYTHON_VERSION detected"
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    
    # Download models
    echo "Downloading NLP models (this may take a moment)..."
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" 2>/dev/null
    python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" 2>/dev/null
    python -m spacy download en_core_web_sm --quiet 2>/dev/null
    
    echo ""
    echo "✓ Setup complete!"
    echo ""
    echo "Starting Streamlit application..."
    streamlit run src/app.py
}
