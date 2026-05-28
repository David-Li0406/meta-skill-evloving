"""LLM prompt building functions."""

from __future__ import annotations

from typing import Any


def _format_year_suffix(year: int | None) -> str:
    """Format year as parenthetical suffix or empty string.

    Args:
        year: Publication year or None

    Returns:
        ' (year)' if year is provided, else ''
    """
    return f" ({year})" if year else ""


def format_claim_line(claim: dict[str, str]) -> str:
    """Format a claim as a prompt line.

    Args:
        claim: Dict with 'uri' and 'text' keys

    Returns:
        Formatted string like '- [uri] "text"'
    """
    return f"- [{claim['uri']}] \"{claim['text']}\""


def format_ref_claim_line(ref_claim: dict[str, Any]) -> str:
    """Format a reference claim as a prompt line with optional year and context.

    Args:
        ref_claim: Dict with 'claim_uri', 'claim_text', optional 'paper_year',
                   and optional 'citation_context'

    Returns:
        Formatted string like '- [uri] (year) "text"' with optional context
    """
    year_suffix = _format_year_suffix(ref_claim.get('paper_year'))
    line = f"- [{ref_claim['claim_uri']}]{year_suffix} \"{ref_claim['claim_text']}\""

    # Add citation context if available
    ctx = ref_claim.get('citation_context')
    if ctx:
        intents = ctx.get('intents', [])
        snippet = ctx.get('snippet')
        if intents or snippet:
            ctx_parts = []
            if intents:
                ctx_parts.append(f"intent: {', '.join(intents)}")
            if snippet:
                # Truncate long snippets
                short_snippet = snippet[:200] + "..." if len(snippet) > 200 else snippet
                ctx_parts.append(f'context: "{short_snippet}"')
            line += f"\n  Citation: {'; '.join(ctx_parts)}"

    return line


def build_ref_claims_context(ref_claims: list[dict[str, Any]], limit: int = 20) -> str:
    """Build reference claims context for prompts.

    Args:
        ref_claims: List of reference claim dictionaries
        limit: Maximum number of claims to include

    Returns:
        Formatted context string, empty if no claims
    """
    if not ref_claims:
        return ""
    lines = [f"- [{rc['claim_uri']}] \"{rc['claim_text']}\"" for rc in ref_claims[:limit]]
    return "\n\nClaims from papers this paper cites:\n" + "\n".join(lines)


def build_claim_relations_prompt(
    my_claims: list[dict[str, str]],
    ref_claims: list[dict[str, Any]],
    paper_year: int | None,
    claim_relation_definitions: str,
    limit: int = 20
) -> str:
    """Build prompt for finding claim relations."""
    my_section = "\n".join(format_claim_line(c) for c in my_claims)
    ref_section = "\n".join(format_ref_claim_line(rc) for rc in ref_claims[:limit])

    return f"""Find relationships between claims from this paper and claims from papers it cites.

## This paper's claims{_format_year_suffix(paper_year)}:
{my_section}

## Claims from cited papers (with publication year):
{ref_section}

## Relationship types:
{claim_relation_definitions}

## Important
- Only include clear, meaningful relationships. Use EXACT URIs from the lists above.
- This paper can only extend/refute/support claims from EARLIER papers (check years).
- Do not create relations if the semantic connection is weak or speculative.
- When citation context is provided (intent and/or context snippet), use it to understand HOW this paper uses the cited work:
  - "background" intent: cited for general context, less likely to have extends/refutes relations
  - "methodology" intent: cited for methods used, more likely to have extends/supports relations
  - "result" intent: cited for comparison of results, look for extends/refutes/supports relations
  - The context snippet shows the actual text where the citation occurs"""


def build_extraction_prompt(
    title: str,
    abstract: str,
    year: int | None,
    ref_claims_context: str,
    claim_relation_definitions: str,
) -> str:
    """Build prompt for extracting concepts and claims from a paper.

    Args:
        title: Paper title
        abstract: Paper abstract
        year: Publication year (or None)
        ref_claims_context: Formatted context of referenced claims
        claim_relation_definitions: Text defining extends/refutes/supports

    Returns:
        Formatted prompt string
    """
    return f"""Extract concepts and claims from this research paper.

Title: {title}
Year: {year or 'Unknown'}
Abstract: {abstract}{ref_claims_context}

## Concepts
Extract key technical concepts (methods, models, techniques, theories). For each concept:
- description: Write a general, standalone definition (1-2 sentences) that does NOT reference
  this specific paper. Avoid phrases like "In this research...", "The proposed method...",
  "This study...", "The authors...". The definition should make sense without paper context.
  Be specific and technical.
- broader: taxonomic is-a parent (e.g., "CNN" has broader "neural network")
- partOf: the whole containing this part (e.g., "attention mechanism" partOf "transformer")
- dependsOn: prerequisite concept (e.g., "fine-tuning" dependsOn "pre-trained model")

Use null if no relationship applies. Relationships should be to OTHER concepts you're extracting or well-known concepts.

## Claims
Extract main findings or contributions as specific, verifiable statements. Examples:
- "Self-attention achieves O(1) sequential operations compared to O(n) for RNNs"
- "The proposed method outperforms BERT by 2.3% on GLUE benchmark"

For each claim:
1. List which concepts (from above) the claim is about in `regarding` (use exact concept names, can be empty if none apply)
2. Check if it relates to referenced claims:
{claim_relation_definitions}

Use the exact claim_uri in brackets for extends/refutes/supports. Use null if no relationship exists.

## Important
- Only extract claims EXPLICITLY stated in the abstract. Do not infer, speculate, or add claims not directly supported by the text.
- Keep claim text concise but complete enough to be understood without the paper context.
- If the abstract lacks concrete findings (e.g., only describes methodology), extract fewer claims rather than fabricating them."""
