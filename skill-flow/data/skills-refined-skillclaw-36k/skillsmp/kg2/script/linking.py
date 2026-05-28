"""Claim linking - finding relations between claims across papers."""

from __future__ import annotations

import json
import logging
from typing import Any

from .clients import OpenAIClient, SparqlClient
from .constants import CLAIM_RELATION_DEFINITIONS, EMBEDDING_THRESHOLD_CLAIM_FILTER
from .db import Database
from .embeddings import find_similar_pairs
from .kg2_helpers import add_claim_relation, get_claims_for_paper, get_ref_claims
from .processing import iter_papers
from .prompt_builders import build_claim_relations_prompt
from .schemas import ClaimRelationsResponse
from .sparql_parsers import validate_claim_relations

logger = logging.getLogger(__name__)


class Linker:
    """Finds missed claim relations between papers."""

    def __init__(self, sparql: SparqlClient, db: Database, openai: OpenAIClient | None):
        self.sparql = sparql
        self.db = db
        self.openai = openai

    def link(self, max_papers: int | None = None,
             watch: bool = False, poll_interval: int = 10,
             parallel: bool = False) -> int:
        """Find missed claim relations for enriched papers.

        Args:
            max_papers: Max papers to process (None = all pending)
            watch: If True, poll for new papers instead of exiting
            poll_interval: Seconds between polls when watching
            parallel: If True, use atomic claims (for multi-worker mode)

        Returns:
            Number of papers link-checked
        """
        processed = 0

        papers = iter_papers(
            db=self.db,
            claim_fn=self.db.claim_unlinked_paper,
            next_fn=self.db.next_unlinked_paper,
            reset_stale_fn=self.db.reset_stale_linking,
            parallel=parallel,
            watch=watch,
            poll_interval=poll_interval,
            max_papers=max_papers,
            log_waiting_msg="Waiting for enriched papers...",
        )

        for row in papers:
            refs = json.loads(row.refs) if row.refs else []
            logger.info("  Linking: %s...", row.title[:50])

            my_claims = get_claims_for_paper(self.sparql, row.kg2_uri)
            if not my_claims:
                self.db.mark_link_checked(row.id)
                self.db.commit()
                continue

            ref_claims = get_ref_claims(self.sparql, self.db, refs, citing_paper_id=row.id)
            relations = self.find_claim_relations(my_claims, ref_claims, row.year)

            for rel in relations:
                add_claim_relation(self.sparql, rel['from'], rel['type'], rel['to'])

            self.db.mark_link_checked(row.id)
            self.db.commit()
            processed += 1

            logger.info("    -> %d relations found", len(relations))

        logger.info("Link-checked %d papers", processed)
        return processed

    def find_claim_relations(
        self,
        my_claims: list[dict[str, str]],
        ref_claims: list[dict[str, Any]],
        paper_year: int | None = None,
    ) -> list[dict[str, str]]:
        """Find relations between this paper's claims and referenced claims.

        Uses embedding similarity to pre-filter candidate pairs before LLM.
        """
        if not self.openai or not my_claims or not ref_claims:
            return []

        # Build valid URI sets for validation
        valid_from_uris = {c['uri'] for c in my_claims}
        valid_to_uris = {rc['claim_uri'] for rc in ref_claims[:20]}

        # Try embedding-based pre-filtering
        filtered_ref_claims = self._filter_by_embedding_similarity(
            my_claims, ref_claims[:20]
        )

        # If no similar claims found, skip LLM call entirely
        if not filtered_ref_claims:
            logger.debug("    No similar claims found (embedding pre-filter)")
            return []

        # Use filtered claims for LLM
        prompt = build_claim_relations_prompt(
            my_claims, filtered_ref_claims, paper_year, CLAIM_RELATION_DEFINITIONS
        )

        try:
            result = self.openai.structured_completion(
                messages=[{"role": "user", "content": prompt}],
                schema=ClaimRelationsResponse.json_schema(),
                schema_name="claim_relations",
            )
            relations = result.get('relations', [])

            validated, invalid_count = validate_claim_relations(
                relations, valid_from_uris, valid_to_uris
            )

            if invalid_count > 0:
                logger.info("    (filtered %d relations with invalid URIs)", invalid_count)

            return validated
        except Exception as e:
            logger.warning("    OpenAI error: %s", e)
            return []

    def _filter_by_embedding_similarity(
        self,
        my_claims: list[dict[str, str]],
        ref_claims: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Filter ref_claims to those with at least one similar my_claim.

        Returns ref_claims that have embedding similarity >= threshold
        with at least one of my_claims.
        """
        # Get embeddings for my claims
        my_uris = [c['uri'] for c in my_claims]
        my_embeddings = self.db.get_claim_embeddings(my_uris)

        if not my_embeddings:
            # No embeddings available - return all claims (no filtering)
            return ref_claims

        # Get embeddings for ref claims
        ref_uris = [rc['claim_uri'] for rc in ref_claims]
        ref_embeddings = self.db.get_claim_embeddings(ref_uris)

        if not ref_embeddings:
            # No embeddings available - return all claims (no filtering)
            return ref_claims

        # Find similar pairs
        similar_pairs = find_similar_pairs(
            my_embeddings, ref_embeddings, EMBEDDING_THRESHOLD_CLAIM_FILTER
        )

        if not similar_pairs:
            return []

        # Get unique ref URIs that have at least one similar my_claim
        similar_ref_uris = {pair[1] for pair in similar_pairs}

        # Filter ref_claims to only those with similar embeddings
        filtered = [rc for rc in ref_claims if rc['claim_uri'] in similar_ref_uris]

        if len(filtered) < len(ref_claims):
            logger.debug("    Embedding filter: %d/%d ref claims", len(filtered), len(ref_claims))

        return filtered
