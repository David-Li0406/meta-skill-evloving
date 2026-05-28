"""
Layered Searcher - Extends Searcher with active/dormant skill support.

Searches the active tree first, then always suggests dormant skills
to provide users with additional options beyond the active tree results.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console

from config import PROJECT_ROOT, get_config, LayeringConfig
from constants import EventCallback
from .searcher import Searcher, SearchResult
from .user_prefs import load_user_prefs, UserPreferences
from .dormant_searcher import DormantVectorSearcher


console = Console()


@dataclass
class LayeredSearchResult:
    """Result from layered search (active + dormant suggestions)."""
    query: str
    selected_skills: list[dict]  # From active tree search
    dormant_suggestions: list[dict] = field(default_factory=list)  # Suggested dormant skills

    # Search metadata
    llm_calls: int = 0
    parallel_rounds: int = 0
    explored_nodes: list[str] = field(default_factory=list)
    selected_paths: list[str] = field(default_factory=list)

    # Layering metadata
    active_tree_used: bool = True
    dormant_search_performed: bool = False


class DormantIndexLoader:
    """Loader and searcher for dormant skills index."""

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self._skills: list[dict] = []
        self._loaded = False

    def _load(self) -> None:
        """Lazy load the dormant index."""
        if self._loaded:
            return

        if not self.index_path.exists():
            self._loaded = True
            return

        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self._skills = data.get("skills", [])
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to load dormant index: {e}[/yellow]")
            self._skills = []

        self._loaded = True

    def search_keyword(self, query: str, limit: int = 10, exclude_ids: Optional[set[str]] = None) -> list[dict]:
        """
        Search dormant skills by keyword matching.

        Args:
            query: Search query
            limit: Maximum results to return
            exclude_ids: Skill IDs to exclude from results

        Returns:
            List of matching dormant skill dicts.
        """
        self._load()
        exclude_ids = exclude_ids or set()

        # Simple keyword matching: split query into terms and match against name/description
        query_lower = query.lower()
        terms = set(re.findall(r'\w+', query_lower))

        results = []
        for skill in self._skills:
            if skill.get("id") in exclude_ids:
                continue

            # Score based on term matches
            name_lower = skill.get("name", "").lower()
            desc_lower = skill.get("description", "").lower()
            text = f"{name_lower} {desc_lower}"

            score = 0
            for term in terms:
                if term in text:
                    # Higher score for name matches
                    if term in name_lower:
                        score += 3
                    else:
                        score += 1

            if score > 0:
                results.append({
                    **skill,
                    "_search_score": score,
                })

        # Sort by score (descending), then by installs (descending)
        results.sort(key=lambda s: (s.get("_search_score", 0), s.get("installs_count", 0)), reverse=True)

        # Remove score field and limit
        return [{k: v for k, v in s.items() if not k.startswith("_")} for s in results[:limit]]

    def get_top_by_installs(self, limit: int = 10, exclude_ids: Optional[set[str]] = None) -> list[dict]:
        """Get top dormant skills by install count."""
        self._load()
        exclude_ids = exclude_ids or set()

        # Filter and sort
        filtered = [s for s in self._skills if s.get("id") not in exclude_ids]
        filtered.sort(key=lambda s: s.get("installs_count", 0), reverse=True)

        return filtered[:limit]

    @property
    def skills(self) -> list[dict]:
        """Get all dormant skills."""
        self._load()
        return self._skills


class LayeredSearcher:
    """
    Layered skill searcher with active/dormant support.

    Wraps the original Searcher and adds dormant skill suggestions.
    The original Searcher is completely unchanged.
    """

    def __init__(
        self,
        active_tree_path: Optional[Path] = None,
        dormant_index_path: Optional[Path] = None,
        config: Optional[LayeringConfig] = None,
        user_prefs: Optional[UserPreferences] = None,
        event_callback: Optional[EventCallback] = None,
        **searcher_kwargs,
    ):
        cfg = get_config()
        self.config = config or cfg.layering_config()
        self.user_prefs = user_prefs or load_user_prefs()
        self.event_callback = event_callback
        self._searcher_kwargs = searcher_kwargs

        # Determine paths
        default_dir = PROJECT_ROOT / "data" / "capability_trees"
        self.active_tree_path = active_tree_path or (default_dir / "active_tree.yaml")
        self.dormant_index_path = dormant_index_path or (default_dir / "dormant_index.yaml")

        # Base searcher for active tree
        self._base_searcher: Optional[Searcher] = None

        # Dormant vector searcher (lazy loaded)
        self._dormant_vector_searcher: Optional[DormantVectorSearcher] = None
        self._dormant_vector_unavailable: bool = False

        # Fallback keyword-based index (used when vector search unavailable)
        self._dormant_index: Optional[DormantIndexLoader] = None

    def search(
        self,
        query: str,
        verbose: bool = False,
        include_dormant: bool = True,
    ) -> LayeredSearchResult:
        """
        Execute layered search.

        Args:
            query: User's task description
            verbose: Print detailed search process
            include_dormant: Whether to include dormant skill suggestions

        Returns:
            LayeredSearchResult with selected skills and dormant suggestions.
        """
        # Initialize base searcher if needed
        if self._base_searcher is None:
            self._base_searcher = Searcher(
                tree_path=self.active_tree_path,
                event_callback=self.event_callback,
                **self._searcher_kwargs,
            )

        # Search active tree
        active_result = self._base_searcher.search(query, verbose=verbose)

        # Emit layered search event
        self._emit_event("layered_search_active_complete", {
            "query": query,
            "active_skills_count": len(active_result.selected_skills),
            "llm_calls": active_result.llm_calls,
        })

        # Initialize result
        result = LayeredSearchResult(
            query=query,
            selected_skills=active_result.selected_skills,
            llm_calls=active_result.llm_calls,
            parallel_rounds=active_result.parallel_rounds,
            explored_nodes=active_result.explored_nodes,
            selected_paths=active_result.selected_paths,
            active_tree_used=True,
        )

        # Always search dormant skills for additional suggestions
        if include_dormant:
            dormant_suggestions = self._search_dormant(
                query,
                max_results=self.config.max_dormant_suggestions,
                exclude_ids={s["id"] for s in active_result.selected_skills},
            )
            result.dormant_suggestions = dormant_suggestions
            result.dormant_search_performed = True

            self._emit_event("layered_search_dormant_complete", {
                "dormant_suggestions_count": len(dormant_suggestions),
            })

        return result

    def _search_dormant(
        self,
        query: str,
        max_results: int = 10,
        exclude_ids: Optional[set[str]] = None,
    ) -> list[dict]:
        """
        Search dormant skills using vector similarity search.

        Falls back to keyword search if vector search is unavailable.

        Args:
            query: Search query
            max_results: Maximum results to return
            exclude_ids: Skill IDs to exclude

        Returns:
            List of matching dormant skill dicts.
        """
        exclude_ids = exclude_ids or set()

        # Try vector search first (lazy init)
        if self._dormant_vector_searcher is None and not self._dormant_vector_unavailable:
            try:
                self._dormant_vector_searcher = DormantVectorSearcher(
                    event_callback=self.event_callback
                )
            except (ValueError, RuntimeError) as e:
                # API not configured or index not built - fall back to keyword search
                console.print(f"[dim]Dormant vector search unavailable: {e}[/dim]")
                self._dormant_vector_unavailable = True

        # Use vector search if available
        if self._dormant_vector_searcher is not None:
            try:
                return self._dormant_vector_searcher.search(
                    query=query,
                    max_results=max_results,
                    exclude_ids=exclude_ids,
                )
            except Exception as e:
                console.print(f"[yellow]Vector search error: {e}, falling back to keyword[/yellow]")

        # Fallback to keyword search
        if self._dormant_index is None:
            self._dormant_index = DormantIndexLoader(self.dormant_index_path)

        results = []
        if self.config.dormant_search.keyword_enabled:
            keyword_results = self._dormant_index.search_keyword(
                query,
                limit=max_results,
                exclude_ids=exclude_ids,
            )
            results.extend(keyword_results)

        # Dedupe and limit
        seen_ids = set()
        final_results = []
        for skill in results:
            sid = skill.get("id")
            if sid and sid not in seen_ids and sid not in exclude_ids:
                seen_ids.add(sid)
                skill["is_dormant_suggestion"] = True
                final_results.append(skill)
                if len(final_results) >= max_results:
                    break

        return final_results

    def _emit_event(self, event_type: str, data: dict) -> None:
        """Emit an event to the callback if set."""
        if self.event_callback:
            try:
                self.event_callback(event_type, data)
            except Exception as e:
                console.print(f"[yellow]Event callback error: {e}[/yellow]")

    def get_tree_data(self) -> Optional[dict]:
        """Get active tree data for visualization."""
        if self._base_searcher is None:
            self._base_searcher = Searcher(
                tree_path=self.active_tree_path,
                event_callback=self.event_callback,
                **self._searcher_kwargs,
            )
        return self._base_searcher.get_tree_data()


def layered_files_exist(tree_dir: Optional[Path] = None) -> bool:
    """Check if layered tree files exist."""
    base_dir = tree_dir or (PROJECT_ROOT / "data" / "capability_trees")
    return (
        (base_dir / "active_tree.yaml").exists() and
        (base_dir / "dormant_index.yaml").exists()
    )


def create_searcher(
    tree_path: Optional[Path] = None,
    event_callback: Optional[EventCallback] = None,
    **kwargs,
):
    """
    Factory function to create appropriate searcher based on config.

    Supports two layering modes:
    - Directory-based (mode="directory"): dormant skills in separate dir, normal tree as active tree
    - Install-count-based (mode="install-count"): dormant/active split via separate active_tree.yaml

    Args:
        tree_path: Path to tree file (used for non-layered mode)
        event_callback: Event callback for search events
        **kwargs: Additional arguments passed to searcher

    Returns:
        Searcher or LayeredSearcher instance.
    """
    cfg = get_config()
    layering_cfg = cfg.layering_config()
    tree_dir = tree_path.parent if tree_path else None

    # Path A: directory-based layering
    if layering_cfg.is_directory_mode:
        if not tree_dir:
            console.print("[yellow]Warning: tree_path is None, cannot resolve dormant index for directory mode.[/yellow]")
            return Searcher(tree_path=tree_path, event_callback=event_callback, **kwargs)
        dormant_index_path = tree_dir / "dormant_index.yaml"
        if dormant_index_path.exists():
            return LayeredSearcher(
                active_tree_path=tree_path,  # normal tree IS the active tree
                dormant_index_path=dormant_index_path,
                config=layering_cfg,
                event_callback=event_callback,
                **kwargs,
            )
        else:
            console.print("[yellow]Warning: dormant_index.yaml not found. Run 'build' first for dormant search.[/yellow]")
            # Fall through to disabled searcher, NOT to install-count mode
            return Searcher(tree_path=tree_path, event_callback=event_callback, **kwargs)

    # Path B: install-count-based layering
    if layering_cfg.is_install_count_mode and tree_dir and layered_files_exist(tree_dir):
        active_tree_path = tree_dir / "active_tree.yaml"
        dormant_index_path = tree_dir / "dormant_index.yaml"

        return LayeredSearcher(
            active_tree_path=active_tree_path,
            dormant_index_path=dormant_index_path,
            config=layering_cfg,
            event_callback=event_callback,
            **kwargs,
        )

    # Path C: disabled — use original searcher
    return Searcher(
        tree_path=tree_path,
        event_callback=event_callback,
        **kwargs,
    )
