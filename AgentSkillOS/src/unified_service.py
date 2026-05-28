"""Unified WebUI service integrating skill search and orchestration.

Provides a one-stop workflow:
1. User enters task description
2. Automatic skill search with tree visualization
3. Review and adjust skill selection
4. Generate execution plans
5. Select and execute plan
6. Real-time DAG execution with logs
"""

import asyncio
import logging
import re
import tempfile
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Set

logger = logging.getLogger(__name__)

# Common binary file extensions that cannot be displayed as text
BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.svg',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz',
    '.exe', '.dll', '.so', '.dylib', '.app',
    '.pyc', '.pyo', '.class', '.o', '.obj',
    '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac', '.ogg', '.webm',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.db', '.sqlite', '.sqlite3', '.bin', '.dat', '.pkl', '.pickle',
    '.parquet', '.arrow', '.feather',
}

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
import uvicorn

# Temporary upload directory
UPLOAD_DIR = Path(tempfile.gettempdir()) / "unified_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

from skill_retriever.search.searcher import Searcher, SearchResult
from skill_orchestrator.orchestrator import SkillOrchestrator
from skill_orchestrator.run_context import RunContext
from skill_orchestrator.web_ui import WebVisualizer, OrchestratorState
from web import get_unified_html, mount_static
from config import SKILL_GROUPS, SKILL_GROUP_ALIASES, PROJECT_ROOT, DEMO_TASKS


class UnifiedPhase(str, Enum):
    """Phases of the unified workflow."""
    IDLE = "idle"
    SEARCHING = "searching"
    REVIEWING = "reviewing"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class UnifiedState:
    """State for the unified search + orchestration workflow."""
    phase: UnifiedPhase = UnifiedPhase.IDLE
    task: str = ""
    task_name: str = ""
    files: list[str] = field(default_factory=list)
    start_time: Optional[datetime] = None

    # Mode state: "full" for complete workflow, "execute" for direct execution
    mode: str = "full"
    # Run mode: "baseline", "free-style", "dag" (only used when mode="execute")
    run_mode: Optional[str] = None
    # Preset skills for execute mode (can be empty list for baseline)
    preset_skills: list[str] = field(default_factory=list)
    # Execution mode for unified flow: "dag" or "free-style"
    execution_mode: str = "dag"

    # Skill group state
    current_group_id: str = "default"

    # Custom skill group configuration
    custom_skills_dir: str = ""
    custom_tree_path: str = ""

    # Search state
    search_result: Optional[SearchResult] = None
    selected_skill_ids: list[str] = field(default_factory=list)
    tree_data: Optional[dict] = None
    search_events: list[dict] = field(default_factory=list)
    search_complete: bool = False  # Flag: search completed, waiting for user confirmation

    # Orchestration state (inherits from OrchestratorState)
    orchestrator_state: Optional[OrchestratorState] = None

    # Working directory (relative path for display)
    work_dir: str = ""

    # Logs
    logs: list[dict] = field(default_factory=list)

    def get_elapsed(self) -> str:
        """Get elapsed time string."""
        if not self.start_time:
            return "0:00"
        elapsed = datetime.now() - self.start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        return f"{minutes}:{seconds:02d}"

    def add_log(self, message: str, level: str = "info") -> dict:
        """Add a log entry and return it."""
        entry = {
            "message": message,
            "level": level,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "elapsed": self.get_elapsed(),
        }
        self.logs.append(entry)
        return entry

    def to_dict(self) -> dict:
        """Convert state to dict for sending to frontend."""
        result = {
            "phase": self.phase.value,
            "task": self.task,
            "elapsed": self.get_elapsed(),
            "logs": self.logs,
            "tree_data": self.tree_data,
            "search_events": self.search_events,
            "search_complete": self.search_complete,
            # Execute mode info
            "mode": self.mode,
            "run_mode": self.run_mode,
            "preset_skills": self.preset_skills,
            # Execution mode for unified flow
            "execution_mode": self.execution_mode,
            # Working directory
            "work_dir": self.work_dir,
        }

        # Add search result if available
        if self.search_result:
            result["search_result"] = {
                "skills": self.search_result.selected_skills,
                "llm_calls": self.search_result.llm_calls,
            }
            result["selected_skill_ids"] = self.selected_skill_ids

        # Add orchestrator state if available
        if self.orchestrator_state:
            result["orchestrator"] = self.orchestrator_state.to_dict()

        return result


