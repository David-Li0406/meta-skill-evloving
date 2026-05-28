"""PydanticAI agent for strain entity reconciliation.

This module provides LLM-powered entity resolution for microbial strains,
helping match records across different data sources with varying naming
conventions, identifier schemes, and taxonomic classifications.

Example use cases:
- Match "Sinorhizobium meliloti 2011" to BacDive entry for "Ensifer meliloti DSM 1981"
- Recognize that genus "Sinorhizobium" is a synonym of "Ensifer"
- Identify that strain designations "2011", "SU47", "DSM 1981" refer to the same isolate
- Link species-level NCBI taxon IDs to strain-level records
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from pydantic_ai import Agent

logger = logging.getLogger(__name__)


class MatchConfidence(str, Enum):
    """Confidence level for entity matches."""

    HIGH = "high"  # Very likely the same entity (>90%)
    MEDIUM = "medium"  # Probably the same entity (60-90%)
    LOW = "low"  # Possibly the same entity (30-60%)
    NONE = "none"  # Unlikely to be the same entity (<30%)


class ReconciliationResult(BaseModel):
    """Result of an entity reconciliation comparison."""

    is_match: bool = Field(description="Whether the two records refer to the same entity")
    confidence: MatchConfidence = Field(description="Confidence level of the match assessment")
    reasoning: str = Field(description="Explanation of why the records match or don't match")
    matched_fields: list[str] = Field(
        default_factory=list,
        description="Fields that contributed to the match (e.g., 'genus synonym', 'strain designation')",
    )
    conflicts: list[str] = Field(
        default_factory=list,
        description="Fields that conflict between records",
    )
    suggested_canonical_id: str | None = Field(
        default=None,
        description="Suggested canonical identifier if records match (prefer NCBI > BacDive > culture collection)",
    )


@dataclass
class StrainCandidate:
    """A candidate strain record for comparison."""

    source: str  # e.g., "input_sheet", "bacdive", "ncbi"
    identifier: str | None  # Primary ID if known
    name: str | None  # Full name
    scientific_name: str | None  # Binomial name
    strain_designation: str | None  # e.g., "DSM 1981", "2011", "SU47"
    ncbi_taxon_id: str | None  # NCBITaxon ID
    synonyms: list[str]  # Name synonyms
    culture_collection_ids: list[str]  # e.g., ["DSM:1981", "ATCC:9930"]
    extra: dict[str, Any] | None = None  # Additional context

    def to_prompt_dict(self) -> dict[str, Any]:
        """Convert to dictionary for prompt inclusion."""
        return {
            "source": self.source,
            "identifier": self.identifier,
            "name": self.name,
            "scientific_name": self.scientific_name,
            "strain_designation": self.strain_designation,
            "ncbi_taxon_id": self.ncbi_taxon_id,
            "synonyms": self.synonyms,
            "culture_collection_ids": self.culture_collection_ids,
        }


# System prompt for the reconciliation agent
RECONCILIATION_SYSTEM_PROMPT = """You are an expert microbiologist and bioinformatician specializing in
bacterial taxonomy and strain identification. Your task is to determine whether two strain records
from different data sources refer to the same microbial isolate.

Key knowledge you should apply:

1. **Genus synonyms**: Many bacterial genera have been reclassified. For example:
   - Sinorhizobium = Ensifer (synonyms)
   - Methylobacterium = Methylorubrum (for some species)
   - Pseudomonas fluorescens complex has many reclassified species

2. **Strain designations**: The same strain may have multiple designations:
   - Culture collection numbers (DSM, ATCC, JCM, etc.)
   - Lab strain names (2011, SU47, PA1, etc.)
   - Type strain designations (T, type, etc.)

3. **NCBI Taxonomy**:
   - Species-level taxon IDs (e.g., 382 for Ensifer meliloti) vs
   - Strain-level taxon IDs (e.g., 1286640 for strain 2011)
   - Both can refer to the same strain at different taxonomic resolution

4. **Name variations**:
   - Spelling variants (Methylobrum vs Methylorubrum)
   - Authority differences
   - Old vs new nomenclature

When analyzing records:
- Look for culture collection ID matches (strong evidence)
- Consider genus synonymy
- Check if strain designations match across sources
- Note if one has strain-level NCBI ID and other has species-level

Return a structured assessment with confidence level and reasoning.
"""


class StrainReconciler:
    """PydanticAI-powered strain entity reconciliation agent."""

    def __init__(self, model: str = "openai:gpt-4o-mini"):
        """Initialize the reconciliation agent.

        Args:
            model: PydanticAI model identifier (e.g., "openai:gpt-4o-mini", "anthropic:claude-3-haiku")
        """
        self.agent = Agent(
            model,
            output_type=ReconciliationResult,
            system_prompt=RECONCILIATION_SYSTEM_PROMPT,
        )

    async def compare_strains(
        self,
        record_a: StrainCandidate,
        record_b: StrainCandidate,
    ) -> ReconciliationResult:
        """Compare two strain records to determine if they're the same entity.

        Args:
            record_a: First strain record (typically from input sheet)
            record_b: Second strain record (typically from BacDive or other source)

        Returns:
            ReconciliationResult with match assessment and reasoning
        """
        prompt = f"""Compare these two strain records and determine if they refer to the same microbial isolate:

**Record A** (from {record_a.source}):
{record_a.to_prompt_dict()}

**Record B** (from {record_b.source}):
{record_b.to_prompt_dict()}

Analyze the records and provide your assessment. Consider genus synonyms, strain designation
variations, and NCBI taxonomy levels. Return your structured assessment.
"""
        result = await self.agent.run(prompt)
        return result.output  # type: ignore[no-any-return]

    def compare_strains_sync(
        self,
        record_a: StrainCandidate,
        record_b: StrainCandidate,
    ) -> ReconciliationResult:
        """Synchronous version of compare_strains.

        Args:
            record_a: First strain record
            record_b: Second strain record

        Returns:
            ReconciliationResult with match assessment and reasoning
        """
        import asyncio

        return asyncio.run(self.compare_strains(record_a, record_b))

    async def find_best_match(
        self,
        target: StrainCandidate,
        candidates: list[StrainCandidate],
        min_confidence: MatchConfidence = MatchConfidence.MEDIUM,
    ) -> tuple[StrainCandidate | None, ReconciliationResult | None]:
        """Find the best matching candidate for a target strain.

        Args:
            target: The strain record to find a match for
            candidates: List of potential matches
            min_confidence: Minimum confidence level to accept a match

        Returns:
            Tuple of (best_match, result) or (None, None) if no match found
        """
        confidence_order = [MatchConfidence.HIGH, MatchConfidence.MEDIUM, MatchConfidence.LOW]
        min_index = confidence_order.index(min_confidence)

        best_match = None
        best_result = None
        best_confidence_index = len(confidence_order)

        for candidate in candidates:
            result = await self.compare_strains(target, candidate)

            if result.is_match:
                conf_index = confidence_order.index(result.confidence)
                if conf_index <= min_index and conf_index < best_confidence_index:
                    best_match = candidate
                    best_result = result
                    best_confidence_index = conf_index

                    # Early exit on HIGH confidence match
                    if result.confidence == MatchConfidence.HIGH:
                        break

        return best_match, best_result
