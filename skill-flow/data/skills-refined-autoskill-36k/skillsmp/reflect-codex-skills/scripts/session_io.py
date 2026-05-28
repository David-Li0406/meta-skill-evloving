"""Utilities for reading and copying Codex session JSONL files."""

from __future__ import annotations

import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REQUEST_TITLE_MARKER = "## my request for codex:"


def extract_uuid_from_filename(path: Path) -> str:
    """Extract the UUID suffix from a rollout JSONL filename.

    Args:
        path: Path to the rollout JSONL file.

    Returns:
        UUID portion of the filename.

    Example:
        uuid_value = extract_uuid_from_filename(
            path=Path("rollout-2026-01-12T00-00-00-uuid.jsonl")
        )
    """
    parts = path.stem.split("-")
    assert len(parts) >= 6, "Unexpected filename format"
    return "-".join(parts[-5:])


def format_timestamp(timestamp: datetime) -> str:
    """Format a UTC timestamp for rollout filenames.

    Args:
        timestamp: A timezone-aware datetime.

    Returns:
        Timestamp string in filename format.

    Example:
        stamp = format_timestamp(
            timestamp=datetime(2026, 1, 12, 0, 0, 0, tzinfo=timezone.utc)
        )
    """
    assert timestamp.tzinfo is not None, "Timestamp must be timezone-aware"
    return timestamp.strftime("%Y-%m-%dT%H-%M-%S")


def build_rollout_filename(timestamp: str, session_id: str) -> str:
    """Build a rollout filename from a timestamp and session id.

    Args:
        timestamp: Timestamp string for the filename.
        session_id: UUID to embed in the filename.

    Returns:
        Rollout filename including timestamp and UUID.

    Example:
        name = build_rollout_filename(timestamp="2026-01-12T00-00-00", session_id="uuid")
    """
    return f"rollout-{timestamp}-{session_id}.jsonl"


def generate_destination_path(*, dest_dir: Path, timestamp: str, session_id: str) -> Path:
    """Generate the destination path for a copied session file.

    Args:
        dest_dir: Directory to place the copied file.
        timestamp: Timestamp string for the filename.
        session_id: UUID to embed in the filename.

    Returns:
        Full path to the destination file.

    Example:
        dest = generate_destination_path(
            dest_dir=Path("/tmp"),
            timestamp="2026-01-12T00-00-00",
            session_id="uuid",
        )
    """
    filename = build_rollout_filename(timestamp=timestamp, session_id=session_id)
    return dest_dir / filename


def read_lines(path: Path) -> list[str]:
    """Read a text file into a list of lines.

    Args:
        path: File to read.

    Returns:
        List of lines without trailing newline characters.
    """
    return path.read_text().splitlines()


def write_lines(path: Path, lines: list[str]) -> None:
    """Write lines to a file with a trailing newline.

    Args:
        path: File to write.
        lines: Lines to write.
    """
    path.write_text("\n".join(lines) + "\n")


def discover_session_files(*, root: Path) -> list[Path]:
    """Discover rollout JSONL files under the sessions root.

    Args:
        root: Root directory to search.

    Returns:
        Sorted list of rollout JSONL paths.
    """
    assert root.exists(), f"Sessions root not found: {root}"
    paths = [path for path in root.rglob("rollout-*.jsonl") if "-copy" not in path.name]
    return sorted(paths)


def update_session_id(lines: list[str], new_id: str) -> list[str]:
    """Update the session_meta payload id in the first JSONL line.

    Args:
        lines: JSONL file split into lines.
        new_id: Session id to store in session_meta payload.

    Returns:
        Updated list of lines.

    Example:
        updated = update_session_id(lines=lines, new_id="uuid")
    """
    assert lines, "File is empty"
    first = json.loads(lines[0])
    assert first.get("type") == "session_meta", "First line is not session_meta"
    payload = first.get("payload")
    assert isinstance(payload, dict), "session_meta payload is not a dict"
    payload["id"] = new_id
    lines[0] = json.dumps(first, separators=(",", ":"))
    return lines


def sync_session_file(*, path: Path, session_id: str) -> None:
    """Sync the session_meta id in a JSONL file.

    Args:
        path: File to update.
        session_id: Session id to write.

    Example:
        sync_session_file(path=Path("rollout-...jsonl"), session_id="uuid")
    """
    lines = read_lines(path=path)
    updated = update_session_id(lines=lines, new_id=session_id)
    write_lines(path=path, lines=updated)


def copy_session(*, source: Path, dest: Path) -> None:
    """Copy a session file, preserving metadata.

    Args:
        source: Source JSONL file.
        dest: Destination path for the copy.

    Example:
        copy_session(source=Path("a.jsonl"), dest=Path("b.jsonl"))
    """
    assert not dest.exists(), f"Destination already exists: {dest}"
    shutil.copy2(src=source, dst=dest)


