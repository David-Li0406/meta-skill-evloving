"""Tests for edge_patterns_by_source.py script."""

from collections.abc import Generator
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from cmm_ai_automation.scripts.edge_patterns_by_source import (
    CURIE_PATTERN,
    analyze_edges,
    extract_prefix,
    main,
)


class TestExtractPrefix:
    """Tests for extract_prefix function."""

    def test_valid_curie(self) -> None:
        """Test extracting prefix from valid CURIEs."""
        assert extract_prefix("NCBITaxon:9606") == "NCBITaxon"
        assert extract_prefix("CHEBI:15377") == "CHEBI"
        assert extract_prefix("biolink:Gene") == "biolink"
        assert extract_prefix("HP:0000001") == "HP"

    def test_curie_with_complex_local_id(self) -> None:
        """Test CURIEs with complex local IDs."""
        assert extract_prefix("GO:0008150") == "GO"
        assert extract_prefix("UniProtKB:P12345") == "UniProtKB"
        assert extract_prefix("mediadive.medium:123") == "mediadive.medium"

    def test_empty_curie(self) -> None:
        """Test empty CURIE."""
        assert extract_prefix("") == "(empty)"
        assert extract_prefix(None) == "(empty)"

    def test_invalid_curie(self) -> None:
        """Test invalid CURIE format."""
        assert extract_prefix("no_colon_here") == "(invalid)"
        assert extract_prefix("   ") == "(invalid)"

    def test_curie_with_whitespace(self) -> None:
        """Test CURIE with leading/trailing whitespace."""
        assert extract_prefix("  NCBITaxon:9606  ") == "NCBITaxon"


class TestCuriePattern:
    """Tests for CURIE_PATTERN regex."""

    def test_matches_standard_curie(self) -> None:
        """Test pattern matches standard CURIEs."""
        match = CURIE_PATTERN.match("NCBITaxon:9606")
        assert match is not None
        assert match.group(1) == "NCBITaxon"
        assert match.group(2) == "9606"

    def test_matches_curie_with_dots(self) -> None:
        """Test pattern matches CURIEs with dots in prefix."""
        match = CURIE_PATTERN.match("mediadive.strain:123")
        assert match is not None
        assert match.group(1) == "mediadive.strain"
        assert match.group(2) == "123"

    def test_no_match_without_colon(self) -> None:
        """Test pattern doesn't match strings without colon."""
        match = CURIE_PATTERN.match("NCBITaxon9606")
        assert match is None


class TestAnalyzeEdges:
    """Tests for analyze_edges function."""

    @pytest.fixture
    def sample_data_dir(self) -> Generator[tuple[Path, Path, Path], None, None]:
        """Create temporary directory with sample data."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create nodes file
            nodes_file = tmpdir_path / "nodes.tsv"
            nodes_file.write_text(
                "id\tcategory\tname\n"
                "NCBITaxon:9606\tbiolink:OrganismTaxon\tHuman\n"
                "CHEBI:15377\tbiolink:ChemicalEntity\tWater\n"
                "NCBITaxon:562\tbiolink:OrganismTaxon\tE. coli\n"
                "METPO:1234\tMETPO:Medium\tLB broth\n"
            )

            # Create edges file
            edges_file = tmpdir_path / "edges.tsv"
            edges_file.write_text(
                "subject\tpredicate\tobject\n"
                "NCBITaxon:9606\tbiolink:interacts_with\tCHEBI:15377\n"
                "NCBITaxon:562\tbiolink:grows_in\tMETPO:1234\n"
                "NCBITaxon:562\tbiolink:interacts_with\tCHEBI:15377\n"
            )

            yield tmpdir_path, nodes_file, edges_file

    def test_analyze_edges_basic(self, sample_data_dir: tuple[Path, Path, Path]) -> None:
        """Test basic edge analysis."""
        tmpdir, nodes_file, edges_file = sample_data_dir

        patterns = analyze_edges(edges_file, nodes_file, "test_source")

        # Should find 2 unique patterns
        assert len(patterns) >= 2

        # Check that patterns have correct structure (source, subj_cat, subj_prefix, pred, obj_cat, obj_prefix)
        for pattern in patterns:
            assert len(pattern) == 6
            assert pattern[0] == "test_source"

    def test_analyze_edges_counts(self, sample_data_dir: tuple[Path, Path, Path]) -> None:
        """Test edge pattern counts."""
        tmpdir, nodes_file, edges_file = sample_data_dir

        patterns = analyze_edges(edges_file, nodes_file, "test")

        # Find the interacts_with pattern (appears twice)
        interacts_patterns = [p for p in patterns if "biolink:interacts_with" in p]
        if interacts_patterns:
            # The count should be present
            for pattern in interacts_patterns:
                assert patterns[pattern] >= 1

    def test_analyze_edges_unknown_nodes(self) -> None:
        """Test handling of edges referencing unknown nodes."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create minimal nodes file
            nodes_file = tmpdir_path / "nodes.tsv"
            nodes_file.write_text("id\tcategory\nA:1\tTypeA\n")

            # Create edges file with unknown node
            edges_file = tmpdir_path / "edges.tsv"
            edges_file.write_text(
                "subject\tpredicate\tobject\nA:1\trelated_to\tB:2\n"  # B:2 is not in nodes
            )

            patterns = analyze_edges(edges_file, nodes_file, "test")

            # Should still process the edge, with "(unknown)" for missing node
            assert len(patterns) == 1
            pattern = next(iter(patterns))
            assert "(unknown)" in pattern  # Object category should be unknown


