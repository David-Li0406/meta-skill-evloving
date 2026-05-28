"""Generate Codex session reflections and cache them for reuse.

Example:
    python3 reflect_sessions.py --limit 5 --output reflections.json
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from reflect_sessions.cache import ensure_cache_dir, reflect_session
from reflect_sessions.cli import parse_args
from reflect_sessions.config import DEFAULT_MAX_REFLECTIONS, DEFAULT_MAX_WORKERS
from reflect_sessions.debug import debug_print
from reflect_sessions.models import ReflectionRecord, SessionMeta
from reflect_sessions.output import (
    build_human_payload,
    build_output_payload,
    build_projects_payload,
    render_projects_human,
    write_output,
)
from reflect_sessions.prompt import (
    compute_prompt_hash,
    ensure_prompt_version_state,
    is_default_prompt_path,
    prompt_cache_key,
    resolve_prompt_selection,
)
from reflect_sessions.sessions import filter_sessions, load_sessions, project_counts
from reflect_sessions.time import parse_datetime_arg
from session_io import discover_session_files


def resolve_session_ids(*, args: argparse.Namespace) -> list[str]:
    """Collect session ids from CLI arguments.

    Args:
        args: Parsed CLI arguments.

    Returns:
        List of session ids parsed from the CLI.

    Example:
        session_ids = resolve_session_ids(args=args)
    """
    session_ids: list[str] = []
    if args.session_id:
        session_ids.extend(args.session_id)
    if args.session_ids:
        session_ids.extend(
            [item.strip() for item in args.session_ids.split(",") if item.strip()]
        )
    return session_ids


def select_sessions(
    *,
    sessions: list[SessionMeta],
    session_ids: list[str],
    project: str | None,
    since: datetime | None,
    until: datetime | None,
    limit: int | None,
    include_most_recent: bool,
) -> list[SessionMeta]:
    """Select sessions after applying filters and defaults.

    Args:
        sessions: Candidate sessions.
        session_ids: Explicit session ids to include (if any).
        project: Optional project filter.
        since: Optional start datetime filter.
        until: Optional end datetime filter.
        limit: Optional limit to the most recent N sessions.
        include_most_recent: Whether to keep the most recent session.

    Returns:
        Filtered list of sessions to reflect.
    """
    explicit_ids = bool(session_ids)
    selected = filter_sessions(
        sessions=sessions,
        session_ids=session_ids or None,
        project=None if explicit_ids else project,
        since=None if explicit_ids else since,
        until=None if explicit_ids else until,
        limit=None,
    )
    if selected and not include_most_recent:
        newest = max(session.timestamp for session in selected)
        selected = [item for item in selected if item.timestamp != newest]
    if limit and not explicit_ids:
        selected = selected[-limit:]
    return selected


def render_projects_listing(*, sessions: list[SessionMeta], output_style: str) -> None:
    """Render and print the project listing output.

    Args:
        sessions: Filtered sessions for listing.
        output_style: Output style to use.
    """
    counts = project_counts(sessions=sessions)
    current_project = Path.cwd().name
    payload = build_projects_payload(counts=counts, current=current_project)
    if output_style == "human":
        rendered = render_projects_human(payload=payload)
    else:
        rendered = json.dumps(payload, indent=2, ensure_ascii=True)
    print(rendered)


def build_records(
    *,
    selected: list[SessionMeta],
    cache_dir: Path,
    prompt: str,
    prompt_hash: str,
    prompt_version: str,
    prompt_updated_at: str,
    prefix: str,
    refresh_mode: str,
    prompt_cache_key: str,
    allow_legacy_cache: bool,
    sandbox: str,
    approval: str,
    debug: bool,
    codex_path: str | None,
    timeout_seconds: int,
    sequential: bool,
) -> list[ReflectionRecord]:
    """Generate reflection records for selected sessions.

    Args:
        selected: Sessions to reflect.
        cache_dir: Directory for cached reflections.
        prompt: Prompt text to use.
        prompt_hash: SHA-256 hash for the prompt.
        prompt_version: Prompt version string.
        prompt_updated_at: Prompt updated timestamp.
        prefix: Prefix for duplicated session user message.
        refresh_mode: Cache refresh mode.
        prompt_cache_key: Stable cache key for the prompt selection.
        allow_legacy_cache: Whether to reuse legacy cache entries.
        sandbox: Sandbox mode for codex.
        approval: Approval policy for codex.
        debug: Whether to emit debug output.
        codex_path: Optional path to the codex binary.
        timeout_seconds: Timeout for the codex call.
        sequential: Whether to force sequential execution.

    Returns:
        List of reflection records.
    """
    if sequential or len(selected) <= 1:
        return [
            reflect_session(
                meta=meta,
                cache_dir=cache_dir,
                prompt=prompt,
                prompt_hash=prompt_hash,
                prompt_version=prompt_version,
                prompt_updated_at=prompt_updated_at,
                prefix=prefix,
                refresh_mode=refresh_mode,
                prompt_cache_key=prompt_cache_key,
                allow_legacy_cache=allow_legacy_cache,
                sandbox=sandbox,
                approval=approval,
                debug=debug,
                codex_path=codex_path,
                timeout_seconds=timeout_seconds,
            )
            for meta in selected
        ]

    max_workers = min(DEFAULT_MAX_WORKERS, len(selected))
    records: list[ReflectionRecord | None] = [None] * len(selected)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(
                reflect_session,
                meta=meta,
                cache_dir=cache_dir,
                prompt=prompt,
                prompt_hash=prompt_hash,
                prompt_version=prompt_version,
                prompt_updated_at=prompt_updated_at,
                prefix=prefix,
                refresh_mode=refresh_mode,
                prompt_cache_key=prompt_cache_key,
                allow_legacy_cache=allow_legacy_cache,
                sandbox=sandbox,
                approval=approval,
                debug=debug,
                codex_path=codex_path,
                timeout_seconds=timeout_seconds,
            ): index
            for index, meta in enumerate(selected)
        }
        for future in as_completed(future_map):
            index = future_map[future]
            records[index] = future.result()
    return [record for record in records if record is not None]


def main() -> None:
    """Run the reflection CLI."""
    args = parse_args()
    sessions_root = args.sessions_root.expanduser()
    cache_dir = ensure_cache_dir(sessions_root=sessions_root, cache_dir=args.cache_dir)
    prompt_selection = resolve_prompt_selection(
        prompt_file=args.prompt_file,
        prompt_preset=args.prompt_preset,
        prompt_text=args.prompt_text,
    )
    prompt_hash = compute_prompt_hash(prompt_text=prompt_selection.prompt_text)
    prompt_state_path = prompt_selection.version_state_path(
        prompt_hash=prompt_hash,
        cache_dir=cache_dir,
    )
    prompt_state = ensure_prompt_version_state(
        state_path=prompt_state_path,
        prompt_hash=prompt_hash,
        now=datetime.now(timezone.utc),
    )
    prompt_label = prompt_selection.label(prompt_hash=prompt_hash)
    prompt = prompt_selection.prompt_text
    cache_key = prompt_cache_key(prompt_label=prompt_label)
    allow_legacy_cache = is_default_prompt_path(prompt_path=prompt_selection.prompt_path)
    output_style = args.output_style
    extra_metadata = output_style == "json_extra_metadata"
    since = parse_datetime_arg(value=args.since) if args.since else None
    until = parse_datetime_arg(value=args.until) if args.until else None

    paths = discover_session_files(root=sessions_root)
    sessions = load_sessions(paths=paths, prefix=args.prefix, debug=args.debug)
    session_ids = resolve_session_ids(args=args)

    explicit_ids = bool(session_ids)
    applied_limit = args.limit if not explicit_ids else None
    if applied_limit is None and not explicit_ids:
        applied_limit = DEFAULT_MAX_REFLECTIONS

    selected = select_sessions(
        sessions=sessions,
        session_ids=session_ids,
        project=None if explicit_ids else args.project,
        since=None if explicit_ids else since,
        until=None if explicit_ids else until,
        limit=applied_limit,
        include_most_recent=args.include_most_recent,
    )
    debug_print(enabled=args.debug, message=f"Selected {len(selected)} sessions")

    if args.list_projects:
        render_projects_listing(sessions=selected, output_style=output_style)
        return

    records = build_records(
        selected=selected,
        cache_dir=cache_dir,
        prompt=prompt,
        prompt_hash=prompt_hash,
        prompt_version=prompt_state.prompt_version,
        prompt_updated_at=prompt_state.updated_at,
        prefix=args.prefix,
        refresh_mode=args.refresh_mode,
        prompt_cache_key=cache_key,
        allow_legacy_cache=allow_legacy_cache,
        sandbox=args.codex_sandbox,
        approval=args.codex_approval,
        debug=args.debug,
        codex_path=args.codex_path,
        timeout_seconds=args.codex_timeout_seconds,
        sequential=args.sequential,
    )

    payload = build_output_payload(
        records=records,
        sessions_root=sessions_root,
        cache_dir=cache_dir,
        prompt_label=prompt_label,
        prompt_version=prompt_state.prompt_version,
        prompt_updated_at=prompt_state.updated_at,
        extra_metadata=extra_metadata,
    )
    if output_style == "human":
        payload = build_human_payload(
            records=records,
            sessions_root=sessions_root,
            cache_dir=cache_dir,
            prompt_label=prompt_label,
            prompt_version=prompt_state.prompt_version,
            prompt_updated_at=prompt_state.updated_at,
            extra_metadata=False,
        )
    write_output(
        payload=payload,
        output=args.output,
        output_style=output_style,
    )


if __name__ == "__main__":
    main()
