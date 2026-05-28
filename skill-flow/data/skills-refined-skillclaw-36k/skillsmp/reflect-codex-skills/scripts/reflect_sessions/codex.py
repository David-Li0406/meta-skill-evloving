"""Codex execution helpers for reflect_sessions."""

from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .debug import debug_print
from .models import SessionMeta
from session_io import create_copy_with_new_id, extract_uuid_from_filename, read_lines


def extract_message_text(payload: dict[str, Any]) -> str | None:
    """Extract assistant output text from a message payload.

    Args:
        payload: Response payload dictionary.

    Returns:
        Concatenated output text if present.
    """
    content = payload.get("content")
    if not isinstance(content, list):
        return None
    chunks: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "output_text":
            continue
        text = item.get("text")
        if isinstance(text, str):
            chunks.append(text)
    if not chunks:
        return None
    return "".join(chunks).strip()


def extract_last_assistant_text(*, lines: list[str]) -> str:
    """Extract the last assistant response text from JSONL lines.

    Args:
        lines: JSONL lines from a session file.

    Returns:
        Last assistant response text.
    """
    last_text: str | None = None
    for line in lines:
        data = json.loads(line)
        if data.get("type") != "response_item":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get("type") != "message" or payload.get("role") != "assistant":
            continue
        text = extract_message_text(payload=payload)
        if text:
            last_text = text
    assert last_text, "No assistant response found in session"
    return last_text


def list_vscode_codex_candidates(*, base_dir: Path) -> list[Path]:
    """Return codex binaries under a VS Code extensions directory.

    Args:
        base_dir: Base VS Code directory (e.g., ~/.vscode).

    Returns:
        List of candidate codex paths.
    """
    extensions_dir = base_dir / "extensions"
    if not extensions_dir.exists():
        return []
    pattern = str(extensions_dir / "openai.chatgpt-*" / "bin" / "*" / "codex")
    return [Path(path) for path in glob.glob(pattern)]


def choose_newest_path(paths: list[Path]) -> Path | None:
    """Choose the newest path by modification time.

    Args:
        paths: Candidate paths to compare.

    Returns:
        Path with the most recent mtime, if any.
    """
    if not paths:
        return None
    return max(paths, key=lambda path: path.stat().st_mtime)


def find_vscode_codex() -> Path | None:
    """Find the newest codex binary from VS Code extensions."""
    candidates: list[Path] = []
    for base_dir in (Path.home() / ".vscode", Path.home() / ".vscode-insiders"):
        candidates.extend(list_vscode_codex_candidates(base_dir=base_dir))
    candidates = [
        path for path in candidates if path.is_file() and os.access(path, os.X_OK)
    ]
    return choose_newest_path(paths=candidates)


def resolve_codex_path(*, override: str | None) -> str:
    """Resolve the codex binary path.

    Args:
        override: Optional codex path override from CLI.

    Returns:
        Absolute path to the codex binary.
    """
    if override:
        path = Path(override).expanduser()
        assert path.exists(), f"codex path not found: {path}"
        return str(path)
    env_path = os.environ.get("CODEX_BIN")
    if env_path:
        path = Path(env_path).expanduser()
        assert path.exists(), f"CODEX_BIN not found: {path}"
        return str(path)
    resolved = shutil.which("codex")
    if resolved:
        return resolved
    vscode_codex = find_vscode_codex()
    if vscode_codex:
        return str(vscode_codex)
    for candidate in ("/opt/homebrew/bin/codex", "/usr/local/bin/codex"):
        if Path(candidate).exists():
            return candidate
    assert False, "codex not found in PATH; use --codex-path or set CODEX_BIN"


def run_codex_reflection(
    *,
    session_id: str,
    prompt: str,
    sandbox: str,
    approval: str,
    debug: bool,
    codex_path: str | None,
    timeout_seconds: int,
) -> None:
    """Run codex exec resume to generate a reflection.

    Args:
        session_id: Session id to resume.
        prompt: Prompt text to send.
        sandbox: Sandbox mode for codex.
        approval: Approval policy for codex.
        debug: Whether to emit debug output.
        codex_path: Optional path to the codex binary.
        timeout_seconds: Timeout for the codex call.

    Example:
        run_codex_reflection(
            session_id="uuid",
            prompt="Summarize.",
            sandbox="read-only",
            approval="never",
            debug=False,
            codex_path=None,
            timeout_seconds=120,
        )
    """
    codex_bin = resolve_codex_path(override=codex_path)
    command = [
        codex_bin,
        "--sandbox",
        sandbox,
        "--ask-for-approval",
        approval,
        "exec",
        "--skip-git-repo-check",
        "resume",
        session_id,
        "-",
    ]
    result = subprocess.run(
        args=command,
        input=prompt.strip() + "\n",
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    if debug:
        debug_print(enabled=True, message=result.stdout)
        debug_print(enabled=True, message=result.stderr)
    assert result.returncode == 0, result.stderr.strip()


def generate_reflection(
    *,
    session_meta: SessionMeta,
    prompt: str,
    prefix: str,
    sandbox: str,
    approval: str,
    debug: bool,
    codex_path: str | None,
    timeout_seconds: int,
) -> str:
    """Generate a reflection by branching a session and running codex.

    Args:
        session_meta: Session metadata to reflect on.
        prompt: Prompt text to send.
        prefix: Prefix for the duplicated session's user message.
        sandbox: Sandbox mode for codex.
        approval: Approval policy for codex.
        debug: Whether to emit debug output.
        codex_path: Optional path to the codex binary.
        timeout_seconds: Timeout for the codex call.

    Returns:
        Reflection paragraph text.

    Example:
        text = generate_reflection(
            session_meta=meta,
            prompt="Summarize this chat.",
            prefix="[SELF-REFLECTION] ",
            sandbox="read-only",
            approval="never",
            debug=False,
            codex_path=None,
            timeout_seconds=120,
        )
    """
    copy_path: Path | None = None
    try:
        copy_path = create_copy_with_new_id(
            source=session_meta.path,
            dest_dir=session_meta.path.parent,
            timestamp=None,
            session_id=None,
            prefix=prefix,
        )
        copy_id = extract_uuid_from_filename(path=copy_path)
        debug_print(
            enabled=debug,
            message=(
                f"Created reflection copy {copy_path.name} for {session_meta.label()}"
            ),
        )
        run_codex_reflection(
            session_id=copy_id,
            prompt=prompt,
            sandbox=sandbox,
            approval=approval,
            debug=debug,
            codex_path=codex_path,
            timeout_seconds=timeout_seconds,
        )
        lines = read_lines(path=copy_path)
        reflection = extract_last_assistant_text(lines=lines)
        return reflection
    finally:
        if copy_path is not None and copy_path.exists():
            copy_path.unlink()
            debug_print(
                enabled=debug,
                message=f"Removed reflection copy {copy_path.name}",
            )
