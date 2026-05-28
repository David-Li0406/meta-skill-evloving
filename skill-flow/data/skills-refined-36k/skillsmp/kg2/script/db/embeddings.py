"""Embedding storage operations for the database."""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

from ..embeddings import deserialize_embedding, serialize_embedding

if TYPE_CHECKING:
    import sqlite3


# --- Paper Embeddings ---

def save_paper_embedding(
    conn: sqlite3.Connection,
    paper_id: str,
    embedding: list[float],
    model: str,
) -> None:
    """Save paper embedding."""
    conn.execute("""
        INSERT OR REPLACE INTO paper_embeddings (paper_id, embedding, model, created_at)
        VALUES (?, ?, ?, ?)
    """, (paper_id, serialize_embedding(embedding), model, datetime.now().isoformat()))


def get_paper_embedding(
    conn: sqlite3.Connection,
    paper_id: str,
) -> list[float] | None:
    """Get paper embedding."""
    row = conn.execute(
        "SELECT embedding FROM paper_embeddings WHERE paper_id = ?",
        (paper_id,)
    ).fetchone()
    if not row:
        return None
    return deserialize_embedding(row['embedding'])


def get_paper_embeddings(
    conn: sqlite3.Connection,
    paper_ids: list[str],
) -> list[tuple[str, list[float]]]:
    """Get embeddings for multiple papers.

    Returns:
        List of (paper_id, embedding) tuples for papers that have embeddings
    """
    if not paper_ids:
        return []

    placeholders = ','.join('?' * len(paper_ids))
    rows = conn.execute(f"""
        SELECT paper_id, embedding FROM paper_embeddings
        WHERE paper_id IN ({placeholders})
    """, paper_ids).fetchall()

    return [(row['paper_id'], deserialize_embedding(row['embedding'])) for row in rows]


def get_all_paper_embeddings(
    conn: sqlite3.Connection,
) -> list[tuple[str, list[float]]]:
    """Get all paper embeddings."""
    rows = conn.execute(
        "SELECT paper_id, embedding FROM paper_embeddings"
    ).fetchall()
    return [(row['paper_id'], deserialize_embedding(row['embedding'])) for row in rows]


# --- Claim Embeddings ---

def save_claim_embedding(
    conn: sqlite3.Connection,
    claim_uri: str,
    embedding: list[float],
    model: str,
) -> None:
    """Save claim embedding."""
    conn.execute("""
        INSERT OR REPLACE INTO claim_embeddings (claim_uri, embedding, model, created_at)
        VALUES (?, ?, ?, ?)
    """, (claim_uri, serialize_embedding(embedding), model, datetime.now().isoformat()))


def get_claim_embedding(
    conn: sqlite3.Connection,
    claim_uri: str,
) -> list[float] | None:
    """Get claim embedding."""
    row = conn.execute(
        "SELECT embedding FROM claim_embeddings WHERE claim_uri = ?",
        (claim_uri,)
    ).fetchone()
    if not row:
        return None
    return deserialize_embedding(row['embedding'])


def get_claim_embeddings(
    conn: sqlite3.Connection,
    claim_uris: list[str],
) -> list[tuple[str, list[float]]]:
    """Get embeddings for multiple claims."""
    if not claim_uris:
        return []

    placeholders = ','.join('?' * len(claim_uris))
    rows = conn.execute(f"""
        SELECT claim_uri, embedding FROM claim_embeddings
        WHERE claim_uri IN ({placeholders})
    """, claim_uris).fetchall()

    return [(row['claim_uri'], deserialize_embedding(row['embedding'])) for row in rows]


# --- Concept Embeddings ---

def save_concept_embedding(
    conn: sqlite3.Connection,
    concept_uri: str,
    embedding: list[float],
    model: str,
) -> None:
    """Save concept embedding."""
    conn.execute("""
        INSERT OR REPLACE INTO concept_embeddings (concept_uri, embedding, model, created_at)
        VALUES (?, ?, ?, ?)
    """, (concept_uri, serialize_embedding(embedding), model, datetime.now().isoformat()))


def get_concept_embedding(
    conn: sqlite3.Connection,
    concept_uri: str,
) -> list[float] | None:
    """Get concept embedding."""
    row = conn.execute(
        "SELECT embedding FROM concept_embeddings WHERE concept_uri = ?",
        (concept_uri,)
    ).fetchone()
    if not row:
        return None
    return deserialize_embedding(row['embedding'])


def get_all_concept_embeddings(
    conn: sqlite3.Connection,
) -> list[tuple[str, list[float]]]:
    """Get all concept embeddings."""
    rows = conn.execute(
        "SELECT concept_uri, embedding FROM concept_embeddings"
    ).fetchall()
    return [(row['concept_uri'], deserialize_embedding(row['embedding'])) for row in rows]


def delete_concept_embedding(
    conn: sqlite3.Connection,
    concept_uri: str,
) -> bool:
    """Delete concept embedding (after merge).

    Returns:
        True if deleted, False if not found
    """
    cursor = conn.execute(
        "DELETE FROM concept_embeddings WHERE concept_uri = ?",
        (concept_uri,)
    )
    return cursor.rowcount > 0


def has_concept_embedding(
    conn: sqlite3.Connection,
    concept_uri: str,
) -> bool:
    """Check if concept has an embedding (without fetching the full embedding)."""
    row = conn.execute(
        "SELECT 1 FROM concept_embeddings WHERE concept_uri = ?",
        (concept_uri,)
    ).fetchone()
    return row is not None


# --- Seed Centroid ---

def save_seed_centroid(
    conn: sqlite3.Connection,
    embedding: list[float],
    model: str,
    paper_ids: list[str],
) -> None:
    """Save seed centroid (singleton - only one allowed)."""
    conn.execute("""
        INSERT OR REPLACE INTO seed_centroid (id, embedding, model, paper_ids, created_at)
        VALUES (1, ?, ?, ?, ?)
    """, (
        serialize_embedding(embedding),
        model,
        json.dumps(paper_ids),
        datetime.now().isoformat()
    ))


def get_seed_centroid(
    conn: sqlite3.Connection,
) -> tuple[list[float], str, list[str]] | None:
    """Get seed centroid.

    Returns:
        Tuple of (embedding, model, paper_ids) or None if not set
    """
    row = conn.execute(
        "SELECT embedding, model, paper_ids FROM seed_centroid WHERE id = 1"
    ).fetchone()
    if not row:
        return None
    return (
        deserialize_embedding(row['embedding']),
        row['model'],
        json.loads(row['paper_ids'])
    )


def has_seed_centroid(conn: sqlite3.Connection) -> bool:
    """Check if seed centroid exists."""
    row = conn.execute(
        "SELECT 1 FROM seed_centroid WHERE id = 1"
    ).fetchone()
    return row is not None
