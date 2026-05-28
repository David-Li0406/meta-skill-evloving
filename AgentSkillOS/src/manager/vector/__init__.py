"""Vector manager: ChromaDB-based vector similarity skill retrieval.

Uses embedding models to encode skills and queries, then performs
top-k similarity search via ChromaDB for skill selection.
"""
from typing import Optional

from ..base import RetrievalResult, EventCallback
from ..registry import register_manager

__all__ = ["VectorManager"]

UI_CONTRIBUTION = {
    "id": "vector",
    "partials": {
        "search": "modules/manager_vector/vector-search.html",
        "review": "modules/manager_vector/skill-review.html",
    },
    "scripts": [
        "modules/manager_vector/vector-search.js",
        "modules/manager_vector/skill-review.js",
    ],
    "modals": [
        "modules/manager_vector/skill-detail-modal.html",
    ],
}


@register_manager("vector")
class VectorManager:
    """Wraps VectorIndexer + VectorSearcher into unified Manager interface."""

    ui_contribution = UI_CONTRIBUTION

    @property
    def visual_type(self) -> str:
        return "list"

    def __init__(
        self,
        vector_db_path: Optional[str] = None,
        event_callback: Optional[EventCallback] = None,
        **kwargs,
    ):
        self._vector_db_path = vector_db_path
        self._event_callback = event_callback
        self._kwargs = kwargs

    def build(
        self,
        skills_dir: Optional[str] = None,
        output_path: Optional[str] = None,
        verbose: bool = False,
        show_tree: bool = True,
        generate_html: bool = True,
    ) -> dict:
        from .indexer import VectorIndexer
        from config import get_config

        cfg = get_config()
        mcfg = cfg.manager_config("vector")
        collection_name = mcfg.collection_name if mcfg else "skills"

        indexer = VectorIndexer(
            skills_dir=skills_dir,
            vector_db_path=self._vector_db_path,
            collection_name=collection_name,
            event_callback=self._event_callback,
        )
        return indexer.build()

    def search(self, query: str, verbose: bool = False) -> RetrievalResult:
        from .searcher import VectorSearcher
        from config import get_config

        cfg = get_config()
        mcfg = cfg.manager_config("vector")
        top_k = mcfg.top_k if mcfg else 10
        collection_name = mcfg.collection_name if mcfg else "skills"

        searcher = VectorSearcher(
            vector_db_path=self._vector_db_path,
            collection_name=collection_name,
            event_callback=self._event_callback,
        )
        skills = searcher.search(query, top_k=top_k)

        return RetrievalResult(
            query=query,
            selected_skills=skills,
            metadata={
                "top_k": top_k,
                "result_count": len(skills),
                "similarities": {s["id"]: s.get("similarity", 0) for s in skills},
            },
        )

    def get_visual_data(self) -> Optional[dict]:
        return None
