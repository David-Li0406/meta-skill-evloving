"""Global concept deduplication with clustering.

Algorithm:
1. Load all concepts and compute embeddings
2. Build global similarity matrix
3. Auto-merge pairs with similarity >= 0.95
4. Cluster remaining pairs with similarity 0.80-0.95
5. Verify each cluster with LLM and merge confirmed duplicates
"""

from __future__ import annotations

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from . import queries
from .constants import (
    DEDUP_MAX_CLUSTER_SIZE,
    EMBEDDING_THRESHOLD_AUTO_MERGE,
    EMBEDDING_THRESHOLD_LLM_VERIFY,
)
from .embeddings import format_concept_for_embedding
from .kg2_helpers import merge_concepts
from .turtle_builders import build_relation_turtle

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from .clients import OpenAIClient, SparqlClient
    from .embedding_cache import EmbeddingCache

logger = logging.getLogger(__name__)


@dataclass
class ConceptInfo:
    """Concept with metadata for deduplication."""
    uri: str
    name: str
    description: str | None


@dataclass
class MergeResult:
    """Result of a merge operation."""
    keep_uri: str
    keep_name: str
    removed_uri: str
    removed_name: str
    similarity: float
    method: str  # "auto" or "llm" or "llm_pairwise"


@dataclass
class RelationResult:
    """Result of a concept relation operation."""
    from_uri: str
    from_name: str
    relation: str  # "broader" | "partOf" | "dependsOn"
    to_uri: str
    to_name: str
    similarity: float


@dataclass
class ClusterVerification:
    """LLM verification result for a cluster."""
    groups: list[list[int]]  # Indices of concepts that are the same


