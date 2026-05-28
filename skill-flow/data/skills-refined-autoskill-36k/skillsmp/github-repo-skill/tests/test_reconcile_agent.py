"""Tests for reconciliation agent data structures."""

from cmm_ai_automation.reconcile.agent import (
    MatchConfidence,
    ReconciliationResult,
    StrainCandidate,
)


class TestMatchConfidence:
    """Tests for MatchConfidence enum."""

    def test_confidence_levels(self) -> None:
        """Test that confidence levels have expected values."""
        assert MatchConfidence.HIGH.value == "high"
        assert MatchConfidence.MEDIUM.value == "medium"
        assert MatchConfidence.LOW.value == "low"
        assert MatchConfidence.NONE.value == "none"

    def test_confidence_ordering(self) -> None:
        """Test that we can work with confidence levels."""
        levels = [MatchConfidence.HIGH, MatchConfidence.MEDIUM, MatchConfidence.LOW, MatchConfidence.NONE]
        assert len(levels) == 4
        assert MatchConfidence.HIGH in levels


class TestReconciliationResult:
    """Tests for ReconciliationResult Pydantic model."""

    def test_create_match_result(self) -> None:
        """Test creating a positive match result."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.HIGH,
            reasoning="Culture collection IDs match exactly",
            matched_fields=["culture_collection_id", "strain_designation"],
            conflicts=[],
            suggested_canonical_id="NCBITaxon:123456",
        )

        assert result.is_match is True
        assert result.confidence == MatchConfidence.HIGH
        assert result.reasoning == "Culture collection IDs match exactly"
        assert len(result.matched_fields) == 2
        assert "culture_collection_id" in result.matched_fields
        assert len(result.conflicts) == 0
        assert result.suggested_canonical_id == "NCBITaxon:123456"

    def test_create_no_match_result(self) -> None:
        """Test creating a negative match result."""
        result = ReconciliationResult(
            is_match=False,
            confidence=MatchConfidence.NONE,
            reasoning="Different genera, no overlapping identifiers",
            matched_fields=[],
            conflicts=["genus", "species"],
        )

        assert result.is_match is False
        assert result.confidence == MatchConfidence.NONE
        assert len(result.matched_fields) == 0
        assert len(result.conflicts) == 2
        assert "genus" in result.conflicts

    def test_default_fields(self) -> None:
        """Test that optional fields have correct defaults."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.MEDIUM,
            reasoning="Partial match",
        )

        assert result.matched_fields == []
        assert result.conflicts == []
        assert result.suggested_canonical_id is None

    def test_model_to_dict(self) -> None:
        """Test converting result to dictionary."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.HIGH,
            reasoning="Test",
            matched_fields=["field1"],
        )

        d = result.model_dump()
        assert d["is_match"] is True
        assert d["confidence"] == "high"
        assert d["reasoning"] == "Test"
        assert d["matched_fields"] == ["field1"]


class TestStrainCandidate:
    """Tests for StrainCandidate dataclass."""

    def test_create_minimal_candidate(self) -> None:
        """Test creating candidate with minimal fields."""
        candidate = StrainCandidate(
            source="test_source",
            identifier=None,
            name=None,
            scientific_name=None,
            strain_designation=None,
            ncbi_taxon_id=None,
            synonyms=[],
            culture_collection_ids=[],
        )

        assert candidate.source == "test_source"
        assert candidate.identifier is None
        assert candidate.name is None
        assert candidate.synonyms == []
        assert candidate.extra is None

    def test_create_full_candidate(self) -> None:
        """Test creating candidate with all fields."""
        candidate = StrainCandidate(
            source="bacdive",
            identifier="bacdive:12345",
            name="Ensifer meliloti DSM 1981",
            scientific_name="Ensifer meliloti",
            strain_designation="DSM 1981",
            ncbi_taxon_id="NCBITaxon:1286640",
            synonyms=["Sinorhizobium meliloti", "Rhizobium meliloti"],
            culture_collection_ids=["DSM:1981", "ATCC:9930"],
            extra={"genome_id": "GCA_000006965.1"},
        )

        assert candidate.source == "bacdive"
        assert candidate.identifier == "bacdive:12345"
        assert candidate.name == "Ensifer meliloti DSM 1981"
        assert candidate.scientific_name == "Ensifer meliloti"
        assert candidate.strain_designation == "DSM 1981"
        assert candidate.ncbi_taxon_id == "NCBITaxon:1286640"
        assert len(candidate.synonyms) == 2
        assert "Sinorhizobium meliloti" in candidate.synonyms
        assert len(candidate.culture_collection_ids) == 2
        assert "DSM:1981" in candidate.culture_collection_ids
        assert candidate.extra is not None
        assert candidate.extra["genome_id"] == "GCA_000006965.1"

    def test_to_prompt_dict(self) -> None:
        """Test converting candidate to prompt dictionary."""
        candidate = StrainCandidate(
            source="input_sheet",
            identifier="DSM:1981",
            name="Test strain",
            scientific_name="Bacterium test",
            strain_designation="TEST1",
            ncbi_taxon_id="NCBITaxon:123",
            synonyms=["Synonym 1", "Synonym 2"],
            culture_collection_ids=["DSM:1981", "ATCC:100"],
            extra={"some_field": "value"},  # Should not be in prompt dict
        )

        prompt_dict = candidate.to_prompt_dict()

        assert prompt_dict["source"] == "input_sheet"
        assert prompt_dict["identifier"] == "DSM:1981"
        assert prompt_dict["name"] == "Test strain"
        assert prompt_dict["scientific_name"] == "Bacterium test"
        assert prompt_dict["strain_designation"] == "TEST1"
        assert prompt_dict["ncbi_taxon_id"] == "NCBITaxon:123"
        assert prompt_dict["synonyms"] == ["Synonym 1", "Synonym 2"]
        assert prompt_dict["culture_collection_ids"] == ["DSM:1981", "ATCC:100"]
        # extra should not be in prompt dict
        assert "extra" not in prompt_dict

    def test_to_prompt_dict_with_none_values(self) -> None:
        """Test prompt dict includes None values for missing fields."""
        candidate = StrainCandidate(
            source="test",
            identifier=None,
            name="Test",
            scientific_name=None,
            strain_designation=None,
            ncbi_taxon_id=None,
            synonyms=[],
            culture_collection_ids=[],
        )

        prompt_dict = candidate.to_prompt_dict()

        assert prompt_dict["identifier"] is None
        assert prompt_dict["scientific_name"] is None
        assert prompt_dict["strain_designation"] is None
        assert prompt_dict["ncbi_taxon_id"] is None
        assert prompt_dict["synonyms"] == []

    def test_candidate_with_empty_lists(self) -> None:
        """Test candidate handles empty lists correctly."""
        candidate = StrainCandidate(
            source="test",
            identifier="test:1",
            name="Test",
            scientific_name="Test test",
            strain_designation="T1",
            ncbi_taxon_id="NCBITaxon:1",
            synonyms=[],
            culture_collection_ids=[],
        )

        assert candidate.synonyms == []
        assert candidate.culture_collection_ids == []
        prompt_dict = candidate.to_prompt_dict()
        assert prompt_dict["synonyms"] == []
        assert prompt_dict["culture_collection_ids"] == []

    def test_candidate_sources(self) -> None:
        """Test different source types."""
        sources = ["input_sheet", "bacdive", "ncbi", "mediadive", "custom"]
        for source in sources:
            candidate = StrainCandidate(
                source=source,
                identifier=None,
                name=None,
                scientific_name=None,
                strain_designation=None,
                ncbi_taxon_id=None,
                synonyms=[],
                culture_collection_ids=[],
            )
            assert candidate.source == source
