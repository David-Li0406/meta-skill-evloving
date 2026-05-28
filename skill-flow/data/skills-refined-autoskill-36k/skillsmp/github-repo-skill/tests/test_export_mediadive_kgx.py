"""Tests for export_mediadive_kgx.py script."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from cmm_ai_automation.scripts.export_mediadive_kgx import (
    CONTAINS,
    GROWS_IN,
    INGREDIENT_CATEGORY,
    MEDIUM_CATEGORY,
    PROVIDED_BY,
    SOLUTION_CATEGORY,
    STRAIN_CATEGORY,
    export_mediadive,
    main,
)


@pytest.fixture
def mock_mongodb_data() -> dict[str, list[dict[str, Any]]]:
    """Create mock MongoDB collections with sample data."""
    media_details = [
        {
            "_id": 1,
            "medium": {
                "name": "Nutrient Broth",
                "complex_medium": True,
                "min_pH": 6.5,
                "max_pH": 7.5,
                "source": "Difco",
                "link": "http://example.com/nb",
                "reference": "Smith et al., 2020",
            },
        },
        {
            "_id": 2,
            "medium": {
                "name": "Minimal Medium",
                "complex_medium": False,
                "min_pH": 7.0,
                "max_pH": 7.2,
            },
        },
    ]

    strains = [
        {
            "id": 100,
            "species": "Escherichia coli K-12",
            "ccno": "DSM:498",
            "bacdive_id": 12345,
            "media": [
                {"medium_id": 1, "growth": True},
                {"medium_id": 2, "growth": False},  # Should not create edge
            ],
        },
        {
            "id": 101,
            "species": "Bacillus subtilis 168",
            "ccno": "ATCC:6633",
            # No bacdive_id
            "media": [{"medium_id": 1, "growth": True}],
        },
    ]

    ingredient_details = [
        {
            "id": 10,
            "name": "Sodium chloride",
            "ChEBI": "26710",
            "PubChem": "5234",
            "CAS-RN": "7647-14-5",
            "KEGG-Compound": "C00735",
            "BRENDA-Ligand": "1234",
            "MetaCyc": "CPD-8587",
            "ZVG": "987654",
            "formula": "NaCl",
            "mass": "58.44",
            "density": "2.16",
            "synonyms": ["table salt", "halite"],
            "complex_compound": False,
        },
        {
            "id": 11,
            "name": "Yeast extract",
            # No xrefs
            "complex_compound": True,
        },
    ]

    solution_details = [
        {
            "id": 200,
            "name": "10x PBS",
            "volume": 1000,
            "steps": ["Dissolve NaCl in water", "Adjust pH to 7.4"],
            "equipment": ["Magnetic stirrer", "pH meter"],
            "recipe": [
                {"id": 10, "g_l": 80.0},
                {"id": 11, "mmol_l": 10.0, "optional": True},
            ],
        },
        {
            "id": 201,
            "name": "Empty solution",
            "recipe": [],
        },
    ]

    medium_compositions = [
        {
            "_id": 1,
            "data": [
                {"id": 10, "g_l": 5.0},
                {"id": 11, "mmol_l": 1.0, "optional": True},
            ],
        },
        {
            "_id": 2,
            "data": [{"id": 10, "g_l": 10.0}],
        },
    ]

    return {
        "media_details": media_details,
        "strains": strains,
        "ingredient_details": ingredient_details,
        "solution_details": solution_details,
        "medium_compositions": medium_compositions,
    }


@pytest.fixture
def mock_db(mock_mongodb_data: dict[str, list[dict[str, Any]]]) -> MagicMock:
    """Create a mock MongoDB database."""
    db = MagicMock()

    # Each collection's find() returns an iterator over its data
    db.media_details.find.return_value = iter(mock_mongodb_data["media_details"])
    db.strains.find.return_value = iter(mock_mongodb_data["strains"])
    db.ingredient_details.find.return_value = iter(mock_mongodb_data["ingredient_details"])
    db.solution_details.find.return_value = iter(mock_mongodb_data["solution_details"])
    db.medium_compositions.find.return_value = iter(mock_mongodb_data["medium_compositions"])

    return db


class TestExportMediadive:
    """Tests for export_mediadive function."""

    def test_exports_correct_counts(self, mock_db: MagicMock) -> None:
        """Test that export returns correct entity counts."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                counts = export_mediadive("mongodb://localhost:27017", output_path)

                assert counts["media"] == 2
                assert counts["strains"] == 2
                assert counts["ingredients"] == 2
                assert counts["solutions"] == 2
                # 1 edge from strain 100 to medium 1, 1 from strain 101 to medium 1
                assert counts["grows_in_edges"] == 2
                # 2 from solutions + 3 from medium compositions
                assert counts["contains_edges"] == 5

    def test_creates_output_files(self, mock_db: MagicMock) -> None:
        """Test that TSV files are created."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                export_mediadive("mongodb://localhost:27017", output_path)

                nodes_file = Path(tmpdir) / "mediadive_nodes.tsv"
                edges_file = Path(tmpdir) / "mediadive_edges.tsv"

                assert nodes_file.exists()
                assert edges_file.exists()

    def test_nodes_file_content(self, mock_db: MagicMock) -> None:
        """Test nodes TSV file has expected content."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                export_mediadive("mongodb://localhost:27017", output_path)

                nodes_file = Path(tmpdir) / "mediadive_nodes.tsv"
                content = nodes_file.read_text()

                # Check header
                assert "id\t" in content
                assert "name" in content
                assert "category" in content

                # Check nodes are present
                assert "mediadive.medium:1" in content
                assert "Nutrient Broth" in content
                assert "mediadive.strain:100" in content
                assert "Escherichia coli" in content
                assert "mediadive.ingredient:10" in content
                assert "Sodium chloride" in content
                assert "mediadive.solution:200" in content
                assert "10x PBS" in content

    def test_edges_file_content(self, mock_db: MagicMock) -> None:
        """Test edges TSV file has expected content."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                export_mediadive("mongodb://localhost:27017", output_path)

                edges_file = Path(tmpdir) / "mediadive_edges.tsv"
                content = edges_file.read_text()

                # Check header
                assert "subject" in content
                assert "predicate" in content
                assert "object" in content

                # Check grows_in edges
                assert GROWS_IN in content
                assert "mediadive.strain:100" in content
                assert "mediadive.medium:1" in content

                # Check contains edges
                assert CONTAINS in content
                assert "mediadive.solution:200" in content
                assert "mediadive.ingredient:10" in content

    def test_ingredient_xrefs(self, mock_db: MagicMock) -> None:
        """Test that ingredient xrefs are properly exported."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                export_mediadive("mongodb://localhost:27017", output_path)

                nodes_file = Path(tmpdir) / "mediadive_nodes.tsv"
                content = nodes_file.read_text()

                # Check xrefs are present
                assert "CHEBI:26710" in content
                assert "PUBCHEM.COMPOUND:5234" in content
                assert "CAS:7647-14-5" in content
                assert "KEGG.COMPOUND:C00735" in content
                assert "BRENDA:1234" in content
                assert "MetaCyc:CPD-8587" in content
                assert "ZVG:987654" in content

    def test_strain_bacdive_xref(self, mock_db: MagicMock) -> None:
        """Test that BacDive IDs are exported as xrefs on strains."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                export_mediadive("mongodb://localhost:27017", output_path)

                nodes_file = Path(tmpdir) / "mediadive_nodes.tsv"
                content = nodes_file.read_text()

                # Check bacdive xref
                assert "bacdive.strain:12345" in content

    def test_concentration_on_edges(self, mock_db: MagicMock) -> None:
        """Test that concentration values are on contains edges."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            with TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "mediadive"
                export_mediadive("mongodb://localhost:27017", output_path)

                edges_file = Path(tmpdir) / "mediadive_edges.tsv"
                content = edges_file.read_text()

                # Check concentration
                assert "g/L" in content


