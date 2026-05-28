"""Tests for Neo4j load and clear scripts."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest

from cmm_ai_automation.scripts.neo4j_clear import main as neo4j_clear_main
from cmm_ai_automation.scripts.neo4j_load import (
    CATEGORY_TO_LABEL,
    PREDICATE_TO_TYPE,
    category_to_label,
    predicate_to_type,
)
from cmm_ai_automation.scripts.neo4j_load import (
    main as neo4j_load_main,
)


class TestCategoryToLabel:
    """Tests for category_to_label function."""

    def test_known_categories(self) -> None:
        """Test mapping of known categories."""
        assert category_to_label("METPO:1004005") == "GrowthMedium"
        assert category_to_label("biolink:OrganismTaxon") == "Strain"
        assert category_to_label("biolink:ChemicalEntity") == "Ingredient"
        assert category_to_label("biolink:ChemicalMixture") == "Solution"

    def test_unknown_curie_category(self) -> None:
        """Test unknown CURIE category uses local part."""
        assert category_to_label("biolink:NewCategory") == "NewCategory"
        assert category_to_label("CUSTOM:MyType") == "MyType"

    def test_non_curie_category(self) -> None:
        """Test non-CURIE category is returned as-is."""
        assert category_to_label("SomeLabel") == "SomeLabel"

    def test_empty_category(self) -> None:
        """Test empty category returns Unknown."""
        assert category_to_label("") == "Unknown"
        assert category_to_label("   ") == "Unknown"

    def test_none_category(self) -> None:
        """Test None category returns Unknown."""
        assert category_to_label(None) == "Unknown"


class TestPredicateToType:
    """Tests for predicate_to_type function."""

    def test_known_predicates(self) -> None:
        """Test mapping of known predicates."""
        assert predicate_to_type("RO:0001019") == "CONTAINS"
        assert predicate_to_type("METPO:2000517") == "GROWS_IN"

    def test_unknown_predicate(self) -> None:
        """Test unknown predicate uses local part uppercased."""
        assert predicate_to_type("biolink:related_to") == "RELATED_TO"
        assert predicate_to_type("RO:new_relation") == "NEW_RELATION"


class TestNeo4jLoadMain:
    """Tests for neo4j_load main function."""

    @pytest.fixture
    def mock_neo4j_driver(self) -> tuple[MagicMock, MagicMock]:
        """Create a mock Neo4j driver."""
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_driver.session.return_value.__exit__ = MagicMock(return_value=None)

        # Mock result for edge creation
        mock_result = MagicMock()
        mock_result.single.return_value = {"created": 1}
        mock_session.run.return_value = mock_result

        return mock_driver, mock_session

    def test_load_nodes_and_edges(self, mock_neo4j_driver: tuple[MagicMock, MagicMock]) -> None:
        """Test loading nodes and edges from TSV files."""
        mock_driver, mock_session = mock_neo4j_driver

        with TemporaryDirectory() as tmpdir:
            # Create mock TSV files
            nodes_file = Path(tmpdir) / "mediadive_nodes.tsv"
            edges_file = Path(tmpdir) / "mediadive_edges.tsv"

            nodes_file.write_text(
                "id\tname\tcategory\n"
                "mediadive.medium:1\tNutrient Broth\tMETPO:1004005\n"
                "mediadive.strain:100\tE. coli\tbiolink:OrganismTaxon\n"
            )

            edges_file.write_text(
                "subject\tobject\tpredicate\nmediadive.strain:100\tmediadive.medium:1\tMETPO:2000517\n"
            )

            with (
                patch("cmm_ai_automation.scripts.neo4j_load.GraphDatabase.driver") as mock_gd,
                patch("cmm_ai_automation.scripts.neo4j_load.NODES_FILE", nodes_file),
                patch("cmm_ai_automation.scripts.neo4j_load.EDGES_FILE", edges_file),
                patch.dict(
                    "os.environ",
                    {
                        "NEO4J_URI": "bolt://test:7687",
                        "NEO4J_USER": "testuser",
                        "NEO4J_PASSWORD": "testpass",
                    },
                ),
            ):
                mock_gd.return_value = mock_driver

                neo4j_load_main()

                # Verify driver was created with correct credentials
                mock_gd.assert_called_once_with("bolt://test:7687", auth=("testuser", "testpass"))

                # Verify nodes were created
                assert mock_session.run.call_count >= 4  # 2 index ops + 2 nodes + 1 edge


class TestNeo4jClearMain:
    """Tests for neo4j_clear main function."""

    def test_clear_database(self) -> None:
        """Test clearing the database."""
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.nodes_deleted = 100
        mock_summary.counters.relationships_deleted = 50
        mock_result.consume.return_value = mock_summary

        mock_session.run.return_value = mock_result
        mock_driver.session.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_driver.session.return_value.__exit__ = MagicMock(return_value=None)

        with (
            patch("cmm_ai_automation.scripts.neo4j_clear.GraphDatabase.driver") as mock_gd,
            patch.dict(
                "os.environ",
                {
                    "NEO4J_URI": "bolt://test:7687",
                    "NEO4J_USER": "testuser",
                    "NEO4J_PASSWORD": "testpass",
                },
            ),
        ):
            mock_gd.return_value = mock_driver

            neo4j_clear_main()

            # Verify DETACH DELETE was called
            mock_session.run.assert_called_once_with("MATCH (n) DETACH DELETE n")

            # Verify driver was closed
            mock_driver.close.assert_called_once()


class TestConstants:
    """Test module constants."""

    def test_category_mapping_values(self) -> None:
        """Test category mapping has expected labels."""
        assert all(isinstance(label, str) for label in CATEGORY_TO_LABEL.values())
        assert "GrowthMedium" in CATEGORY_TO_LABEL.values()
        assert "Strain" in CATEGORY_TO_LABEL.values()

    def test_predicate_mapping_values(self) -> None:
        """Test predicate mapping has expected relationship types."""
        assert all(isinstance(rel_type, str) for rel_type in PREDICATE_TO_TYPE.values())
        assert "CONTAINS" in PREDICATE_TO_TYPE.values()
        assert "GROWS_IN" in PREDICATE_TO_TYPE.values()
