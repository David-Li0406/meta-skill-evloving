"""Task and batch configuration loader."""

import glob
import json
from pathlib import Path
from typing import Optional

import yaml
from loguru import logger

from .models import TaskConfig, BatchConfig


def scan_completed_tasks(batch_dir: Path) -> dict[str, dict]:
    """Scan batch directory for successfully completed tasks.

    A task is considered completed if its subdirectory contains:
    - meta.json with a task_id and non-null completed_at
    - result.json with status == "completed"

    Failed or partially written tasks are treated as incomplete.

    Args:
        batch_dir: Path to the batch output directory

    Returns:
        dict mapping task_id -> {run_id, meta, result, evaluation}
    """
    completed = {}
    if not batch_dir.is_dir():
        return completed

    for sub in sorted(batch_dir.iterdir()):
        if not sub.is_dir():
            continue
        try:
            meta_path = sub / "meta.json"
            result_path = sub / "result.json"
            if not meta_path.exists() or not result_path.exists():
                continue

            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            with open(result_path, "r", encoding="utf-8") as f:
                result = json.load(f)

            task_id = meta.get("task_id")
            if not task_id:
                # Derive task_id from run_id
                # Format: YYYYMMDD-HHMMSS-mode-taskid-hash (hash is 6 hex chars)
                # Mode may contain hyphens (e.g. free-style, no-skill),
                # but task_id always contains underscores while mode never does.
                # Find the first segment after timestamp that contains '_'.
                run_id = meta.get("run_id", "")
                parts = run_id.split("-")
                if len(parts) >= 5:
                    task_start = None
                    for i in range(2, len(parts) - 1):
                        if "_" in parts[i]:
                            task_start = i
                            break
                    if task_start is not None:
                        task_id = "-".join(parts[task_start:-1])
            if not task_id:
                continue

            if result.get("status") != "completed":
                continue
            if not meta.get("completed_at"):
                continue

            entry = {
                "run_id": meta.get("run_id", sub.name),
                "meta": meta,
                "result": result,
                "evaluation": None,
            }

            eval_path = sub / "evaluation.json"
            if eval_path.exists():
                with open(eval_path, "r", encoding="utf-8") as f:
                    entry["evaluation"] = json.load(f)

            completed[task_id] = entry
        except (json.JSONDecodeError, OSError, KeyError) as e:
            logger.debug(f"Skipping incomplete task dir {sub.name}: {e}")
            continue

    return completed


