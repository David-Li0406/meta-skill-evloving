"""Tests for strains inference functions."""

from cmm_ai_automation.strains.inference import (
    infer_species_from_bacdive,
    infer_species_from_self,
    infer_taxonomic_rank,
    run_inference_pipeline,
)
from cmm_ai_automation.strains.models import StrainRecord


class TestInferSpeciesFromBacdive:
    """Tests for infer_species_from_bacdive()."""

    def test_infer_from_bacdive_strain(self) -> None:
        """Test inferring species from BacDive for strain-level record."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            bacdive_id="12345",
            ncbi_taxon_id="NCBITaxon:999",
            species_taxon_id=None,
            has_taxonomic_rank="strain",
        )
        records = [record]

        count = infer_species_from_bacdive(records)

        assert count == 1
        assert record.species_taxon_id == "999"

    def test_skip_if_species_already_set(self) -> None:
        """Test skipping records that already have species_taxon_id."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            bacdive_id="12345",
            ncbi_taxon_id="NCBITaxon:999",
            species_taxon_id="123",  # Already set
            has_taxonomic_rank="strain",
        )
        records = [record]

        count = infer_species_from_bacdive(records)

        assert count == 0
        assert record.species_taxon_id == "123"  # Unchanged

    def test_skip_if_no_bacdive_id(self) -> None:
        """Test skipping records without BacDive ID."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            bacdive_id=None,
            ncbi_taxon_id="NCBITaxon:999",
            species_taxon_id=None,
            has_taxonomic_rank="strain",
        )
        records = [record]

        count = infer_species_from_bacdive(records)

        assert count == 0
        assert record.species_taxon_id is None

    def test_skip_if_not_strain_rank(self) -> None:
        """Test skipping records not at strain rank."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            bacdive_id="12345",
            ncbi_taxon_id="NCBITaxon:999",
            species_taxon_id=None,
            has_taxonomic_rank="species",  # Not strain
        )
        records = [record]

        count = infer_species_from_bacdive(records)

        assert count == 0
        assert record.species_taxon_id is None

    def test_multiple_records(self) -> None:
        """Test inferring species for multiple records."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                bacdive_id="1",
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id=None,
                has_taxonomic_rank="strain",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                bacdive_id="2",
                ncbi_taxon_id="NCBITaxon:200",
                species_taxon_id=None,
                has_taxonomic_rank="strain",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=3,
                bacdive_id=None,  # Should be skipped
                ncbi_taxon_id="NCBITaxon:300",
                species_taxon_id=None,
                has_taxonomic_rank="strain",
            ),
        ]

        count = infer_species_from_bacdive(records)

        assert count == 2
        assert records[0].species_taxon_id == "100"
        assert records[1].species_taxon_id == "200"
        assert records[2].species_taxon_id is None


class TestInferSpeciesFromSelf:
    """Tests for infer_species_from_self()."""

    def test_infer_for_species_rank(self) -> None:
        """Test inferring species_taxon_id for species-level record."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:562",
            species_taxon_id=None,
            has_taxonomic_rank="species",
        )
        records = [record]

        count = infer_species_from_self(records)

        assert count == 1
        assert record.species_taxon_id == "562"

    def test_skip_if_species_already_set(self) -> None:
        """Test skipping records that already have species_taxon_id."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:562",
            species_taxon_id="999",  # Already set
            has_taxonomic_rank="species",
        )
        records = [record]

        count = infer_species_from_self(records)

        assert count == 0
        assert record.species_taxon_id == "999"  # Unchanged

    def test_skip_if_not_species_rank(self) -> None:
        """Test skipping records not at species rank."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:562",
            species_taxon_id=None,
            has_taxonomic_rank="strain",  # Not species
        )
        records = [record]

        count = infer_species_from_self(records)

        assert count == 0
        assert record.species_taxon_id is None

    def test_multiple_records(self) -> None:
        """Test inferring species for multiple species-level records."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id=None,
                has_taxonomic_rank="species",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                ncbi_taxon_id="NCBITaxon:200",
                species_taxon_id=None,
                has_taxonomic_rank="species",
            ),
        ]

        count = infer_species_from_self(records)

        assert count == 2
        assert records[0].species_taxon_id == "100"
        assert records[1].species_taxon_id == "200"


class TestInferTaxonomicRank:
    """Tests for infer_taxonomic_rank()."""

    def test_infer_strain_from_designation(self) -> None:
        """Test inferring strain rank from strain_designation."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            strain_designation="AM1",
            has_taxonomic_rank=None,
        )
        records = [record]

        count = infer_taxonomic_rank(records)

        assert count == 1
        assert record.has_taxonomic_rank == "strain"

    def test_infer_strain_from_bacdive(self) -> None:
        """Test inferring strain rank from bacdive_id."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            bacdive_id="12345",
            has_taxonomic_rank=None,
        )
        records = [record]

        count = infer_taxonomic_rank(records)

        assert count == 1
        assert record.has_taxonomic_rank == "strain"

    def test_infer_species_when_no_strain_evidence(self) -> None:
        """Test inferring species rank when no strain evidence."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            strain_designation=None,
            bacdive_id=None,
            has_taxonomic_rank=None,
        )
        records = [record]

        count = infer_taxonomic_rank(records)

        assert count == 1
        assert record.has_taxonomic_rank == "species"

    def test_skip_if_rank_already_set(self) -> None:
        """Test skipping records that already have rank from NCBI."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            strain_designation="AM1",
            has_taxonomic_rank="species",  # Already set by NCBI
        )
        records = [record]

        count = infer_taxonomic_rank(records)

        assert count == 0
        assert record.has_taxonomic_rank == "species"  # Unchanged

    def test_multiple_records_mixed(self) -> None:
        """Test inferring rank for multiple records with different evidence."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                strain_designation="AM1",
                has_taxonomic_rank=None,
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                bacdive_id="12345",
                has_taxonomic_rank=None,
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=3,
                strain_designation=None,
                bacdive_id=None,
                has_taxonomic_rank=None,
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=4,
                strain_designation="TEST",
                has_taxonomic_rank="subspecies",  # Already set
            ),
        ]

        count = infer_taxonomic_rank(records)

        assert count == 3  # First 3 records
        assert records[0].has_taxonomic_rank == "strain"
        assert records[1].has_taxonomic_rank == "strain"
        assert records[2].has_taxonomic_rank == "species"
        assert records[3].has_taxonomic_rank == "subspecies"  # Unchanged


