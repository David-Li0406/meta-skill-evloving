"""Shared helper functions for KG2 operations.

These functions are used by both Enricher and Linker to avoid duplication.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from . import queries
from .constants import EMBEDDING_THRESHOLD_AUTO_MERGE
from .exceptions import SparqlError
from .sparql_parsers import parse_sparql_claims_result
from .turtle_builders import build_relation_turtle

if TYPE_CHECKING:
    from collections.abc import Callable

    from .clients import OpenAIClient, SparqlClient
    from .db import Database

logger = logging.getLogger(__name__)


def verify_and_merge_concepts(
    openai: OpenAIClient | None,
    sparql: SparqlClient,
    keep_uri: str,
    keep_name: str,
    keep_desc: str | None,
    remove_uri: str,
    remove_name: str,
    remove_desc: str | None,
    similarity: float,
    context: str | None = None,
    on_merge_success: Callable[[], None] | None = None,
) -> bool:
    """Verify two concepts are the same and merge them if so.

    Handles the common pattern:
    1. If similarity >= AUTO_MERGE threshold -> merge directly
    2. Otherwise if OpenAI available -> verify with LLM, then merge if confirmed

    Args:
        openai: OpenAI client (None to skip LLM verification)
        sparql: SPARQL client for merge operation
        keep_uri: URI of concept to keep
        keep_name: Name of concept to keep
        keep_desc: Description of concept to keep
        remove_uri: URI of concept to remove
        remove_name: Name of concept to remove
        remove_desc: Description of concept to remove
        similarity: Embedding similarity score
        context: Optional context for LLM verification
        on_merge_success: Optional callback after successful merge

    Returns:
        True if merged successfully
    """
    if similarity >= EMBEDDING_THRESHOLD_AUTO_MERGE:
        verified = True
    elif openai:
        verified = llm_verify_same_concept(
            openai, keep_name, keep_desc, remove_name, remove_desc, context
        )
    else:
        return False

    if not verified:
        logger.debug("LLM rejected merge: '%s' ~ '%s'", keep_name, remove_name)
        return False

    if merge_concepts(sparql, keep_uri, remove_uri, remove_name):
        logger.info("Merged: '%s' -> '%s' (sim=%.3f)", remove_name, keep_name, similarity)
        if on_merge_success:
            on_merge_success()
        return True
    return False


# --- LLM Verification ---

_CONCEPT_MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "same_concept": {
            "type": "boolean",
            "description": "True if both concepts refer to the same thing"
        },
        "reason": {
            "type": "string",
            "description": "Brief explanation for the decision"
        }
    },
    "required": ["same_concept"],
    "additionalProperties": False
}


def llm_verify_same_concept(
    openai: OpenAIClient,
    name_a: str,
    desc_a: str | None,
    name_b: str,
    desc_b: str | None,
    context: str | None = None,
) -> bool:
    """Use LLM to verify if two concepts are the same.

    Args:
        openai: OpenAI client
        name_a: First concept name
        desc_a: First concept description
        name_b: Second concept name
        desc_b: Second concept description
        context: Optional additional context (e.g., paper title/abstract)

    Returns:
        True if LLM confirms they are the same concept
    """
    context_str = f"{context}\n\n" if context else ""

    prompt = f"""{context_str}Are these two concepts referring to the same thing?

Concept A:
- Name: {name_a}
- Description: {desc_a or '(none)'}

Concept B:
- Name: {name_b}
- Description: {desc_b or '(none)'}

Consider:
- Same concept may have different names (e.g., "CNN" vs "Convolutional Neural Network")
- Different concepts may have similar names (e.g., "transformer" in ML vs electrical engineering)"""

    try:
        result = openai.structured_completion(
            messages=[{"role": "user", "content": prompt}],
            schema=_CONCEPT_MATCH_SCHEMA,
            schema_name="concept_match",
        )
        is_same = result.get("same_concept", False)
        reason = result.get("reason", "")
        logger.debug("LLM verification: %s ~ %s => %s (%s)", name_a, name_b, is_same, reason)
        return is_same
    except Exception as e:
        logger.debug("LLM verification failed: %s", e)
        return False


def get_claims_for_paper(sparql: SparqlClient, paper_uri: str) -> list[dict[str, str]]:
    """Get claims for a paper from kg2.

    Args:
        sparql: SPARQL client
        paper_uri: URI of the paper

    Returns:
        List of claim dicts with 'uri' and 'text' keys
    """
    results = sparql.query(queries.get_claims_for_paper(paper_uri))
    return parse_sparql_claims_result(results)


def get_ref_claims(
    sparql: SparqlClient, db: Database, ref_ids: list[str],
    citing_paper_id: str | None = None,
) -> list[dict[str, Any]]:
    """Get claims from enriched referenced papers.

    Args:
        sparql: SPARQL client
        db: Database connection
        ref_ids: List of paper IDs to get claims from
        citing_paper_id: Optional citing paper ID to include citation context

    Returns:
        List of ref claim dicts with paper_id, paper_title, paper_year,
        claim_uri, claim_text, and optionally citation_context keys
    """
    ref_claims = []
    enriched_refs = db.get_enriched_refs(ref_ids)

    # Get citation contexts if citing paper is provided
    citation_contexts: dict[str, dict] = {}
    if citing_paper_id:
        citation_contexts = db.get_citation_contexts_for_paper(citing_paper_id)

    for ref in enriched_refs:
        claims = get_claims_for_paper(sparql, ref.kg2_uri)

        # Get citation context for this reference
        ctx = citation_contexts.get(ref.id)
        context_info = None
        if ctx:
            # Combine intents and first context snippet
            intents = ctx.get('intents', [])
            contexts = ctx.get('contexts', [])
            if intents or contexts:
                context_info = {
                    'intents': intents,
                    'snippet': contexts[0] if contexts else None,
                }

        for claim in claims:
            ref_claims.append({
                'paper_id': ref.id,
                'paper_title': ref.title,
                'paper_year': ref.year,
                'claim_uri': claim['uri'],
                'claim_text': claim['text'],
                'citation_context': context_info,
            })

    return ref_claims


def add_claim_relation(
    sparql: SparqlClient, from_claim: str, rel_type: str, to_claim: str
) -> bool:
    """Add relation between claims.

    Args:
        sparql: SPARQL client
        from_claim: Source claim URI
        rel_type: Relation type (extends, refutes, supports)
        to_claim: Target claim URI

    Returns:
        True if inserted successfully, False otherwise
    """
    return sparql.insert_turtle_silent(
        build_relation_turtle(from_claim, rel_type, to_claim)
    )


def merge_concepts(
    sparql: SparqlClient, keep_uri: str, remove_uri: str, remove_name: str | None = None
) -> bool:
    """Merge two concepts: transfer all relationships from remove_uri to keep_uri."""
    try:
        # 1. Move all triples where remove_uri is object
        sparql.update(queries.merge_concepts_as_object(keep_uri, remove_uri))

        # 2. Move all triples where remove_uri is subject (except type/label/comment)
        sparql.update(queries.merge_concepts_as_subject(keep_uri, remove_uri))

        # 3. Preserve removed concept's name as alias
        if remove_name:
            sparql.update(queries.add_alias_label(keep_uri, remove_name))

        # 4. Delete remaining triples (type, label, comment)
        sparql.update(queries.delete_concept(remove_uri))

        logger.debug("Merged concept %s into %s", remove_uri, keep_uri)
        return True

    except SparqlError as e:
        logger.warning("Failed to merge concepts %s -> %s: %s", remove_uri, keep_uri, e)
        return False
