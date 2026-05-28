"""Web UI template loader and static file utilities.

Provides functions to load and assemble HTML templates for the AgentSkillOS web UI.
Supports INCLUDE (static file inclusion) and SLOT (module-contributed UI fragments).
"""

import re
from pathlib import Path
from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Directory paths
WEB_DIR = Path(__file__).parent
TEMPLATES_DIR = WEB_DIR / "templates"
STATIC_DIR = WEB_DIR / "static"

# Pattern for <!-- INCLUDE:path/to/fragment.html -->
_INCLUDE_RE = re.compile(r"[ \t]*<!-- INCLUDE:(\S+) -->[ \t]*\n?")

# Pattern for <!-- SLOT:name -->
_SLOT_RE = re.compile(r"[ \t]*<!-- SLOT:(\w+) -->[ \t]*\n?")


# ── UI Contributions ────────────────────────────────────────────
# Dynamically collected from registered manager/orchestrator classes.
# Each class declares a ``ui_contribution`` class attribute with its
# partials, scripts, and modals.

def _get_manager_contributions() -> dict[str, dict]:
    from manager.registry import get_all_manager_contributions
    return get_all_manager_contributions()

def _get_orchestrator_contributions() -> dict[str, dict]:
    from orchestrator.registry import get_all_engine_contributions
    return get_all_engine_contributions()

# Default contributions used when no specific module is requested
_DEFAULT_MANAGER = "tree"
_DEFAULT_ORCHESTRATOR = "dag"


def _resolve_includes(html: str, max_depth: int = 5) -> str:
    """Recursively resolve <!-- INCLUDE:path --> markers in HTML.

    Each marker is replaced with the contents of the referenced file
    under TEMPLATES_DIR. Supports nested includes up to max_depth.
    """
    for _ in range(max_depth):
        match = _INCLUDE_RE.search(html)
        if not match:
            break
        fragment_path = TEMPLATES_DIR / match.group(1)
        fragment = fragment_path.read_text(encoding="utf-8")
        html = html[:match.start()] + fragment + html[match.end():]
    return html


def _resolve_slots(html: str, slot_map: dict[str, str]) -> str:
    """Resolve <!-- SLOT:name --> markers using the provided slot_map.

    Args:
        html: HTML string containing SLOT markers
        slot_map: Mapping from slot name to HTML content to insert

    Unmatched slots are replaced with empty string (slot is optional).
    """
    def _replace_slot(match: re.Match) -> str:
        slot_name = match.group(1)
        return slot_map.get(slot_name, "")
    return _SLOT_RE.sub(_replace_slot, html)


def _build_slot_map(
    manager_contrib: Optional[dict] = None,
) -> dict[str, str]:
    """Build a slot name -> HTML content mapping from contributions.

    Manager partials are loaded from a single contribution.
    Orchestrator partials are loaded from ALL contributions so that
    every execute partial is present in the page (each guarded by x-show).
    """
    slot_map = {}

    if manager_contrib:
        for slot_name, partial_path in manager_contrib.get("partials", {}).items():
            path = TEMPLATES_DIR / partial_path
            if path.exists():
                slot_map[slot_name] = path.read_text(encoding="utf-8")

    # Build execute slot from ALL orchestrator partials
    orch_contribs = _get_orchestrator_contributions()
    execute_parts = []
    for contrib in orch_contribs.values():
        partial_path = contrib.get("partials", {}).get("execute")
        if partial_path:
            path = TEMPLATES_DIR / partial_path
            if path.exists():
                execute_parts.append(path.read_text(encoding="utf-8"))
    slot_map["execute"] = "\n".join(execute_parts)

    # Build manager modals
    manager_modals = []
    if manager_contrib:
        for modal_path in manager_contrib.get("modals", []):
            path = TEMPLATES_DIR / modal_path
            if path.exists():
                manager_modals.append(path.read_text(encoding="utf-8"))
    # Add standalone recipe modal (not tied to any specific manager)
    recipe_modal_path = TEMPLATES_DIR / "modules/recipe/recipe-detail-modal.html"
    if recipe_modal_path.exists():
        manager_modals.append(recipe_modal_path.read_text(encoding="utf-8"))
    slot_map["manager_modals"] = "\n".join(manager_modals)

    # Build orchestrator modals from ALL orchestrators (deduplicated)
    orchestrator_modals = []
    seen_modals = set()
    for contrib in orch_contribs.values():
        for modal_path in contrib.get("modals", []):
            if modal_path not in seen_modals:
                seen_modals.add(modal_path)
                path = TEMPLATES_DIR / modal_path
                if path.exists():
                    orchestrator_modals.append(path.read_text(encoding="utf-8"))
    slot_map["orchestrator_modals"] = "\n".join(orchestrator_modals)

    return slot_map


