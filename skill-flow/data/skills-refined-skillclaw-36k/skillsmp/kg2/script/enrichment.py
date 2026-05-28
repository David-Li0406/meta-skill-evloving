"""LLM enrichment for extracting concepts and claims from papers."""

from __future__ import annotations

import json
import logging
from typing import Any

from . import queries
from .clients import OpenAIClient, SparqlClient, escape_sparql
from .concept_dedup import ConceptDeduplicator
from .constants import CLAIM_RELATION_DEFINITIONS, CLAIM_RELATIONS, DEFAULT_EMBEDDING_MODEL
from .db import Database
from .exceptions import EnrichmentError
from .kg2_helpers import add_claim_relation, get_ref_claims
from .models import ConceptMatchType
from .processing import iter_papers
from .prompt_builders import build_extraction_prompt, build_ref_claims_context
from .schemas import ExtractionResponse
from .sparql_parsers import parse_extraction_concepts
from .turtle_builders import (
    build_claim_turtle,
    build_concept_turtle,
    build_new_concept_turtle,
    build_relation_turtle,
    expand_prefixed_uri,
)

logger = logging.getLogger(__name__)


class Enricher:
    """Enriches papers with LLM-extracted concepts and claims."""

    def __init__(self, sparql: SparqlClient, db: Database, openai: OpenAIClient | None):
        self.sparql = sparql
        self.db = db
        self.openai = openai
        self._pending_concept_relations: list[dict[str, str]] = []
        self._deduplicator = ConceptDeduplicator(sparql, db, openai)

    def enrich(self, max_papers: int | None = None,
               watch: bool = False, poll_interval: int = 10,
               parallel: bool = False) -> int:
        """Enrich papers with LLM-extracted concepts and claims.

        Args:
            max_papers: Max papers to process (None = all pending)
            watch: If True, poll for new papers instead of exiting
            poll_interval: Seconds between polls when watching
            parallel: If True, use atomic claims (for multi-worker mode)

        Returns:
            Number of papers enriched
        """
        processed = 0

        papers = iter_papers(
            db=self.db,
            claim_fn=self.db.claim_unenriched_paper,
            next_fn=self.db.next_unenriched_paper,
            reset_stale_fn=self.db.reset_stale_enrichment,
            parallel=parallel,
            watch=watch,
            poll_interval=poll_interval,
            max_papers=max_papers,
            log_waiting_msg="Waiting for new papers...",
        )

        for row in papers:
            refs = json.loads(row.refs) if row.refs else []

            if not row.abstract:
                self.db.mark_enriched_skipped(row.id, 'no_abstract')
                self.db.commit()
                logger.info("  Skipped (no abstract): %s", row.title[:50])
                continue

            ref_claims = get_ref_claims(self.sparql, self.db, refs)

            try:
                if self._enrich_paper(row.id, row.kg2_uri, row.title, row.abstract, row.year, ref_claims):
                    processed += 1
            except EnrichmentError as e:
                logger.warning("  %s", e)
                self.db.rollback()
                continue

        logger.info("Enriched %d papers", processed)
        return processed

    def _enrich_paper(self, paper_id: str, paper_uri: str, title: str,
                      abstract: str, year: int | None,
                      ref_claims: list[dict[str, Any]]) -> bool:
        """Enrich a single paper.

        Returns:
            True if enriched successfully

        Raises:
            EnrichmentError: If LLM extraction fails
        """
        logger.info("  Enriching: %s...", title[:50])

        # Reset pending concept relations
        self._pending_concept_relations = []

        # Build valid claim URIs for relation validation (Bug 2 fix)
        valid_claim_uris = {rc['claim_uri'] for rc in ref_claims}

        # Extract concepts and claims using LLM
        concepts, claims = self._extract_concepts_and_claims(
            paper_id, title, abstract, year, ref_claims
        )

        # Helper to resolve concept name to URI (with caching)
        concept_uris: dict[str, str] = {}

        def resolve_concept(name: str, description: str | None = None) -> str:
            if name not in concept_uris:
                concept_uris[name] = self._ensure_concept(name, paper_uri, description)
            return concept_uris[name]

        # Insert concepts
        for concept_name, description in concepts.items():
            resolve_concept(concept_name, description)

        # Add concept relations
        concept_rels = 0
        for rel in self._pending_concept_relations:
            self._add_concept_relation(
                resolve_concept(rel['from']), rel['type'], resolve_concept(rel['to'])
            )
            concept_rels += 1

        # Insert claims
        claim_rels = 0
        invalid_rels = 0
        for claim in claims:
            regarding_uris = [resolve_concept(n) for n in claim.get('regarding', [])]
            claim_uri = self._insert_claim(paper_uri, claim['text'], regarding_uris)

            # Add relations if specified - validate target URIs first
            for rel_type in CLAIM_RELATIONS:
                target_uri = claim.get(rel_type)
                if not target_uri:
                    continue
                if target_uri in valid_claim_uris:
                    add_claim_relation(self.sparql, claim_uri, rel_type, target_uri)
                    claim_rels += 1
                else:
                    invalid_rels += 1

        # Mark as enriched
        self.db.mark_enriched(paper_id)

        # Reset link_checked_at for papers that cite this one
        reset_count = self.db.reset_link_checked_for_citers(paper_id)

        self.db.commit()

        msg = f"    -> {len(concepts)} concepts, {len(claims)} claims, {concept_rels + claim_rels} relations"
        if invalid_rels > 0:
            msg += f" (filtered {invalid_rels} invalid claim relations)"
        if reset_count > 0:
            msg += f" (reset {reset_count} citers for re-linking)"
        logger.info(msg)

        return True

    def _extract_concepts_and_claims(
        self,
        paper_id: str,
        title: str,
        abstract: str,
        year: int | None,
        ref_claims: list[dict[str, Any]],
    ) -> tuple[dict[str, str], list[dict[str, Any]]]:
        """Extract concepts and claims from paper using LLM.

        Raises:
            EnrichmentError: If OpenAI client is not configured or API call fails
        """
        if not self.openai:
            raise EnrichmentError(paper_id, "OpenAI client not configured")

        ref_context = build_ref_claims_context(ref_claims)
        prompt = build_extraction_prompt(
            title, abstract, year, ref_context, CLAIM_RELATION_DEFINITIONS
        )

        try:
            result = self.openai.structured_completion(
                messages=[{"role": "user", "content": prompt}],
                schema=ExtractionResponse.json_schema(),
                schema_name="paper_extraction",
            )
            concepts_raw = result.get('concepts', [])
            concepts, concept_relations = parse_extraction_concepts(concepts_raw)
            self._pending_concept_relations = concept_relations
            return concepts, result.get('claims', [])
        except Exception as e:
            raise EnrichmentError(paper_id, f"OpenAI API error: {e}") from e

    def _ensure_concept(self, concept_name: str, paper_uri: str | None = None,
                        description: str | None = None) -> str:
        """Get or create Concept URI.

        Uses context-aware deduplication:
        1. Exact name match with context verification
        2. Embedding similarity with lazy backfill
        """
        if paper_uri:
            match = self._deduplicator.find_or_create_concept(
                concept_name, paper_uri, description
            )

            if match.match_type != ConceptMatchType.NEW:
                # Found existing - add description if missing
                if description and match.match_type == ConceptMatchType.EXACT_WITH_CONTEXT:
                    results = self.sparql.query(queries.find_concept_by_name(concept_name))
                    if results and 'comment' not in results[0]:
                        self.sparql.insert_turtle(
                            build_concept_turtle(match.uri, escape_sparql(description))
                        )
                return match.uri

            # NEW concept - create it and save embedding if available
            concept_uri = self.sparql.generate_uri("co")
            turtle = build_new_concept_turtle(
                concept_uri,
                escape_sparql(concept_name),
                escape_sparql(description) if description else None,
                paper_uri,
            )
            self.sparql.insert_turtle(turtle)

            if match.embedding:
                self._deduplicator.save_concept_embedding(concept_uri, match.embedding)
            return concept_uri

        # No paper context - just create concept without dedup
        concept_uri = self.sparql.generate_uri("co")
        turtle = build_new_concept_turtle(
            concept_uri,
            escape_sparql(concept_name),
            escape_sparql(description) if description else None,
            paper_uri,
        )
        self.sparql.insert_turtle(turtle)
        return concept_uri

    def _insert_claim(self, paper_uri: str, claim_text: str,
                      concept_uris: list[str] | None = None) -> str:
        """Create Claim and add hasClaim relationship.

        Also computes and saves claim embedding for similarity-based linking.
        """
        claim_uri = self.sparql.generate_uri("cl")
        turtle = build_claim_turtle(
            claim_uri, paper_uri, escape_sparql(claim_text), concept_uris
        )
        self.sparql.insert_turtle(turtle)

        # Save claim embedding for similarity-based linking
        if self.openai:
            try:
                claim_embedding = self.openai.embed(claim_text)
                full_uri = expand_prefixed_uri(claim_uri)
                self.db.save_claim_embedding(full_uri, claim_embedding, DEFAULT_EMBEDDING_MODEL)
            except Exception as e:
                logger.debug("  Claim embedding failed: %s", e)

        return claim_uri

    def _add_concept_relation(self, from_concept: str, rel_type: str, to_concept: str):
        """Add relation between concepts."""
        self.sparql.insert_turtle_silent(build_relation_turtle(from_concept, rel_type, to_concept))
