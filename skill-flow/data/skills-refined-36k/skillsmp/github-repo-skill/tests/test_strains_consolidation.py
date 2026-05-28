"""Tests for strain record consolidation and deduplication."""

from cmm_ai_automation.strains.consolidation import (
    consolidate_strains,
    deduplicate_by_canonical_id,
    merge_records,
)
from cmm_ai_automation.strains.models import StrainRecord


class TestMergeRecords:
    """Tests for merge_records()."""

    def test_merge_fills_missing_name(self) -> None:
        """Test merging fills in missing name."""
        target = StrainRecord(source_sheet="test.tsv", source_row=1, name=None)
        source = StrainRecord(source_sheet="test.tsv", source_row=2, name="Test strain")

        merge_records(target, source)

        assert target.name == "Test strain"

    def test_merge_preserves_existing_name(self) -> None:
        """Test merging preserves existing name."""
        target = StrainRecord(source_sheet="test.tsv", source_row=1, name="Original")
        source = StrainRecord(source_sheet="test.tsv", source_row=2, name="New")

        merge_records(target, source)

        assert target.name == "Original"

    def test_merge_fills_all_simple_fields(self) -> None:
        """Test merging fills all simple scalar fields."""
        target = StrainRecord(source_sheet="test.tsv", source_row=1)
        source = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            scientific_name="Bacterium test",
            strain_designation="TEST1",
            ncbi_taxon_id="NCBITaxon:123",
            species_taxon_id="122",
            parent_taxon_id="121",
            bacdive_id="12345",
            genome_accession="GCA_000000001.1",
            has_taxonomic_rank="strain",
        )

        merge_records(target, source)

        assert target.scientific_name == "Bacterium test"
        assert target.strain_designation == "TEST1"
        assert target.ncbi_taxon_id == "NCBITaxon:123"
        assert target.species_taxon_id == "122"
        assert target.parent_taxon_id == "121"
        assert target.bacdive_id == "12345"
        assert target.genome_accession == "GCA_000000001.1"
        assert target.has_taxonomic_rank == "strain"

    def test_merge_combines_culture_collection_ids(self) -> None:
        """Test merging combines culture collection IDs."""
        target = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            culture_collection_ids=["DSM:1", "ATCC:100"],
        )
        source = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            culture_collection_ids=["ATCC:100", "JCM:200"],  # One duplicate, one new
        )

        merge_records(target, source)

        assert len(target.culture_collection_ids) == 3
        assert "DSM:1" in target.culture_collection_ids
        assert "ATCC:100" in target.culture_collection_ids
        assert "JCM:200" in target.culture_collection_ids

    def test_merge_combines_synonyms(self) -> None:
        """Test merging combines synonyms."""
        target = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            synonyms=["Name 1", "Name 2"],
        )
        source = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            synonyms=["Name 2", "Name 3"],  # One duplicate, one new
        )

        merge_records(target, source)

        assert len(target.synonyms) == 3
        assert "Name 1" in target.synonyms
        assert "Name 2" in target.synonyms
        assert "Name 3" in target.synonyms

    def test_merge_combines_xrefs(self) -> None:
        """Test merging combines xrefs."""
        target = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            xrefs=["ref:1", "ref:2"],
        )
        source = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            xrefs=["ref:2", "ref:3"],  # One duplicate, one new
        )

        merge_records(target, source)

        assert len(target.xrefs) == 3
        assert "ref:1" in target.xrefs
        assert "ref:2" in target.xrefs
        assert "ref:3" in target.xrefs

    def test_merge_with_empty_source(self) -> None:
        """Test merging with empty source doesn't change target."""
        target = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            name="Original",
            ncbi_taxon_id="NCBITaxon:123",
        )
        source = StrainRecord(source_sheet="test.tsv", source_row=2)

        merge_records(target, source)

        assert target.name == "Original"
        assert target.ncbi_taxon_id == "NCBITaxon:123"


