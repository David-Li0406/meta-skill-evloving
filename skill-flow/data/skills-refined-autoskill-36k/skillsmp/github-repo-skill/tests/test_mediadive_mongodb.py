"""Tests for MediaDive MongoDB client."""

from unittest.mock import MagicMock, patch

import pytest

from cmm_ai_automation.clients.mediadive_mongodb import (
    DEFAULT_DATABASE_NAME,
    DEFAULT_MONGODB_URI,
    MediaDiveMongoClient,
    MediaDiveMongoIngredient,
    MediaDiveMongoLookupError,
    MediaDiveMongoMedium,
    MediaDiveMongoRecipeItem,
    MediaDiveMongoSolution,
    MediaDiveMongoStrainGrowth,
)


class TestMediaDiveMongoIngredient:
    """Tests for MediaDiveMongoIngredient dataclass."""

    def test_create_ingredient(self) -> None:
        """Test creating an ingredient with all fields."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Sodium chloride",
            cas_rn="7647-14-5",
            chebi=26710,
            pubchem=5234,
            kegg="C00535",
            metacyc="NACL",
            formula="NaCl",
            mass=58.44,
            is_complex=False,
            synonyms=["table salt", "halite"],
        )

        assert ingredient.id == 1
        assert ingredient.name == "Sodium chloride"
        assert ingredient.cas_rn == "7647-14-5"
        assert ingredient.chebi == 26710
        assert ingredient.is_complex is False
        assert "table salt" in ingredient.synonyms

    def test_create_minimal_ingredient(self) -> None:
        """Test creating an ingredient with minimal fields."""
        ingredient = MediaDiveMongoIngredient(id=2, name="Unknown compound")

        assert ingredient.id == 2
        assert ingredient.name == "Unknown compound"
        assert ingredient.cas_rn is None
        assert ingredient.chebi is None
        assert ingredient.synonyms == []

    def test_to_dict(self) -> None:
        """Test converting ingredient to dictionary."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="NaCl",
            cas_rn="7647-14-5",
            chebi=26710,
            pubchem=5234,
        )

        d = ingredient.to_dict()

        assert d["mediadive_id"] == 1
        assert d["mediadive_name"] == "NaCl"
        assert d["mediadive_cas_rn"] == "7647-14-5"
        assert d["mediadive_chebi"] == 26710
        assert d["mediadive_pubchem"] == 5234


class TestMediaDiveMongoSolution:
    """Tests for MediaDiveMongoSolution dataclass."""

    def test_create_solution(self) -> None:
        """Test creating a solution."""
        solution = MediaDiveMongoSolution(
            id=100,
            name="10x PBS",
            volume=1000.0,
            recipe=[{"compound": "NaCl", "g_l": 80.0}],
            steps=[{"step": 1, "description": "Dissolve"}],
        )

        assert solution.id == 100
        assert solution.name == "10x PBS"
        assert solution.volume == 1000.0
        assert len(solution.recipe) == 1
        assert len(solution.steps) == 1

    def test_to_curie(self) -> None:
        """Test generating CURIE for solution."""
        solution = MediaDiveMongoSolution(id=123, name="Test solution")
        assert solution.to_curie() == "mediadive.solution:123"


class TestMediaDiveMongoMedium:
    """Tests for MediaDiveMongoMedium dataclass."""

    def test_create_medium(self) -> None:
        """Test creating a medium."""
        medium = MediaDiveMongoMedium(
            id=1,
            name="Nutrient Broth",
            complex_medium=True,
            source="DSMZ",
            link="https://example.com",
            min_ph=6.5,
            max_ph=7.5,
            reference="Smith et al., 2020",
        )

        assert medium.id == 1
        assert medium.name == "Nutrient Broth"
        assert medium.complex_medium is True
        assert medium.min_ph == 6.5
        assert medium.max_ph == 7.5

    def test_to_curie(self) -> None:
        """Test generating CURIE for medium."""
        medium = MediaDiveMongoMedium(id=456, name="Test medium")
        assert medium.to_curie() == "mediadive.medium:456"


