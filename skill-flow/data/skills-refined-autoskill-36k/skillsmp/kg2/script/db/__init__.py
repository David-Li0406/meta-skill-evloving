"""SQLite database operations.

This package provides the Database class for managing paper collection state.

Usage:
    from .db import Database

    db = Database("papers.db")
    db.insert_paper(paper, kg2_uri)
    db.commit()
"""

from __future__ import annotations

import contextlib
import logging
import random
import sqlite3
import time
from typing import Any

from ..constants import DB_BUSY_TIMEOUT_MS, DB_TIMEOUT_SECONDS
from ..models import Config, DbStats, EnrichedRef, Paper, PaperRow, QueueCandidate
from . import citation_contexts as citation_ctx_ops
from . import config as config_ops
from . import embeddings as embedding_ops
from . import enrichment as enrichment_ops
from . import papers as paper_ops
from . import pending_cites as pending_cites_ops
from . import queue as queue_ops
from . import stats as stats_ops
from .schema import MIGRATIONS, SCHEMA

logger = logging.getLogger(__name__)

# Retry settings for locked database
MAX_RETRIES = 10
INITIAL_RETRY_DELAY = 1.0  # seconds
MAX_RETRY_DELAY = 30.0  # cap the delay


def _retry_on_locked(func):
    """Decorator to retry database operations on lock."""
    def wrapper(*args, **kwargs):
        delay = INITIAL_RETRY_DELAY
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if "locked" in str(e) and attempt < MAX_RETRIES - 1:
                    # Add jitter to avoid thundering herd
                    jittered_delay = delay * (0.5 + random.random())
                    logger.warning(
                        "Database locked (attempt %d/%d), retrying in %.1fs...",
                        attempt + 1, MAX_RETRIES, jittered_delay
                    )
                    time.sleep(jittered_delay)
                    delay = min(delay * 2, MAX_RETRY_DELAY)
                else:
                    logger.error("Database locked after %d attempts, giving up", attempt + 1)
                    raise
    return wrapper


