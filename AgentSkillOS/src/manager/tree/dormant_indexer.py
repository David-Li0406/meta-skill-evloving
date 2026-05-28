"""Builder for dormant skill vector index."""

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Optional

import chromadb
import litellm
import yaml
from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from cache import ensure_cache
from config import get_config, PROJECT_ROOT


class DormantIndexBuilder:
    """
    Build vector index for dormant skills.

    Reads skill data from dormant_index.yaml,
    generates embeddings, and stores in ChromaDB.
    """

    COLLECTION_NAME = "dormant_skills"

    def __init__(
        self,
        dormant_index_path: Optional[Path] = None,
        vector_db_path: Optional[Path] = None,
        event_callback: Optional[Callable] = None,
    ):
        cfg = get_config()

        # Path configuration
        default_tree_dir = PROJECT_ROOT / "data" / "capability_trees"
        self._index_path = dormant_index_path or (default_tree_dir / "dormant_index.yaml")
        self._db_path = vector_db_path or (PROJECT_ROOT / "data" / "vector_stores" / "dormant")

        # Embedding configuration
        self._model = cfg.embedding_model
        self._api_key = cfg.embedding_api_key
        self._base_url = cfg.embedding_base_url

        # Validate API configuration
        if not self._api_key:
            raise ValueError(
                "EMBEDDING_API_KEY not configured. "
                "Please set it in .env file."
            )

        # Build configuration (reuse tree manager's build settings if available)
        mcfg = cfg.manager_config("tree")
        if mcfg and hasattr(mcfg, "build"):
            self._batch_size = getattr(mcfg.build, "batch_size", 100)
            self._max_workers = getattr(mcfg.build, "max_workers", 4)
            self._caching = getattr(mcfg.build, "caching", True)
        else:
            self._batch_size = 100
            self._max_workers = 4
            self._caching = True

        self._event_callback = event_callback
        ensure_cache()

    def _load_dormant_skills(self) -> list[dict]:
        """Load dormant skill data."""
        if not self._index_path.exists():
            raise FileNotFoundError(
                f"Dormant index not found: {self._index_path}. "
                f"Run 'python src/cli.py build --layered' first."
            )

        with open(self._index_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return data.get("skills", [])

    def _make_document(self, skill: dict) -> str:
        """Build embedding document."""
        parts = [skill.get("name", ""), skill.get("description", "")]
        return "\n\n".join(p for p in parts if p)

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Batch embedding."""
        kwargs = {
            "model": self._model,
            "input": texts,
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
            return [item["embedding"] for item in response.data]
        except Exception as e:
            logger.warning(f"Embedding batch failed: {e}")
            raise

    def _compute_hash(self, skills: list[dict]) -> str:
        """Compute hash of skill list."""
        data = json.dumps(
            [(s["id"], s.get("description", "")[:100]) for s in skills],
            sort_keys=True,
        )
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def build(self) -> dict:
        """
        Build dormant skill vector index.

        Returns:
            Build result info dict
        """
        # Load skills
        skills = self._load_dormant_skills()
        total = len(skills)
        logger.info(f"Building dormant vector index: {total} skills")

        # Ensure directory exists
        Path(self._db_path).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB
        client = chromadb.PersistentClient(path=str(self._db_path))

        # Check cache
        existing = [c.name for c in client.list_collections()]
        if self._caching and self.COLLECTION_NAME in existing:
            collection = client.get_collection(self.COLLECTION_NAME)
            if collection.count() == total:
                cache_hash = self._compute_hash(skills)
                existing_meta = collection.metadata or {}
                if existing_meta.get("skills_hash") == cache_hash:
                    logger.info("Dormant index cache hit - skipping rebuild")
                    return {
                        "collection": self.COLLECTION_NAME,
                        "total_skills": total,
                        "cached": True,
                    }

        # Delete old collection
        if self.COLLECTION_NAME in existing:
            client.delete_collection(self.COLLECTION_NAME)

        # Create new collection
        skills_hash = self._compute_hash(skills)
        collection = client.create_collection(
            name=self.COLLECTION_NAME,
            metadata={"skills_hash": skills_hash, "skills_count": total},
        )

        # Prepare batches
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
                    "installs_count": s.get("installs_count", 0),
                }
                for s in batch
            ]
            batches.append((ids, documents, metadatas))

        # Parallel embedding
        embedded_count = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task(f"Embedding {total} dormant skills...", total=total)

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
                    progress.update(task, completed=embedded_count)

        logger.info(f"Dormant vector index built: {total} skills")
        return {
            "collection": self.COLLECTION_NAME,
            "total_skills": total,
            "cached": False,
        }