class TestMediaDiveMongoStrainGrowth:
    """Tests for MediaDiveMongoStrainGrowth dataclass."""

    def test_create_strain_growth(self) -> None:
        """Test creating a strain growth record."""
        strain = MediaDiveMongoStrainGrowth(
            strain_id=100,
            species="Escherichia coli K-12",
            ccno="DSM:498",
            growth=True,
            bacdive_id=12345,
            domain="B",
        )

        assert strain.strain_id == 100
        assert strain.species == "Escherichia coli K-12"
        assert strain.ccno == "DSM:498"
        assert strain.growth is True
        assert strain.bacdive_id == 12345

    def test_strain_curie_with_bacdive_id(self) -> None:
        """Test strain CURIE when BacDive ID is present."""
        strain = MediaDiveMongoStrainGrowth(
            strain_id=100,
            species="E. coli",
            ccno="DSM:498",
            growth=True,
            bacdive_id=12345,
        )
        assert strain.strain_curie() == "bacdive.strain:12345"

    def test_strain_curie_without_bacdive_id(self) -> None:
        """Test strain CURIE when BacDive ID is absent."""
        strain = MediaDiveMongoStrainGrowth(
            strain_id=100,
            species="E. coli",
            ccno="DSM:498",
            growth=True,
        )
        assert strain.strain_curie() is None


class TestMediaDiveMongoRecipeItem:
    """Tests for MediaDiveMongoRecipeItem dataclass."""

    def test_create_recipe_item_ingredient(self) -> None:
        """Test creating a recipe item for an ingredient."""
        item = MediaDiveMongoRecipeItem(
            compound="NaCl",
            compound_id=10,
            amount=5.0,
            unit="g",
            g_l=5.0,
            optional=False,
        )

        assert item.compound == "NaCl"
        assert item.compound_id == 10
        assert item.g_l == 5.0

    def test_create_recipe_item_solution(self) -> None:
        """Test creating a recipe item for a solution reference."""
        item = MediaDiveMongoRecipeItem(
            compound="",
            solution="10x PBS",
            solution_id=100,
            amount=100.0,
            unit="ml",
        )

        assert item.solution == "10x PBS"
        assert item.solution_id == 100

    def test_ingredient_curie(self) -> None:
        """Test ingredient CURIE."""
        item = MediaDiveMongoRecipeItem(compound="NaCl", compound_id=10)
        assert item.ingredient_curie() == "mediadive.ingredient:10"

        item_no_id = MediaDiveMongoRecipeItem(compound="Unknown")
        assert item_no_id.ingredient_curie() is None

    def test_solution_curie(self) -> None:
        """Test solution CURIE."""
        item = MediaDiveMongoRecipeItem(compound="", solution="PBS", solution_id=100)
        assert item.solution_curie() == "mediadive.solution:100"

        item_no_id = MediaDiveMongoRecipeItem(compound="", solution="PBS")
        assert item_no_id.solution_curie() is None


class TestMediaDiveMongoLookupError:
    """Tests for MediaDiveMongoLookupError dataclass."""

    def test_create_error(self) -> None:
        """Test creating a lookup error."""
        error = MediaDiveMongoLookupError(
            query="ingredient_id:999",
            error_code="NOT_FOUND",
            error_message="Ingredient ID 999 not found",
        )

        assert error.query == "ingredient_id:999"
        assert error.error_code == "NOT_FOUND"
        assert "not found" in error.error_message


