"""Bridge module to call benchmark evaluation from AgentSkillOS."""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from loguru import logger

from benchmark.AgentSkillOS_bench import (
    EvaluationOrchestrator,
    TaskConfig as SBTaskConfig,
    EvaluatorConfig,
    AggregationConfig,
)


@dataclass
class EvaluationResult:
    """Wrapper for benchmark evaluation results."""

    passed: bool = False
    total_score: float = 0.0
    max_score: float = 100.0
    pass_rate: float = 0.0
    summary: str = ""
    evaluator_details: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "total_score": self.total_score,
            "max_score": self.max_score,
            "pass_rate": self.pass_rate,
            "summary": self.summary,
            "evaluator_details": self.evaluator_details,
        }


async def evaluate_workspace(
    evaluators_config: list[dict],
    aggregation_config: dict,
    workspace_path: Path,
    task_id: str = "",
) -> Optional[EvaluationResult]:
    """Call benchmark evaluation on a workspace.

    Args:
        evaluators_config: Raw evaluator dicts from task JSON.
        aggregation_config: Raw aggregation dict from task JSON.
        workspace_path: Path to the agent workspace directory.
        task_id: Task identifier for logging.

    Returns:
        EvaluationResult if evaluators exist, None otherwise.
    """
    if not evaluators_config:
        return None

    # Ensure evaluators are registered even if loader was bypassed
    from benchmark import _ensure_registered
    _ensure_registered()

    sb_config = SBTaskConfig(
        task_id=task_id,
        evaluators=[EvaluatorConfig.from_dict(e) for e in evaluators_config],
        aggregation=AggregationConfig.from_dict(aggregation_config),
    )
    sb_result = await EvaluationOrchestrator(sb_config, workspace_path).run()

    # Save evaluation.json next to workspace (in the run directory)
    eval_path = workspace_path.parent / "evaluation.json"
    with open(eval_path, "w", encoding="utf-8") as f:
        json.dump(sb_result.to_dict(), f, indent=2, ensure_ascii=False)
    logger.info(f"Evaluation saved to {eval_path}")

    return EvaluationResult(
        passed=sb_result.passed,
        total_score=sb_result.total_score,
        max_score=sb_result.max_score,
        pass_rate=sb_result.pass_rate,
        summary=sb_result.summary,
        evaluator_details=[r.to_dict() for r in sb_result.evaluator_results],
    )