class RetryConnection:
    """Wrapper around sqlite3.Connection that retries on lock."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def __getattr__(self, name):
        return getattr(self._conn, name)

    @_retry_on_locked
    def execute(self, sql, parameters=()):
        return self._conn.execute(sql, parameters)

    @_retry_on_locked
    def executemany(self, sql, parameters):
        return self._conn.executemany(sql, parameters)

    @_retry_on_locked
    def executescript(self, sql):
        return self._conn.executescript(sql)

    @_retry_on_locked
    def commit(self):
        return self._conn.commit()


class Database:
    """SQLite database wrapper for paper collection state."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        raw_conn = sqlite3.connect(db_path, timeout=DB_TIMEOUT_SECONDS)
        raw_conn.row_factory = sqlite3.Row
        raw_conn.execute("PRAGMA journal_mode=WAL")
        raw_conn.execute(f"PRAGMA busy_timeout={DB_BUSY_TIMEOUT_MS}")
        self.conn = RetryConnection(raw_conn)
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema and run migrations."""
        self.conn.executescript(SCHEMA)
        # Run migrations for existing databases
        for migration in MIGRATIONS:
            with contextlib.suppress(sqlite3.OperationalError):
                self.conn.execute(migration)
        self.conn.commit()

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()

    def commit(self) -> None:
        """Commit current transaction."""
        self.conn.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        self.conn.rollback()

    # --- Config ---

    def save_config(self, key: str, value: Any) -> None:
        """Save config value."""
        config_ops.save_config(self.conn, key, value)

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get config value."""
        return config_ops.get_config(self.conn, key, default)

    def load_config(self) -> Config | None:
        """Load full config. Returns None if not initialized."""
        return config_ops.load_config(self.conn)

    def save_full_config(self, config: Config) -> None:
        """Save full config."""
        config_ops.save_full_config(self.conn, config)

    # --- Papers ---

    def paper_exists(self, paper_id: str) -> bool:
        """Check if paper exists."""
        return paper_ops.paper_exists(self.conn, paper_id)

    def get_kg2_uri(self, paper_id: str) -> str | None:
        """Get kg2 URI for paper."""
        return paper_ops.get_kg2_uri(self.conn, paper_id)

    def insert_paper(self, paper: Paper, kg2_uri: str) -> None:
        """Insert paper into database."""
        paper_ops.insert_paper(self.conn, paper, kg2_uri)

    def load_paper(self, paper_id: str) -> Paper | None:
        """Load paper from database."""
        return paper_ops.load_paper(self.conn, paper_id)

    def count_papers(self) -> int:
        """Count total papers."""
        return paper_ops.count_papers(self.conn)

    def get_seed_ids(self) -> set[str]:
        """Get set of seed paper IDs."""
        return paper_ops.get_seed_ids(self.conn)

    def get_collected_ids(self) -> set[str]:
        """Get set of all collected paper IDs."""
        return paper_ops.get_collected_ids(self.conn)

    def iter_papers_without_abstract(self):
        """Iterate over papers missing abstracts."""
        return paper_ops.iter_papers_without_abstract(self.conn)

    def update_abstract(self, paper_id: str, abstract: str) -> None:
        """Update paper's abstract."""
        paper_ops.update_abstract(self.conn, paper_id, abstract)

    # --- Queue ---

    def queue_exists(self, paper_id: str) -> bool:
        """Check if paper is in queue."""
        return queue_ops.queue_exists(self.conn, paper_id)

    def enqueue(self, paper_id: str, score: float, source_id: str,
                relation: str) -> None:
        """Add paper to queue if not already present."""
        queue_ops.enqueue(self.conn, paper_id, score, source_id, relation)

    def next_candidate(self) -> QueueCandidate | None:
        """Get highest-score pending candidate."""
        return queue_ops.next_candidate(self.conn)

    def update_queue_status(self, paper_id: str, status: str,
                            skip_reason: str | None = None) -> None:
        """Update queue item status."""
        queue_ops.update_queue_status(self.conn, paper_id, status, skip_reason)

    def reset_processing_to_pending(self) -> int:
        """Reset all 'processing' queue items back to 'pending'."""
        return queue_ops.reset_processing_to_pending(self.conn)

    # --- Pending Cites ---

    def add_pending_cites(self, citing_id: str, cited_id: str) -> None:
        """Add pending citation relationship."""
        pending_cites_ops.add_pending_cites(self.conn, citing_id, cited_id)

    def get_pending_cites_to(self, cited_id: str) -> list[str]:
        """Get papers waiting to cite this paper."""
        return pending_cites_ops.get_pending_cites_to(self.conn, cited_id)

    def delete_pending_cites(self, citing_id: str, cited_id: str) -> None:
        """Delete pending citation relationship."""
        pending_cites_ops.delete_pending_cites(self.conn, citing_id, cited_id)

    # --- Statistics ---

    def stats(self) -> DbStats:
        """Get collection statistics."""
        return stats_ops.stats(self.conn)

    # --- Enrichment ---

    def claim_unenriched_paper(self) -> PaperRow | None:
        """Atomically claim next unenriched paper (parallel-safe)."""
        return enrichment_ops.claim_unenriched_paper(self.conn)

    def next_unenriched_paper(self) -> PaperRow | None:
        """Get next paper that hasn't been enriched (oldest first).

        DEPRECATED: Use claim_unenriched_paper() for parallel-safe processing.
        """
        return enrichment_ops.next_unenriched_paper(self.conn)

    def mark_enriched(self, paper_id: str) -> None:
        """Mark paper as enriched."""
        enrichment_ops.mark_enriched(self.conn, paper_id)

    def mark_enriched_skipped(self, paper_id: str, reason: str) -> None:
        """Mark paper as enriched but skipped, with a reason."""
        enrichment_ops.mark_enriched_skipped(self.conn, paper_id, reason)

    def get_enriched_refs(self, ref_ids: list[str]) -> list[EnrichedRef]:
        """Get enriched papers from a list of reference IDs."""
        return enrichment_ops.get_enriched_refs(self.conn, ref_ids)

    def claim_unlinked_paper(self) -> PaperRow | None:
        """Atomically claim next unlinked paper (parallel-safe)."""
        return enrichment_ops.claim_unlinked_paper(self.conn)

    def next_unlinked_paper(self) -> PaperRow | None:
        """Get next enriched paper that hasn't been link-checked (oldest first).

        DEPRECATED: Use claim_unlinked_paper() for parallel-safe processing.
        """
        return enrichment_ops.next_unlinked_paper(self.conn)

    def mark_link_checked(self, paper_id: str) -> None:
        """Mark paper as link-checked."""
        enrichment_ops.mark_link_checked(self.conn, paper_id)

    def reset_link_checked_for_citers(self, cited_id: str) -> int:
        """Reset link_checked_at for papers that cite the given paper."""
        return enrichment_ops.reset_link_checked_for_citers(self.conn, cited_id)

    def reset_stale_enrichment(self, timeout_minutes: int = 30) -> int:
        """Reset papers stuck in enrichment processing (crashed workers)."""
        return enrichment_ops.reset_stale_enrichment(self.conn, timeout_minutes)

    def reset_stale_linking(self, timeout_minutes: int = 30) -> int:
        """Reset papers stuck in linking processing (crashed workers)."""
        return enrichment_ops.reset_stale_linking(self.conn, timeout_minutes)

    # --- Citation Contexts ---

    def save_citation_contexts(self, citing_id: str, contexts: list[dict]) -> int:
        """Save citation contexts for a paper's references."""
        return citation_ctx_ops.save_citation_contexts(self.conn, citing_id, contexts)

    def get_citation_context(self, citing_id: str, cited_id: str) -> dict | None:
        """Get citation context between two papers."""
        return citation_ctx_ops.get_citation_context(self.conn, citing_id, cited_id)

    def get_citation_contexts_for_paper(self, citing_id: str) -> dict[str, dict]:
        """Get all citation contexts for a paper's references."""
        return citation_ctx_ops.get_citation_contexts_for_paper(self.conn, citing_id)

    def mark_contexts_fetched(self, paper_id: str) -> None:
        """Mark that citation contexts have been fetched for a paper."""
        citation_ctx_ops.mark_contexts_fetched(self.conn, paper_id)

    def get_papers_needing_contexts(self, limit: int = 100) -> list[str]:
        """Get paper IDs that need citation contexts fetched."""
        return citation_ctx_ops.get_papers_needing_contexts(self.conn, limit)

    # --- Embeddings ---

    def save_paper_embedding(self, paper_id: str, embedding: list[float],
                             model: str) -> None:
        """Save paper embedding."""
        embedding_ops.save_paper_embedding(self.conn, paper_id, embedding, model)

    def get_paper_embedding(self, paper_id: str) -> list[float] | None:
        """Get paper embedding."""
        return embedding_ops.get_paper_embedding(self.conn, paper_id)

    def get_paper_embeddings(self, paper_ids: list[str]) -> list[tuple[str, list[float]]]:
        """Get embeddings for multiple papers."""
        return embedding_ops.get_paper_embeddings(self.conn, paper_ids)

    def get_all_paper_embeddings(self) -> list[tuple[str, list[float]]]:
        """Get all paper embeddings."""
        return embedding_ops.get_all_paper_embeddings(self.conn)

    def save_claim_embedding(self, claim_uri: str, embedding: list[float],
                             model: str) -> None:
        """Save claim embedding."""
        embedding_ops.save_claim_embedding(self.conn, claim_uri, embedding, model)

    def get_claim_embedding(self, claim_uri: str) -> list[float] | None:
        """Get claim embedding."""
        return embedding_ops.get_claim_embedding(self.conn, claim_uri)

    def get_claim_embeddings(self, claim_uris: list[str]) -> list[tuple[str, list[float]]]:
        """Get embeddings for multiple claims."""
        return embedding_ops.get_claim_embeddings(self.conn, claim_uris)

    def save_concept_embedding(self, concept_uri: str, embedding: list[float],
                               model: str) -> None:
        """Save concept embedding."""
        embedding_ops.save_concept_embedding(self.conn, concept_uri, embedding, model)

    def get_concept_embedding(self, concept_uri: str) -> list[float] | None:
        """Get concept embedding."""
        return embedding_ops.get_concept_embedding(self.conn, concept_uri)

    def get_all_concept_embeddings(self) -> list[tuple[str, list[float]]]:
        """Get all concept embeddings."""
        return embedding_ops.get_all_concept_embeddings(self.conn)

    def delete_concept_embedding(self, concept_uri: str) -> bool:
        """Delete concept embedding (after merge)."""
        return embedding_ops.delete_concept_embedding(self.conn, concept_uri)

    def save_seed_centroid(self, embedding: list[float], model: str,
                           paper_ids: list[str]) -> None:
        """Save seed centroid."""
        embedding_ops.save_seed_centroid(self.conn, embedding, model, paper_ids)

    def get_seed_centroid(self) -> tuple[list[float], str, list[str]] | None:
        """Get seed centroid."""
        return embedding_ops.get_seed_centroid(self.conn)

    def has_seed_centroid(self) -> bool:
        """Check if seed centroid exists."""
        return embedding_ops.has_seed_centroid(self.conn)

    def has_concept_embedding(self, concept_uri: str) -> bool:
        """Check if concept has an embedding."""
        return embedding_ops.has_concept_embedding(self.conn, concept_uri)
