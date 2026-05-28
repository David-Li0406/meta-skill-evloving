---
id: embedding-generation
name: "Embedding Generation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Embedding Generation

## Overview

Embeddings are dense vector representations of text that capture semantic meaning. They enable similarity search, clustering, classification, and form the foundation of RAG systems. This methodology covers embedding models, generation strategies, and optimization techniques.

## When to Use

- Semantic search implementations
- Document similarity matching
- RAG pipeline construction
- Text clustering and classification
- Recommendation systems
- Anomaly detection in text

## Key Concepts

### Embedding Models Comparison

| Model | Dimensions | Context | Provider | Cost |
|-------|------------|---------|----------|------|
| text-embedding-3-large | 3072 | 8191 | OpenAI | $0.13/1M |
| text-embedding-3-small | 1536 | 8191 | OpenAI | $0.02/1M |
| text-embedding-ada-002 | 1536 | 8191 | OpenAI | $0.10/1M |
| voyage-3 | 1024 | 32K | Voyage | $0.06/1M |
| embed-v3 | 1024 | 512 | Cohere | $0.10/1M |
| nomic-embed-text | 768 | 8192 | Local/Ollama | Free |
| all-MiniLM-L6-v2 | 384 | 256 | Local/HF | Free |
| bge-large-en-v1.5 | 1024 | 512 | Local/HF | Free |

### How Embeddings Work

```
Text: "Machine learning is fascinating"
         │
         ▼
    ┌─────────────┐
    │  Embedding  │
    │    Model    │
    └─────────────┘
         │
         ▼
Vector: [0.023, -0.156, 0.089, ..., 0.045]
        └──────────── 1536 dimensions ──────────────┘
```

## Implementation

### OpenAI Embeddings

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """Generate embedding using OpenAI."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def get_embeddings_batch(texts: list[str], model: str = "text-embedding-3-small") -> list:
    """Generate embeddings for multiple texts."""
    texts = [t.replace("\n", " ") for t in texts]
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]

# With dimension reduction (text-embedding-3 models)
def get_reduced_embedding(text: str, dimensions: int = 256) -> list:
    """Get lower-dimensional embedding for efficiency."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
        dimensions=dimensions  # Only for text-embedding-3 models
    )
    return response.data[0].embedding
```

### Local Embeddings with Sentence Transformers

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model (downloads on first use)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_local_embedding(text: str) -> np.ndarray:
    """Generate embedding locally."""
    return model.encode(text)

def get_local_embeddings_batch(texts: list[str]) -> np.ndarray:
    """Batch embedding generation."""
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

# Using BGE models (better quality)
bge_model = SentenceTransformer('BAAI/bge-large-en-v1.5')

def get_bge_embedding(text: str) -> np.ndarray:
    """BGE embeddings with instruction prefix."""
    # BGE models work better with instruction prefix for queries
    instruction = "Represent this sentence for retrieval: "
    return bge_model.encode(instruction + text)
```

### Ollama Embeddings

```python
import ollama

def get_ollama_embedding(text: str, model: str = "nomic-embed-text") -> list:
    """Generate embedding using Ollama."""
    response = ollama.embeddings(
        model=model,
        prompt=text
    )
    return response["embedding"]

def get_ollama_embeddings_batch(texts: list[str]) -> list:
    """Batch embeddings with Ollama."""
    embeddings = []
    for text in texts:
        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=text
        )
        embeddings.append(response["embedding"])
    return embeddings
```

### Cohere Embeddings

```python
import cohere

co = cohere.Client(api_key="your-api-key")

def get_cohere_embedding(
    texts: list[str],
    input_type: str = "search_document"
) -> list:
    """
    Generate Cohere embeddings.

    input_type options:
    - search_document: For documents to be searched
    - search_query: For search queries
    - classification: For classification tasks
    - clustering: For clustering tasks
    """
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type=input_type
    )
    return response.embeddings
```

### Similarity Calculations

```python
import numpy as np
from typing import List, Tuple

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate Euclidean distance between two vectors."""
    return np.linalg.norm(a - b)

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate dot product (for normalized vectors)."""
    return np.dot(a, b)

def find_most_similar(
    query_embedding: np.ndarray,
    document_embeddings: np.ndarray,
    top_k: int = 5
) -> List[Tuple[int, float]]:
    """Find most similar documents to query."""
    # Calculate all similarities at once
    similarities = np.dot(document_embeddings, query_embedding) / (
        np.linalg.norm(document_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # Get top-k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [(idx, similarities[idx]) for idx in top_indices]
```

### Embedding Cache

