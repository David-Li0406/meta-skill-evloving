---
id: hybrid-search
name: "Hybrid Search"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Hybrid Search

## Overview

Hybrid search combines semantic (vector) search with lexical (keyword) search to leverage the strengths of both approaches. Semantic search excels at understanding meaning, while lexical search captures exact matches and rare terms. Together, they provide more robust retrieval.

## When to Use

- Technical documentation with specific terminology
- Legal or medical domains with exact phrase requirements
- When queries mix conceptual and specific terms
- Improving recall over pure vector search
- When users search using exact product names or codes

## Key Concepts

### Search Types Comparison

| Aspect | Semantic Search | Lexical Search | Hybrid |
|--------|-----------------|----------------|--------|
| Meaning | Understands context | Literal matching | Both |
| Rare terms | May miss | Excels | Captures |
| Synonyms | Handles well | Misses | Handles |
| Speed | Slower | Fast | Balanced |
| Typos | Tolerant | Sensitive | Moderate |

### Fusion Strategies

```
┌─────────────────┐     ┌─────────────────┐
│  Vector Search  │     │ Keyword Search  │
│  (Semantic)     │     │ (BM25/TF-IDF)   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
              ┌──────▼──────┐
              │   Fusion    │
              │  Strategy   │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │   Ranked    │
              │   Results   │
              └─────────────┘
```

## Implementation

### Basic Hybrid Search

```python
from typing import List, Dict, Tuple
import numpy as np
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

class HybridSearch:
    """Combine vector and BM25 search."""

    def __init__(
        self,
        documents: List[Dict],
        embedding_func: callable,
        alpha: float = 0.5  # Weight for semantic (1-alpha for keyword)
    ):
        self.documents = documents
        self.embedding_func = embedding_func
        self.alpha = alpha

        # Build indices
        self._build_bm25_index()
        self._build_vector_index()

    def _build_bm25_index(self):
        """Build BM25 keyword index."""
        tokenized_docs = [
            word_tokenize(doc["content"].lower())
            for doc in self.documents
        ]
        self.bm25 = BM25Okapi(tokenized_docs)

    def _build_vector_index(self):
        """Build vector index."""
        self.embeddings = np.array([
            self.embedding_func(doc["content"])
            for doc in self.documents
        ])
        # Normalize for cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.embeddings = self.embeddings / norms

    def search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Tuple[Dict, float]]:
        """Execute hybrid search."""
        # Semantic search
        query_embedding = self.embedding_func(query)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        semantic_scores = np.dot(self.embeddings, query_embedding)

        # BM25 search
        tokenized_query = word_tokenize(query.lower())
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Normalize scores to [0, 1]
        semantic_scores = self._normalize(semantic_scores)
        bm25_scores = self._normalize(bm25_scores)

        # Combine scores
        combined_scores = (
            self.alpha * semantic_scores +
            (1 - self.alpha) * bm25_scores
        )

        # Get top-k
        top_indices = np.argsort(combined_scores)[::-1][:top_k]

        return [
            (self.documents[i], combined_scores[i])
            for i in top_indices
        ]

    def _normalize(self, scores: np.ndarray) -> np.ndarray:
        """Min-max normalization."""
        min_score = scores.min()
        max_score = scores.max()
        if max_score == min_score:
            return np.zeros_like(scores)
        return (scores - min_score) / (max_score - min_score)
```

### Reciprocal Rank Fusion (RRF)

```python
from collections import defaultdict

def reciprocal_rank_fusion(
    rankings: List[List[str]],  # List of ranked document ID lists
    k: int = 60  # RRF constant
) -> List[Tuple[str, float]]:
    """
    Combine multiple rankings using Reciprocal Rank Fusion.
    RRF is more robust than simple score averaging.
    """
    rrf_scores = defaultdict(float)

    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            rrf_scores[doc_id] += 1.0 / (k + rank + 1)

    # Sort by RRF score
    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results

# Usage example
vector_ranking = ["doc1", "doc3", "doc2", "doc5", "doc4"]
bm25_ranking = ["doc2", "doc1", "doc4", "doc3", "doc6"]

fused = reciprocal_rank_fusion([vector_ranking, bm25_ranking])
# Result: [('doc1', 0.032), ('doc2', 0.032), ('doc3', 0.031), ...]
```

### Weaviate Hybrid Search

```python
import weaviate
from weaviate.classes.query import HybridFusion

client = weaviate.connect_to_local()

def weaviate_hybrid_search(
    collection_name: str,
    query: str,
    alpha: float = 0.5,
    limit: int = 10
) -> list:
    """
    Weaviate built-in hybrid search.

    alpha: 0 = pure BM25, 1 = pure vector
    """
    collection = client.collections.get(collection_name)

    response = collection.query.hybrid(
        query=query,
        alpha=alpha,
        limit=limit,
        fusion_type=HybridFusion.RELATIVE_SCORE  # or RANKED
    )

    return [
        {"content": obj.properties, "score": obj.metadata.score}
        for obj in response.objects
    ]
```

