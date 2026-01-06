# Nix environment for reproducible builds
{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python311;
  pythonPackages = python.pkgs;
in

pkgs.mkShell {
  name = "rag-text-summarizer-env";
  
  buildInputs = with pkgs; [
    # Python and core tools
    python
    pythonPackages.pip
    pythonPackages.virtualenv
    
    # System dependencies
    gcc
    stdenv.cc.cc.lib
    zlib
    
    # Development tools
    git
    curl
    
    # For Docker (optional)
    docker
    docker-compose
  ];
  
  shellHook = ''
    echo "RAG Text Summarizer Development Environment"
    echo "Python version: $(python --version)"
    echo ""
    echo "Setting up virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
      python -m venv venv
      echo "Virtual environment created."
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
      echo "Installing Python dependencies..."
      pip install --upgrade pip
      pip install -r requirements.txt
      echo "Dependencies installed."
    fi
    
    # Download required models and data
    echo "Downloading NLP models..."
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" 2>/dev/null || true
    python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" 2>/dev/null || true
    python -m spacy download en_core_web_sm 2>/dev/null || true
    
    echo ""
    echo "Environment ready! Available commands:"
    echo "  - make run          : Run Streamlit app"
    echo "  - make test         : Run tests"
    echo "  - make docker-build : Build Docker image"
    echo "  - make docker-run   : Run Docker container"
    echo ""
  '';
  
  # Set environment variables
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
  ];
}