def _find_request_title_index(*, lines: list[str]) -> int | None:
    """Find the index of the request title line.

    Args:
        lines: User message split into lines.

    Returns:
        Index of the request title line, or None if missing.
    """
    for index, line in enumerate(lines):
        if line.strip().lower() != _REQUEST_TITLE_MARKER:
            continue
        for next_index in range(index + 1, len(lines)):
            if lines[next_index].strip():
                return next_index
        return None
    return None


def _normalize_user_text(*, text: str, prefix: str) -> str:
    """Normalize user text for matching.

    Args:
        text: Raw user text.
        prefix: Prefix string to remove when present.

    Returns:
        Normalized text without the prefix.
    """
    normalized = text
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix) :]
    lines = normalized.splitlines()
    title_index = _find_request_title_index(lines=lines)
    if title_index is None:
        return normalized
    title_line = lines[title_index]
    if not title_line.startswith(prefix):
        return normalized
    lines[title_index] = title_line[len(prefix) :]
    return "\n".join(lines)


def _prefix_request_title(*, text: str, prefix: str) -> tuple[str, bool]:
    """Prefix the request title line when present.

    Args:
        text: Raw user text.
        prefix: Prefix string to add.

    Returns:
        Tuple of (updated_text, changed).

    Example:
        updated, changed = _prefix_request_title(text=message, prefix="[SELF-REFLECTION] ")
    """
    lines = text.splitlines()
    title_index = _find_request_title_index(lines=lines)
    if title_index is None:
        if text.startswith(prefix):
            return text, False
        return f"{prefix}{text}", True
    title_line = lines[title_index]
    if title_line.startswith(prefix):
        return text, False
    lines[title_index] = f"{prefix}{title_line}"
    return "\n".join(lines), True


def _has_prefixed_request_title(*, text: str, prefix: str) -> bool:
    """Check whether a user message has a prefixed request title.

    Args:
        text: Raw user text.
        prefix: Prefix string to detect.

    Returns:
        True if the request title or message start is prefixed.
    """
    if text.startswith(prefix):
        return True
    lines = text.splitlines()
    title_index = _find_request_title_index(lines=lines)
    if title_index is None:
        return False
    return lines[title_index].startswith(prefix)


def _first_event_user_text(*, lines: list[str]) -> str | None:
    """Return the first event_msg user text found.

    Args:
        lines: JSONL file split into lines.

    Returns:
        User message text, if found.
    """
    for line in lines:
        data = json.loads(line)
        if data.get("type") != "event_msg":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict) or payload.get("type") != "user_message":
            continue
        message = payload.get("message")
        if isinstance(message, str):
            return message
    return None


def _first_response_user_text(*, lines: list[str]) -> str | None:
    """Return the first response_item user text found.

    Args:
        lines: JSONL file split into lines.

    Returns:
        User message text, if found.
    """
    for line in lines:
        data = json.loads(line)
        if data.get("type") != "response_item":
            continue
        payload = data.get("payload")
        if (
            not isinstance(payload, dict)
            or payload.get("type") != "message"
            or payload.get("role") != "user"
        ):
            continue
        content = payload.get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if not isinstance(item, dict) or item.get("type") != "input_text":
                continue
            text = item.get("text")
            if isinstance(text, str):
                return text
    return None


def _update_event_message(
    *, payload: dict[str, Any], prefix: str, target: str
) -> tuple[bool, bool]:
    """Update an event_msg payload if it matches the target text.

    Args:
        payload: event_msg payload dictionary.
        prefix: String to prepend to the message.
        target: Normalized target text to match.

    Returns:
        Tuple of (matched, changed).
    """
    if payload.get("type") != "user_message":
        return False, False
    message = payload.get("message")
    if not isinstance(message, str):
        return False, False
    if _normalize_user_text(text=message, prefix=prefix) != target:
        return False, False
    updated_message, changed = _prefix_request_title(text=message, prefix=prefix)
    if not changed:
        return True, False
    payload["message"] = updated_message
    return True, True


def _update_response_item(
    *, payload: dict[str, Any], prefix: str, target: str
) -> tuple[bool, bool, bool]:
    """Update a response_item payload if it matches the target text.

    Args:
        payload: response_item payload dictionary.
        prefix: String to prepend to the input text.
        target: Normalized target text to match.

    Returns:
        Tuple of (matched, changed, found_user).
    """
    if payload.get("type") != "message" or payload.get("role") != "user":
        return False, False, False
    content = payload.get("content")
    if not isinstance(content, list):
        return False, False, False
    found_user = False
    for item in content:
        if not isinstance(item, dict) or item.get("type") != "input_text":
            continue
        text = item.get("text")
        if not isinstance(text, str):
            continue
        found_user = True
        if _normalize_user_text(text=text, prefix=prefix) != target:
            continue
        updated_text, changed = _prefix_request_title(text=text, prefix=prefix)
        if not changed:
            return True, False, True
        item["text"] = updated_text
        return True, True, True
    return False, False, found_user


