"""Embedding service for skill and plan retrieval."""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
import requests

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Embedding service for similarity-based retrieval.

    Supports multiple backends:
    - HTTP API (e.g., local Qwen embedding server)
    - In-process model (future)
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:7000",
        model: str = "Qwen3-Embedding-8B",
        timeout: int = 30
    ):
        """
        Initialize embedding service.

        Args:
            base_url: API endpoint for embedding service
            model: Embedding model name
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._cache: Dict[str, np.ndarray] = {}

    def encode(self, texts: List[str], use_cache: bool = True) -> np.ndarray:
        """
        Encode texts into embeddings.

        Args:
            texts: List of texts to encode
            use_cache: Whether to use cached embeddings

        Returns:
            Numpy array of shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])

        embeddings = []
        uncached_indices = []
        uncached_texts = []

        for i, text in enumerate(texts):
            if use_cache and text in self._cache:
                embeddings.append(self._cache[text])
            else:
                uncached_indices.append(i)
                uncached_texts.append(text)
                embeddings.append(None)

        if uncached_texts:
            new_embeddings = self._call_api(uncached_texts)
            for idx, text, emb in zip(uncached_indices, uncached_texts, new_embeddings):
                embeddings[idx] = emb
                if use_cache:
                    self._cache[text] = emb

        return np.array(embeddings)

    def _call_api(self, texts: List[str]) -> List[np.ndarray]:
        """Call embedding API."""
        try:
            response = requests.post(
                f"{self.base_url}/encode",
                json={"texts": texts, "model": self.model},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return [np.array(emb) for emb in data.get("embeddings", [])]
        except requests.RequestException as e:
            logger.error(f"Embedding API error: {e}")
            dim = 4096
            return [np.zeros(dim) for _ in texts]

    def similarity(
        self,
        query_embedding: np.ndarray,
        corpus_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Compute cosine similarity.

        Args:
            query_embedding: Query embedding (1D or 2D array)
            corpus_embeddings: Corpus embeddings (2D array)

        Returns:
            Similarity scores
        """
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        query_norm = query_embedding / (np.linalg.norm(query_embedding, axis=1, keepdims=True) + 1e-10)
        corpus_norm = corpus_embeddings / (np.linalg.norm(corpus_embeddings, axis=1, keepdims=True) + 1e-10)

        return np.dot(query_norm, corpus_norm.T).flatten()

    def top_k(
        self,
        query: str,
        corpus: List[str],
        corpus_embeddings: Optional[np.ndarray] = None,
        k: int = 5,
        threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Find top-k similar items.

        Args:
            query: Query text
            corpus: List of corpus texts
            corpus_embeddings: Pre-computed corpus embeddings (optional)
            k: Number of results
            threshold: Minimum similarity threshold

        Returns:
            List of dicts with index, text, and similarity
        """
        if not corpus:
            return []

        query_emb = self.encode([query])[0]
        if corpus_embeddings is None:
            corpus_embeddings = self.encode(corpus)

        similarities = self.similarity(query_emb, corpus_embeddings)

        indices = np.argsort(similarities)[::-1]
        results = []
        for idx in indices[:k]:
            if similarities[idx] >= threshold:
                results.append({
                    "index": int(idx),
                    "text": corpus[idx],
                    "similarity": float(similarities[idx])
                })

        return results
