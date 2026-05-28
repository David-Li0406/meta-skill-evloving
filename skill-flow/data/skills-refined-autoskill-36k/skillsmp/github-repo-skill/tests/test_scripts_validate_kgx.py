import logging
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from click.testing import CliRunner

from cmm_ai_automation.scripts.validate_kgx_custom import validate


@pytest.fixture
def mock_config(tmp_path: Path) -> Path:
    config = {"custom_prefixes": {"TEST": "http://example.org/test/"}}
    config_file = tmp_path / "config.yaml"
    with config_file.open("w") as f:
        yaml.dump(config, f)
    return config_file


def test_validate_kgx_success(tmp_path: Path, mock_config: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test validation success path."""
    nodes_file = tmp_path / "nodes.tsv"
    edges_file = tmp_path / "edges.tsv"
    output_file = tmp_path / "report.json"

    # Create dummy files (content doesn't matter as we mock Transformer)
    nodes_file.touch()
    edges_file.touch()

    runner = CliRunner()

    with (
        patch("cmm_ai_automation.scripts.validate_kgx_custom.Validator") as MockValidator,
        patch("cmm_ai_automation.scripts.validate_kgx_custom.Transformer") as MockTransformer,
    ):
        # Setup Mock Validator
        mock_validator_instance = MockValidator.return_value
        mock_validator_instance.prefixes = set()  # Start with empty prefixes
        mock_validator_instance.errors = {}  # No errors

        # Setup Mock Transformer
        mock_transformer_instance = MockTransformer.return_value

        with caplog.at_level(logging.INFO):
            result = runner.invoke(
                validate,
                [
                    "--nodes",
                    str(nodes_file),
                    "--edges",
                    str(edges_file),
                    "--config",
                    str(mock_config),
                    "--output",
                    str(output_file),
                ],
            )

        # Check that custom prefixes were added
        assert "TEST" in mock_validator_instance.prefixes

        # Check that transform was called
        mock_transformer_instance.transform.assert_called_once()

        # Check that report was written
        mock_validator_instance.write_report.assert_called_once()

        assert result.exit_code == 0
        assert "SUCCESS: No validation errors found!" in caplog.text


def test_validate_kgx_failure(tmp_path: Path, mock_config: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test validation failure path."""
    nodes_file = tmp_path / "nodes.tsv"
    edges_file = tmp_path / "edges.tsv"
    output_file = tmp_path / "report.json"

    nodes_file.touch()
    edges_file.touch()

    runner = CliRunner()

    with (
        patch("cmm_ai_automation.scripts.validate_kgx_custom.Validator") as MockValidator,
        patch("cmm_ai_automation.scripts.validate_kgx_custom.Transformer"),
    ):
        # Setup Mock Validator with errors
        mock_validator_instance = MockValidator.return_value
        mock_validator_instance.prefixes = set()
        mock_validator_instance.errors = {"duplicate_node": {"id:123": ["Node 'id:123' is duplicated"]}}

        with caplog.at_level(logging.ERROR):
            result = runner.invoke(
                validate,
                [
                    "--nodes",
                    str(nodes_file),
                    "--edges",
                    str(edges_file),
                    "--config",
                    str(mock_config),
                    "--output",
                    str(output_file),
                ],
            )

        assert result.exit_code == 1
        assert "FAILURE: Found 1 errors." in caplog.text


# ==============================================================================
# Integration Tests - Test with real KGX files and actual validation
# ==============================================================================


@pytest.fixture
def integration_config(tmp_path: Path) -> Path:
    """Config with custom prefixes for DOI and UUID."""
    config = {
        "custom_prefixes": {
            "doi": "https://doi.org/",
            "uuid": "http://example.org/uuid/",
        }
    }
    config_file = tmp_path / "config.yaml"
    with config_file.open("w") as f:
        yaml.dump(config, f)
    return config_file


@pytest.fixture
def kgx_with_doi_nodes(tmp_path: Path) -> Path:
    """KGX nodes file with DOI identifiers (containing slashes)."""
    nodes_file = tmp_path / "nodes.tsv"
    nodes_content = """id\tname\tcategory
doi:10.1007/s00203-018-1567-5\tSample Publication\tbiolink:Publication
CHEBI:12345\tGlucose\tbiolink:ChemicalEntity
"""
    nodes_file.write_text(nodes_content)
    return nodes_file


@pytest.fixture
def kgx_with_uuid_nodes(tmp_path: Path) -> Path:
    """KGX nodes file with UUID identifiers."""
    nodes_file = tmp_path / "nodes.tsv"
    nodes_content = """id\tname\tcategory
uuid:550e8400-e29b-41d4-a716-446655440000\tCustom Entity\tbiolink:NamedThing
CHEBI:12345\tGlucose\tbiolink:ChemicalEntity
"""
    nodes_file.write_text(nodes_content)
    return nodes_file


@pytest.fixture
def minimal_edges(tmp_path: Path) -> Path:
    """Minimal valid KGX edges file."""
    edges_file = tmp_path / "edges.tsv"
    edges_content = """subject\tpredicate\tobject\tknowledge_level\tagent_type
CHEBI:12345\tbiolink:related_to\tCHEBI:12345\tknowledge_assertion\tmanual_agent
"""
    edges_file.write_text(edges_content)
    return edges_file


@pytest.mark.integration
def test_validate_doi_with_slashes_integration(
    kgx_with_doi_nodes: Path,
    minimal_edges: Path,
    integration_config: Path,
    tmp_path: Path,
) -> None:
    """Integration test: Verify DOIs with slashes pass validation."""
    output_file = tmp_path / "report.json"
    runner = CliRunner()

    result = runner.invoke(
        validate,
        [
            "--nodes",
            str(kgx_with_doi_nodes),
            "--edges",
            str(minimal_edges),
            "--config",
            str(integration_config),
            "--output",
            str(output_file),
        ],
    )

    # Validation should succeed (DOIs with slashes should be accepted)
    assert result.exit_code == 0, f"Validation failed: {result.output}"
    assert output_file.exists(), "Validation report should be created"


@pytest.mark.integration
def test_validate_uuid_integration(
    kgx_with_uuid_nodes: Path,
    minimal_edges: Path,
    integration_config: Path,
    tmp_path: Path,
) -> None:
    """Integration test: Verify UUIDs are accepted as valid identifiers."""
    output_file = tmp_path / "report.json"
    runner = CliRunner()

    result = runner.invoke(
        validate,
        [
            "--nodes",
            str(kgx_with_uuid_nodes),
            "--edges",
            str(minimal_edges),
            "--config",
            str(integration_config),
            "--output",
            str(output_file),
        ],
    )

    # Validation should succeed (UUIDs should be accepted)
    assert result.exit_code == 0, f"Validation failed: {result.output}"
    assert output_file.exists(), "Validation report should be created"


@pytest.mark.integration
def test_monkey_patch_allows_slashes_in_curies() -> None:
    """Integration test: Verify monkey-patching of is_curie works."""
    from kgx.prefix_manager import PrefixManager

    from cmm_ai_automation.scripts.validate_kgx_custom import loose_is_curie

    # Apply monkey-patch
    original_is_curie = PrefixManager.is_curie
    PrefixManager.is_curie = loose_is_curie

    try:
        # Test DOI with slashes (should pass with monkey-patch)
        assert PrefixManager.is_curie("doi:10.1007/s00203-018-1567-5")

        # Test UUID (should pass)
        assert PrefixManager.is_curie("uuid:550e8400-e29b-41d4-a716-446655440000")

        # Test standard CURIE (should still pass)
        assert PrefixManager.is_curie("CHEBI:12345")

        # Test invalid CURIE (should fail)
        assert not PrefixManager.is_curie("not a curie")
        assert not PrefixManager.is_curie("has spaces:123")

    finally:
        # Restore original
        PrefixManager.is_curie = original_is_curie
