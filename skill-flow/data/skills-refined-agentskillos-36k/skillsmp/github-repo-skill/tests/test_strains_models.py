"""Tests for strains models and data structures."""

from cmm_ai_automation.strains.models import (
    BIOLINK_CATEGORY,
    COLLECTION_PREFIX_MAP,
    RANK_TO_TAXRANK,
    TAXRANK_LABELS,
    StrainRecord,
)


class TestConstants:
    """Tests for module-level constants."""

    def test_biolink_category(self) -> None:
        """Test BIOLINK_CATEGORY constant."""
        assert BIOLINK_CATEGORY == "biolink:OrganismTaxon"

    def test_rank_to_taxrank_has_common_ranks(self) -> None:
        """Test that RANK_TO_TAXRANK has common taxonomic ranks."""
        assert "species" in RANK_TO_TAXRANK
        assert "genus" in RANK_TO_TAXRANK
        assert "strain" in RANK_TO_TAXRANK
        assert RANK_TO_TAXRANK["species"] == "TAXRANK:0000006"
        assert RANK_TO_TAXRANK["strain"] == "TAXRANK:0000060"

    def test_taxrank_labels_matches_rank_values(self) -> None:
        """Test that TAXRANK_LABELS has entries for rank CURIEs."""
        for curie in RANK_TO_TAXRANK.values():
            if curie:  # Skip empty strings
                assert curie in TAXRANK_LABELS

    def test_collection_prefix_map_has_common_collections(self) -> None:
        """Test that COLLECTION_PREFIX_MAP has common culture collections."""
        assert "DSM" in COLLECTION_PREFIX_MAP
        assert "ATCC" in COLLECTION_PREFIX_MAP
        assert "JCM" in COLLECTION_PREFIX_MAP
        assert COLLECTION_PREFIX_MAP["DSM"] == "dsmz"
        assert COLLECTION_PREFIX_MAP["ATCC"] == "atcc"


