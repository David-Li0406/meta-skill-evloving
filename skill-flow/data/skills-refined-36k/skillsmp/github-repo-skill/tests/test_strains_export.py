"""Tests for strains KGX export functions."""

import csv
from pathlib import Path

from cmm_ai_automation.strains.export import (
    SUBCLASS_OF_PREDICATE,
    TAXON_ASSOCIATION_CATEGORY,
    TAXONOMIC_RANK_CATEGORY,
    export_kgx_edges,
    export_kgx_nodes,
    export_taxrank_nodes,
)
from cmm_ai_automation.strains.models import StrainRecord


class TestExportKGXNodes:
    """Tests for export_kgx_nodes()."""

    def test_export_empty_records(self, tmp_path: Path) -> None:
        """Test exporting empty list of records."""
        output = tmp_path / "nodes.tsv"
        export_kgx_nodes([], output)

        assert output.exists()
        # Should have header but no data rows
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        assert len(rows) == 0

    def test_export_single_record(self, tmp_path: Path) -> None:
        """Test exporting single strain record."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            name="Test strain",
            ncbi_taxon_id="NCBITaxon:408",
            species_taxon_id="408",
            strain_designation="AM1",
            has_taxonomic_rank="strain",
        )
        output = tmp_path / "nodes.tsv"
        export_kgx_nodes([record], output)

        assert output.exists()
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["id"] == "NCBITaxon:408"
        assert rows[0]["name"] == "Test strain"
        assert rows[0]["strain_designation"] == "AM1"

    def test_export_multiple_records(self, tmp_path: Path) -> None:
        """Test exporting multiple records."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                name="Strain 1",
                primary_collection_id="DSM:1",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                name="Strain 2",
                primary_collection_id="DSM:2",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=3,
                name="Strain 3",
                primary_collection_id="DSM:3",
            ),
        ]
        output = tmp_path / "nodes.tsv"
        export_kgx_nodes(records, output)

        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        assert len(rows) == 3
        assert rows[0]["name"] == "Strain 1"
        assert rows[1]["name"] == "Strain 2"
        assert rows[2]["name"] == "Strain 3"

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        """Test that parent directories are created."""
        output = tmp_path / "subdir" / "nodes.tsv"
        record = StrainRecord(source_sheet="test.tsv", source_row=1, primary_collection_id="DSM:1")
        export_kgx_nodes([record], output)

        assert output.exists()
        assert output.parent.exists()


