"""Core workflow: search skills → create run context → run engine.

No UI dependencies — usable from both Web and CLI adapters.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Callable

from loguru import logger

from constants import resolve_skill_group
from manager import create_manager
from orchestrator.base import EngineRequest, ExecutionResult
from orchestrator.registry import create_engine
from orchestrator.runtime.run_context import RunContext
from orchestrator.visualizers import NullVisualizer

from .models import TaskRequest, EventCallback


def discover_skills(
    task_description: str,
    skill_group: str = "skill_seeds",
    event_callback: Optional[EventCallback] = None,
) -> list[str]:
    """Search for relevant skills using the manager.

    Args:
        task_description: The task to search skills for.
        skill_group: Skill group ID.
        event_callback: Optional callback for search progress events.

    Returns:
        List of skill IDs.
    """
    group = resolve_skill_group(skill_group)
    tree_path = group.get("tree_path")
    vector_db_path = group.get("vector_db_path")

    manager = create_manager(
        tree_path=tree_path,
        vector_db_path=vector_db_path,
        event_callback=event_callback,
    )
    result = manager.search(task_description, verbose=False)
    # Limit skills returned based on max_skills config
    from config import get_config
    cfg = get_config()
    return [s["id"] for s in result.selected_skills][:cfg.max_skills]


async def run_task(
    request: TaskRequest,
    on_event: Optional[EventCallback] = None,
) -> ExecutionResult:
    """Execute a single task through the full workflow.

    Steps:
        1. Resolve skill group
        2. Discover skills (if not pre-specified)
        3. Create RunContext
        4. Instantiate engine via registry
        5. Run engine

    Args:
        request: Task request parameters.
        on_event: Optional progress callback.

    Returns:
        ExecutionResult from the engine.
    """
    # 1. Resolve skill group → get skill_dir
    group = resolve_skill_group(request.skill_group)
    skill_dir = Path(group["skills_dir"])

    # 2. Discover skills (if needed)
    from config import get_config
    cfg = get_config()

    if request.skills is not None:
        skills = request.skills
    elif request.mode == "no-skill":
        skills = []
    elif cfg.manager == "direct":
        skills = []
        logger.info("manager=direct: skipping skill discovery, all skills will be copied")
    else:
        if on_event:
            on_event("search_start", {"task": request.task})
        skills = discover_skills(
            request.task,
            skill_group=request.skill_group,
            event_callback=on_event,
        )
        if on_event:
            on_event("search_complete", {"skills": skills})

    if cfg.manager == "direct" and cfg.max_skills:
        logger.warning(
            f"max_skills={cfg.max_skills} is configured but will not be enforced: "
            f"manager=direct copies all skills to the execution environment"
        )

    # 3. Create RunContext
    run_context = RunContext.create(
        task=request.task,
        mode=request.mode,
        task_name=request.task_name or None,
        task_id=request.task_id,
        base_dir=request.base_dir or "runs",
    )

    # 4. Build engine via registry
    engine = create_engine(
        request.mode,
        run_context=run_context,
        skill_dir=skill_dir,
        allowed_tools=request.allowed_tools,
    )

    # 5. Build EngineRequest and run
    if request.visualizer:
        visualizer = request.visualizer
    else:
        # Read batch_auto_plan from DAG orchestrator config
        dag_cfg = cfg.orchestrator_config("dag")
        auto_plan = dag_cfg.batch_auto_plan if dag_cfg else 0
        visualizer = NullVisualizer(auto_select_plan=auto_plan)
    should_copy_all = request.copy_all_skills or (cfg.manager == "direct")

    engine_request = EngineRequest(
        task=request.task,
        skills=skills,
        files=request.files,
        visualizer=visualizer,
        copy_all_skills=should_copy_all,
        allowed_tools=request.allowed_tools,
    )

    result = await engine.run(engine_request)

    # Auto-evaluate if evaluators are configured
    if request.evaluators_config:
        try:
            from .evaluation import evaluate_workspace
            eval_result = await evaluate_workspace(
                evaluators_config=request.evaluators_config,
                aggregation_config=request.aggregation_config,
                workspace_path=run_context.run_dir / "workspace",
                task_id=request.task_id or "",
            )
            if eval_result:
                result.metadata["evaluation"] = eval_result.to_dict()
        except Exception as e:
            logger.warning(f"Evaluation failed for {request.task_id}: {e}")

    if on_event:
        on_event("execution_complete", {
            "status": result.status,
            "error": result.error,
        })

    return result
