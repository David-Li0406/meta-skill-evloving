"""Time parsing and formatting helpers for reflect_sessions."""

from __future__ import annotations

from datetime import datetime, timezone


def parse_timestamp(value: str) -> datetime:
    """Parse a session timestamp into UTC.

    Args:
        value: ISO timestamp string (with optional 'Z').

    Returns:
        Timezone-aware datetime in UTC.

    Example:
        parsed = parse_timestamp(value="2026-01-12T00:00:00Z")
    """
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def format_iso_utc(timestamp: datetime) -> str:
    """Format a datetime in ISO 8601 UTC with Z suffix.

    Args:
        timestamp: Timezone-aware datetime.

    Returns:
        ISO 8601 UTC timestamp string.
    """
    return timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime_arg(value: str) -> datetime:
    """Parse a CLI datetime argument (date or datetime) into UTC.

    Args:
        value: ISO date or datetime string.

    Returns:
        Timezone-aware datetime in UTC.

    Example:
        parsed = parse_datetime_arg(value="2026-01-12")
    """
    if len(value) == 10:
        parsed = datetime.fromisoformat(value)
        return parsed.replace(tzinfo=timezone.utc)
    return parse_timestamp(value=value)


def utc_date_str(timestamp: datetime) -> str:
    """Return a UTC date string (YYYY-MM-DD).

    Args:
        timestamp: Timezone-aware datetime.

    Returns:
        Date string in UTC.
    """
    return timestamp.astimezone(timezone.utc).date().isoformat()


def now_iso() -> str:
    """Return the current time as an ISO 8601 UTC string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
