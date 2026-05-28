# RAG Pipeline Reference

Build document ingestion pipelines, create vector indices, perform semantic and hybrid search, and generate responses with source citations.

## Modes

| Mode | Purpose |
|------|---------|
| **build** | Ingest documents, create vector index |
| **query** | Semantic search with citations |
| **evaluate** | Retrieval quality metrics (MRR, recall, faithfulness) |

---

## BUILD Mode: Document Ingestion

```
Documents → Load → Parse → Chunk → Embed → Store → Verify
```

### Step 1: Load Documents

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".docx", ".md", ".txt", ".html"],
    exclude_hidden=True,
).load_data()

print(f"Loaded {len(documents)} documents")
```

### Step 2: Configure Chunking

```python
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(
    chunk_size=1024,       # Optimal for most use cases
    chunk_overlap=200,     # 20% overlap
    paragraph_separator="\n\n",
)

nodes = parser.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} chunks")
```

### Step 3: Create Vector Index

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Production: Qdrant
client = QdrantClient(path="./qdrant_data")  # Local persistent
vector_store = QdrantVectorStore(
    client=client,
    collection_name="knowledge_base",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True,
)

# Save for later
index.storage_context.persist(persist_dir="./index_storage")
```

### Step 4: Verify Index

```python
info = client.get_collection("knowledge_base")
print(f"Points indexed: {info.points_count}")
print(f"Vectors: {info.indexed_vectors_count}")
```

---

## QUERY Mode: Semantic Search with Citations

```
Query → Embed → Retrieve → Rerank → Synthesize → Cite Sources
```

### Load Index

```python
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="./index_storage")
index = load_index_from_storage(storage_context)
```

### Configure Query Engine

```python
from llama_index.core import PromptTemplate

qa_prompt = PromptTemplate(
    """You are a helpful assistant. Answer the question using ONLY the provided context.
Always cite your sources using [Source: filename, page X] format.

Context:
{context_str}

Question: {query_str}

Instructions:
1. Answer based only on the context provided
2. Cite specific sources for each claim
3. If the context doesn't contain the answer, say "I don't have information about that in the knowledge base"

Answer:"""
)

query_engine = index.as_query_engine(
    similarity_top_k=10,
    response_mode="compact",
    text_qa_template=qa_prompt,
)
```

### Execute Query with Sources

```python
response = query_engine.query("What is the main topic?")

print("Answer:", response.response)
print("\n--- Sources ---")
for i, node in enumerate(response.source_nodes, 1):
    print(f"\n[{i}] Score: {node.score:.3f}")
    print(f"Source: {node.metadata.get('file_name', 'unknown')}")
    print(f"Text: {node.text[:200]}...")
```

---

## Hybrid Search (Vector + Keyword)

```python
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# BM25 retriever for keyword matching
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=10,
)

# Vector retriever
vector_retriever = index.as_retriever(similarity_top_k=10)

# Fusion with reciprocal rank
hybrid_retriever = QueryFusionRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    retriever_weights=[0.4, 0.6],  # 40% keyword, 60% semantic
    mode="reciprocal_rerank",
)

nodes = hybrid_retriever.retrieve("search query")
```

---

## Reranking for Quality

```python
from llama_index.core.postprocessor import SentenceTransformerRerank

reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2",
    top_n=5,  # Return top 5 after reranking
)

query_engine = index.as_query_engine(
    similarity_top_k=20,  # Retrieve more
    node_postprocessors=[reranker],  # Rerank to top 5
)
```

---

## EVALUATE Mode: Quality Assessment

```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
)

faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)
relevancy_evaluator = RelevancyEvaluator(llm=llm)

response = query_engine.query("test query")

faithfulness_result = faithfulness_evaluator.evaluate_response(
    query="test query",
    response=response,
)

relevancy_result = relevancy_evaluator.evaluate_response(
    query="test query",
    response=response,
)

print(f"Faithful: {faithfulness_result.passing} ({faithfulness_result.score:.2f})")
print(f"Relevant: {relevancy_result.passing} ({relevancy_result.score:.2f})")
```

---

## Configuration Defaults

| Parameter | Default | Description |
|-----------|---------|-------------|
| vector_db | qdrant | Vector database backend |
| embedding_model | text-embedding-3-large | OpenAI embedding model |
| chunk_size | 1024 | Characters per chunk |
| chunk_overlap | 200 | Overlap between chunks |
| top_k | 10 | Number of chunks to retrieve |
| rerank | true | Use cross-encoder reranking |
| response_mode | compact | LlamaIndex response synthesis |