class UnifiedService:
    """Unified service combining skill search and orchestration."""

    def __init__(
        self,
        max_concurrent: int = 6,
        # Execute mode parameters
        task: str = None,
        preset_skills: list = None,
        mode: str = "full",
        run_mode: str = None,
        files: list = None,
        task_name: str = None,
    ):
        self.max_concurrent = max_concurrent
        self.state = UnifiedState()
        self.clients: Set[WebSocket] = set()
        self.searcher: Optional[Searcher] = None
        self.executor = ThreadPoolExecutor(max_workers=1)  # For running sync search
        self._loop: Optional[asyncio.AbstractEventLoop] = None  # Store event loop for thread-safe broadcasts
        self._execution_started = False  # Track if execute mode has started

        # Configure execute mode
        self.state.mode = mode
        self.state.run_mode = run_mode
        if task:
            self.state.task = task
        if task_name:
            self.state.task_name = task_name
        if files:
            self.state.files = files
        if preset_skills is not None:
            self.state.preset_skills = preset_skills
            self.state.selected_skill_ids = preset_skills

        # Set initial skill group from default
        self.state.current_group_id = self._get_default_group_id()

        # Set skill_dir from current group
        current_group = self._get_group_by_id(self.state.current_group_id)
        if current_group:
            self.skill_dir = self._get_absolute_path(current_group["skills_dir"]) if current_group["skills_dir"] else None
        else:
            self.skill_dir = None

    def _get_group_by_id(self, group_id: str) -> Optional[dict]:
        """Get a skill group by ID.

        For predefined groups, returns the entry from SKILL_GROUPS.
        For 'custom' group, returns a dynamically-built dict using state's custom paths.
        Supports alias resolution for backward compatibility (e.g., "default" -> "skill_seeds").
        """
        # Resolve alias for backward compatibility
        resolved_id = SKILL_GROUP_ALIASES.get(group_id, group_id)

        # Handle custom group specially
        if resolved_id == "custom":
            return {
                "id": "custom",
                "name": "Custom",
                "description": "User-defined skill set with configurable paths",
                "skills_dir": self.state.custom_skills_dir,
                "tree_path": self.state.custom_tree_path,
                "is_configurable": True,
            }

        # Look up predefined groups
        for group in SKILL_GROUPS:
            if group["id"] == resolved_id:
                return group
        return None

    def _get_default_group_id(self) -> str:
        """Get the default skill group ID."""
        for group in SKILL_GROUPS:
            if group.get("is_default"):
                return group["id"]
        return SKILL_GROUPS[0]["id"] if SKILL_GROUPS else "default"

    def _get_absolute_path(self, path: str) -> Path:
        """Convert a relative path to absolute path."""
        if not path:
            return None
        p = Path(path)
        if p.is_absolute():
            return p
        return PROJECT_ROOT / p

    def get_skill_groups(self) -> list[dict]:
        """Get all skill groups with current selection status.

        Returns predefined groups from SKILL_GROUPS plus a dynamically-built
        'Custom' group entry with is_configurable: True.
        """
        groups = []
        # Add predefined groups from SKILL_GROUPS
        for group in SKILL_GROUPS:
            group_data = {
                "id": group["id"],
                "name": group["name"],
                "description": group["description"],
                "is_current": group["id"] == self.state.current_group_id,
            }
            groups.append(group_data)

        # Dynamically append the "Custom" group entry
        groups.append({
            "id": "custom",
            "name": "Custom",
            "description": "User-defined skill set with configurable paths",
            "is_current": self.state.current_group_id == "custom",
            "is_configurable": True,
            "custom_skills_dir": self.state.custom_skills_dir,
            "custom_tree_path": self.state.custom_tree_path,
        })

        return groups

    async def set_skill_group(self, group_id: str) -> bool:
        """Set the current skill group.

        Returns True if the group was changed, False otherwise.
        """
        group = self._get_group_by_id(group_id)
        if not group:
            logger.warning(f"Skill group '{group_id}' not found")
            return False

        if self.state.current_group_id == group_id:
            return False

        self.state.current_group_id = group_id

        # Update skill_dir from group dict (for custom group, _get_group_by_id uses state's custom paths)
        if group["skills_dir"]:
            self.skill_dir = self._get_absolute_path(group["skills_dir"])
        else:
            self.skill_dir = None

        self.searcher = None  # Reset searcher to use new tree_path

        logger.info(f"Switched to skill group: {group['name']} ({group_id})")

        # Broadcast the change
        await self.broadcast("skill_group_changed", {
            "group_id": group_id,
            "groups": self.get_skill_groups(),
        })

        return True

    async def set_custom_config(self, skills_dir: str, tree_path: str) -> None:
        """Set custom skill group configuration."""
        self.state.custom_skills_dir = skills_dir
        self.state.custom_tree_path = tree_path

        # If currently using custom group, update skill_dir
        if self.state.current_group_id == "custom":
            if skills_dir:
                self.skill_dir = self._get_absolute_path(skills_dir)
            else:
                self.skill_dir = None
            self.searcher = None  # Reset searcher

        logger.info(f"Custom config updated: skills_dir={skills_dir}, tree_path={tree_path}")

        # Broadcast the change
        await self.broadcast("custom_config_changed", {
            "skills_dir": skills_dir,
            "tree_path": tree_path,
        })

    async def broadcast(self, msg_type: str, data: dict) -> None:
        """Broadcast message to all connected clients."""
        message = {"type": msg_type, "data": data}
        disconnected = set()
        for client in list(self.clients):
            try:
                await client.send_json(message)
            except Exception:
                disconnected.add(client)
        self.clients -= disconnected

    async def broadcast_log(self, message: str, level: str = "info") -> None:
        """Add log and broadcast to clients."""
        entry = self.state.add_log(message, level)
        await self.broadcast("log", entry)

    def _handle_search_event(self, event_type: str, data: dict) -> None:
        """Handle search events from Searcher (called from sync context in thread)."""
        event = {"type": event_type, "data": data, "timestamp": datetime.now().isoformat()}
        self.state.search_events.append(event)
        # Use run_coroutine_threadsafe to safely broadcast from thread
        if self._loop is not None:
            asyncio.run_coroutine_threadsafe(
                self.broadcast("search_event", event),
                self._loop
            )

    async def start_search(self, task: str, task_name: str = None, files: Optional[list[str]] = None) -> None:
        """Start the skill search process."""
        # Save event loop reference for thread-safe broadcasts
        self._loop = asyncio.get_running_loop()

        self.state.task = task
        self.state.task_name = task_name or ""
        self.state.files = files or []
        self.state.start_time = datetime.now()
        self.state.phase = UnifiedPhase.SEARCHING
        self.state.search_events = []
        self.state.logs = []

        await self.broadcast("phase", {"phase": "searching"})
        await self.broadcast_log(f"Starting search for: {task}", "info")

        # Get current skill group's tree path
        current_group = self._get_group_by_id(self.state.current_group_id)
        if current_group:
            group_name = current_group["name"]
            # tree_path comes from group dict (for custom group, _get_group_by_id uses state's custom paths)
            tree_path = self._get_absolute_path(current_group["tree_path"]) if current_group["tree_path"] else None
        else:
            group_name = "Unknown"
            tree_path = None

        await self.broadcast_log(f"Using skill group: {group_name}", "info")

        # Create searcher with event callback and tree path
        self.searcher = Searcher(tree_path=str(tree_path) if tree_path else None, event_callback=self._handle_search_event)

        # Get tree data for visualization
        self.state.tree_data = self.searcher.get_tree_data()
        await self.broadcast("tree_data", {"tree": self.state.tree_data})

        # Run search in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.searcher.search(task, verbose=False)
            )
            self.state.search_result = result
            self.state.selected_skill_ids = [s["id"] for s in result.selected_skills]
            self.state.search_complete = True  # Mark search as complete, waiting for user confirmation
            # Keep phase as SEARCHING - user must confirm to proceed to reviewing

            await self.broadcast("search_complete", {
                "skills": result.selected_skills,
                "llm_calls": result.llm_calls,
                "selected_ids": self.state.selected_skill_ids,
            })
            # Don't auto-transition to reviewing - wait for user confirmation
            await self.broadcast_log(
                f"Found {len(result.selected_skills)} skills in {result.llm_calls} LLM calls",
                "ok"
            )

        except Exception as e:
            self.state.phase = UnifiedPhase.ERROR
            await self.broadcast("error", {"message": str(e)})
            await self.broadcast_log(f"Search failed: {e}", "error")

    async def update_skills(self, skill_ids: list[str]) -> None:
        """Update selected skill IDs."""
        self.state.selected_skill_ids = skill_ids
        await self.broadcast("skills_updated", {"selected_ids": skill_ids})
        await self.broadcast_log(f"Updated skill selection: {len(skill_ids)} skills", "info")

    async def confirm_search(self) -> None:
        """Confirm search results and proceed to review phase."""
        self.state.search_complete = False  # Reset flag
        self.state.phase = UnifiedPhase.REVIEWING
        await self.broadcast("phase", {"phase": "reviewing"})
        await self.broadcast_log("Proceeding to review skills", "info")

    async def confirm_skills(self, execution_mode: str = "dag") -> None:
        """Confirm skill selection and start execution.

        Args:
            execution_mode: "dag" for DAG orchestration, "free-style" for Claude free-style mode
        """
        self.state.execution_mode = execution_mode

        if execution_mode == "dag":
            await self._execute_dag_mode()
        else:  # free-style
            await self._execute_free_style_mode()

    async def _execute_dag_mode(self) -> None:
        """Execute using DAG orchestration (plan and parallel execution)."""
        # Allow 0 skills to continue
        self.state.phase = UnifiedPhase.PLANNING
        await self.broadcast("phase", {"phase": "planning"})
        await self.broadcast_log(
            f"Starting DAG planning with {len(self.state.selected_skill_ids)} skills",
            "info"
        )

        # Create run context with mode and task_name
        run_context = RunContext.create(
            self.state.task,
            mode="dag",  # DAG mode
            task_name=self.state.task_name if self.state.task_name else None
        )

        # Setup run context first - this copies skills to isolated directory
        # Must be done before creating orchestrator so registry finds skills
        run_context.setup(self.state.selected_skill_ids, self.skill_dir)
        await self.broadcast_log(
            f"Skills copied to: {run_context.skills_dir}",
            "info"
        )

        # Create orchestrator with the isolated skills directory
        orchestrator = SkillOrchestrator(
            skill_dir=str(run_context.skills_dir),
            run_context=run_context,
            max_concurrent=self.max_concurrent,
        )

        # Create orchestrator state for WebVisualizer
        self.state.orchestrator_state = OrchestratorState()

        # Create visualizer
        visualizer = WebVisualizer(self.state.orchestrator_state, self.clients)

        # Run orchestration
        await visualizer.start()
        try:
            self.state.phase = UnifiedPhase.EXECUTING
            await self.broadcast("phase", {"phase": "executing"})
            self.state.work_dir = str(run_context.run_dir)
            await self.broadcast("work_dir", {"path": self.state.work_dir})

            result = await orchestrator.run_with_visualizer(
                task=self.state.task,
                skill_names=self.state.selected_skill_ids,
                visualizer=visualizer,
                files=self.state.files,
            )

            self.state.phase = UnifiedPhase.COMPLETE
            await self.broadcast("phase", {"phase": "complete"})
            await self.broadcast("result", result)
            await self.broadcast_log(
                f"Orchestration completed: {result.get('status', 'unknown')}",
                "ok" if result.get("status") == "completed" else "warn"
            )

        except Exception as e:
            self.state.phase = UnifiedPhase.ERROR
            await self.broadcast("error", {"message": str(e)})
            await self.broadcast_log(f"Execution failed: {e}", "error")
        finally:
            await visualizer.stop()

    async def _execute_free_style_mode(self) -> None:
        """Execute using Free-Style mode (Claude decides which skills to call)."""
        from skill_orchestrator.client import SkillClient

        self.state.phase = UnifiedPhase.EXECUTING
        await self.broadcast("phase", {"phase": "executing"})

        # Create run context
        skills = self.state.selected_skill_ids or []
        folder_mode = "free_style_selected" if skills else "free_style_all"
        run_context = RunContext.create(
            self.state.task,
            mode=folder_mode,
            task_name=self.state.task_name if self.state.task_name else None
        )

        if skills:
            run_context.setup(skills, self.skill_dir, copy_all=False)
            run_context.save_meta(self.state.task, "with_skills", skills)
        else:
            run_context.setup([], self.skill_dir, copy_all=True)
            copied_skills = [d.name for d in run_context.skills_dir.iterdir() if d.is_dir()] if run_context.skills_dir.exists() else []
            run_context.save_meta(self.state.task, "with_skills", copied_skills)

        if self.state.files:
            run_context.copy_files(self.state.files)
            run_context.update_meta(files=self.state.files)

        self.state.work_dir = str(run_context.run_dir)
        await self.broadcast("work_dir", {"path": self.state.work_dir})
        await self.broadcast_log("Starting free-style mode execution", "info")

        # Create orchestrator state for logging
        self.state.orchestrator_state = OrchestratorState()
        visualizer = WebVisualizer(self.state.orchestrator_state, self.clients)
        await visualizer.start()

        # Create FreeStyleExecution node for visualization
        auto_node = {
            "id": "FreeStyleExecution",
            "name": "FreeStyleExecution",
            "type": "primary",
            "depends_on": [],
            "purpose": "Claude directly executes the task using available skills",
            "outputs_summary": "Task output",
        }
        await visualizer.set_nodes([auto_node], [[auto_node["id"]]])
        await visualizer.update_status("FreeStyleExecution", "running")

        try:
            # Create async-compatible log callback
            def log_callback(msg: str, level: str = "info") -> None:
                asyncio.create_task(visualizer.add_log(msg, level))

            cwd = str(run_context.run_dir.resolve())  # Convert to absolute path
            async with SkillClient(
                session_id=run_context.run_id,
                cwd=cwd,
                log_callback=log_callback,
            ) as client:
                # Build free-style prompt with working directory constraint
                free_style_prompt = f"""Please complete the following task.

## Working Directory
Your working directory is: {cwd}
**IMPORTANT**: All file operations MUST be performed within this directory or its subdirectories.
Do NOT create or modify files outside of this directory.

## Task
{self.state.task}"""
                response = await client.execute(free_style_prompt)

            result = {"status": "completed", "response": response}
            run_context.save_result(result)
            await visualizer.update_status("FreeStyleExecution", "completed")

            self.state.phase = UnifiedPhase.COMPLETE
            await self.broadcast("phase", {"phase": "complete"})
            await self.broadcast("result", result)
            await self.broadcast_log("Auto mode execution completed", "ok")

        except Exception as e:
            result = {"status": "failed", "error": str(e)}
            run_context.save_result(result)
            await visualizer.update_status("FreeStyleExecution", "failed")
            self.state.phase = UnifiedPhase.ERROR
            await self.broadcast("error", {"message": str(e)})
            await self.broadcast_log(f"Execution failed: {e}", "error")
        finally:
            await visualizer.stop()

    async def start_direct_execution(self) -> None:
        """Start direct execution for execute mode (bypasses search).

        Used when mode='execute' to run baseline/auto/dag directly.
        """
        from skill_orchestrator.client import SkillClient
        from skill_orchestrator.run_context import RunContext
        from pathlib import Path

        if self._execution_started:
            return
        self._execution_started = True

        self.state.start_time = datetime.now()
        run_mode = self.state.run_mode or "dag"
        skills = self.state.preset_skills or []
        files = self.state.files or []

        await self.broadcast_log(f"Starting direct execution in {run_mode} mode", "info")

        if run_mode == "dag":
            # DAG mode: Use the orchestrator (same as confirm_skills)
            self.state.selected_skill_ids = skills
            await self.confirm_skills()
        else:
            # baseline or free-style mode: Use SkillClient directly
            self.state.phase = UnifiedPhase.EXECUTING
            await self.broadcast("phase", {"phase": "executing"})

            # Create run context
            folder_mode = "baseline" if run_mode == "baseline" else ("free_style_selected" if skills else "free_style_all")
            run_context = RunContext.create(
                self.state.task,
                mode=folder_mode,
                task_name=self.state.task_name if self.state.task_name else None
            )
            skill_dir = Path(".claude/skills")

            if run_mode == "baseline":
                run_context.setup([], skill_dir, copy_all=False)
                run_context.save_meta(self.state.task, "baseline", [])
            else:  # auto
                if skills:
                    run_context.setup(skills, skill_dir, copy_all=False)
                    run_context.save_meta(self.state.task, "with_skills", skills)
                else:
                    run_context.setup([], skill_dir, copy_all=True)
                    copied_skills = [d.name for d in run_context.skills_dir.iterdir() if d.is_dir()] if run_context.skills_dir.exists() else []
                    run_context.save_meta(self.state.task, "with_skills", copied_skills)

            if files:
                run_context.copy_files(files)
                run_context.update_meta(files=files)

            self.state.work_dir = str(run_context.run_dir)
            await self.broadcast("work_dir", {"path": self.state.work_dir})
            await self.broadcast_log(f"Run directory: {run_context.run_dir}", "info")

            # Create orchestrator state for logging
            self.state.orchestrator_state = OrchestratorState()
            visualizer = WebVisualizer(self.state.orchestrator_state, self.clients)
            await visualizer.start()

            try:
                # Create async-compatible log callback
                def log_callback(msg: str, level: str = "info") -> None:
                    asyncio.create_task(visualizer.add_log(msg, level))

                cwd = str(run_context.run_dir.resolve())  # Convert to absolute path
                # Build prompt with working directory constraint
                prompt_with_cwd = f"""Please complete the following task.

## Working Directory
Your working directory is: {cwd}
**IMPORTANT**: All file operations MUST be performed within this directory or its subdirectories.
Do NOT create or modify files outside of this directory.

## Task
{self.state.task}"""

                if run_mode == "baseline":
                    async with SkillClient(
                        session_id=run_context.run_id,
                        cwd=cwd,
                        allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep"],
                        log_callback=log_callback,
                    ) as client:
                        response = await client.execute(prompt_with_cwd)
                else:  # auto
                    async with SkillClient(
                        session_id=run_context.run_id,
                        cwd=cwd,
                        log_callback=log_callback,
                    ) as client:
                        response = await client.execute(prompt_with_cwd)

                result = {"status": "completed", "response": response}
                run_context.save_result(result)

                self.state.phase = UnifiedPhase.COMPLETE
                await self.broadcast("phase", {"phase": "complete"})
                await self.broadcast("result", result)
                await self.broadcast_log("Execution completed", "ok")

            except Exception as e:
                result = {"status": "failed", "error": str(e)}
                run_context.save_result(result)
                self.state.phase = UnifiedPhase.ERROR
                await self.broadcast("error", {"message": str(e)})
                await self.broadcast_log(f"Execution failed: {e}", "error")
            finally:
                await visualizer.stop()

    async def get_skill_detail(self, skill_id: str, skill_path: str) -> None:
        """Get skill details including directory structure and SKILL.md content.

        Args:
            skill_id: The skill identifier
            skill_path: Path to the SKILL.md file
        """
        try:
            # Get skill directory from skill_path
            skill_md_path = Path(skill_path)
            if not skill_md_path.exists():
                await self.broadcast("skill_detail", {
                    "skill_id": skill_id,
                    "name": "",
                    "description": "",
                    "content": "SKILL.md not found",
                    "directory_tree": None,
                })
                return

            skill_dir = skill_md_path.parent

            # Read SKILL.md content
            raw_content = skill_md_path.read_text(encoding="utf-8")

            # Parse frontmatter
            parsed = self._parse_skill_md(raw_content)

            # Build directory tree
            directory_tree = self._build_directory_tree(skill_dir)

            # Broadcast the result with parsed content
            await self.broadcast("skill_detail", {
                "skill_id": skill_id,
                "name": parsed["name"],
                "description": parsed["description"],
                "content": parsed["body"],
                "directory_tree": directory_tree,
            })

        except Exception as e:
            logger.error(f"Error getting skill detail: {e}")
            await self.broadcast("skill_detail", {
                "skill_id": skill_id,
                "name": "",
                "description": "",
                "content": f"Error: {str(e)}",
                "directory_tree": None,
            })

    def _build_directory_tree(self, path: Path, max_depth: int = 5, current_depth: int = 0) -> dict:
        """Recursively build directory tree structure.

        Args:
            path: Directory path to scan
            max_depth: Maximum depth to recurse
            current_depth: Current recursion depth

        Returns:
            Dictionary with name, type, and children
        """
        if current_depth > max_depth:
            return None

        result = {
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
        }

        if path.is_dir():
            children = []
            try:
                # Sort entries: directories first, then files, alphabetically
                entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for entry in entries:
                    # Skip hidden files and common non-essential directories
                    if entry.name.startswith('.') or entry.name in ['__pycache__', 'node_modules', '.git']:
                        continue
                    child = self._build_directory_tree(entry, max_depth, current_depth + 1)
                    if child:
                        children.append(child)
            except PermissionError:
                pass
            if children:
                result["children"] = children

        return result

    def _parse_skill_md(self, content: str) -> dict:
        """Parse SKILL.md content, extracting YAML frontmatter and body.

        Args:
            content: Raw SKILL.md file content

        Returns:
            Dictionary with name, description, and body keys
        """
        result = {"name": "", "description": "", "body": content}

        # Match YAML frontmatter: ---\n...\n---
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n?'
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        if match:
            frontmatter_text = match.group(1)
            body = content[match.end():]

            # Extract name from frontmatter
            name_match = re.search(r'^name:\s*(.+)$', frontmatter_text, re.MULTILINE)
            if name_match:
                result["name"] = name_match.group(1).strip().strip('"\'')

            # Extract description from frontmatter
            desc_match = re.search(r'^description:\s*(.+)$', frontmatter_text, re.MULTILINE)
            if desc_match:
                result["description"] = desc_match.group(1).strip().strip('"\'')

            result["body"] = body.strip()

        return result

    async def get_file_content(self, skill_path: str, relative_path: str) -> None:
        """Get content of a file within a skill directory.

        Args:
            skill_path: Path to the SKILL.md file (used to determine skill directory)
            relative_path: Relative path to the file from the skill directory
        """
        try:
            skill_dir = Path(skill_path).parent
            file_path = skill_dir / relative_path

            # Security check: ensure file is within skill directory
            if not file_path.resolve().is_relative_to(skill_dir.resolve()):
                await self.broadcast("file_content", {
                    "path": relative_path,
                    "content": "",
                    "error": "Access denied: file outside skill directory"
                })
                return

            if not file_path.exists():
                await self.broadcast("file_content", {
                    "path": relative_path,
                    "content": "",
                    "error": "File not found"
                })
                return

            if not file_path.is_file():
                await self.broadcast("file_content", {
                    "path": relative_path,
                    "content": "",
                    "error": "Not a file"
                })
                return

            # Check for binary file
            file_ext = file_path.suffix.lower()
            if file_ext in BINARY_EXTENSIONS:
                await self.broadcast("file_content", {
                    "path": relative_path,
                    "content": "",
                    "is_binary": True,
                    "error": f"Binary file ({file_ext}) cannot be displayed"
                })
                return

            # Read file content
            content = file_path.read_text(encoding="utf-8", errors="replace")

            await self.broadcast("file_content", {
                "path": relative_path,
                "content": content,
            })

        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            await self.broadcast("file_content", {
                "path": relative_path,
                "content": "",
                "error": str(e)
            })


