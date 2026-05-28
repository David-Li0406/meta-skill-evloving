"""Data models for reflect_sessions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .time import format_iso_utc


@dataclass(slots=True)
class SessionMeta:
    """Metadata for a Codex session JSONL file.

    Attributes:
        session_id: Session UUID.
        timestamp: Session timestamp in UTC.
        cwd: Working directory captured in session metadata.
        path: Path to the JSONL file on disk.

    Example:
        meta = SessionMeta(
            session_id="uuid",
            timestamp=datetime(2026, 1, 12, tzinfo=timezone.utc),
            cwd=Path("/tmp"),
            path=Path("rollout-...jsonl"),
        )
    """

    session_id: str
    timestamp: datetime
    cwd: Path | None
    path: Path

    def project_name(self) -> str:
        """Return a project label based on the session cwd.

        Returns:
            Project name derived from the cwd, or "unknown".
        """
        return self.cwd.name if self.cwd else "unknown"

    def iso_timestamp(self) -> str:
        """Return the timestamp as an ISO 8601 UTC string."""
        return format_iso_utc(timestamp=self.timestamp)

    def label(self) -> str:
        """Return a canonical label for debug output.

        Returns:
            Label string for the session.
        """
        return f"{self.session_id} ({self.project_name()})"


@dataclass(slots=True)
class CacheEntry:
    """Cached reflection metadata for a session.

    Attributes:
        session_id: Original session UUID.
        session_timestamp: ISO timestamp from the session meta.
        project: Project label derived from cwd.
        source_path: Path to the original session JSONL.
        reflection: Reflection paragraph text.
        created_at: ISO timestamp when the cache entry was created.
        cache_schema_version: Schema version for cache entries.
        prompt_version: Version string for the reflection prompt.
        prompt_updated_at: ISO timestamp for the prompt version.
        prompt_hash: SHA-256 hash of the prompt text.
        prompt: Prompt text used to generate the reflection.

    Example:
        entry = CacheEntry(
            session_id="uuid",
            session_timestamp="2026-01-12T00:00:00Z",
            project="AutoSkill",
            source_path="/tmp/rollout.jsonl",
            reflection="One paragraph summary...",
            created_at="2026-01-12T00:00:00Z",
            cache_schema_version="cache-v1",
            prompt_version="v1",
            prompt_updated_at="2026-01-12T00:00:00Z",
            prompt_hash="hash",
            prompt="Prompt text",
        )
    """

    session_id: str
    session_timestamp: str
    project: str
    source_path: str
    reflection: str
    created_at: str
    cache_schema_version: str
    prompt_version: str
    prompt_updated_at: str
    prompt_hash: str
    prompt: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation.

        Returns:
            Dict representation of the cache entry.
        """
        return {
            "session_id": self.session_id,
            "session_timestamp": self.session_timestamp,
            "project": self.project,
            "source_path": self.source_path,
            "reflection": self.reflection,
            "created_at": self.created_at,
            "cache_schema_version": self.cache_schema_version,
            "prompt_version": self.prompt_version,
            "prompt_updated_at": self.prompt_updated_at,
            "prompt_hash": self.prompt_hash,
            "prompt": self.prompt,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheEntry":
        """Create a CacheEntry from a parsed dict.

        Args:
            data: Parsed JSON dictionary.

        Returns:
            CacheEntry instance.
        """
        return cls(
            session_id=str(data["session_id"]),
            session_timestamp=str(data["session_timestamp"]),
            project=str(data["project"]),
            source_path=str(data["source_path"]),
            reflection=str(data["reflection"]),
            created_at=str(data["created_at"]),
            cache_schema_version=str(data.get("cache_schema_version", "legacy")),
            prompt_version=str(data.get("prompt_version", "legacy")),
            prompt_updated_at=str(data.get("prompt_updated_at", "unknown")),
            prompt_hash=str(data.get("prompt_hash", "")),
            prompt=str(data["prompt"]),
        )


@dataclass(slots=True)
class ReflectionRecord:
    """Reflection output for a session.

    Attributes:
        meta: Session metadata.
        reflection: Reflection paragraph.
        cached: Whether the reflection came from cache.
        cache_path: Path to the cache entry file.
        cache_schema_version: Cache schema version stored with the entry.
        cache_prompt_version: Prompt version stored with the entry.
        cache_prompt_updated_at: Prompt updated timestamp stored with the entry.
        conversation_updated_at: Latest timestamp in the session history.
        conversation_title: First user message truncated for display.
        reflection_created_at: Timestamp when reflection was created.
        cache_status: Reflection freshness status (fresh/out_of_date).
        cache_status_reason: Explanation for the freshness decision.
    """

    meta: SessionMeta
    reflection: str
    cached: bool
    cache_path: Path
    cache_schema_version: str
    cache_prompt_version: str
    cache_prompt_updated_at: str
    conversation_updated_at: str
    conversation_title: str
    reflection_created_at: str
    cache_status: str
    cache_status_reason: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation.

        Returns:
            Dict representation of the reflection record.
        """
        return {
            "session_id": self.meta.session_id,
            "timestamp": self.meta.iso_timestamp(),
            "project": self.meta.project_name(),
            "source_path": str(self.meta.path),
            "reflection": self.reflection,
            "cached": self.cached,
            "cache_path": str(self.cache_path),
            "cache_schema_version": self.cache_schema_version,
            "cache_prompt_version": self.cache_prompt_version,
            "cache_prompt_updated_at": self.cache_prompt_updated_at,
            "conversation_updated_at": self.conversation_updated_at,
            "conversation_title": self.conversation_title,
            "reflection_created_at": self.reflection_created_at,
            "cache_status": self.cache_status,
            "cache_status_reason": self.cache_status_reason,
        }


@dataclass(slots=True)
class ConversationInfo:
    """Metadata derived from a conversation history.

    Attributes:
        updated_at: Latest timestamp in the session history.
        updated_at_iso: ISO timestamp for updated_at.
        title: Truncated first user message for display.
    """

    updated_at: datetime
    updated_at_iso: str
    title: str


@dataclass(slots=True)
class CacheDecision:
    """Decision on whether to use cached reflection content.

    Attributes:
        use_cache: Whether to return cached reflection.
        status: Reflection freshness status (fresh/out_of_date).
        reason: Explanation for the status decision.
    """

    use_cache: bool
    status: str
    reason: str


@dataclass(slots=True)
class ProjectGroup:
    """Group of reflections for a project.

    Attributes:
        project: Project label.
        sessions: Session reflection records.
    """

    project: str
    sessions: list[ReflectionRecord]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation.

        Returns:
            Dict representation of the project group.
        """
        return {
            "project": self.project,
            "sessions": [record.to_dict() for record in self.sessions],
        }


@dataclass(slots=True)
class PromptVersionState:
    """Prompt version metadata stored alongside the prompt.

    Attributes:
        prompt_version: Version string for the prompt.
        prompt_hash: SHA-256 hash of the prompt text.
        updated_at: ISO timestamp for when the prompt version was set.
    """

    prompt_version: str
    prompt_hash: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "prompt_version": self.prompt_version,
            "prompt_hash": self.prompt_hash,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PromptVersionState":
        """Create PromptVersionState from a parsed dict.

        Args:
            data: Parsed JSON dictionary.

        Returns:
            PromptVersionState instance.
        """
        return cls(
            prompt_version=str(data.get("prompt_version", "")),
            prompt_hash=str(data.get("prompt_hash", "")),
            updated_at=str(data.get("updated_at", "")),
        )
