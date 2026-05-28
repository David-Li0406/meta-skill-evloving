"""Session parsing and filtering helpers for reflect_sessions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .debug import debug_print
from .models import ConversationInfo, SessionMeta
from .time import format_iso_utc, parse_timestamp
from session_io import is_reflection_copy, read_lines


def session_last_updated_at(*, path: Path) -> datetime:
    """Return the latest timestamp seen in a session JSONL file.

    Args:
        path: Path to the session JSONL file.

    Returns:
        Latest timestamp found in the session history.
    """
    latest: datetime | None = None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            timestamp = data.get("timestamp")
            if not isinstance(timestamp, str):
                continue
            parsed = parse_timestamp(value=timestamp)
            if latest is None or parsed > latest:
                latest = parsed
    assert latest, f"No timestamps found in {path}"
    return latest


def _event_user_message(*, data: dict[str, Any]) -> str | None:
    """Extract user message text from an event_msg payload.

    Args:
        data: Parsed JSONL line dictionary.

    Returns:
        User message text, if present.
    """
    if data.get("type") != "event_msg":
        return None
    payload = data.get("payload")
    if not isinstance(payload, dict) or payload.get("type") != "user_message":
        return None
    message = payload.get("message")
    return message if isinstance(message, str) else None


def _response_user_message(*, data: dict[str, Any]) -> str | None:
    """Extract user input text from a response_item payload.

    Args:
        data: Parsed JSONL line dictionary.

    Returns:
        User input text, if present.
    """
    if data.get("type") != "response_item":
        return None
    payload = data.get("payload")
    if (
        not isinstance(payload, dict)
        or payload.get("type") != "message"
        or payload.get("role") != "user"
    ):
        return None
    content = payload.get("content")
    if not isinstance(content, list):
        return None
    for item in content:
        if not isinstance(item, dict) or item.get("type") != "input_text":
            continue
        text = item.get("text")
        if isinstance(text, str):
            return text
    return None


def extract_first_user_text(*, path: Path) -> str:
    """Extract the first user message text from a session file.

    Args:
        path: Path to the session JSONL file.

    Returns:
        First user message text (event_msg preferred), or an empty string.
    """
    first_response: str | None = None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_text = _event_user_message(data=data)
            if event_text:
                return event_text
            response_text = _response_user_message(data=data)
            if response_text and first_response is None:
                first_response = response_text
    return first_response or ""


def extract_request_title(*, text: str, prefix: str | None = None) -> str:
    """Extract the first request line from IDE context blocks.

    Args:
        text: User message text to search.
        prefix: Optional prefix to strip from the request line.

    Returns:
        First non-empty line after the request header, or empty string.
    """
    lines = [line.strip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        if line.lower() == "## my request for codex:":
            for next_line in lines[index + 1 :]:
                if next_line:
                    line = next_line
                    if prefix:
                        line = strip_prefix(text=line, prefix=prefix).strip()
                    return line
            return ""
    return ""


def truncate_text(*, text: str, limit: int) -> str:
    """Truncate text to a character limit.

    Args:
        text: Text to truncate.
        limit: Maximum length.

    Returns:
        Truncated text.
    """
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "…"


def strip_prefix(*, text: str, prefix: str) -> str:
    """Remove the prefix from the text when present.

    Args:
        text: Text to normalize.
        prefix: Prefix to remove.

    Returns:
        Text without the prefix.
    """
    return text[len(prefix) :] if text.startswith(prefix) else text


def build_conversation_info(*, meta: SessionMeta, prefix: str) -> ConversationInfo:
    """Build conversation metadata for output.

    Args:
        meta: Session metadata for the conversation.
        prefix: Prefix used to mark reflection copies.

    Returns:
        ConversationInfo with title and last-updated timestamp.
    """
    updated_at = session_last_updated_at(path=meta.path)
    updated_at_iso = format_iso_utc(timestamp=updated_at)
    raw_title = extract_first_user_text(path=meta.path)
    raw_title = strip_prefix(text=raw_title, prefix=prefix).strip()
    request_title = extract_request_title(text=raw_title, prefix=prefix)
    title_source = request_title or raw_title
    normalized_title = " ".join(title_source.split())
    title = truncate_text(
        text=normalized_title or "Untitled conversation",
        limit=80,
    )
    return ConversationInfo(
        updated_at=updated_at,
        updated_at_iso=updated_at_iso,
        title=title,
    )


def extract_session_payload(*, data: dict[str, Any], path: Path) -> dict[str, Any]:
    """Extract session metadata payload from new or legacy formats.

    Args:
        data: Parsed JSON line.
        path: Path to the session JSONL file.

    Returns:
        Session metadata payload dictionary.

    Example:
        payload = extract_session_payload(data=data, path=Path("rollout-...jsonl"))
    """
    if data.get("type") == "session_meta":
        payload = data.get("payload")
        assert isinstance(payload, dict), "session_meta payload is not a dict"
        return payload
    if "id" in data and "timestamp" in data:
        return data
    assert False, f"Unrecognized session meta format: {path}"


def load_session_meta(*, path: Path) -> SessionMeta:
    """Load session metadata from a JSONL file.

    Args:
        path: Path to the session JSONL file.

    Returns:
        SessionMeta populated from the session_meta line.

    Example:
        meta = load_session_meta(path=Path("rollout-...jsonl"))
    """
    with path.open("r", encoding="utf-8") as handle:
        first_line = handle.readline().strip()
    data = json.loads(first_line)
    assert isinstance(data, dict), "First line is not a JSON object"
    payload = extract_session_payload(data=data, path=path)
    session_id = payload.get("id")
    timestamp = payload.get("timestamp")
    cwd_value = payload.get("cwd")
    assert isinstance(session_id, str), "session_meta id missing"
    assert isinstance(timestamp, str), "session_meta timestamp missing"
    cwd = Path(cwd_value) if isinstance(cwd_value, str) else None
    return SessionMeta(
        session_id=session_id,
        timestamp=parse_timestamp(value=timestamp),
        cwd=cwd,
        path=path,
    )


def load_sessions(*, paths: list[Path], prefix: str, debug: bool) -> list[SessionMeta]:
    """Load session metadata for candidate JSONL files.

    Args:
        paths: List of session JSONL paths.
        prefix: Prefix used to mark reflection copies.
        debug: Whether to emit debug output.

    Returns:
        List of SessionMeta objects.
    """
    sessions: list[SessionMeta] = []
    for path in paths:
        lines = read_lines(path=path)
        if is_reflection_copy(lines=lines, prefix=prefix):
            debug_print(enabled=debug, message=f"Skipping reflection copy: {path}")
            continue
        sessions.append(load_session_meta(path=path))
    return sessions


def filter_sessions(
    *,
    sessions: list[SessionMeta],
    session_ids: list[str] | None,
    project: str | None,
    since: datetime | None,
    until: datetime | None,
    limit: int | None,
) -> list[SessionMeta]:
    """Filter sessions by id, project, and time range.

    Args:
        sessions: Candidate sessions.
        session_ids: Optional list of session ids to include.
        project: Optional project label filter.
        since: Optional start datetime (inclusive).
        until: Optional end datetime (inclusive).
        limit: Optional limit to most recent sessions.

    Returns:
        Filtered list of SessionMeta objects.
    """
    allowed_ids = set(session_ids or [])
    filtered = []
    for session in sessions:
        if allowed_ids and session.session_id not in allowed_ids:
            continue
        if project and session.project_name() != project:
            continue
        if since and session.timestamp < since:
            continue
        if until and session.timestamp > until:
            continue
        filtered.append(session)
    filtered.sort(key=lambda item: item.timestamp)
    if limit:
        return filtered[-limit:]
    return filtered


def project_counts(*, sessions: list[SessionMeta]) -> list[dict[str, Any]]:
    """Count sessions per project.

    Args:
        sessions: Sessions to summarize.

    Returns:
        Sorted list of project count dicts.
    """
    counts: dict[str, int] = {}
    for session in sessions:
        name = session.project_name()
        counts[name] = counts.get(name, 0) + 1
    return [
        {"project": name, "count": counts[name]}
        for name in sorted(counts.keys())
    ]
