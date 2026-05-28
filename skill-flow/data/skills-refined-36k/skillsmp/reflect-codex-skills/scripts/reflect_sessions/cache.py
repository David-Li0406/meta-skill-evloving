"""Cache handling for reflect_sessions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import (
    AUTO_REFRESH_REASONS,
    CACHE_SCHEMA_VERSION,
    DEFAULT_CACHE_DIR_NAME,
)
from .debug import debug_print
from .models import (
    CacheDecision,
    CacheEntry,
    ConversationInfo,
    ReflectionRecord,
    SessionMeta,
)
from .sessions import build_conversation_info
from .time import now_iso, parse_timestamp


@dataclass(slots=True)
class CacheContext:
    """Cache context for a single reflection run.

    Attributes:
        cache_path: Path to write new cache entries.
        entry_path: Path where an existing cache entry was loaded from.
        conversation: Conversation metadata for freshness checks.
        entry: Cached reflection entry, if any.
        decision: Cache decision for this entry.
    """

    cache_path: Path
    entry_path: Path | None
    conversation: ConversationInfo
    entry: CacheEntry | None
    decision: CacheDecision


def format_refresh_reason(
    *, staleness_reasons: list[str], refresh_mode: str
) -> str:
    """Format a refresh reason string for cache status output.

    Args:
        staleness_reasons: Reasons the cached reflection is outdated.
        refresh_mode: Refresh mode that triggered regeneration.

    Returns:
        Refresh reason string for output.
    """
    if staleness_reasons:
        return f"refreshed:{','.join(staleness_reasons)}"
    return f"refreshed:{refresh_mode}"


def refresh_decision(
    *, staleness_reasons: list[str], refresh_mode: str
) -> CacheDecision:
    """Build a cache decision for a refreshed reflection.

    Args:
        staleness_reasons: Reasons the cached reflection is outdated.
        refresh_mode: Refresh mode that triggered regeneration.

    Returns:
        CacheDecision for a regenerated reflection.
    """
    return CacheDecision(
        use_cache=False,
        status="fresh",
        reason=format_refresh_reason(
            staleness_reasons=staleness_reasons,
            refresh_mode=refresh_mode,
        ),
    )


def assess_cache_decision(
    *,
    entry: CacheEntry | None,
    conversation_updated_at: datetime,
    prompt_updated_at: datetime,
    refresh_mode: str,
) -> CacheDecision:
    """Assess whether to use cached reflection content.

    Args:
        entry: Cache entry if present.
        conversation_updated_at: Latest conversation update timestamp.
        prompt_updated_at: Prompt updated timestamp.
        refresh_mode: Cache refresh mode (never, auto, always).

    Returns:
        CacheDecision indicating whether to use the cache.
    """
    if entry is None:
        return CacheDecision(use_cache=False, status="fresh", reason="generated")
    created_at = parse_timestamp(value=entry.created_at)
    staleness_reasons: list[str] = []
    if conversation_updated_at > created_at:
        staleness_reasons.append("conversation_updated_after_reflection")
    if prompt_updated_at > created_at:
        staleness_reasons.append("prompt_updated_after_reflection")
    if entry.cache_schema_version != CACHE_SCHEMA_VERSION:
        staleness_reasons.append("cache_schema_mismatch")
    auto_refresh_reasons = [r for r in staleness_reasons if r in AUTO_REFRESH_REASONS]
    if refresh_mode == "always":
        return refresh_decision(
            staleness_reasons=staleness_reasons,
            refresh_mode=refresh_mode,
        )
    if refresh_mode == "auto" and auto_refresh_reasons:
        return refresh_decision(
            staleness_reasons=staleness_reasons,
            refresh_mode=refresh_mode,
        )
    if staleness_reasons:
        return CacheDecision(
            use_cache=True,
            status="out_of_date",
            reason=",".join(staleness_reasons),
        )
    return CacheDecision(use_cache=True, status="fresh", reason="cache_up_to_date")


def build_reflection_record(
    *,
    meta: SessionMeta,
    entry: CacheEntry,
    cache_path: Path,
    conversation: ConversationInfo,
    cached: bool,
    cache_status: str,
    cache_status_reason: str,
) -> ReflectionRecord:
    """Build a ReflectionRecord from cache entry metadata.

    Args:
        meta: Session metadata.
        entry: Cache entry for the reflection.
        cache_path: Path to the cache entry file.
        conversation: Derived conversation metadata.
        cached: Whether the reflection came from cache.
        cache_status: Reflection freshness status.
        cache_status_reason: Explanation for freshness.

    Returns:
        ReflectionRecord instance.
    """
    return ReflectionRecord(
        meta=meta,
        reflection=entry.reflection,
        cached=cached,
        cache_path=cache_path,
        cache_schema_version=entry.cache_schema_version,
        cache_prompt_version=entry.prompt_version,
        cache_prompt_updated_at=entry.prompt_updated_at,
        conversation_updated_at=conversation.updated_at_iso,
        conversation_title=conversation.title,
        reflection_created_at=entry.created_at,
        cache_status=cache_status,
        cache_status_reason=cache_status_reason,
    )


def maybe_cached_record(
    *,
    meta: SessionMeta,
    entry: CacheEntry | None,
    entry_path: Path | None,
    conversation: ConversationInfo,
    decision: CacheDecision,
    debug: bool,
) -> ReflectionRecord | None:
    """Return a cached reflection record when allowed.

    Args:
        meta: Session metadata.
        entry: Cache entry if available.
        entry_path: Path to cache entry file.
        conversation: Derived conversation metadata.
        decision: Cache decision for this session.
        debug: Whether to emit debug output.

    Returns:
        ReflectionRecord when cache should be used, otherwise None.
    """
    if entry is None or not decision.use_cache:
        return None
    assert entry_path is not None, "Cache entry path is missing"
    debug_print(enabled=debug, message=f"Using cache for {meta.label()}")
    return build_reflection_record(
        meta=meta,
        entry=entry,
        cache_path=entry_path,
        conversation=conversation,
        cached=True,
        cache_status=decision.status,
        cache_status_reason=decision.reason,
    )


def ensure_cache_dir(*, sessions_root: Path, cache_dir: Path | None) -> Path:
    """Ensure the cache directory exists.

    Args:
        sessions_root: Root directory for sessions.
        cache_dir: Optional override cache directory.

    Returns:
        Path to the cache directory.
    """
    resolved = cache_dir or sessions_root / DEFAULT_CACHE_DIR_NAME
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def cache_path_for_session(
    *, cache_dir: Path, session_id: str, prompt_cache_key: str
) -> Path:
    """Return the cache path for a session id and prompt key.

    Args:
        cache_dir: Cache directory path.
        session_id: Session UUID.
        prompt_cache_key: Stable cache key for the prompt.

    Returns:
        Cache file path.
    """
    return cache_dir / f"{session_id}-{prompt_cache_key}.json"


def legacy_cache_path_for_session(*, cache_dir: Path, session_id: str) -> Path:
    """Return the legacy cache path for a session id.

    Args:
        cache_dir: Cache directory path.
        session_id: Session UUID.

    Returns:
        Legacy cache file path.
    """
    return cache_dir / f"{session_id}.json"


def load_cache_entry(*, path: Path) -> CacheEntry:
    """Load a cached reflection entry.

    Args:
        path: Cache file path.

    Returns:
        CacheEntry parsed from disk.

    Example:
        entry = load_cache_entry(path=Path("cache.json"))
    """
    data = json.loads(path.read_text())
    assert isinstance(data, dict), "Cache entry is not a dict"
    return CacheEntry.from_dict(data=data)


def write_cache_entry(*, path: Path, entry: CacheEntry) -> None:
    """Write a cached reflection entry.

    Args:
        path: Cache file path.
        entry: Cache entry to write.
    """
    payload = json.dumps(entry.to_dict(), indent=2, ensure_ascii=True)
    path.write_text(payload + "\n")


def build_cache_entry(
    *,
    meta: SessionMeta,
    reflection: str,
    prompt: str,
    prompt_hash: str,
    prompt_version: str,
    prompt_updated_at: str,
) -> CacheEntry:
    """Build a cache entry for a reflection.

    Args:
        meta: Session metadata.
        reflection: Reflection paragraph.
        prompt: Prompt text used to generate the reflection.
        prompt_hash: SHA-256 hash for the prompt.
        prompt_version: Prompt version string.
        prompt_updated_at: Prompt updated timestamp.

    Returns:
        CacheEntry instance.
    """
    return CacheEntry(
        session_id=meta.session_id,
        session_timestamp=meta.iso_timestamp(),
        project=meta.project_name(),
        source_path=str(meta.path),
        reflection=reflection,
        created_at=now_iso(),
        cache_schema_version=CACHE_SCHEMA_VERSION,
        prompt_version=prompt_version,
        prompt_updated_at=prompt_updated_at,
        prompt_hash=prompt_hash,
        prompt=prompt,
    )


def generate_reflection_entry(
    *,
    meta: SessionMeta,
    prompt: str,
    prompt_hash: str,
    prompt_version: str,
    prompt_updated_at: str,
    prefix: str,
    sandbox: str,
    approval: str,
    debug: bool,
    codex_path: str | None,
    timeout_seconds: int,
    cache_path: Path,
    action_label: str,
) -> CacheEntry:
    """Generate and cache a new reflection entry.

    Args:
        meta: Session metadata.
        prompt: Prompt text to send.
        prompt_hash: SHA-256 hash for the prompt.
        prompt_version: Prompt version string.
        prompt_updated_at: Prompt updated timestamp.
        prefix: Prefix for duplicated session user message.
        sandbox: Sandbox mode for codex.
        approval: Approval policy for codex.
        debug: Whether to emit debug output.
        codex_path: Optional path to the codex binary.
        timeout_seconds: Timeout for the codex call.
        cache_path: Path to cache entry file.
        action_label: Human-readable label for debug output.

    Returns:
        CacheEntry for the generated reflection.
    """
    from .codex import generate_reflection

    debug_print(enabled=debug, message=f"{action_label} reflection for {meta.label()}")
    reflection = generate_reflection(
        session_meta=meta,
        prompt=prompt,
        prefix=prefix,
        sandbox=sandbox,
        approval=approval,
        debug=debug,
        codex_path=codex_path,
        timeout_seconds=timeout_seconds,
    )
    entry = build_cache_entry(
        meta=meta,
        reflection=reflection,
        prompt=prompt,
        prompt_hash=prompt_hash,
        prompt_version=prompt_version,
        prompt_updated_at=prompt_updated_at,
    )
    write_cache_entry(path=cache_path, entry=entry)
    return entry


def _prepare_cache_context(
    *,
    meta: SessionMeta,
    cache_dir: Path,
    prefix: str,
    prompt_updated_at: str,
    refresh_mode: str,
    prompt_cache_key: str,
    allow_legacy_cache: bool,
) -> CacheContext:
    """Prepare cache context for a session reflection.

    Args:
        meta: Session metadata.
        cache_dir: Directory for cached reflections.
        prefix: Prefix for duplicated session user message.
        prompt_updated_at: Prompt updated timestamp.
        refresh_mode: Cache refresh mode (never, auto, always).
        prompt_cache_key: Stable cache key for the prompt selection.
        allow_legacy_cache: Whether to reuse legacy cache entries.

    Returns:
        CacheContext with cache paths and cache decision.
    """
    cache_path = cache_path_for_session(
        cache_dir=cache_dir,
        session_id=meta.session_id,
        prompt_cache_key=prompt_cache_key,
    )
    conversation = build_conversation_info(meta=meta, prefix=prefix)
    prompt_updated_at_dt = parse_timestamp(value=prompt_updated_at)
    entry_path: Path | None = None
    if cache_path.exists():
        entry_path = cache_path
    elif allow_legacy_cache:
        legacy_path = legacy_cache_path_for_session(
            cache_dir=cache_dir,
            session_id=meta.session_id,
        )
        if legacy_path.exists():
            entry_path = legacy_path
    entry = load_cache_entry(path=entry_path) if entry_path else None
    decision = assess_cache_decision(
        entry=entry,
        conversation_updated_at=conversation.updated_at,
        prompt_updated_at=prompt_updated_at_dt,
        refresh_mode=refresh_mode,
    )
    return CacheContext(
        cache_path=cache_path,
        entry_path=entry_path,
        conversation=conversation,
        entry=entry,
        decision=decision,
    )


def reflect_session(
    *,
    meta: SessionMeta,
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
) -> ReflectionRecord:
    """Return a reflection record, using cache when available.

    Args:
        meta: Session metadata.
        cache_dir: Directory for cached reflections.
        prompt: Prompt text to use.
        prompt_hash: SHA-256 hash for the prompt.
        prompt_version: Prompt version string.
        prompt_updated_at: Prompt updated timestamp.
        prefix: Prefix for duplicated session user message.
        refresh_mode: Cache refresh mode (never, auto, always).
        prompt_cache_key: Stable cache key for the prompt selection.
        allow_legacy_cache: Whether to reuse legacy cache entries.
        sandbox: Sandbox mode for codex.
        approval: Approval policy for codex.
        debug: Whether to emit debug output.
        codex_path: Optional path to the codex binary.
        timeout_seconds: Timeout for the codex call.

    Returns:
        ReflectionRecord instance.

    Example:
        record = reflect_session(
            meta=meta,
            cache_dir=Path("/tmp/cache"),
            prompt="Summarize.",
            prompt_hash="hash",
            prompt_version="2026-01-12-v1",
            prompt_updated_at="2026-01-12T00:00:00Z",
            prefix="[SELF-REFLECTION] ",
            refresh_mode="never",
            prompt_cache_key="abc123",
            allow_legacy_cache=True,
            sandbox="read-only",
            approval="never",
            debug=False,
            codex_path=None,
            timeout_seconds=120,
        )
    """
    context = _prepare_cache_context(
        meta=meta,
        cache_dir=cache_dir,
        prefix=prefix,
        prompt_updated_at=prompt_updated_at,
        refresh_mode=refresh_mode,
        prompt_cache_key=prompt_cache_key,
        allow_legacy_cache=allow_legacy_cache,
    )
    cached_record = maybe_cached_record(
        meta=meta,
        entry=context.entry,
        entry_path=context.entry_path,
        conversation=context.conversation,
        decision=context.decision,
        debug=debug,
    )
    if cached_record:
        return cached_record
    action_label = "Refreshing" if context.entry else "Generating"
    entry = generate_reflection_entry(
        meta=meta,
        prompt=prompt,
        prompt_hash=prompt_hash,
        prompt_version=prompt_version,
        prompt_updated_at=prompt_updated_at,
        prefix=prefix,
        sandbox=sandbox,
        approval=approval,
        debug=debug,
        codex_path=codex_path,
        timeout_seconds=timeout_seconds,
        cache_path=context.cache_path,
        action_label=action_label,
    )
    return build_reflection_record(
        meta=meta,
        entry=entry,
        cache_path=context.cache_path,
        conversation=context.conversation,
        cached=False,
        cache_status=context.decision.status,
        cache_status_reason=context.decision.reason,
    )
