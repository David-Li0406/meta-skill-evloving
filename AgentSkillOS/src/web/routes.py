"""FastAPI routes and WebSocket handlers for the web UI.

Contains the application factory, HTTP endpoints, and WebSocket message dispatch.
"""

import asyncio
import tempfile
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from manager import create_manager
from config import PROJECT_ROOT
from constants import DEMO_TASKS

from . import get_index_html, mount_static
from .state import WorkflowState
from loguru import logger

from orchestrator.runtime.async_utils import create_tracked_task
from .service import WorkflowService

# Temporary upload directory
UPLOAD_DIR = Path(tempfile.gettempdir()) / "unified_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Background task registry to prevent fire-and-forget garbage collection
_background_tasks: set[asyncio.Task] = set()



def create_app(
    max_concurrent: int = 6,
    # Execute mode parameters
    task: str = None,
    preset_skills: list = None,
    mode: str = "full",
    run_mode: str = None,
    files: list = None,
    task_name: str = None,
) -> FastAPI:
    """Create the FastAPI application.

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

    service = WorkflowService(
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
        return get_index_html()

    @app.get("/tree")
    async def get_tree():
        """Get the capability tree data."""
        if service.manager is None:
            service.manager = create_manager()
        return service.manager.get_visual_data()

    @app.post("/api/upload")
    async def upload_files(files: list[UploadFile] = File(...)):
        """Handle file upload."""
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
        results = []
        for file in files:
            # Sanitize filename to prevent path traversal
            safe_name = Path(file.filename).name
            if not safe_name:
                continue

            # Save to temporary directory
            file_path = UPLOAD_DIR / safe_name
            content = await file.read()

            # Enforce file size limit
            if len(content) > MAX_FILE_SIZE:
                return JSONResponse(
                    content={"error": f"File '{safe_name}' exceeds 50MB limit"},
                    status_code=413,
                )

            with open(file_path, "wb") as f:
                f.write(content)

            results.append({
                "name": safe_name,
                "path": str(file_path),
                "size": len(content)
            })

        return {"files": results}

    @app.delete("/api/upload/{filename:path}")
    async def delete_file(filename: str):
        """Delete an uploaded file."""
        file_path = UPLOAD_DIR / filename
        # Prevent path traversal: ensure file is within UPLOAD_DIR
        if not file_path.resolve().is_relative_to(UPLOAD_DIR.resolve()):
            return JSONResponse(
                content={"error": "Access denied: path traversal detected"},
                status_code=403,
            )
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

    # ── Skill layering REST endpoints ────────────────────────────────

    @app.get("/api/skills/status")
    async def get_skills_status():
        """Get skill status statistics (active/dormant/pinned counts)."""
        return await service.get_skill_status_stats()

    class SedimentationRequest(BaseModel):
        skill_ids: list[str]

    @app.post("/api/skills/sedimentation/confirm")
    async def confirm_sedimentation(data: SedimentationRequest):
        """Confirm sedimentation of dormant skills."""
        return await service.confirm_skill_sedimentation(data.skill_ids)

    @app.post("/api/skills/{skill_id}/pin")
    async def pin_skill(skill_id: str):
        """Pin a skill (make permanently active)."""
        result = await service.pin_skill(skill_id)
        return {"skill_id": skill_id, "pinned": result}

    @app.delete("/api/skills/{skill_id}/pin")
    async def unpin_skill(skill_id: str):
        """Unpin a skill (allow it to become dormant)."""
        result = await service.unpin_skill(skill_id)
        return {"skill_id": skill_id, "unpinned": result}

    @app.post("/api/demos/{demo_id}/load")
    async def load_demo(demo_id: str):
        """Load a demo: copy files to upload dir and return prompt + file info."""
        import shutil

        # Find the demo
        demo = next((d for d in DEMO_TASKS if d["id"] == demo_id), None)
        if not demo:
            return JSONResponse(content={"error": "Demo not found"}, status_code=404)

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
                create_tracked_task(service.start_direct_execution(), _background_tasks)

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
                    except Exception:
                        break
                except Exception as e:
                    logger.error(f"WebSocket error: {e}")
                    break

        except WebSocketDisconnect:
            pass
        finally:
            service.clients.discard(websocket)

    return app


async def handle_message(service: WorkflowService, data: dict) -> None:
    """Handle incoming WebSocket messages."""
    msg_type = data.get("type")

    if msg_type == "start_search":
        task = data.get("task", "")
        task_name = data.get("task_name", "")
        files = data.get("files", [])
        create_tracked_task(service.start_search(task, task_name, files), _background_tasks)

    elif msg_type == "update_skills":
        skill_ids = data.get("skill_ids", [])
        await service.update_skills(skill_ids)

    elif msg_type == "confirm_search":
        await service.confirm_search()

    elif msg_type == "confirm_skills":
        execution_mode = data.get("execution_mode", "dag")
        create_tracked_task(service.confirm_skills(execution_mode=execution_mode), _background_tasks)

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
        create_tracked_task(service.get_skill_detail(skill_id, skill_path), _background_tasks)

    elif msg_type == "get_file_content":
        skill_path = data.get("skill_path", "")
        relative_path = data.get("relative_path", "")
        create_tracked_task(service.get_file_content(skill_path, relative_path), _background_tasks)

    elif msg_type == "reset":
        # Reset service state but preserve current skill group and custom config
        current_group_id = service.state.current_group_id
        custom_skills_dir = service.state.custom_skills_dir
        custom_tree_path = service.state.custom_tree_path
        service.state = WorkflowState()
        service.state.current_group_id = current_group_id
        service.state.custom_skills_dir = custom_skills_dir
        service.state.custom_tree_path = custom_tree_path
        # Broadcast phase change
        await service.broadcast("phase", {"phase": "idle"})
        logger.info("State reset to idle")

    # ── Recipe handlers ──────────────────────────────────────────

    elif msg_type == "recommend_recipes":
        prompt = data.get("prompt", "")
        create_tracked_task(service.recommend_recipes(prompt), _background_tasks)

    elif msg_type == "save_recipe":
        name = data.get("name", "")
        create_tracked_task(service.save_recipe(name), _background_tasks)

    elif msg_type == "execute_recipe":
        recipe_id = data.get("recipe_id", "")
        files = data.get("files", [])
        create_tracked_task(service.execute_recipe(recipe_id, files), _background_tasks)

    elif msg_type == "get_recipes":
        from dataclasses import asdict
        recipes = [asdict(r) for r in service.recipe_store.list_all()]
        await service.broadcast("recipes_list", {"recipes": recipes})

    elif msg_type == "delete_recipe":
        recipe_id = data.get("recipe_id", "")
        success = service.recipe_store.delete(recipe_id)
        await service.broadcast("recipe_deleted", {"recipe_id": recipe_id, "success": success})

    # ── Skill layering handlers (sedimentation) ─────────────────────

    elif msg_type == "confirm_sedimentation":
        skill_ids = data.get("skill_ids", [])
        result = await service.confirm_skill_sedimentation(skill_ids)
        await service.broadcast("sedimentation_result", result)

    elif msg_type == "pin_skill":
        skill_id = data.get("skill_id", "")
        await service.pin_skill(skill_id)

    elif msg_type == "unpin_skill":
        skill_id = data.get("skill_id", "")
        await service.unpin_skill(skill_id)

    elif msg_type == "get_skill_status":
        stats = await service.get_skill_status_stats()
        await service.broadcast("skill_status_stats", stats)
