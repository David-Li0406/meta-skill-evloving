#!/usr/bin/env python3
"""
CLI utilities for memory_helper.py - shared functions for ID resolution, date parsing, etc.
"""

import sys
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps

# Import from hooks.common
from hooks.common import check_helix_running, get_all_memories


def requires_helix(func):
    """Decorator that ensures HelixDB is running before executing command."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_helix_running():
            print("ERROR: HelixDB not running", file=sys.stderr)
            sys.exit(1)
        return func(*args, **kwargs)
    return wrapper


def resolve_memory_id(partial_id: str, memories: list = None) -> str:
    """
    Resolve partial ID prefix to full memory ID.

    Args:
        partial_id: Full or partial UUID
        memories: Optional list of memories (fetched if not provided)

    Returns:
        Full memory ID

    Raises:
        SystemExit: If no match or multiple matches found
    """
    # If already a full UUID, return as-is
    if len(partial_id) >= 36:
        return partial_id

    # Fetch memories if not provided
    if memories is None:
        memories = get_all_memories()

    # Find matches by prefix
    matches = [m for m in memories if m.get('id', '').startswith(partial_id)]

    if len(matches) == 0:
        print(f"ERROR: No memory found with ID prefix: {partial_id}", file=sys.stderr)
        sys.exit(1)
    elif len(matches) > 1:
        print(f"ERROR: Multiple memories match prefix '{partial_id}':", file=sys.stderr)
        for m in matches:
            print(f"  {m.get('id')} - {m.get('content', '')[:50]}...", file=sys.stderr)
        print("Provide more characters to uniquely identify", file=sys.stderr)
        sys.exit(1)
    else:
        return matches[0].get('id')


def parse_date_arg(date_str: str) -> Optional[datetime]:
    """
    Parse date argument. Supports:
    - 'yesterday', 'today'
    - 'YYYY-MM-DD' format
    - 'N days ago' format

    Args:
        date_str: Date string to parse

    Returns:
        datetime object or None if parsing fails
    """
    date_str = date_str.strip().lower()

    if date_str == 'today':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str == 'yesterday':
        return (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str.endswith(' days ago'):
        try:
            days = int(date_str.split()[0])
            return (datetime.now() - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            pass

    # Try ISO format YYYY-MM-DD
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        pass

    return None


def parse_memory_timestamp(memory: dict) -> Optional[datetime]:
    """
    Extract creation timestamp from memory.
    First tries created_at field (ISO timestamp), falls back to UUID parsing.

    Args:
        memory: Memory dictionary

    Returns:
        datetime object or None if parsing fails
    """
    # Try created_at field first (ISO format)
    created_at = memory.get('created_at')
    if created_at:
        try:
            # Handle ISO format with/without microseconds
            if '.' in created_at:
                return datetime.fromisoformat(created_at)
            else:
                return datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            pass

    # Fallback: try to parse from UUID (less reliable)
    uuid_str = memory.get('id', '')
    if uuid_str:
        try:
            # Remove hyphens and get first 12 hex chars
            hex_str = uuid_str.replace('-', '')[:12]
            unix_ms = int(hex_str, 16)
            # Validate reasonable timestamp range (2020-2030)
            if 1577836800000 < unix_ms < 1893456000000:
                return datetime.fromtimestamp(unix_ms / 1000.0)
        except (ValueError, OSError):
            pass

    return None


def filter_memories_by_date(
    memories: list,
    since_date: Optional[datetime] = None,
    exact_date: Optional[datetime] = None
) -> list:
    """
    Filter memories by date range.

    Args:
        memories: List of memory dictionaries
        since_date: If provided, return memories created on or after this date
        exact_date: If provided, return memories created on this exact day

    Returns:
        Filtered list of memories (with _created_at field added)
    """
    if not since_date and not exact_date:
        return memories

    filtered = []
    for m in memories:
        created = parse_memory_timestamp(m)
        if not created:
            continue  # Skip if can't parse timestamp

        if since_date and created >= since_date:
            m_copy = m.copy()
            m_copy['_created_at'] = created
            filtered.append(m_copy)
        elif exact_date:
            # Exact date match (same day)
            next_day = exact_date + timedelta(days=1)
            if exact_date <= created < next_day:
                m_copy = m.copy()
                m_copy['_created_at'] = created
                filtered.append(m_copy)

    return filtered