def create_unified_app(
    max_concurrent: int = 6,
    # Execute mode parameters
    task: str = None,
    preset_skills: list = None,
    mode: str = "full",
    run_mode: str = None,
    files: list = None,
    task_name: str = None,
) -> FastAPI:
    """Create the unified FastAPI application.

    Args:
        max_concurrent: Maximum concurrent executions
        task: Pre-set task (for execute mode)
        preset_skills: Pre-set skills list (for execute mode)
        mode: "full" for complete workflow, "execute" for direct execution
        run_mode: "baseline" | "free-style" | "dag" (for execute mode)
        files: Pre-set files list (for execute mode)
        task_name: Task name for folder naming (for execute mode)
    """
    app = FastAPI(title="Unified AgentSkillOS")

    # Mount static files for CSS/JS
    mount_static(app)

    service = UnifiedService(
        max_concurrent=max_concurrent,
        task=task,
        preset_skills=preset_skills,
        mode=mode,
        run_mode=run_mode,
        files=files,
        task_name=task_name,
    )

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return get_unified_html()

    @app.get("/tree")
    async def get_tree():
        """Get the capability tree data."""
        if service.searcher is None:
            service.searcher = Searcher()
        return service.searcher.get_tree_data()

    @app.post("/api/upload")
    async def upload_files(files: list[UploadFile] = File(...)):
        """Handle file upload."""
        results = []
        for file in files:
            # Save to temporary directory
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            results.append({
                "name": file.filename,
                "path": str(file_path),
                "size": len(content)
            })

        return {"files": results}

    @app.delete("/api/upload/{filename:path}")
    async def delete_file(filename: str):
        """Delete an uploaded file."""
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()
        return {"status": "ok"}

    @app.get("/api/skill-groups")
    async def get_skill_groups():
        """Get all available skill groups."""
        return {"groups": service.get_skill_groups()}

    @app.get("/api/demos")
    async def get_demos():
        """Get all available demo tasks."""
        # Return demo configs without the full prompt for listing
        demos = []
        for demo in DEMO_TASKS:
            demos.append({
                "id": demo["id"],
                "title": demo["title"],
                "description": demo["description"],
                "icon": demo.get("icon", "default"),
                "file_count": len(demo.get("files", [])),
            })
        return {"demos": demos}

    @app.post("/api/demos/{demo_id}/load")
    async def load_demo(demo_id: str):
        """Load a demo: copy files to upload dir and return prompt + file info."""
        import shutil

        # Find the demo
        demo = next((d for d in DEMO_TASKS if d["id"] == demo_id), None)
        if not demo:
            return {"error": "Demo not found"}, 404

        # Copy files to upload directory
        uploaded_files = []
        for file_path in demo.get("files", []):
            src_path = PROJECT_ROOT / file_path
            if src_path.exists():
                dest_path = UPLOAD_DIR / src_path.name
                shutil.copy2(src_path, dest_path)
                uploaded_files.append({
                    "name": src_path.name,
                    "path": str(dest_path),
                    "size": dest_path.stat().st_size,
                })

        return {
            "prompt": demo["prompt"],
            "files": uploaded_files,
        }

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        service.clients.add(websocket)

        def get_init_data():
            """Get init data including skill groups."""
            data = service.state.to_dict()
            data["skill_groups"] = service.get_skill_groups()
            return data

        try:
            # Send current state with skill groups
            await websocket.send_json({"type": "init", "data": get_init_data()})

            # In execute mode, auto-start execution after client connects
            if service.state.mode == "execute" and not service._execution_started:
                asyncio.create_task(service.start_direct_execution())

            # Handle messages
            while True:
                try:
                    data = await asyncio.wait_for(websocket.receive_json(), timeout=30)
                    if data.get("type") == "sync":
                        await websocket.send_json({"type": "init", "data": get_init_data()})
                        continue
                    await handle_message(service, data)
                except asyncio.TimeoutError:
                    # Send ping
                    try:
                        await websocket.send_json({"type": "ping"})
                    except:
                        break
                except Exception as e:
                    print(f"WebSocket error: {e}")
                    break

        except WebSocketDisconnect:
            pass
        finally:
            service.clients.discard(websocket)

    return app


