"""Turtle/RDF building functions for knowledge graph operations."""

from __future__ import annotations

# Minimal prefixes for single-statement inserts
_PREFIX_PAPER = "@prefix paper: <https://kg.corca.ai/paper#> ."
_PREFIX_RDFS = "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."


def expand_prefixed_uri(uri: str) -> str:
    """Expand prefixed URI to full URI.

    Args:
        uri: URI string (full https:// or prefixed like paper:co_xxx)

    Returns:
        Full URI (e.g., https://kg.corca.ai/paper#co_xxx)
    """
    if uri.startswith("https://"):
        return uri
    if uri.startswith("paper:"):
        return uri.replace("paper:", "https://kg.corca.ai/paper#", 1)
    return uri


def format_uri_ref(uri: str) -> str:
    """Format URI as Turtle reference (angle brackets for full URIs).

    Args:
        uri: URI string (full https:// or prefixed like paper:co_xxx)

    Returns:
        Formatted URI reference for Turtle
    """
    if uri.startswith("https://"):
        return f"<{uri}>"
    return uri


def build_concept_turtle(concept_uri: str, description: str) -> str:
    """Build Turtle statement for adding concept description.

    Args:
        concept_uri: Full URI of the concept
        description: Description text (should be pre-escaped)

    Returns:
        Turtle statement string
    """
    uri_ref = format_uri_ref(concept_uri)
    return f'{_PREFIX_RDFS}\n{uri_ref} rdfs:comment "{description}" .'


def build_cites_turtle(citing_uri: str, cited_uri: str) -> str:
    """Build Turtle for paper citation relationship.

    Args:
        citing_uri: URI of the citing paper
        cited_uri: URI of the cited paper

    Returns:
        Turtle statement string
    """
    return f"{_PREFIX_PAPER}\n{format_uri_ref(citing_uri)} paper:cites {format_uri_ref(cited_uri)} ."


def build_relation_turtle(from_uri: str, rel_type: str, to_uri: str) -> str:
    """Build Turtle for a relationship between two entities.

    Args:
        from_uri: Subject URI
        rel_type: Relationship type (e.g., 'extends', 'broader')
        to_uri: Object URI

    Returns:
        Turtle statement string
    """
    return f"{_PREFIX_PAPER}\n{format_uri_ref(from_uri)} paper:{rel_type} {format_uri_ref(to_uri)} ."


def build_new_concept_turtle(
    concept_uri: str,
    name: str,
    description: str | None = None,
    paper_uri: str | None = None,
) -> str:
    """Build Turtle for creating a new concept.

    Args:
        concept_uri: URI for the new concept
        name: Concept label (should be pre-escaped)
        description: Optional description (should be pre-escaped)
        paper_uri: Optional paper URI to link concept via paper:about

    Returns:
        Turtle statement string
    """
    lines = [
        _PREFIX_PAPER,
        _PREFIX_RDFS,
        f'{concept_uri} a paper:Concept ;',
        f'    rdfs:label "{name}"',
    ]
    if description:
        lines[-1] += ' ;'
        lines.append(f'    rdfs:comment "{description}"')
    lines[-1] += ' .'

    if paper_uri:
        lines.append(f'{format_uri_ref(paper_uri)} paper:about {concept_uri} .')

    return '\n'.join(lines)


def build_claim_turtle(
    claim_uri: str,
    paper_uri: str,
    claim_text: str,
    concept_uris: list[str] | None = None
) -> str:
    """Build Turtle for a claim with hasClaim and optional regarding links.

    Args:
        claim_uri: URI for the new claim
        paper_uri: URI of the paper making the claim
        claim_text: Text of the claim (should be pre-escaped)
        concept_uris: Optional list of concept URIs this claim is about

    Returns:
        Turtle statement string
    """
    claim_ref = format_uri_ref(claim_uri)
    lines = [
        _PREFIX_PAPER,
        _PREFIX_RDFS,
        f'{claim_ref} a paper:Claim ;',
        f'    rdfs:label "{claim_text}" .',
        f'{format_uri_ref(paper_uri)} paper:hasClaim {claim_ref} .',
    ]
    for uri in concept_uris or []:
        lines.append(f'{claim_ref} paper:regarding {format_uri_ref(uri)} .')
    return '\n'.join(lines)
