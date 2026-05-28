"""Run context management for isolated execution."""

import asyncio
import hashlib
import logging
import shutil
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import PROJECT_ROOT

logger = logging.getLogger(__name__)


class RunContext:
    """Manage isolated environment for single execution.

    Uses a dual-directory architecture:
    - exec_dir: Temporary directory in /tmp for CLI execution (isolated from AgentSkillOS)
    - run_dir:  Permanent directory in runs/ for metadata, logs, and final results

    The exec_dir is placed in system temp to break all ancestor relationships
    with AgentSkillOS, preventing CLI from discovering parent .claude/ via
    upward directory traversal.
    """

    def __init__(self, run_id: str, base_dir: Path):
        self.run_id = run_id
        self.run_dir = base_dir / run_id          # Permanent storage (meta, logs, final results)

        # Isolated temp directory for CLI execution.
        # Placed in system temp to break all ancestor relationships
        # with AgentSkillOS, preventing CLI from discovering parent .claude/.
        self._exec_root = Path(tempfile.mkdtemp(prefix=f"aso-{run_id[:20]}-"))
        self.exec_dir = self._exec_root           # CLI subprocess cwd

        self.skills_dir = self.exec_dir / ".claude" / "skills"   # Skills in exec dir
        self.workspace_dir = self.exec_dir / "workspace"          # Workspace in exec dir
        self.logs_dir = self.run_dir / "logs"                     # Logs in permanent dir
        self._setup_done = False
        self._finalized = False

    @classmethod
    def create(
        cls,
        task: str,
        base_dir: str = "runs",
        mode: str = None,
        task_name: str = None,
        task_id: str = None,
    ) -> "RunContext":
        """Create a new execution context.

        Args:
            task: Task description for generating hash
            base_dir: Path to runs directory
            mode: Execution mode (dag, free-style, auto_selected, auto_all, baseline)
            task_name: User-specified task name (optional)
            task_id: Task identifier for batch execution (optional)

        Returns:
            RunContext instance
        """
        import re
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        task_hash = hashlib.md5(task.encode()).hexdigest()[:6]

        parts = [timestamp]
        if mode:
            parts.append(mode)
        # Prefer task_id over task_name for naming (task_id is more structured)
        if task_id:
            safe_id = cls._sanitize_name(task_id)
            if safe_id:
                parts.append(safe_id)
        elif task_name:
            safe_name = cls._sanitize_name(task_name)
            if safe_name:
                parts.append(safe_name)
        parts.append(task_hash)

        run_id = "-".join(parts)
        return cls(run_id, Path(base_dir))

    @staticmethod
    def _sanitize_name(name: str, max_length: int = 30) -> str:
        """Sanitize task name for safe folder naming.

        Args:
            name: Raw task name
            max_length: Maximum length of sanitized name

        Returns:
            Sanitized name safe for use in folder names
        """
        import re
        sanitized = name.replace(" ", "_")
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', sanitized)
        sanitized = sanitized.lower()[:max_length].rstrip('_-')
        return sanitized

    def setup(
        self,
        skill_names: list[str],
        source_skill_dir: Path,
        copy_all: bool = False,
    ) -> None:
        """Initialize directory structures and copy skills.

        Sets up two directories:
        - exec_dir (temp): isolated CLI environment with workspace and skills
        - run_dir (permanent): logs and metadata only (workspace copied back after execution)

        Args:
            skill_names: List of skill names to copy
            source_skill_dir: Source skill directory (usually .claude/skills)
            copy_all: If True, copy all skills; otherwise only copy skill_names
        """
        if self._setup_done:
            return

        # Permanent dir: logs only (meta.json written separately)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Exec dir: workspace only (no git init, no settings.json needed —
        # /tmp ancestor chain has no .claude/ so CLI won't find parent config)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # Copy .env to exec_dir so CLI subprocess / skills can access API keys
        env_file = PROJECT_ROOT / ".env"
        if env_file.exists():
            shutil.copy2(env_file, self.exec_dir / ".env")

        if copy_all:
            # Copy all skills
            if source_skill_dir.exists():
                self.skills_dir.mkdir(parents=True, exist_ok=True)
                for skill_dir in source_skill_dir.iterdir():
                    if skill_dir.is_dir():
                        dst = self.skills_dir / skill_dir.name
                        shutil.copytree(skill_dir, dst, dirs_exist_ok=True)
        elif skill_names:
            # Copy only specified skills
            self.skills_dir.mkdir(parents=True, exist_ok=True)
            for name in skill_names:
                src = source_skill_dir / name
                dst = self.skills_dir / name
                if src.exists():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
        # If skill_names is empty and copy_all is False, don't create .claude/skills/

        self._setup_done = True

    def copy_files(self, file_paths: list[str]) -> list[str]:
        """Copy specified files to workspace directory.

        Args:
            file_paths: List of file paths (supports absolute and relative paths)

        Returns:
            List of successfully copied filenames
        """
        copied = []
        for path_str in file_paths:
            src = Path(path_str).expanduser().resolve()
            if not src.exists():
                continue
            dst = self.workspace_dir / src.name
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            copied.append(src.name)
        return copied

    def save_meta(
        self,
        task: str,
        mode: str,
        skills: list[str],
        task_id: str = None,
        copy_all: bool = False,
    ) -> None:
        """Save execution metadata.

        Args:
            task: Task description
            mode: Execution mode
            skills: List of used skills
            task_id: Task identifier (for batch execution)
            copy_all: If True, indicates all skills were copied to exec env
        """
        meta = {
            "run_id": self.run_id,
            "task": task,
            "mode": mode,
            "skills": skills,
            "skills_copy_all": copy_all,
            "started_at": datetime.now().isoformat(),
        }
        if task_id:
            meta["task_id"] = task_id
        with open(self.run_dir / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    def update_meta(self, **kwargs) -> None:
        """Update metadata fields.

        Args:
            **kwargs: Fields to update
        """
        meta_path = self.run_dir / "meta.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        else:
            meta = {}

        meta.update(kwargs)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    def save_result(self, result: dict) -> None:
        """Save execution result.

        Args:
            result: Execution result dictionary
        """
        # Also update completed_at in meta.json
        self.update_meta(completed_at=datetime.now().isoformat())

        with open(self.run_dir / "result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    def save_plan(self, plan: dict) -> None:
        """Save execution plan.

        Args:
            plan: Execution plan dictionary
        """
        with open(self.run_dir / "plan.json", "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)

    def get_log_path(self, name: str) -> Path:
        """Get path for a log file.

        Args:
            name: Log file name (without extension)

        Returns:
            Path to the log file in logs_dir
        """
        # Ensure logs_dir exists
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        return self.logs_dir / f"{name}.log"

    def finalize(self) -> None:
        """Copy workspace results from exec dir to permanent storage, then clean up.

        Should be called after execution completes (in engine finally blocks).
        Copies the entire exec_dir to the permanent run_dir (preserving
        workspace, .claude/skills, and any other files), then removes the
        temp directory.

        Idempotent: safe to call multiple times (e.g. from both normal flow
        and a finally block).
        """
        if self._finalized:
            return
        self._finalized = True

        try:
            if self._exec_root.exists():
                shutil.copytree(self._exec_root, self.run_dir, dirs_exist_ok=True)
        except Exception:
            # Copy failed — keep temp dir so data can be recovered manually
            logger.warning(
                "Failed to copy exec_dir from %s to %s; "
                "temp directory preserved for recovery",
                self._exec_root, self.run_dir,
                exc_info=True,
            )
            return
        # Clean up temp dir only after successful copy
        shutil.rmtree(self._exec_root, ignore_errors=True)

    def __del__(self) -> None:
        """Safety net: clean up temp directory if finalize() was never called."""
        try:
            if not self._finalized and self._exec_root.exists():
                shutil.rmtree(self._exec_root, ignore_errors=True)
        except Exception:
            pass

    # ----- async wrappers (delegate to thread to avoid blocking event loop) -----

    async def async_setup(self, *args, **kwargs) -> None:
        await asyncio.to_thread(self.setup, *args, **kwargs)

    async def async_copy_files(self, *args, **kwargs) -> list[str]:
        return await asyncio.to_thread(self.copy_files, *args, **kwargs)

    async def async_save_meta(self, *args, **kwargs) -> None:
        await asyncio.to_thread(self.save_meta, *args, **kwargs)

    async def async_save_result(self, *args, **kwargs) -> None:
        await asyncio.to_thread(self.save_result, *args, **kwargs)

    async def async_finalize(self) -> None:
        """Async wrapper for finalize()."""
        await asyncio.to_thread(self.finalize)
