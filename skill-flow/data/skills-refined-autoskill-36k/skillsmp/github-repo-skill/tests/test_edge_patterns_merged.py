"""Tests for edge_patterns_merged.py script."""

from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from cmm_ai_automation.scripts.edge_patterns_merged import (
    analyze_edges,
    extract_prefix,
    load_node_categories,
    main,
)


class TestExtractPrefix:
    """Tests for extract_prefix function."""

    def test_valid_curie(self) -> None:
        """Test extracting prefix from valid CURIEs."""
        assert extract_prefix("NCBITaxon:9606") == "NCBITaxon"
        assert extract_prefix("CHEBI:15377") == "CHEBI"
        assert extract_prefix("biolink:Gene") == "biolink"

    def test_curie_with_dots(self) -> None:
        """Test CURIEs with dots in prefix."""
        assert extract_prefix("mediadive.medium:123") == "mediadive.medium"
        assert extract_prefix("mediadive.strain:456") == "mediadive.strain"

    def test_empty_curie(self) -> None:
        """Test empty CURIE returns (empty)."""
        assert extract_prefix("") == "(empty)"
        assert extract_prefix(None) == "(empty)"

    def test_invalid_curie(self) -> None:
        """Test invalid CURIE returns (invalid)."""
        assert extract_prefix("no_colon") == "(invalid)"

    def test_whitespace(self) -> None:
        """Test CURIE with whitespace."""
        assert extract_prefix("  NCBITaxon:123  ") == "NCBITaxon"


class TestLoadNodeCategories:
    """Tests for load_node_categories function."""

    def test_load_single_file(self) -> None:
        """Test loading categories from a single file."""
        with TemporaryDirectory() as tmpdir:
            nodes_file = Path(tmpdir) / "test_nodes.tsv"
            nodes_file.write_text("id\tcategory\tname\nA:1\tTypeA\tNode A\nB:2\tTypeB\tNode B\n")

            categories = load_node_categories([nodes_file])

            assert categories["A:1"] == "TypeA"
            assert categories["B:2"] == "TypeB"

    def test_load_multiple_files(self) -> None:
        """Test loading categories from multiple files."""
        with TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "source1_nodes.tsv"
            file2 = Path(tmpdir) / "source2_nodes.tsv"

            file1.write_text("id\tcategory\nA:1\tTypeA\n")
            file2.write_text("id\tcategory\nB:1\tTypeB\n")

            categories = load_node_categories([file1, file2])

            assert categories["A:1"] == "TypeA"
            assert categories["B:1"] == "TypeB"

    def test_empty_category(self) -> None:
        """Test nodes with empty category."""
        with TemporaryDirectory() as tmpdir:
            nodes_file = Path(tmpdir) / "nodes.tsv"
            nodes_file.write_text("id\tcategory\nA:1\t\n")

            categories = load_node_categories([nodes_file])

            assert categories["A:1"] == "(empty)"


class TestAnalyzeEdges:
    """Tests for analyze_edges function."""

    def test_basic_analysis(self) -> None:
        """Test basic edge analysis."""
        with TemporaryDirectory() as tmpdir:
            edges_file = Path(tmpdir) / "test_edges.tsv"
            edges_file.write_text("subject\tpredicate\tobject\nA:1\trelated_to\tB:1\nA:2\trelated_to\tB:2\n")

            node_categories: dict[str, str] = {"A:1": "TypeA", "A:2": "TypeA", "B:1": "TypeB", "B:2": "TypeB"}

            patterns = analyze_edges(edges_file, node_categories, "test")

            assert len(patterns) == 1  # Same pattern twice
            pattern = next(iter(patterns.keys()))
            assert pattern[0] == "test"  # source
            assert pattern[1] == "TypeA"  # subject category
            assert pattern[2] == "A"  # subject prefix
            assert pattern[3] == "related_to"  # predicate
            assert pattern[4] == "TypeB"  # object category
            assert pattern[5] == "B"  # object prefix
            assert patterns[pattern] == 2  # count

    def test_unknown_nodes(self) -> None:
        """Test handling of unknown nodes."""
        with TemporaryDirectory() as tmpdir:
            edges_file = Path(tmpdir) / "edges.tsv"
            edges_file.write_text("subject\tpredicate\tobject\nX:1\trelates\tY:1\n")

            node_categories: dict[str, str] = {}  # Empty - no known nodes

            patterns = analyze_edges(edges_file, node_categories, "test")

            pattern = next(iter(patterns.keys()))
            assert pattern[1] == "(unknown)"  # subject category
            assert pattern[4] == "(unknown)"  # object category


