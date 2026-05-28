"""Queue operations for the database."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3

from ..models import QueueCandidate, QueueStatus, Relation
from .papers import paper_exists


def queue_exists(conn: sqlite3.Connection, paper_id: str) -> bool:
    """Check if paper is in queue."""
    row = conn.execute(
        "SELECT 1 FROM queue WHERE id = ?", (paper_id,)
    ).fetchone()
    return row is not None


def enqueue(conn: sqlite3.Connection, paper_id: str, score: float,
            source_id: str, relation: Relation | str) -> None:
    """Add paper to queue if not already present."""
    if paper_exists(conn, paper_id) or queue_exists(conn, paper_id):
        return
    # Convert Enum to string value for SQL
    relation_str = relation.value if isinstance(relation, Relation) else relation
    conn.execute("""
        INSERT INTO queue (id, score, source_id, relation, status, discovered_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (paper_id, score, source_id, relation_str, QueueStatus.PENDING.value, datetime.now().isoformat()))


def next_candidate(conn: sqlite3.Connection) -> QueueCandidate | None:
    """Get highest-score pending candidate."""
    row = conn.execute("""
        SELECT id, score, source_id, relation, status FROM queue
        WHERE status = ?
        ORDER BY score DESC
        LIMIT 1
    """, (QueueStatus.PENDING.value,)).fetchone()
    if not row:
        return None
    return QueueCandidate(
        id=row['id'],
        score=row['score'],
        source_id=row['source_id'],
        relation=row['relation'],
        status=row['status'],
    )


def update_queue_status(conn: sqlite3.Connection, paper_id: str,
                        status: QueueStatus | str,
                        skip_reason: str | None = None) -> None:
    """Update queue item status."""
    status_str = status.value if isinstance(status, QueueStatus) else status
    conn.execute("""
        UPDATE queue SET status = ?, processed_at = ?, skip_reason = ?
        WHERE id = ?
    """, (status_str, datetime.now().isoformat(), skip_reason, paper_id))


def reset_processing_to_pending(conn: sqlite3.Connection) -> int:
    """Reset all 'processing' queue items back to 'pending'.

    Used when resuming after an interrupted collection.

    Returns:
        Number of items reset
    """
    cursor = conn.execute("""
        UPDATE queue
        SET status = ?, processed_at = NULL
        WHERE status = ?
    """, (QueueStatus.PENDING.value, QueueStatus.PROCESSING.value))
    return cursor.rowcount