class GlobalConceptDeduplicator:
    """Handles global deduplication of all concepts."""

    def __init__(
        self,
        sparql: SparqlClient,
        openai: OpenAIClient,
        embedding_cache: EmbeddingCache,
    ):
        self.sparql = sparql
        self.openai = openai
        self.cache = embedding_cache
        self._concepts: list[ConceptInfo] = []
        self._embeddings: NDArray[np.float32] | None = None
        self._merged_uris: set[str] = set()
        self._lock = threading.Lock()  # For thread-safe updates to _merged_uris

    def load_concepts(self) -> int:
        """Load all concepts from the graph.

        Returns:
            Number of concepts loaded
        """
        logger.info("Loading concepts from graph...")
        results = self.sparql.query(queries.get_all_concepts_with_description())
        self._concepts = [
            ConceptInfo(
                uri=row['uri']['value'],
                name=row['label']['value'],
                description=row.get('comment', {}).get('value'),
            )
            for row in results
        ]
        logger.info("Loaded %d concepts", len(self._concepts))
        return len(self._concepts)

    def compute_embeddings(self, batch_size: int = 500) -> int:
        """Compute embeddings for all concepts.

        Returns:
            Number of embeddings computed
        """
        if not self._concepts:
            return 0

        logger.info("Computing embeddings for %d concepts...", len(self._concepts))
        texts = [
            format_concept_for_embedding(c.name, c.description)
            for c in self._concepts
        ]

        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.cache.embed_batch(batch)
            all_embeddings.extend(batch_embeddings)
            if i + batch_size < len(texts):
                logger.info("  Embedded %d/%d...", i + batch_size, len(texts))

        self._embeddings = np.array(all_embeddings, dtype=np.float32)
        logger.info("Computed %d embeddings", len(self._embeddings))
        return len(self._embeddings)

    def find_similar_pairs(
        self, threshold: float = EMBEDDING_THRESHOLD_LLM_VERIFY
    ) -> list[tuple[int, int, float]]:
        """Find all pairs with similarity >= threshold.

        Returns:
            List of (idx_a, idx_b, similarity) tuples, sorted by similarity desc
        """
        if self._embeddings is None or len(self._embeddings) < 2:
            return []

        logger.info("Computing similarity matrix...")

        # Normalize embeddings
        norms = np.linalg.norm(self._embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        normalized = self._embeddings / norms

        # Compute similarity matrix (upper triangle only)
        similarity = normalized @ normalized.T

        # Find pairs above threshold (upper triangle only to avoid duplicates)
        pairs = []
        n = len(self._embeddings)
        for i in range(n):
            for j in range(i + 1, n):
                sim = float(similarity[i, j])
                if sim >= threshold:
                    pairs.append((i, j, sim))

        # Sort by similarity descending
        pairs.sort(key=lambda x: x[2], reverse=True)
        logger.info("Found %d pairs above threshold %.2f", len(pairs), threshold)
        return pairs

    def auto_merge_high_similarity(
        self, pairs: list[tuple[int, int, float]]
    ) -> list[MergeResult]:
        """Auto-merge pairs with similarity >= 0.95.

        Returns:
            List of successful merges
        """
        results = []
        high_sim_pairs = [(i, j, s) for i, j, s in pairs if s >= EMBEDDING_THRESHOLD_AUTO_MERGE]

        if not high_sim_pairs:
            return results

        logger.info("Auto-merging %d high-similarity pairs (>= 0.95)...", len(high_sim_pairs))

        for idx_a, idx_b, sim in high_sim_pairs:
            concept_a = self._concepts[idx_a]
            concept_b = self._concepts[idx_b]

            # Skip if either already merged
            if concept_a.uri in self._merged_uris or concept_b.uri in self._merged_uris:
                continue

            # Decide which to keep (prefer longer description, then alphabetical)
            keep, remove = self._choose_keep_remove(concept_a, concept_b)

            if merge_concepts(self.sparql, keep.uri, remove.uri, remove.name):
                self._merged_uris.add(remove.uri)
                results.append(MergeResult(
                    keep_uri=keep.uri,
                    keep_name=keep.name,
                    removed_uri=remove.uri,
                    removed_name=remove.name,
                    similarity=sim,
                    method="auto",
                ))
                logger.info("  Merged '%s' -> '%s' (sim=%.3f)", remove.name, keep.name, sim)

        logger.info("Auto-merged %d pairs", len(results))
        return results

    def cluster_medium_similarity(
        self, pairs: list[tuple[int, int, float]]
    ) -> list[list[int]]:
        """Cluster concepts with medium similarity (0.80-0.95) using Union-Find.

        Returns:
            List of clusters (each cluster is a list of concept indices)
        """
        # Filter to medium similarity pairs, excluding already merged
        medium_pairs = [
            (i, j, s) for i, j, s in pairs
            if EMBEDDING_THRESHOLD_LLM_VERIFY <= s < EMBEDDING_THRESHOLD_AUTO_MERGE
            and self._concepts[i].uri not in self._merged_uris
            and self._concepts[j].uri not in self._merged_uris
        ]

        if not medium_pairs:
            return []

        # Union-Find
        parent = {}

        def find(x: int) -> int:
            if x not in parent:
                parent[x] = x
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py

        # Build clusters
        for i, j, _ in medium_pairs:
            union(i, j)

        # Group by root
        clusters: dict[int, list[int]] = {}
        for idx in parent:
            root = find(idx)
            clusters.setdefault(root, []).append(idx)

        # Only return clusters with 2+ members
        result = [sorted(c) for c in clusters.values() if len(c) >= 2]
        logger.info("Found %d clusters with medium similarity", len(result))
        return result

    def verify_cluster_with_llm(self, cluster: list[int]) -> list[list[int]]:
        """Use LLM to verify which concepts in a cluster are duplicates.

        Returns:
            List of groups (each group contains indices of concepts that are the same)
        """
        if len(cluster) < 2:
            return []

        concepts = [self._concepts[i] for i in cluster]

        # Build prompt
        concept_list = "\n".join(
            f"{i+1}. {c.name}" + (f": {c.description[:100]}..." if c.description and len(c.description) > 100 else f": {c.description}" if c.description else "")
            for i, c in enumerate(concepts)
        )

        prompt = f"""These are technical concepts extracted from ML/AI research papers. Identify which concepts refer to the SAME thing and should be merged.

{concept_list}

## When to merge
- Exact synonyms: "CNN" = "Convolutional Neural Network"
- Acronym expansions: "BERT" = "Bidirectional Encoder Representations from Transformers"
- Spelling/capitalization variants: "self-attention" = "Self-Attention"

## When NOT to merge
- Related but distinct concepts: "attention mechanism" ≠ "self-attention" (one is more specific)
- Same name, different domains: "transformer" (ML architecture) ≠ "transformer" (electrical)
- Parent-child relationships: "neural network" ≠ "CNN" (CNN is a type of neural network)
- If descriptions describe different things, do NOT merge even if names are similar

## Important
Be CONSERVATIVE. When uncertain, do NOT merge. It's better to miss a duplicate than to wrongly merge distinct concepts.

Return groups of concept numbers that are definitely the same.
Example: {{"groups": [[1, 3], [2, 4]]}} means 1=3 and 2=4.
If all concepts are distinct, return {{"groups": []}}."""

        schema = {
            "type": "object",
            "properties": {
                "groups": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "description": "Groups of concept numbers that are the same"
                }
            },
            "required": ["groups"],
            "additionalProperties": False
        }

        try:
            result = self.openai.structured_completion(
                messages=[{"role": "user", "content": prompt}],
                schema=schema,
                schema_name="concept_groups",
            )
            raw_groups = result.get("groups", [])

            # Convert 1-indexed to 0-indexed and map back to original indices
            verified_groups = []
            for group in raw_groups:
                if len(group) >= 2:
                    original_indices = [cluster[num - 1] for num in group if 1 <= num <= len(cluster)]
                    if len(original_indices) >= 2:
                        verified_groups.append(original_indices)

            return verified_groups

        except Exception as e:
            logger.warning("LLM cluster verification failed: %s", e)
            return []

    def verify_pair_with_llm(self, idx_a: int, idx_b: int) -> dict[str, str | None]:
        """Analyze relationship between two concepts using LLM.

        Returns:
            Dict with 'result' (same/broader/partOf/dependsOn/none) and
            'direction' (a_to_b/b_to_a, only for relations)
        """
        concept_a = self._concepts[idx_a]
        concept_b = self._concepts[idx_b]

        desc_a = f": {concept_a.description}" if concept_a.description else ""
        desc_b = f": {concept_b.description}" if concept_b.description else ""

        prompt = f"""Analyze the relationship between these two technical concepts from ML/AI research papers.

Concept A: {concept_a.name}{desc_a}
Concept B: {concept_b.name}{desc_b}

## Possible relationships

1. **same**: Identical concepts (synonyms, acronym expansions)
   - "CNN" = "Convolutional Neural Network"
   - "BERT" = "Bidirectional Encoder Representations from Transformers"

2. **broader**: One is a more general category containing the other
   - "neural network" is broader than "CNN" (CNN is a type of neural network)
   - "optimization" is broader than "gradient descent"

3. **partOf**: One is a component/part of the other
   - "attention head" is partOf "multi-head attention"
   - "encoder" is partOf "transformer"

4. **dependsOn**: One requires/presupposes the other
   - "fine-tuning" dependsOn "pre-trained model"
   - "backpropagation" dependsOn "gradient computation"

5. **none**: No clear relationship (or too weak to assert)

## Important
- Be CONSERVATIVE. Only return a relationship if you are confident.
- If concepts are related but the relationship type is unclear, return "none".
- For "same": only if they are truly identical, not just related.
- For relations: specify direction as "a_to_b" (A is broader/partOf/dependsOn B) or "b_to_a" (B is broader/partOf/dependsOn A)."""

        schema = {
            "type": "object",
            "properties": {
                "result": {
                    "type": "string",
                    "enum": ["same", "broader", "partOf", "dependsOn", "none"],
                    "description": "The relationship type between the concepts"
                },
                "direction": {
                    "type": ["string", "null"],
                    "enum": ["a_to_b", "b_to_a", None],
                    "description": "Direction of the relationship (null for 'same' or 'none')"
                }
            },
            "required": ["result", "direction"],
            "additionalProperties": False
        }

        try:
            result = self.openai.structured_completion(
                messages=[{"role": "user", "content": prompt}],
                schema=schema,
                schema_name="concept_relationship",
            )
            return {
                "result": result.get("result", "none"),
                "direction": result.get("direction"),
            }
        except Exception as e:
            logger.warning("LLM pair verification failed: %s", e)
            return {"result": "none", "direction": None}

    def verify_large_cluster_pairwise(
        self, cluster: list[int], similarities: dict[tuple[int, int], float]
    ) -> tuple[list[MergeResult], list[RelationResult]]:
        """Verify large cluster by checking each pair individually.

        More conservative than cluster verification - only merges pairs
        that are directly confirmed by LLM. Also detects and adds relations.

        Returns:
            Tuple of (merge_results, relation_results)
        """
        merge_results = []
        relation_results = []
        related_pairs: set[tuple[str, str]] = set()  # Track pairs with relations

        # Get pairs within this cluster, sorted by similarity (highest first)
        cluster_set = set(cluster)
        cluster_pairs = [
            (i, j, s) for (i, j), s in similarities.items()
            if i in cluster_set and j in cluster_set
        ]
        cluster_pairs.sort(key=lambda x: x[2], reverse=True)

        for idx_a, idx_b, sim in cluster_pairs:
            concept_a = self._concepts[idx_a]
            concept_b = self._concepts[idx_b]

            # Skip if either already merged
            if concept_a.uri in self._merged_uris or concept_b.uri in self._merged_uris:
                continue

            # Analyze with LLM
            llm_result = self.verify_pair_with_llm(idx_a, idx_b)
            result_type = llm_result["result"]
            direction = llm_result["direction"]

            if result_type == "same":
                # Merge
                keep, remove = self._choose_keep_remove(concept_a, concept_b)
                if merge_concepts(self.sparql, keep.uri, remove.uri, remove.name):
                    self._merged_uris.add(remove.uri)
                    merge_results.append(MergeResult(
                        keep_uri=keep.uri,
                        keep_name=keep.name,
                        removed_uri=remove.uri,
                        removed_name=remove.name,
                        similarity=sim,
                        method="llm_pairwise",
                    ))
                    logger.info("  Merged '%s' -> '%s' (pairwise, sim=%.3f)",
                               remove.name, keep.name, sim)

            elif result_type in ("broader", "partOf", "dependsOn") and direction:
                # Add relation
                if direction == "a_to_b":
                    from_concept, to_concept = concept_a, concept_b
                else:
                    from_concept, to_concept = concept_b, concept_a

                # Skip if relation already exists between these concepts
                pair_key = (from_concept.uri, to_concept.uri)
                if pair_key in related_pairs:
                    continue
                related_pairs.add(pair_key)

                # Insert relation to KG
                turtle = build_relation_turtle(from_concept.uri, result_type, to_concept.uri)
                self.sparql.insert_turtle_silent(turtle)

                relation_results.append(RelationResult(
                    from_uri=from_concept.uri,
                    from_name=from_concept.name,
                    relation=result_type,
                    to_uri=to_concept.uri,
                    to_name=to_concept.name,
                    similarity=sim,
                ))
                logger.info("  Related '%s' -[%s]-> '%s' (sim=%.3f)",
                           from_concept.name, result_type, to_concept.name, sim)

        return merge_results, relation_results

    def find_relations_in_cluster(
        self, cluster: list[int], similarities: dict[tuple[int, int], float]
    ) -> tuple[list[MergeResult], list[RelationResult]]:
        """Find relations between non-merged concepts in a small cluster.

        Called after cluster merge verification to detect relations between
        concepts that weren't merged.

        Returns:
            Tuple of (merge_results, relation_results)
        """
        relation_results = []
        related_pairs: set[tuple[str, str]] = set()

        # Get pairs within this cluster (only non-merged concepts)
        cluster_set = set(cluster)
        cluster_pairs = [
            (i, j, s) for (i, j), s in similarities.items()
            if i in cluster_set and j in cluster_set
        ]
        cluster_pairs.sort(key=lambda x: x[2], reverse=True)

        for idx_a, idx_b, sim in cluster_pairs:
            concept_a = self._concepts[idx_a]
            concept_b = self._concepts[idx_b]

            # Skip if either was merged
            if concept_a.uri in self._merged_uris or concept_b.uri in self._merged_uris:
                continue

            # Skip if we already have a relation between these
            pair_key = (min(concept_a.uri, concept_b.uri), max(concept_a.uri, concept_b.uri))
            if pair_key in related_pairs:
                continue

            # Analyze with LLM
            llm_result = self.verify_pair_with_llm(idx_a, idx_b)
            result_type = llm_result["result"]
            direction = llm_result["direction"]

            # Skip "same" (should have been caught by cluster verification) and "none"
            if result_type not in ("broader", "partOf", "dependsOn") or not direction:
                continue

            # Determine direction
            if direction == "a_to_b":
                from_concept, to_concept = concept_a, concept_b
            else:
                from_concept, to_concept = concept_b, concept_a

            # Track this pair
            related_pairs.add(pair_key)

            # Insert relation to KG
            turtle = build_relation_turtle(from_concept.uri, result_type, to_concept.uri)
            self.sparql.insert_turtle_silent(turtle)

            relation_results.append(RelationResult(
                from_uri=from_concept.uri,
                from_name=from_concept.name,
                relation=result_type,
                to_uri=to_concept.uri,
                to_name=to_concept.name,
                similarity=sim,
            ))
            logger.info("  Related '%s' -[%s]-> '%s' (sim=%.3f)",
                       from_concept.name, result_type, to_concept.name, sim)

        # No additional merges from this method
        return [], relation_results

    def merge_verified_groups(
        self, groups: list[list[int]], similarities: dict[tuple[int, int], float]
    ) -> list[MergeResult]:
        """Merge concepts within verified groups.

        Returns:
            List of successful merges
        """
        results = []

        for group in groups:
            if len(group) < 2:
                continue

            # Get concepts
            concepts = [self._concepts[i] for i in group]

            # Filter out already merged
            valid = [(i, c) for i, c in zip(group, concepts, strict=True) if c.uri not in self._merged_uris]
            if len(valid) < 2:
                continue

            # Choose the best one to keep
            valid_concepts = [c for _, c in valid]
            keep = max(valid_concepts, key=lambda c: (len(c.description) if c.description else 0, c.name))

            # Merge others into keep
            for idx, concept in valid:
                if concept.uri == keep.uri:
                    continue
                if concept.uri in self._merged_uris:
                    continue

                # Find similarity (may not exist if transitive)
                sim = similarities.get((min(idx, group[0]), max(idx, group[0])), 0.85)

                if merge_concepts(self.sparql, keep.uri, concept.uri, concept.name):
                    self._merged_uris.add(concept.uri)
                    results.append(MergeResult(
                        keep_uri=keep.uri,
                        keep_name=keep.name,
                        removed_uri=concept.uri,
                        removed_name=concept.name,
                        similarity=sim,
                        method="llm",
                    ))
                    logger.info("  Merged '%s' -> '%s' (LLM verified)", concept.name, keep.name)

        return results

    def run(self, skip_llm: bool = False, workers: int = 1) -> tuple[int, int, int]:
        """Run full concept organization: merge duplicates and add relations.

        Args:
            skip_llm: If True, only do auto-merge (skip LLM verification)
            workers: Number of parallel workers for cluster processing (default: 1)

        Returns:
            Tuple of (auto_merged_count, llm_merged_count, relations_added_count)
        """
        # Load and embed
        self.load_concepts()
        self.compute_embeddings()

        # Find all similar pairs
        pairs = self.find_similar_pairs()

        # Build similarity lookup
        similarities = {(i, j): s for i, j, s in pairs}

        # Phase 1: Auto-merge high similarity (sequential - fast, no LLM)
        auto_results = self.auto_merge_high_similarity(pairs)

        # Phase 2: Cluster and verify medium similarity
        llm_merge_results: list[MergeResult] = []
        relation_results: list[RelationResult] = []

        if not skip_llm:
            clusters = self.cluster_medium_similarity(pairs)

            if clusters:
                small_clusters = [c for c in clusters if len(c) <= DEDUP_MAX_CLUSTER_SIZE]
                large_clusters = [c for c in clusters if len(c) > DEDUP_MAX_CLUSTER_SIZE]
                all_clusters = (
                    [("small", c) for c in small_clusters] +
                    [("large", c) for c in large_clusters]
                )

                if workers > 1 and len(all_clusters) > 1:
                    # Parallel processing
                    logger.info("Processing %d clusters with %d workers...",
                               len(all_clusters), workers)

                    with ThreadPoolExecutor(max_workers=workers) as executor:
                        futures = {}
                        for cluster_type, cluster in all_clusters:
                            if cluster_type == "small":
                                future = executor.submit(
                                    self._process_small_cluster, cluster, similarities
                                )
                            else:
                                future = executor.submit(
                                    self._process_large_cluster, cluster, similarities
                                )
                            futures[future] = (cluster_type, len(cluster))

                        for future in as_completed(futures):
                            cluster_type, size = futures[future]
                            try:
                                merges, relations = future.result()
                                llm_merge_results.extend(merges)
                                relation_results.extend(relations)
                                logger.info("  Completed %s cluster (%d concepts): %d merges, %d relations",
                                           cluster_type, size, len(merges), len(relations))
                            except Exception as e:
                                logger.warning("  Cluster processing failed: %s", e)
                else:
                    # Sequential processing (single worker)
                    if small_clusters:
                        logger.info("Verifying %d small clusters with LLM...", len(small_clusters))
                        for i, cluster in enumerate(small_clusters):
                            logger.info("  Cluster %d/%d: %d concepts",
                                       i + 1, len(small_clusters), len(cluster))
                            merges, relations = self._process_small_cluster(cluster, similarities)
                            llm_merge_results.extend(merges)
                            relation_results.extend(relations)

                    if large_clusters:
                        logger.info("Verifying %d large clusters pairwise (>%d concepts)...",
                                   len(large_clusters), DEDUP_MAX_CLUSTER_SIZE)
                        for i, cluster in enumerate(large_clusters):
                            logger.info("  Large cluster %d/%d: %d concepts (pairwise)",
                                       i + 1, len(large_clusters), len(cluster))
                            merges, relations = self._process_large_cluster(cluster, similarities)
                            llm_merge_results.extend(merges)
                            relation_results.extend(relations)

        logger.info("Organization complete: %d auto-merged, %d LLM-merged, %d relations added",
                   len(auto_results), len(llm_merge_results), len(relation_results))
        return len(auto_results), len(llm_merge_results), len(relation_results)

    def _choose_keep_remove(
        self, a: ConceptInfo, b: ConceptInfo
    ) -> tuple[ConceptInfo, ConceptInfo]:
        """Choose which concept to keep vs remove."""
        a_desc_len = len(a.description) if a.description else 0
        b_desc_len = len(b.description) if b.description else 0

        if a_desc_len > b_desc_len:
            return a, b
        elif b_desc_len > a_desc_len:
            return b, a
        else:
            return (a, b) if a.name.lower() < b.name.lower() else (b, a)

    def _is_merged(self, uri: str) -> bool:
        """Thread-safe check if URI has been merged."""
        with self._lock:
            return uri in self._merged_uris

    def _mark_merged(self, uri: str) -> bool:
        """Thread-safe mark URI as merged. Returns False if already merged."""
        with self._lock:
            if uri in self._merged_uris:
                return False
            self._merged_uris.add(uri)
            return True

    def _process_small_cluster(
        self,
        cluster: list[int],
        similarities: dict[tuple[int, int], float],
    ) -> tuple[list[MergeResult], list[RelationResult]]:
        """Process a small cluster: verify with LLM and find relations.

        Thread-safe worker method for parallel processing.
        """
        merge_results = []
        relation_results = []

        # Step 1: Cluster verification for merging
        verified_groups = self.verify_cluster_with_llm(cluster)
        if verified_groups:
            merges = self._merge_verified_groups_safe(verified_groups, similarities)
            merge_results.extend(merges)

        # Step 2: Find relations between non-merged concepts
        _, relations = self._find_relations_safe(cluster, similarities)
        relation_results.extend(relations)

        return merge_results, relation_results

    def _process_large_cluster(
        self,
        cluster: list[int],
        similarities: dict[tuple[int, int], float],
    ) -> tuple[list[MergeResult], list[RelationResult]]:
        """Process a large cluster with pairwise verification.

        Thread-safe worker method for parallel processing.
        """
        return self._verify_pairwise_safe(cluster, similarities)

    def _merge_verified_groups_safe(
        self,
        groups: list[list[int]],
        similarities: dict[tuple[int, int], float],
    ) -> list[MergeResult]:
        """Thread-safe version of merge_verified_groups."""
        results = []

        for group in groups:
            if len(group) < 2:
                continue

            concepts = [self._concepts[i] for i in group]
            valid = [(i, c) for i, c in zip(group, concepts, strict=True)
                     if not self._is_merged(c.uri)]
            if len(valid) < 2:
                continue

            valid_concepts = [c for _, c in valid]
            keep = max(valid_concepts, key=lambda c: (len(c.description) if c.description else 0, c.name))

            for idx, concept in valid:
                if concept.uri == keep.uri:
                    continue
                if not self._mark_merged(concept.uri):
                    continue  # Already merged by another thread

                sim = similarities.get((min(idx, group[0]), max(idx, group[0])), 0.85)

                if merge_concepts(self.sparql, keep.uri, concept.uri, concept.name):
                    results.append(MergeResult(
                        keep_uri=keep.uri,
                        keep_name=keep.name,
                        removed_uri=concept.uri,
                        removed_name=concept.name,
                        similarity=sim,
                        method="llm",
                    ))
                    logger.info("  Merged '%s' -> '%s' (LLM verified)", concept.name, keep.name)

        return results

    def _verify_pairwise_safe(
        self,
        cluster: list[int],
        similarities: dict[tuple[int, int], float],
    ) -> tuple[list[MergeResult], list[RelationResult]]:
        """Thread-safe pairwise verification for large clusters."""
        merge_results = []
        relation_results = []
        related_pairs: set[tuple[str, str]] = set()

        cluster_set = set(cluster)
        cluster_pairs = [
            (i, j, s) for (i, j), s in similarities.items()
            if i in cluster_set and j in cluster_set
        ]
        cluster_pairs.sort(key=lambda x: x[2], reverse=True)

        for idx_a, idx_b, sim in cluster_pairs:
            concept_a = self._concepts[idx_a]
            concept_b = self._concepts[idx_b]

            if self._is_merged(concept_a.uri) or self._is_merged(concept_b.uri):
                continue

            llm_result = self.verify_pair_with_llm(idx_a, idx_b)
            result_type = llm_result["result"]
            direction = llm_result["direction"]

            if result_type == "same":
                keep, remove = self._choose_keep_remove(concept_a, concept_b)
                if not self._mark_merged(remove.uri):
                    continue  # Already merged by another thread

                if merge_concepts(self.sparql, keep.uri, remove.uri, remove.name):
                    merge_results.append(MergeResult(
                        keep_uri=keep.uri,
                        keep_name=keep.name,
                        removed_uri=remove.uri,
                        removed_name=remove.name,
                        similarity=sim,
                        method="llm_pairwise",
                    ))
                    logger.info("  Merged '%s' -> '%s' (pairwise, sim=%.3f)",
                               remove.name, keep.name, sim)

            elif result_type in ("broader", "partOf", "dependsOn") and direction:
                if direction == "a_to_b":
                    from_concept, to_concept = concept_a, concept_b
                else:
                    from_concept, to_concept = concept_b, concept_a

                pair_key = (from_concept.uri, to_concept.uri)
                if pair_key in related_pairs:
                    continue
                related_pairs.add(pair_key)

                turtle = build_relation_turtle(from_concept.uri, result_type, to_concept.uri)
                self.sparql.insert_turtle_silent(turtle)

                relation_results.append(RelationResult(
                    from_uri=from_concept.uri,
                    from_name=from_concept.name,
                    relation=result_type,
                    to_uri=to_concept.uri,
                    to_name=to_concept.name,
                    similarity=sim,
                ))
                logger.info("  Related '%s' -[%s]-> '%s' (sim=%.3f)",
                           from_concept.name, result_type, to_concept.name, sim)

        return merge_results, relation_results

    def _find_relations_safe(
        self,
        cluster: list[int],
        similarities: dict[tuple[int, int], float],
    ) -> tuple[list[MergeResult], list[RelationResult]]:
        """Thread-safe version of find_relations_in_cluster."""
        relation_results = []
        related_pairs: set[tuple[str, str]] = set()

        cluster_set = set(cluster)
        cluster_pairs = [
            (i, j, s) for (i, j), s in similarities.items()
            if i in cluster_set and j in cluster_set
        ]
        cluster_pairs.sort(key=lambda x: x[2], reverse=True)

        for idx_a, idx_b, sim in cluster_pairs:
            concept_a = self._concepts[idx_a]
            concept_b = self._concepts[idx_b]

            if self._is_merged(concept_a.uri) or self._is_merged(concept_b.uri):
                continue

            pair_key = (min(concept_a.uri, concept_b.uri), max(concept_a.uri, concept_b.uri))
            if pair_key in related_pairs:
                continue

            llm_result = self.verify_pair_with_llm(idx_a, idx_b)
            result_type = llm_result["result"]
            direction = llm_result["direction"]

            if result_type not in ("broader", "partOf", "dependsOn") or not direction:
                continue

            if direction == "a_to_b":
                from_concept, to_concept = concept_a, concept_b
            else:
                from_concept, to_concept = concept_b, concept_a

            related_pairs.add(pair_key)

            turtle = build_relation_turtle(from_concept.uri, result_type, to_concept.uri)
            self.sparql.insert_turtle_silent(turtle)

            relation_results.append(RelationResult(
                from_uri=from_concept.uri,
                from_name=from_concept.name,
                relation=result_type,
                to_uri=to_concept.uri,
                to_name=to_concept.name,
                similarity=sim,
            ))
            logger.info("  Related '%s' -[%s]-> '%s' (sim=%.3f)",
                       from_concept.name, result_type, to_concept.name, sim)

        return [], relation_results
