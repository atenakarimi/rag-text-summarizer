# System Architecture

## Overview

The RAG-Enhanced Text Summarizer is designed with a modular architecture that separates concerns and enables easy testing and extension. The system combines traditional NLP algorithms with modern embedding-based retrieval.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Simple     │  │  RAG-Enhanced │  │  Comparison  │    │
│  │Summarization │  │      Tab      │  │     Tab      │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌──────────────┐    ┌─────────────┐
│  Algorithms   │   │ RAG Pipeline │    │   Utils     │
│               │   │              │    │             │
│  Extractive:  │   │  Embeddings  │    │ Data Loading│
│  - TextRank   │   │  Retrieval   │    │ Validation  │
│  - LexRank    │   │  Orchestration│   │ Cleaning    │
│  - Luhn       │   │              │    │             │
│               │   │              │    │             │
│  Statistical: │   │              │    │             │
│  - TF-IDF     │   │              │    │             │
│  - Frequency  │   │              │    │             │
│               │   │              │    │             │
│  Metrics      │   │              │    │             │
└───────────────┘   └──────────────┘    └─────────────┘
        │                    │                    │
        └────────────────────┴────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Data Layer    │
                    │                 │
                    │ Sample Articles │
                    │    (50 docs)    │
                    └─────────────────┘
```

## Module Descriptions

### 1. Algorithms Module (`src/algorithms/`)

#### Extractive Summarization
- **TextRank**: Graph-based ranking using sentence similarity
  - Builds graph of sentences as nodes
  - Edges weighted by cosine similarity
  - Uses PageRank algorithm to score sentences
  - Extracts top-ranked sentences

- **LexRank**: Eigenvector centrality approach
  - Similar to TextRank but uses different graph construction
  - Threshold-based edge creation
  - Considers sentence similarity matrix

- **Luhn**: Keyword-based sentence scoring
  - Identifies significant words by frequency
  - Scores sentences based on keyword clusters
  - Simple but effective for keyword-rich texts

#### Statistical Summarization
- **TF-IDF**: Term frequency-inverse document frequency
  - Scores words by importance in document vs. corpus
  - Sentences scored by sum of word TF-IDF values
  - Good for identifying unique content

- **Frequency-Based**: Simple word frequency scoring
  - Counts word occurrences
  - Scores sentences by word importance
  - Fast and interpretable

#### Metrics
- Compression ratio: Summary length / Original length
- Word count: Total words in text
- Sentence count: Total sentences
- Average sentence length: Words per sentence

### 2. RAG Module (`src/rag/`)

#### Embeddings (`embeddings.py`)
```python
EmbeddingModel
├── __init__(model_name)
├── embed_text(text) → ndarray[384]
└── embed_batch(texts) → ndarray[N, 384]
```
- Uses `sentence-transformers/all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Optimized for semantic similarity

#### Retrieval (`retrieval.py`)
```python
VectorRetriever
├── build_index(texts, documents)
├── retrieve(query, top_k) → (docs, scores)
└── _compute_similarity(query_embedding, doc_embeddings)
```
- FAISS IndexFlatL2 for efficient similarity search
- L2 distance metric (lower = more similar)
- Returns ranked documents with scores

#### Pipeline (`pipeline.py`)
```python
RAGPipeline
├── index_documents(documents)
├── query_and_summarize(query, top_k, num_sentences, method)
└── compare_methods(text, num_sentences)
```
- Orchestrates RAG workflow
- Combines retrieval with summarization
- Supports multiple summarization methods

### 3. Utils Module (`src/utils/`)

#### Data Loading
- `load_sample_articles()`: Load all articles from CSV
- `load_articles_by_category()`: Filter by category
- `get_available_categories()`: List categories
- `validate_text()`: Check text validity
- `clean_text()`: Normalize whitespace
- `chunk_text()`: Split long texts

### 4. Streamlit Application (`src/app.py`)

#### UI Components
- **Tab 1: Simple Summarization**
  - Article/text selection
  - Algorithm selection (multi-select)
  - Length control
  - Side-by-side results

- **Tab 2: RAG-Enhanced**
  - Query input
  - Retrieval configuration
  - Retrieved document display
  - Focused summary generation

- **Tab 3: Comparison**
  - Extractive vs. Statistical comparison
  - Metrics visualization
  - Analysis notes

#### State Management
- Uses `st.cache_resource` for models
- Uses `st.cache_data` for data
- Session state for RAG indexing

## Data Flow

### Simple Summarization Flow
```
User Input → Text Validation → Algorithm Selection →
Summarization → Metrics Calculation → Display
```

### RAG-Enhanced Flow
```
Initialization → Index Documents (embeddings + FAISS) →
User Query → Retrieve Top-K Docs → Combine Content →
Summarize → Display Results + Metadata
```

### Comparison Flow
```
Input Text → Generate Extractive Summary →
Generate Statistical Summary → Calculate Metrics →
Display Side-by-Side with Analysis
```

## Performance Considerations

### Memory Optimization
- Lightweight models (all-MiniLM-L6-v2: 80MB vs. 500MB+ for BERT)
- Batch processing for multiple texts
- Lazy loading of models
- Cached embeddings

### Speed Optimization
- FAISS for fast vector search
- Pre-computed embeddings during indexing
- Streamlit caching for repeated operations
- Efficient sentence tokenization

### Container Size Optimization
- Python 3.11-slim base image
- Minimal system dependencies
- No-cache pip installations
- Pre-downloaded models in Docker build

## Extensibility

### Adding New Algorithms
1. Implement in `src/algorithms/extractive.py` or `statistical.py`
2. Follow interface: `summarize(text, num_sentences) → str`
3. Add tests in `tests/test_extractive.py` or `test_statistical.py`
4. Update UI to include new algorithm

### Adding New Embedding Models
1. Update `src/rag/embeddings.py` with new model
2. Adjust dimension size in retrieval module
3. Update Docker build to cache new model
4. Test with existing pipeline

### Adding New Data Sources
1. Update `src/utils/data.py` with new loader
2. Ensure consistent format (title, content, category)
3. Add validation for new data
4. Update tests

## Testing Strategy

### Unit Tests
- Individual algorithm testing
- Metrics calculation verification
- Data loading and validation
- Embedding and retrieval functionality

### Integration Tests
- Full RAG pipeline workflow
- End-to-end summarization
- Multi-document processing

### Performance Tests
- Large document handling
- Batch processing efficiency
- Memory usage monitoring

## Deployment

### Docker Deployment
```
Build → Test → Run → Health Check → Monitor
```

### Nix Deployment
```
Enter Shell → Install Deps → Download Models → Run
```

### Cloud Deployment Options
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Heroku

## Security Considerations

- Non-root user in Docker
- Read-only volume mounts
- Input validation and sanitization
- No external API calls (fully local)
- Regular dependency updates

## Monitoring and Logging

- Streamlit health check endpoint
- Docker health checks
- Application logs via stdout
- Metrics tracking in UI

## Future Enhancements

1. **Additional Algorithms**
   - BERT-based extractive summarization
   - GPT-based abstractive summarization
   - Hybrid approaches

2. **Advanced RAG Features**
   - Query expansion
   - Re-ranking algorithms
   - Multi-hop reasoning

3. **UI Improvements**
   - Export summaries to PDF/Word
   - Comparison with reference summaries
   - Visualization of sentence importance

4. **Performance**
   - GPU support for embeddings
   - Distributed processing
   - Caching layer for common queries

5. **Features**
   - Multi-language support
   - Custom training data upload
   - API endpoint for programmatic access
