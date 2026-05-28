# Vector Databases & Embeddings

Semantic search and similarity-based context retrieval for intelligent memory systems.

## Vector Database Options

| Database  | Strengths                          | Best For                    |
| --------- | ---------------------------------- | --------------------------- |
| Pinecone  | Fully managed, fast, scalable      | Production RAG, enterprise  |
| Weaviate  | Open source, hybrid search, GraphQL| Flexible deployments        |
| Qdrant    | Open source, Rust performance      | High-performance local      |
| Chroma    | Lightweight, embedded              | Prototyping, small projects |
| pgvector  | PostgreSQL extension               | Existing Postgres stacks    |

## Embedding Strategies

### Model Selection

| Model                    | Dimensions | Use Case              |
| ------------------------ | ---------- | --------------------- |
| OpenAI text-embedding-3  | 1536/3072  | General purpose       |
| Cohere embed-v3          | 1024       | Multilingual          |
| Voyage-2                 | 1024       | Code and technical    |
| BGE-large-en             | 1024       | Open source option    |
| E5-large-v2              | 1024       | Retrieval-optimized   |

### Multi-Modal Embeddings

```python
class MultiModalEmbedder:
    def embed(self, content, content_type):
        if content_type == "text":
            return self.text_model.encode(content)
        elif content_type == "code":
            return self.code_model.encode(content)
        elif content_type == "image":
            return self.vision_model.encode(content)
```

## Vector Store Implementation

```python
class MetadataVectorStore:
    def __init__(self, embedding_model, vector_db):
        self.embedder = embedding_model
        self.db = vector_db

    def add(self, text, metadata):
        embedding = self.embedder.encode(text)
        doc = {
            "text": text,
            "embedding": embedding,
            "entities": metadata.get("entities", []),
            "timestamp": metadata.get("timestamp"),
            "source": metadata.get("source")
        }
        self.db.upsert(doc)
        self.index_by_entity(doc)

    def search(self, query, top_k=5, filter=None):
        query_embedding = self.embedder.encode(query)
        return self.db.search(
            query_embedding,
            top_k=top_k,
            filter=filter
        )

    def search_by_entity(self, entity, top_k=5):
        return self.entity_index.get(entity, [])[:top_k]
```

## Hybrid Search

Combine vector similarity with keyword matching for best results.

```python
def hybrid_search(query, alpha=0.7):
    """
    alpha: weight for semantic search (1-alpha for keyword)
    """
    semantic_results = vector_search(query)
    keyword_results = keyword_search(query)

    combined = {}
    for doc, score in semantic_results:
        combined[doc.id] = alpha * score

    for doc, score in keyword_results:
        combined[doc.id] = combined.get(doc.id, 0) + (1-alpha) * score

    return sorted(combined.items(), key=lambda x: x[1], reverse=True)
```

## Chunking Strategies

| Strategy        | Chunk Size  | Overlap | Use Case               |
| --------------- | ----------- | ------- | ---------------------- |
| Fixed           | 512 tokens  | 50      | General documents      |
| Semantic        | Variable    | None    | Structured content     |
| Sentence-based  | 3-5 sent    | 1 sent  | Prose, articles        |
| Code-aware      | Function    | Context | Source code            |
| Hierarchical    | Multi-level | Varies  | Long documents         |

```python
def semantic_chunking(document):
    """Chunk at semantic boundaries."""
    chunks = []
    for section in document.sections:
        if section.token_count < MAX_CHUNK_SIZE:
            chunks.append(section)
        else:
            chunks.extend(split_section(section))
    return chunks
```

## Index Optimization

```python
# Build index with appropriate parameters
index_config = {
    "metric": "cosine",  # or "euclidean", "dot_product"
    "pods": 1,
    "replicas": 1,
    "shards": 1,
    "pod_type": "p1.x1"  # Adjust for scale
}

# For large datasets
index_config["metadata_config"] = {
    "indexed": ["source", "timestamp", "category"]
}
```

## Performance Targets

| Metric              | Target          | Notes                   |
| ------------------- | --------------- | ----------------------- |
| Query latency       | <100ms          | P95                     |
| Recall@10           | >0.9            | Relevant docs retrieved |
| Index build time    | <1hr/1M docs    | Initial indexing        |
| Incremental update  | <1s             | Single doc update       |

## Guidelines

1. Choose embedding model based on content type
2. Use hybrid search for best recall
3. Chunk at semantic boundaries when possible
4. Include rich metadata for filtering
5. Monitor index size and query latency
6. Implement incremental updates for real-time
7. Use approximate nearest neighbor for scale

## Related

- [Memory Systems](./memory-systems.md)
- [Context Optimization](./context-optimization.md)
