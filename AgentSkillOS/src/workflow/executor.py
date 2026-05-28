"""Batch task executor — CLI adapter with Rich progress UI.

Business logic (skill discovery + engine execution) is delegated to
workflow.service.run_task() via workflow.batch.run_batch().
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger
from rich.console import Console

from orchestrator.base import ExecutionResult

from .models import (
    TaskConfig,
    TaskRequest,
    BatchConfig,
    TaskResult,
    BatchResult,
    TaskStatus,
)
from .batch import run_batch
from .progress import BatchProgressManager


class BatchExecutor:
    """Execute batch tasks with parallel support and progress tracking."""

    def __init__(
        self,
        config: BatchConfig,
        console: Optional[Console] = None,
        dry_run: bool = False,
        prior_results: Optional[list[TaskResult]] = None,
        total_override: Optional[int] = None,
    ):
        self.config = config
        self.console = console or Console()
        self.dry_run = dry_run
        self.prior_results = prior_results or []
        self._total_override = total_override

        # Resolve output directory
        self.output_dir = Path(config.output_dir).resolve()
        self.batch_dir = self.output_dir / config.batch_id

        # Progress manager
        self.progress: Optional[BatchProgressManager] = None

    def run(self) -> BatchResult:
        """Execute all tasks in the batch."""
        # Reload Config singleton if batch specifies a custom config file
        if self.config.config_file:
            from config import Config, get_config
            # Preserve CLI overrides across Config reset
            cli_overrides = Config._instance._cli.copy() if Config._instance else {}
            # NOTE: Config.reset() is only safe here because BatchExecutor.run()
            # is called from the main thread before any async tasks start.
            logger.warning("Resetting Config singleton for batch config_file override")
            Config.reset()
            get_config(cli_args=cli_overrides, config_path=self.config.config_file)

        start_time = datetime.now()

        self.batch_dir.mkdir(parents=True, exist_ok=True)

        display_total = self._total_override or len(self.config.tasks)
        self.progress = BatchProgressManager(
            self.config.batch_id,
            display_total,
            self.console,
            search_enabled=self.config.defaults.get("skill_mode", "auto") == "auto",
        )
        self.progress.set_pending_tasks(self.config.tasks)
        self.progress.start()

        # Pre-advance progress for previously completed (resumed) tasks
        if self.prior_results:
            self.progress.set_resumed_count(len(self.prior_results))

        try:
            if self.dry_run:
                results = self._run_dry()
            else:
                results = self._run_batch()
        finally:
            self.progress.stop()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Merge prior (resumed) results with new results
        all_results = self.prior_results + results

        completed = sum(1 for r in all_results if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in all_results if r.status == TaskStatus.FAILED)
        skipped = sum(1 for r in all_results if r.status == TaskStatus.SKIPPED)

        # Compute evaluation summary
        eval_results = [r for r in all_results if r.evaluation]
        eval_total = len(eval_results)
        eval_passed = sum(1 for r in eval_results if r.evaluation.get("passed"))
        avg_eval_score = (
            sum(r.evaluation["total_score"] for r in eval_results) / eval_total
            if eval_total else 0.0
        )

        # Aggregate SDK metrics across all tasks
        total_cost = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        for r in all_results:
            if r.sdk_metrics:
                total_cost += r.sdk_metrics.get("total_cost_usd", 0.0)
                total_input_tokens += r.sdk_metrics.get("input_tokens", 0)
                total_output_tokens += r.sdk_metrics.get("output_tokens", 0)

        result = BatchResult(
            batch_id=self.config.batch_id,
            started_at=start_time,
            completed_at=end_time,
            duration_seconds=duration,
            total=self._total_override or len(self.config.tasks),
            completed=completed,
            failed=failed,
            skipped=skipped,
            task_results=all_results,
            output_dir=str(self.batch_dir),
            eval_total=eval_total,
            eval_passed=eval_passed,
            avg_eval_score=avg_eval_score,
            total_cost_usd=total_cost,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
        )

        self._save_batch_result(result)
        self.progress.print_summary(result)
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_dry(self) -> list[TaskResult]:
        """Dry-run: mark every task as skipped without executing."""
        from config import get_config
        results: list[TaskResult] = []
        for task in self.config.tasks:
            self.progress.task_started(task)
            result = TaskResult(
                task_id=task.task_id,
                status=TaskStatus.SKIPPED,
                summary="Dry run - not executed",
                run_id=get_config()._get("orchestrator"),
            )
            results.append(result)
            self.progress.task_completed(result)
        return results

    def _run_batch(self) -> list[TaskResult]:
        """Execute tasks via async run_batch()."""
        # Build a mapping from TaskRequest back to TaskConfig for progress callbacks
        task_configs: dict[str, TaskConfig] = {}
        requests: list[TaskRequest] = []
        for tc in self.config.tasks:
            req = self._to_task_request(tc)
            requests.append(req)
            task_configs[tc.task_id] = tc

        start_times: dict[str, datetime] = {}
        task_results: list[TaskResult] = []

        def on_start(req: TaskRequest) -> None:
            tc = task_configs.get(req.task_id)
            if tc:
                start_times[req.task_id] = datetime.now()
                self.progress.task_started(tc)
                self.progress.task_phase_update(
                    req.task_id, f"Executing ({req.mode})", 30
                )

        def on_complete(req: TaskRequest, exec_result: ExecutionResult) -> None:
            now = datetime.now()
            started = start_times.get(req.task_id)
            duration = (now - started).total_seconds() if started else 0.0
            status = TaskStatus.COMPLETED if exec_result.status != "failed" else TaskStatus.FAILED
            eval_data = exec_result.metadata.get("evaluation")
            # Extract SDK metrics, strip node_metrics for batch-level summary
            sdk_metrics = exec_result.metadata.get("sdk_metrics")
            if sdk_metrics:
                sdk_metrics = {k: v for k, v in sdk_metrics.items() if k != "node_metrics"}
            tr = TaskResult(
                task_id=req.task_id,
                status=status,
                started_at=started,
                completed_at=now,
                duration_seconds=duration,
                skills_used=req.skills or [],
                summary=exec_result.summary,
                error=exec_result.error,
                evaluation=eval_data,
                run_id=req.mode,
                sdk_metrics=sdk_metrics,
            )
            task_results.append(tr)
            self.progress.task_completed(tr)

        def on_error(req: TaskRequest, exc: Exception) -> None:
            now = datetime.now()
            started = start_times.get(req.task_id)
            duration = (now - started).total_seconds() if started else 0.0
            tr = TaskResult(
                task_id=req.task_id,
                status=TaskStatus.FAILED,
                started_at=started,
                completed_at=now,
                duration_seconds=duration,
                error=str(exc),
                run_id=req.mode,
            )
            task_results.append(tr)
            self.progress.task_completed(tr)

        raw_results = asyncio.run(
            run_batch(
                requests,
                max_parallel=self.config.parallel,
                on_task_start=on_start,
                on_task_complete=on_complete,
                on_task_error=on_error,
                continue_on_error=self.config.continue_on_error,
            )
        )

        # Handle cancelled tasks that bypassed callbacks
        # (when continue_on_error=False, remaining tasks are cancelled
        # without triggering on_task_start/on_task_error)
        processed_ids = {tr.task_id for tr in task_results}
        for req, result_or_exc in raw_results:
            if req.task_id not in processed_ids:
                now = datetime.now()
                started = start_times.get(req.task_id)
                duration = (now - started).total_seconds() if started else 0.0
                tr = TaskResult(
                    task_id=req.task_id,
                    status=TaskStatus.FAILED,
                    started_at=started,
                    completed_at=now,
                    duration_seconds=duration,
                    error=str(result_or_exc) if isinstance(result_or_exc, Exception) else None,
                    run_id=req.mode,
                )
                task_results.append(tr)
                self.progress.task_completed(tr)

        return task_results

    def _to_task_request(self, tc: TaskConfig) -> TaskRequest:
        """Convert a TaskConfig to a TaskRequest."""
        from config import get_config
        mode = get_config()._get("orchestrator")

        # When skill_mode="specified", pass skills explicitly so run_task() skips discovery
        skills = None
        if tc.skill_mode == "specified":
            skills = tc.skills
        elif mode == "no-skill":
            skills = []

        return TaskRequest(
            task=tc.description,
            skills=skills,
            mode=mode,
            skill_group=tc.skill_group,
            files=tc.files or None,
            task_name=tc.name,
            task_id=tc.task_id,
            base_dir=str(self.batch_dir),
            evaluators_config=tc.evaluators_config,
            aggregation_config=tc.aggregation_config,
        )

    def _save_batch_result(self, result: BatchResult) -> None:
        result_path = self.batch_dir / "batch_result.json"
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
