from typing import Protocol, Optional, runtime_checkable
from dataclasses import dataclass, field

from constants import EventCallback

@dataclass
class RetrievalResult:
    """Unified retrieval result."""
    query: str
    selected_skills: list[dict]
    metadata: dict = field(default_factory=dict)


@runtime_checkable
class BaseManager(Protocol):
    """Skill management interface: build index + search. Replaced as a whole unit."""

    def build(
        self,
        skills_dir: Optional[str] = None,
        output_path: Optional[str] = None,
        verbose: bool = False,
        show_tree: bool = True,
        generate_html: bool = True,
    ) -> dict:
        """Build index (tree/vector/keyword etc.), return structure data."""
        ...

    def search(self, query: str, verbose: bool = False) -> RetrievalResult:
        """Search for relevant skills."""
        ...

    def get_visual_data(self) -> Optional[dict]:
        """Return visualization data (optional, None if unsupported)."""
        ...

    @property
    def visual_type(self) -> str:
        """搜索结果的可视化类型: "tree" | "list" | "none" """
        ...
