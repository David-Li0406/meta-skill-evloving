"""
Type definitions for the evaluation framework.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pathlib import Path
from enum import Enum


class ScoringMethod(Enum):
    """Scoring aggregation methods"""
    WEIGHTED_SUM = "weighted_sum"
    ALL_PASS = "all_pass"
    THRESHOLD = "threshold"


class EvaluatorType(Enum):
    """
    Categories of evaluation.

    - OBJECTIVE_USABILITY: Deterministic checks using objective evaluators (returns 0 or 1)

    LLM-based evaluators (llm_usability, llm_quality) have been removed.
    Use benchmark.ranking for post-hoc quality comparison via pairwise LLM judging.
    """
    OBJECTIVE_USABILITY = "objective_usability"


@dataclass
class EvaluatorResult:
    """Result from a single evaluator"""
    evaluator_id: str
    score: float                    # Continuous score (0.0-1.0)
    message: str = ""               # Details/error message
    weight: float = 1.0             # Weight for scoring
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        """Consider passed if score > 0.5"""
        return self.score > 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluator_id": self.evaluator_id,
            "passed": self.passed,
            "score": self.score,
            "message": self.message,
            "weight": self.weight,
            "details": self.details
        }


@dataclass
class TaskEvaluationResult:
    """Overall evaluation result for a task"""
    task_id: str
    total_score: float              # Weighted score (0-100)
    max_score: float = 100.0
    evaluator_results: List[EvaluatorResult] = field(default_factory=list)
    summary: str = ""

    @property
    def passed(self) -> bool:
        """Consider passed if total_score >= 60%"""
        return self.total_score >= 60.0

    @property
    def pass_rate(self) -> float:
        """Return pass rate as ratio (0.0-1.0)"""
        return self.total_score / self.max_score if self.max_score > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "passed": self.passed,
            "total_score": self.total_score,
            "max_score": self.max_score,
            "pass_rate": self.pass_rate,
            "summary": self.summary,
            "evaluator_results": [r.to_dict() for r in self.evaluator_results]
        }


@dataclass
class EvaluatorConfig:
    """Configuration for a single evaluator"""
    id: str
    type: EvaluatorType             # Evaluation category (one of three types)
    op_func: str                    # Function name in registry (e.g., "file_exists", "llm_quality_judge")
    description: str = ""
    op_args: Dict[str, Any] = field(default_factory=dict)
    value: Any = None               # Expected answer / ground truth
    weight: float = 1.0
    depends_on: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluatorConfig":
        # Parse type as EvaluatorType enum
        type_str = data["type"]
        eval_type = EvaluatorType(type_str)

        return cls(
            id=data["id"],
            type=eval_type,
            op_func=data["op_func"],
            description=data.get("description", ""),
            op_args=data.get("op_args", {}),
            value=data.get("value"),
            weight=data.get("weight", 1.0),
            depends_on=data.get("depends_on", [])
        )


@dataclass
class AggregationConfig:
    """Configuration for scoring/aggregation"""
    strategy: str = "weighted_sum"      # weighted_sum, all_pass, threshold

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AggregationConfig":
        return cls(
            strategy=data.get("strategy", "weighted_sum")
        )


# Alias for backward compatibility
ScoringConfig = AggregationConfig


@dataclass
class TaskConfig:
    """Full task configuration"""
    task_id: str
    workspace_path: Optional[Path] = None  # Now optional - workspace is evaluation.json's directory
    evaluators: List[EvaluatorConfig] = field(default_factory=list)
    aggregation: AggregationConfig = field(default_factory=AggregationConfig)
    task_name: str = ""
    description: str = ""
    category: str = ""
    outputs: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskConfig":
        evaluators = [EvaluatorConfig.from_dict(e) for e in data.get("evaluators", [])]
        aggregation = AggregationConfig.from_dict(data.get("aggregation", {}))
        return cls(
            task_id=data.get("task_id", "unknown"),
            workspace_path=Path(data["workspace_path"]) if data.get("workspace_path") else None,
            evaluators=evaluators,
            aggregation=aggregation,
            task_name=data.get("task_name", ""),
            description=data.get("description", ""),
            category=data.get("category", ""),
            outputs=data.get("outputs", []),
        )
