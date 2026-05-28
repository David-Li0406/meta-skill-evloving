"""
Evaluation orchestrator - parses config, calls evaluators, aggregates results.
"""
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional

from .types import (
    TaskConfig,
    EvaluatorConfig,
    EvaluatorResult,
    TaskEvaluationResult,
    AggregationConfig,
    EvaluatorType,
)
from .registry import EVALUATOR_REGISTRY


class EvaluationOrchestrator:
    """
    Orchestrator for running task evaluations.

    Responsibilities:
    - Parse task configuration
    - Topologically sort evaluators by dependencies
    - Execute evaluators in order
    - Aggregate results according to scoring method
    """

    def __init__(self, task_config: TaskConfig, workspace: Path):
        """
        Initialize orchestrator.

        Args:
            task_config: Task configuration object
            workspace: Path to workspace directory
        """
        self.config = task_config
        self.workspace = workspace
        self.results: List[EvaluatorResult] = []
        self.completed: Dict[str, EvaluatorResult] = {}

    async def run(self) -> TaskEvaluationResult:
        """
        Execute the full evaluation flow.

        Returns:
            TaskEvaluationResult with aggregated scores
        """
        # Sort evaluators by dependencies
        sorted_evaluators = self._topological_sort(self.config.evaluators)

        # Execute each evaluator
        for eval_config in sorted_evaluators:
            result = await self._execute_evaluator(eval_config)
            self.results.append(result)
            self.completed[eval_config.id] = result

        # Aggregate and return results
        return self._aggregate_results()

    async def _execute_evaluator(self, eval_config: EvaluatorConfig) -> EvaluatorResult:
        """
        Execute a single evaluator.

        Args:
            eval_config: Evaluator configuration

        Returns:
            EvaluatorResult
        """
        eval_id = eval_config.id
        eval_type = eval_config.type      # EvaluatorType enum
        op_func = eval_config.op_func     # Function name to call
        op_args = eval_config.op_args
        value = eval_config.value
        weight = eval_config.weight

        # Check if dependencies are satisfied (score > 0 means passed)
        for dep_id in eval_config.depends_on:
            if dep_id not in self.completed:
                return EvaluatorResult(
                    evaluator_id=eval_id,
                    score=0.0,
                    message=f"Dependency not found: {dep_id}",
                    weight=weight
                )
            if self.completed[dep_id].score == 0.0:
                return EvaluatorResult(
                    evaluator_id=eval_id,
                    score=0.0,
                    message=f"Skipped: dependency {dep_id} failed",
                    weight=weight
                )

        # Auto-sort path list to match task outputs order
        if isinstance(op_args.get("path"), list) and self.config.outputs:
            outputs_order = self.config.outputs
            def _sort_key(p):
                try:
                    return outputs_order.index(p)
                except ValueError:
                    return len(outputs_order)
            op_args = {**op_args, "path": sorted(op_args["path"], key=_sort_key)}

        # Get evaluator function from registry using op_func
        evaluator_func = EVALUATOR_REGISTRY.get(op_func)
        if evaluator_func is None:
            return EvaluatorResult(
                evaluator_id=eval_id,
                score=0.0,
                message=f"Unknown evaluator function: {op_func}",
                weight=weight
            )

        # Call the evaluator and interpret result based on type
        try:
            if value is not None:
                result = await evaluator_func(self.workspace, op_args, value)
            else:
                result = await evaluator_func(self.workspace, op_args)

            # Interpret result — only objective evaluators remain
            if len(result) == 3:
                raw_passed, message, _ = result
            else:
                raw_passed, message = result
            score = 1.0 if raw_passed else 0.0

            return EvaluatorResult(
                evaluator_id=eval_id,
                score=score,
                message=message,
                weight=weight,
                details={
                    "type": eval_type.value,
                    "op_func": op_func,
                    "op_args": op_args,
                    "value": value
                }
            )
        except Exception as e:
            return EvaluatorResult(
                evaluator_id=eval_id,
                score=0.0,
                message=f"Evaluator exception: {str(e)}",
                weight=weight
            )

    def _aggregate_results(self) -> TaskEvaluationResult:
        """
        Aggregate all evaluator results using continuous scores.

        Each evaluator contributes score * weight to the total.
        Objective evaluators return score 0.0 or 1.0.

        Returns:
            TaskEvaluationResult
        """
        total_weight = sum(r.weight for r in self.results)
        scored_weight = sum(r.score * r.weight for r in self.results)

        # Score is weighted average scaled to 0-100
        total_score = (scored_weight / total_weight * 100) if total_weight > 0 else 0

        # Generate summary
        low_score = [r for r in self.results if r.score < 1.0]
        if low_score:
            details = [f"{r.evaluator_id}({r.score:.1f})" for r in low_score]
            summary = f"Partial scores: {details}"
        else:
            summary = "All evaluators scored full marks"

        return TaskEvaluationResult(
            task_id=self.config.task_id,
            total_score=round(total_score, 2),
            max_score=100.0,
            evaluator_results=self.results,
            summary=summary
        )

    def _topological_sort(self, evaluators: List[EvaluatorConfig]) -> List[EvaluatorConfig]:
        """
        Sort evaluators by dependencies using topological sort.

        Args:
            evaluators: List of evaluator configs

        Returns:
            Sorted list of evaluator configs
        """
        sorted_list = []
        remaining = list(evaluators)
        resolved = set()

        max_iterations = len(evaluators) * 2  # Prevent infinite loop
        iterations = 0

        while remaining and iterations < max_iterations:
            iterations += 1
            progress = False

            for eval_config in remaining[:]:
                deps = set(eval_config.depends_on)
                if deps <= resolved:
                    sorted_list.append(eval_config)
                    resolved.add(eval_config.id)
                    remaining.remove(eval_config)
                    progress = True

            if not progress and remaining:
                # Circular dependency or missing dependency - add remaining items
                sorted_list.extend(remaining)
                break

        return sorted_list


# ==================== Entry Functions ====================

async def evaluate_task(task_config_path: str, workspace_path: str) -> TaskEvaluationResult:
    """
    Evaluate a task given config file and workspace paths.

    Args:
        task_config_path: Path to task configuration JSON file
        workspace_path: Path to workspace directory

    Returns:
        TaskEvaluationResult
    """
    with open(task_config_path, 'r', encoding='utf-8') as f:
        config_dict = json.load(f)

    config = TaskConfig.from_dict(config_dict)
    workspace = Path(workspace_path)

    orchestrator = EvaluationOrchestrator(config, workspace)
    return await orchestrator.run()


def evaluate_task_sync(task_config_path: str, workspace_path: str) -> TaskEvaluationResult:
    """
    Synchronous wrapper for evaluate_task.

    Args:
        task_config_path: Path to task configuration JSON file
        workspace_path: Path to workspace directory

    Returns:
        TaskEvaluationResult
    """
    return asyncio.run(evaluate_task(task_config_path, workspace_path))


async def evaluate_task_from_dict(config_dict: Dict[str, Any],
                                   workspace_path: str) -> TaskEvaluationResult:
    """
    Evaluate a task given config dict and workspace path.

    Args:
        config_dict: Task configuration dictionary
        workspace_path: Path to workspace directory

    Returns:
        TaskEvaluationResult
    """
    config = TaskConfig.from_dict(config_dict)
    workspace = Path(workspace_path)

    orchestrator = EvaluationOrchestrator(config, workspace)
    return await orchestrator.run()
