"""Orchestrator state model (no web framework dependency).

The WebVisualizer class has moved to web/visualizer.py to keep
FastAPI dependencies out of the engine layer.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class OrchestratorState:
    """Global state for orchestration, shared across WebSocket connections."""
    task: str = ""
    start_time: Optional[datetime] = None
    current_phase: int = 0
    nodes: list = field(default_factory=list)
    logs: list = field(default_factory=list)
    node_times: dict = field(default_factory=dict)
    is_running: bool = False
    result: Optional[dict] = None
    # Plan selection
    plans: list = field(default_factory=list)
    selected_plan_index: Optional[int] = None
    waiting_for_selection: bool = False

    def get_elapsed(self) -> str:
        """Get elapsed time string."""
        if not self.start_time:
            return "0:00"
        elapsed = datetime.now() - self.start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        return f"{minutes}:{seconds:02d}"

    def to_dict(self) -> dict:
        """Convert state to dict for sending to frontend."""
        return {
            "task": self.task,
            "elapsed": self.get_elapsed(),
            "current_phase": self.current_phase,
            "nodes": self.nodes,
            "logs": self.logs,
            "plans": self.plans,
            "selected_plan_index": self.selected_plan_index,
            "waiting_for_selection": self.waiting_for_selection,
        }
