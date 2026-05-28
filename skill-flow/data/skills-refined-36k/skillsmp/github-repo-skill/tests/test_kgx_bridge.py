"""Tests for KGX bridge module - converting reconciliation results to same_as edges."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from cmm_ai_automation.reconcile.agent import MatchConfidence, ReconciliationResult
from cmm_ai_automation.reconcile.kgx_bridge import (
    ASSOCIATION_CATEGORY,
    PREFIX_PRIORITY,
    SAME_AS_PREDICATE,
    export_same_as_edges,
    filter_high_confidence_matches,
    generate_kgx_merge_config,
    reconciliation_to_same_as_edge,
)


class TestReconciliationToSameAsEdge:
    """Tests for reconciliation_to_same_as_edge function."""

    def test_basic_edge_creation(self) -> None:
        """Test creating a same_as edge from reconciliation result."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.HIGH,
            reasoning="Genus Sinorhizobium is a synonym of Ensifer.",
            matched_fields=["genus_synonym", "strain_designation"],
            conflicts=[],
        )
        edge = reconciliation_to_same_as_edge(
            subject_id="NCBITaxon:1286640",
            object_id="bacdive:13541",
            result=result,
        )

        assert edge["subject"] == "NCBITaxon:1286640"
        assert edge["object"] == "bacdive:13541"
        assert edge["predicate"] == SAME_AS_PREDICATE
        assert edge["category"] == ASSOCIATION_CATEGORY
        assert edge["reconciliation_confidence"] == "high"
        assert "Sinorhizobium" in edge["reconciliation_reasoning"]
        assert edge["matched_fields"] == "genus_synonym|strain_designation"

    def test_edge_id_format(self) -> None:
        """Test that edge ID follows expected format."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.MEDIUM,
            reasoning="Match by culture collection ID.",
            matched_fields=["culture_collection_id"],
        )
        edge = reconciliation_to_same_as_edge("cmm:123", "bacdive:456", result)

        assert edge["id"] == f"cmm:123--{SAME_AS_PREDICATE}--bacdive:456"

    def test_long_reasoning_truncation(self) -> None:
        """Test that very long reasoning is truncated."""
        long_reasoning = "x" * 1000  # Longer than 500 char limit
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.HIGH,
            reasoning=long_reasoning,
            matched_fields=[],
        )
        edge = reconciliation_to_same_as_edge("a:1", "b:2", result)

        assert len(edge["reconciliation_reasoning"]) == 500

    def test_empty_matched_fields(self) -> None:
        """Test edge with no matched fields."""
        result = ReconciliationResult(
            is_match=True,
            confidence=MatchConfidence.LOW,
            reasoning="Weak match based on name similarity.",
            matched_fields=[],
        )
        edge = reconciliation_to_same_as_edge("x:1", "y:2", result)

        assert edge["matched_fields"] == ""


class TestFilterHighConfidenceMatches:
    """Tests for filter_high_confidence_matches function."""

    @pytest.fixture
    def sample_results(self) -> list[tuple[str, str, ReconciliationResult]]:
        """Create sample reconciliation results at various confidence levels."""
        return [
            (
                "a:1",
                "b:1",
                ReconciliationResult(
                    is_match=True,
                    confidence=MatchConfidence.HIGH,
                    reasoning="High confidence match",
                    matched_fields=["id"],
                ),
            ),
            (
                "a:2",
                "b:2",
                ReconciliationResult(
                    is_match=True,
                    confidence=MatchConfidence.MEDIUM,
                    reasoning="Medium confidence match",
                    matched_fields=["name"],
                ),
            ),
            (
                "a:3",
                "b:3",
                ReconciliationResult(
                    is_match=True,
                    confidence=MatchConfidence.LOW,
                    reasoning="Low confidence match",
                    matched_fields=["partial_name"],
                ),
            ),
            (
                "a:4",
                "b:4",
                ReconciliationResult(
                    is_match=False,
                    confidence=MatchConfidence.NONE,
                    reasoning="Not a match",
                    matched_fields=[],
                ),
            ),
            (
                "a:5",
                "b:5",
                ReconciliationResult(
                    is_match=True,
                    confidence=MatchConfidence.NONE,
                    reasoning="Match with no confidence",
                    matched_fields=[],
                ),
            ),
        ]

    def test_filter_high_only(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test filtering for HIGH confidence only."""
        filtered = filter_high_confidence_matches(sample_results, MatchConfidence.HIGH)
        assert len(filtered) == 1
        assert filtered[0][0] == "a:1"

    def test_filter_medium_and_above(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test filtering for MEDIUM and above."""
        filtered = filter_high_confidence_matches(sample_results, MatchConfidence.MEDIUM)
        assert len(filtered) == 2
        ids = [r[0] for r in filtered]
        assert "a:1" in ids
        assert "a:2" in ids

    def test_filter_low_and_above(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test filtering for LOW and above."""
        filtered = filter_high_confidence_matches(sample_results, MatchConfidence.LOW)
        assert len(filtered) == 3

    def test_non_matches_excluded(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test that is_match=False results are always excluded."""
        # Even with NONE confidence filter, non-matches should be excluded
        filtered = filter_high_confidence_matches(sample_results, MatchConfidence.NONE)
        # Should include all matches (4 total) but exclude non-matches
        assert len(filtered) == 4
        assert all(r[2].is_match for r in filtered)


class TestExportSameAsEdges:
    """Tests for export_same_as_edges function."""

    @pytest.fixture
    def sample_results(self) -> list[tuple[str, str, ReconciliationResult]]:
        """Sample results for export testing."""
        return [
            (
                "NCBITaxon:123",
                "bacdive:456",
                ReconciliationResult(
                    is_match=True,
                    confidence=MatchConfidence.HIGH,
                    reasoning="Exact match on culture collection ID",
                    matched_fields=["culture_collection_id", "species"],
                ),
            ),
            (
                "cmm:789",
                "bacdive:101",
                ReconciliationResult(
                    is_match=True,
                    confidence=MatchConfidence.MEDIUM,
                    reasoning="Name similarity match",
                    matched_fields=["scientific_name"],
                ),
            ),
            (
                "cmm:999",
                "bacdive:888",
                ReconciliationResult(
                    is_match=False,
                    confidence=MatchConfidence.NONE,
                    reasoning="Different organisms",
                    matched_fields=[],
                ),
            ),
        ]

    def test_export_creates_file(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test that export creates a TSV file."""
        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "same_as_edges.tsv"
            count = export_same_as_edges(sample_results, output_path)

            assert output_path.exists()
            assert count == 2  # Only matches exported

    def test_export_tsv_format(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test TSV file format and content."""
        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "same_as_edges.tsv"
            export_same_as_edges(sample_results, output_path)

            content = output_path.read_text()
            lines = content.strip().split("\n")

            # Check header
            header = lines[0].split("\t")
            assert "id" in header
            assert "subject" in header
            assert "predicate" in header
            assert "object" in header
            assert "reconciliation_confidence" in header

            # Check data rows
            assert len(lines) == 3  # header + 2 data rows

    def test_export_with_confidence_filter(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test export with minimum confidence filter."""
        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "high_only.tsv"
            count = export_same_as_edges(sample_results, output_path, min_confidence=MatchConfidence.HIGH)

            assert count == 1  # Only high confidence match

    def test_export_creates_parent_dirs(self, sample_results: list[tuple[str, str, ReconciliationResult]]) -> None:
        """Test that export creates parent directories if needed."""
        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "dir" / "same_as.tsv"
            export_same_as_edges(sample_results, output_path)

            assert output_path.exists()
            assert output_path.parent.exists()


class TestGenerateKgxMergeConfig:
    """Tests for generate_kgx_merge_config function."""

    def test_config_structure(self) -> None:
        """Test that config has expected structure."""
        config = generate_kgx_merge_config(
            nodes_files=[Path("nodes.tsv")],
            edges_files=[Path("edges.tsv")],
            same_as_file=Path("same_as.tsv"),
            output_dir=Path("output"),
        )

        assert "configuration" in config
        assert "target" in config
        assert "source" in config
        assert "operations" in config

    def test_config_output_directory(self) -> None:
        """Test output directory is set correctly."""
        config = generate_kgx_merge_config(
            nodes_files=[Path("nodes.tsv")],
            edges_files=[Path("edges.tsv")],
            same_as_file=Path("same_as.tsv"),
            output_dir=Path("/custom/output"),
        )

        assert config["configuration"]["output_directory"] == "/custom/output"

    def test_config_multiple_files(self) -> None:
        """Test config with multiple nodes/edges files."""
        config = generate_kgx_merge_config(
            nodes_files=[Path("nodes1.tsv"), Path("nodes2.tsv")],
            edges_files=[Path("edges1.tsv"), Path("edges2.tsv")],
            same_as_file=Path("same_as.tsv"),
            output_dir=Path("output"),
        )

        # Target should have both node files
        assert len(config["target"]["filename"]) == 2

        # Source should include edges and same_as
        assert len(config["source"]) == 2

    def test_config_clique_merge_operation(self) -> None:
        """Test that clique merge operation is configured."""
        config = generate_kgx_merge_config(
            nodes_files=[Path("nodes.tsv")],
            edges_files=[Path("edges.tsv")],
            same_as_file=Path("same_as.tsv"),
            output_dir=Path("output"),
        )

        operations = config["operations"]
        assert len(operations) == 1
        assert operations[0]["name"] == "clique_merge"
        assert "prefix_prioritization_map" in operations[0]["args"]

    def test_config_prefix_priority(self) -> None:
        """Test prefix prioritization is correctly ordered."""
        config = generate_kgx_merge_config(
            nodes_files=[Path("nodes.tsv")],
            edges_files=[Path("edges.tsv")],
            same_as_file=Path("same_as.tsv"),
            output_dir=Path("output"),
        )

        priority_map = config["operations"][0]["args"]["prefix_prioritization_map"]

        # NCBITaxon should have lowest priority number (highest priority)
        assert priority_map["NCBITaxon"] < priority_map["cmm"]
        assert priority_map["bacdive"] < priority_map["cmm"]


class TestPrefixPriority:
    """Tests for PREFIX_PRIORITY constant."""

    def test_ncbitaxon_highest_priority(self) -> None:
        """Test that NCBITaxon has highest priority (first in list)."""
        assert PREFIX_PRIORITY[0] == "NCBITaxon"

    def test_cmm_lowest_priority(self) -> None:
        """Test that cmm (local IDs) has lowest priority (last in list)."""
        assert PREFIX_PRIORITY[-1] == "cmm"

    def test_common_prefixes_included(self) -> None:
        """Test that common culture collection prefixes are included."""
        common_prefixes = ["bacdive", "dsmz", "atcc", "jcm"]
        for prefix in common_prefixes:
            assert prefix in PREFIX_PRIORITY
