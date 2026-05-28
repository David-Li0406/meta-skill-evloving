"""Data models for the collector."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PaperStatus(str, Enum):
    """Paper collection status."""
    SEED = 'seed'
    COLLECTED = 'collected'


class QueueStatus(str, Enum):
    """Queue item status."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    DONE = 'done'
    SKIPPED = 'skipped'


class Relation(str, Enum):
    """Paper relationship type (how discovered)."""
    REFERENCE = 'reference'
    CITATION = 'citation'


class ClaimRelation(str, Enum):
    """Claim relationship type."""
    EXTENDS = 'extends'
    REFUTES = 'refutes'
    SUPPORTS = 'supports'


class ConceptRelation(str, Enum):
    """Concept relationship type."""
    BROADER = 'broader'
    PART_OF = 'partOf'
    DEPENDS_ON = 'dependsOn'


class ConceptMatchType(str, Enum):
    """How a concept was matched during deduplication."""
    EXACT_WITH_CONTEXT = 'exact_with_context'
    EMBEDDING = 'embedding'
    EMBEDDING_LLM = 'embedding_llm'
    NEW = 'new'


@dataclass
class Author:
    """Paper author."""
    name: str
    author_id: str | None = None  # Semantic Scholar Author ID
    orcid: str | None = None  # ORCID


@dataclass
class Venue:
    """Publication venue."""
    name: str
    venue_id: str | None = None  # Semantic Scholar Venue ID
    venue_type: str | None = None  # 'conference' | 'journal' | 'preprint' | 'workshop'


@dataclass
class Paper:
    """Paper metadata."""
    id: str  # Semantic Scholar Paper ID
    title: str
    authors: list[Author]
    citation_count: int = 0
    year: int | None = None
    abstract: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    venue: Venue | None = None
    references: list[str] = field(default_factory=list)  # Paper IDs
    citations: list[str] = field(default_factory=list)  # Paper IDs
    status: PaperStatus = PaperStatus.COLLECTED


@dataclass
class Config:
    """Collection configuration."""
    seed_ids: list[str]
    max_papers: int = 2000

    def to_dict(self) -> dict:
        return {
            'seed_ids': self.seed_ids,
            'max_papers': self.max_papers,
        }


# --- Database return types ---

@dataclass
class QueueCandidate:
    """A candidate paper from the queue."""
    id: str
    score: float
    source_id: str | None
    relation: str | None
    status: str


@dataclass
class PaperRow:
    """Paper data for enrichment/linking."""
    id: str
    kg2_uri: str
    title: str
    abstract: str | None = None
    year: int | None = None
    authors: str | None = None  # JSON string
    refs: str | None = None  # JSON string

    @classmethod
    def from_row(cls, row) -> PaperRow:
        """Construct PaperRow from a database row."""
        d = dict(row)
        return cls(
            id=d['id'],
            kg2_uri=d['kg2_uri'],
            title=d['title'],
            abstract=d.get('abstract'),
            year=d.get('year'),
            authors=d.get('authors'),
            refs=d.get('refs'),
        )


@dataclass
class EnrichedRef:
    """Reference paper that has been enriched."""
    id: str
    kg2_uri: str
    title: str
    year: int | None


@dataclass
class DbStats:
    """Database statistics."""
    papers: dict[str, int]
    queue: dict[str, int]
    total_papers: int
    pending_cites: int
    enriched: int
    unenriched: int
    linked: int
    unlinked: int
    contexts_fetched: int = 0
    contexts_pending: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'papers': self.papers,
            'queue': self.queue,
            'total_papers': self.total_papers,
            'pending_cites': self.pending_cites,
            'enriched': self.enriched,
            'unenriched': self.unenriched,
            'linked': self.linked,
            'unlinked': self.unlinked,
            'contexts_fetched': self.contexts_fetched,
            'contexts_pending': self.contexts_pending,
        }
