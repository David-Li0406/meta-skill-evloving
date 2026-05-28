"""Data models for skill orchestration - simplified."""

from dataclasses import dataclass as std_dataclass
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from constants import TaskStatus as NodeStatus  # noqa: F401 — re-exported


# =============================================================================
# SDK Metrics (standard dataclass, not Pydantic)
# =============================================================================


@std_dataclass
class SDKMetrics:
    """Metrics from a single Claude Agent SDK ResultMessage."""

    duration_ms: int = 0
    total_cost_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0
    num_turns: int = 0
    is_error: bool = False
    subtype: str = ""

    @classmethod
    def from_result_message(cls, message) -> "SDKMetrics":
        """Extract metrics from a Claude Agent SDK ResultMessage."""
        return cls(
            duration_ms=getattr(message, "duration_ms", 0) or 0,
            total_cost_usd=getattr(message, "total_cost_usd", 0.0) or 0.0,
            input_tokens=getattr(message, "input_tokens", 0) or 0,
            output_tokens=getattr(message, "output_tokens", 0) or 0,
            cache_creation_input_tokens=getattr(message, "cache_creation_input_tokens", 0) or 0,
            cache_read_input_tokens=getattr(message, "cache_read_input_tokens", 0) or 0,
            num_turns=getattr(message, "num_turns", 0) or 0,
            is_error=getattr(message, "is_error", False) or False,
            subtype=getattr(message, "subtype", "") or "",
        )

    def to_dict(self) -> dict:
        """Serialize to a plain dict."""
        return {
            "duration_ms": self.duration_ms,
            "total_cost_usd": self.total_cost_usd,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_creation_input_tokens": self.cache_creation_input_tokens,
            "cache_read_input_tokens": self.cache_read_input_tokens,
            "num_turns": self.num_turns,
            "is_error": self.is_error,
            "subtype": self.subtype,
        }

    @staticmethod
    def aggregate(
        phase_node_metrics: list[list[tuple[str, "SDKMetrics"]]],
        extra_metrics: dict[str, "SDKMetrics"] | None = None,
    ) -> dict:
        """Phase-aware aggregation.

        - extra_metrics (e.g. planning): duration added directly
        - phase_node_metrics: per-phase max duration, cross-phase sum
        - tokens/cost/num_turns: summed across all sessions
        - is_error: True if any session errored
        - Multi-node: includes node_metrics sub-dict
        """
        all_metrics: list[SDKMetrics] = []
        node_metrics_map: dict[str, dict] = {}
        session_count = 0

        # Extra metrics (planning, etc.) — duration adds directly
        extra_duration = 0
        if extra_metrics:
            for name, m in extra_metrics.items():
                all_metrics.append(m)
                node_metrics_map[name] = m.to_dict()
                extra_duration += m.duration_ms
                session_count += 1

        # Phase-aware duration: per-phase max, then sum across phases
        phase_duration = 0
        for phase_list in phase_node_metrics:
            if not phase_list:
                continue
            phase_max = 0
            for node_name, m in phase_list:
                all_metrics.append(m)
                node_metrics_map[node_name] = m.to_dict()
                session_count += 1
                if m.duration_ms > phase_max:
                    phase_max = m.duration_ms
            phase_duration += phase_max

        total_duration = extra_duration + phase_duration

        # Sum all additive fields
        result: dict = {
            "duration_ms": total_duration,
            "total_cost_usd": sum(m.total_cost_usd for m in all_metrics),
            "input_tokens": sum(m.input_tokens for m in all_metrics),
            "output_tokens": sum(m.output_tokens for m in all_metrics),
            "cache_creation_input_tokens": sum(m.cache_creation_input_tokens for m in all_metrics),
            "cache_read_input_tokens": sum(m.cache_read_input_tokens for m in all_metrics),
            "num_turns": sum(m.num_turns for m in all_metrics),
            "is_error": any(m.is_error for m in all_metrics),
            "session_count": session_count,
        }

        # Only include node_metrics when there are multiple nodes
        if len(node_metrics_map) > 1:
            result["node_metrics"] = node_metrics_map

        return result


# =============================================================================
# Enums
# =============================================================================


class SkillType(str, Enum):
    """Type of skill in the orchestration graph."""

    PRIMARY = "primary"  # Produces final deliverables
    HELPER = "helper"  # Supports primary or other helpers


class NodeFailureReason(str, Enum):
    """Reason for node execution failure."""

    SUCCESS = "success"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    SKILL_ERROR = "skill_error"

    UNKNOWN = "unknown"
    EXECUTION_ERROR = "execution_error"


# =============================================================================
# Pydantic Models
# =============================================================================


class SkillMetadata(BaseModel):
    """Metadata parsed from SKILL.md frontmatter."""

    name: str
    description: str
    path: str
    allowed_tools: list[str] = Field(default_factory=list)
    category: str = "other"
    content: str = ""  # SKILL.md content (first 5000 chars)

    class Config:
        frozen = True


class SkillNode(BaseModel):
    """Represents a skill in the dependency graph."""

    id: str
    name: str
    skill_type: SkillType = SkillType.HELPER
    depends_on: list[str] = Field(default_factory=list)
    purpose: str = ""
    status: NodeStatus = NodeStatus.PENDING
    output_path: Optional[str] = None
    # Collaboration fields
    outputs_summary: str = ""  # Expected outputs description
    downstream_hint: str = ""  # Role in workflow + quality requirements
    usage_hints: dict[str, str] = Field(default_factory=dict)  # {consumer_node_id: usage_instruction}

    @property
    def is_terminal(self) -> bool:
        """Check if node is in a terminal state."""
        return self.status in {
            NodeStatus.COMPLETED,
            NodeStatus.FAILED,
            NodeStatus.SKIPPED,
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.skill_type.value,
            "depends_on": self.depends_on,
            "purpose": self.purpose,
            "status": self.status.value,
        }
        if self.output_path:
            result["output_path"] = self.output_path
        return result


class ExecutionPhase(BaseModel):
    """A group of skills that can run in parallel."""

    phase_number: int
    nodes: list[str]
    mode: str = "parallel"  # parallel | sequential

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "phase": self.phase_number,
            "mode": self.mode,
            "nodes": self.nodes,
        }


class NodeExecutionResult(BaseModel):
    """Result returned from an isolated session execution."""

    node_id: str
    status: NodeStatus
    output_path: Optional[str] = None
    summary: str = ""  # Brief summary of what was accomplished
    error: Optional[str] = None
    failure_reason: NodeFailureReason = NodeFailureReason.SUCCESS
    execution_time_seconds: float = 0.0
    cost_usd: float = 0.0
    sdk_metrics: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "node_id": self.node_id,
            "status": self.status.value,
            "failure_reason": self.failure_reason.value,
            "execution_time_seconds": self.execution_time_seconds,
        }
        if self.output_path:
            result["output_path"] = self.output_path
        if self.summary:
            result["summary"] = self.summary
        if self.error:
            result["error"] = self.error
        if self.cost_usd > 0:
            result["cost_usd"] = self.cost_usd
        if self.sdk_metrics:
            result["sdk_metrics"] = self.sdk_metrics
        return result
