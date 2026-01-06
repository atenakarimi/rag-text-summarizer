"""
RAG-Enhanced Text Summarizer - Streamlit Application

A Streamlit app demonstrating multiple summarization approaches:
- Extractive algorithms (TextRank, LexRank, Luhn)
- Statistical methods (TF-IDF, Frequency-based)
- RAG-enhanced summarization with semantic search
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms.extractive import TextRankSummarizer, LexRankSummarizer, LuhnSummarizer
from algorithms.statistical import TFIDFSummarizer, FrequencySummarizer
from algorithms.metrics import compression_ratio, word_count, sentence_count
from rag.pipeline import RAGPipeline
from utils.data import (
    load_sample_articles,
    get_available_categories,
    load_articles_by_category,
    validate_text,
    clean_text
)


# Page configuration
st.set_page_config(
    page_title="RAG-Enhanced Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .summary-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_summarizers():
    """Load and cache all summarizers."""
    return {
        "textrank": TextRankSummarizer(),
        "lexrank": LexRankSummarizer(),
        "luhn": LuhnSummarizer(),
        "tfidf": TFIDFSummarizer(),
        "frequency": FrequencySummarizer()
    }


@st.cache_resource
def load_rag_pipeline():
    """Load and cache RAG pipeline."""
    return RAGPipeline()


@st.cache_data
def load_data():
    """Load and cache sample articles."""
    titles, contents, categories = load_sample_articles()
    return titles, contents, categories


def display_metrics(original_text: str, summary: str):
    """Display summary metrics in columns."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Compression Ratio", f"{compression_ratio(original_text, summary):.1%}")
    
    with col2:
        orig_words = word_count(original_text)
        summ_words = word_count(summary)
        st.metric("Word Count", f"{summ_words} / {orig_words}")
    
    with col3:
        orig_sents = sentence_count(original_text)
        summ_sents = sentence_count(summary)
        st.metric("Sentence Count", f"{summ_sents} / {orig_sents}")


def simple_summarization_tab():
    """Tab 1: Simple summarization with multiple algorithms."""
    st.header("📝 Simple Summarization")
    st.markdown("Compare different summarization algorithms on your text or sample articles.")
    
    # Input options
    input_option = st.radio("Choose input:", ["Sample Articles", "Custom Text"], horizontal=True)
    
    if input_option == "Sample Articles":
        titles, contents, categories = load_data()
        
        # Category filter
        category_filter = st.selectbox(
            "Filter by category:",
            ["All"] + get_available_categories()
        )
        
        if category_filter != "All":
            titles, contents = load_articles_by_category(category_filter)
        
        # Article selection
        selected_idx = st.selectbox("Select an article:", range(len(titles)), format_func=lambda i: titles[i])
        text_input = clean_text(contents[selected_idx])
        
        st.info(f"**Selected:** {titles[selected_idx]}")
        
    else:
        text_input = st.text_area("Enter text to summarize:", height=200, placeholder="Paste your text here...")
        
        if text_input:
            text_input = clean_text(text_input)
            if not validate_text(text_input):
                st.warning("⚠️ Text should have at least 10 words for meaningful summarization.")
    
    # Summarization controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        algorithms = st.multiselect(
            "Select algorithms:",
            ["TextRank", "LexRank", "Luhn", "TF-IDF", "Frequency"],
            default=["TextRank", "LexRank"]
        )
    
    with col2:
        num_sentences = st.slider("Summary length:", 2, 10, 3)
    
    if st.button("Generate Summaries", type="primary", use_container_width=True):
        if not text_input or not validate_text(text_input):
            st.error("Please provide valid text input.")
            return
        
        if not algorithms:
            st.error("Please select at least one algorithm.")
            return
        
        summarizers = load_summarizers()
        
        with st.spinner("Generating summaries..."):
            for algo_name in algorithms:
                st.markdown(f"### {algo_name}")
                
                # Map algorithm name to summarizer
                algo_key = algo_name.lower().replace("-", "")
                summarizer = summarizers.get(algo_key)
                
                if summarizer:
                    try:
                        summary = summarizer.summarize(text_input, num_sentences=num_sentences)
                        
                        # Display summary
                        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display metrics
                        display_metrics(text_input, summary)
                        
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
                
                st.divider()