class TestMediaDiveMongoClient:
    """Tests for MediaDiveMongoClient."""

    @pytest.fixture
    def mock_mongo(self) -> tuple[MagicMock, MagicMock]:
        """Create a mock MongoDB client and database."""
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_client.__getitem__ = MagicMock(return_value=mock_db)
        return mock_client, mock_db

    def test_init_defaults(self) -> None:
        """Test client initialization with defaults."""
        client = MediaDiveMongoClient()
        assert client.mongodb_uri == DEFAULT_MONGODB_URI
        assert client.database_name == DEFAULT_DATABASE_NAME
        assert client._client is None

    def test_init_custom(self) -> None:
        """Test client initialization with custom values."""
        client = MediaDiveMongoClient(
            mongodb_uri="mongodb://custom:27017",
            database_name="custom_db",
        )
        assert client.mongodb_uri == "mongodb://custom:27017"
        assert client.database_name == "custom_db"

    def test_get_ingredient_by_id_found(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test getting an ingredient by ID when found."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = {
            "_id": 1,
            "name": "Sodium chloride",
            "CAS-RN": "7647-14-5",
            "ChEBI": 26710,
            "PubChem": 5234,
        }

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.get_ingredient_by_id(1)

            assert isinstance(result, MediaDiveMongoIngredient)
            assert result.id == 1
            assert result.name == "Sodium chloride"
            assert result.cas_rn == "7647-14-5"

    def test_get_ingredient_by_id_not_found(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test getting an ingredient by ID when not found."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = None

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.get_ingredient_by_id(999)

            assert isinstance(result, MediaDiveMongoLookupError)
            assert result.error_code == "NOT_FOUND"

    def test_search_ingredients_by_name(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test searching ingredients by name."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find.return_value = [
            {"_id": 1, "name": "Peptone"},
            {"_id": 2, "name": "Peptone from casein"},
        ]

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            results = client.search_ingredients_by_name("peptone")

            assert len(results) == 2
            assert all(isinstance(r, MediaDiveMongoIngredient) for r in results)

    def test_search_ingredients_by_name_exact(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test exact name search."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find.return_value = [{"_id": 1, "name": "Peptone"}]

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            # Call the function - we just need to verify the query pattern
            client.search_ingredients_by_name("Peptone", exact=True)

            # Verify the query used exact match pattern
            call_args = mock_collection.find.call_args
            query = call_args[0][0]
            assert "$regex" in query["name"]
            assert query["name"]["$regex"].startswith("^")
            assert query["name"]["$regex"].endswith("$")

    def test_find_ingredient_by_cas(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test finding ingredient by CAS number."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = {
            "_id": 1,
            "name": "Sodium chloride",
            "CAS-RN": "7647-14-5",
        }

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.find_ingredient_by_cas("7647-14-5")

            assert isinstance(result, MediaDiveMongoIngredient)
            assert result.cas_rn == "7647-14-5"

    def test_find_ingredient_by_cas_not_found(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test finding ingredient by CAS when not found."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = None

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.find_ingredient_by_cas("999-99-9")

            assert result is None

    def test_find_ingredient_by_chebi(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test finding ingredient by ChEBI ID."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = {
            "_id": 1,
            "name": "Water",
            "ChEBI": 15377,
        }

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.find_ingredient_by_chebi(15377)

            assert isinstance(result, MediaDiveMongoIngredient)
            assert result.chebi == 15377

    def test_find_ingredient_by_chebi_with_prefix(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test finding ingredient by ChEBI ID with CHEBI: prefix."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = {
            "_id": 1,
            "name": "Water",
            "ChEBI": 15377,
        }

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.find_ingredient_by_chebi("CHEBI:15377")

            assert isinstance(result, MediaDiveMongoIngredient)

    def test_find_ingredient_by_pubchem(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test finding ingredient by PubChem CID."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.return_value = {
            "_id": 1,
            "name": "Glucose",
            "PubChem": 5793,
        }

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.find_ingredient_by_pubchem(5793)

            assert isinstance(result, MediaDiveMongoIngredient)
            assert result.pubchem == 5793

    def test_close(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test closing the client."""
        mock_client, mock_db = mock_mongo

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            # Force connection
            _ = client._get_db()
            # Close
            client.close()

            mock_client.close.assert_called_once()
            assert client._client is None
            assert client._db is None

    def test_close_without_connection(self) -> None:
        """Test closing client that was never connected."""
        client = MediaDiveMongoClient()
        # Should not raise
        client.close()
        assert client._client is None

    def test_mongodb_error_handling(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test error handling when MongoDB raises exception."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find_one.side_effect = Exception("Connection failed")

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            result = client.get_ingredient_by_id(1)

            assert isinstance(result, MediaDiveMongoLookupError)
            assert result.error_code == "MONGODB_ERROR"
            assert "Connection failed" in result.error_message

    def test_search_error_returns_empty_list(self, mock_mongo: tuple[MagicMock, MagicMock]) -> None:
        """Test that search errors return empty list."""
        mock_client, mock_db = mock_mongo
        mock_collection = MagicMock()
        mock_db.ingredients = mock_collection
        mock_collection.find.side_effect = Exception("Search failed")

        with patch(
            "cmm_ai_automation.clients.mediadive_mongodb.MongoClient",
            return_value=mock_client,
        ):
            client = MediaDiveMongoClient()
            results = client.search_ingredients_by_name("test")

            assert results == []
