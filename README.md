# RAG-Enhanced Text Summarizer

[![CI/CD](https://github.com/atenakarimi/rag-text-summarizer/actions/workflows/ci.yml/badge.svg)](https://github.com/atenakarimi/rag-text-summarizer/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reproducible ML project demonstrating multiple text summarization approaches: extractive algorithms (TextRank, LexRank, Luhn), statistical methods (TF-IDF, Frequency-based), and RAG-enhanced summarization with semantic search.

## 🎯 Features

- **Multiple Summarization Algorithms**
  - Extractive: TextRank, LexRank, Luhn
  - Statistical: TF-IDF, Frequency-based
  - RAG-Enhanced: Semantic search with query-focused summarization

- **Interactive Streamlit Interface**
  - Simple summarization with algorithm comparison
  - RAG-enhanced summarization with query support
  - Side-by-side method comparison

- **50 Curated Sample Articles**
  - AI/ML, Healthcare/Biotech, Quantum Computing, Cybersecurity

- **Fully Reproducible**
  - Docker containerization
  - Nix environment
  - Comprehensive test suite (30+ tests)
  - CI/CD pipeline

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/atenakarimi/rag-text-summarizer.git
cd rag-text-summarizer

# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Open http://localhost:8501 in your browser
```

### Option 2: Nix

```bash
# Enter Nix environment
nix-shell

# Run the application
make run
```

### Option 3: Local Python

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
python -m spacy download en_core_web_sm

# Run the application
streamlit run src/app.py
```

### Automated Setup Script

On Linux/Mac:
```bash
chmod +x run.sh
./run.sh
```

## 📊 Usage

### Simple Summarization
1. Select "Simple Summarization" tab
2. Choose a sample article or paste custom text
3. Select algorithms (TextRank, LexRank, Luhn, TF-IDF, Frequency)
4. Adjust summary length
5. Click "Generate Summaries"

### RAG-Enhanced Summarization
1. Select "RAG-Enhanced" tab
2. Enter a query (e.g., "What are developments in quantum computing?")
3. Adjust number of articles to retrieve
4. Choose summarization method
5. Click "Search & Summarize"

### Method Comparison
1. Select "Comparison" tab
2. Choose or paste text
3. Click "Compare Methods"
4. View extractive vs. statistical summaries side by side

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🏗️ Architecture

```
rag-text-summarizer/
├── src/
│   ├── algorithms/          # Summarization algorithms
│   │   ├── extractive.py   # TextRank, LexRank, Luhn
│   │   ├── statistical.py  # TF-IDF, Frequency-based
│   │   └── metrics.py      # Evaluation metrics
│   ├── rag/                # RAG components
│   │   ├── embeddings.py   # Sentence embeddings
│   │   ├── retrieval.py    # Vector search with FAISS
│   │   └── pipeline.py     # RAG orchestration
│   ├── utils/              # Utilities
│   │   └── data.py         # Data loading and validation
│   └── app.py              # Streamlit application
├── tests/                  # Test suite (30+ tests)
├── data/                   # Sample articles (50 articles)
├── .github/workflows/      # CI/CD pipeline
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── default.nix            # Nix environment
└── requirements.txt        # Python dependencies
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

## 📦 Technologies

- **NLP**: sentence-transformers, FAISS, sumy, nltk, spacy
- **UI**: Streamlit
- **Testing**: pytest, pytest-cov
- **Containerization**: Docker, docker-compose
- **Reproducibility**: Nix
- **CI/CD**: GitHub Actions

## 🔧 Development

```bash
# Install development dependencies
pip install -r requirements.txt pytest pytest-cov flake8 black

# Run linter
flake8 src/

# Format code
black src/

# Run tests
make test

# Build Docker image
make docker-build

# Clean artifacts
make clean
```

## 📈 Model Information

- **Embedding Model**: `all-MiniLM-L6-v2` (~80MB)
  - 384-dimensional sentence embeddings
  - Optimized for semantic search
  - Fast inference time

- **Language Model**: spaCy `en_core_web_sm`
  - English language processing
  - ~15MB size

Total container size: **~3GB** (10x smaller than typical transformer-based approaches)

## 🎓 Use Cases

- Document summarization for research papers
- News article condensation
- Meeting notes summarization
- Query-based information extraction
- Comparative analysis of summarization methods

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

Atena Karimi - atenakarimii2001@gmail.com

Project Link: [https://github.com/atenakarimi/rag-text-summarizer](https://github.com/atenakarimi/rag-text-summarizer)

## 🙏 Acknowledgments

- Built as part of the RAP4MADS course project
- Uses state-of-the-art NLP libraries and algorithms
- Inspired by modern RAG architectures

---

**Note**: This is a reproducible ML project demonstrating best practices in:
- Code organization and modularity
- Testing and quality assurance
- Containerization and environment management
- CI/CD automation
- Documentation and usability