---

## Document Types Supported

| Format | Extension | Loader |
|--------|-----------|--------|
| PDF | .pdf | PDFReader |
| Word | .docx | DocxReader |
| Markdown | .md | MarkdownReader |
| Text | .txt | TextReader |
| HTML | .html | HTMLReader |
| JSON | .json | JSONReader |
| CSV | .csv | CSVReader |
| Web pages | URL | WebPageReader |
| Notion | - | NotionPageReader |
| GitHub | - | GithubRepositoryReader |

---

## Chunking Strategy Guide

| Document Type | Chunk Size | Overlap | Rationale |
|---------------|------------|---------|-----------|
| **Q&A docs** | 512 | 100 | Focused answers |
| **Technical manuals** | 1024 | 200 | Complete concepts |
| **Legal documents** | 768 | 150 | Complete clauses |
| **Code documentation** | 512 | 256 | Preserve context |
| **Research papers** | 1500 | 300 | Maintain arguments |

---

## Vector Database Selection

| Use Case | Recommended | Why |
|----------|-------------|-----|
| **Prototyping** | Chroma | Simple, in-memory |
| **Production self-hosted** | Qdrant | Performant, filtering |
| **Existing PostgreSQL** | pgvector | No new infrastructure |
| **Fully managed** | Pinecone | Zero ops |
| **Large scale (1B+)** | Milvus | GPU support, scale |

---

## Retrieval Strategies

### 1. Basic Semantic Search
```
Query → Embed → Vector Search → Top K
```
Best for: Simple Q&A, similar content

### 2. Hybrid Search (BM25 + Vector)
```
Query → [BM25 + Vector] → RRF Fusion → Top K
```
Best for: Mixed technical/semantic queries

### 3. Multi-Query Retrieval
```
Query → Generate Variations → Multiple Searches → Merge → Dedupe
```
Best for: Complex questions, broader coverage

### 4. Hierarchical Retrieval
```
Query → Summary Index → Section Index → Chunk Index
```
Best for: Large document sets, document navigation

### 5. Auto-Merging Retrieval
```
Query → Retrieve Chunks → If >50% children → Return Parent
```
Best for: Context-dependent answers

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| **Empty results** | Query too specific | Expand query, lower threshold |
| **Irrelevant results** | Poor chunking | Adjust chunk size/overlap |
| **Hallucinations** | Context insufficient | Add more sources, stricter prompt |
| **Slow queries** | Large index | Add filtering, reduce top_k |
| **Memory issues** | Large documents | Stream processing, batching |
| **Token limit** | Too many chunks | Reduce top_k, increase chunk size |

---

## Best Practices

### Document Preparation

1. **Clean text** - Remove headers, footers, page numbers
2. **Preserve structure** - Keep headings, lists intact
3. **Add metadata** - Source, date, category, author
4. **Deduplicate** - Remove near-duplicate content

### Index Design

1. **Separate by domain** - Different indices for different topics
2. **Metadata filtering** - Enable fast pre-filtering
3. **Regular updates** - Incremental indexing strategy
4. **Versioning** - Keep previous index versions

### Query Optimization

1. **Reranking** - Always use cross-encoder for quality
2. **Hybrid search** - Combine semantic + keyword
3. **Query expansion** - Generate query variations
4. **Caching** - Cache frequent queries

### Evaluation

1. **Regular benchmarks** - Track quality over time
2. **User feedback** - Collect relevance ratings
3. **A/B testing** - Compare configurations
4. **Error analysis** - Review failed queries

---

## Production Checklist

Before deploying RAG pipeline:

- [ ] Documents preprocessed and cleaned
- [ ] Optimal chunk size determined via testing
- [ ] Vector database deployed and configured
- [ ] Reranking enabled
- [ ] Evaluation metrics acceptable (MRR > 0.7)
- [ ] Faithfulness score > 0.9
- [ ] Response latency < 2 seconds
- [ ] Error handling implemented
- [ ] Monitoring and logging active
- [ ] Backup strategy for index

---

## Quick Start

```python
# 1. Install
# pip install llama-index llama-index-vector-stores-qdrant qdrant-client

# 2. Build index
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# 3. Query
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What is the main topic?")

print(response.response)
for node in response.source_nodes:
    print(f"Source: {node.metadata.get('file_name')}")
```