async def handle_message(service: UnifiedService, data: dict) -> None:
    """Handle incoming WebSocket messages."""
    msg_type = data.get("type")

    if msg_type == "start_search":
        task = data.get("task", "")
        task_name = data.get("task_name", "")
        files = data.get("files", [])
        asyncio.create_task(service.start_search(task, task_name, files))

    elif msg_type == "update_skills":
        skill_ids = data.get("skill_ids", [])
        await service.update_skills(skill_ids)

    elif msg_type == "confirm_search":
        await service.confirm_search()

    elif msg_type == "confirm_skills":
        execution_mode = data.get("execution_mode", "dag")
        asyncio.create_task(service.confirm_skills(execution_mode=execution_mode))

    elif msg_type == "select_plan":
        # Forward to orchestrator state
        if service.state.orchestrator_state:
            service.state.orchestrator_state.selected_plan_index = data.get("index", 0)

    elif msg_type == "set_skill_group":
        group_id = data.get("group_id", "")
        await service.set_skill_group(group_id)

    elif msg_type == "set_custom_config":
        skills_dir = data.get("skills_dir", "")
        tree_path = data.get("tree_path", "")
        await service.set_custom_config(skills_dir, tree_path)

    elif msg_type == "get_skill_detail":
        skill_id = data.get("skill_id", "")
        skill_path = data.get("skill_path", "")
        asyncio.create_task(service.get_skill_detail(skill_id, skill_path))

    elif msg_type == "get_file_content":
        skill_path = data.get("skill_path", "")
        relative_path = data.get("relative_path", "")
        asyncio.create_task(service.get_file_content(skill_path, relative_path))

    elif msg_type == "reset":
        # Reset service state but preserve current skill group and custom config
        current_group_id = service.state.current_group_id
        custom_skills_dir = service.state.custom_skills_dir
        custom_tree_path = service.state.custom_tree_path
        service.state = UnifiedState()
        service.state.current_group_id = current_group_id
        service.state.custom_skills_dir = custom_skills_dir
        service.state.custom_tree_path = custom_tree_path
        # Broadcast phase change
        await service.broadcast("phase", "idle")
        logger.info("State reset to idle")


def run_unified_service(
    host: str = "127.0.0.1",
    port: int = 8765,
    open_browser: bool = True,
    # Execute mode parameters
    task: str = None,
    preset_skills: list = None,
    mode: str = "full",
    run_mode: str = None,
    files: list = None,
    task_name: str = None,
) -> None:
    """Run the unified service.

    Args:
        host: Server host
        port: Server port
        open_browser: Whether to open browser automatically
        task: Pre-set task (for execute mode)
        preset_skills: Pre-set skills list (for execute mode)
        mode: "full" for complete workflow, "execute" for direct execution
        run_mode: "baseline" | "free-style" | "dag" (for execute mode)
        files: Pre-set files list (for execute mode)
        task_name: Task name for folder naming (for execute mode)
    """
    app = create_unified_app(
        task=task,
        preset_skills=preset_skills,
        mode=mode,
        run_mode=run_mode,
        files=files,
        task_name=task_name,
    )

    if open_browser:
        import threading
        def open_browser_delayed():
            import time
            time.sleep(1)
            webbrowser.open(f"http://{host}:{port}")
        threading.Thread(target=open_browser_delayed, daemon=True).start()

    config = uvicorn.Config(app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config)

    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        pass
