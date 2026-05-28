---
id: reranking
name: "Reranking"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Reranking

## Overview

Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models. While first-stage retrieval prioritizes speed (bi-encoders), reranking uses slower but more accurate cross-encoders to improve result quality.

## When to Use

- When initial retrieval returns noisy results
- High-precision requirements (legal, medical)
- After hybrid search to refine fusion results
- When you can afford latency for quality
- Improving RAG answer accuracy

## Key Concepts

### Two-Stage Retrieval

```
┌─────────────────────────────────────────────────────────────┐
│                     STAGE 1: RETRIEVAL                       │
│  Query → Bi-Encoder → Vector Search → Top 100 candidates    │
│                    (Fast, ~10ms)                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     STAGE 2: RERANKING                       │
│  (Query, Doc) pairs → Cross-Encoder → Top 10 reranked       │
│                    (Slower, ~100-500ms)                      │
└─────────────────────────────────────────────────────────────┘
```

### Bi-Encoder vs Cross-Encoder

| Aspect | Bi-Encoder | Cross-Encoder |
|--------|------------|---------------|
| Speed | Fast (separate encoding) | Slow (joint encoding) |
| Accuracy | Good | Excellent |
| Precomputation | Yes (store doc embeddings) | No |
| Use | First-stage retrieval | Reranking |

## Implementation

### Cohere Rerank

```python
import cohere

co = cohere.Client(api_key="your-api-key")

def cohere_rerank(
    query: str,
    documents: list[str],
    top_n: int = 5,
    model: str = "rerank-english-v3.0"
) -> list[dict]:
    """
    Rerank documents using Cohere Rerank API.
    """
    response = co.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model=model
    )

    return [
        {
            "document": documents[result.index],
            "score": result.relevance_score,
            "index": result.index
        }
        for result in response.results
    ]

# Usage
documents = [
    "Python is a programming language.",
    "Machine learning uses Python extensively.",
    "JavaScript is used for web development.",
    "Python has great ML libraries like scikit-learn.",
]

results = cohere_rerank(
    query="What programming language is best for ML?",
    documents=documents,
    top_n=3
)

for r in results:
    print(f"Score: {r['score']:.4f} - {r['document']}")
```

### Cross-Encoder with Sentence Transformers

```python
from sentence_transformers import CrossEncoder
import numpy as np

# Load reranking model
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

def cross_encoder_rerank(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    Rerank using local cross-encoder model.
    """
    # Create query-document pairs
    pairs = [[query, doc] for doc in documents]

    # Score pairs
    scores = reranker.predict(pairs)

    # Sort by score
    sorted_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "document": documents[idx],
            "score": float(scores[idx]),
            "index": idx
        }
        for idx in sorted_indices
    ]

# More powerful model options
RERANKER_MODELS = {
    "fast": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "balanced": "cross-encoder/ms-marco-MiniLM-L-12-v2",
    "accurate": "cross-encoder/ms-marco-electra-base",
    "multilingual": "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
}
```

### Jina Rerank

```python
import requests

def jina_rerank(
    query: str,
    documents: list[str],
    top_n: int = 5,
    api_key: str = None
) -> list[dict]:
    """
    Rerank using Jina AI Reranker.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.jina.ai/v1/rerank",
        headers=headers,
        json={
            "query": query,
            "documents": documents,
            "top_n": top_n,
            "model": "jina-reranker-v2-base-multilingual"
        }
    )

    data = response.json()

    return [
        {
            "document": documents[r["index"]],
            "score": r["relevance_score"],
            "index": r["index"]
        }
        for r in data["results"]
    ]
```

### Voyage AI Rerank

```python
import voyageai

vo = voyageai.Client(api_key="your-api-key")

def voyage_rerank(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    Rerank using Voyage AI.
    """
    response = vo.rerank(
        query=query,
        documents=documents,
        model="rerank-2",
        top_k=top_k
    )

    return [
        {
            "document": documents[r.index],
            "score": r.relevance_score,
            "index": r.index
        }
        for r in response.results
    ]
```

### LLM-based Reranking

```python
from openai import OpenAI
import json

client = OpenAI()

def llm_rerank(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    Rerank using LLM (slower but can handle complex queries).
    """
    # Format documents with indices
    doc_list = "\n".join([
        f"[{i}] {doc[:500]}"  # Truncate long docs
        for i, doc in enumerate(documents)
    ])

    prompt = f"""Given the query and documents, rank the documents by relevance.

Query: {query}

Documents:
{doc_list}

Return a JSON array of document indices ordered by relevance (most relevant first).
Only include the top {top_k} most relevant documents.
Format: {{"rankings": [index1, index2, ...]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)
    rankings = result.get("rankings", [])[:top_k]

    return [
        {
            "document": documents[idx],
            "rank": rank + 1,
            "index": idx
        }
        for rank, idx in enumerate(rankings)
        if idx < len(documents)
    ]

def llm_rerank_with_scores(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    LLM rerank with relevance scores.
    """
    doc_list = "\n".join([
        f"[{i}] {doc[:500]}"
        for i, doc in enumerate(documents)
    ])

    prompt = f"""Score each document's relevance to the query from 0-10.

Query: {query}

Documents:
{doc_list}

Return JSON with scores: {{"scores": [{{"index": 0, "score": 8}}, ...]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)
    scores = sorted(result["scores"], key=lambda x: x["score"], reverse=True)

    return [
        {
            "document": documents[s["index"]],
            "score": s["score"] / 10.0,
            "index": s["index"]
        }
        for s in scores[:top_k]
        if s["index"] < len(documents)
    ]
```

