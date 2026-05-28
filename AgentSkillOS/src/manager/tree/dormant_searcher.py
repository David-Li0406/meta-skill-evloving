"""Dormant skill vector searcher using ChromaDB."""

from pathlib import Path
from typing import Callable, Optional

import chromadb
import litellm
from loguru import logger

from cache import ensure_cache
from config import get_config, PROJECT_ROOT


class DormantVectorSearcher:
    """
    Dormant skill vector searcher.

    Uses ChromaDB for efficient semantic similarity search,
    supporting 100k+ skills with fast retrieval.
    """

    COLLECTION_NAME = "dormant_skills"

    def __init__(
        self,
        vector_db_path: Optional[Path] = None,
        event_callback: Optional[Callable] = None,
    ):
        cfg = get_config()

        # Vector DB path
        if vector_db_path:
            self._db_path = str(vector_db_path)
        else:
            self._db_path = str(PROJECT_ROOT / "data" / "vector_stores" / "dormant")

        # Embedding configuration
        self._model = cfg.embedding_model
        self._api_key = cfg.embedding_api_key
        self._base_url = cfg.embedding_base_url
        mcfg = cfg.manager_config("tree")
        self._caching = mcfg.build.caching if mcfg else True

        # Validate API configuration
        if not self._api_key:
            raise ValueError(
                "EMBEDDING_API_KEY not configured. "
                "Please set it in .env file for dormant skill search."
            )

        self._event_callback = event_callback
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection: Optional[chromadb.Collection] = None
        ensure_cache()

    def _ensure_collection(self) -> None:
        """Ensure collection is loaded."""
        if self._collection is not None:
            return

        self._client = chromadb.PersistentClient(path=self._db_path)

        # Check if collection exists
        existing = [c.name for c in self._client.list_collections()]
        if self.COLLECTION_NAME not in existing:
            raise RuntimeError(
                f"Dormant index not found. "
                f"Run 'python src/cli.py build' with layering enabled first."
            )

        self._collection = self._client.get_collection(self.COLLECTION_NAME)

    def _embed_query(self, text: str) -> list[float]:
        """Embed query text."""
        kwargs = {
            "model": self._model,
            "input": [text],
            "encoding_format": "float",
            "drop_params": True,
            "num_retries": 3,
            "timeout": 600,
            "caching": self._caching,
        }
        if self._api_key:
            kwargs["api_key"] = self._api_key
        if self._base_url:
            kwargs["api_base"] = self._base_url

        try:
            response = litellm.embedding(**kwargs)
            return response.data[0]["embedding"]
        except Exception as e:
            logger.warning(f"Embedding query failed: {e}")
            raise

    def search(
        self,
        query: str,
        max_results: int = 10,
        exclude_ids: Optional[set[str]] = None,
    ) -> list[dict]:
        """
        Search for similar dormant skills.

        Args:
            query: Search query
            max_results: Maximum number of results to return
            exclude_ids: Set of skill IDs to exclude

        Returns:
            List of matching dormant skill dicts
        """
        self._ensure_collection()
        exclude_ids = exclude_ids or set()

        # Request extra results to compensate for excluded IDs
        n_results = max_results + len(exclude_ids) + 5

        # Embed query
        query_embedding = self._embed_query(query)

        # ChromaDB search
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self._collection.count()),
            include=["metadatas", "distances"],
        )

        # Process results
        skills = []
        ids = results["ids"][0] if results["ids"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []

        for i, skill_id in enumerate(ids):
            if skill_id in exclude_ids:
                continue

            meta = metadatas[i] if i < len(metadatas) else {}
            distance = distances[i] if i < len(distances) else 0.0

            # Convert L2 distance to similarity score
            similarity = 1.0 / (1.0 + distance)

            skills.append({
                "id": skill_id,
                "name": meta.get("name", skill_id),
                "description": meta.get("description", ""),
                "skill_path": meta.get("skill_path", ""),
                "github_url": meta.get("github_url", ""),
                "stars": meta.get("stars", 0),
                "is_official": meta.get("is_official", False),
                "author": meta.get("author", ""),
                "installs_count": meta.get("installs_count", 0),
                "similarity": round(similarity, 4),
                "is_dormant_suggestion": True,
            })

            if len(skills) >= max_results:
                break

        logger.info(f"Dormant vector search: query='{query[:50]}...', found {len(skills)} results")
        return skills

    def is_available(self) -> bool:
        """Check if index is available."""
        try:
            self._ensure_collection()
            return True
        except Exception:
            return False