class TestConstants:
    """Test module constants."""

    def test_categories_are_curies(self) -> None:
        """Test category constants are valid CURIEs or biolink prefixes."""
        assert ":" in MEDIUM_CATEGORY or MEDIUM_CATEGORY.startswith("biolink:")
        assert ":" in STRAIN_CATEGORY or STRAIN_CATEGORY.startswith("biolink:")
        assert ":" in INGREDIENT_CATEGORY or INGREDIENT_CATEGORY.startswith("biolink:")
        assert ":" in SOLUTION_CATEGORY or SOLUTION_CATEGORY.startswith("biolink:")

    def test_predicates_are_curies(self) -> None:
        """Test predicate constants are valid CURIEs."""
        assert ":" in GROWS_IN
        assert ":" in CONTAINS

    def test_provided_by(self) -> None:
        """Test provenance constant."""
        assert PROVIDED_BY == "mediadive"


class TestCLI:
    """Tests for CLI interface."""

    def test_cli_help(self) -> None:
        """Test CLI --help works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Export MediaDive data to KGX format" in result.output

    def test_cli_with_options(self, mock_db: MagicMock) -> None:
        """Test CLI with options."""
        with patch("cmm_ai_automation.scripts.export_mediadive_kgx.MongoClient") as mock_client:
            mock_client.return_value.__getitem__.return_value = mock_db

            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    [
                        "--output",
                        "test_output",
                        "--mongodb-uri",
                        "mongodb://test:27017",
                    ],
                )

                # CLI should complete successfully
                assert result.exit_code == 0
                assert "Summary:" in result.output
                assert "Media:" in result.output
                assert "Strains:" in result.output