```python
import hashlib
import json
from pathlib import Path
from typing import Optional

class EmbeddingCache:
    """Cache embeddings to avoid recomputation."""

    def __init__(self, cache_dir: str = ".embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_key(self, text: str, model: str) -> str:
        """Generate cache key from text and model."""
        content = f"{model}:{text}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, text: str, model: str) -> Optional[list]:
        """Retrieve cached embedding."""
        key = self._get_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            with open(cache_file, "r") as f:
                return json.load(f)
        return None

    def set(self, text: str, model: str, embedding: list):
        """Cache embedding."""
        key = self._get_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"

        with open(cache_file, "w") as f:
            json.dump(embedding, f)

    def get_or_create(
        self,
        text: str,
        model: str,
        embed_func: callable
    ) -> list:
        """Get from cache or generate and cache."""
        cached = self.get(text, model)
        if cached:
            return cached

        embedding = embed_func(text)
        self.set(text, model, embedding)
        return embedding
```

### Production Embedding Service

```python
from dataclasses import dataclass
from typing import List, Optional, Union
import numpy as np
import logging
from concurrent.futures import ThreadPoolExecutor

@dataclass
class EmbeddingConfig:
    provider: str = "openai"  # openai, local, ollama, cohere
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    batch_size: int = 100
    cache_enabled: bool = True

class EmbeddingService:
    """Production-ready embedding service."""

    def __init__(self, config: Optional[EmbeddingConfig] = None):
        self.config = config or EmbeddingConfig()
        self.logger = logging.getLogger(__name__)
        self.cache = EmbeddingCache() if self.config.cache_enabled else None
        self._init_model()

    def _init_model(self):
        """Initialize embedding model based on provider."""
        if self.config.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI()
        elif self.config.provider == "local":
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.config.model)
        elif self.config.provider == "ollama":
            import ollama
            self.client = ollama

    def embed(self, text: str) -> np.ndarray:
        """Generate single embedding."""
        if self.cache:
            cached = self.cache.get(text, self.config.model)
            if cached:
                return np.array(cached)

        embedding = self._generate_embedding(text)

        if self.cache:
            self.cache.set(text, self.config.model, embedding.tolist())

        return embedding

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        if self.config.provider == "openai":
            return self._embed_batch_openai(texts)
        elif self.config.provider == "local":
            return self.model.encode(texts, batch_size=self.config.batch_size)
        else:
            # Fallback to sequential
            return np.array([self.embed(t) for t in texts])

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding based on provider."""
        if self.config.provider == "openai":
            kwargs = {"input": text, "model": self.config.model}
            if self.config.dimensions:
                kwargs["dimensions"] = self.config.dimensions
            response = self.client.embeddings.create(**kwargs)
            return np.array(response.data[0].embedding)

        elif self.config.provider == "local":
            return self.model.encode(text)

        elif self.config.provider == "ollama":
            response = self.client.embeddings(
                model=self.config.model,
                prompt=text
            )
            return np.array(response["embedding"])

    def _embed_batch_openai(self, texts: List[str]) -> np.ndarray:
        """Batch embedding with OpenAI (handles rate limits)."""
        all_embeddings = []

        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            kwargs = {"input": batch, "model": self.config.model}
            if self.config.dimensions:
                kwargs["dimensions"] = self.config.dimensions

            response = self.client.embeddings.create(**kwargs)
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)

        return np.array(all_embeddings)

    def similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        emb1 = self.embed(text1)
        emb2 = self.embed(text2)
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
```

### Embedding Normalization

```python
def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    """Normalize embedding to unit length."""
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm

def normalize_batch(embeddings: np.ndarray) -> np.ndarray:
    """Normalize batch of embeddings."""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1  # Avoid division by zero
    return embeddings / norms
```

## Best Practices

1. **Model Selection**
   - Use OpenAI text-embedding-3-small for cost-effectiveness
   - Use local models for privacy/offline requirements
   - Match embedding model to your similarity task

2. **Batching**
   - Always batch when embedding multiple texts
   - Use appropriate batch sizes (100-1000 for APIs)
   - Implement rate limiting for API calls

3. **Caching**
   - Cache embeddings for repeated texts
   - Use content-based keys (hash of text + model)
   - Consider TTL for dynamic content

4. **Normalization**
   - Normalize embeddings for cosine similarity
   - Pre-normalize for faster dot product search
   - Store normalized embeddings in vector DBs

5. **Dimension Reduction**
   - Use native dimension reduction when available
   - Consider PCA for local models
   - Balance accuracy vs. storage/speed

## Common Pitfalls

1. **Token Limit Exceeded** - Not truncating long texts
2. **Wrong Similarity Metric** - Using Euclidean with unnormalized vectors
3. **Model Mismatch** - Querying with different model than indexing
4. **No Batching** - Making individual API calls for each text
5. **Ignoring Empty Texts** - Empty strings produce zero vectors
6. **Inconsistent Preprocessing** - Different cleaning for index vs. query

## References

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Cohere Embed Documentation](https://docs.cohere.com/reference/embed)
