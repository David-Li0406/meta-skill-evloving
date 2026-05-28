"""Embedding utilities - pure functions for vector operations.

This module provides pure functions for working with embeddings.
All I/O (API calls, database) is handled elsewhere.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def format_concept_for_embedding(name: str, description: str | None) -> str:
    """Format concept name and description for embedding.

    Args:
        name: Concept name
        description: Optional concept description

    Returns:
        Formatted string suitable for embedding
    """
    if description:
        return f"{name}: {description}"
    return name


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between two vectors.

    Args:
        a: First vector
        b: Second vector (must be same length as a)

    Returns:
        Cosine similarity in range [-1, 1]

    Raises:
        ValueError: If vectors have different lengths or are empty
    """
    if len(a) != len(b):
        raise ValueError(f"Vector length mismatch: {len(a)} vs {len(b)}")
    if len(a) == 0:
        raise ValueError("Empty vectors")

    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def compute_centroid(vectors: list[Sequence[float]]) -> list[float]:
    """Compute centroid (mean) of a list of vectors.

    Args:
        vectors: List of vectors (all must be same length)

    Returns:
        Centroid vector

    Raises:
        ValueError: If vectors list is empty or vectors have different lengths
    """
    if not vectors:
        raise ValueError("Empty vector list")

    dim = len(vectors[0])
    if any(len(v) != dim for v in vectors):
        raise ValueError("All vectors must have same dimension")

    n = len(vectors)
    centroid = [0.0] * dim
    for v in vectors:
        for i, x in enumerate(v):
            centroid[i] += x / n

    return centroid


def normalize_vector(v: Sequence[float]) -> list[float]:
    """Normalize vector to unit length.

    Args:
        v: Input vector

    Returns:
        Unit vector (same direction, length 1)
    """
    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0:
        return [0.0] * len(v)
    return [x / norm for x in v]


def find_similar(
    query: Sequence[float],
    candidates: list[tuple[str, Sequence[float]]],
    threshold: float = 0.5,
    top_k: int | None = None,
) -> list[tuple[str, float]]:
    """Find candidates similar to query vector.

    Args:
        query: Query vector
        candidates: List of (id, vector) tuples
        threshold: Minimum similarity threshold
        top_k: Maximum results to return (None = all above threshold)

    Returns:
        List of (id, similarity) tuples, sorted by similarity descending
    """
    results = []
    for cand_id, cand_vec in candidates:
        sim = cosine_similarity(query, cand_vec)
        if sim >= threshold:
            results.append((cand_id, sim))

    results.sort(key=lambda x: x[1], reverse=True)

    if top_k is not None:
        results = results[:top_k]

    return results


def find_similar_pairs(
    group_a: list[tuple[str, Sequence[float]]],
    group_b: list[tuple[str, Sequence[float]]],
    threshold: float = 0.5,
) -> list[tuple[str, str, float]]:
    """Find similar pairs between two groups of vectors.

    Args:
        group_a: First group of (id, vector) tuples
        group_b: Second group of (id, vector) tuples
        threshold: Minimum similarity threshold

    Returns:
        List of (id_a, id_b, similarity) tuples, sorted by similarity descending
    """
    pairs = []
    for id_a, vec_a in group_a:
        for id_b, vec_b in group_b:
            sim = cosine_similarity(vec_a, vec_b)
            if sim >= threshold:
                pairs.append((id_a, id_b, sim))

    pairs.sort(key=lambda x: x[2], reverse=True)
    return pairs


def find_similar_pairs_within(
    items: list[tuple[str, Sequence[float]]],
    threshold: float = 0.5,
) -> list[tuple[str, str, float]]:
    """Find similar pairs within a single group of vectors.

    Compares each item with all items after it (avoiding duplicates).

    Args:
        items: List of (id, vector) tuples
        threshold: Minimum similarity threshold

    Returns:
        List of (id_a, id_b, similarity) tuples, sorted by similarity descending
    """
    pairs = []
    for i, (id_a, vec_a) in enumerate(items):
        for id_b, vec_b in items[i + 1:]:
            sim = cosine_similarity(vec_a, vec_b)
            if sim >= threshold:
                pairs.append((id_a, id_b, sim))

    pairs.sort(key=lambda x: x[2], reverse=True)
    return pairs


def find_nearest_above_threshold(
    query: Sequence[float],
    candidates: list[tuple[str, Sequence[float]]],
    threshold: float,
) -> tuple[str, float] | None:
    """Find the nearest candidate above a similarity threshold.

    Useful for concept deduplication - find if similar concept exists.

    Args:
        query: Query vector
        candidates: List of (id, vector) tuples
        threshold: Minimum similarity threshold

    Returns:
        (id, similarity) of nearest match, or None if none above threshold
    """
    best_id = None
    best_sim = threshold

    for cand_id, cand_vec in candidates:
        sim = cosine_similarity(query, cand_vec)
        if sim > best_sim:
            best_sim = sim
            best_id = cand_id

    if best_id is None:
        return None
    return (best_id, best_sim)


def serialize_embedding(embedding: Sequence[float]) -> bytes:
    """Serialize embedding to bytes for SQLite storage.

    Uses simple format: 4-byte floats in sequence.

    Args:
        embedding: Vector to serialize

    Returns:
        Bytes representation
    """
    import struct
    return struct.pack(f'{len(embedding)}f', *embedding)


def deserialize_embedding(data: bytes) -> list[float]:
    """Deserialize embedding from bytes.

    Args:
        data: Bytes from serialize_embedding

    Returns:
        Vector as list of floats
    """
    import struct
    count = len(data) // 4
    return list(struct.unpack(f'{count}f', data))
