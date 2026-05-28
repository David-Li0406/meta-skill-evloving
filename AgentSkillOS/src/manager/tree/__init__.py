"""Tree manager: LLM recursive tree build + multi-level tree search.

Uses a capability tree structure for intelligent skill selection.
LLM-based multi-level search for handling fuzzy queries.
Supports active/dormant skill layering strategy.
"""
from typing import Optional
from ..base import RetrievalResult, EventCallback
from ..registry import register_manager

from .builder import TreeBuilder, build_tree
from .models import TreeNode, Skill, DynamicTreeConfig, SkillStatus
from .searcher import Searcher, SearchResult, search
from .layered_searcher import LayeredSearcher, LayeredSearchResult, create_searcher, layered_files_exist
from .layer_processor import LayerPostProcessor, LayeredOutput, process_tree_layering, build_dormant_index_from_directory
from .user_prefs import UserPreferences, UserPrefsManager, load_user_prefs, save_user_prefs
from .scheduled_updater import ScheduledUpdater, UpdateResult, run_update
from .dormant_searcher import DormantVectorSearcher
from .dormant_indexer import DormantIndexBuilder

__all__ = [
    # Manager
    "TreeManager",
    # Tree
    "TreeBuilder",
    "build_tree",
    "TreeNode",
    "Skill",
    "DynamicTreeConfig",
    "SkillStatus",
    # Search
    "Searcher",
    "SearchResult",
    "search",
    # Layered Search
    "LayeredSearcher",
    "LayeredSearchResult",
    "create_searcher",
    "layered_files_exist",
    # Layer Processing
    "LayerPostProcessor",
    "LayeredOutput",
    "process_tree_layering",
    "build_dormant_index_from_directory",
    # User Preferences
    "UserPreferences",
    "UserPrefsManager",
    "load_user_prefs",
    "save_user_prefs",
    # Scheduled Updates
    "ScheduledUpdater",
    "UpdateResult",
    "run_update",
    # Dormant Vector Search
    "DormantVectorSearcher",
    "DormantIndexBuilder",
]


UI_CONTRIBUTION = {
    "id": "tree",
    "partials": {
        "search": "modules/manager_tree/tree-search.html",
        "review": "modules/manager_tree/skill-review.html",
    },
    "scripts": [
        "modules/manager_tree/tree-search.js",
        "modules/manager_tree/skill-review.js",
    ],
    "modals": [
        "modules/manager_tree/tree-browser-modal.html",
        "modules/manager_tree/skill-detail-modal.html",
    ],
}


@register_manager("tree")
class TreeManager:
    """Wraps TreeBuilder + Searcher into unified Manager interface.

    Supports optional layered search (active/dormant strategy) when enabled
    in config.yaml. The layering is transparent - same search interface.
    """

    ui_contribution = UI_CONTRIBUTION

    @property
    def visual_type(self) -> str:
        return "tree"

    def __init__(
        self,
        tree_path: Optional[str] = None,
        event_callback: Optional[EventCallback] = None,
        **kwargs,
    ):
        self._tree_path = tree_path
        self._event_callback = event_callback
        self._kwargs = kwargs
        self._searcher = None  # Lazy creation
        self._is_layered = False  # Track if using layered searcher

    def build(
        self,
        skills_dir: Optional[str] = None,
        output_path: Optional[str] = None,
        verbose: bool = False,
        show_tree: bool = True,
        generate_html: bool = True,
    ) -> dict:
        from .builder import TreeBuilder

        builder_keys = ("config", "model", "api_key", "base_url", "max_workers")
        builder_kwargs = {k: v for k, v in self._kwargs.items() if k in builder_keys}

        builder = TreeBuilder(
            skills_dir=skills_dir,
            output_path=output_path,
            **builder_kwargs,
        )
        return builder.build(
            verbose=verbose,
            show_tree=show_tree,
            generate_html=generate_html,
        )

    def search(self, query: str, verbose: bool = False) -> RetrievalResult:
        if self._searcher is None:
            self._init_searcher()

        result = self._searcher.search(query, verbose=verbose)

        # Build metadata based on searcher type
        metadata = {
            "llm_calls": result.llm_calls,
            "parallel_rounds": result.parallel_rounds,
            "explored_nodes": result.explored_nodes,
            "selected_paths": result.selected_paths,
        }

        # Add layered search metadata if applicable
        if self._is_layered and hasattr(result, "dormant_suggestions"):
            metadata["dormant_suggestions"] = result.dormant_suggestions
            metadata["dormant_search_performed"] = getattr(result, "dormant_search_performed", False)

        return RetrievalResult(
            query=result.query,
            selected_skills=result.selected_skills,
            metadata=metadata,
        )

    def get_visual_data(self) -> Optional[dict]:
        if self._searcher is None:
            self._init_searcher()
        return self._searcher.get_tree_data()

    def _init_searcher(self):
        from .layered_searcher import create_searcher
        from pathlib import Path

        searcher_keys = ("config", "model", "api_key", "base_url", "max_parallel", "prune")
        searcher_kwargs = {k: v for k, v in self._kwargs.items() if k in searcher_keys}

        tree_path = Path(self._tree_path) if self._tree_path else None

        # Use factory function that selects appropriate searcher
        self._searcher = create_searcher(
            tree_path=tree_path,
            event_callback=self._event_callback,
            **searcher_kwargs,
        )

        # Track if we're using the layered searcher
        self._is_layered = isinstance(self._searcher, LayeredSearcher)
