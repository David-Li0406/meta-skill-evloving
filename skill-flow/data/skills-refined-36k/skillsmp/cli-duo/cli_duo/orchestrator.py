#!/usr/bin/env python3
"""Coordinate two AI CLIs working in the same repository."""
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config/cli-duo"
DATA_DIR = Path.home() / ".local/share/cli-duo"
REGISTRY_FILE = CONFIG_DIR / "registry.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
WORKTREES_DIR = DATA_DIR / "worktrees"


def ensure_dirs() -> None:
    """Create config and data directories."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WORKTREES_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("Failed to parse %s; using defaults.", path)
        return default


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_registry() -> Dict[str, Dict[str, str]]:
    ensure_dirs()
    payload = _read_json(REGISTRY_FILE, {"clis": {}})
    return payload.get("clis", {})


def save_registry(clis: Dict[str, Dict[str, str]]) -> None:
    ensure_dirs()
    _write_json(REGISTRY_FILE, {"clis": clis})


def list_registered_clis() -> List[Dict[str, str]]:
    clis = load_registry()
    return [
        {"name": name, **meta}
        for name, meta in sorted(clis.items(), key=lambda item: item[0])
    ]


def register_cli(
    name: str,
    command: str,
    repo: Optional[str],
    cli_type: Optional[str],
    description: Optional[str],
) -> Tuple[bool, str]:
    ensure_dirs()
    clis = load_registry()
    clis[name] = {
        "command": command,
        "default_repo": str(Path(repo).expanduser().resolve())
        if repo
        else None,
        "type": cli_type,
        "description": description,
    }
    save_registry(clis)
    return True, f"✓ Registered CLI '{name}' ({command})"


def remove_cli(name: str) -> Tuple[bool, str]:
    clis = load_registry()
    if name not in clis:
        return False, f"CLI '{name}' is not registered"
    clis.pop(name)
    save_registry(clis)
    return True, f"✓ Removed CLI '{name}'"


def load_sessions() -> Dict[str, dict]:
    ensure_dirs()
    payload = _read_json(SESSIONS_FILE, {"sessions": {}})
    return payload.get("sessions", {})


def save_sessions(sessions: Dict[str, dict]) -> None:
    ensure_dirs()
    _write_json(SESSIONS_FILE, {"sessions": sessions})


def _verify_git_repo(repo_path: Path) -> Tuple[bool, str]:
    try:
        subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True, ""
    except FileNotFoundError:
        return False, "git is not installed or not on PATH"
    except subprocess.CalledProcessError as exc:
        return False, f"{repo_path} is not a git repository: {exc.stderr.decode('utf-8', 'ignore')}"


def _create_worktree(repo_path: Path, worktree_path: Path) -> Tuple[bool, str]:
    if worktree_path.exists():
        return False, f"Worktree path already exists: {worktree_path}"
    worktree_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "add", "--detach", str(worktree_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True, f"Created subordinate worktree at {worktree_path}"
    except subprocess.CalledProcessError as exc:
        return False, f"Failed to create worktree: {exc.stderr.decode('utf-8', 'ignore')}"


def _remove_worktree(repo_path: Path, worktree_path: Path) -> Tuple[bool, str]:
    if not worktree_path.exists():
        return True, f"Worktree path already removed: {worktree_path}"
    try:
        subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "remove", "--force", str(worktree_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True, f"Removed worktree at {worktree_path}"
    except subprocess.CalledProcessError as exc:
        return False, f"Failed to remove worktree: {exc.stderr.decode('utf-8', 'ignore')}"


def create_session(
    session: str,
    primary_cli: str,
    secondary_cli: str,
    mode: str,
    repo: Optional[str],
    worktree_path: Optional[str],
    rounds_per_role: int,
    description: Optional[str],
    dry_run: bool,
    confirm: bool,
) -> Tuple[bool, str, Optional[dict]]:
    ensure_dirs()
    clis = load_registry()
    if primary_cli not in clis:
        return False, f"Primary CLI '{primary_cli}' is not registered", None
    if secondary_cli not in clis:
        return False, f"Secondary CLI '{secondary_cli}' is not registered", None

    sessions = load_sessions()
    if session in sessions and not dry_run:
        return False, f"Session '{session}' already exists", None

    repo_path = Path(repo).expanduser().resolve() if repo else None
    session_payload: dict = {
        "mode": mode,
        "primary_cli": primary_cli,
        "secondary_cli": secondary_cli,
        "description": description,
        "repo": str(repo_path) if repo_path else None,
        "rounds_per_role": rounds_per_role,
        "current_round": 1,
    }

    if mode == "subordinate":
        if not repo_path:
            return False, "--repo is required for subordinate mode", None
        valid_repo, reason = _verify_git_repo(repo_path)
        if not valid_repo:
            return False, reason, None
        worktree = (
            Path(worktree_path).expanduser().resolve()
            if worktree_path
            else WORKTREES_DIR / session / "secondary"
        )
        session_payload["worktree_path"] = str(worktree)
        session_payload["roles"] = {"primary": primary_cli, "subordinate": secondary_cli}
        if dry_run:
            return True, f"DRY RUN: would create worktree at {worktree}", session_payload
        if not confirm:
            return False, "--confirm required to create subordinate worktree", None
        success, msg = _create_worktree(repo_path, worktree)
        if not success:
            return False, msg, None
    elif mode == "engineer-judge":
        session_payload["roles"] = {"engineer": primary_cli, "judge": secondary_cli}
        session_payload["worktree_path"] = None
    else:
        return False, f"Unsupported mode '{mode}'", None

    if not dry_run:
        sessions[session] = session_payload
        save_sessions(sessions)
    summary = render_session_summary(session, session_payload)
    return True, summary, session_payload


def list_sessions() -> List[dict]:
    sessions = load_sessions()
    return [
        {"name": name, **payload}
        for name, payload in sorted(sessions.items(), key=lambda item: item[0])
    ]


def get_session(session: str) -> Optional[dict]:
    sessions = load_sessions()
    return sessions.get(session)


def swap_roles(session: str) -> Tuple[bool, str, Optional[dict]]:
    sessions = load_sessions()
    payload = sessions.get(session)
    if not payload:
        return False, f"Session '{session}' not found", None

    mode = payload.get("mode")
    roles = payload.get("roles", {})
    if mode == "engineer-judge":
        roles["engineer"], roles["judge"] = roles.get("judge"), roles.get("engineer")
        payload["current_round"] = int(payload.get("current_round", 1)) + 1
    elif mode == "subordinate":
        roles["primary"], roles["subordinate"] = roles.get("subordinate"), roles.get("primary")
    else:
        return False, f"Unsupported mode '{mode}'", None

    payload["roles"] = roles
    sessions[session] = payload
    save_sessions(sessions)
    return True, render_session_summary(session, payload), payload


def end_session(session: str, confirm: bool, dry_run: bool) -> Tuple[bool, str]:
    sessions = load_sessions()
    payload = sessions.get(session)
    if not payload:
        return False, f"Session '{session}' not found"

    worktree_path = payload.get("worktree_path")
    repo_path = payload.get("repo")

    if worktree_path and repo_path:
        if dry_run:
            return True, f"DRY RUN: would remove worktree {worktree_path} and delete session '{session}'"
        if not confirm:
            return False, "--confirm required to remove worktree and delete session"
        success, msg = _remove_worktree(Path(repo_path), Path(worktree_path))
        if not success:
            return False, msg

    if dry_run:
        return True, f"DRY RUN: would delete session '{session}'"

    sessions.pop(session, None)
    save_sessions(sessions)
    return True, f"✓ Deleted session '{session}'"


def render_session_summary(name: str, payload: dict) -> str:
    mode = payload.get("mode")
    lines = [f"Session: {name}", f"Mode: {mode}"]
    roles = payload.get("roles", {})
    if mode == "engineer-judge":
        lines.append(f"Engineer: {roles.get('engineer')}")
        lines.append(f"Judge: {roles.get('judge')}")
        lines.append(f"Rounds per role: {payload.get('rounds_per_role')}")
        lines.append(f"Current round: {payload.get('current_round', 1)}")
    else:
        lines.append(f"Primary: {roles.get('primary')}")
        lines.append(f"Subordinate: {roles.get('subordinate')}")
    if payload.get("repo"):
        lines.append(f"Repo: {payload['repo']}")
    if payload.get("worktree_path"):
        lines.append(f"Subordinate worktree: {payload['worktree_path']}")
    if payload.get("description"):
        lines.append(f"Notes: {payload['description']}")
    return "\n".join(lines)
