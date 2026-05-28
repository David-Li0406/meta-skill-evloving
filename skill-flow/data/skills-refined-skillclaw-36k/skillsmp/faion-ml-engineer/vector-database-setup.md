---
id: vector-database-setup
name: "Vector Database Setup"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Vector Database Setup

## Overview

Vector databases are specialized systems for storing, indexing, and querying high-dimensional vectors (embeddings). They enable fast similarity search at scale, forming the retrieval layer of RAG systems and recommendation engines.

## When to Use

- Building RAG (Retrieval Augmented Generation) systems
- Semantic search over documents
- Recommendation systems
- Image/audio similarity search
- Duplicate detection
- Clustering and classification

## Key Concepts

### Vector Database Comparison

| Database | Type | Best For | Scaling | Cost |
|----------|------|----------|---------|------|
| Pinecone | Managed | Production, serverless | Auto | Pay-per-use |
| Weaviate | Open/Managed | Hybrid search, GraphQL | K8s | Free/Paid |
| Chroma | Open | Prototyping, local dev | Limited | Free |
| Qdrant | Open/Managed | Performance, filtering | Docker/K8s | Free/Paid |
| Milvus | Open | Enterprise scale | K8s | Free |
| pgvector | Extension | PostgreSQL integration | PostgreSQL | Free |

### Index Types

| Index | Speed | Accuracy | Memory | Use Case |
|-------|-------|----------|--------|----------|
| Flat | Slow | 100% | High | Small datasets (<10K) |
| IVF | Fast | 95-99% | Medium | Medium datasets |
| HNSW | Fastest | 95-99% | High | Production, real-time |
| PQ | Fastest | 90-95% | Low | Huge datasets, cost-sensitive |

## Implementation

### Pinecone Setup

```python
from pinecone import Pinecone, ServerlessSpec
import os

# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# Create index
def create_pinecone_index(index_name: str, dimension: int = 1536):
    """Create a serverless Pinecone index."""
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    return pc.Index(index_name)

# Usage
index = create_pinecone_index("my-index")

# Upsert vectors
def upsert_documents(index, documents: list[dict]):
    """
    Upsert documents with embeddings.
    documents: [{"id": "1", "embedding": [...], "metadata": {...}}]
    """
    vectors = [
        {
            "id": doc["id"],
            "values": doc["embedding"],
            "metadata": doc.get("metadata", {})
        }
        for doc in documents
    ]

    # Batch upsert (max 100 per request)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)

# Query
def query_similar(index, query_embedding: list, top_k: int = 5, filter: dict = None):
    """Query for similar vectors."""
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter
    )
    return results.matches
```

### Chroma Setup (Local Development)

```python
import chromadb
from chromadb.config import Settings

# Persistent local storage
client = chromadb.PersistentClient(path="./chroma_db")

# Or ephemeral (in-memory)
# client = chromadb.Client()

# Create collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # or "l2", "ip"
)

def add_documents(collection, documents: list[dict]):
    """
    Add documents to Chroma.
    documents: [{"id": "1", "text": "...", "embedding": [...], "metadata": {...}}]
    """
    collection.add(
        ids=[d["id"] for d in documents],
        embeddings=[d["embedding"] for d in documents],
        documents=[d.get("text", "") for d in documents],
        metadatas=[d.get("metadata", {}) for d in documents]
    )

def query_documents(collection, query_embedding: list, n_results: int = 5):
    """Query similar documents."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results

# With automatic embedding
from chromadb.utils import embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

auto_collection = client.get_or_create_collection(
    name="auto_embed",
    embedding_function=openai_ef
)

# Now you can add just text
auto_collection.add(
    ids=["1", "2"],
    documents=["First document", "Second document"]
)

# Query with text
results = auto_collection.query(
    query_texts=["search query"],
    n_results=5
)
```

### Qdrant Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Local Qdrant
client = QdrantClient(path="./qdrant_db")

# Or remote
# client = QdrantClient(url="http://localhost:6333")

# Cloud Qdrant
# client = QdrantClient(
#     url="https://xxx.qdrant.io",
#     api_key="your-api-key"
# )

def create_collection(client, collection_name: str, vector_size: int = 1536):
    """Create Qdrant collection."""
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE
        )
    )

def upsert_points(client, collection_name: str, documents: list[dict]):
    """
    Upsert documents to Qdrant.
    documents: [{"id": 1, "embedding": [...], "payload": {...}}]
    """
    points = [
        models.PointStruct(
            id=doc["id"],
            vector=doc["embedding"],
            payload=doc.get("payload", {})
        )
        for doc in documents
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )

def search_points(
    client,
    collection_name: str,
    query_vector: list,
    limit: int = 5,
    filter: dict = None
):
    """Search for similar points."""
    search_filter = None
    if filter:
        search_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
                for key, value in filter.items()
            ]
        )

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
        query_filter=search_filter
    )
    return results
```

### Weaviate Setup

```python
import weaviate
from weaviate.classes.init import Auth

# Local Weaviate
client = weaviate.connect_to_local()

# Cloud Weaviate
# client = weaviate.connect_to_weaviate_cloud(
#     cluster_url="https://xxx.weaviate.network",
#     auth_credentials=Auth.api_key("your-api-key")
# )