class TaskLoader:
    """Load task configurations from JSON files and YAML batch configs.

    Supports:
    - Loading single JSON task files
    - Loading YAML batch configuration files
    - Directory scanning with glob patterns
    - Configuration merging and override
    """

    # Default values for task parameters
    DEFAULTS = {
        "skill_mode": "auto",
        "skill_group": "skill_seeds",
        "output_dir": "./runs",
        "continue_on_error": True,
    }

    def __init__(self, base_dir: Optional[str] = None):
        """Initialize TaskLoader.

        Args:
            base_dir: Base directory for resolving relative paths
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()

    def load_task_file(self, file_path: str | Path, overrides: dict = None) -> TaskConfig:
        """Load a single task from a JSON file.

        Args:
            file_path: Path to the JSON task file
            overrides: Optional parameter overrides

        Returns:
            TaskConfig instance
        """
        path = self._resolve_path(file_path)
        return TaskConfig.from_json_file(path, overrides)

    def load_batch_config(self, config_path: str | Path) -> BatchConfig:
        """Load a batch configuration from a YAML file.

        Args:
            config_path: Path to the YAML batch config file

        Returns:
            BatchConfig instance
        """
        path = self._resolve_path(config_path)

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Extract global defaults
        defaults = data.get("defaults", {})
        merged_defaults = {**self.DEFAULTS, **defaults}

        # Extract execution settings
        execution = data.get("execution", {})
        parallel = execution.get("parallel", 1)
        retry_failed = execution.get("retry_failed", 0)

        # Process task list
        tasks = []
        for task_entry in data.get("tasks", []):
            task_configs = self._process_task_entry(task_entry, merged_defaults, path.parent)
            tasks.extend(task_configs)

        # Generate batch ID with timestamp suffix for uniqueness and sorting
        base_batch_id = data.get("batch_id")
        if base_batch_id:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_id = f"{base_batch_id}_{timestamp}"
        else:
            batch_id = BatchConfig.generate_batch_id()

        # Resolve optional config_file (relative to YAML directory)
        config_file = data.get("config_file")
        if config_file:
            config_file = str(self._resolve_path(config_file, path.parent))

        return BatchConfig(
            batch_id=batch_id,
            tasks=tasks,
            parallel=parallel,
            output_dir=merged_defaults.get("output_dir", "./runs"),
            continue_on_error=merged_defaults.get("continue_on_error", True),
            retry_failed=retry_failed,
            defaults=merged_defaults,
            config_file=config_file,
        )

    def _process_task_entry(
        self, entry: dict, defaults: dict, config_dir: Path
    ) -> list[TaskConfig]:
        """Process a single task entry from the YAML config.

        Supports three types:
        1. file: reference to a JSON task file
        2. dir: directory scan with pattern
        3. inline: inline task definition

        Args:
            entry: Task entry from YAML
            defaults: Default parameters
            config_dir: Directory of the config file (for relative paths)

        Returns:
            List of TaskConfig instances
        """
        # Build overrides from entry + defaults
        overrides = self._build_overrides(entry, defaults)

        if "file" in entry:
            file_ref = entry["file"]
            # Support benchmark:// URI (e.g. benchmark://AgentSkillOS_bench/task.json)
            if isinstance(file_ref, str) and file_ref.startswith("benchmark://"):
                file_path = self._resolve_benchmark_uri(file_ref)
            else:
                file_path = self._resolve_path(file_ref, config_dir)
            return [TaskConfig.from_json_file(file_path, overrides)]

        elif "benchmark" in entry:
            # Scan an entire benchmark: benchmark: AgentSkillOS_bench
            return self._scan_benchmark(entry, overrides)

        elif "dir" in entry:
            # Directory scan
            return self._scan_directory(entry, overrides, config_dir)

        else:
            # Inline task definition
            return [self._create_inline_task(entry, overrides)]

    def _build_overrides(self, entry: dict, defaults: dict) -> dict:
        """Build parameter overrides from entry and defaults.

        Priority: entry values > defaults

        Args:
            entry: Task entry from YAML
            defaults: Default parameters

        Returns:
            Dict of override parameters
        """
        overrides = {}

        # Deprecation warning: mode should be set via config.yaml orchestrator
        if "mode" in entry:
            logger.opt(once=True).warning(
                "Task-level 'mode' in batch YAML is deprecated and ignored. "
                "Use config.yaml 'orchestrator' instead."
            )
        if "mode" in defaults:
            logger.opt(once=True).warning(
                "defaults.mode in batch YAML is deprecated and ignored. "
                "Use config.yaml 'orchestrator' instead."
            )

        # skill_mode flag
        if "skill_mode" in entry:
            overrides["skill_mode"] = entry["skill_mode"]
        elif "skill_mode" in defaults:
            overrides["skill_mode"] = defaults["skill_mode"]

        # Skills list
        if "skills" in entry:
            overrides["skills"] = entry["skills"]
            overrides["skill_mode"] = "specified"  # Explicit skills implies specified
        elif "skills" in defaults:
            overrides["skills"] = defaults["skills"]

        # Skill group
        if "skill_group" in entry:
            overrides["skill_group"] = entry["skill_group"]
        elif "skill_group" in defaults:
            overrides["skill_group"] = defaults["skill_group"]

        return overrides

    def _scan_directory(
        self, entry: dict, overrides: dict, config_dir: Path
    ) -> list[TaskConfig]:
        """Scan a directory for task files matching a pattern.

        Args:
            entry: Directory entry with 'dir' and optional 'pattern'
            overrides: Parameter overrides
            config_dir: Directory of the config file

        Returns:
            List of TaskConfig instances
        """
        dir_path = self._resolve_path(entry["dir"], config_dir)
        pattern = entry.get("pattern", "*.json")

        # Use glob to find matching files
        full_pattern = str(dir_path / pattern)
        matching_files = sorted(glob.glob(full_pattern))

        tasks = []
        for file_path in matching_files:
            try:
                task = TaskConfig.from_json_file(file_path, overrides)
                tasks.append(task)
            except (json.JSONDecodeError, KeyError) as e:
                # Log warning but continue with other files
                logger.warning(f"Failed to load {file_path}: {e}")

        return tasks

    def _create_inline_task(self, entry: dict, overrides: dict) -> TaskConfig:
        """Create a TaskConfig from an inline definition.

        Args:
            entry: Inline task entry
            overrides: Parameter overrides

        Returns:
            TaskConfig instance
        """
        task_id = entry.get("id", f"inline_{id(entry)}")
        name = entry.get("name", task_id)
        description = entry.get("description", "")
        category = entry.get("category", "general")
        files = entry.get("files", [])

        return TaskConfig(
            task_id=task_id,
            name=name,
            description=description,
            category=category,
            files=files,
            skill_mode=overrides.get("skill_mode", "auto"),
            skills=overrides.get("skills", []),
            skill_group=overrides.get("skill_group", "skill_seeds"),
        )

    def _resolve_benchmark_uri(self, uri: str) -> Path:
        """Resolve a benchmark:// URI to an absolute task file path.

        Format: benchmark://BENCH_NAME/task_filename.json

        Args:
            uri: URI string starting with ``benchmark://``

        Returns:
            Resolved Path to the task file
        """
        from benchmark import resolve_task_file

        stripped = uri[len("benchmark://"):]
        parts = stripped.split("/", 1)
        if len(parts) != 2:
            raise ValueError(
                f"Invalid benchmark URI '{uri}'. "
                "Expected format: benchmark://BENCH_NAME/filename.json"
            )
        bench_name, filename = parts
        return resolve_task_file(bench_name, filename)

    def _scan_benchmark(self, entry: dict, overrides: dict) -> list[TaskConfig]:
        """Scan all task files from a registered benchmark.

        YAML example::

            - benchmark: AgentSkillOS_bench
              pattern: "*.json"

        Args:
            entry: Task entry dict with ``benchmark`` key.
            overrides: Parameter overrides.

        Returns:
            List of TaskConfig instances.
        """
        import glob as globmod
        from benchmark import get_benchmark

        bench_name = entry["benchmark"]
        bench = get_benchmark(bench_name)
        pattern = entry.get("pattern", "*.json")
        full_pattern = str(bench.tasks_dir / pattern)
        matching_files = sorted(globmod.glob(full_pattern))

        tasks = []
        for file_path in matching_files:
            try:
                task = TaskConfig.from_json_file(file_path, overrides)
                tasks.append(task)
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to load {file_path}: {e}")
        return tasks

    def _resolve_path(self, path: str | Path, relative_to: Path = None) -> Path:
        """Resolve a path, handling relative paths.

        Args:
            path: Path to resolve
            relative_to: Directory to resolve relative paths against

        Returns:
            Resolved Path
        """
        p = Path(path)
        if p.is_absolute():
            return p

        base = relative_to if relative_to else self.base_dir
        return (base / p).resolve()

    def validate_batch_config(self, config: BatchConfig) -> list[str]:
        """Validate a batch configuration.

        Args:
            config: BatchConfig to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not config.tasks:
            errors.append("No tasks defined in batch configuration")

        for task in config.tasks:
            # Check that description is not empty
            if not task.description:
                errors.append(f"Task {task.task_id}: description (question) is required")

            # Check skills are specified when skill_mode is "specified"
            # (direct manager provides all skills, so this check is skipped)
            from config import get_config
            if task.skill_mode == "specified" and not task.skills and get_config().manager != "direct":
                errors.append(
                    f"Task {task.task_id}: skills must be specified when skill_mode is 'specified'"
                )

        return errors
