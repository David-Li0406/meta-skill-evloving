"""DBSCAN clustering over pre-computed cosine distances.

Mirrors SkillX/clustering/dbscan.py — same eps semantics (0.10 ≈ 0.90
cosine similarity), min_samples=1 so noise → singletons.
"""

from __future__ import annotations

import logging

import numpy as np
from sklearn.cluster import DBSCAN

logger = logging.getLogger(__name__)


def cluster_skills(
    embeddings: np.ndarray,
    eps: float = 0.10,
) -> list[list[int]]:
    """Return clusters of row indices in ``embeddings``.

    Assumes ``embeddings`` are L2-normalized (skill-flow's FAISS index
    stores normalized vectors). Cosine distance = 1 - dot product.
    """
    n = embeddings.shape[0]
    if n == 0:
        return []
    if n == 1:
        return [[0]]

    sim = embeddings @ embeddings.T
    distances = np.clip(1.0 - sim, 0.0, 2.0)

    dbscan = DBSCAN(eps=eps, min_samples=1, metric="precomputed")
    labels = dbscan.fit_predict(distances)

    by_label: dict[int, list[int]] = {}
    next_singleton = max(int(labels.max()), -1) + 1
    for idx, label in enumerate(labels):
        lab = int(label)
        if lab == -1:
            lab = next_singleton
            next_singleton += 1
        by_label.setdefault(lab, []).append(idx)

    clusters = sorted(by_label.values(), key=lambda c: (-len(c), c[0]))
    sizes = [len(c) for c in clusters if len(c) >= 2]
    logger.info(
        "DBSCAN(eps=%.2f) → %d clusters (%d with size>=2, sizes=%s)",
        eps,
        len(clusters),
        len(sizes),
        sizes[:10],
    )
    return clusters
