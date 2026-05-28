"""Unified execution engine interface."""

from dataclasses import dataclass, field
from typing import Optional, Protocol


@dataclass
class EngineRequest:
    """Standardized request for any execution engine."""

    task: str
    skills: list[str] = field(default_factory=list)
    files: Optional[list[str]] = None
    # DAG-specific
    visualizer: Optional[object] = None  # VisualizerProtocol instance
    # Freestyle-specific
    copy_all_skills: bool = False
    # Direct-specific
    allowed_tools: Optional[list[str]] = None


@dataclass
class ExecutionResult:
    """Standardized result from any execution engine."""

    status: str
    summary: str = ""
    error: Optional[str] = None
    artifacts: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class ExecutionEngine(Protocol):
    """Any execution strategy implements this."""

    async def run(self, request: EngineRequest) -> ExecutionResult: ...


@dataclass(frozen=True)
class EngineMeta:
    """Engine metadata — declared once per engine class, read by registry."""

    label: str
    description: str = ""
    show_in_review: bool = True
    execution_visual: str = "single"    # "graph" | "single"
    initial_phase: str = "executing"    # "planning" | "executing"
    folder_mode: str | None = None      # None = use registered name
    aliases: tuple[str, ...] = ()