class TestExportKGXEdges:
    """Tests for export_kgx_edges()."""

    def test_export_empty_records(self, tmp_path: Path) -> None:
        """Test exporting empty list returns 0."""
        output = tmp_path / "edges.tsv"
        count = export_kgx_edges([], output)

        assert count == 0
        assert output.exists()

    def test_export_record_with_species_taxon(self, tmp_path: Path) -> None:
        """Test exporting record with species taxon creates edge."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:1000",
            species_taxon_id="500",  # Different from ncbi_taxon_id
        )
        output = tmp_path / "edges.tsv"
        count = export_kgx_edges([record], output)

        assert count == 1
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["subject"] == "NCBITaxon:1000"
        assert rows[0]["predicate"] == SUBCLASS_OF_PREDICATE
        assert rows[0]["object"] == "NCBITaxon:500"
        assert rows[0]["category"] == TAXON_ASSOCIATION_CATEGORY

    def test_no_edge_for_self_loop(self, tmp_path: Path) -> None:
        """Test that no edge is created when species taxon equals strain taxon."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:500",
            species_taxon_id="500",  # Same as ncbi_taxon_id
        )
        output = tmp_path / "edges.tsv"
        count = export_kgx_edges([record], output)

        assert count == 0
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        assert len(rows) == 0

    def test_no_edge_without_species_taxon(self, tmp_path: Path) -> None:
        """Test that no edge is created without species_taxon_id."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:1000",
            species_taxon_id=None,
        )
        output = tmp_path / "edges.tsv"
        count = export_kgx_edges([record], output)

        assert count == 0

    def test_edge_id_format(self, tmp_path: Path) -> None:
        """Test that edge ID has correct format."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:1000",
            species_taxon_id="500",
        )
        output = tmp_path / "edges.tsv"
        export_kgx_edges([record], output)

        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        edge_id = rows[0]["id"]
        assert "NCBITaxon:1000" in edge_id
        assert SUBCLASS_OF_PREDICATE in edge_id
        assert "NCBITaxon:500" in edge_id

    def test_multiple_records_some_with_edges(self, tmp_path: Path) -> None:
        """Test exporting mix of records with and without edges."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                ncbi_taxon_id="NCBITaxon:1000",
                species_taxon_id="500",  # Creates edge
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                ncbi_taxon_id="NCBITaxon:2000",
                species_taxon_id=None,  # No edge
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=3,
                ncbi_taxon_id="NCBITaxon:3000",
                species_taxon_id="600",  # Creates edge
            ),
        ]
        output = tmp_path / "edges.tsv"
        count = export_kgx_edges(records, output)

        assert count == 2
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        assert len(rows) == 2


class TestExportTaxrankNodes:
    """Tests for export_taxrank_nodes()."""

    def test_export_empty_records(self, tmp_path: Path) -> None:
        """Test exporting empty list returns 0."""
        output = tmp_path / "taxranks.tsv"
        count = export_taxrank_nodes([], output)

        assert count == 0
        assert output.exists()

    def test_export_single_rank(self, tmp_path: Path) -> None:
        """Test exporting records with single rank type."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                has_taxonomic_rank="strain",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                has_taxonomic_rank="strain",
            ),
        ]
        output = tmp_path / "taxranks.tsv"
        count = export_taxrank_nodes(records, output)

        assert count == 1  # Only one unique rank
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["id"] == "TAXRANK:0000060"  # strain rank
        assert rows[0]["category"] == TAXONOMIC_RANK_CATEGORY
        assert rows[0]["name"] == "strain"

    def test_export_multiple_ranks(self, tmp_path: Path) -> None:
        """Test exporting records with different ranks."""
        records = [
            StrainRecord(source_sheet="test.tsv", source_row=1, has_taxonomic_rank="strain"),
            StrainRecord(source_sheet="test.tsv", source_row=2, has_taxonomic_rank="species"),
            StrainRecord(source_sheet="test.tsv", source_row=3, has_taxonomic_rank="genus"),
            StrainRecord(source_sheet="test.tsv", source_row=4, has_taxonomic_rank="species"),  # Duplicate
        ]
        output = tmp_path / "taxranks.tsv"
        count = export_taxrank_nodes(records, output)

        assert count == 3  # Three unique ranks
        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        assert len(rows) == 3
        rank_ids = [r["id"] for r in rows]
        assert "TAXRANK:0000060" in rank_ids  # strain
        assert "TAXRANK:0000006" in rank_ids  # species
        assert "TAXRANK:0000005" in rank_ids  # genus

    def test_skip_records_without_rank(self, tmp_path: Path) -> None:
        """Test that records without rank are skipped."""
        records = [
            StrainRecord(source_sheet="test.tsv", source_row=1, has_taxonomic_rank="strain"),
            StrainRecord(source_sheet="test.tsv", source_row=2, has_taxonomic_rank=None),
            StrainRecord(source_sheet="test.tsv", source_row=3, has_taxonomic_rank=""),
        ]
        output = tmp_path / "taxranks.tsv"
        count = export_taxrank_nodes(records, output)

        assert count == 1  # Only one with valid rank

    def test_output_is_sorted(self, tmp_path: Path) -> None:
        """Test that rank nodes are sorted by CURIE."""
        records = [
            StrainRecord(source_sheet="test.tsv", source_row=1, has_taxonomic_rank="strain"),  # TAXRANK:0000060
            StrainRecord(source_sheet="test.tsv", source_row=2, has_taxonomic_rank="genus"),  # TAXRANK:0000005
            StrainRecord(source_sheet="test.tsv", source_row=3, has_taxonomic_rank="species"),  # TAXRANK:0000006
        ]
        output = tmp_path / "taxranks.tsv"
        export_taxrank_nodes(records, output)

        with output.open() as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        # Should be sorted by CURIE
        ids = [r["id"] for r in rows]
        assert ids == sorted(ids)
