"""Enrichment and linking state operations for the database."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3

from ..models import EnrichedRef, PaperRow

STALE_TIMEOUT_MINUTES = 30


# --- Internal helpers ---

def _claim_paper(
    conn: sqlite3.Connection,
    processing_col: str,
    done_col: str,
    extra_condition: str,
    order_by: str,
    columns: str,
) -> PaperRow | None:
    """Atomically claim a paper for processing. Internal helper.

    Args:
        processing_col: Column to set timestamp (e.g., 'llm_processing_at')
        done_col: Column indicating completion (e.g., 'llm_enriched_at')
        extra_condition: Additional WHERE conditions (e.g., 'AND llm_enriched_at IS NOT NULL')
        order_by: ORDER BY clause (e.g., 'collected_at')
        columns: Columns to return (e.g., 'id, kg2_uri, title, abstract, year, authors, refs')
    """
    now = datetime.now().isoformat()
    sql = f"""
        UPDATE papers
        SET {processing_col} = ?
        WHERE id = (
            SELECT id FROM papers
            WHERE {done_col} IS NULL
              AND {processing_col} IS NULL
              {extra_condition}
            ORDER BY CASE WHEN year IS NULL THEN 1 ELSE 0 END, year ASC, {order_by}
            LIMIT 1
        )
        RETURNING {columns}
    """
    row = conn.execute(sql, (now,)).fetchone()
    conn.commit()
    return PaperRow.from_row(row) if row else None


def _next_paper(
    conn: sqlite3.Connection,
    done_col: str,
    extra_condition: str,
    order_by: str,
    columns: str,
) -> PaperRow | None:
    """Get next paper for processing (non-atomic). Internal helper."""
    sql = f"""
        SELECT {columns}
        FROM papers
        WHERE {done_col} IS NULL
          {extra_condition}
        ORDER BY CASE WHEN year IS NULL THEN 1 ELSE 0 END, year ASC, {order_by}
        LIMIT 1
    """
    row = conn.execute(sql).fetchone()
    return PaperRow.from_row(row) if row else None


def _reset_stale(
    conn: sqlite3.Connection,
    processing_col: str,
    done_col: str,
    timeout_minutes: int,
) -> int:
    """Reset papers stuck in processing state. Internal helper."""
    cutoff = (datetime.now() - timedelta(minutes=timeout_minutes)).isoformat()
    cursor = conn.execute(f"""
        UPDATE papers
        SET {processing_col} = NULL
        WHERE {processing_col} IS NOT NULL
          AND {done_col} IS NULL
          AND {processing_col} < ?
    """, (cutoff,))
    return cursor.rowcount


# --- Enrichment columns ---
_ENRICH_PROCESSING = 'llm_processing_at'
_ENRICH_DONE = 'llm_enriched_at'
_ENRICH_COLS = 'id, kg2_uri, title, abstract, year, authors, refs'
_ENRICH_ORDER = 'collected_at'

# --- Linking columns ---
_LINK_PROCESSING = 'link_processing_at'
_LINK_DONE = 'link_checked_at'
_LINK_COLS = 'id, kg2_uri, title, refs, year'
_LINK_ORDER = 'llm_enriched_at'
_LINK_CONDITION = 'AND llm_enriched_at IS NOT NULL'


# --- Public API ---

def claim_unenriched_paper(conn: sqlite3.Connection) -> PaperRow | None:
    """Atomically claim the next unenriched paper for processing."""
    return _claim_paper(conn, _ENRICH_PROCESSING, _ENRICH_DONE, '', _ENRICH_ORDER, _ENRICH_COLS)


def next_unenriched_paper(conn: sqlite3.Connection) -> PaperRow | None:
    """Get next unenriched paper (not parallel-safe)."""
    return _next_paper(conn, _ENRICH_DONE, '', _ENRICH_ORDER, _ENRICH_COLS)


def claim_unlinked_paper(conn: sqlite3.Connection) -> PaperRow | None:
    """Atomically claim the next unlinked paper for processing."""
    return _claim_paper(conn, _LINK_PROCESSING, _LINK_DONE, _LINK_CONDITION, _LINK_ORDER, _LINK_COLS)


def next_unlinked_paper(conn: sqlite3.Connection) -> PaperRow | None:
    """Get next unlinked paper (not parallel-safe)."""
    return _next_paper(conn, _LINK_DONE, _LINK_CONDITION, _LINK_ORDER, _LINK_COLS)


def mark_enriched(conn: sqlite3.Connection, paper_id: str) -> None:
    """Mark paper as enriched and clear processing flag."""
    conn.execute(
        f"UPDATE papers SET {_ENRICH_DONE} = ?, {_ENRICH_PROCESSING} = NULL WHERE id = ?",
        (datetime.now().isoformat(), paper_id)
    )


def mark_enriched_skipped(conn: sqlite3.Connection, paper_id: str, reason: str) -> None:
    """Mark paper as enriched but skipped, with a reason."""
    conn.execute(
        f"""UPDATE papers
           SET {_ENRICH_DONE} = ?, {_ENRICH_PROCESSING} = NULL, enrichment_skip_reason = ?
           WHERE id = ?""",
        (datetime.now().isoformat(), reason, paper_id)
    )


def mark_link_checked(conn: sqlite3.Connection, paper_id: str) -> None:
    """Mark paper as link-checked and clear processing flag."""
    conn.execute(
        f"UPDATE papers SET {_LINK_DONE} = ?, {_LINK_PROCESSING} = NULL WHERE id = ?",
        (datetime.now().isoformat(), paper_id)
    )


def reset_stale_enrichment(conn: sqlite3.Connection,
                           timeout_minutes: int = STALE_TIMEOUT_MINUTES) -> int:
    """Reset papers stuck in enrichment processing (crashed worker)."""
    return _reset_stale(conn, _ENRICH_PROCESSING, _ENRICH_DONE, timeout_minutes)


def reset_stale_linking(conn: sqlite3.Connection,
                        timeout_minutes: int = STALE_TIMEOUT_MINUTES) -> int:
    """Reset papers stuck in linking processing (crashed worker)."""
    return _reset_stale(conn, _LINK_PROCESSING, _LINK_DONE, timeout_minutes)


def reset_link_checked_for_citers(conn: sqlite3.Connection, cited_id: str) -> int:
    """Reset link_checked_at for papers that cite the given paper."""
    cursor = conn.execute(f"""
        UPDATE papers
        SET {_LINK_DONE} = NULL, {_LINK_PROCESSING} = NULL
        WHERE {_LINK_DONE} IS NOT NULL
          AND refs LIKE ?
    """, (f'%"{cited_id}"%',))
    return cursor.rowcount


def get_enriched_refs(conn: sqlite3.Connection, ref_ids: list[str]) -> list[EnrichedRef]:
    """Get enriched papers from a list of reference IDs."""
    if not ref_ids:
        return []
    placeholders = ','.join('?' * len(ref_ids))
    rows = conn.execute(f"""
        SELECT id, kg2_uri, title, year
        FROM papers
        WHERE id IN ({placeholders})
          AND {_ENRICH_DONE} IS NOT NULL
    """, ref_ids).fetchall()
    return [
        EnrichedRef(id=row['id'], kg2_uri=row['kg2_uri'], title=row['title'], year=row['year'])
        for row in rows
    ]
