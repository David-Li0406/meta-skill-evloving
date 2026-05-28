"""Tests for MediaDive client."""

import tempfile
from pathlib import Path

import pytest

from cmm_ai_automation.clients.mediadive import (
    IngredientResult,
    MediaDiveClient,
    MediaDiveLookupError,
    SolutionResult,
    get_known_ingredient_id,
    get_known_solution_id,
)


class TestMediaDiveClient:
    """Tests for MediaDiveClient."""

    @pytest.fixture
    def client(self) -> MediaDiveClient:
        """Create a MediaDive client for testing."""
        return MediaDiveClient()

    @pytest.mark.mediadive
    def test_get_ingredient_peptone(self, client: MediaDiveClient) -> None:
        """Test looking up peptone (ingredient ID 1)."""
        result = client.get_ingredient(1)

        assert isinstance(result, IngredientResult)
        assert result.id == 1
        assert result.name == "Peptone"
        assert result.cas_rn == "73049-73-7"
        assert result.is_complex is True
        assert "Tryptones" in result.synonyms or "Pepton" in result.synonyms

    @pytest.mark.mediadive
    def test_get_ingredient_casamino_acids(self, client: MediaDiveClient) -> None:
        """Test looking up casamino acids (ingredient ID 101)."""
        result = client.get_ingredient(101)

        assert isinstance(result, IngredientResult)
        assert result.id == 101
        assert result.name == "Casamino acids"
        assert result.is_complex is True

    @pytest.mark.mediadive
    def test_get_ingredient_with_chebi(self, client: MediaDiveClient) -> None:
        """Test looking up Fe(III)-EDTA which has a ChEBI ID."""
        result = client.get_ingredient(952)

        assert isinstance(result, IngredientResult)
        assert result.id == 952
        assert result.name == "Fe(III)-EDTA"
        assert result.chebi == 30729
        assert result.is_complex is False
        assert result.formula == "C10H12FeN2O8"

    @pytest.mark.mediadive
    def test_get_ingredient_not_found(self, client: MediaDiveClient) -> None:
        """Test looking up a nonexistent ingredient."""
        result = client.get_ingredient(999999)

        assert isinstance(result, MediaDiveLookupError)
        assert result.error_code in ("NOT_FOUND", "404")

    @pytest.mark.mediadive
    def test_get_solution_sl6(self, client: MediaDiveClient) -> None:
        """Test looking up trace element solution SL-6."""
        result = client.get_solution(25)

        assert isinstance(result, SolutionResult)
        assert result.id == 25
        assert result.name == "Trace element solution SL-6"
        assert result.volume == 1000
        assert len(result.recipe) > 0

        # Check first recipe item
        first_item = result.recipe[0]
        assert first_item.compound == "ZnSO4 x 7 H2O"
        assert first_item.amount == 0.1
        assert first_item.unit == "g"

    @pytest.mark.mediadive
    def test_get_solution_not_found(self, client: MediaDiveClient) -> None:
        """Test looking up a nonexistent solution."""
        result = client.get_solution(999999)

        assert isinstance(result, MediaDiveLookupError)
        assert result.error_code in ("NOT_FOUND", "404")

    def test_ingredient_result_to_dict(self) -> None:
        """Test IngredientResult serialization."""
        result = IngredientResult(
            id=952,
            name="Fe(III)-EDTA",
            cas_rn="15275-07-7",
            chebi=30729,
            formula="C10H12FeN2O8",
            mass=344.056,
            is_complex=False,
        )

        d = result.to_dict()
        assert d["mediadive_id"] == 952
        assert d["mediadive_name"] == "Fe(III)-EDTA"
        assert d["mediadive_cas_rn"] == "15275-07-7"
        assert d["mediadive_chebi"] == "30729"
        assert d["mediadive_formula"] == "C10H12FeN2O8"
        assert d["mediadive_is_complex"] == "false"


class TestMediaDiveCaching:
    """Tests for MediaDive client caching."""

    def test_cache_saves_and_loads(self) -> None:
        """Test that cache saves and loads correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = Path(tmpdir) / "test_cache.json"

            # Create client with cache
            client = MediaDiveClient(cache_file=cache_file)

            # Manually add to cache
            client._cache["ingredient:1"] = {
                "id": 1,
                "name": "Peptone",
                "CAS-RN": "73049-73-7",
                "complex_compound": 1,
            }
            client.save_cache()

            # Verify file was created
            assert cache_file.exists()

            # Load cache in new client
            client2 = MediaDiveClient(cache_file=cache_file)
            assert "ingredient:1" in client2._cache
            assert client2._cache["ingredient:1"]["name"] == "Peptone"

    @pytest.mark.mediadive
    def test_cache_prevents_duplicate_requests(self) -> None:
        """Test that cached results are returned without API calls."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = Path(tmpdir) / "test_cache.json"

            client = MediaDiveClient(cache_file=cache_file)

            # First request - hits API
            result1 = client.get_ingredient(1)
            assert isinstance(result1, IngredientResult)

            # Should be in cache now
            assert "ingredient:1" in client._cache

            # Second request - should use cache
            result2 = client.get_ingredient(1)
            assert isinstance(result2, IngredientResult)
            assert result1.name == result2.name


class TestKnownIngredients:
    """Tests for known ingredient/solution lookups."""

    def test_get_known_ingredient_id(self) -> None:
        """Test looking up known ingredient IDs."""
        assert get_known_ingredient_id("peptone") == 1
        assert get_known_ingredient_id("Peptone") == 1  # case-insensitive
        assert get_known_ingredient_id("PEPTONE") == 1
        assert get_known_ingredient_id("yeast extract") == 16
        assert get_known_ingredient_id("casamino acids") == 101
        assert get_known_ingredient_id("proteose peptone") == 208
        assert get_known_ingredient_id("unknown thing") is None

    def test_get_known_solution_id(self) -> None:
        """Test looking up known solution IDs."""
        assert get_known_solution_id("trace element solution sl-6") == 25
        assert get_known_solution_id("Trace Element Solution SL-6") == 25
        assert get_known_solution_id("trace element solution sl-10") == 3527
        assert get_known_solution_id("unknown solution") is None

    @pytest.mark.mediadive
    def test_search_ingredients_by_name_known(self) -> None:
        """Test searching for a known ingredient by name."""
        client = MediaDiveClient()
        result = client.search_ingredients_by_name("peptone")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == "Peptone"

    def test_search_ingredients_by_name_unknown(self) -> None:
        """Test searching for an unknown ingredient returns error."""
        client = MediaDiveClient()
        result = client.search_ingredients_by_name("xyznotreal123")

        assert isinstance(result, MediaDiveLookupError)
        assert result.error_code == "NO_SEARCH_API"
