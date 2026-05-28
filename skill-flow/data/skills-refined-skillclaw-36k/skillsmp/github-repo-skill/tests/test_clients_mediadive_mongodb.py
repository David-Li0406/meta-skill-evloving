"""Tests for MediaDive MongoDB client data structures."""

from cmm_ai_automation.clients.mediadive_mongodb import MediaDiveMongoIngredient


class TestMediaDiveMongoIngredient:
    """Tests for MediaDiveMongoIngredient dataclass."""

    def test_create_minimal_ingredient(self) -> None:
        """Test creating ingredient with only required fields."""
        ingredient = MediaDiveMongoIngredient(id=1, name="Test ingredient")

        assert ingredient.id == 1
        assert ingredient.name == "Test ingredient"
        assert ingredient.cas_rn is None
        assert ingredient.chebi is None
        assert ingredient.pubchem is None
        assert ingredient.kegg is None
        assert ingredient.metacyc is None
        assert ingredient.formula is None
        assert ingredient.mass is None
        assert ingredient.is_complex is False
        assert ingredient.synonyms == []

    def test_create_full_ingredient(self) -> None:
        """Test creating ingredient with all fields."""
        ingredient = MediaDiveMongoIngredient(
            id=42,
            name="D-glucose",
            cas_rn="50-99-7",
            chebi=17634,
            pubchem=5793,
            kegg="C00031",
            metacyc="GLUCOSE",
            formula="C6H12O6",
            mass=180.156,
            is_complex=False,
            synonyms=["glucose", "dextrose", "grape sugar"],
        )

        assert ingredient.id == 42
        assert ingredient.name == "D-glucose"
        assert ingredient.cas_rn == "50-99-7"
        assert ingredient.chebi == 17634
        assert ingredient.pubchem == 5793
        assert ingredient.kegg == "C00031"
        assert ingredient.metacyc == "GLUCOSE"
        assert ingredient.formula == "C6H12O6"
        assert ingredient.mass == 180.156
        assert ingredient.is_complex is False
        assert len(ingredient.synonyms) == 3
        assert "glucose" in ingredient.synonyms

    def test_to_dict_minimal(self) -> None:
        """Test converting minimal ingredient to dictionary."""
        ingredient = MediaDiveMongoIngredient(id=1, name="Test")
        d = ingredient.to_dict()

        assert d["mediadive_id"] == 1
        assert d["mediadive_name"] == "Test"
        assert d["mediadive_cas_rn"] is None
        assert d["mediadive_chebi"] is None
        assert d["mediadive_pubchem"] is None
        assert d["mediadive_kegg"] is None
        assert d["mediadive_metacyc"] is None
        assert d["mediadive_formula"] is None
        assert d["mediadive_mass"] is None
        assert d["mediadive_is_complex"] is False

    def test_to_dict_full(self) -> None:
        """Test converting full ingredient to dictionary."""
        ingredient = MediaDiveMongoIngredient(
            id=42,
            name="D-glucose",
            cas_rn="50-99-7",
            chebi=17634,
            pubchem=5793,
            kegg="C00031",
            metacyc="GLUCOSE",
            formula="C6H12O6",
            mass=180.156,
            is_complex=False,
        )
        d = ingredient.to_dict()

        assert d["mediadive_id"] == 42
        assert d["mediadive_name"] == "D-glucose"
        assert d["mediadive_cas_rn"] == "50-99-7"
        assert d["mediadive_chebi"] == 17634
        assert d["mediadive_pubchem"] == 5793
        assert d["mediadive_kegg"] == "C00031"
        assert d["mediadive_metacyc"] == "GLUCOSE"
        assert d["mediadive_formula"] == "C6H12O6"
        assert d["mediadive_mass"] == 180.156
        assert d["mediadive_is_complex"] is False

    def test_complex_ingredient_flag(self) -> None:
        """Test marking ingredient as complex."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Yeast extract",
            is_complex=True,
        )

        assert ingredient.is_complex is True

        d = ingredient.to_dict()
        assert d["mediadive_is_complex"] is True

    def test_ingredient_with_synonyms(self) -> None:
        """Test ingredient with multiple synonyms."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Primary name",
            synonyms=["syn1", "syn2", "syn3"],
        )

        assert len(ingredient.synonyms) == 3
        assert "syn1" in ingredient.synonyms
        assert "syn2" in ingredient.synonyms
        assert "syn3" in ingredient.synonyms

    def test_ingredient_with_empty_synonyms(self) -> None:
        """Test that empty synonyms list is default."""
        ingredient = MediaDiveMongoIngredient(id=1, name="Test")

        assert ingredient.synonyms == []

    def test_ingredient_with_numeric_ids(self) -> None:
        """Test ingredient with various numeric identifiers."""
        ingredient = MediaDiveMongoIngredient(
            id=123,
            name="Test",
            chebi=45678,
            pubchem=987654,
        )

        assert ingredient.id == 123
        assert ingredient.chebi == 45678
        assert ingredient.pubchem == 987654

    def test_ingredient_with_string_ids(self) -> None:
        """Test ingredient with string identifiers."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Test",
            cas_rn="123-45-6",
            kegg="C12345",
            metacyc="COMPOUND-123",
        )

        assert ingredient.cas_rn == "123-45-6"
        assert ingredient.kegg == "C12345"
        assert ingredient.metacyc == "COMPOUND-123"

    def test_ingredient_with_chemical_properties(self) -> None:
        """Test ingredient with chemical properties."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Test compound",
            formula="C6H12O6",
            mass=180.156,
        )

        assert ingredient.formula == "C6H12O6"
        assert ingredient.mass == 180.156

    def test_ingredient_mass_can_be_float(self) -> None:
        """Test that mass supports float values."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Test",
            mass=123.456789,
        )

        assert ingredient.mass == 123.456789

    def test_to_dict_excludes_synonyms(self) -> None:
        """Test that to_dict does not include synonyms."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Test",
            synonyms=["syn1", "syn2"],
        )
        d = ingredient.to_dict()

        # Synonyms should not be in the dict output
        assert "synonyms" not in d
        assert "mediadive_synonyms" not in d

    def test_multiple_ingredients_with_same_name(self) -> None:
        """Test that different IDs can have same name."""
        ing1 = MediaDiveMongoIngredient(id=1, name="Common name")
        ing2 = MediaDiveMongoIngredient(id=2, name="Common name")

        assert ing1.id != ing2.id
        assert ing1.name == ing2.name

    def test_ingredient_with_all_none_optional_fields(self) -> None:
        """Test ingredient with explicitly None optional fields."""
        ingredient = MediaDiveMongoIngredient(
            id=1,
            name="Test",
            cas_rn=None,
            chebi=None,
            pubchem=None,
            kegg=None,
            metacyc=None,
            formula=None,
            mass=None,
        )

        d = ingredient.to_dict()
        assert all(
            d[key] is None
            for key in [
                "mediadive_cas_rn",
                "mediadive_chebi",
                "mediadive_pubchem",
                "mediadive_kegg",
                "mediadive_metacyc",
                "mediadive_formula",
                "mediadive_mass",
            ]
        )
