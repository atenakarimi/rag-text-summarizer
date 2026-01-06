.PHONY: help install test run docker-build docker-run docker-stop clean

help:
	@echo "RAG Text Summarizer - Available Commands"
	@echo "========================================"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make run           - Run Streamlit app"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make docker-stop   - Stop Docker container"
	@echo "  make clean         - Clean build artifacts"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
	python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
	python -m spacy download en_core_web_sm

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

run:
	streamlit run src/app.py

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d
	@echo "Application running at http://localhost:8501"

docker-stop:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "Cleaned build artifacts"
