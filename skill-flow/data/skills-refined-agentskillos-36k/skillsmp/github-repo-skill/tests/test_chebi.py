"""Tests for ChEBI 2.0 REST API client."""

import pytest

from cmm_ai_automation.clients.chebi import (
    ChEBIClient,
    ChEBICompound,
    ChEBILookupError,
    ChEBISearchResult,
)


class TestChEBIClient:
    """Tests for ChEBIClient."""

    @pytest.fixture
    def client(self) -> ChEBIClient:
        """Create a ChEBI client for testing."""
        return ChEBIClient()

    @pytest.mark.integration
    def test_get_compound_glucose(self, client: ChEBIClient) -> None:
        """Test looking up D-glucose (CHEBI:17634)."""
        result = client.get_compound("CHEBI:17634")

        assert isinstance(result, ChEBICompound)
        assert result.chebi_id == "CHEBI:17634"
        assert result.ascii_name == "D-glucose"
        assert result.definition is not None
        assert result.stars == 3  # 3-star (fully curated)
        assert result.formula == "C6H12O6"
        assert result.mass is not None
        assert 179 < result.mass < 181  # ~180

    @pytest.mark.integration
    def test_get_compound_numeric_id(self, client: ChEBIClient) -> None:
        """Test looking up with numeric ID."""
        result = client.get_compound(17634)

        assert isinstance(result, ChEBICompound)
        assert result.chebi_id == "CHEBI:17634"

    @pytest.mark.integration
    def test_get_compound_string_numeric(self, client: ChEBIClient) -> None:
        """Test looking up with string numeric ID."""
        result = client.get_compound("17634")

        assert isinstance(result, ChEBICompound)
        assert result.chebi_id == "CHEBI:17634"

    @pytest.mark.integration
    def test_get_compound_not_found(self, client: ChEBIClient) -> None:
        """Test looking up a nonexistent compound."""
        result = client.get_compound("CHEBI:999999999")

        assert isinstance(result, ChEBILookupError)
        assert result.error_code == "NOT_FOUND"

    @pytest.mark.integration
    def test_get_compound_with_roles(self, client: ChEBIClient) -> None:
        """Test that roles are parsed correctly."""
        result = client.get_compound("CHEBI:17634")  # D-glucose

        assert isinstance(result, ChEBICompound)
        assert len(result.roles) > 0

        # Should have biological roles
        bio_roles = result.get_biological_roles()
        assert len(bio_roles) > 0

    @pytest.mark.integration
    def test_get_compound_with_cas(self, client: ChEBIClient) -> None:
        """Test that CAS numbers are extracted correctly."""
        result = client.get_compound("CHEBI:17634")  # D-glucose

        assert isinstance(result, ChEBICompound)
        cas_numbers = result.get_cas_numbers()
        assert len(cas_numbers) > 0
        assert "50-99-7" in cas_numbers

    @pytest.mark.integration
    def test_get_compound_synonyms(self, client: ChEBIClient) -> None:
        """Test that synonyms are parsed."""
        result = client.get_compound("CHEBI:17634")

        assert isinstance(result, ChEBICompound)
        assert len(result.synonyms) > 0
        synonyms_lower = [s.lower() for s in result.synonyms]
        assert any("glucose" in s or "dextrose" in s for s in synonyms_lower)

    @pytest.mark.integration
    def test_search_glucose(self, client: ChEBIClient) -> None:
        """Test searching for glucose."""
        results = client.search("glucose", size=5)

        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(r, ChEBISearchResult) for r in results)

        # First result should be highly relevant
        first = results[0]
        assert first.score > 0
        assert "glucose" in (first.ascii_name or "").lower() or "glucose" in first.name.lower()

    @pytest.mark.integration
    def test_search_exact(self, client: ChEBIClient) -> None:
        """Test exact search."""
        result = client.search_exact("D-glucose")

        assert result is not None
        assert isinstance(result, ChEBISearchResult)
        assert result.chebi_id == "CHEBI:17634"

    @pytest.mark.integration
    def test_search_exact_not_found(self, client: ChEBIClient) -> None:
        """Test exact search for nonexistent term."""
        result = client.search_exact("xyznotarealchemical12345")

        assert result is None

    @pytest.mark.integration
    def test_search_by_formula(self, client: ChEBIClient) -> None:
        """Test searching by molecular formula."""
        results = client.search("C6H12O6", size=10)

        assert isinstance(results, list)
        # Should find glucose and other hexoses
        assert len(results) > 0

    @pytest.mark.integration
    def test_compound_ontology_relations(self, client: ChEBIClient) -> None:
        """Test that ontology relations are parsed."""
        result = client.get_compound("CHEBI:17634")

        assert isinstance(result, ChEBICompound)
        # Should have some parent relations
        assert len(result.parents) > 0 or len(result.outgoing_relations) > 0

    def test_compound_to_dict(self) -> None:
        """Test ChEBICompound serialization."""
        from cmm_ai_automation.clients.chebi import ChEBIRole

        compound = ChEBICompound(
            chebi_id="CHEBI:17634",
            name="D-glucose",
            ascii_name="D-glucose",
            definition="A glucose with D-configuration.",
            stars=3,
            formula="C6H12O6",
            mass=180.156,
            roles=[
                ChEBIRole(
                    chebi_id="CHEBI:78675",
                    name="fundamental metabolite",
                    is_biological_role=True,
                )
            ],
            synonyms=["dextrose", "grape sugar"],
        )

        d = compound.to_dict()
        assert d["chebi_id"] == "CHEBI:17634"
        assert d["ascii_name"] == "D-glucose"
        assert d["formula"] == "C6H12O6"
        assert d["stars"] == 3
        assert len(d["roles"]) == 1
        assert d["roles"][0]["is_biological"] is True

    def test_compound_helper_methods(self) -> None:
        """Test helper methods on ChEBICompound."""
        from cmm_ai_automation.clients.chebi import ChEBIDatabaseRef, ChEBIRole

        compound = ChEBICompound(
            chebi_id="CHEBI:17634",
            name="D-glucose",
            roles=[
                ChEBIRole("CHEBI:1", "bio role", is_biological_role=True),
                ChEBIRole("CHEBI:2", "chem role", is_chemical_role=True),
                ChEBIRole("CHEBI:3", "another bio", is_biological_role=True),
            ],
            database_refs={
                "CAS": [
                    ChEBIDatabaseRef("CAS", "50-99-7", "NIST"),
                    ChEBIDatabaseRef("CAS", "50-99-7", "ChemIDplus"),  # duplicate
                ]
            },
        )

        bio_roles = compound.get_biological_roles()
        assert len(bio_roles) == 2

        chem_roles = compound.get_chemical_roles()
        assert len(chem_roles) == 1

        cas_numbers = compound.get_cas_numbers()
        assert cas_numbers == ["50-99-7"]  # deduped