def get_template(
    name: str,
    manager_id: Optional[str] = None,
) -> str:
    """Load and assemble a template by name.

    Args:
        name: Template name without extension (currently only 'unified' is supported)
        manager_id: Manager module ID (e.g., 'tree'). Defaults to 'tree'.

    Returns:
        Complete HTML string with base template and content merged

    All registered orchestrator contributions are loaded automatically so that
    the frontend can switch between engines without a page reload.

    The template system uses simple string replacement:
    - <!-- TITLE --> is replaced with the page title
    - <!-- HEAD_EXTRA --> is replaced with extra head content (e.g., D3.js for unified)
    - <!-- SCRIPTS --> is replaced with page-specific script tags
    - <!-- APP_DATA --> is replaced with the Alpine.js app function name
    - <!-- ESCAPE_HANDLER --> is replaced with the escape key handler
    - <!-- CONTENT --> is replaced with the page-specific HTML content
    - <!-- APP_SCRIPT --> is replaced with the page-specific JavaScript
    - <!-- INCLUDE:path --> is replaced with the contents of templates/path
    - <!-- SLOT:name --> is replaced with module-contributed partials
    """
    base_html = (TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
    content_html = (TEMPLATES_DIR / f"{name}.html").read_text(encoding="utf-8")

    # Resolve module contributions
    mgr_id = manager_id or _DEFAULT_MANAGER
    manager_contrib = _get_manager_contributions().get(mgr_id)

    # Resolve slots in content (manager partials + ALL orchestrator partials/modals)
    slot_map = _build_slot_map(manager_contrib)
    content_html = _resolve_slots(content_html, slot_map)

    # Resolve includes in content
    content_html = _resolve_includes(content_html)

    # Build script tags: core → module slices → app-shell
    core_scripts = (
        '<script src="/static/js/core/initial-state.js"></script>\n'
        '<script src="/static/js/core/ws-handlers.js"></script>\n'
        '<script src="/static/js/core/phase-hooks.js"></script>\n'
        '<script src="/static/js/core/slice-registry.js"></script>'
    )

    # Collect module scripts (deduplicated, preserving order)
    # Manager scripts first, then ALL orchestrator scripts
    orch_contribs_for_scripts = _get_orchestrator_contributions()
    module_script_tags = []
    seen_scripts = set()
    if manager_contrib:
        for script_path in manager_contrib.get("scripts", []):
            if script_path not in seen_scripts:
                seen_scripts.add(script_path)
                module_script_tags.append(
                    f'<script src="/static/js/{script_path}"></script>'
                )
    for contrib in orch_contribs_for_scripts.values():
        for script_path in contrib.get("scripts", []):
            if script_path not in seen_scripts:
                seen_scripts.add(script_path)
                module_script_tags.append(
                    f'<script src="/static/js/{script_path}"></script>'
                )

    all_scripts = core_scripts
    if module_script_tags:
        all_scripts += "\n" + "\n".join(module_script_tags)
    # Add recipe module script (standalone, not tied to manager/orchestrator)
    all_scripts += '\n<script src="/static/js/modules/recipe/recipe.js"></script>'
    all_scripts += '\n<script src="/static/js/core/app-shell.js"></script>'

    configs = {
        "unified": {
            "title": "AgentSkillOS",
            "head_extra": '<script src="https://d3js.org/d3.v7.min.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>',
            "scripts": all_scripts,
            "app_data": "unifiedApp()",
            "escape_handler": "closeModals()",
            "app_script": "",
        },
    }

    config = configs.get(name, configs["unified"])

    # Perform replacements
    html = base_html
    html = html.replace("<!-- TITLE -->", config["title"])
    html = html.replace("<!-- HEAD_EXTRA -->", config["head_extra"])
    html = html.replace("<!-- SCRIPTS -->", config["scripts"])
    html = html.replace("<!-- APP_DATA -->", config["app_data"])
    html = html.replace("<!-- ESCAPE_HANDLER -->", config["escape_handler"])
    html = html.replace("<!-- CONTENT -->", content_html)
    html = html.replace("<!-- APP_SCRIPT -->", config["app_script"])

    # Resolve any remaining includes (e.g., in base.html)
    html = _resolve_includes(html)

    return html


def mount_static(app: FastAPI) -> None:
    """Mount the static files directory to a FastAPI app.

    Args:
        app: FastAPI application instance

    Mounts static files at /static/ serving CSS and JS from the static directory.
    """
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def get_index_html() -> str:
    """Get the complete HTML for the unified UI.

    Reads the active manager from config to load the correct UI module.

    Returns:
        Complete HTML string ready to serve
    """
    from config import get_config
    cfg = get_config()
    return get_template("unified", manager_id=cfg.manager)


# Import from new modules
from .service import WorkflowService
from .routes import create_app
from .app import run_server

__all__ = [
    "get_template",
    "mount_static",
    "get_index_html",
    "WEB_DIR",
    "TEMPLATES_DIR",
    "STATIC_DIR",
    "WorkflowService",
    "create_app",
    "run_server",
]
