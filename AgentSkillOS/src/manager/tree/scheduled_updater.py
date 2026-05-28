"""
Scheduled Updater - Periodic update of active/dormant skill sets.

This module handles the periodic refresh of the active skill set based on
the latest install data from skills.sh. User-pinned skills are protected
from demotion.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console

from config import PROJECT_ROOT, get_config, LayeringConfig
from .layer_processor import LayerPostProcessor, LayeredOutput
from .user_prefs import load_user_prefs, save_user_prefs, UserPreferences


console = Console()


@dataclass
class UpdateResult:
    """Result from a scheduled update."""
    success: bool
    timestamp: str
    promoted: list[str] = field(default_factory=list)   # Skills moved to active
    demoted: list[str] = field(default_factory=list)    # Skills moved to dormant
    protected: list[str] = field(default_factory=list)  # Pinned skills protected from demotion
    stats: dict = field(default_factory=dict)
    error: Optional[str] = None


class ScheduledUpdater:
    """
    Handles periodic updates of the active/dormant skill sets.

    Update rules:
    1. Re-fetch/reload install data from skills_scraped.json
    2. Recalculate active set (Top N by installs)
    3. User-pinned skills are NEVER demoted
    4. Generate update report showing changes
    """

    def __init__(
        self,
        config: Optional[LayeringConfig] = None,
        user_prefs: Optional[UserPreferences] = None,
    ):
        self.config = config or get_config().layering_config()
        self.user_prefs = user_prefs or load_user_prefs()

    def update(self, tree_path: Path, output_dir: Optional[Path] = None) -> UpdateResult:
        """
        Run an update of the active/dormant sets.

        NOTE: This method regenerates active/dormant YAML files but does NOT
        rebuild the ChromaDB vector index. Callers should invoke
        DormantIndexBuilder.build() separately if vector search is in use.

        Args:
            tree_path: Path to the original tree.yaml file
            output_dir: Directory for output files

        Returns:
            UpdateResult with change details.
        """
        timestamp = datetime.now().isoformat()
        output_dir = output_dir or tree_path.parent

        # Load current active/dormant state
        active_tree_path = output_dir / "active_tree.yaml"
        dormant_index_path = output_dir / "dormant_index.yaml"

        old_active_ids = set()
        old_dormant_ids = set()

        if active_tree_path.exists():
            old_active_ids = self._collect_skill_ids_from_tree(active_tree_path)

        if dormant_index_path.exists():
            old_dormant_ids = self._collect_skill_ids_from_dormant_index(dormant_index_path)

        console.print(f"[dim]Current state: {len(old_active_ids)} active, {len(old_dormant_ids)} dormant[/dim]")

        # Run layer processor to generate new active/dormant sets
        try:
            processor = LayerPostProcessor(
                config=self.config,
                user_prefs=self.user_prefs,
            )
            output = processor.process(tree_path, output_dir)
        except Exception as e:
            return UpdateResult(
                success=False,
                timestamp=timestamp,
                error=str(e),
            )

        # Calculate changes
        new_active_ids = self._collect_skill_ids_from_tree_dict(output.active_tree)
        new_dormant_ids = {s.id for s in output.dormant_index.skills}

        promoted = list(new_active_ids - old_active_ids - set(self.user_prefs.pinned_skill_ids))
        demoted = list(old_active_ids - new_active_ids - set(self.user_prefs.pinned_skill_ids))
        protected = list(set(self.user_prefs.pinned_skill_ids) & old_active_ids)

        # Save updated files
        output.save(active_tree_path, dormant_index_path)

        console.print(f"[dim]New state: {len(new_active_ids)} active, {len(new_dormant_ids)} dormant[/dim]")

        return UpdateResult(
            success=True,
            timestamp=timestamp,
            promoted=promoted,
            demoted=demoted,
            protected=protected,
            stats={
                "total_skills": output.stats.get("total_skills", 0),
                "active_skills": len(new_active_ids),
                "dormant_skills": len(new_dormant_ids),
                "pinned_skills": len(self.user_prefs.pinned_skill_ids),
                "threshold": self.config.active_threshold,
            },
        )

    def _collect_skill_ids_from_tree(self, tree_path: Path) -> set[str]:
        """Collect all skill IDs from a tree YAML file."""
        if not tree_path.exists():
            return set()

        with open(tree_path, "r", encoding="utf-8") as f:
            tree_dict = yaml.safe_load(f)

        return self._collect_skill_ids_from_tree_dict(tree_dict)

    def _collect_skill_ids_from_tree_dict(self, tree_dict: dict) -> set[str]:
        """Recursively collect all skill IDs from tree structure."""
        ids = set()

        for skill in tree_dict.get("skills", []):
            sid = skill.get("id")
            if sid:
                ids.add(sid)

        for child in tree_dict.get("children", []):
            ids.update(self._collect_skill_ids_from_tree_dict(child))

        return ids

    def _collect_skill_ids_from_dormant_index(self, index_path: Path) -> set[str]:
        """Collect all skill IDs from dormant index YAML file."""
        if not index_path.exists():
            return set()

        with open(index_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return {s.get("id") for s in data.get("skills", []) if s.get("id")}


def run_update(
    tree_path: Path,
    output_dir: Optional[Path] = None,
    verbose: bool = False,
) -> UpdateResult:
    """
    Convenience function to run a scheduled update.

    Args:
        tree_path: Path to the original tree.yaml file
        output_dir: Directory for output files
        verbose: Print progress

    Returns:
        UpdateResult with change details.
    """
    cfg = get_config()
    layering_cfg = cfg.layering_config()

    if not layering_cfg.is_enabled:
        console.print("[yellow]Layering is disabled in config.[/yellow]")
        return UpdateResult(
            success=False,
            timestamp=datetime.now().isoformat(),
            error="Layering is disabled",
        )

    if layering_cfg.is_directory_mode:
        console.print("[yellow]run_update() is for install-count mode. Use CLI 'update-layer' for directory mode.[/yellow]")
        return UpdateResult(
            success=False,
            timestamp=datetime.now().isoformat(),
            error="Use 'update-layer' command for directory-based layering",
        )

    updater = ScheduledUpdater(config=layering_cfg)
    result = updater.update(tree_path, output_dir)

    if verbose and result.success:
        console.print(f"\n[bold green]Update complete![/bold green]")
        console.print(f"  Timestamp: {result.timestamp}")
        console.print(f"  Active skills: {result.stats['active_skills']}")
        console.print(f"  Dormant skills: {result.stats['dormant_skills']}")
        console.print(f"  Pinned skills: {result.stats['pinned_skills']}")

        if result.promoted:
            console.print(f"\n  [green]Promoted to active ({len(result.promoted)}):[/green]")
            for sid in result.promoted[:10]:  # Show first 10
                console.print(f"    + {sid}")
            if len(result.promoted) > 10:
                console.print(f"    ... and {len(result.promoted) - 10} more")

        if result.demoted:
            console.print(f"\n  [yellow]Demoted to dormant ({len(result.demoted)}):[/yellow]")
            for sid in result.demoted[:10]:
                console.print(f"    - {sid}")
            if len(result.demoted) > 10:
                console.print(f"    ... and {len(result.demoted) - 10} more")

        if result.protected:
            console.print(f"\n  [cyan]Protected (pinned): {len(result.protected)} skills[/cyan]")

    elif verbose and not result.success:
        console.print(f"[red]Update failed: {result.error}[/red]")

    return result
