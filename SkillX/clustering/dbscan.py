"""DBSCAN clustering for skill deduplication."""

import logging
from typing import List, Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class DBSCANClustering:
    """
    DBSCAN clustering with cosine similarity.

    Used for grouping similar skills for merging.
    """

    def __init__(
        self,
        eps: float = 0.10,  # 1 - cosine_similarity_threshold (0.90)
        min_samples: int = 1,
        metric: str = "cosine",
        embedding_service=None
    ):
        """
        Initialize DBSCAN clustering.

        Args:
            eps: Maximum distance between samples (1 - similarity_threshold)
            min_samples: Minimum samples per cluster
            metric: Distance metric (default: cosine)
            embedding_service: Optional EmbeddingService instance
        """
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.embedding_service = embedding_service

    def fit(self, embeddings: np.ndarray) -> List[List[int]]:
        """
        Cluster embeddings using DBSCAN.

        Args:
            embeddings: Numpy array of embeddings (n_samples, n_features)

        Returns:
            List of clusters, each cluster is a list of indices
        """
        try:
            from sklearn.cluster import DBSCAN
            from sklearn.metrics.pairwise import cosine_distances

            # Compute cosine distances
            distances = cosine_distances(embeddings)

            # Run DBSCAN
            clustering = DBSCAN(
                eps=self.eps,
                min_samples=self.min_samples,
                metric='precomputed'
            ).fit(distances)

            # Group by cluster
            clusters = {}
            for idx, label in enumerate(clustering.labels_):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(idx)

            # Convert to list (noise points get their own cluster)
            result = []
            for label, indices in clusters.items():
                if label == -1:
                    # Noise points - each as separate cluster
                    for idx in indices:
                        result.append([idx])
                else:
                    result.append(indices)

            logger.info(f"Created {len(result)} clusters from {len(embeddings)} items")
            return result

        except ImportError:
            logger.error("sklearn not installed, using simple grouping")
            return [[i] for i in range(len(embeddings))]

    def cluster_skills(
        self,
        skills: List[Dict],
        embeddings: np.ndarray
    ) -> List[List[Dict]]:
        """
        Cluster skills based on their embeddings.

        Args:
            skills: List of skill dictionaries
            embeddings: Corresponding embeddings

        Returns:
            List of skill clusters
        """
        cluster_indices = self.fit(embeddings)

        clusters = []
        for indices in cluster_indices:
            cluster = [skills[i] for i in indices]
            clusters.append(cluster)

        return clusters

    async def cluster_async(
        self,
        skills: List[Dict]
    ) -> Dict[int, List[int]]:
        """
        Async clustering method for pipeline integration.

        Args:
            skills: List of skill dictionaries with 'embedding_text' field

        Returns:
            Dictionary mapping cluster_id to list of skill indices
        """
        if not skills:
            return {}

        # Get or create embedding service
        if self.embedding_service is None:
            from .embedding import EmbeddingService
            self.embedding_service = EmbeddingService()

        # Generate embeddings
        embeddings = await self.embedding_service.embed_batch(
            [s.get("embedding_text", "") for s in skills],
            show_progress=True
        )

        # Run DBSCAN clustering
        cluster_indices = self.fit(embeddings)

        # Convert to dict format: {cluster_id: [indices]}
        result = {}
        for cluster_id, indices in enumerate(cluster_indices):
            result[cluster_id] = indices

        logger.info(f"Clustered {len(skills)} skills into {len(result)} groups")
        return result


# Alias for backward compatibility
DBSCANClusterer = DBSCANClustering
