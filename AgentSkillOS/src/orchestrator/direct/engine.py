"""Direct execution engine — no skills, Claude with base tools only."""

import asyncio
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
    "id": "direct",
    "partials": {
        "execute": "modules/orchestrator_direct/direct-execute.html",
    },
    "scripts": [
        "modules/orchestrator_direct/direct-execute.js",
    ],
    "modals": [
        "modules/orchestrator_dag/node-log-modal.html",
    ],
}


@register_engine("no-skill")
class DirectEngine:
    """No skills. Claude with base tools only."""

    ui_contribution = UI_CONTRIBUTION
    meta = EngineMeta(
        label="Baseline",
        description="Claude with base tools only, no skills",
        folder_mode="baseline",
        aliases=("baseline",),
    )

    @classmethod
    def create(cls, *, run_context, log_callback=None, allowed_tools=None, **kw):
        return cls(run_context=run_context, log_callback=log_callback, allowed_tools=allowed_tools)

    def __init__(
        self,
        run_context: RunContext,
        log_callback: Optional[Callable[[str, str], None]] = None,
        allowed_tools: Optional[list[str]] = None,
    ):
        self.run_context = run_context
        self.log_callback = log_callback
        self.allowed_tools = allowed_tools
        cfg = get_config()
        self._runtime = cfg.orchestrator_config("no-skill").runtime

    async def run(self, request: EngineRequest) -> ExecutionResult:
        """Unified engine interface with optional visualizer support."""
        viz = request.visualizer
        if viz:
            auto_node = {
                "id": "DirectExecution",
                "name": "DirectExecution",
                "type": "primary",
                "depends_on": [],
                "purpose": "Claude completes the task with base tools only",
                "outputs_summary": "Task output",
            }
            await viz.set_nodes([auto_node], [[auto_node["id"]]])
            await viz.update_status("DirectExecution", "running")

        result = await self.execute(
            task=request.task,
            files=request.files,
        )

        if viz:
            status = "completed" if result.status == "completed" else "failed"
            await viz.update_status("DirectExecution", status)

        return result

    async def execute(
        self,
        task: str,
        files: Optional[list[str]] = None,
    ) -> ExecutionResult:
        """Execute a task directly without skills.

        Args:
            task: Task description
            files: Optional list of files to copy into workspace

        Returns:
            ExecutionResult with status and response
        """
        run_context = self.run_context

        # 1. Setup run context without skills
        await run_context.async_setup([], run_context.run_dir, copy_all=False)

        # 2. Copy input files
        if files:
            await run_context.async_copy_files(files)

        # 3. Save metadata
        await run_context.async_save_meta(task, "no-skill", [])

        # 4. Build prompt
        cwd = str(run_context.exec_dir)
        output_dir = run_context.workspace_dir

        prompt = build_direct_executor_prompt(
            task=task,
            output_dir=str(output_dir),
            working_dir=cwd,
        )

        # 5. Create file logger
        sink_key = f"direct-{run_context.run_id}"
        sink_id = add_file_sink(run_context.get_log_path("execution"), filter_key=sink_key)
        execution_logger = _logger.bind(sink_key=sink_key)
        execution_logger.info(f"{'='*60}\nTask: direct execution\n{'='*60}")
        execution_logger.info(f"Description: {task}")
        execution_logger.info(f"Mode: no-skill")
        execution_logger.info("Skills: (none)")
        execution_logger.info(f"{'-'*60}\nExecution Log\n{'-'*60}")

        def _log_callback(message: str, level: str = "info") -> None:
            execution_logger.log(map_level(level), message)
            if self.log_callback:
                self.log_callback(message, level)

        try:
            # 6. Execute with client
            client_kwargs = {
                "session_id": f"direct-{run_context.run_id}",
                "cwd": cwd,
                "log_callback": _log_callback,
                "model": self._runtime.model,
            }
            if self.allowed_tools is not None:
                client_kwargs["allowed_tools"] = self.allowed_tools

            async with SkillClient(**client_kwargs) as client:
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