def _prefix_line(
    *, line: str, prefix: str, target: str
) -> tuple[str, bool, bool, bool]:
    """Prefix a JSONL line when it matches the target user text.

    Args:
        line: JSONL line string.
        prefix: Prefix string to apply.
        target: Normalized target text to match.

    Returns:
        Tuple of (line, updated_event, updated_response, found_response).
    """
    data = json.loads(line)
    changed = False
    updated_event = False
    updated_response = False
    found_response = False
    if data.get("type") == "event_msg":
        payload = data.get("payload")
        if isinstance(payload, dict):
            matched, updated = _update_event_message(
                payload=payload,
                prefix=prefix,
                target=target,
            )
            updated_event = matched
            changed = changed or updated
    if data.get("type") == "response_item":
        payload = data.get("payload")
        if isinstance(payload, dict):
            matched, updated, found = _update_response_item(
                payload=payload,
                prefix=prefix,
                target=target,
            )
            updated_response = matched
            found_response = found
            changed = changed or updated
    if changed:
        line = json.dumps(data, separators=(",", ":"))
    return line, updated_event, updated_response, found_response


def is_reflection_copy(*, lines: list[str], prefix: str) -> bool:
    """Check whether a session appears to be a reflection copy.

    Args:
        lines: JSONL file split into lines.
        prefix: Prefix used to mark reflection copies.

    Returns:
        True if any user message has the prefix at the request title or start.

    Example:
        is_copy = is_reflection_copy(lines=lines, prefix="[SELF-REFLECTION] ")
    """
    for line in lines:
        data = json.loads(line)
        if data.get("type") == "event_msg":
            payload = data.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "user_message":
                message = payload.get("message")
                if isinstance(message, str) and _has_prefixed_request_title(
                    text=message, prefix=prefix
                ):
                    return True
        if data.get("type") == "response_item":
            payload = data.get("payload")
            if (
                isinstance(payload, dict)
                and payload.get("type") == "message"
                and payload.get("role") == "user"
            ):
                content = payload.get("content")
                if isinstance(content, list):
                    for item in content:
                        if not isinstance(item, dict):
                            continue
                        if item.get("type") != "input_text":
                            continue
                        text = item.get("text")
                        if isinstance(text, str) and _has_prefixed_request_title(
                            text=text, prefix=prefix
                        ):
                            return True
    return False


def prefix_first_user_message(lines: list[str], prefix: str) -> list[str]:
    """Prefix the request title line in the first user message entries.

    Args:
        lines: JSONL file split into lines.
        prefix: String to prepend to the request title line.

    Returns:
        Updated list of lines.

    Example:
        updated = prefix_first_user_message(lines=lines, prefix="[SELF-REFLECTION] ")
    """
    target = _first_event_user_text(lines=lines)
    target_source = "event_msg" if target else "response_item"
    if target is None:
        target = _first_response_user_text(lines=lines)
    assert target, "No user message found to prefix"
    target_norm = _normalize_user_text(text=target, prefix=prefix)
    updated_event = False
    updated_response = False
    found_response = False
    updated_lines: list[str] = []
    for line in lines:
        line, event_hit, response_hit, response_found = _prefix_line(
            line=line,
            prefix=prefix,
            target=target_norm,
        )
        updated_event = updated_event or event_hit
        updated_response = updated_response or response_hit
        found_response = found_response or response_found
        updated_lines.append(line)
    if target_source == "event_msg":
        assert updated_event, "No matching event_msg user_message found to prefix"
    if found_response:
        assert (
            updated_response
        ), "No matching response_item user message found to prefix"
    return updated_lines


def create_copy_with_new_id(
    *,
    source: Path,
    dest_dir: Path,
    timestamp: str | None,
    session_id: str | None,
    prefix: str | None,
) -> Path:
    """Create a new copy with a fresh id and synced session_meta.

    Args:
        source: Source session JSONL file.
        dest_dir: Destination directory for the copy.
        timestamp: Optional timestamp override for the filename.
        session_id: Optional UUID override for the filename.
        prefix: Optional prefix for the first user message entries.

    Returns:
        Path to the newly created session file.

    Example:
        new_path = create_copy_with_new_id(
            source=Path("rollout-...jsonl"),
            dest_dir=Path("."),
            timestamp=None,
            session_id=None,
            prefix=None,
        )
    """
    resolved_timestamp = timestamp or format_timestamp(
        timestamp=datetime.now(timezone.utc)
    )
    resolved_id = session_id or str(uuid.uuid4())
    dest = generate_destination_path(
        dest_dir=dest_dir,
        timestamp=resolved_timestamp,
        session_id=resolved_id,
    )
    copy_session(source=source, dest=dest)
    lines = read_lines(path=dest)
    lines = update_session_id(lines=lines, new_id=resolved_id)
    if prefix:
        lines = prefix_first_user_message(lines=lines, prefix=prefix)
    write_lines(path=dest, lines=lines)
    return dest
