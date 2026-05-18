"""Embedding service for skill clustering."""

import time
import random
import logging
from typing import List, Optional

import numpy as np
import requests

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Embedding service for skill text.

    Supports vLLM and other OpenAI-compatible embedding backends.
    """

    def __init__(
        self,
        model: str = "Qwen3-Embedding-8B",
        base_url: str = "http://127.0.0.1:7000",
        api_key: str = "",
        batch_size: int = 32,
        timeout: int = 120,
        max_retries: int = 5
    ):
        """
        Initialize embedding service.

        Args:
            model: Embedding model name
            base_url: vLLM server URL
            api_key: Optional API key
            batch_size: Batch size for embedding
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.batch_size = batch_size
        self.timeout = timeout
        self.max_retries = max_retries

    def embed_sync(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts (synchronous).

        Args:
            texts: List of text strings

        Returns:
            Numpy array of embeddings (n_samples, n_features), L2-normalized
        """
        vecs = []

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for i in range(0, len(texts), self.batch_size):
            chunk = texts[i:i + self.batch_size]

            for attempt in range(self.max_retries + 1):
                try:
                    r = requests.post(
                        f"{self.base_url}/v1/embeddings",
                        headers=headers,
                        json={"model": self.model, "input": chunk},
                        timeout=self.timeout,
                    )
                    r.raise_for_status()
                    data = sorted(r.json()["data"], key=lambda x: x["index"])
                    vecs.extend([d["embedding"] for d in data])
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        logger.error(f"Embedding failed after {self.max_retries} retries: {e}")
                        raise

                    sleep_time = min(10.0, 0.5 * (2 ** attempt) + random.uniform(0, 0.2))
                    logger.warning(f"Embedding attempt {attempt + 1} failed, retrying in {sleep_time:.1f}s: {e}")
                    time.sleep(sleep_time)

        X = np.array(vecs, dtype=np.float32)
        X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
        return X

    async def embed(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts (async wrapper).

        Args:
            texts: List of text strings

        Returns:
            Numpy array of embeddings (n_samples, n_features)
        """
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.embed_sync, texts)

    async def embed_batch(
        self,
        texts: List[str],
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for large batches with progress.

        Args:
            texts: List of text strings
            show_progress: Whether to show progress

        Returns:
            Numpy array of embeddings
        """
        if show_progress:
            logger.info(f"Embedding {len(texts)} texts...")

        embeddings = await self.embed(texts)

        if show_progress:
            logger.info(f"Embedding complete: {embeddings.shape}")

        return embeddings

    def embed_skills(self, skills: List[dict]) -> np.ndarray:
        """
        Generate embeddings for skill dictionaries.

        Uses 'embedding_text' field if present, otherwise constructs from skill fields.

        Args:
            skills: List of skill dictionaries

        Returns:
            Numpy array of embeddings
        """
        texts = []
        for skill in skills:
            if "embedding_text" in skill:
                texts.append(skill["embedding_text"])
            else:
                skill_data = skill.get("skill", skill)
                text = f"{skill_data.get('name', '')}\n{skill_data.get('document', '')}\n{skill_data.get('content', '')}"
                texts.append(text)

        return self.embed_sync(texts)