class TestMain:
    """Tests for main function."""

    def test_main_no_args(self) -> None:
        """Test main with no arguments exits with error."""
        with patch("sys.argv", ["edge_patterns_merged.py"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_invalid_directory(self) -> None:
        """Test main with invalid directory exits with error."""
        with patch("sys.argv", ["edge_patterns_merged.py", "/nonexistent/path"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_no_nodes_files(self) -> None:
        """Test main with no *_nodes.tsv files exits with error."""
        with TemporaryDirectory() as tmpdir:
            # Create only edges file
            edges_file = Path(tmpdir) / "test_edges.tsv"
            edges_file.write_text("subject\tpredicate\tobject\n")

            with patch("sys.argv", ["edge_patterns_merged.py", tmpdir]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1

    def test_main_no_edges_files(self) -> None:
        """Test main with no *_edges.tsv files exits with error."""
        with TemporaryDirectory() as tmpdir:
            # Create only nodes file
            nodes_file = Path(tmpdir) / "test_nodes.tsv"
            nodes_file.write_text("id\tcategory\n")

            with patch("sys.argv", ["edge_patterns_merged.py", tmpdir]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1

    def test_main_success(self) -> None:
        """Test successful execution."""
        with TemporaryDirectory() as tmpdir:
            # Create nodes and edges files
            nodes_file = Path(tmpdir) / "test_nodes.tsv"
            nodes_file.write_text("id\tcategory\nA:1\tTypeA\nB:1\tTypeB\n")

            edges_file = Path(tmpdir) / "test_edges.tsv"
            edges_file.write_text("subject\tpredicate\tobject\nA:1\trelated_to\tB:1\n")

            stdout_capture = StringIO()

            with (
                patch("sys.argv", ["edge_patterns_merged.py", tmpdir]),
                patch("sys.stdout", stdout_capture),
            ):
                main()

            output = stdout_capture.getvalue()

            # Check header
            assert "source\tsubject_category" in output

            # Check data
            assert "test" in output
            assert "TypeA" in output
            assert "TypeB" in output

    def test_main_source_name_extraction(self) -> None:
        """Test that source name is correctly extracted from filename."""
        with TemporaryDirectory() as tmpdir:
            # Create files with specific naming
            nodes_file = Path(tmpdir) / "mediadive_nodes.tsv"
            nodes_file.write_text("id\tcategory\nX:1\tType\n")

            edges_file = Path(tmpdir) / "mediadive_edges.tsv"
            edges_file.write_text("subject\tpredicate\tobject\nX:1\trel\tX:1\n")

            stdout_capture = StringIO()

            with (
                patch("sys.argv", ["edge_patterns_merged.py", tmpdir]),
                patch("sys.stdout", stdout_capture),
            ):
                main()

            output = stdout_capture.getvalue()
            # Source should be "mediadive" (with _edges removed)
            assert "mediadive\t" in output

    def test_main_multiple_files(self) -> None:
        """Test with multiple node and edge files."""
        with TemporaryDirectory() as tmpdir:
            # Create multiple pairs of files
            for prefix in ["source1", "source2"]:
                nodes = Path(tmpdir) / f"{prefix}_nodes.tsv"
                edges = Path(tmpdir) / f"{prefix}_edges.tsv"

                nodes.write_text(f"id\tcategory\n{prefix}:1\tType{prefix}\n")
                edges.write_text(f"subject\tpredicate\tobject\n{prefix}:1\trel\t{prefix}:1\n")

            stdout_capture = StringIO()

            with (
                patch("sys.argv", ["edge_patterns_merged.py", tmpdir]),
                patch("sys.stdout", stdout_capture),
            ):
                main()

            output = stdout_capture.getvalue()
            assert "source1" in output
            assert "source2" in output
