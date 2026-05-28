"""Rich-based progress manager for batch execution."""

import threading
from datetime import datetime
from typing import Optional

from loguru import logger
import rich.box
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.table import Table
from rich.text import Text

from config import get_config
from .models import TaskConfig, TaskResult, TaskStatus, BatchResult


class BatchProgressManager:
    """Rich-based progress display for batch task execution.

    Provides a real-time terminal UI showing:
    - Overall batch progress
    - Running tasks with details
    - Completed/failed task history

    Note: Detailed logs are written to files, not displayed in terminal.
    """

    MAX_COMPLETED_DISPLAY = 20

    def __init__(self, batch_id: str, total_tasks: int, console: Optional[Console] = None, search_enabled: bool = True):
        """Initialize the progress manager.

        Args:
            batch_id: Unique identifier for this batch
            total_tasks: Total number of tasks
            console: Optional Rich Console instance
        """
        self.batch_id = batch_id
        self.total_tasks = total_tasks
        self.console = console or Console()

        # Thread lock for concurrent access
        self._lock = threading.Lock()

        # Task tracking
        self.pending_tasks: list[TaskConfig] = []
        self.running_tasks: dict[str, dict] = {}  # task_id -> {config, start_time, phase, ...}
        self.completed_tasks: list[TaskResult] = []
        self.failed_tasks: list[TaskResult] = []

        # Counters
        self.completed_count = 0
        self.failed_count = 0
        self.skipped_count = 0

        # Rich components
        self.live: Optional[Live] = None
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
            expand=True,
        )
        self.overall_task: Optional[TaskID] = None

        # Config names for display
        self.manager_name = get_config()._get("manager")
        self.orchestrator_name = get_config()._get("orchestrator")
        self.search_enabled = search_enabled

        # Timing
        self.start_time: Optional[datetime] = None

        # Background refresh thread
        self._refresh_thread: Optional[threading.Thread] = None
        self._stop_refresh = threading.Event()

    def _refresh_loop(self) -> None:
        """Background thread to periodically refresh the display."""
        while not self._stop_refresh.is_set():
            if self.live:
                try:
                    self.live.update(self._build_layout())
                except Exception as e:
                    logger.debug(f"Progress display refresh failed: {e}")
            self._stop_refresh.wait(0.25)  # Refresh every 0.25 seconds

    def start(self) -> None:
        """Start the live display."""
        self.start_time = datetime.now()
        self.overall_task = self.progress.add_task(
            f"[bold blue]Batch Progress[/bold blue]",
            total=self.total_tasks,
        )
        self.live = Live(
            self._build_layout(),
            console=self.console,
            refresh_per_second=4,
            transient=False,
        )
        self.live.start()

        # Start background refresh thread
        self._stop_refresh.clear()
        self._refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._refresh_thread.start()

    def stop(self) -> None:
        """Stop the live display."""
        # Stop the background refresh thread
        self._stop_refresh.set()
        if self._refresh_thread:
            self._refresh_thread.join(timeout=1)
            self._refresh_thread = None

        if self.live:
            self.live.stop()
            self.live = None

    def set_resumed_count(self, count: int) -> None:
        """Pre-advance progress for previously completed tasks."""
        self.completed_count = count
        if self.overall_task is not None:
            self.progress.update(self.overall_task, completed=count)

    def set_pending_tasks(self, tasks: list[TaskConfig]) -> None:
        """Set the list of pending tasks.

        Args:
            tasks: List of pending TaskConfig instances
        """
        self.pending_tasks = list(tasks)
        self._update_display()

    def task_started(self, task: TaskConfig) -> None:
        """Mark a task as started.

        Args:
            task: The task that started
        """
        with self._lock:
            # Remove from pending
            self.pending_tasks = [t for t in self.pending_tasks if t.task_id != task.task_id]

            # Add to running
            self.running_tasks[task.task_id] = {
                "config": task,
                "start_time": datetime.now(),
                "phase": "Starting",
                "progress": 0,
            }

        self._update_display()

    def task_phase_update(self, task_id: str, phase: str, progress: int = 0) -> None:
        """Update the current phase of a running task.

        Args:
            task_id: Task identifier
            phase: Current phase description
            progress: Optional progress percentage (0-100)
        """
        with self._lock:
            if task_id in self.running_tasks:
                self.running_tasks[task_id]["phase"] = phase
                self.running_tasks[task_id]["progress"] = progress
        self._update_display()

    def task_completed(self, result: TaskResult) -> None:
        """Mark a task as completed.

        Args:
            result: The task result
        """
        with self._lock:
            # Remove from running
            if result.task_id in self.running_tasks:
                del self.running_tasks[result.task_id]

            if result.status == TaskStatus.COMPLETED:
                self.completed_tasks.append(result)
                self.completed_count += 1
            elif result.status == TaskStatus.FAILED:
                self.failed_tasks.append(result)
                self.failed_count += 1
            else:
                self.skipped_count += 1

        # Update overall progress
        self.progress.update(
            self.overall_task,
            completed=self.completed_count + self.failed_count + self.skipped_count,
        )
        self._update_display()

    def _update_display(self) -> None:
        """Update the live display."""
        if self.live:
            self.live.update(self._build_layout())

    def _build_layout(self) -> Panel:
        """Build the complete Rich layout."""
        # Calculate elapsed time
        elapsed = ""
        if self.start_time:
            delta = datetime.now() - self.start_time
            minutes = int(delta.total_seconds() // 60)
            seconds = int(delta.total_seconds() % 60)
            elapsed = f"{minutes:02d}:{seconds:02d}"

        # Build header info
        running_count = len(self.running_tasks)
        pending_count = len(self.pending_tasks)
        header = Text()
        header.append(f"Batch: ", style="dim")
        header.append(self.batch_id, style="bold cyan")
        header.append(f"  |  Tasks: ", style="dim")
        header.append(f"{self.total_tasks} total", style="bold")
        header.append(f" | ", style="dim")
        header.append(f"{self.completed_count} completed", style="green")
        header.append(f" | ", style="dim")
        header.append(f"{running_count} running", style="yellow")
        header.append(f" | ", style="dim")
        header.append(f"{pending_count} pending", style="dim")
        if self.failed_count > 0:
            header.append(f" | ", style="dim")
            header.append(f"{self.failed_count} failed", style="red")
        if elapsed:
            header.append(f"  |  Elapsed: ", style="dim")
            header.append(elapsed, style="cyan")

        # Config info line
        config_line = Text()
        config_line.append("Manager: ", style="dim")
        config_line.append(self.manager_name, style="bold magenta")
        config_line.append("  |  ", style="dim")
        config_line.append("Orchestrator: ", style="dim")
        config_line.append(self.orchestrator_name, style="bold cyan")
        config_line.append("  |  ", style="dim")
        config_line.append("Skills: ", style="dim")
        if self.manager_name == "direct":
            config_line.append("DIRECT (no filter)", style="bold yellow")
        elif self.search_enabled:
            config_line.append("Auto", style="bold green")
        else:
            config_line.append("Specified", style="bold yellow")

        # Build sections
        sections = [header, config_line, "", self.progress]

        # Running tasks section - create a snapshot under lock to avoid iteration errors
        with self._lock:
            running_tasks_snapshot = dict(self.running_tasks)

        if running_tasks_snapshot:
            sections.append("")
            sections.append(Text("RUNNING TASKS", style="bold yellow"))
            for task_id, info in running_tasks_snapshot.items():
                config = info["config"]
                start = info["start_time"]
                phase = info["phase"]

                # Calculate elapsed time for this task
                task_elapsed = datetime.now() - start
                task_minutes = int(task_elapsed.total_seconds() // 60)
                task_seconds = int(task_elapsed.total_seconds() % 60)

                # Build task info
                task_text = Text()
                task_text.append(f"  ● ", style="yellow")
                task_text.append(f"{config.name}", style="bold")
                task_text.append(f" ({task_id})", style="dim")
                task_text.append(f"\n    Mode: ", style="dim")
                task_text.append(f"{get_config()._get('orchestrator')}", style="cyan")
                if config.skills:
                    task_text.append(f" | Skills: ", style="dim")
                    task_text.append(", ".join(config.skills[:3]), style="cyan")
                    if len(config.skills) > 3:
                        task_text.append(f" +{len(config.skills) - 3}", style="dim")
                task_text.append(f"\n    Phase: ", style="dim")
                task_text.append(phase, style="white")
                task_text.append(f"  Elapsed: ", style="dim")
                task_text.append(f"{task_minutes}:{task_seconds:02d}", style="cyan")

                sections.append(task_text)

        # Completed tasks section (show last few, sorted by completion time)
        if self.completed_tasks:
            sections.append("")
            sections.append(Text("COMPLETED", style="bold green"))
            sorted_completed = sorted(self.completed_tasks, key=lambda r: r.completed_at or datetime.min)
            for result in sorted_completed[-self.MAX_COMPLETED_DISPLAY:]:
                mode_label = result.run_id or "free"
                eval_info = ""
                if result.evaluation:
                    score = result.evaluation.get("total_score", 0)
                    icon = "P" if result.evaluation.get("passed") else "F"
                    eval_info = f"  eval:{icon} {score:.0f}%"
                sections.append(
                    Text(
                        f"  ✓ {result.task_id}  [{mode_label}]  "
                        f"{result.duration_seconds:.1f}s  Success{eval_info}",
                        style="green",
                    )
                )
            if len(self.completed_tasks) > self.MAX_COMPLETED_DISPLAY:
                sections.append(
                    Text(f"  ... and {len(self.completed_tasks) - self.MAX_COMPLETED_DISPLAY} more", style="green dim")
                )

        # Failed tasks section
        if self.failed_tasks:
            sections.append("")
            sections.append(Text("FAILED", style="bold red"))
            for result in self.failed_tasks[-3:]:
                error_short = result.error[:50] if result.error else "Unknown error"
                sections.append(
                    Text(f"  ✗ {result.task_id}: {error_short}", style="red")
                )

        # Pending tasks section (show first few)
        if self.pending_tasks and len(self.pending_tasks) <= 5:
            sections.append("")
            sections.append(Text("PENDING", style="bold dim"))
            for task in self.pending_tasks[:3]:
                sections.append(
                    Text(f"  ○ {task.task_id}: {task.name}", style="dim")
                )
            if len(self.pending_tasks) > 3:
                sections.append(
                    Text(f"  ... and {len(self.pending_tasks) - 3} more", style="dim")
                )

        # Combine into a panel
        content = Group(*sections)
        return Panel(
            content,
            title="[bold]AgentSkillOS Batch Executor[/bold]",
            border_style="blue",
            padding=(1, 2),
        )

    def print_summary(self, result: BatchResult) -> None:
        """Print the final execution summary.

        Args:
            result: The batch result
        """
        # Format duration
        minutes = int(result.duration_seconds // 60)
        seconds = int(result.duration_seconds % 60)
        duration_str = f"{minutes:02d}:{seconds:02d}"

        # Build summary table
        summary = Table(show_header=False, box=None, padding=(0, 2))
        summary.add_column(style="dim")
        summary.add_column(style="bold")

        summary.add_row("Batch ID:", result.batch_id)
        summary.add_row("Duration:", duration_str)
        summary.add_row("", "")
        summary.add_row("Results:", "")
        summary.add_row("  ✓ Completed:", str(result.completed), style="green")
        summary.add_row("  ✗ Failed:", str(result.failed), style="red" if result.failed else "dim")
        summary.add_row("  ○ Skipped:", str(result.skipped), style="dim")
        if result.eval_total > 0:
            summary.add_row("", "")
            summary.add_row("Evaluation:", "")
            summary.add_row("  Evaluated:", str(result.eval_total))
            summary.add_row(
                "  Passed:",
                f"{result.eval_passed}/{result.eval_total}",
                style="green" if result.eval_passed == result.eval_total else "yellow",
            )
            summary.add_row("  Avg Score:", f"{result.avg_eval_score:.1f}%")
        summary.add_row("", "")
        summary.add_row("Output:", result.output_dir)

        # Print in a panel
        self.console.print()
        self.console.print(
            Panel(
                summary,
                title="[bold]Batch Execution Summary[/bold]",
                border_style="green" if result.failed == 0 else "yellow",
                padding=(1, 2),
            )
        )

        # Per-task detail table
        if result.task_results:
            detail = Table(show_header=True, box=rich.box.SIMPLE, padding=(0, 1))
            detail.add_column("Task ID", style="bold")
            detail.add_column("Status")
            detail.add_column("Duration")
            detail.add_column("Eval")

            for tr in sorted(result.task_results, key=lambda r: r.completed_at or datetime.min):
                status_str = "✓ Success" if tr.status == TaskStatus.COMPLETED else "✗ Failed"
                status_style = "green" if tr.status == TaskStatus.COMPLETED else "red"
                duration = f"{tr.duration_seconds:.1f}s"
                eval_str = ""
                if tr.evaluation:
                    score = tr.evaluation.get("total_score", 0)
                    icon = "P" if tr.evaluation.get("passed") else "F"
                    eval_str = f"{icon} {score:.0f}%"
                detail.add_row(tr.task_id, Text(status_str, style=status_style), duration, eval_str)

            self.console.print(Panel(detail, title="[bold]Task Details[/bold]", border_style="blue"))
