"""Pending citation operations for the database."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3


def add_pending_cites(conn: sqlite3.Connection, citing_id: str, cited_id: str) -> None:
    """Add pending citation relationship."""
    conn.execute("""
        INSERT OR IGNORE INTO pending_cites (citing_id, cited_id, created_at)
        VALUES (?, ?, ?)
    """, (citing_id, cited_id, datetime.now().isoformat()))


def get_pending_cites_to(conn: sqlite3.Connection, cited_id: str) -> list[str]:
    """Get papers waiting to cite this paper."""
    rows = conn.execute(
        "SELECT citing_id FROM pending_cites WHERE cited_id = ?",
        (cited_id,)
    ).fetchall()
    return [row['citing_id'] for row in rows]


def delete_pending_cites(conn: sqlite3.Connection, citing_id: str, cited_id: str) -> None:
    """Delete pending citation relationship."""
    conn.execute(
        "DELETE FROM pending_cites WHERE citing_id = ? AND cited_id = ?",
        (citing_id, cited_id)
    )