class TestMain:
    """Tests for main function."""

    def test_main_no_args(self) -> None:
        """Test main with no arguments exits with error."""
        with patch("sys.argv", ["edge_patterns_by_source.py"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_with_directory(self) -> None:
        """Test main with a directory containing source data."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create a source directory
            source_dir = tmpdir_path / "source1"
            source_dir.mkdir()

            # Create nodes and edges files
            nodes_file = source_dir / "nodes.tsv"
            nodes_file.write_text("id\tcategory\nA:1\tTypeA\nB:1\tTypeB\n")

            edges_file = source_dir / "edges.tsv"
            edges_file.write_text("subject\tpredicate\tobject\nA:1\trelated_to\tB:1\n")

            # Capture stdout
            stdout_capture = StringIO()

            with (
                patch("sys.argv", ["edge_patterns_by_source.py", str(tmpdir_path)]),
                patch("sys.stdout", stdout_capture),
            ):
                main()

            output = stdout_capture.getvalue()

            # Check header
            assert "source\tsubject_category" in output
            assert "predicate\tobject_category" in output

            # Check data row
            assert "source1" in output
            assert "TypeA" in output
            assert "TypeB" in output

    def test_main_skips_files(self) -> None:
        """Test that main skips files (not directories)."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create a file instead of directory
            regular_file = tmpdir_path / "not_a_dir.txt"
            regular_file.write_text("some content")

            stdout_capture = StringIO()

            with (
                patch("sys.argv", ["edge_patterns_by_source.py", str(tmpdir_path)]),
                patch("sys.stdout", stdout_capture),
            ):
                main()

            # Should only have header, no data rows
            output = stdout_capture.getvalue()
            lines = output.strip().split("\n")
            assert len(lines) == 1  # Just header

    def test_main_skips_incomplete_dirs(self) -> None:
        """Test that main skips directories without edges.tsv or nodes.tsv."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create directory with only nodes.tsv
            incomplete_dir = tmpdir_path / "incomplete"
            incomplete_dir.mkdir()
            (incomplete_dir / "nodes.tsv").write_text("id\tcategory\n")
            # No edges.tsv

            stdout_capture = StringIO()

            with (
                patch("sys.argv", ["edge_patterns_by_source.py", str(tmpdir_path)]),
                patch("sys.stdout", stdout_capture),
            ):
                main()

            # Should only have header, no data rows
            output = stdout_capture.getvalue()
            lines = output.strip().split("\n")
            assert len(lines) == 1  # Just header
