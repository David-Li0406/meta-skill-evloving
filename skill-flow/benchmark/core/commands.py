"""Harbor command building utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from benchmark.core.config import AgentBackend, EvalConfig, EvalMode

if TYPE_CHECKING:
    from pathlib import Path

_CODEX_AGENT = "benchmark.agents.skillflow_injection_agent:SkillFlowInjectionAgent"
_CLAUDE_AGENT = "benchmark.agents.skillflow_claude_code_agent:SkillFlowClaudeCodeAgent"
_DEFAULT_CODEX_VERSION = "0.112"


def _agent_base_args(config: EvalConfig) -> list[str]:
    """Return the agent import path + optional version pin for the backend.

    Codex defaults to a pinned CLI version; Claude Code installs the latest
    unless ``agent_version`` is set. Both accept the ``version`` kwarg.
    """
    if config.agent_backend == AgentBackend.CLAUDE_CODE:
        args = ["--agent-import-path", _CLAUDE_AGENT]
        if config.agent_version:
            args.extend(["--agent-kwarg", f'version="{config.agent_version}"'])
        return args
    version = config.agent_version or _DEFAULT_CODEX_VERSION
    return [
        "--agent-import-path",
        _CODEX_AGENT,
        "--agent-kwarg",
        f'version="{version}"',
    ]


def build_harbor_run_command(config: EvalConfig, job_name: str) -> list[str]:
    """Build the harbor run command.

    Args:
        config: Evaluation configuration
        job_name: Name for this evaluation job

    Returns:
        List of command arguments
    """
    # The apptainer backend isn't a built-in harbor env, so it must be
    # registered via our shim (which then hands off to harbor's CLI).
    if config.environment.resolved_backend == "apptainer":
        cmd = ["uv", "run", "python", "-m", "benchmark.scripts.harbor_apptainer", "run"]
    else:
        cmd = ["uv", "run", "harbor", "run"]
    cmd += [
        "--job-name",
        job_name,
        "--jobs-dir",
        str(config.jobs_dir),
        "--n-concurrent",
        str(config.environment.n_concurrent),
    ]

    # Add mode-specific arguments
    cmd.extend(build_mode_args(config))

    # Add task filter arguments
    cmd.extend(build_task_args(config))

    # Add benchmark source (dataset name or local tasks path)
    if config.tasks_path:
        cmd.extend(["-p", str(config.tasks_path)])
    elif config.dataset:
        cmd.extend(["--dataset", config.dataset])

    # Add environment backend. apptainer runs through the shim which remaps the
    # harbor "docker" slot to ApptainerEnvironment, so it passes --env docker.
    backend = config.environment.resolved_backend
    cmd.extend(["--env", "docker" if backend == "apptainer" else backend])
    if backend == "docker" and config.environment.force_build:
        cmd.append("--force-build")

    return cmd


def build_mode_args(config: EvalConfig) -> list[str]:
    """Build mode-specific command arguments.

    Args:
        config: Evaluation configuration

    Returns:
        List of mode-specific arguments
    """
    if config.mode == EvalMode.SKILLFLOW_INJECTION:
        return _build_skillflow_injection_args(config)

    if config.mode == EvalMode.SKILLFLOW_CACHED:
        return _build_skillflow_cached_args(config)

    if config.mode == EvalMode.MCP:
        return _build_mcp_args(config)

    if config.mode == EvalMode.BASELINE:
        return _build_baseline_args(config)

    # Skills mode
    return _build_skills_args(config)


def _add_reasoning_effort(args: list[str], config: EvalConfig) -> None:
    """Add reasoning_effort + other Claude Code agent kwargs if configured."""
    if config.reasoning_effort:
        args.extend(["--agent-kwarg", f"reasoning_effort={config.reasoning_effort}"])
    if config.thinking:
        args.extend(["--agent-kwarg", f"thinking={config.thinking}"])
    if config.max_thinking_tokens is not None:
        args.extend(["--agent-kwarg", f"max_thinking_tokens={config.max_thinking_tokens}"])
    if config.max_turns is not None:
        args.extend(["--agent-kwarg", f"max_turns={config.max_turns}"])


def _build_skillflow_cached_args(config: EvalConfig) -> list[str]:
    """Build arguments for cached SkillFlow mode."""
    assert config.selector_cache
    args = [
        "--agent-import-path",
        "benchmark.agents.skillflow_mcp_cached_agent:SkillFlowMCPCachedAgent",
        "--agent-kwarg",
        'version="0.112"',
        "--agent-kwarg",
        f"mcp_url={config.mcp_url}",
        "--agent-kwarg",
        f"selector_cache={config.selector_cache}",
    ]
    _add_reasoning_effort(args, config)
    args.extend(["--model", config.model])
    return args


def _build_mcp_args(config: EvalConfig) -> list[str]:
    """Build arguments for MCP test mode."""
    args = [
        "--agent-import-path",
        "benchmark.agents.skillflow_mcp_agent:SkillFlowMCPAgent",
        "--agent-kwarg",
        'version="0.112"',
        "--agent-kwarg",
        f"mcp_url={config.mcp_url}",
    ]
    _add_reasoning_effort(args, config)
    args.extend(["--model", config.model])
    return args


def _build_skillflow_injection_args(config: EvalConfig) -> list[str]:
    """Build arguments for SkillFlow injection mode."""
    args = _agent_base_args(config)
    if config.eval_results:
        args.extend(["--agent-kwarg", f"eval_results={config.eval_results}"])
    if config.selector_cache:
        args.extend(["--agent-kwarg", f"selector_cache={config.selector_cache}"])
    if config.tasks_dir_for_skills:
        args.extend(["--agent-kwarg", f"tasks_dir={config.tasks_dir_for_skills}"])
    if config.corpus_dir:
        args.extend(["--agent-kwarg", f"corpus_dir={config.corpus_dir}"])
    _add_reasoning_effort(args, config)
    args.extend(["--model", config.model])
    return args


def _build_baseline_args(config: EvalConfig) -> list[str]:
    """Build arguments for baseline mode."""
    args = _agent_base_args(config)
    _add_reasoning_effort(args, config)
    args.extend(["--model", config.model])
    return args


def _build_skills_args(config: EvalConfig) -> list[str]:
    """Build arguments for skills mode."""
    assert config.skills
    args = _agent_base_args(config)
    args.extend(["--agent-kwarg", f"skills_dir={config.skills.skills_dir}"])

    if config.skills.match_skill_to_task:
        args.extend(["--agent-kwarg", "match_skill_to_task=True"])

    _add_reasoning_effort(args, config)
    args.extend(["--model", config.model])
    return args


def build_task_args(config: EvalConfig) -> list[str]:
    """Build task filter arguments.

    Args:
        config: Evaluation configuration

    Returns:
        List of task filter arguments
    """
    args: list[str] = []
    all_tasks = config.tasks.get_all_tasks()

    if all_tasks:
        for task in all_tasks:
            args.extend(["--task-name", task])
    else:
        # Apply exclude tasks only when not filtering
        for task in config.tasks.exclude_tasks:
            args.extend(["--exclude-task-name", task])

    return args


def build_resume_command(job_path: Path) -> list[str]:
    """Build the harbor resume command.

    Args:
        job_path: Path to the job directory

    Returns:
        List of command arguments
    """
    return ["uv", "run", "harbor", "jobs", "resume", "--job-path", str(job_path)]


def build_retry_errors_command(job_path: Path, error_types: list[str]) -> list[str]:
    """Build the harbor retry errors command.

    Args:
        job_path: Path to the job directory
        error_types: List of error types to retry

    Returns:
        List of command arguments
    """
    cmd = ["uv", "run", "harbor", "jobs", "resume", "--job-path", str(job_path)]
    for error_type in error_types:
        cmd.extend(["--filter-error-type", error_type])
    return cmd
