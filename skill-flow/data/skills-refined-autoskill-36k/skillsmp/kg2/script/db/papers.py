"""Paper operations for the database."""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3

from ..models import Author, Paper, PaperStatus, Venue


def paper_exists(conn: sqlite3.Connection, paper_id: str) -> bool:
    """Check if paper exists."""
    row = conn.execute(
        "SELECT 1 FROM papers WHERE id = ?", (paper_id,)
    ).fetchone()
    return row is not None


def get_kg2_uri(conn: sqlite3.Connection, paper_id: str) -> str | None:
    """Get kg2 URI for paper."""
    row = conn.execute(
        "SELECT kg2_uri FROM papers WHERE id = ?", (paper_id,)
    ).fetchone()
    return row['kg2_uri'] if row else None


def insert_paper(conn: sqlite3.Connection, paper: Paper, kg2_uri: str) -> None:
    """Insert paper into database."""
    authors_json = json.dumps([
        {'authorId': a.author_id, 'name': a.name}
        for a in paper.authors
    ])
    # Convert Enum to string value for SQL
    status_str = paper.status.value if isinstance(paper.status, PaperStatus) else paper.status
    conn.execute("""
        INSERT INTO papers (
            id, doi, arxiv_id, kg2_uri, title, authors, year, abstract,
            citation_count, venue_id, venue_name, venue_type,
            refs, cites, status, collected_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        paper.id, paper.doi, paper.arxiv_id, kg2_uri, paper.title,
        authors_json, paper.year, paper.abstract, paper.citation_count,
        paper.venue.venue_id if paper.venue else None,
        paper.venue.name if paper.venue else None,
        paper.venue.venue_type if paper.venue else None,
        json.dumps(paper.references), json.dumps(paper.citations),
        status_str, datetime.now().isoformat()
    ))


def load_paper(conn: sqlite3.Connection, paper_id: str) -> Paper | None:
    """Load paper from database."""
    row = conn.execute(
        "SELECT * FROM papers WHERE id = ?", (paper_id,)
    ).fetchone()
    if not row:
        return None
    return _row_to_paper(row)


def _row_to_paper(row: sqlite3.Row) -> Paper:
    """Convert database row to Paper object."""
    authors_data = json.loads(row['authors']) if row['authors'] else []
    authors = [
        Author(name=a['name'], author_id=a.get('authorId'))
        for a in authors_data
    ]

    venue = None
    if row['venue_name']:
        venue = Venue(
            name=row['venue_name'],
            venue_id=row['venue_id'],
            venue_type=row['venue_type'],
        )

    # Convert string status to Enum
    status = PaperStatus(row['status']) if row['status'] else PaperStatus.COLLECTED

    return Paper(
        id=row['id'],
        title=row['title'],
        year=row['year'],
        abstract=row['abstract'],
        doi=row['doi'],
        arxiv_id=row['arxiv_id'],
        citation_count=row['citation_count'] or 0,
        authors=authors,
        venue=venue,
        references=json.loads(row['refs']) if row['refs'] else [],
        citations=json.loads(row['cites']) if row['cites'] else [],
        status=status,
    )


def count_papers(conn: sqlite3.Connection) -> int:
    """Count total papers."""
    row = conn.execute("SELECT COUNT(*) as cnt FROM papers").fetchone()
    return row['cnt']


def get_seed_ids(conn: sqlite3.Connection) -> set[str]:
    """Get set of seed paper IDs."""
    rows = conn.execute(
        "SELECT id FROM papers WHERE status = ?", (PaperStatus.SEED.value,)
    ).fetchall()
    return {row['id'] for row in rows}


def get_collected_ids(conn: sqlite3.Connection) -> set[str]:
    """Get set of all collected paper IDs."""
    rows = conn.execute("SELECT id FROM papers").fetchall()
    return {row['id'] for row in rows}


def iter_papers_without_abstract(conn: sqlite3.Connection):
    """Iterate over papers missing abstracts.

    Yields:
        Row dicts with id, arxiv_id, doi, title fields
    """
    cursor = conn.execute("""
        SELECT id, arxiv_id, doi, title
        FROM papers
        WHERE abstract IS NULL
        ORDER BY collected_at
    """)
    return cursor


def update_abstract(conn: sqlite3.Connection, paper_id: str, abstract: str) -> None:
    """Update paper's abstract."""
    conn.execute(
        "UPDATE papers SET abstract = ? WHERE id = ?",
        (abstract, paper_id)
    )