### Integrated RAG with Reranking

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class RetrievalConfig:
    initial_top_k: int = 50
    rerank_top_k: int = 5
    reranker: str = "cross-encoder"  # cross-encoder, cohere, llm

class RerankingRAG:
    """RAG pipeline with reranking stage."""

    def __init__(
        self,
        vector_store,
        embedding_service,
        config: RetrievalConfig = None
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.config = config or RetrievalConfig()

        # Initialize reranker
        if self.config.reranker == "cross-encoder":
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')
        elif self.config.reranker == "cohere":
            import cohere
            self.reranker = cohere.Client()

    def retrieve(
        self,
        query: str,
        filter: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Two-stage retrieval with reranking."""
        # Stage 1: Initial retrieval
        query_embedding = self.embedding_service.embed(query)
        initial_results = self.vector_store.search(
            query_embedding,
            top_k=self.config.initial_top_k,
            filter=filter
        )

        documents = [r["content"] for r in initial_results]

        # Stage 2: Reranking
        if self.config.reranker == "cross-encoder":
            reranked = self._cross_encoder_rerank(query, documents, initial_results)
        elif self.config.reranker == "cohere":
            reranked = self._cohere_rerank(query, documents, initial_results)
        else:
            reranked = self._llm_rerank(query, documents, initial_results)

        return reranked[:self.config.rerank_top_k]

    def _cross_encoder_rerank(
        self,
        query: str,
        documents: List[str],
        results: List[Dict]
    ) -> List[Dict]:
        """Cross-encoder reranking."""
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs)

        for i, result in enumerate(results):
            result["rerank_score"] = float(scores[i])

        return sorted(results, key=lambda x: x["rerank_score"], reverse=True)

    def _cohere_rerank(
        self,
        query: str,
        documents: List[str],
        results: List[Dict]
    ) -> List[Dict]:
        """Cohere reranking."""
        response = self.reranker.rerank(
            query=query,
            documents=documents,
            top_n=self.config.rerank_top_k,
            model="rerank-english-v3.0"
        )

        reranked = []
        for r in response.results:
            result = results[r.index].copy()
            result["rerank_score"] = r.relevance_score
            reranked.append(result)

        return reranked

    def _llm_rerank(
        self,
        query: str,
        documents: List[str],
        results: List[Dict]
    ) -> List[Dict]:
        """LLM-based reranking."""
        rerank_results = llm_rerank_with_scores(
            query=query,
            documents=documents,
            top_k=self.config.rerank_top_k
        )

        reranked = []
        for r in rerank_results:
            result = results[r["index"]].copy()
            result["rerank_score"] = r["score"]
            reranked.append(result)

        return reranked
```

### Batch Reranking

```python
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

def batch_rerank(
    queries: List[str],
    document_lists: List[List[str]],
    reranker,
    top_k: int = 5,
    max_workers: int = 4
) -> List[List[dict]]:
    """
    Rerank multiple query-documents pairs in parallel.
    """
    def rerank_single(args: Tuple[str, List[str]]) -> List[dict]:
        query, documents = args
        pairs = [[query, doc] for doc in documents]
        scores = reranker.predict(pairs)

        sorted_indices = np.argsort(scores)[::-1][:top_k]
        return [
            {"document": documents[i], "score": float(scores[i])}
            for i in sorted_indices
        ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(
            rerank_single,
            zip(queries, document_lists)
        ))

    return results
```

### Reranking with Diversity

```python
import numpy as np
from typing import List, Dict

def maximal_marginal_relevance(
    query_embedding: np.ndarray,
    document_embeddings: np.ndarray,
    relevance_scores: np.ndarray,
    lambda_param: float = 0.5,
    top_k: int = 5
) -> List[int]:
    """
    MMR reranking for diversity.
    Balances relevance with diversity.
    """
    selected = []
    remaining = list(range(len(relevance_scores)))

    # Normalize embeddings
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    doc_norms = document_embeddings / np.linalg.norm(
        document_embeddings, axis=1, keepdims=True
    )

    while len(selected) < top_k and remaining:
        mmr_scores = []

        for idx in remaining:
            # Relevance to query
            relevance = relevance_scores[idx]

            # Max similarity to already selected docs
            if selected:
                similarities = np.dot(doc_norms[selected], doc_norms[idx])
                max_sim = np.max(similarities)
            else:
                max_sim = 0

            # MMR score
            mmr = lambda_param * relevance - (1 - lambda_param) * max_sim
            mmr_scores.append((idx, mmr))

        # Select highest MMR
        best_idx = max(mmr_scores, key=lambda x: x[1])[0]
        selected.append(best_idx)
        remaining.remove(best_idx)

    return selected

def diverse_rerank(
    query: str,
    documents: List[str],
    reranker,
    embedding_service,
    lambda_param: float = 0.5,
    top_k: int = 5
) -> List[Dict]:
    """
    Rerank with diversity consideration.
    """
    # Get relevance scores
    pairs = [[query, doc] for doc in documents]
    relevance_scores = reranker.predict(pairs)

    # Get embeddings for diversity calculation
    query_emb = embedding_service.embed(query)
    doc_embs = embedding_service.embed_batch(documents)

    # MMR selection
    selected_indices = maximal_marginal_relevance(
        query_emb, doc_embs, relevance_scores,
        lambda_param=lambda_param,
        top_k=top_k
    )

    return [
        {
            "document": documents[idx],
            "score": float(relevance_scores[idx]),
            "index": idx
        }
        for idx in selected_indices
    ]
```

### Production Reranking Service

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import logging
import time

class RerankerType(Enum):
    CROSS_ENCODER = "cross_encoder"
    COHERE = "cohere"
    JINA = "jina"
    LLM = "llm"

@dataclass
class RerankerConfig:
    reranker_type: RerankerType = RerankerType.CROSS_ENCODER
    model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    batch_size: int = 32
    timeout: float = 30.0
    fallback_to_original: bool = True

class RerankerService:
    """Production reranking service with fallback."""

    def __init__(self, config: Optional[RerankerConfig] = None):
        self.config = config or RerankerConfig()
        self.logger = logging.getLogger(__name__)
        self._init_reranker()

    def _init_reranker(self):
        """Initialize reranker based on type."""
        if self.config.reranker_type == RerankerType.CROSS_ENCODER:
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder(self.config.model)
        elif self.config.reranker_type == RerankerType.COHERE:
            import cohere
            self.reranker = cohere.Client()

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        metadata: Optional[List[Dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents with error handling and metrics.
        """
        start_time = time.time()

        try:
            if self.config.reranker_type == RerankerType.CROSS_ENCODER:
                results = self._cross_encoder_rerank(query, documents, top_k)
            elif self.config.reranker_type == RerankerType.COHERE:
                results = self._cohere_rerank(query, documents, top_k)
            else:
                results = self._llm_rerank(query, documents, top_k)

            # Attach metadata if provided
            if metadata:
                for result in results:
                    idx = result["index"]
                    if idx < len(metadata):
                        result["metadata"] = metadata[idx]

            latency = time.time() - start_time
            self.logger.info(f"Reranking completed in {latency:.3f}s")

            return results

        except Exception as e:
            self.logger.error(f"Reranking failed: {e}")

            if self.config.fallback_to_original:
                # Return original order
                return [
                    {"document": doc, "score": 1.0 - i/len(documents), "index": i}
                    for i, doc in enumerate(documents[:top_k])
                ]
            raise

    def _cross_encoder_rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict]:
        """Cross-encoder reranking."""
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs, batch_size=self.config.batch_size)

        sorted_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {"document": documents[i], "score": float(scores[i]), "index": i}
            for i in sorted_indices
        ]