### Qdrant Hybrid Search

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(path="./qdrant_db")

def qdrant_hybrid_search(
    collection_name: str,
    query_vector: list,
    query_text: str,
    limit: int = 10
) -> list:
    """
    Qdrant hybrid search using prefetch and fusion.
    """
    # Create sparse vector for BM25-like search
    # (Qdrant requires setting up sparse vectors separately)

    # Vector search with text filtering
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="content",
                    match=models.MatchText(text=query_text)
                )
            ]
        ),
        limit=limit
    )

    return results
```

### Pinecone Hybrid Search

```python
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

# Initialize
pc = Pinecone(api_key="your-api-key")
index = pc.Index("hybrid-index")

# Initialize BM25 encoder
bm25 = BM25Encoder()
bm25.fit(documents)  # Fit on your corpus

def pinecone_hybrid_search(
    query: str,
    dense_embedding: list,
    alpha: float = 0.5,
    top_k: int = 10
) -> list:
    """
    Pinecone hybrid search with sparse-dense vectors.
    """
    # Generate sparse vector
    sparse_vector = bm25.encode_queries(query)

    # Query with both vectors
    results = index.query(
        vector=dense_embedding,
        sparse_vector=sparse_vector,
        top_k=top_k,
        include_metadata=True
    )

    return results.matches

# When upserting, include both dense and sparse vectors
def upsert_hybrid(doc_id: str, text: str, dense_vector: list):
    """Upsert document with both vector types."""
    sparse_vector = bm25.encode_documents(text)

    index.upsert(vectors=[{
        "id": doc_id,
        "values": dense_vector,
        "sparse_values": sparse_vector,
        "metadata": {"content": text}
    }])
```

### Advanced Hybrid with Elasticsearch

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

def create_hybrid_index(index_name: str):
    """Create Elasticsearch index with both dense and sparse search."""
    mapping = {
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": 1536,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)

def elasticsearch_hybrid_search(
    index_name: str,
    query_text: str,
    query_vector: list,
    alpha: float = 0.5,
    size: int = 10
) -> list:
    """
    Elasticsearch hybrid search using script_score.
    """
    query = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "content": {
                                        "query": query_text,
                                        "boost": 1 - alpha
                                    }
                                }
                            }
                        ]
                    }
                },
                "script": {
                    "source": f"""
                        {alpha} * cosineSimilarity(params.query_vector, 'embedding') +
                        (1 - {alpha}) * _score / 10
                    """,
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        },
        "size": size
    }

    results = es.search(index=index_name, body=query)
    return results["hits"]["hits"]
```

### Dynamic Alpha Selection

```python
def determine_alpha(query: str) -> float:
    """
    Dynamically select alpha based on query characteristics.
    """
    # Check for exact match indicators
    has_quotes = '"' in query
    has_codes = any(char.isdigit() for char in query)
    is_short = len(query.split()) <= 3

    # More specific queries → more keyword weight
    if has_quotes:
        return 0.3  # Favor keyword search
    elif has_codes:
        return 0.4
    elif is_short:
        return 0.5  # Balanced
    else:
        return 0.7  # Favor semantic for longer queries

def intelligent_hybrid_search(
    search_engine,
    query: str,
    top_k: int = 10
) -> list:
    """Hybrid search with dynamic alpha."""
    alpha = determine_alpha(query)
    return search_engine.search(query, alpha=alpha, top_k=top_k)
```

### Production Hybrid Search Service

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

class FusionMethod(Enum):
    LINEAR = "linear"
    RRF = "rrf"
    WEIGHTED_RRF = "weighted_rrf"

@dataclass
class HybridSearchConfig:
    alpha: float = 0.5
    fusion_method: FusionMethod = FusionMethod.RRF
    bm25_k1: float = 1.5
    bm25_b: float = 0.75
    rrf_k: int = 60
    enable_auto_alpha: bool = False

