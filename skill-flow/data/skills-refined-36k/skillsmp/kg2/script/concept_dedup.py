"""Concept deduplication during enrichment.

Simple embedding-based deduplication:
1. Compute embedding for new concept
2. Compare against existing concepts
3. If similarity >= 0.95, return existing concept
4. Otherwise, create new concept (duplicates are cleaned up later by batch dedup)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .constants import DEFAULT_EMBEDDING_MODEL, EMBEDDING_THRESHOLD_AUTO_MERGE
from .embeddings import find_nearest_above_threshold, format_concept_for_embedding
from .models import ConceptMatchType

if TYPE_CHECKING:
    from .clients import OpenAIClient, SparqlClient
    from .db import Database

logger = logging.getLogger(__name__)


@dataclass
class ConceptMatch:
    """Result of concept matching."""
    uri: str
    name: str
    similarity: float | None
    match_type: ConceptMatchType
    embedding: list[float] | None = None


class ConceptDeduplicator:
    """Simple embedding-based concept deduplication during enrichment."""

    def __init__(
        self,
        sparql: SparqlClient,
        db: Database,
        openai: OpenAIClient | None,
    ):
        self.sparql = sparql
        self.db = db
        self.openai = openai
        self._name_cache: dict[str, str] = {}  # uri -> name

    def find_or_create_concept(
        self,
        concept_name: str,
        paper_uri: str,
        description: str | None = None,
    ) -> ConceptMatch:
        """Find existing concept or prepare to create new one.

        Args:
            concept_name: Name of the concept
            paper_uri: URI of the paper (unused, kept for API compatibility)
            description: Optional description

        Returns:
            ConceptMatch with:
            - uri: existing concept URI, or empty string for NEW
            - embedding: computed embedding (for NEW concepts, to save after creation)
        """
        if not self.openai:
            return ConceptMatch("", concept_name, None, ConceptMatchType.NEW)

        # Compute embedding for the new concept
        try:
            embed_text = format_concept_for_embedding(concept_name, description)
            embedding = self.openai.embed(embed_text)
        except Exception as e:
            logger.debug("Concept embedding failed: %s", e)
            return ConceptMatch("", concept_name, None, ConceptMatchType.NEW)

        # Compare against existing concepts
        existing = self.db.get_all_concept_embeddings()
        if not existing:
            return ConceptMatch("", concept_name, None, ConceptMatchType.NEW, embedding=embedding)

        match = find_nearest_above_threshold(
            embedding, existing, EMBEDDING_THRESHOLD_AUTO_MERGE
        )

        if match:
            uri, sim = match
            name = self._get_concept_name(uri) or concept_name
            logger.info("  Concept '%s' -> '%s' (sim=%.3f)", concept_name, name, sim)
            return ConceptMatch(uri, name, sim, ConceptMatchType.EMBEDDING)

        # No match - return NEW with the computed embedding
        return ConceptMatch("", concept_name, None, ConceptMatchType.NEW, embedding=embedding)

    def save_concept_embedding(self, concept_uri: str, embedding: list[float]) -> None:
        """Save embedding for a newly created concept."""
        if embedding is None:
            return
        from .turtle_builders import expand_prefixed_uri
        full_uri = expand_prefixed_uri(concept_uri)
        self.db.save_concept_embedding(full_uri, embedding, DEFAULT_EMBEDDING_MODEL)

    def _get_concept_name(self, concept_uri: str) -> str | None:
        """Get name for a concept URI (cached to avoid repeated SPARQL queries)."""
        if concept_uri in self._name_cache:
            return self._name_cache[concept_uri]

        from . import queries
        results = self.sparql.query(queries.get_concept_label(concept_uri))
        name = results[0]['label']['value'] if results else None
        if name:
            self._name_cache[concept_uri] = name
        return name
