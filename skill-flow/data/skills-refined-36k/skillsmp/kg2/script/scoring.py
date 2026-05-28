"""Scoring functions for paper prioritization."""

from __future__ import annotations

import math
from datetime import datetime
from typing import TYPE_CHECKING

from .embeddings import cosine_similarity
from .models import PaperStatus, Relation

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .models import Paper


def _current_year() -> int:
    """Get current year."""
    return datetime.now().year


def normalize_log(value: float, max_val: float) -> float:
    """Normalize value to 0-1 range using log scale.

    - value <= 1 -> 0.0
    - value = max_val -> 1.0
    """
    if value <= 1:
        return 0.0
    if max_val <= 1:
        return 0.0
    return min(1.0, math.log10(value) / math.log10(max_val))


def citation_impact_factor(
    citation_count: int, year: int | None, *, current_year: int | None = None
) -> float:
    """Calculate a multiplier based on citation performance.

    Uses age-adjusted citations compared to expected baseline.
    Returns a factor that penalizes low-citation papers and rewards high-citation ones.

    Args:
        citation_count: Number of citations
        year: Publication year (None treated as current year)
        current_year: Override for current year (for testing)

    Returns:
        Multiplier in range [0.2, 1.5]:
        - 0.2: Very low citations (e.g., 0 citations)
        - 0.5: Below average
        - 1.0: Average (~10 citations/year)
        - 1.5: High impact (>50 citations/year)
    """
    now_year = current_year if current_year is not None else _current_year()
    paper_year = year if year else now_year
    age = max(1, now_year - paper_year + 1)

    citations_per_year = citation_count / age

    # Sigmoid centered on expected citations/year
    # 10 citations/year is roughly "average" for a well-cited ML paper
    expected = 10.0
    # Scale of 15 gives smooth transition: ~0.3 factor at 0 cit/yr, ~1.0 at 10, ~1.3 at 25
    scale = 15.0

    x = (citations_per_year - expected) / scale
    sigmoid = 1 / (1 + math.exp(-x))

    # Output range [0.2, 1.5]: papers with few citations are penalized (0.2x),
    # average papers neutral (1.0x), highly-cited papers boosted (up to 1.5x)
    min_factor = 0.2
    max_factor = 1.5
    factor = min_factor + sigmoid * (max_factor - min_factor)

    return factor


def count_connections(paper: Paper, target_ids: set[str]) -> int:
    """Count how many citation relationships paper has with target_ids."""
    refs = set(paper.references) & target_ids
    cits = set(paper.citations) & target_ids
    return len(refs) + len(cits)


def semantic_similarity_score(
    paper_embedding: Sequence[float] | None,
    centroid: Sequence[float] | None,
) -> float:
    """Compute semantic similarity score between paper and seed centroid.

    Args:
        paper_embedding: Paper's embedding vector (or None if not available)
        centroid: Seed centroid embedding (or None if not computed)

    Returns:
        Similarity score in range [0, 1], or 0.5 (neutral) if embeddings unavailable
    """
    if paper_embedding is None or centroid is None:
        return 0.5  # Neutral score when embeddings unavailable

    # cosine_similarity returns [-1, 1], map to [0, 1]
    sim = cosine_similarity(paper_embedding, centroid)
    return (sim + 1) / 2


def estimate_score(source_paper: Paper, relation: Relation) -> float:
    """Estimate score before API fetch. Uses only source paper info.

    Args:
        source_paper: The paper from which this candidate was discovered
        relation: How the candidate was discovered (reference or citation)
    """
    score = 0.5  # Base score

    # Papers discovered from seeds are more likely important
    if source_paper.status == PaperStatus.SEED:
        score += 0.3

    # References (backward) slightly preferred over citations (forward)
    # Reason: references are explicitly chosen by authors
    if relation == Relation.REFERENCE:
        score += 0.1

    return score


def compute_score(
    paper: Paper,
    seed_ids: set[str],
    collected_ids: set[str],
    source_id: str | None = None,
    relation: str | None = None,
    paper_embedding: Sequence[float] | None = None,
    seed_centroid: Sequence[float] | None = None,
    *,
    current_year: int | None = None,
) -> float:
    """Compute actual score after API fetch.

    Args:
        paper: The paper to score
        seed_ids: Set of seed paper IDs
        collected_ids: Set of all collected paper IDs
        source_id: ID of paper that led to discovering this one
        relation: How it was discovered ('reference' or 'citation')
        paper_embedding: Optional paper embedding for semantic scoring
        seed_centroid: Optional seed centroid for semantic scoring
        current_year: Override for current year (for testing)
    """
    now_year = current_year if current_year is not None else _current_year()
    score = 0.0

    # Scoring weights sum to 1.0 before impact multiplier:
    # - Citation performance: 0.2 (favor well-cited papers)
    # - Seed proximity: 0.3 (stay close to starting point)
    # - Network density: 0.15 (prefer papers connected to collection)
    # - Bidirectional: 0.1 (bonus for mutual citations with seeds)
    # - Semantic similarity: 0.25 (stay on-topic)

    # 1. Age-normalized citation count
    if paper.year:
        age = now_year - paper.year + 1
        citations_per_year = paper.citation_count / age
        score += 0.2 * normalize_log(citations_per_year, max_val=100)

    # 2. Seed connection strength
    seed_connections = count_connections(paper, seed_ids) if seed_ids else 0
    if source_id and source_id in seed_ids:
        seed_connections += 1
    if seed_ids:
        score += 0.3 * min(1.0, seed_connections / len(seed_ids))

    # 3. Connection density with collected papers (saturates at 5 connections)
    collected_connections = count_connections(paper, collected_ids) if collected_ids else 0
    if source_id and source_id in collected_ids:
        collected_connections += 1
    if collected_ids:
        score += 0.15 * min(1.0, collected_connections / 5)

    # 4. Bidirectional citation bonus (paper cites AND is cited by seeds)
    refs_set = set(paper.references)
    cits_set = set(paper.citations)
    if (refs_set & seed_ids) and (cits_set & seed_ids):
        score += 0.1

    # 5. Semantic similarity to seeds (keeps collection on topic)
    sem_score = semantic_similarity_score(paper_embedding, seed_centroid)
    score += 0.25 * sem_score

    # 6. Apply citation impact factor (0.2x to 1.5x multiplier)
    impact = citation_impact_factor(paper.citation_count, paper.year, current_year=now_year)
    score *= impact

    return score
