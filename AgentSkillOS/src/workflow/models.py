"""Workflow data models."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from constants import TaskStatus, EventCallback


@dataclass
class TaskRequest:
    """Standardized request for a single workflow task."""

    task: str
    skills: Optional[list[str]] = None  # Pre-selected skills (skip search if set)
    mode: str = "dag"  # "dag" | "free-style" | "no-skill"
    skill_group: str = "skill_seeds"
    files: Optional[list[str]] = None
    task_name: str = ""
    # DAG-specific: visualizer instance (VisualizerProtocol)
    visualizer: Optional[object] = None
    # Freestyle-specific
    copy_all_skills: bool = False
    # Direct/baseline-specific
    allowed_tools: Optional[list[str]] = None
    # Batch-specific: custom base_dir and task_id for RunContext
    base_dir: Optional[str] = None
    task_id: Optional[str] = None
    # Evaluation config (from benchmark task JSON)
    evaluators_config: list[dict] = field(default_factory=list)
    aggregation_config: dict = field(default_factory=dict)



@dataclass
class TaskConfig:
    """Configuration for a single task.

    Attributes:
        task_id: Unique identifier for the task
        name: Display name for the task
        description: Task description (question for the agent)
        category: Task category
        files: List of input files to copy to workspace
        skill_mode: "auto" = auto-discover skills, "specified" = use user-specified skills
        skills: List of skill names (when skill_mode="specified")
        skill_group: Skill group to use for search
        source_file: Path to the source JSON file (if loaded from file)
    """

    task_id: str
    name: str
    description: str
    category: str = "general"
    files: list[str] = field(default_factory=list)
    skill_mode: str = "auto"  # "auto" | "specified"
    skills: list[str] = field(default_factory=list)
    skill_group: str = "skill_seeds"
    source_file: Optional[str] = None
    evaluators_config: list[dict] = field(default_factory=list)
    aggregation_config: dict = field(default_factory=dict)

    @classmethod
    def from_json_file(cls, file_path: str | Path, overrides: dict = None) -> "TaskConfig":
        """Create TaskConfig from a JSON task file.

        Args:
            file_path: Path to the JSON task file
            overrides: Optional dict of parameters to override

        Returns:
            TaskConfig instance
        """
        import json

        path = Path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Build base config from JSON (benchmark task format)
        # Resolve file paths relative to the JSON file's directory
        raw_files = data.get("files", [])
        resolved_files = []
        for f in raw_files:
            fp = Path(f)
            if not fp.is_absolute():
                fp = (path.parent / f).resolve()
            resolved_files.append(str(fp))

        # Auto-discover task_data for benchmark tasks
        # Convention: .../tasks/xxx.json -> .../task_data/xxx/
        task_id = data.get("task_id", path.stem)
        task_data_dir = path.parent.parent / "task_data" / task_id
        if task_data_dir.is_dir() and path.parent.name == "tasks":
            for item in task_data_dir.iterdir():
                resolved_files.append(str(item.resolve()))

        config = {
            "task_id": task_id,
            "name": data.get("task_name") or data.get("name", task_id),
            "description": data.get("prompt") or data.get("question", ""),
            "category": data.get("category", "general"),
            "files": resolved_files,
            "source_file": str(path),
            "evaluators_config": data.get("evaluators", []),
            "aggregation_config": data.get("aggregation", {}),
        }

        # Benchmark "skills" field as default (when no explicit override)
        sb_skills = data.get("skills", [])
        if sb_skills and not (overrides and "skills" in overrides):
            config["skills"] = sb_skills
            config["skill_mode"] = "specified"

        # Apply overrides (from YAML batch config)
        if overrides:
            for key in ["skill_mode", "skills", "skill_group"]:
                if key in overrides:
                    config[key] = overrides[key]

        return cls(**config)


@dataclass
class TaskResult:
    """Result of a single task execution.

    Attributes:
        task_id: Task identifier
        status: Final status
        run_id: Run context ID (folder name in runs/)
        output_dir: Path to output directory
        started_at: Execution start time
        completed_at: Execution completion time
        duration_seconds: Total execution time
        error: Error message if failed
        skills_used: List of skills that were used
        summary: Brief summary of execution
    """

    task_id: str
    status: TaskStatus
    run_id: Optional[str] = None
    output_dir: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    error: Optional[str] = None
    skills_used: list[str] = field(default_factory=list)
    summary: str = ""
    evaluation: Optional[dict] = None  # EvaluationResult.to_dict()
    sdk_metrics: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        d = {
            "task_id": self.task_id,
            "status": self.status.value,
            "run_id": self.run_id,
            "output_dir": self.output_dir,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "error": self.error,
            "skills_used": self.skills_used,
            "summary": self.summary,
            "evaluation": self.evaluation,
        }
        if self.sdk_metrics:
            d["sdk_metrics"] = self.sdk_metrics
        return d


@dataclass
class BatchConfig:
    """Configuration for batch execution.

    Attributes:
        batch_id: Unique identifier for this batch run
        tasks: List of task configurations
        parallel: Maximum parallel tasks
        output_dir: Base output directory
        continue_on_error: Whether to continue when a task fails
        retry_failed: Number of retries for failed tasks
        defaults: Default parameters for tasks
    """

    batch_id: str
    tasks: list[TaskConfig]
    parallel: int = 1
    output_dir: str = "./runs"
    continue_on_error: bool = True
    retry_failed: int = 0
    defaults: dict = field(default_factory=dict)
    config_file: Optional[str] = None

    @classmethod
    def generate_batch_id(cls) -> str:
        """Generate a unique batch ID based on timestamp."""
        return f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


@dataclass
class BatchResult:
    """Result of batch execution.

    Attributes:
        batch_id: Batch identifier
        started_at: Batch start time
        completed_at: Batch completion time
        duration_seconds: Total batch execution time
        total: Total number of tasks
        completed: Number of completed tasks
        failed: Number of failed tasks
        skipped: Number of skipped tasks
        task_results: Results for each task
        output_dir: Path to batch output directory
    """

    batch_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    total: int = 0
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    task_results: list[TaskResult] = field(default_factory=list)
    output_dir: str = ""
    eval_total: int = 0
    eval_passed: int = 0
    avg_eval_score: float = 0.0
    total_cost_usd: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "batch_id": self.batch_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "total": self.total,
            "completed": self.completed,
            "failed": self.failed,
            "skipped": self.skipped,
            "task_results": [r.to_dict() for r in self.task_results],
            "output_dir": self.output_dir,
            "eval_total": self.eval_total,
            "eval_passed": self.eval_passed,
            "avg_eval_score": self.avg_eval_score,
            "total_cost_usd": self.total_cost_usd,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
        }
