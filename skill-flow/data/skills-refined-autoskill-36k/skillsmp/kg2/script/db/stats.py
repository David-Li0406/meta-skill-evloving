"""Statistics operations for the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import DbStats

if TYPE_CHECKING:
    import sqlite3


def stats(conn: sqlite3.Connection) -> DbStats:
    """Get collection statistics."""
    papers_by_status = {}
    for row in conn.execute(
        "SELECT status, COUNT(*) as cnt FROM papers GROUP BY status"
    ).fetchall():
        papers_by_status[row['status']] = row['cnt']

    queue_by_status = {}
    for row in conn.execute(
        "SELECT status, COUNT(*) as cnt FROM queue GROUP BY status"
    ).fetchall():
        queue_by_status[row['status']] = row['cnt']

    enriched = conn.execute(
        "SELECT COUNT(*) as cnt FROM papers WHERE llm_enriched_at IS NOT NULL"
    ).fetchone()['cnt']
    unenriched = conn.execute(
        "SELECT COUNT(*) as cnt FROM papers WHERE llm_enriched_at IS NULL"
    ).fetchone()['cnt']
    linked = conn.execute(
        "SELECT COUNT(*) as cnt FROM papers WHERE link_checked_at IS NOT NULL"
    ).fetchone()['cnt']
    unlinked = conn.execute(
        "SELECT COUNT(*) as cnt FROM papers WHERE llm_enriched_at IS NOT NULL AND link_checked_at IS NULL"
    ).fetchone()['cnt']

    # Context stats (safe even if column doesn't exist yet)
    try:
        contexts_fetched = conn.execute(
            "SELECT COUNT(*) as cnt FROM papers WHERE contexts_fetched_at IS NOT NULL"
        ).fetchone()['cnt']
        contexts_pending = conn.execute(
            """SELECT COUNT(*) as cnt FROM papers
               WHERE contexts_fetched_at IS NULL
               AND status IN ('collected', 'seed')
               AND refs IS NOT NULL AND refs != '[]'"""
        ).fetchone()['cnt']
    except Exception:
        contexts_fetched = 0
        contexts_pending = 0

    return DbStats(
        papers=papers_by_status,
        queue=queue_by_status,
        total_papers=sum(papers_by_status.values()),
        pending_cites=conn.execute(
            "SELECT COUNT(*) as cnt FROM pending_cites"
        ).fetchone()['cnt'],
        enriched=enriched,
        unenriched=unenriched,
        linked=linked,
        unlinked=unlinked,
        contexts_fetched=contexts_fetched,
        contexts_pending=contexts_pending,
    )
