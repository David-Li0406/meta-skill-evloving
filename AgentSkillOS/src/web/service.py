"""Web UI adapter — WebSocket broadcasting and UI state management.

Business logic (search → execute) is delegated to workflow.service.
"""

import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

from fastapi import WebSocket
from loguru import logger

from manager import create_manager
from orchestrator.runtime.run_context import RunContext
from orchestrator.visualizers import OrchestratorState
from config import PROJECT_ROOT, get_config
from constants import SKILL_GROUPS, SKILL_GROUP_ALIASES, resolve_skill_group, DEFAULT_BASELINE_TOOLS
from orchestrator.runtime.async_utils import create_tracked_task

from .state import WorkflowPhase, WorkflowState
from .visualizer import WebVisualizer
from .recipe import RecipeStore, RecipeRecommender

# Background task registry to prevent fire-and-forget garbage collection
_bg_tasks: set[asyncio.Task] = set()



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


class WorkflowService:
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
        self.state = WorkflowState()
        self.clients: Set[WebSocket] = set()
        self.manager = None
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

        # Initialize recipe store and recommender
        self.recipe_store = RecipeStore(PROJECT_ROOT / "data/recipes/recipes.json")
        self._recipe_recommender: Optional[RecipeRecommender] = None

        # Cached user prefs manager (avoid re-reading from disk every call)
        self._user_prefs_manager = None

    @property
    def user_prefs_manager(self):
        """Lazily create and cache UserPrefsManager."""
        if self._user_prefs_manager is None:
            from manager.tree.user_prefs import UserPrefsManager
            self._user_prefs_manager = UserPrefsManager()
        return self._user_prefs_manager

    @property
    def recipe_recommender(self) -> RecipeRecommender:
        """Lazily create and cache RecipeRecommender."""
        if self._recipe_recommender is None:
            self._recipe_recommender = RecipeRecommender(self.recipe_store)
        return self._recipe_recommender

    # ── Skill group helpers ────────────────────────────────────────

    def _get_group_by_id(self, group_id: str) -> Optional[dict]:
        """Get a skill group by ID (with alias resolution)."""
        resolved_id = SKILL_GROUP_ALIASES.get(group_id, group_id)

        if resolved_id == "custom":
            return {
                "id": "custom",
                "name": "Custom",
                "description": "User-defined skill set with configurable paths",
                "skills_dir": self.state.custom_skills_dir,
                "tree_path": self.state.custom_tree_path,
                "is_configurable": True,
            }

        return resolve_skill_group(group_id)

    def _get_default_group_id(self) -> str:
        for group in SKILL_GROUPS:
            if group.get("is_default"):
                return group["id"]
        return SKILL_GROUPS[0]["id"] if SKILL_GROUPS else "default"

    def _get_absolute_path(self, path: str) -> Optional[Path]:
        if not path:
            return None
        p = Path(path)
        if p.is_absolute():
            return p
        return PROJECT_ROOT / p

    def get_skill_groups(self) -> list[dict]:
        """Get all skill groups with current selection status."""
        groups = []
        for group in SKILL_GROUPS:
            groups.append({
                "id": group["id"],
                "name": group["name"],
                "description": group["description"],
                "is_current": group["id"] == self.state.current_group_id,
            })
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
        group = self._get_group_by_id(group_id)
        if not group:
            logger.warning(f"Skill group '{group_id}' not found")
            return False
        if self.state.current_group_id == group_id:
            return False

        self.state.current_group_id = group_id
        if group["skills_dir"]:
            self.skill_dir = self._get_absolute_path(group["skills_dir"])
        else:
            self.skill_dir = None
        self.manager = None
        logger.info(f"Switched to skill group: {group['name']} ({group_id})")
        await self.broadcast("skill_group_changed", {
            "group_id": group_id,
            "groups": self.get_skill_groups(),
        })
        return True

    async def set_custom_config(self, skills_dir: str, tree_path: str) -> None:
        self.state.custom_skills_dir = skills_dir
        self.state.custom_tree_path = tree_path
        if self.state.current_group_id == "custom":
            if skills_dir:
                self.skill_dir = self._get_absolute_path(skills_dir)
            else:
                self.skill_dir = None
            self.manager = None
        logger.info(f"Custom config updated: skills_dir={skills_dir}, tree_path={tree_path}")
        await self.broadcast("custom_config_changed", {
            "skills_dir": skills_dir,
            "tree_path": tree_path,
        })

    # ── WebSocket broadcasting ─────────────────────────────────────

    async def broadcast(self, msg_type: str, data: dict) -> None:
        message = {"type": msg_type, "data": data}
        disconnected = set()
        for client in list(self.clients):
            try:
                await client.send_json(message)
            except Exception as e:
                logger.debug(f"Broadcast to client failed: {e}")
                disconnected.add(client)
        self.clients -= disconnected

    async def broadcast_log(self, message: str, level: str = "info") -> None:
        entry = self.state.add_log(message, level)
        await self.broadcast("log", entry)

    def _handle_search_event(self, event_type: str, data: dict) -> None:
        event = {"type": event_type, "data": data, "timestamp": datetime.now().isoformat()}
        self.state.search_events.append(event)
        if self._loop is not None:
            asyncio.run_coroutine_threadsafe(
                self.broadcast("search_event", event),
                self._loop
            )

    # ── UI hints ───────────────────────────────────────────────────

    def _compute_ui_hints(self) -> dict:
        from orchestrator.registry import get_engine_ui_hints

        search_visual = "none"
        if self.manager:
            search_visual = getattr(self.manager, 'visual_type', "tree")

        hints = get_engine_ui_hints(self.state.execution_mode)
        return {
            "search_visual": search_visual,
            "has_planning": hints["needs_planning"],
            "execution_visual": hints["execution_visual"],
            "has_search": self.state.mode == "full",
            "has_skill_review": self.state.mode == "full",
        }

    # ── Common execution lifecycle ─────────────────────────────────

    async def _run_with_lifecycle(
        self,
        run_mode: str,
        folder_mode: str,
        initial_phase: WorkflowPhase,
        run_fn,
    ) -> None:
        """Common execution lifecycle template."""
        self.state.phase = initial_phase
        await self.broadcast("phase", {"phase": initial_phase.value})

        run_context = RunContext.create(
            self.state.task,
            mode=folder_mode,
            task_name=self.state.task_name if self.state.task_name else None,
        )

        self.state.work_dir = str(run_context.run_dir)
        await self.broadcast("work_dir", {"path": self.state.work_dir})

        self.state.orchestrator_state = OrchestratorState()

        def _sync_phase(phase: str) -> None:
            """Keep service state in sync when engine drives phase changes."""
            try:
                self.state.phase = WorkflowPhase(phase)
            except ValueError:
                pass

        visualizer = WebVisualizer(
            self.state.orchestrator_state,
            self.clients,
            on_phase_change=_sync_phase,
        )
        await visualizer.start()

        try:
            result = await run_fn(run_context, visualizer)

            result_dict = {"status": result.status, **result.metadata}
            if result.error:
                result_dict["error"] = result.error

            if result.status == "failed":
                self.state.phase = WorkflowPhase.ERROR
                self.state.completion_status = "failed"
                self.state.error_message = result.error or "Execution failed"
                await self.broadcast("phase", {"phase": "error"})
                await self.broadcast("error", {"message": result.error or "Execution failed"})
                await self.broadcast("result", result_dict)
                await self.broadcast_log(
                    f"{run_mode} execution failed: {result.error or 'unknown error'}",
                    "error",
                )
            else:
                self.state.phase = WorkflowPhase.COMPLETE
                self.state.completion_status = result.status
                await self.broadcast("phase", {"phase": "complete"})
                await self.broadcast("result", result_dict)
                await self.broadcast_log(
                    f"{run_mode} execution completed: {result.status}",
                    "ok" if result.status == "completed" else "warn",
                )
        except Exception as e:
            run_context.save_result({"status": "failed", "error": str(e)})
            self.state.phase = WorkflowPhase.ERROR
            self.state.completion_status = "failed"
            self.state.error_message = str(e)
            await self.broadcast("phase", {"phase": "error"})
            await self.broadcast("error", {"message": str(e)})
            await self.broadcast_log(f"Execution failed: {e}", "error")
        finally:
            await run_context.async_finalize()
            await visualizer.stop()

    # ── Search flow ────────────────────────────────────────────────

    async def start_search(self, task: str, task_name: str = None, files: Optional[list[str]] = None) -> None:
        self._loop = asyncio.get_running_loop()

        self.state.task = task
        self.state.task_name = task_name or ""
        self.state.files = files or []
        self.state.start_time = datetime.now()
        self.state.phase = WorkflowPhase.SEARCHING
        self.state.search_events = []
        self.state.logs = []

        await self.broadcast("phase", {"phase": "searching"})
        await self.broadcast_log(f"Starting search for: {task}", "info")

        current_group = self._get_group_by_id(self.state.current_group_id)
        if current_group:
            group_name = current_group["name"]
            tree_path = self._get_absolute_path(current_group["tree_path"]) if current_group["tree_path"] else None
        else:
            group_name = "Unknown"
            tree_path = None

        await self.broadcast_log(f"Using skill group: {group_name}", "info")

        vector_db_path = self._get_absolute_path(current_group.get("vector_db_path")) if current_group.get("vector_db_path") else None

        self.manager = create_manager(
            tree_path=str(tree_path) if tree_path else None,
            vector_db_path=str(vector_db_path) if vector_db_path else None,
            event_callback=self._handle_search_event,
        )
        self.state.tree_data = self.manager.get_visual_data()
        await self.broadcast("tree_data", {"tree": self.state.tree_data})

        self.state.ui_hints = self._compute_ui_hints()
        await self.broadcast("ui_hints", self.state.ui_hints)

        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.manager.search(task, verbose=False)
            )
            self.state.search_result = result
            # Only pre-select first N skills based on max_skills config
            cfg = get_config()
            all_ids = [s["id"] for s in result.selected_skills]
            self.state.selected_skill_ids = all_ids[:cfg.max_skills]
            self.state.search_complete = True

            # Extract dormant suggestions from layered search
            dormant_suggestions = result.metadata.get("dormant_suggestions", [])
            self.state.dormant_suggestions = dormant_suggestions

            llm_calls = result.metadata.get("llm_calls", 0)
            await self.broadcast("search_complete", {
                "skills": result.selected_skills,
                "llm_calls": llm_calls,
                "selected_ids": self.state.selected_skill_ids,
                "dormant_suggestions": dormant_suggestions,
            })
            await self.broadcast_log(
                f"Found {len(result.selected_skills)} skills in {llm_calls} LLM calls",
                "ok"
            )
        except Exception as e:
            self.state.phase = WorkflowPhase.ERROR
            await self.broadcast("phase", {"phase": "error"})
            await self.broadcast("error", {"message": str(e)})
            await self.broadcast_log(f"Search failed: {e}", "error")

    async def update_skills(self, skill_ids: list[str]) -> None:
        """Update the selected skill IDs, tracking any dormant skills used."""
        # Track dormant skills being added
        dormant_ids = {s.get("id") for s in self.state.dormant_suggestions}
        newly_added_dormant = [sid for sid in skill_ids if sid in dormant_ids and sid not in self.state.dormant_skills_used]
        if newly_added_dormant:
            self.state.dormant_skills_used.extend(newly_added_dormant)

        self.state.selected_skill_ids = skill_ids
        await self.broadcast("skills_updated", {"selected_ids": skill_ids})
        await self.broadcast_log(f"Updated skill selection: {len(skill_ids)} skills", "info")

    async def confirm_search(self) -> None:
        self.state.search_complete = False
        self.state.phase = WorkflowPhase.REVIEWING
        await self.broadcast("phase", {"phase": "reviewing"})
        await self.broadcast_log("Proceeding to review skills", "info")

    # ── Execution (delegates to engine via registry) ────────────────

    async def confirm_skills(self, execution_mode: str = "dag") -> None:
        """Start execution with the selected engine mode."""
        from orchestrator.registry import create_engine, get_engine_execution_meta
        from orchestrator.base import EngineRequest

        self.state.execution_mode = execution_mode
        self.state.ui_hints = self._compute_ui_hints()
        await self.broadcast("ui_hints", self.state.ui_hints)

        skills = self.state.selected_skill_ids or []
        files = self.state.files or None

        # Read folder_mode and initial_phase from engine class metadata
        meta = get_engine_execution_meta(execution_mode)
        folder_mode = meta["folder_mode"]
        initial_phase_str = meta["initial_phase"]

        # Freestyle special case: folder_mode depends on whether skills are selected
        if execution_mode == "free-style":
            folder_mode = "free_style_selected" if skills else "free_style_all"

        initial_phase = WorkflowPhase(initial_phase_str)

        await self.broadcast_log(
            f"Starting {execution_mode} execution with {len(skills)} skills", "info"
        )

        async def _run(run_context, visualizer):
            # Build log_callback that bridges to visualizer
            def log_callback(msg: str, level: str = "info") -> None:
                create_tracked_task(visualizer.add_log(msg, level), _bg_tasks)

            # DAG needs explicit setup before engine construction
            if execution_mode == "dag":
                run_context.setup(skills, self.skill_dir)
                await self.broadcast_log(f"Skills copied to: {run_context.skills_dir}", "info")
                skill_dir = run_context.skills_dir
                # Don't override phase here — let the engine manage
                # planning → executing transition via visualizer
            else:
                skill_dir = self.skill_dir

            engine = create_engine(
                execution_mode,
                run_context=run_context,
                skill_dir=skill_dir,
                log_callback=log_callback,
                allowed_tools=DEFAULT_BASELINE_TOOLS if execution_mode == "no-skill" else None,
                max_concurrent=self.max_concurrent,
            )

            request = EngineRequest(
                task=self.state.task,
                skills=skills,
                files=files,
                visualizer=visualizer,
                copy_all_skills=(execution_mode == "free-style" and not skills),
            )
            return await engine.run(request)

        await self._run_with_lifecycle(execution_mode, folder_mode, initial_phase, _run)

    async def start_direct_execution(self) -> None:
        """Start direct execution for execute mode (bypasses search)."""
        if self._execution_started:
            return
        self._execution_started = True

        from orchestrator.registry import resolve_engine_alias

        self.state.start_time = datetime.now()
        run_mode = self.state.run_mode or "dag"
        engine_mode = resolve_engine_alias(run_mode)
        skills = self.state.preset_skills or []

        self.state.selected_skill_ids = skills
        self.state.execution_mode = engine_mode
        self.state.ui_hints = self._compute_ui_hints()
        await self.broadcast("ui_hints", self.state.ui_hints)
        await self.broadcast_log(f"Starting direct execution in {engine_mode} mode", "info")

        # All modes go through the unified confirm_skills path
        await self.confirm_skills(engine_mode)

    # ── Skill detail / file content (UI helpers) ───────────────────

    async def get_skill_detail(self, skill_id: str, skill_path: str) -> None:
        try:
            skill_md_path = Path(skill_path)
            if not skill_md_path.exists():
                await self.broadcast("skill_detail", {
                    "skill_id": skill_id, "name": "", "description": "",
                    "content": "SKILL.md not found", "directory_tree": None,
                })
                return

            skill_dir = skill_md_path.parent
            raw_content = skill_md_path.read_text(encoding="utf-8")
            parsed = self._parse_skill_md(raw_content)
            directory_tree = self._build_directory_tree(skill_dir)

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
                "skill_id": skill_id, "name": "", "description": "",
                "content": f"Error: {str(e)}", "directory_tree": None,
            })

    def _build_directory_tree(self, path: Path, max_depth: int = 5, current_depth: int = 0) -> dict:
        if current_depth > max_depth:
            return None
        result = {
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
        }
        if path.is_dir():
            children = []
            try:
                entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for entry in entries:
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
        result = {"name": "", "description": "", "body": content}
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n?'
        match = re.match(frontmatter_pattern, content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            body = content[match.end():]
            name_match = re.search(r'^name:\s*(.+)$', frontmatter_text, re.MULTILINE)
            if name_match:
                result["name"] = name_match.group(1).strip().strip('"\'')
            desc_match = re.search(r'^description:\s*(.+)$', frontmatter_text, re.MULTILINE)
            if desc_match:
                result["description"] = desc_match.group(1).strip().strip('"\'')
            result["body"] = body.strip()
        return result

    async def get_file_content(self, skill_path: str, relative_path: str) -> None:
        try:
            skill_dir = Path(skill_path).parent
            file_path = skill_dir / relative_path

            if not file_path.resolve().is_relative_to(skill_dir.resolve()):
                await self.broadcast("file_content", {
                    "path": relative_path, "content": "",
                    "error": "Access denied: file outside skill directory"
                })
                return

            if not file_path.exists():
                await self.broadcast("file_content", {
                    "path": relative_path, "content": "",
                    "error": "File not found"
                })
                return

            if not file_path.is_file():
                await self.broadcast("file_content", {
                    "path": relative_path, "content": "",
                    "error": "Not a file"
                })
                return

            file_ext = file_path.suffix.lower()
            if file_ext in BINARY_EXTENSIONS:
                await self.broadcast("file_content", {
                    "path": relative_path, "content": "", "is_binary": True,
                    "error": f"Binary file ({file_ext}) cannot be displayed"
                })
                return

            content = file_path.read_text(encoding="utf-8", errors="replace")
            await self.broadcast("file_content", {
                "path": relative_path,
                "content": content,
            })
        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            await self.broadcast("file_content", {
                "path": relative_path, "content": "",
                "error": str(e)
            })

    # ── Recipe methods ────────────────────────────────────────────

    async def save_recipe(self, name: str) -> dict:
        """Save current execution as a recipe with LLM-generated description."""
        from dataclasses import asdict
        from orchestrator.runtime.client import SkillClient

        if not self.state.orchestrator_state:
            raise ValueError("No execution state to save")

        # Get the current selected plan
        plan_index = self.state.orchestrator_state.selected_plan_index or 0
        plans = self.state.orchestrator_state.plans
        dag_plan = plans[plan_index] if plans and plan_index < len(plans) else {}

        # Generate description using LLM for semantic matching
        skills_str = ", ".join(self.state.selected_skill_ids[:10])
        desc_prompt = f"""Generate a concise description (1-2 sentences) for a recipe that:
- Accomplishes this task: "{self.state.task[:200]}"
- Uses these skills: {skills_str}

The description should capture the core purpose and be useful for semantic matching.
Return only the description text, no quotes or labels."""

        try:
            client = SkillClient()
            description = await client.execute(desc_prompt)
            description = description.strip().strip('"')[:200]
        except Exception as e:
            logger.warning(f"Failed to generate recipe description: {e}")
            description = f"Recipe using {len(self.state.selected_skill_ids)} skills"

        recipe = self.recipe_store.create(
            name=name,
            description=description,
            original_prompt=self.state.task,
            skill_ids=self.state.selected_skill_ids,
            dag_plan=dag_plan,
            skill_group_id=self.state.current_group_id,
        )
        await self.broadcast("recipe_saved", {"recipe": asdict(recipe)})
        await self.broadcast_log(f"Recipe saved: {name}", "ok")
        return asdict(recipe)

    async def recommend_recipes(self, prompt: str, limit: int = 3) -> list[dict]:
        """Recommend relevant recipes using embedding similarity.

        Uses pure cosine similarity on embeddings for near-instant matching
        instead of LLM calls.
        """
        from dataclasses import asdict

        recipes = self.recipe_store.list_all()
        if not recipes:
            self.state.recommended_recipes = []
            await self.broadcast("recipe_recommendations", {"recipes": []})
            return []

        try:
            matched = await asyncio.to_thread(
                self.recipe_recommender.recommend, prompt, limit
            )
            result = [asdict(r) for r in matched]
            self.state.recommended_recipes = result  # persist for refresh restore
            await self.broadcast("recipe_recommendations", {"recipes": result})
            return result
        except Exception as e:
            logger.error(f"Recipe recommendation failed: {e}")
            self.state.recommended_recipes = []
            await self.broadcast("recipe_recommendations", {"recipes": []})
            return []

    async def execute_recipe(self, recipe_id: str, files: list[str] = None) -> None:
        """Execute a recipe directly, skipping search."""
        from dataclasses import asdict

        recipe = self.recipe_store.get(recipe_id)
        if not recipe:
            await self.broadcast("error", {"message": f"Recipe not found: {recipe_id}"})
            return

        # Increment usage count
        self.recipe_store.increment_usage(recipe_id)

        # Set execution state from recipe
        self.state.task = recipe.original_prompt
        self.state.selected_skill_ids = recipe.skill_ids
        self.state.files = files or []

        # Use set_skill_group to properly sync skill_dir (not just current_group_id)
        if recipe.skill_group_id != self.state.current_group_id:
            await self.set_skill_group(recipe.skill_group_id)

        await self.broadcast_log(f"Executing recipe: {recipe.name}", "info")
        await self.broadcast("recipe_execution_started", {"recipe_id": recipe_id})

        # Skip search and go directly to DAG execution
        await self.confirm_skills(execution_mode="dag")

    # ── Skill sedimentation (active/dormant layering) ─────────────────

    def _resolve_layered_tree_paths(self) -> tuple[Optional[Path], Optional[Path]]:
        """Resolve active_tree and dormant_index paths for current skill group."""
        layering_cfg = get_config().layering_config()

        current_group = self._get_group_by_id(self.state.current_group_id)
        if current_group and current_group.get("tree_path"):
            tree_path = self._get_absolute_path(current_group["tree_path"])
            tree_dir = tree_path.parent
            if layering_cfg.is_directory_mode:
                # Directory-based: normal tree IS the active tree
                return tree_path, tree_dir / "dormant_index.yaml"
            else:
                # Install-count based: separate active_tree.yaml
                return tree_dir / "active_tree.yaml", tree_dir / "dormant_index.yaml"
        return None, None

    async def _promote_skill_to_active_tree(self, skill_id: str) -> bool:
        """Promote a single skill to active tree and update vector index.

        Returns True if the skill was promoted.
        """
        from manager.tree.layer_processor import promote_skill_to_active

        active_tree_path, dormant_index_path = self._resolve_layered_tree_paths()
        if not active_tree_path or not dormant_index_path:
            return False
        if not active_tree_path.exists() or not dormant_index_path.exists():
            return False

        promoted = await asyncio.to_thread(
            promote_skill_to_active,
            skill_id, active_tree_path, dormant_index_path,
        )
        if promoted:
            await self.broadcast_log(f"Added {skill_id} to active tree", "ok")
            await self._remove_skill_from_vector_index(skill_id)
        return promoted

    async def confirm_skill_sedimentation(self, skill_ids: list[str]) -> dict:
        """
        Confirm sedimentation of dormant skills after successful execution.

        This pins the dormant skills permanently so they become part of the
        active set in future searches.

        Args:
            skill_ids: List of dormant skill IDs to pin

        Returns:
            Dict with pinned skill info.
        """
        cfg = get_config()
        layering_cfg = cfg.layering_config()

        if not layering_cfg.is_enabled:
            await self.broadcast_log("Layering is disabled, skipping sedimentation", "warn")
            return {"pinned": [], "skipped": skill_ids}

        current_group = self._get_group_by_id(self.state.current_group_id)

        prefs_manager = self.user_prefs_manager
        pinned = []
        promoted = []
        skipped = []

        for skill_id in skill_ids:
            # Only pin if it was actually a dormant skill used in this session
            if skill_id in self.state.dormant_skills_used:
                if prefs_manager.pin_skill(skill_id):
                    pinned.append(skill_id)
                    await self.broadcast_log(f"Pinned dormant skill: {skill_id}", "ok")

                    if await self._promote_skill_to_active_tree(skill_id):
                        promoted.append(skill_id)

                    # Create symlink only after successful tree promotion
                    if layering_cfg.is_directory_mode:
                        await self._create_active_symlink(skill_id, current_group)
                else:
                    skipped.append(skill_id)  # Already pinned
            else:
                skipped.append(skill_id)

        if pinned:
            await self.broadcast("skill_pinned", {
                "skill_ids": pinned,
                "status": "pinned",
            })

        # Clear dormant skills used for this session
        self.state.dormant_skills_used = []

        return {"pinned": pinned, "promoted": promoted, "skipped": skipped}

    async def pin_skill(self, skill_id: str) -> bool:
        """Pin a single skill (make it permanently active)."""
        prefs_manager = self.user_prefs_manager
        result = prefs_manager.pin_skill(skill_id)

        if result:
            await self.broadcast("skill_pinned", {
                "skill_id": skill_id,
                "status": "pinned",
            })
            await self.broadcast_log(f"Pinned skill: {skill_id}", "ok")

            layering_cfg = get_config().layering_config()

            if layering_cfg.is_directory_mode:
                current_group = self._get_group_by_id(self.state.current_group_id)
                if current_group:
                    await self._create_active_symlink(skill_id, current_group)

            # Promote in active tree (works for both directory-based and install-count)
            if layering_cfg.is_enabled:
                await self._promote_skill_to_active_tree(skill_id)

        return result

    async def unpin_skill(self, skill_id: str) -> bool:
        """Unpin a single skill (allow it to become dormant again)."""
        prefs_manager = self.user_prefs_manager
        result = prefs_manager.unpin_skill(skill_id)

        if result:
            await self.broadcast("skill_unpinned", {
                "skill_id": skill_id,
                "status": "unpinned",
            })

            layering_cfg = get_config().layering_config()
            if layering_cfg.is_directory_mode:
                current_group = self._get_group_by_id(self.state.current_group_id)
                if current_group:
                    await self._remove_active_symlink(skill_id, current_group)

            await self.broadcast_log(f"Unpinned skill: {skill_id}", "info")

        return result

    async def _create_active_symlink(self, skill_id: str, group: dict) -> None:
        """Create symlink in skills_dir -> dormant_skills_dir for pinned skill."""
        if not group or ".." in skill_id or "/" in skill_id:
            return

        try:
            layering_cfg = get_config().layering_config()
            if not layering_cfg.dormant_skills_dir:
                return
            dormant_dir = PROJECT_ROOT / layering_cfg.dormant_skills_dir
            skills_dir = self._get_absolute_path(group["skills_dir"])
            if not skills_dir:
                return
            source = dormant_dir / skill_id
            target = skills_dir / skill_id
            if source.exists() and not target.exists():
                # Validate source resolves within dormant_dir (prevent path traversal)
                if not source.resolve().is_relative_to(dormant_dir.resolve()):
                    await self.broadcast_log(f"Rejected symlink for {skill_id}: source outside dormant dir", "warn")
                    return
                skills_dir.mkdir(parents=True, exist_ok=True)
                target.symlink_to(source.resolve())
                await self.broadcast_log(f"Created symlink: {skill_id} -> active", "ok")
        except OSError as e:
            await self.broadcast_log(f"Failed to create symlink for {skill_id}: {e}", "warn")

    async def _remove_active_symlink(self, skill_id: str, group: dict) -> None:
        """Remove symlink from skills_dir if it points to dormant_skills_dir."""
        if not group or ".." in skill_id or "/" in skill_id:
            return
        try:
            layering_cfg = get_config().layering_config()
            if not layering_cfg.dormant_skills_dir:
                return
            skills_dir = self._get_absolute_path(group["skills_dir"])
            if not skills_dir:
                return
            target = skills_dir / skill_id
            if target.is_symlink():
                dormant_dir = (PROJECT_ROOT / layering_cfg.dormant_skills_dir).resolve()
                # Only remove if it's a symlink pointing to dormant dir
                resolved = target.resolve()
                if resolved.is_relative_to(dormant_dir):
                    target.unlink()
                    await self.broadcast_log(f"Removed symlink: {skill_id} -> dormant", "info")
        except OSError as e:
            await self.broadcast_log(f"Failed to remove symlink for {skill_id}: {e}", "warn")

    async def _remove_skill_from_vector_index(self, skill_id: str) -> None:
        """Incrementally remove a single skill from the dormant vector index."""
        try:
            import chromadb
            from manager.tree.dormant_searcher import DormantVectorSearcher

            db_path = str(PROJECT_ROOT / "data" / "vector_stores" / "dormant")
            client = chromadb.PersistentClient(path=db_path)
            existing = [c.name for c in client.list_collections()]
            if DormantVectorSearcher.COLLECTION_NAME in existing:
                collection = client.get_collection(DormantVectorSearcher.COLLECTION_NAME)
                await asyncio.to_thread(collection.delete, ids=[skill_id])
        except Exception as e:
            await self.broadcast_log(f"Vector index incremental delete warning: {e}", "warn")

    async def get_skill_status_stats(self) -> dict:
        """Get statistics about active/dormant/pinned skills."""
        from manager.tree.layered_searcher import layered_files_exist

        import yaml

        cfg = get_config()
        layering_cfg = cfg.layering_config()

        if not layering_cfg.is_enabled:
            return {"enabled": False}

        current_group = self._get_group_by_id(self.state.current_group_id)
        if not current_group:
            return {"enabled": True, "error": "No skill group selected"}

        tree_path = current_group.get("tree_path")
        if not tree_path:
            return {"enabled": True, "error": "No tree path configured"}

        tree_dir = self._get_absolute_path(tree_path)
        if tree_dir:
            tree_dir = tree_dir.parent
        else:
            return {"enabled": True, "error": "Invalid tree path"}

        # Directory mode: only dormant_index.yaml is required (active tree is the normal tree)
        # Install-count mode: both active_tree.yaml and dormant_index.yaml are required
        if layering_cfg.is_directory_mode:
            if not (tree_dir / "dormant_index.yaml").exists():
                return {"enabled": True, "layered_files_exist": False}
        elif not layered_files_exist(tree_dir):
            return {"enabled": True, "layered_files_exist": False}

        prefs_manager = self.user_prefs_manager
        pinned_count = len(prefs_manager.get_pinned_ids())

        # Count skills from active tree and dormant index (offload IO to thread)
        active_count = 0
        dormant_count = 0

        def _read_counts():
            a_count, d_count = 0, 0
            try:
                # For directory-based: active tree is the normal tree file
                if layering_cfg.is_directory_mode:
                    a_path = self._get_absolute_path(current_group["tree_path"])
                else:
                    a_path = tree_dir / "active_tree.yaml"
                d_path = tree_dir / "dormant_index.yaml"
                if a_path and a_path.exists():
                    with open(a_path, "r", encoding="utf-8") as f:
                        a_tree = yaml.safe_load(f)
                    a_count = self._count_skills_in_tree(a_tree)
                if d_path.exists():
                    with open(d_path, "r", encoding="utf-8") as f:
                        d_idx = yaml.safe_load(f)
                    d_count = d_idx.get("skills_count", 0)
            except Exception as e:
                logger.error(f"Failed to count skills: {e}")
            return a_count, d_count

        active_count, dormant_count = await asyncio.to_thread(_read_counts)

        return {
            "enabled": True,
            "layered_files_exist": True,
            "active": active_count,
            "dormant": dormant_count,
            "pinned": pinned_count,
            "threshold": layering_cfg.active_threshold,
        }

    @staticmethod
    def _count_skills_in_tree(tree_dict: dict) -> int:
        """Recursively count skills in a tree structure."""
        from manager.tree.layer_processor import _count_skills_in_node
        return _count_skills_in_node(tree_dict)