class HybridSearchService:
    """Production-ready hybrid search service."""

    def __init__(
        self,
        documents: List[Dict],
        embedding_service,
        config: Optional[HybridSearchConfig] = None
    ):
        self.documents = documents
        self.embedding_service = embedding_service
        self.config = config or HybridSearchConfig()
        self.logger = logging.getLogger(__name__)

        self._build_indices()

    def _build_indices(self):
        """Build both search indices."""
        from rank_bm25 import BM25Okapi

        # BM25 index
        tokenized = [self._tokenize(d["content"]) for d in self.documents]
        self.bm25 = BM25Okapi(
            tokenized,
            k1=self.config.bm25_k1,
            b=self.config.bm25_b
        )

        # Vector index
        self.logger.info("Building vector index...")
        texts = [d["content"] for d in self.documents]
        self.embeddings = self.embedding_service.embed_batch(texts)

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return text.lower().split()

    def search(
        self,
        query: str,
        top_k: int = 10,
        alpha: Optional[float] = None,
        filters: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Execute hybrid search."""
        # Determine alpha
        if alpha is None:
            if self.config.enable_auto_alpha:
                alpha = determine_alpha(query)
            else:
                alpha = self.config.alpha

        # Get rankings from both methods
        vector_ranking = self._vector_search(query, top_k * 2)
        keyword_ranking = self._keyword_search(query, top_k * 2)

        # Fuse results
        if self.config.fusion_method == FusionMethod.RRF:
            fused = self._rrf_fusion(vector_ranking, keyword_ranking)
        else:
            fused = self._linear_fusion(vector_ranking, keyword_ranking, alpha)

        # Apply filters
        if filters:
            fused = self._apply_filters(fused, filters)

        return fused[:top_k]

    def _vector_search(self, query: str, top_k: int) -> List[Tuple[int, float]]:
        """Semantic search component."""
        query_embedding = self.embedding_service.embed(query)

        similarities = np.dot(self.embeddings, query_embedding)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [(idx, similarities[idx]) for idx in top_indices]

    def _keyword_search(self, query: str, top_k: int) -> List[Tuple[int, float]]:
        """BM25 search component."""
        tokens = self._tokenize(query)
        scores = self.bm25.get_scores(tokens)

        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(idx, scores[idx]) for idx in top_indices]

    def _rrf_fusion(
        self,
        vector_results: List[Tuple[int, float]],
        keyword_results: List[Tuple[int, float]]
    ) -> List[Dict]:
        """Reciprocal Rank Fusion."""
        rrf_scores = defaultdict(float)
        k = self.config.rrf_k

        for rank, (idx, _) in enumerate(vector_results):
            rrf_scores[idx] += 1.0 / (k + rank + 1)

        for rank, (idx, _) in enumerate(keyword_results):
            rrf_scores[idx] += 1.0 / (k + rank + 1)

        sorted_indices = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        return [
            {
                "document": self.documents[idx],
                "score": score,
                "fusion_method": "rrf"
            }
            for idx, score in sorted_indices
        ]

    def _linear_fusion(
        self,
        vector_results: List[Tuple[int, float]],
        keyword_results: List[Tuple[int, float]],
        alpha: float
    ) -> List[Dict]:
        """Linear combination of scores."""
        combined_scores = {}

        # Normalize and combine
        vector_dict = {idx: score for idx, score in vector_results}
        keyword_dict = {idx: score for idx, score in keyword_results}

        all_indices = set(vector_dict.keys()) | set(keyword_dict.keys())

        for idx in all_indices:
            v_score = vector_dict.get(idx, 0)
            k_score = keyword_dict.get(idx, 0)
            combined_scores[idx] = alpha * v_score + (1 - alpha) * k_score

        sorted_indices = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        return [
            {
                "document": self.documents[idx],
                "score": score,
                "fusion_method": "linear",
                "alpha": alpha
            }
            for idx, score in sorted_indices
        ]

    def _apply_filters(
        self,
        results: List[Dict],
        filters: Dict
    ) -> List[Dict]:
        """Apply metadata filters to results."""
        filtered = []
        for result in results:
            doc = result["document"]
            match = all(
                doc.get("metadata", {}).get(key) == value
                for key, value in filters.items()
            )
            if match:
                filtered.append(result)
        return filtered
```

## Best Practices

1. **Alpha Tuning**
   - Start with 0.5 and tune based on query types
   - Use higher alpha for conceptual queries
   - Use lower alpha for specific/technical queries

2. **Fusion Method Selection**
   - RRF is generally more robust
   - Linear fusion is faster
   - Test both on your data

3. **Index Optimization**
   - Use appropriate BM25 parameters for your domain
   - Consider stop words for keyword search
   - Normalize vectors for cosine similarity

4. **Query Analysis**
   - Detect query type dynamically
   - Handle edge cases (empty queries, very long queries)
   - Log and analyze search patterns

5. **Evaluation**
   - Compare hybrid vs. pure approaches
   - Test on diverse query sets
   - Monitor production performance

## Common Pitfalls

1. **Score Scale Mismatch** - Not normalizing scores before fusion
2. **Wrong Alpha** - Using same alpha for all query types
3. **BM25 Without Preprocessing** - Not handling stop words, case
4. **Ignoring Rare Terms** - Semantic search missing exact matches
5. **Over-relying on One Method** - Not testing both components separately
6. **No Query Analysis** - Static approach for dynamic queries

## References

- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Weaviate Hybrid Search](https://weaviate.io/developers/weaviate/search/hybrid)
- [Pinecone Hybrid Search](https://docs.pinecone.io/docs/hybrid-search)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)
