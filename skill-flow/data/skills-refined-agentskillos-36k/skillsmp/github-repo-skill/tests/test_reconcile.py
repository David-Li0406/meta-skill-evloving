"""Tests for strain reconciliation agent."""

import os

import pytest

from cmm_ai_automation.reconcile.agent import (
    MatchConfidence,
    ReconciliationResult,
    StrainCandidate,
    StrainReconciler,
)


class TestStrainCandidate:
    """Tests for StrainCandidate dataclass."""

    def test_create_candidate(self) -> None:
        """Test creating a strain candidate."""
        candidate = StrainCandidate(
            source="input_sheet",
            identifier="NCBITaxon:1286640",
            name="Sinorhizobium meliloti 2011",
            scientific_name="Sinorhizobium meliloti",
            strain_designation="2011",
            ncbi_taxon_id="1286640",
            synonyms=[],
            culture_collection_ids=[],
        )
        assert candidate.source == "input_sheet"
        assert candidate.strain_designation == "2011"

    def test_to_prompt_dict(self) -> None:
        """Test converting candidate to prompt dictionary."""
        candidate = StrainCandidate(
            source="bacdive",
            identifier="bacdive:13541",
            name="Ensifer meliloti DSM 1981",
            scientific_name="Ensifer meliloti",
            strain_designation="DSM 1981",
            ncbi_taxon_id="382",
            synonyms=["Sinorhizobium meliloti", "Rhizobium meliloti"],
            culture_collection_ids=["DSM:1981"],
        )
        d = candidate.to_prompt_dict()
        assert d["source"] == "bacdive"
        assert d["synonyms"] == ["Sinorhizobium meliloti", "Rhizobium meliloti"]
        assert "extra" not in d  # extra is excluded


class TestReconciliationResult:
    """Tests for ReconciliationResult model."""

    def test_create_result(self) -> None:
        """Test creating a reconciliation result."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.HIGH,
            reasoning="Genus Sinorhizobium is a synonym of Ensifer. Strain 2011 is also known as SU47 and DSM 1981.",
            matched_fields=["genus_synonym", "strain_designation"],
            conflicts=[],
            suggested_canonical_id="NCBITaxon:1286640",
        )
        assert result.is_match is True
        assert result.confidence == MatchConfidence.HIGH
        assert "DSM 1981" in result.reasoning


class TestMatchConfidence:
    """Tests for MatchConfidence enum."""

    def test_confidence_values(self) -> None:
        """Test confidence enum values."""
        assert MatchConfidence.HIGH.value == "high"
        assert MatchConfidence.MEDIUM.value == "medium"
        assert MatchConfidence.LOW.value == "low"
        assert MatchConfidence.NONE.value == "none"


@pytest.fixture
def sinorhizobium_input_record() -> StrainCandidate:
    """Input sheet record for Sinorhizobium meliloti 2011."""
    return StrainCandidate(
        source="input_sheet",
        identifier="NCBITaxon:1286640",
        name="Sinorhizobium meliloti 2011",
        scientific_name="Sinorhizobium meliloti",
        strain_designation="2011",
        ncbi_taxon_id="1286640",
        synonyms=[],
        culture_collection_ids=[],
    )


@pytest.fixture
def ensifer_bacdive_record() -> StrainCandidate:
    """BacDive record for Ensifer meliloti DSM 1981 (same strain, different name)."""
    return StrainCandidate(
        source="bacdive",
        identifier="bacdive:13541",
        name="Ensifer meliloti DSM 1981",
        scientific_name="Ensifer meliloti",
        strain_designation="DSM 1981",
        ncbi_taxon_id="382",
        synonyms=["Sinorhizobium meliloti", "Rhizobium meliloti", "Ensifer kummerowiae"],
        culture_collection_ids=["DSM:1981"],
        extra={"strain_history": "SU 47"},  # Historical strain name
    )


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set; skipping OpenAI-dependent tests",
)
class TestStrainReconcilerIntegration:
    """Integration tests for StrainReconciler (requires API access)."""

    @pytest.mark.asyncio
    async def test_compare_sinorhizobium_ensifer(
        self,
        sinorhizobium_input_record: StrainCandidate,
        ensifer_bacdive_record: StrainCandidate,
    ) -> None:
        """Test comparing Sinorhizobium meliloti 2011 vs Ensifer meliloti DSM 1981.

        These are the SAME strain but with:
        - Different genus names (Sinorhizobium vs Ensifer - synonyms)
        - Different strain designations (2011 vs DSM 1981 - both valid)
        - Different NCBI taxon IDs (1286640 strain-level vs 382 species-level)
        """
        reconciler = StrainReconciler()
        result = await reconciler.compare_strains(
            sinorhizobium_input_record,
            ensifer_bacdive_record,
        )

        # The LLM should recognize these as the same strain
        assert result.is_match is True
        assert result.confidence in [MatchConfidence.HIGH, MatchConfidence.MEDIUM]
        assert len(result.reasoning) > 0

        # Should identify genus synonymy as evidence
        matched_lower = [f.lower() for f in result.matched_fields]
        assert any("synonym" in f or "genus" in f for f in matched_lower) or "synonym" in result.reasoning.lower()

    @pytest.mark.asyncio
    async def test_compare_different_strains(self) -> None:
        """Test comparing genuinely different strains."""
        strain_a = StrainCandidate(
            source="input_sheet",
            identifier="NCBITaxon:123",
            name="Escherichia coli K-12",
            scientific_name="Escherichia coli",
            strain_designation="K-12",
            ncbi_taxon_id="123",
            synonyms=[],
            culture_collection_ids=["ATCC:10798"],
        )

        strain_b = StrainCandidate(
            source="bacdive",
            identifier="bacdive:999",
            name="Bacillus subtilis 168",
            scientific_name="Bacillus subtilis",
            strain_designation="168",
            ncbi_taxon_id="456",
            synonyms=[],
            culture_collection_ids=["ATCC:6633"],
        )

        reconciler = StrainReconciler()
        result = await reconciler.compare_strains(strain_a, strain_b)

        # Should clearly recognize these as different organisms
        assert result.is_match is False
        assert result.confidence == MatchConfidence.NONE