def create_collection(client, collection_name: str):
    """Create Weaviate collection with vectorizer."""
    from weaviate.classes.config import Configure, Property, DataType

    client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        properties=[
            Property(name="content", data_type=DataType.TEXT),
            Property(name="source", data_type=DataType.TEXT),
        ]
    )

def add_objects(client, collection_name: str, objects: list[dict]):
    """Add objects (auto-vectorized)."""
    collection = client.collections.get(collection_name)

    with collection.batch.dynamic() as batch:
        for obj in objects:
            batch.add_object(
                properties=obj
            )

def search_objects(client, collection_name: str, query: str, limit: int = 5):
    """Semantic search."""
    collection = client.collections.get(collection_name)

    response = collection.query.near_text(
        query=query,
        limit=limit
    )
    return response.objects
```

### pgvector Setup (PostgreSQL)

```python
import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="vectordb",
    user="user",
    password="password"
)
register_vector(conn)

def setup_pgvector(conn):
    """Initialize pgvector extension and table."""
    cur = conn.cursor()

    # Enable extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT,
            metadata JSONB,
            embedding vector(1536)
        )
    """)

    # Create index for fast similarity search
    cur.execute("""
        CREATE INDEX IF NOT EXISTS documents_embedding_idx
        ON documents USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)

    conn.commit()

def insert_document(conn, content: str, embedding: list, metadata: dict = None):
    """Insert document with embedding."""
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO documents (content, metadata, embedding)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (content, metadata, embedding)
    )
    conn.commit()
    return cur.fetchone()[0]

def search_documents(conn, query_embedding: list, limit: int = 5):
    """Search for similar documents."""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, content, metadata, 1 - (embedding <=> %s) as similarity
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (query_embedding, query_embedding, limit)
    )
    return cur.fetchall()
```

### Production Vector Store Service

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging

@dataclass
class SearchResult:
    id: str
    score: float
    content: str
    metadata: Dict[str, Any]

class VectorStoreBase(ABC):
    """Abstract base for vector stores."""

    @abstractmethod
    def upsert(self, documents: List[Dict]) -> None:
        pass

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int = 5) -> List[SearchResult]:
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        pass

class PineconeStore(VectorStoreBase):
    """Pinecone implementation."""

    def __init__(self, index_name: str, api_key: str):
        from pinecone import Pinecone
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)

    def upsert(self, documents: List[Dict]) -> None:
        vectors = [
            {"id": d["id"], "values": d["embedding"], "metadata": d.get("metadata", {})}
            for d in documents
        ]
        self.index.upsert(vectors=vectors)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[SearchResult]:
        results = self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
        return [
            SearchResult(
                id=m.id,
                score=m.score,
                content=m.metadata.get("content", ""),
                metadata=m.metadata
            )
            for m in results.matches
        ]

    def delete(self, ids: List[str]) -> None:
        self.index.delete(ids=ids)

class ChromaStore(VectorStoreBase):
    """Chroma implementation."""

    def __init__(self, collection_name: str, persist_dir: str = "./chroma"):
        import chromadb
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(collection_name)

    def upsert(self, documents: List[Dict]) -> None:
        self.collection.upsert(
            ids=[d["id"] for d in documents],
            embeddings=[d["embedding"] for d in documents],
            documents=[d.get("content", "") for d in documents],
            metadatas=[d.get("metadata", {}) for d in documents]
        )

    def search(self, query_vector: List[float], top_k: int = 5) -> List[SearchResult]:
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return [
            SearchResult(
                id=results["ids"][0][i],
                score=1 - results["distances"][0][i],  # Convert distance to similarity
                content=results["documents"][0][i],
                metadata=results["metadatas"][0][i]
            )
            for i in range(len(results["ids"][0]))
        ]

    def delete(self, ids: List[str]) -> None:
        self.collection.delete(ids=ids)

class VectorStoreFactory:
    """Factory for creating vector stores."""

    @staticmethod
    def create(provider: str, **kwargs) -> VectorStoreBase:
        if provider == "pinecone":
            return PineconeStore(
                index_name=kwargs["index_name"],
                api_key=kwargs["api_key"]
            )
        elif provider == "chroma":
            return ChromaStore(
                collection_name=kwargs["collection_name"],
                persist_dir=kwargs.get("persist_dir", "./chroma")
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
```

## Best Practices

1. **Index Selection**
   - Use HNSW for real-time search (<10ms)
   - Use IVF for memory-constrained environments
   - Use Flat only for <10K vectors

2. **Metadata Design**
   - Store searchable fields in metadata
   - Keep metadata small (KB, not MB)
   - Use consistent field names

3. **Batch Operations**
   - Upsert in batches (100-1000 vectors)
   - Use async/parallel for large imports
   - Monitor rate limits

4. **Namespace/Collection Strategy**
   - Separate collections by use case
   - Use namespaces for multi-tenancy
   - Plan for data isolation

5. **Monitoring**
   - Track query latency
   - Monitor index size
   - Alert on high distances (potential drift)

## Common Pitfalls

1. **Dimension Mismatch** - Embedding size doesn't match index
2. **Wrong Distance Metric** - Using L2 when data expects cosine
3. **No Batching** - Single vector upserts crushing performance
4. **Metadata Too Large** - Storing full documents in metadata
5. **Missing Index** - Queries slow without proper index
6. **Stale Data** - Not handling document updates/deletes

## References

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Chroma Documentation](https://docs.trychroma.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
