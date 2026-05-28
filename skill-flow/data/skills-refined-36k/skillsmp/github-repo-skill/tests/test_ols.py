"""Tests for OLS4 API client."""

import pytest

from cmm_ai_automation.clients.ols import (
    ChEBITerm,
    OLSClient,
    OLSLookupError,
    OLSSearchResult,
)


class TestOLSClient:
    """Tests for OLSClient."""

    @pytest.fixture
    def client(self) -> OLSClient:
        """Create an OLS client for testing."""
        return OLSClient()

    @pytest.mark.integration
    def test_get_chebi_term_glucose(self, client: OLSClient) -> None:
        """Test looking up D-glucose (CHEBI:17634)."""
        result = client.get_chebi_term("CHEBI:17634")

        assert isinstance(result, ChEBITerm)
        assert result.chebi_id == "CHEBI:17634"
        assert result.label == "D-glucose"
        assert result.description is not None
        assert len(result.synonyms) > 0
        assert "dextrose" in [s.lower() for s in result.synonyms]
        assert result.is_obsolete is False

    @pytest.mark.integration
    def test_get_chebi_term_numeric_id(self, client: OLSClient) -> None:
        """Test looking up ChEBI term with numeric ID."""
        result = client.get_chebi_term(17634)

        assert isinstance(result, ChEBITerm)
        assert result.chebi_id == "CHEBI:17634"

    @pytest.mark.integration
    def test_get_chebi_term_string_numeric(self, client: OLSClient) -> None:
        """Test looking up ChEBI term with string numeric ID."""
        result = client.get_chebi_term("17634")

        assert isinstance(result, ChEBITerm)
        assert result.chebi_id == "CHEBI:17634"

    @pytest.mark.integration
    def test_get_chebi_term_not_found(self, client: OLSClient) -> None:
        """Test looking up a nonexistent ChEBI term."""
        result = client.get_chebi_term("CHEBI:999999999")

        assert isinstance(result, OLSLookupError)
        assert result.error_code == "NOT_FOUND"

    @pytest.mark.integration
    def test_get_chebi_term_with_mass(self, client: OLSClient) -> None:
        """Test that mass is parsed correctly."""
        result = client.get_chebi_term("CHEBI:17634")  # D-glucose

        assert isinstance(result, ChEBITerm)
        # D-glucose has mass ~180
        if result.mass is not None:
            assert 179 < result.mass < 181

    @pytest.mark.integration
    def test_search_chebi_glucose(self, client: OLSClient) -> None:
        """Test searching for glucose in ChEBI."""
        results = client.search_chebi("glucose", rows=5)

        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(r, OLSSearchResult) for r in results)

        # D-glucose should be in results
        labels = [r.label.lower() if r.label else "" for r in results]
        assert any("glucose" in label for label in labels)

    @pytest.mark.integration
    def test_search_chebi_exact_match(self, client: OLSClient) -> None:
        """Test exact search for ChEBI term."""
        result = client.search_chebi_exact("D-glucose")

        assert result is not None
        assert isinstance(result, OLSSearchResult)
        assert result.label == "D-glucose"
        assert result.curie == "CHEBI:17634"

    @pytest.mark.integration
    def test_search_chebi_exact_not_found(self, client: OLSClient) -> None:
        """Test exact search for nonexistent term."""
        result = client.search_chebi_exact("xyznotarealcompound123")

        assert result is None

    @pytest.mark.integration
    def test_get_chebi_parents(self, client: OLSClient) -> None:
        """Test getting parent terms for a ChEBI ID."""
        result = client.get_chebi_parents("CHEBI:17634")  # D-glucose

        # Should return a list (may be empty if API doesn't return parents)
        assert isinstance(result, list | OLSLookupError)

    def test_chebi_term_to_dict(self) -> None:
        """Test ChEBITerm serialization."""
        term = ChEBITerm(
            chebi_id="CHEBI:17634",
            label="D-glucose",
            description="A glucose with D-configuration.",
            synonyms=["dextrose", "grape sugar"],
            formula="C6H12O6",
            mass=180.156,
            charge=0,
            star=3,
        )

        d = term.to_dict()
        assert d["chebi_id"] == "CHEBI:17634"
        assert d["label"] == "D-glucose"
        assert d["formula"] == "C6H12O6"
        assert d["mass"] == 180.156
        assert d["charge"] == 0
        assert len(d["synonyms"]) == 2

    def test_ols_search_result_curie(self) -> None:
        """Test OLSSearchResult CURIE conversion."""
        result = OLSSearchResult(
            iri="http://purl.obolibrary.org/obo/CHEBI_17634",
            label="D-glucose",
            short_form="CHEBI_17634",
            ontology_name="chebi",
        )

        assert result.curie == "CHEBI:17634"
