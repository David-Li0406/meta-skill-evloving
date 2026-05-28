"""Recipe data model and storage for the web UI.

Recipes capture successful skill combinations for reuse.
"""

import json
import math
import threading
import uuid
from dataclasses import dataclass, asdict, fields
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Recipe:
    """A saved recipe representing a reusable skill combination."""
    id: str
    name: str
    description: str
    original_prompt: str
    skill_ids: list[str]
    dag_plan: dict
    skill_group_id: str
    created_at: str
    usage_count: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "Recipe":
        """Create a Recipe from a dict, ignoring unknown fields."""
        known = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)


class RecipeStore:
    """Persistent storage for recipes using JSON file."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._recipes: dict[str, Recipe] = {}
        self._lock = threading.Lock()
        self._load()

    def _load(self) -> None:
        """Load recipes from disk."""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                for r in data.get("recipes", []):
                    self._recipes[r["id"]] = Recipe.from_dict(r)
            except (json.JSONDecodeError, KeyError) as e:
                from loguru import logger
                logger.warning(f"Failed to load recipes: {e}")

    def _save(self) -> None:
        """Persist recipes to disk atomically."""
        data = {"recipes": [asdict(r) for r in self._recipes.values()]}
        temp_path = self.storage_path.with_suffix(".json.tmp")
        temp_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temp_path.replace(self.storage_path)

    def create(
        self,
        name: str,
        description: str,
        original_prompt: str,
        skill_ids: list[str],
        dag_plan: dict,
        skill_group_id: str,
    ) -> Recipe:
        """Create and persist a new recipe."""
        recipe = Recipe(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            original_prompt=original_prompt,
            skill_ids=skill_ids,
            dag_plan=dag_plan,
            skill_group_id=skill_group_id,
            created_at=datetime.now().isoformat(),
        )
        with self._lock:
            self._recipes[recipe.id] = recipe
            self._save()
        return recipe

    def list_all(self) -> list[Recipe]:
        """Get all recipes."""
        return list(self._recipes.values())

    def get(self, recipe_id: str) -> Optional[Recipe]:
        """Get a recipe by ID."""
        return self._recipes.get(recipe_id)

    def increment_usage(self, recipe_id: str) -> None:
        """Increment usage count for a recipe."""
        with self._lock:
            if recipe_id in self._recipes:
                self._recipes[recipe_id].usage_count += 1
                self._save()

    def delete(self, recipe_id: str) -> bool:
        """Delete a recipe by ID. Returns True if found and deleted."""
        with self._lock:
            if recipe_id in self._recipes:
                del self._recipes[recipe_id]
                self._save()
                return True
            return False


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class RecipeRecommender:
    """Embedding-based recipe recommender for fast semantic matching.

    Uses cosine similarity on embeddings instead of LLM calls,
    providing near-instant (<100ms) recommendations.
    """

    def __init__(self, store: RecipeStore):
        self._store = store
        self._embeddings: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def _embed(self, text: str) -> list[float]:
        """Embed a single text string."""
        import litellm
        from cache import ensure_cache
        from config import get_config
        from loguru import logger

        ensure_cache()
        cfg = get_config()
        kwargs = {
            "model": cfg.embedding_model,
            "input": [text],
            "encoding_format": "float",
            "drop_params": True,
            "num_retries": 3,
            "timeout": 600,
            "caching": True,
        }
        if cfg.embedding_api_key:
            kwargs["api_key"] = cfg.embedding_api_key
        if cfg.embedding_base_url:
            kwargs["api_base"] = cfg.embedding_base_url

        try:
            response = litellm.embedding(**kwargs)
            return response.data[0]["embedding"]
        except Exception as e:
            logger.warning(f"Embedding failed: {e}")
            raise

    def _ensure_embeddings(self) -> None:
        """Ensure all recipes have cached embeddings."""
        recipes = self._store.list_all()
        missing = [r for r in recipes if r.id not in self._embeddings]
        if not missing:
            return

        # Batch embed missing recipes
        import litellm
        from cache import ensure_cache
        from config import get_config
        from loguru import logger

        ensure_cache()
        cfg = get_config()
        texts = [f"{r.name}: {r.description}" for r in missing]

        kwargs = {
            "model": cfg.embedding_model,
            "input": texts,
            "encoding_format": "float",
            "drop_params": True,
            "num_retries": 3,
            "timeout": 600,
            "caching": True,
        }
        if cfg.embedding_api_key:
            kwargs["api_key"] = cfg.embedding_api_key
        if cfg.embedding_base_url:
            kwargs["api_base"] = cfg.embedding_base_url

        try:
            response = litellm.embedding(**kwargs)
            for recipe, item in zip(missing, response.data):
                self._embeddings[recipe.id] = item["embedding"]
        except Exception as e:
            logger.warning(f"Batch embedding failed ({len(missing)} recipes): {e}")
            # Don't crash the recommender, just leave embeddings missing

    def invalidate(self, recipe_id: str) -> None:
        """Remove cached embedding for a deleted recipe."""
        with self._lock:
            self._embeddings.pop(recipe_id, None)

    def recommend(self, query: str, top_k: int = 5) -> list[Recipe]:
        """Recommend recipes by embedding similarity.

        Args:
            query: User task description
            top_k: Maximum number of recommendations

        Returns:
            List of Recipe objects sorted by relevance (most relevant first).
        """
        with self._lock:
            self._ensure_embeddings()

            if not self._embeddings:
                return []

            query_emb = self._embed(query)
            scores = [
                (rid, _cosine_similarity(query_emb, emb))
                for rid, emb in self._embeddings.items()
            ]
            scores.sort(key=lambda x: x[1], reverse=True)

            results = []
            for rid, score in scores[:top_k]:
                recipe = self._store.get(rid)
                if recipe and score > 0.3:  # Minimum similarity threshold
                    results.append(recipe)
            return results