class TestStrainRecord:
    """Tests for StrainRecord dataclass."""

    def test_create_minimal_record(self) -> None:
        """Test creating record with only required fields."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
        )
        assert record.source_sheet == "test.tsv"
        assert record.source_row == 1
        assert record.id is None
        assert record.name is None

    def test_create_full_record(self) -> None:
        """Test creating record with all fields."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            id="NCBITaxon:408",
            name="Methylobacterium extorquens AM1",
            scientific_name="Methylobacterium extorquens",
            strain_designation="AM1",
            ncbi_taxon_id="NCBITaxon:408",
            species_taxon_id="408",
            parent_taxon_id="407",
            culture_collection_ids=["DSM:16371", "ATCC:700829"],
            primary_collection_id="DSM:16371",
            bacdive_id="12345",
            genome_accession="GCA_000022685.1",
            has_taxonomic_rank="strain",
            synonyms=["M. extorquens AM1"],
            xrefs=["bacdive:12345"],
        )
        assert record.id == "NCBITaxon:408"
        assert record.name == "Methylobacterium extorquens AM1"
        assert record.strain_designation == "AM1"
        assert len(record.culture_collection_ids) == 2
        assert record.has_taxonomic_rank == "strain"

    def test_determine_canonical_id_prefers_bacdive(self) -> None:
        """Test that _determine_canonical_id() prefers BacDive ID (most strain-specific)."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:408",
            primary_collection_id="DSM:16371",
            bacdive_id="12345",
        )
        canonical_id = record._determine_canonical_id()
        assert canonical_id == "bacdive:12345"

    def test_determine_canonical_id_falls_back_to_ncbi(self) -> None:
        """Test fallback to NCBITaxon ID when no BacDive ID (only if strain-specific)."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="408",
            species_taxon_id="382",  # Different species - confirms this is strain-level
            bacdive_id=None,
            primary_collection_id="DSM:16371",
        )
        canonical_id = record._determine_canonical_id()
        assert canonical_id == "NCBITaxon:408"

    def test_determine_canonical_id_falls_back_to_collection(self) -> None:
        """Test fallback to collection ID when no BacDive and no strain-level NCBI."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id=None,
            bacdive_id=None,
            primary_collection_id="DSM:16371",
        )
        canonical_id = record._determine_canonical_id()
        assert canonical_id == "dsmz:16371"

    def test_determine_canonical_id_handles_unknown_collection(self) -> None:
        """Test handling unknown collection prefix."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id=None,
            bacdive_id=None,
            primary_collection_id="UNKNOWN:123",
        )
        canonical_id = record._determine_canonical_id()
        assert canonical_id.startswith("unknown:")

    def test_build_display_name_with_both(self) -> None:
        """Test building display name with scientific name and designation."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            scientific_name="Escherichia coli",
            strain_designation="K-12",
        )
        display_name = record._build_display_name()
        assert display_name == "Escherichia coli K-12"

    def test_build_display_name_scientific_only(self) -> None:
        """Test building display name with only scientific name."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            scientific_name="Escherichia coli",
            strain_designation=None,
        )
        display_name = record._build_display_name()
        assert display_name == "Escherichia coli"

    def test_build_display_name_designation_only(self) -> None:
        """Test building display name with only designation."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            scientific_name=None,
            strain_designation="K-12",
        )
        display_name = record._build_display_name()
        assert display_name == "K-12"

    def test_build_display_name_fallback_to_unknown(self) -> None:
        """Test fallback to 'Unknown strain' when no name components."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            scientific_name=None,
            strain_designation=None,
        )
        display_name = record._build_display_name()
        assert display_name == "Unknown strain"

    def test_collect_xrefs(self) -> None:
        """Test collecting cross-references."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:408",
            species_taxon_id="500",  # Different from ncbi_taxon_id
            culture_collection_ids=["DSM:16371", "ATCC:700829"],
            bacdive_id="12345",
            xrefs=["custom:ref"],
        )
        xrefs = record._collect_xrefs()
        # Should have culture collections and species taxon, plus custom xref
        assert "dsmz:16371" in xrefs or "DSM:16371" in xrefs or any("16371" in x for x in xrefs)
        assert "custom:ref" in xrefs
        # Species taxon added as xref since it differs from main taxon
        assert "NCBITaxon:500" in xrefs

    def test_to_kgx_node_complete_record(self) -> None:
        """Test converting complete record to KGX node."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            name="Methylobacterium extorquens AM1",
            ncbi_taxon_id="NCBITaxon:408",
            species_taxon_id="408",
            parent_taxon_id="407",
            strain_designation="AM1",
            has_taxonomic_rank="strain",
            bacdive_id="12345",
            genome_accession="GCA_000022685.1",
            synonyms=["M. extorquens AM1"],
        )

        node = record.to_kgx_node()

        assert node["id"] == "bacdive:12345"  # BacDive preferred over NCBITaxon
        assert node["category"] == "biolink:OrganismTaxon"
        assert node["name"] == "Methylobacterium extorquens AM1"
        assert node["ncbi_taxon_id"] == "NCBITaxon:408"
        assert node["species_taxon_id"] == "408"
        assert node["parent_taxon_id"] == "407"
        assert node["strain_designation"] == "AM1"
        assert node["has_taxonomic_rank"] == "TAXRANK:0000060"
        assert node["bacdive_id"] == "bacdive:12345"
        assert node["genome_accession"] == "GCA_000022685.1"
        assert "M. extorquens AM1" in node["synonyms"]
        assert node["source_sheet"] == "test.tsv"

    def test_to_kgx_node_minimal_record(self) -> None:
        """Test converting minimal record to KGX node."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            primary_collection_id="DSM:16371",
        )

        node = record.to_kgx_node()

        assert node["id"] == "dsmz:16371"
        assert node["category"] == "biolink:OrganismTaxon"
        assert node["name"] == "Unknown strain"  # No name components
        assert node["ncbi_taxon_id"] == ""
        assert node["species_taxon_id"] == ""
        assert node["strain_designation"] == ""
        assert node["has_taxonomic_rank"] == ""
        assert node["bacdive_id"] == ""
        assert node["synonyms"] == ""

    def test_to_kgx_node_handles_synonyms_list(self) -> None:
        """Test that synonyms are properly joined with pipes."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            primary_collection_id="DSM:1",
            synonyms=["Name 1", "Name 2", "Name 3"],
        )

        node = record.to_kgx_node()

        assert node["synonyms"] == "Name 1|Name 2|Name 3"

    def test_to_kgx_node_handles_xrefs_list(self) -> None:
        """Test that xrefs are properly collected and joined."""
        record = StrainRecord(
            source_sheet="test.tsv",
            source_row=1,
            ncbi_taxon_id="NCBITaxon:408",
            species_taxon_id="500",  # Different from main to generate xref
            culture_collection_ids=["DSM:16371"],
        )

        node = record.to_kgx_node()

        # Should have species taxon xref and culture collection
        xrefs_str = node["xrefs"]
        assert "NCBITaxon:500" in xrefs_str  # Species taxon xref
        assert any(x in xrefs_str for x in ["dsmz", "DSM", "16371"])  # Culture collection
        assert "|" in xrefs_str or len(xrefs_str.split()) > 1  # Multiple xrefs
