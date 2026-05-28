"""Freestyle execution engine — skills available, Claude decides how to use them.

No planning, no DAG. Claude directly executes the task with skills available
in the working directory.
"""

import asyncio
from pathlib import Path
from typing import Optional, Callable

from config import get_config
from orchestrator.runtime.client import SkillClient
from orchestrator.runtime.prompts import build_direct_executor_prompt
from orchestrator.runtime.run_context import RunContext
from loguru import logger as _logger
from logging_config import add_file_sink, map_level
from orchestrator.base import ExecutionResult, EngineRequest, EngineMeta
from orchestrator.registry import register_engine


UI_CONTRIBUTION = {
    "id": "freestyle",
    "partials": {
        "execute": "modules/orchestrator_freestyle/freestyle-execute.html",
    },
    "scripts": [
        "modules/orchestrator_freestyle/freestyle-execute.js",
    ],
    "modals": [
        "modules/orchestrator_dag/node-log-modal.html",
    ],
}


@register_engine("free-style")
class FreestyleEngine:
    """Skills available, Claude decides how to use them. No planning, no DAG."""

    ui_contribution = UI_CONTRIBUTION
    meta = EngineMeta(
        label="Free-Style",
        description="Let Claude decide which skills to call",
    )

    @classmethod
    def create(cls, *, run_context, skill_dir=None, log_callback=None, **kw):
        return cls(skill_dir=skill_dir, run_context=run_context, log_callback=log_callback)

    def __init__(
        self,
        skill_dir: Path,
        run_context: RunContext,
        log_callback: Optional[Callable[[str, str], None]] = None,
    ):
        self.skill_dir = Path(skill_dir)
        self.run_context = run_context
        self.log_callback = log_callback
        cfg = get_config()
        self._runtime = cfg.orchestrator_config("free-style").runtime

    async def run(self, request: EngineRequest) -> ExecutionResult:
        """Unified engine interface with optional visualizer support."""
        viz = request.visualizer
        if viz:
            auto_node = {
                "id": "FreeStyleExecution",
                "name": "FreeStyleExecution",
                "type": "primary",
                "depends_on": [],
                "purpose": "Claude directly executes the task using available skills",
                "outputs_summary": "Task output",
            }
            await viz.set_nodes([auto_node], [[auto_node["id"]]])
            await viz.update_status("FreeStyleExecution", "running")

        result = await self.execute(
            task=request.task,
            skills=request.skills,
            files=request.files,
            copy_all_skills=request.copy_all_skills,
        )

        if viz:
            status = "completed" if result.status == "completed" else "failed"
            await viz.update_status("FreeStyleExecution", status)

        return result

    async def execute(
        self,
        task: str,
        skills: list[str],
        files: Optional[list[str]] = None,
        copy_all_skills: bool = False,
    ) -> ExecutionResult:
        """Execute a task in freestyle mode.

        Args:
            task: Task description
            skills: List of skill names to make available
            files: Optional list of files to copy into workspace
            copy_all_skills: If True, copy all skills from skill_dir

        Returns:
            ExecutionResult with status and response
        """
        run_context = self.run_context

        # 1. Setup run context with skills
        await run_context.async_setup(skills, self.skill_dir, copy_all=copy_all_skills)

        # 2. Copy input files
        if files:
            await run_context.async_copy_files(files)

        # 3. Save metadata
        await run_context.async_save_meta(task, "free-style", skills, copy_all=copy_all_skills)

        # 4. Build prompt
        cwd = str(run_context.exec_dir)
        output_dir = run_context.workspace_dir

        prompt = build_direct_executor_prompt(
            task=task,
            output_dir=str(output_dir),
            working_dir=cwd,
        )

        # 5. Create file logger
        sink_key = f"freestyle-{run_context.run_id}"
        sink_id = add_file_sink(run_context.get_log_path("execution"), filter_key=sink_key)
        execution_logger = _logger.bind(sink_key=sink_key)
        execution_logger.info(f"{'='*60}\nTask: free-style execution\n{'='*60}")
        execution_logger.info(f"Description: {task}")
        execution_logger.info(f"Mode: free-style")
        if copy_all_skills:
            execution_logger.info(f"Skills: ALL (copy_all=True, {len(skills)} from discovery)")
        else:
            execution_logger.info(f"Skills: {', '.join(skills)}")
        execution_logger.info(f"{'-'*60}\nExecution Log\n{'-'*60}")

        def _log_callback(message: str, level: str = "info") -> None:
            execution_logger.log(map_level(level), message)
            if self.log_callback:
                self.log_callback(message, level)

        try:
            # 6. Execute with client
            async with SkillClient(
                session_id=f"freestyle-{run_context.run_id}",
                cwd=cwd,
                log_callback=_log_callback,
                model=self._runtime.model,
            ) as client:
                coro = client.execute(prompt)
                if self._runtime.execution_timeout > 0:
                    response = await asyncio.wait_for(coro, timeout=self._runtime.execution_timeout)
                else:
                    response = await coro

                sdk_metrics = client.last_result_metrics
                metrics_dict = sdk_metrics.to_dict() if sdk_metrics else None

                max_len = self._runtime.summary_max_length
                result = ExecutionResult(
                    status="completed",
                    summary=response[:max_len] if response else "",
                    metadata={"response": response, "sdk_metrics": metrics_dict},
                )

            # 7. Log completion and save result
            execution_logger.info(f"{'='*60}\nExecution Complete\n{'='*60}")
            execution_logger.success(f"Status: {result.status}")
            await run_context.async_save_result({
                "status": result.status,
                "response": response,
                "sdk_metrics": metrics_dict,
            })

            return result
        finally:
            await run_context.async_finalize()
            _logger.remove(sink_id)
