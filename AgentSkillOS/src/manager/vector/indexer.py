"""Vector indexer — scan skills, generate embeddings, store in ChromaDB."""

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

import chromadb
import litellm
from loguru import logger

from cache import ensure_cache
from config import get_config
from constants import EventCallback
from manager.tree.skill_scanner import SkillScanner


class VectorIndexer:
    """Builds a ChromaDB vector index from scanned skills."""

    def __init__(
        self,
        skills_dir: Optional[str] = None,
        vector_db_path: Optional[str] = None,
        collection_name: str = "skills",
        event_callback: Optional[EventCallback] = None,
    ):
        cfg = get_config()
        self._skills_dir = skills_dir
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
        self._batch_size = mcfg.build.batch_size if mcfg else cfg.embedding_batch_size
        self._max_workers = mcfg.build.max_workers if mcfg else 4
        self._caching = mcfg.build.caching if mcfg else True
        ensure_cache()

    def _emit(self, event_type: str, data: dict) -> None:
        if self._event_callback:
            self._event_callback(event_type, data)

    def _make_document(self, skill: dict) -> str:
        """Concatenate skill name + description as the embedding document."""
        parts = [skill.get("name", ""), skill.get("description", "")]
        return "\n\n".join(p for p in parts if p)

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Call litellm.embedding for a batch of texts."""
        kwargs = {"model": self._model, "input": texts, "encoding_format": "float",
                  "drop_params": True, "num_retries": 3, "timeout": 600, "caching": self._caching}
        if self._api_key:
            kwargs["api_key"] = self._api_key
        if self._base_url:
            kwargs["api_base"] = self._base_url

        try:
            response = litellm.embedding(**kwargs)
            return [item["embedding"] for item in response.data]
        except Exception as e:
            logger.warning(f"Embedding batch failed: {e}")
            raise

    def build(self) -> dict:
        """Scan skills, embed, and upsert into ChromaDB.

        Returns:
            dict with collection info and skill count.
        """
        scanner = SkillScanner(self._skills_dir)
        skills = scanner.to_dict_list()
        total = len(skills)

        self._emit("build_start", {"total_skills": total, "db_path": self._db_path})
        logger.info(f"Vector indexer: {total} skills to embed, db_path={self._db_path}")

        client = chromadb.PersistentClient(path=self._db_path)

        # Check cache: if collection exists with same skill count and caching enabled
        existing_collections = [c.name for c in client.list_collections()]
        if self._caching and self._collection_name in existing_collections:
            collection = client.get_collection(self._collection_name)
            if collection.count() == total:
                # Verify content hash to detect changes
                cache_hash = self._compute_skills_hash(skills)
                existing_meta = collection.metadata or {}
                if existing_meta.get("skills_hash") == cache_hash:
                    logger.info("Vector index cache hit — skipping rebuild")
                    self._emit("build_complete", {
                        "total_skills": total,
                        "cached": True,
                    })
                    return {
                        "collection": self._collection_name,
                        "total_skills": total,
                        "cached": True,
                    }

        # Delete and recreate collection
        if self._collection_name in existing_collections:
            client.delete_collection(self._collection_name)

        skills_hash = self._compute_skills_hash(skills)
        collection = client.create_collection(
            name=self._collection_name,
            metadata={"skills_hash": skills_hash},
        )

        # Parallel embed and upsert
        batches = []
        for i in range(0, total, self._batch_size):
            batch = skills[i : i + self._batch_size]
            documents = [self._make_document(s) for s in batch]
            ids = [s["id"] for s in batch]
            metadatas = [
                {
                    "name": s.get("name", ""),
                    "description": s.get("description", ""),
                    "skill_path": s.get("skill_path", ""),
                    "github_url": s.get("github_url", ""),
                    "stars": s.get("stars", 0),
                    "is_official": s.get("is_official", False),
                    "author": s.get("author", ""),
                }
                for s in batch
            ]
            batches.append((ids, documents, metadatas))

        embedded_count = 0
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {
                executor.submit(self._embed_batch, docs): (ids, docs, metas)
                for ids, docs, metas in batches
            }
            for future in as_completed(futures):
                ids, documents, metadatas = futures[future]
                try:
                    embeddings = future.result()
                except Exception as e:
                    logger.error(f"Embedding batch failed, skipping: {e}")
                    continue
                collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                )
                embedded_count += len(ids)
                self._emit("build_progress", {
                    "embedded": embedded_count,
                    "total": total,
                })
                logger.debug(f"Embedded {embedded_count}/{total} skills")

        self._emit("build_complete", {"total_skills": total, "cached": False})
        logger.info(f"Vector index built: {total} skills in collection '{self._collection_name}'")

        return {
            "collection": self._collection_name,
            "total_skills": total,
            "cached": False,
        }

    def _compute_skills_hash(self, skills: list[dict]) -> str:
        """Compute a hash of all skill IDs + content for cache validation."""
        data = json.dumps(
            [(s["id"], s.get("content", "")[:200]) for s in skills],
            sort_keys=True,
        )
        return hashlib.sha256(data.encode()).hexdigest()[:16]
