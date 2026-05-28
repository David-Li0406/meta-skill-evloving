"""Tests for validation schemas."""

from cmm_ai_automation.validation import (
    get_schema_for_sheet,
    list_validated_columns,
    list_validated_sheets,
)
from cmm_ai_automation.validation.schemas import SHEET_SCHEMAS


class TestValidationPackageExports:
    """Test that validation package exports work correctly."""

    def test_get_schema_for_sheet_exported(self) -> None:
        """Test that get_schema_for_sheet is exported."""
        schema = get_schema_for_sheet("strains.tsv")
        assert isinstance(schema, dict)

    def test_list_validated_sheets_exported(self) -> None:
        """Test that list_validated_sheets is exported."""
        sheets = list_validated_sheets()
        assert isinstance(sheets, list)

    def test_list_validated_columns_exported(self) -> None:
        """Test that list_validated_columns is exported."""
        columns = list_validated_columns("strains.tsv")
        assert isinstance(columns, list)


class TestSheetSchemas:
    """Tests for SHEET_SCHEMAS constant."""

    def test_sheet_schemas_exists(self) -> None:
        """Test that SHEET_SCHEMAS is defined."""
        assert SHEET_SCHEMAS is not None
        assert isinstance(SHEET_SCHEMAS, dict)

    def test_strains_schema_exists(self) -> None:
        """Test that strains.tsv schema is defined."""
        assert "strains.tsv" in SHEET_SCHEMAS

    def test_strains_has_species_taxon_validator(self) -> None:
        """Test that strains.tsv has species_taxon_id validator."""
        strains_schema = SHEET_SCHEMAS["strains.tsv"]
        assert "species_taxon_id" in strains_schema
        validator_name, options = strains_schema["species_taxon_id"]
        assert validator_name == "ncbi_taxon"
        assert "check_rank" in options
        assert options["check_rank"] == "species"

    def test_taxa_genomes_schema_exists(self) -> None:
        """Test that taxa_and_genomes.tsv schema is defined."""
        assert "taxa_and_genomes.tsv" in SHEET_SCHEMAS

    def test_growth_preferences_schema_exists(self) -> None:
        """Test that growth_preferences.tsv schema is defined."""
        assert "growth_preferences.tsv" in SHEET_SCHEMAS


class TestGetSchemaForSheet:
    """Tests for get_schema_for_sheet()."""

    def test_get_existing_schema(self) -> None:
        """Test getting schema for existing sheet."""
        schema = get_schema_for_sheet("strains.tsv")
        assert isinstance(schema, dict)
        assert len(schema) > 0

    def test_get_nonexistent_schema(self) -> None:
        """Test getting schema for non-existent sheet."""
        schema = get_schema_for_sheet("nonexistent.tsv")
        assert schema == {}

    def test_schema_format(self) -> None:
        """Test that returned schema has correct format."""
        schema = get_schema_for_sheet("strains.tsv")
        for column, config in schema.items():
            assert isinstance(column, str)
            assert isinstance(config, tuple)
            assert len(config) == 2
            validator_name, options = config
            assert isinstance(validator_name, str)
            assert isinstance(options, dict)


class TestListValidatedSheets:
    """Tests for list_validated_sheets()."""

    def test_returns_list(self) -> None:
        """Test that function returns a list."""
        sheets = list_validated_sheets()
        assert isinstance(sheets, list)

    def test_contains_known_sheets(self) -> None:
        """Test that list contains known sheet names."""
        sheets = list_validated_sheets()
        assert "strains.tsv" in sheets
        assert "taxa_and_genomes.tsv" in sheets
        assert "growth_preferences.tsv" in sheets

    def test_all_items_are_strings(self) -> None:
        """Test that all items in list are strings."""
        sheets = list_validated_sheets()
        assert all(isinstance(s, str) for s in sheets)


class TestListValidatedColumns:
    """Tests for list_validated_columns()."""

    def test_strains_columns(self) -> None:
        """Test getting validated columns for strains.tsv."""
        columns = list_validated_columns("strains.tsv")
        assert isinstance(columns, list)
        assert "species_taxon_id" in columns
        assert "kg_microbe_nodes" in columns

    def test_nonexistent_sheet(self) -> None:
        """Test getting columns for non-existent sheet."""
        columns = list_validated_columns("nonexistent.tsv")
        assert columns == []

    def test_all_items_are_strings(self) -> None:
        """Test that all returned items are strings."""
        columns = list_validated_columns("strains.tsv")
        assert all(isinstance(c, str) for c in columns)

    def test_taxa_genomes_columns(self) -> None:
        """Test getting validated columns for taxa_and_genomes.tsv."""
        columns = list_validated_columns("taxa_and_genomes.tsv")
        assert isinstance(columns, list)
        assert "NCBITaxon id" in columns
