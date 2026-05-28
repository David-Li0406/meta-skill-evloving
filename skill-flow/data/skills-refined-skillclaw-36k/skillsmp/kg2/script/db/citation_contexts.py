"""Citation context operations for the database."""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3


def save_citation_contexts(
    conn: sqlite3.Connection,
    citing_id: str,
    contexts: list[dict],
) -> int:
    """Save citation contexts for a paper's references.

    Args:
        conn: Database connection
        citing_id: S2 paper ID of the citing paper
        contexts: List of dicts with cited_id, intents, contexts

    Returns:
        Number of contexts saved
    """
    saved = 0
    now = datetime.now().isoformat()

    for ctx in contexts:
        cited_id = ctx.get('cited_id')
        if not cited_id:
            continue

        conn.execute("""
            INSERT OR REPLACE INTO citation_contexts
            (citing_id, cited_id, intents, contexts, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            citing_id,
            cited_id,
            json.dumps(ctx.get('intents') or []),
            json.dumps(ctx.get('contexts') or []),
            now,
        ))
        saved += 1

    return saved


def get_citation_context(
    conn: sqlite3.Connection,
    citing_id: str,
    cited_id: str,
) -> dict | None:
    """Get citation context between two papers.

    Args:
        conn: Database connection
        citing_id: S2 paper ID of the citing paper
        cited_id: S2 paper ID of the cited paper

    Returns:
        Dict with intents and contexts, or None if not found
    """
    row = conn.execute("""
        SELECT intents, contexts FROM citation_contexts
        WHERE citing_id = ? AND cited_id = ?
    """, (citing_id, cited_id)).fetchone()

    if not row:
        return None

    return {
        'intents': json.loads(row['intents']) if row['intents'] else [],
        'contexts': json.loads(row['contexts']) if row['contexts'] else [],
    }


def get_citation_contexts_for_paper(
    conn: sqlite3.Connection,
    citing_id: str,
) -> dict[str, dict]:
    """Get all citation contexts for a paper's references.

    Args:
        conn: Database connection
        citing_id: S2 paper ID of the citing paper

    Returns:
        Dict mapping cited_id to {intents, contexts}
    """
    rows = conn.execute("""
        SELECT cited_id, intents, contexts FROM citation_contexts
        WHERE citing_id = ?
    """, (citing_id,)).fetchall()

    result = {}
    for row in rows:
        result[row['cited_id']] = {
            'intents': json.loads(row['intents']) if row['intents'] else [],
            'contexts': json.loads(row['contexts']) if row['contexts'] else [],
        }
    return result


def mark_contexts_fetched(conn: sqlite3.Connection, paper_id: str) -> None:
    """Mark that citation contexts have been fetched for a paper."""
    conn.execute("""
        UPDATE papers SET contexts_fetched_at = ?
        WHERE id = ?
    """, (datetime.now().isoformat(), paper_id))


def get_papers_needing_contexts(
    conn: sqlite3.Connection,
    limit: int = 100,
) -> list[str]:
    """Get paper IDs that need citation contexts fetched.

    Returns papers that:
    - Have been collected (status = 'collected' or 'seed')
    - Don't have contexts_fetched_at set
    - Have references

    Args:
        conn: Database connection
        limit: Maximum papers to return

    Returns:
        List of paper IDs
    """
    rows = conn.execute("""
        SELECT id FROM papers
        WHERE contexts_fetched_at IS NULL
        AND status IN ('collected', 'seed')
        AND refs IS NOT NULL
        AND refs != '[]'
        ORDER BY collected_at
        LIMIT ?
    """, (limit,)).fetchall()

    return [row['id'] for row in rows]
