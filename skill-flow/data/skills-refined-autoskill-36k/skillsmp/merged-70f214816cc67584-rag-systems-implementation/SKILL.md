---
name: rag-systems-implementation
description: Use this skill when building Retrieval-Augmented Generation (RAG) systems, implementing semantic search, or creating knowledge bases with document chunking, embedding generation, and retrieval optimization.
---

# RAG Systems Implementation

## Overview

Retrieval-Augmented Generation (RAG) systems enhance the capabilities of language models by integrating external knowledge through effective retrieval mechanisms. This skill provides a comprehensive guide to building RAG systems, including document chunking, embedding generation, vector database integration, and retrieval strategies.

## Core Principles

1. **Quality of Retrieval**: The effectiveness of RAG systems hinges on the quality of the retrieval process. Poor retrieval leads to irrelevant or incorrect outputs.
2. **Chunking Strategies**: Proper chunking of documents is essential to maintain context and improve retrieval accuracy.
3. **Embedding Models**: Selecting the right embedding model is crucial for effective semantic search and retrieval.

## When to Use This Skill

- Building document Q&A systems
- Implementing semantic search functionalities
- Creating AI-powered knowledge bases
- Document ingestion and embedding generation
- Vector database integration
- Hybrid search (vector + keyword) implementation

## Capabilities

- Document chunking and preprocessing
- Vector embeddings and similarity search
- Retrieval pipeline design and optimization
- Semantic search implementation
- Contextual reranking of retrieved documents
- Hybrid search strategies

## Chunking Strategies

### 1. Fixed-Size Chunking

Use when documents have a consistent structure.

```python
def chunk_fixed_size(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
```

### 2. Semantic Chunking

Use when preserving meaning and context is critical.

```python
def chunk_semantic(text: str, max_chunk_size: int = 1000) -> list[str]:
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para)
        if current_size + para_size > max_chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
        current_chunk.append(para)
        current_size += para_size

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks
```

### 3. Recursive Chunking

Use for hierarchical documents with sections and subsections.

```python
def recursive_chunk(text: str, chunk_size: int = 500, separators=None) -> list[str]:
    if separators is None:
        separators = ['\n\n', '\n', '. ', ' ', '']
    separator = separators[0]
    splits = text.split(separator)
    chunks = []
    current = []
    current_len = 0

    for split in splits:
        if current_len + len(split) > chunk_size:
            if current:
                chunks.append(separator.join(current))
            current = [split]
            current_len = len(split)
        else:
            current.append(split)
            current_len += len(split) + len(separator)

    if current:
        chunks.append(separator.join(current))

    return chunks
```

## Embedding Generation

### Embedding Models

Choose an embedding model based on your requirements for speed, quality, and cost.

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| OpenAI text-embedding-3-small | 1536 | Fast | Good | $0.02/1M |
| OpenAI text-embedding-3-large | 3072 | Medium | Best | $0.13/1M |
| Cohere embed-v3 | 1024 | Fast | Good | $0.10/1M |

### Embedding Implementation

```python
from openai import OpenAI

client = OpenAI()

def embed_texts(texts, model="text-embedding-3-small"):
    embeddings = []
    batch_size = 2048
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        embeddings.extend([e.embedding for e in response.data])
    return embeddings
```

## Vector Database Integration

### Supported Databases

- **Pinecone**: Managed, suitable for production.
- **Chroma**: Open-source, good for prototyping.
- **pgvector**: PostgreSQL extension, cost-effective for existing setups.
- **Weaviate**: Open-source, supports advanced filtering.

### Example: Pinecone Integration

```python
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
index = pc.Index("your-index")

# Upsert vectors
index.upsert(vectors=[{"id": "doc1", "values": embedding_vector, "metadata": {"source": "file1"}}])

# Query
results = index.query(vector=query_embedding, top_k=10, include_metadata=True)
```

## Retrieval Strategies

### Basic Semantic Search

```python
async def semantic_search(query: str, top_k: int = 5):
    query_embedding = embed_query(query)
    results = vector_db.query(vector=query_embedding, top_k=top_k)
    return results
```

### Hybrid Search

Combine vector and keyword search for improved results.

```python
async def hybrid_search(query: str, top_k: int = 10):
    vector_results = await semantic_search(query, top_k)
    keyword_results = await keyword_search(query, top_k)
    combined_results = combine_and_rank(vector_results, keyword_results)
    return combined_results[:top_k]
```

## Reranking

### Contextual Reranking

Use a cross-encoder model to rerank retrieved documents based on relevance.

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, documents: list[str], top_k: int = 3) -> list[str]:
    pairs = [[query, doc] for doc in documents]
    scores = reranker.predict(pairs)
    ranked_indices = np.argsort(scores)[::-1][:top_k]
    return [documents[i] for i in ranked_indices]
```

## Evaluation

### Metrics

Evaluate the performance of your RAG system using metrics such as precision, recall, and mean reciprocal rank (MRR).

```python
def evaluate_retrieval(queries, ground_truth):
    metrics = {'precision@k': [], 'recall@k': [], 'mrr': []}
    for query, relevant_ids in zip(queries, ground_truth):
        retrieved = retrieve(query, k=10)
        retrieved_ids = [r.id for r in retrieved]
        relevant_retrieved = len(set(retrieved_ids) & set(relevant_ids))
        metrics['precision@k'].append(relevant_retrieved / len(retrieved_ids))
        metrics['recall@k'].append(relevant_retrieved / len(relevant_ids))
        for i, rid in enumerate(retrieved_ids):
            if rid in relevant_ids:
                metrics['mrr'].append(1 / (i + 1))
                break
        else:
            metrics['mrr'].append(0)
    return {k: sum(v)/len(v) for k, v in metrics.items()}
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Chunks too small | Lost context | Increase size, add overlap |
| Wrong embedding model | Poor retrieval | Match model to content type |
| No metadata | Can't filter | Add source, date, category |

## Conclusion

Invest in optimizing chunking, embeddings, and retrieval strategies to enhance the quality of RAG systems. Test with real queries, measure retrieval metrics, and iterate for continuous improvement.