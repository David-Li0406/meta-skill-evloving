"""Direct Manager — returns all skills without search/selection.

Designed for the free-style engine: gives the agent full autonomy
over which skills to use by providing every skill in the group.
"""

from pathlib import Path
from typing import Optional

from loguru import logger

from config import get_config
from constants import resolve_skill_group, EventCallback
from manager.base import RetrievalResult
from manager.registry import register_manager
from manager.tree.skill_scanner import SkillScanner


@register_manager("direct")
class DirectManager:
    """Provides all skills directly — no indexing, no filtering."""

    def __init__(
        self,
        event_callback: Optional[EventCallback] = None,
        **kwargs,
    ):
        cfg = get_config()
        orchestrator = cfg._get("orchestrator")
        if orchestrator != "free-style":
            raise ValueError(
                f"DirectManager requires orchestrator 'free-style', "
                f"got '{orchestrator}'. Update config.yaml."
            )
        self._event_callback = event_callback

    # -- BaseManager protocol --------------------------------------------------

    def build(
        self,
        skills_dir: Optional[str] = None,
        output_path: Optional[str] = None,
        verbose: bool = False,
        show_tree: bool = True,
        generate_html: bool = True,
    ) -> dict:
        return {"status": "skipped", "reason": "direct manager requires no index"}

    def search(self, query: str, verbose: bool = False) -> RetrievalResult:
        group = resolve_skill_group(get_config().skill_group)
        skills_dir = Path(group["skills_dir"])

        scanner = SkillScanner(skills_dir)
        all_skills = scanner.to_dict_list()

        logger.info(f"DirectManager: returning all {len(all_skills)} skills")

        if self._event_callback:
            self._event_callback("search_complete", {"skills": all_skills})

        return RetrievalResult(
            query=query,
            selected_skills=all_skills,
            metadata={"strategy": "direct", "total": len(all_skills)},
        )

    def get_visual_data(self) -> Optional[dict]:
        return None

    @property
    def visual_type(self) -> str:
        return "list"