```

## Best Practices

1. **Candidate Pool Size**
   - Retrieve more candidates than needed (3-10x)
   - Balance recall vs. reranking latency
   - Monitor retrieval recall at different pool sizes

2. **Model Selection**
   - Cross-encoders for latency-sensitive applications
   - API services for simplicity
   - LLM reranking for complex queries

3. **Latency Management**
   - Cache reranking results when possible
   - Batch similar queries
   - Set appropriate timeouts

4. **Diversity**
   - Use MMR when results are too similar
   - Balance relevance and diversity
   - Consider user intent

5. **Evaluation**
   - Measure improvement over retrieval-only
   - Track latency vs. quality tradeoff
   - A/B test different rerankers

## Common Pitfalls

1. **Too Few Candidates** - Reranker can't recover if relevant docs not retrieved
2. **Ignoring Latency** - Reranking adds 100-500ms typically
3. **Wrong Model Language** - Using English reranker for multilingual content
4. **No Fallback** - System fails when reranker unavailable
5. **Over-truncating** - Cutting off important document content
6. **Score Misinterpretation** - Different rerankers have different score scales

## References

- [Cross-Encoders (SBERT)](https://www.sbert.net/examples/applications/cross-encoder/README.html)
- [Cohere Rerank](https://docs.cohere.com/docs/rerank)
- [Jina Reranker](https://jina.ai/reranker/)
- [MS MARCO Reranking](https://microsoft.github.io/msmarco/)
