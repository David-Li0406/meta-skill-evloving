"""Clustering module for skill deduplication and merging."""

from .embedding import EmbeddingService
from .dbscan import DBSCANClustering, DBSCANClusterer
from .merger import SkillMerger

__all__ = [
    "EmbeddingService",
    "DBSCANClustering",
    "DBSCANClusterer",
    "SkillMerger",
]