def rag_enhanced_tab():
    """Tab 2: RAG-enhanced summarization with query."""
    st.header("🔍 RAG-Enhanced Summarization")
    st.markdown("Use semantic search to find relevant content and generate targeted summaries.")
    
    # Initialize RAG pipeline
    rag_pipeline = load_rag_pipeline()
    
    # Check if documents are indexed
    if not hasattr(st.session_state, 'rag_indexed') or not st.session_state.rag_indexed:
        with st.spinner("Indexing documents for semantic search..."):
            titles, contents, categories = load_data()
            
            # Create documents with metadata
            documents = []
            for title, content, category in zip(titles, contents, categories):
                documents.append({
                    "title": title,
                    "content": content,
                    "category": category
                })
            
            rag_pipeline.index_documents(documents)
            st.session_state.rag_indexed = True
            st.success("✅ Documents indexed successfully!")
    
    # Query input
    query = st.text_input(
        "Enter your query:",
        placeholder="e.g., 'What are the latest developments in quantum computing?'",
        help="The system will find relevant articles and generate a focused summary."
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        top_k = st.slider("Number of articles to retrieve:", 1, 10, 3)
    
    with col2:
        num_sentences = st.slider("Summary length:", 2, 10, 3)
    
    with col3:
        method = st.selectbox("Method:", ["Extractive", "Statistical"])
    
    if st.button("Search & Summarize", type="primary", use_container_width=True):
        if not query or len(query.strip()) < 3:
            st.error("Please enter a valid query (at least 3 characters).")
            return
        
        with st.spinner("Searching and summarizing..."):
            try:
                result = rag_pipeline.query_and_summarize(
                    query=query,
                    top_k=top_k,
                    num_sentences=num_sentences,
                    method=method.lower()
                )
                
                # Display retrieved documents
                st.subheader("📚 Retrieved Documents")
                
                for i, (doc, score) in enumerate(zip(result["retrieved_docs"], result["similarity_scores"]), 1):
                    with st.expander(f"{i}. {doc['title']} (Similarity: {score:.3f})"):
                        st.markdown(f"**Category:** {doc['category']}")
                        st.markdown("**Content Preview:**")
                        st.write(doc['content'][:300] + "...")
                
                # Display summary
                st.subheader("📝 Generated Summary")
                st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                st.write(result["summary"])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Calculate metrics for combined retrieved content
                combined_content = " ".join([doc["content"] for doc in result["retrieved_docs"]])
                display_metrics(combined_content, result["summary"])
                
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")


def comparison_tab():
    """Tab 3: Compare different summarization approaches."""
    st.header("⚖️ Method Comparison")
    st.markdown("Compare extractive vs. statistical summarization methods side by side.")
    
    # Input options
    input_option = st.radio("Choose input:", ["Sample Articles", "Custom Text"], horizontal=True, key="comp_input")
    
    if input_option == "Sample Articles":
        titles, contents, categories = load_data()
        
        selected_idx = st.selectbox("Select an article:", range(len(titles)), format_func=lambda i: titles[i], key="comp_select")
        text_input = clean_text(contents[selected_idx])
        
        st.info(f"**Selected:** {titles[selected_idx]}")
        
    else:
        text_input = st.text_area("Enter text to summarize:", height=200, placeholder="Paste your text here...", key="comp_text")
        
        if text_input:
            text_input = clean_text(text_input)
            if not validate_text(text_input):
                st.warning("⚠️ Text should have at least 10 words for meaningful summarization.")
    
    num_sentences = st.slider("Summary length:", 2, 10, 3, key="comp_slider")
    
    if st.button("Compare Methods", type="primary", use_container_width=True):
        if not text_input or not validate_text(text_input):
            st.error("Please provide valid text input.")
            return
        
        rag_pipeline = load_rag_pipeline()
        
        with st.spinner("Generating summaries..."):
            try:
                result = rag_pipeline.compare_methods(text_input, num_sentences=num_sentences)
                
                # Display side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Extractive (TextRank)")
                    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                    st.write(result["extractive"])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    display_metrics(text_input, result["extractive"])
                
                with col2:
                    st.subheader("📈 Statistical (TF-IDF)")
                    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                    st.write(result["statistical"])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    display_metrics(text_input, result["statistical"])
                
                # Analysis
                st.divider()
                st.subheader("🔬 Analysis")
                
                ext_ratio = compression_ratio(text_input, result["extractive"])
                stat_ratio = compression_ratio(text_input, result["statistical"])
                
                st.markdown(f"""
                - **Extractive** preserves original sentences, maintaining context and readability
                - **Statistical** uses sentence scoring for more flexible compression
                - Extractive compression: {ext_ratio:.1%} | Statistical compression: {stat_ratio:.1%}
                """)
                
            except Exception as e:
                st.error(f"Error generating comparison: {str(e)}")


def main():
    """Main application."""
    # Header
    st.markdown('<div class="main-header">📝 RAG-Enhanced Text Summarizer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Compare extractive, statistical, and RAG-enhanced summarization approaches</div>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=Text+Summarizer", use_container_width=True)
        
        st.markdown("### About")
        st.markdown("""
        This application demonstrates multiple text summarization approaches:
        
        **Extractive Algorithms:**
        - TextRank: Graph-based ranking
        - LexRank: Sentence similarity
        - Luhn: Keyword significance
        
        **Statistical Methods:**
        - TF-IDF: Term frequency scoring
        - Frequency: Word occurrence analysis
        
        **RAG-Enhanced:**
        - Semantic search with embeddings
        - Query-focused summarization
        - Context-aware retrieval
        """)
        
        st.markdown("### Data")
        if st.button("📊 View Dataset Info"):
            titles, contents, categories = load_data()
            st.write(f"**Total Articles:** {len(titles)}")
            st.write(f"**Categories:** {len(set(categories))}")
            
            for cat in sorted(set(categories)):
                count = categories.count(cat)
                st.write(f"- {cat}: {count} articles")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📝 Simple Summarization", "🔍 RAG-Enhanced", "⚖️ Comparison"])
    
    with tab1:
        simple_summarization_tab()
    
    with tab2:
        rag_enhanced_tab()
    
    with tab3:
        comparison_tab()
    
    # Footer
    st.divider()
    st.markdown(
        '<div style="text-align: center; color: #888; padding: 1rem;">Built with Streamlit | '
        'Reproducible ML Project</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
