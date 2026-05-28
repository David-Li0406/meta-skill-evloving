"""Vector searcher — query ChromaDB for top-k similar skills."""

from pathlib import Path
from typing import Optional

import chromadb
import litellm
from loguru import logger

from cache import ensure_cache
from config import get_config
from constants import EventCallback


class VectorSearcher:
    """Loads a ChromaDB collection and performs similarity search."""

    def __init__(
        self,
        vector_db_path: Optional[str] = None,
        collection_name: str = "skills",
        event_callback: Optional[EventCallback] = None,
    ):
        cfg = get_config()
        self._collection_name = collection_name
        self._event_callback = event_callback

        if vector_db_path:
            self._db_path = str(Path(vector_db_path))
        else:
            from config import PROJECT_ROOT
            self._db_path = str(PROJECT_ROOT / cfg.chroma_persist_dir)

        self._model = cfg.embedding_model
        self._api_key = cfg.embedding_api_key
        self._base_url = cfg.embedding_base_url
        mcfg = cfg.manager_config("vector")
        self._caching = mcfg.build.caching if mcfg else True

        self._client = None
        self._collection = None
        ensure_cache()

    def _emit(self, event_type: str, data: dict) -> None:
        if self._event_callback:
            self._event_callback(event_type, data)

    def _ensure_collection(self) -> None:
        if self._collection is not None:
            return
        self._client = chromadb.PersistentClient(path=self._db_path)
        self._collection = self._client.get_collection(name=self._collection_name)

    def _embed_query(self, text: str) -> list[float]:
        """Embed a single query string."""
        kwargs = {"model": self._model, "input": [text], "encoding_format": "float",
                  "drop_params": True, "num_retries": 3, "timeout": 600, "caching": self._caching}
        if self._api_key:
            kwargs["api_key"] = self._api_key
        if self._base_url:
            kwargs["api_base"] = self._base_url

        response = litellm.embedding(**kwargs)
        return response.data[0]["embedding"]

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """Search for the top-k most similar skills.

        Args:
            query: Natural language query
            top_k: Number of results to return

        Returns:
            List of skill dicts with similarity scores.
        """
        self._ensure_collection()

        total_skills = self._collection.count()
        self._emit("search_start", {"query": query, "top_k": top_k, "total_skills": total_skills})

        self._emit("embedding_query", {"query": query})
        query_embedding = self._embed_query(query)
        self._emit("query_embedded", {"query": query})

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, total_skills),
            include=["metadatas", "distances", "documents"],
        )

        skills = []
        ids = results["ids"][0] if results["ids"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []
        documents = results["documents"][0] if results["documents"] else []

        for i, skill_id in enumerate(ids):
            meta = metadatas[i] if i < len(metadatas) else {}
            distance = distances[i] if i < len(distances) else 0.0
            # ChromaDB returns L2 distance by default; convert to a similarity score
            similarity = 1.0 / (1.0 + distance)

            skills.append({
                "id": skill_id,
                "name": meta.get("name", skill_id),
                "description": meta.get("description", ""),
                "skill_path": meta.get("skill_path", ""),
                "content": documents[i] if i < len(documents) else "",
                "github_url": meta.get("github_url", ""),
                "stars": meta.get("stars", 0),
                "is_official": meta.get("is_official", False),
                "author": meta.get("author", ""),
                "similarity": round(similarity, 4),
                "distance": round(distance, 4),
            })

        self._emit("search_complete", {
            "query": query,
            "result_count": len(skills),
            "skills": [{"id": s["id"], "name": s["name"], "similarity": s["similarity"]} for s in skills],
        })

        logger.info(f"Vector search: query='{query[:50]}...', found {len(skills)} results")
        return skills
