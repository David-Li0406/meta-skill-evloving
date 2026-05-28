"""Embedding cache for avoiding redundant API calls.

Caches embeddings in /tmp directory to avoid repeated API calls for the same text.
Uses a simple file-based cache with hash-based filenames.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .clients import OpenAIClient

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = "/tmp/kg2_embedding_cache"


def _text_hash(text: str) -> str:
    """Compute hash of text for cache key."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


class EmbeddingCache:
    """File-based embedding cache.

    Stores embeddings in /tmp/kg2_embedding_cache/{model}/{hash}.json
    """

    def __init__(
        self,
        openai: OpenAIClient,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        self.openai = openai
        self.cache_dir = Path(cache_dir)
        self.model = openai.embedding_model
        self._model_dir = self.cache_dir / self.model.replace("/", "_")
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        self._model_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, text_hash: str) -> Path:
        """Get cache file path for a text hash."""
        return self._model_dir / f"{text_hash}.json"

    def _load_cached(self, text_hash: str) -> list[float] | None:
        """Load embedding from cache if exists."""
        path = self._cache_path(text_hash)
        if not path.exists():
            return None

        try:
            with open(path) as f:
                data = json.load(f)
                return data.get('embedding')
        except (json.JSONDecodeError, OSError) as e:
            logger.debug("Cache read error for %s: %s", text_hash, e)
            return None

    def _save_cached(self, text_hash: str, embedding: Sequence[float]) -> None:
        """Save embedding to cache."""
        path = self._cache_path(text_hash)
        try:
            with open(path, 'w') as f:
                json.dump({'embedding': list(embedding)}, f)
        except OSError as e:
            logger.debug("Cache write error for %s: %s", text_hash, e)

    def embed(self, text: str) -> list[float]:
        """Get embedding for text, using cache if available.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        text_hash = _text_hash(text)

        # Try cache first
        cached = self._load_cached(text_hash)
        if cached is not None:
            logger.debug("Cache hit for text hash %s", text_hash)
            return cached

        # Compute embedding
        logger.debug("Cache miss for text hash %s, calling API", text_hash)
        embedding = self.openai.embed(text)

        # Save to cache
        self._save_cached(text_hash, embedding)

        return embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts, using cache where available.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (same order as input)
        """
        if not texts:
            return []

        results: list[list[float] | None] = [None] * len(texts)
        uncached_indices: list[int] = []
        uncached_texts: list[str] = []

        # Check cache for each text
        for i, text in enumerate(texts):
            text_hash = _text_hash(text)
            cached = self._load_cached(text_hash)
            if cached is not None:
                results[i] = cached
            else:
                uncached_indices.append(i)
                uncached_texts.append(text)

        logger.debug("Batch embed: %d cached, %d uncached",
                    len(texts) - len(uncached_texts), len(uncached_texts))

        # Fetch uncached embeddings in batch
        if uncached_texts:
            embeddings = self.openai.embed_batch(uncached_texts)
            for idx, text, embedding in zip(uncached_indices, uncached_texts, embeddings, strict=True):
                results[idx] = embedding
                self._save_cached(_text_hash(text), embedding)

        # Type assertion: all results should be filled now
        return [r for r in results if r is not None]

    def clear(self) -> int:
        """Clear all cached embeddings.

        Returns:
            Number of files deleted
        """
        count = 0
        if self._model_dir.exists():
            for f in self._model_dir.glob("*.json"):
                try:
                    f.unlink()
                    count += 1
                except OSError:
                    pass
        return count

    def stats(self) -> dict[str, int]:
        """Get cache statistics.

        Returns:
            Dict with 'count' and 'size_bytes' keys
        """
        count = 0
        size_bytes = 0
        if self._model_dir.exists():
            for f in self._model_dir.glob("*.json"):
                count += 1
                with contextlib.suppress(OSError):
                    size_bytes += f.stat().st_size
        return {'count': count, 'size_bytes': size_bytes}