class TestRunInferencePipeline:
    """Tests for run_inference_pipeline()."""

    def test_empty_records(self) -> None:
        """Test running pipeline on empty list."""
        records: list[StrainRecord] = []

        counts = run_inference_pipeline(records)

        assert counts["taxonomic_rank"] == 0
        assert counts["species_from_bacdive"] == 0
        assert counts["species_from_self"] == 0

    def test_pipeline_runs_all_steps(self) -> None:
        """Test that pipeline runs all inference steps."""
        records = [
            # Will infer rank=strain and species from bacdive
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                bacdive_id="123",
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id=None,
                has_taxonomic_rank=None,
            ),
            # Will infer rank=species and species from self
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                ncbi_taxon_id="NCBITaxon:200",
                species_taxon_id=None,
                has_taxonomic_rank=None,
            ),
        ]

        counts = run_inference_pipeline(records)

        # First pass infers taxonomic_rank
        assert counts["taxonomic_rank"] == 2
        # Second pass infers species from bacdive for strain
        assert counts["species_from_bacdive"] == 1
        # Third pass infers species from self for species
        assert counts["species_from_self"] == 1

        # Check final states
        assert records[0].has_taxonomic_rank == "strain"
        assert records[0].species_taxon_id == "100"
        assert records[1].has_taxonomic_rank == "species"
        assert records[1].species_taxon_id == "200"

    def test_pipeline_with_no_inference_needed(self) -> None:
        """Test pipeline on records that don't need inference."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id="100",
                has_taxonomic_rank="strain",
            )
        ]

        counts = run_inference_pipeline(records)

        assert counts["taxonomic_rank"] == 0
        assert counts["species_from_bacdive"] == 0
        assert counts["species_from_self"] == 0

    def test_pipeline_returns_dict(self) -> None:
        """Test that pipeline returns properly formatted dict."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                strain_designation="TEST",
                has_taxonomic_rank=None,
            )
        ]

        counts = run_inference_pipeline(records)

        assert isinstance(counts, dict)
        assert "taxonomic_rank" in counts
        assert "species_from_bacdive" in counts
        assert "species_from_self" in counts
        assert all(isinstance(v, int) for v in counts.values())
