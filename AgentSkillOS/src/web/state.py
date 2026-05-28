"""Workflow state models for the web UI.

Defines the phase enum and state dataclass used throughout the workflow.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from manager.base import RetrievalResult
from orchestrator.registry import list_review_engines
from orchestrator.visualizers import OrchestratorState


class WorkflowPhase(str, Enum):
    """Phases of the unified workflow."""
    IDLE = "idle"
    SEARCHING = "searching"
    REVIEWING = "reviewing"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class WorkflowState:
    """State for the unified search + orchestration workflow."""
    phase: WorkflowPhase = WorkflowPhase.IDLE
    task: str = ""
    task_name: str = ""
    files: list[str] = field(default_factory=list)
    start_time: Optional[datetime] = None

    # Mode state: "full" for complete workflow, "execute" for direct execution
    mode: str = "full"
    # Run mode: "baseline", "free-style", "dag" (only used when mode="execute")
    run_mode: Optional[str] = None
    # Preset skills for execute mode (can be empty list for baseline)
    preset_skills: list[str] = field(default_factory=list)
    # Execution mode for unified flow: "dag" or "free-style"
    execution_mode: str = "dag"

    # Skill group state
    current_group_id: str = "default"

    # Custom skill group configuration
    custom_skills_dir: str = ""
    custom_tree_path: str = ""

    # Search state
    search_result: Optional[RetrievalResult] = None
    selected_skill_ids: list[str] = field(default_factory=list)
    tree_data: Optional[dict] = None
    search_events: list[dict] = field(default_factory=list)
    search_complete: bool = False  # Flag: search completed, waiting for user confirmation

    # Layering state (active/dormant skill strategy)
    dormant_suggestions: list[dict] = field(default_factory=list)  # Suggested dormant skills
    dormant_skills_used: list[str] = field(default_factory=list)  # Dormant skills added to selection
    recommended_recipes: list[dict] = field(default_factory=list)

    # Completion persistence (survives page refresh)
    completion_status: Optional[str] = None   # "completed" | "partial" | "failed"
    error_message: Optional[str] = None       # Error details for error phase

    # Orchestration state (inherits from OrchestratorState)
    orchestrator_state: Optional[OrchestratorState] = None

    # Working directory (relative path for display)
    work_dir: str = ""

    # UI hints for frontend panel rendering
    ui_hints: dict = field(default_factory=lambda: {
        "search_visual": "tree",
        "has_planning": True,
        "execution_visual": "graph",
        "has_search": True,
        "has_skill_review": True,
    })

    # Logs
    logs: list[dict] = field(default_factory=list)

    def get_elapsed(self) -> str:
        """Get elapsed time string."""
        if not self.start_time:
            return "0:00"
        elapsed = datetime.now() - self.start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        return f"{minutes}:{seconds:02d}"

    def add_log(self, message: str, level: str = "info") -> dict:
        """Add a log entry and return it."""
        entry = {
            "message": message,
            "level": level,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "elapsed": self.get_elapsed(),
        }
        self.logs.append(entry)
        return entry

    def to_dict(self) -> dict:
        """Convert state to dict for sending to frontend."""
        result = {
            "phase": self.phase.value,
            "task": self.task,
            "elapsed": self.get_elapsed(),
            "logs": self.logs,
            "tree_data": self.tree_data,
            "search_events": self.search_events,
            "search_complete": self.search_complete,
            # Execute mode info
            "mode": self.mode,
            "run_mode": self.run_mode,
            "preset_skills": self.preset_skills,
            # Execution mode for unified flow
            "execution_mode": self.execution_mode,
            # Working directory
            "work_dir": self.work_dir,
            # UI hints for frontend panel rendering
            "ui_hints": self.ui_hints,
            # Available engines for skill review UI
            "available_engines": list_review_engines(),
        }

        # Add search result if available
        if self.search_result:
            result["search_result"] = {
                "skills": self.search_result.selected_skills,
                "llm_calls": self.search_result.metadata.get("llm_calls", 0),
            }
            result["selected_skill_ids"] = self.selected_skill_ids

        # Add layering state if available
        if self.dormant_suggestions:
            result["dormant_suggestions"] = self.dormant_suggestions
        if self.dormant_skills_used:
            result["dormant_skills_used"] = self.dormant_skills_used

        # Add recommended recipes if available
        if self.recommended_recipes:
            result["recommended_recipes"] = self.recommended_recipes

        # Add completion persistence fields
        if self.completion_status:
            result["completion_status"] = self.completion_status
        if self.error_message:
            result["error_message"] = self.error_message

        # Add files if available (for restoring file list after refresh)
        if self.files:
            result["files"] = self.files

        # Add orchestrator state if available
        if self.orchestrator_state:
            result["orchestrator"] = self.orchestrator_state.to_dict()

        return result