class TestConsolidateStrains:
    """Tests for consolidate_strains()."""

    def test_consolidate_empty_list(self) -> None:
        """Test consolidating empty list."""
        result = consolidate_strains([])
        assert result == []

    def test_consolidate_single_record(self) -> None:
        """Test consolidating single record."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:123",
        )
        result = consolidate_strains([record])

        assert len(result) == 1
        assert result[0].ncbi_taxon_id == "NCBITaxon:123"

    def test_consolidate_by_ncbi_id(self) -> None:
        """Test consolidating records with same NCBI ID."""
        record1 = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:123",
            name="Name from record 1",
        )
        record2 = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            ncbi_taxon_id="NCBITaxon:123",
            scientific_name="Name from record 2",
        )
        result = consolidate_strains([record1, record2])

        assert len(result) == 1
        assert result[0].name == "Name from record 1"  # From first record
        assert result[0].scientific_name == "Name from record 2"  # From second record

    def test_consolidate_by_collection_id(self) -> None:
        """Test consolidating records with same collection ID."""
        record1 = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            primary_collection_id="DSM:1234",
            name="Name 1",
        )
        record2 = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            primary_collection_id="DSM:1234",
            scientific_name="Scientific name",
        )
        result = consolidate_strains([record1, record2])

        assert len(result) == 1
        assert result[0].name == "Name 1"
        assert result[0].scientific_name == "Scientific name"

    def test_consolidate_by_name(self) -> None:
        """Test consolidating records with same name."""
        record1 = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            name="Test Strain",
            strain_designation="AM1",
        )
        record2 = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            name="Test Strain",  # Same name
            ncbi_taxon_id="NCBITaxon:123",
        )
        result = consolidate_strains([record1, record2])

        assert len(result) == 1
        assert result[0].name == "Test Strain"
        assert result[0].strain_designation == "AM1"
        assert result[0].ncbi_taxon_id == "NCBITaxon:123"

    def test_consolidate_case_insensitive_names(self) -> None:
        """Test that name matching is case-insensitive."""
        record1 = StrainRecord(source_sheet="test.tsv", source_row=1, name="Test Strain")
        record2 = StrainRecord(source_sheet="test.tsv", source_row=2, name="test strain")

        result = consolidate_strains([record1, record2])

        assert len(result) == 1

    def test_consolidate_keeps_separate_strains(self) -> None:
        """Test that different strains are not merged."""
        record1 = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:123",
        )
        record2 = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            ncbi_taxon_id="NCBITaxon:456",
        )
        record3 = StrainRecord(
            source_sheet="test.tsv",
            source_row=3,
            primary_collection_id="DSM:999",
        )

        result = consolidate_strains([record1, record2, record3])

        assert len(result) == 3

    def test_consolidate_multiple_matches(self) -> None:
        """Test consolidating multiple records of same strain."""
        records = [
            StrainRecord(source_sheet="s1.tsv", source_row=1, name="Strain A", strain_designation="A1"),
            StrainRecord(source_sheet="s2.tsv", source_row=1, name="Strain A", ncbi_taxon_id="NCBITaxon:100"),
            StrainRecord(source_sheet="s3.tsv", source_row=1, name="Strain A", genome_accession="GCA_000000001.1"),
        ]

        result = consolidate_strains(records)

        assert len(result) == 1
        assert result[0].name == "Strain A"
        assert result[0].strain_designation == "A1"
        assert result[0].ncbi_taxon_id == "NCBITaxon:100"
        assert result[0].genome_accession == "GCA_000000001.1"


class TestDeduplicateByCanonicalId:
    """Tests for deduplicate_by_canonical_id()."""

    def test_deduplicate_empty_list(self) -> None:
        """Test deduplicating empty list."""
        result = deduplicate_by_canonical_id([])
        assert result == []

    def test_deduplicate_no_duplicates(self) -> None:
        """Test deduplicating records with different canonical IDs."""
        records = [
            StrainRecord(source_sheet="test.tsv", source_row=1, ncbi_taxon_id="NCBITaxon:100"),
            StrainRecord(source_sheet="test.tsv", source_row=2, ncbi_taxon_id="NCBITaxon:200"),
            StrainRecord(source_sheet="test.tsv", source_row=3, ncbi_taxon_id="NCBITaxon:300"),
        ]

        result = deduplicate_by_canonical_id(records)

        assert len(result) == 3

    def test_deduplicate_same_canonical_id(self) -> None:
        """Test deduplicating records with same canonical ID."""
        record1 = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:100",
            species_taxon_id="99",  # Different from ncbi_taxon_id - makes it strain-specific
            name="Name from first",
        )
        record2 = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            ncbi_taxon_id="NCBITaxon:100",
            species_taxon_id="99",  # Same as above - same canonical ID
            scientific_name="Scientific name from second",
        )

        result = deduplicate_by_canonical_id([record1, record2])

        assert len(result) == 1
        assert result[0].name == "Name from first"
        assert result[0].scientific_name == "Scientific name from second"

    def test_deduplicate_by_collection_id(self) -> None:
        """Test deduplicating by collection ID when no NCBI ID."""
        record1 = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            primary_collection_id="DSM:1234",
            name="Name 1",
        )
        record2 = StrainRecord(
            source_sheet="test.tsv",
            source_row=2,
            primary_collection_id="DSM:1234",
            strain_designation="A1",
        )

        result = deduplicate_by_canonical_id([record1, record2])

        assert len(result) == 1
        assert result[0].name == "Name 1"
        assert result[0].strain_designation == "A1"

    def test_deduplicate_merges_multiple(self) -> None:
        """Test deduplicating merges all records with same canonical ID."""
        records = [
            StrainRecord(
                source_sheet="test.tsv",
                source_row=1,
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id="99",  # Makes it strain-specific
                name="Name",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=2,
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id="99",
                strain_designation="A1",
            ),
            StrainRecord(
                source_sheet="test.tsv",
                source_row=3,
                ncbi_taxon_id="NCBITaxon:100",
                species_taxon_id="99",
                genome_accession="GCA_000000001.1",
            ),
        ]

        result = deduplicate_by_canonical_id(records)

        assert len(result) == 1
        assert result[0].name == "Name"
        assert result[0].strain_designation == "A1"
        assert result[0].genome_accession == "GCA_000000001.1"

    def test_deduplicate_preserves_first_record(self) -> None:
        """Test that first record in group is preserved."""
        record1 = StrainRecord(
            source_sheet="first.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:100",
            species_taxon_id="99",  # Makes it strain-specific
        )
        record2 = StrainRecord(
            source_sheet="second.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:100",
            species_taxon_id="99",  # Same as above
        )

        result = deduplicate_by_canonical_id([record1, record2])

        assert len(result) == 1
        assert result[0].source_sheet == "first.tsv"
        assert result[0].source_row == 1
