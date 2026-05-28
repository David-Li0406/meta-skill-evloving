"""Output rendering for reflect_sessions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import CACHE_SCHEMA_VERSION
from .models import ProjectGroup, ReflectionRecord
from .time import now_iso


def build_projects_payload(
    *, counts: list[dict[str, Any]], current: str | None
) -> dict[str, Any]:
    """Build JSON payload for project listing.

    Args:
        counts: Project count dictionaries.
        current: Current project name to highlight.

    Returns:
        JSON payload for project listing.
    """
    return {
        "current_project": current,
        "projects": counts,
    }


def render_projects_human(*, payload: dict[str, Any]) -> str:
    """Render project listing in a human-readable format.

    Args:
        payload: Project listing payload.

    Returns:
        Rendered string for human consumption.
    """
    current = payload.get("current_project")
    projects = payload.get("projects", [])
    lines = ["projects:"]
    for item in projects:
        name = item.get("project")
        count = item.get("count")
        marker = " *" if current and name == current else ""
        lines.append(f"{name}\t{count}{marker}")
    return "\n".join(lines)


def group_by_project(*, records: list[ReflectionRecord]) -> list[ProjectGroup]:
    """Group reflection records by project.

    Args:
        records: Reflection records to group.

    Returns:
        Sorted list of ProjectGroup entries.
    """
    grouped: dict[str, list[ReflectionRecord]] = {}
    for record in records:
        grouped.setdefault(record.meta.project_name(), []).append(record)
    for items in grouped.values():
        items.sort(key=lambda item: item.meta.timestamp)
    return [ProjectGroup(project=key, sessions=grouped[key]) for key in sorted(grouped)]


def build_output_payload(
    *,
    records: list[ReflectionRecord],
    sessions_root: Path,
    cache_dir: Path,
    prompt_label: str,
    prompt_version: str,
    prompt_updated_at: str,
    extra_metadata: bool,
) -> dict[str, Any]:
    """Build the JSON output payload.

    Args:
        records: Reflection records.
        sessions_root: Root directory containing session histories.
        cache_dir: Directory containing cache entries.
        prompt_label: Label describing the prompt used for this run.
        prompt_version: Prompt version string.
        prompt_updated_at: Prompt updated timestamp.
        extra_metadata: Whether to include system metadata fields.

    Returns:
        JSON-serializable output payload.
    """
    groups = group_by_project(records=records)
    payload: dict[str, Any] = {
        "projects": [
            {
                "project": group.project,
                "sessions": [
                    {
                        "conversation_started_at": record.meta.iso_timestamp(),
                        "conversation_updated_at": record.conversation_updated_at,
                        "reflection_created_at": record.reflection_created_at,
                        "reflection": record.reflection,
                    }
                    for record in group.sessions
                ],
            }
            for group in groups
        ]
    }
    if extra_metadata:
        payload.update(
            {
                "generated_at": now_iso(),
                "sessions_root": str(sessions_root),
                "prompt_version": prompt_version,
                "cache": {
                    "schema_version": CACHE_SCHEMA_VERSION,
                    "dir": str(cache_dir),
                    "prompt_path": prompt_label,
                    "prompt_version": prompt_version,
                    "prompt_updated_at": prompt_updated_at,
                },
            }
        )
        for group, payload_group in zip(groups, payload["projects"]):
            for record, payload_record in zip(group.sessions, payload_group["sessions"]):
                payload_record.update(
                    {
                        "session_id": record.meta.session_id,
                        "project": record.meta.project_name(),
                        "source_path": str(record.meta.path),
                        "cached": record.cached,
                        "cache_path": str(record.cache_path),
                        "cache_schema_version": record.cache_schema_version,
                        "cache_prompt_version": record.cache_prompt_version,
                        "cache_prompt_updated_at": record.cache_prompt_updated_at,
                        "cache_status": record.cache_status,
                        "cache_status_reason": record.cache_status_reason,
                        "conversation_title": record.conversation_title,
                    }
                )
    return payload


def build_human_payload(
    *,
    records: list[ReflectionRecord],
    sessions_root: Path,
    cache_dir: Path,
    prompt_label: str,
    prompt_version: str,
    prompt_updated_at: str,
    extra_metadata: bool,
) -> dict[str, Any]:
    """Build payload for human-readable output.

    Args:
        records: Reflection records.
        sessions_root: Root directory containing session histories.
        cache_dir: Directory containing cache entries.
        prompt_label: Label describing the prompt used for this run.
        prompt_version: Prompt version string.
        prompt_updated_at: Prompt updated timestamp.
        extra_metadata: Whether to include metadata header fields.

    Returns:
        Payload for human-readable rendering.
    """
    groups = group_by_project(records=records)
    payload: dict[str, Any] = {
        "projects": [
            {
                "project": group.project,
                "sessions": [
                    {
                        "conversation_title": record.conversation_title,
                        "conversation_updated_at": record.conversation_updated_at,
                        "reflection_created_at": record.reflection_created_at,
                        "cache_status": record.cache_status,
                        "cache_status_reason": record.cache_status_reason,
                        "reflection": record.reflection,
                    }
                    for record in group.sessions
                ],
            }
            for group in groups
        ]
    }
    if extra_metadata:
        payload.update(
            {
                "generated_at": now_iso(),
                "sessions_root": str(sessions_root),
                "prompt_version": prompt_version,
                "cache": {
                    "schema_version": CACHE_SCHEMA_VERSION,
                    "dir": str(cache_dir),
                    "prompt_path": prompt_label,
                    "prompt_version": prompt_version,
                    "prompt_updated_at": prompt_updated_at,
                },
            }
        )
    return payload


def render_cache_lines(*, cache: dict[str, Any]) -> list[str]:
    """Render cache metadata lines for human-readable output.

    Args:
        cache: Cache metadata dictionary.

    Returns:
        List of rendered lines.
    """
    return [
        "cache:",
        f"  schema_version: {cache.get('schema_version')}",
        f"  dir: {cache.get('dir')}",
        f"  prompt_path: {cache.get('prompt_path')}",
        f"  prompt_version: {cache.get('prompt_version')}",
        f"  prompt_updated_at: {cache.get('prompt_updated_at')}",
    ]


def render_session_lines(*, session: dict[str, Any]) -> list[str]:
    """Render a session block for human-readable output.

    Args:
        session: Session dictionary.

    Returns:
        List of rendered lines.
    """
    title = session.get("conversation_title") or "Untitled conversation"
    updated = session.get("conversation_updated_at")
    reflected = session.get("reflection_created_at")
    cache_status = session.get("cache_status")
    cache_reason = session.get("cache_status_reason")
    lines = [
        f"  title: {title}",
        f"  last_updated: {updated}",
        f"  reflected_at: {reflected}",
        f"  cache_status: {cache_status}",
        f"  cache_status_reason: {cache_reason}",
        "  reflection:",
    ]
    reflection = session.get("reflection", "")
    lines.extend([f"    {line}" for line in str(reflection).splitlines()])
    lines.append("")
    return lines


def render_project_lines(*, project: dict[str, Any]) -> list[str]:
    """Render a project block for human-readable output.

    Args:
        project: Project dictionary.

    Returns:
        List of rendered lines.
    """
    sessions = project.get("sessions", [])
    lines = [f"project: {project.get('project')} ({len(sessions)})"]
    for session in sessions:
        lines.extend(render_session_lines(session=session))
    return lines


def render_human_output(*, payload: dict[str, Any], show_metadata: bool) -> str:
    """Render the full output in a human-readable format.

    Args:
        payload: Output payload to render.
        show_metadata: Whether to include cache metadata details.

    Returns:
        Rendered string.
    """
    lines: list[str] = []
    if show_metadata:
        lines.extend(
            [
                f"generated_at: {payload.get('generated_at')}",
                f"sessions_root: {payload.get('sessions_root')}",
                f"prompt_version: {payload.get('prompt_version')}",
            ]
        )
        lines.extend(render_cache_lines(cache=payload.get("cache", {})))
        lines.append("")
    for project in payload.get("projects", []):
        lines.extend(render_project_lines(project=project))
    return "\n".join(lines).rstrip()


def write_output(*, payload: dict[str, Any], output: str, output_style: str) -> None:
    """Write the output payload.

    Args:
        payload: Output payload to write.
        output: Output path or '-' for stdout.
        output_style: Output style (human, json, json_extra_metadata).
    """
    if output_style == "human":
        rendered = render_human_output(payload=payload, show_metadata=False)
    else:
        rendered = json.dumps(payload, indent=2, ensure_ascii=True)
    if output == "-":
        print(rendered)
        return
    Path(output).write_text(rendered + "\n")
