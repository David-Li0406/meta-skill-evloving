"""Tests for strains_kgx_from_curies script."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

from cmm_ai_automation.scripts.strains_kgx_from_curies import (
    BIOLINK_ORGANISM_TAXON,
    COLLECTION_PREFIX_MAP,
    RANK_TO_TAXRANK,
    StrainResult,
    export_kgx,
    normalize_collection_curie,
    parse_curie,
    read_curies_from_file,
    sample_entries,
)


class TestParseCurie:
    """Tests for parse_curie function."""

    def test_parse_bacdive_curie(self) -> None:
        """Test parsing bacdive CURIE."""
        prefix, local_id = parse_curie("bacdive:7142")
        assert prefix == "bacdive"
        assert local_id == "7142"

    def test_parse_ncbitaxon_curie(self) -> None:
        """Test parsing NCBITaxon CURIE."""
        prefix, local_id = parse_curie("NCBITaxon:408")
        assert prefix == "NCBITaxon"
        assert local_id == "408"

    def test_parse_curie_with_whitespace(self) -> None:
        """Test parsing CURIE with surrounding whitespace."""
        prefix, local_id = parse_curie("  bacdive:7142  ")
        assert prefix == "bacdive"
        assert local_id == "7142"

    def test_parse_invalid_curie_no_colon(self) -> None:
        """Test that invalid CURIE without colon raises ValueError."""
        with pytest.raises(ValueError, match="no colon"):
            parse_curie("bacdive7142")


class TestNormalizeCollectionCurie:
    """Tests for normalize_collection_curie function."""

    def test_normalize_dsm_to_dsmz(self) -> None:
        """Test DSM is normalized to dsmz prefix."""
        assert normalize_collection_curie("DSM:16371") == "dsmz:16371"
        assert normalize_collection_curie("DSMZ:16371") == "dsmz:16371"

    def test_normalize_with_space_separator(self) -> None:
        """Test parsing 'DSM 16371' format."""
        assert normalize_collection_curie("DSM 16371") == "dsmz:16371"

    def test_normalize_with_hyphen_separator(self) -> None:
        """Test parsing 'DSM-16371' format."""
        assert normalize_collection_curie("DSM-16371") == "dsmz:16371"

    def test_normalize_atcc(self) -> None:
        """Test ATCC normalization."""
        assert normalize_collection_curie("ATCC:35073") == "atcc:35073"
        assert normalize_collection_curie("ATCC 35073") == "atcc:35073"

    def test_normalize_jcm(self) -> None:
        """Test JCM normalization."""
        assert normalize_collection_curie("JCM:2831") == "jcm:2831"

    def test_normalize_ifo_to_nbrc(self) -> None:
        """Test IFO is normalized to nbrc (merged collection)."""
        assert normalize_collection_curie("IFO:12345") == "nbrc:12345"

    def test_normalize_unknown_prefix(self) -> None:
        """Test unknown prefix is lowercased."""
        assert normalize_collection_curie("UNKNOWN:12345") == "unknown:12345"

    def test_normalize_already_curie(self) -> None:
        """Test already valid CURIE format."""
        assert normalize_collection_curie("dsmz:16371") == "dsmz:16371"


class TestCollectionPrefixMap:
    """Tests for COLLECTION_PREFIX_MAP constants."""

    def test_common_collections_mapped(self) -> None:
        """Test that common culture collections are mapped."""
        assert "DSM" in COLLECTION_PREFIX_MAP
        assert "DSMZ" in COLLECTION_PREFIX_MAP
        assert "ATCC" in COLLECTION_PREFIX_MAP
        assert "JCM" in COLLECTION_PREFIX_MAP
        assert "NBRC" in COLLECTION_PREFIX_MAP

    def test_merged_collections_mapped(self) -> None:
        """Test that merged collections map to current names."""
        assert COLLECTION_PREFIX_MAP["IFO"] == "nbrc"  # IFO merged into NBRC
        assert COLLECTION_PREFIX_MAP["NCIB"] == "ncimb"  # NCIB merged into NCIMB


class TestRankToTaxrank:
    """Tests for RANK_TO_TAXRANK constants."""

    def test_common_ranks_mapped(self) -> None:
        """Test that common taxonomic ranks are mapped."""
        assert RANK_TO_TAXRANK["species"] == "TAXRANK:0000006"
        assert RANK_TO_TAXRANK["subspecies"] == "TAXRANK:0000023"
        assert RANK_TO_TAXRANK["strain"] == "TAXRANK:0001001"

    def test_no_rank_maps_to_empty(self) -> None:
        """Test that 'no rank' maps to empty string."""
        assert RANK_TO_TAXRANK["no rank"] == ""


class TestStrainResult:
    """Tests for StrainResult dataclass."""

    def test_create_basic_result(self) -> None:
        """Test creating a basic StrainResult."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            scientific_name="Methylobacterium extorquens",
            strain_designation="AM1",
        )
        assert result.input_curie == "bacdive:7142"
        assert result.canonical_id == "bacdive:7142"
        assert result.scientific_name == "Methylobacterium extorquens"
        assert result.strain_designation == "AM1"

    def test_to_kgx_node_basic(self) -> None:
        """Test converting StrainResult to KGX node."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            binomial_name="Methylobacterium extorquens",
            strain_designation="AM1",
            ncbi_taxon_id="408",
            species_taxon_id="382",
        )
        node = result.to_kgx_node()

        assert node["id"] == "bacdive:7142"
        assert node["category"] == [BIOLINK_ORGANISM_TAXON]  # List for KGX Sink
        assert "Methylobacterium extorquens" in node["name"]
        assert "AM1" in node["name"]
        assert node["ncbi_taxon_id"] == "NCBITaxon:408"
        assert node["species_taxon_id"] == "NCBITaxon:382"

    def test_to_kgx_node_with_bacdive_forces_strain_rank(self) -> None:
        """Test that BacDive entries are always marked as strain rank."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            bacdive_id="7142",
            has_taxonomic_rank="species",  # Would normally map to species
        )
        node = result.to_kgx_node()

        # BacDive entries should be forced to strain rank
        assert node["has_taxonomic_rank"] == RANK_TO_TAXRANK["strain"]

    def test_to_kgx_node_normalizes_xrefs(self) -> None:
        """Test that culture collection xrefs are normalized."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            culture_collection_ids=["DSM 13060", "ATCC:33596"],
            xrefs=["JCM 2831"],
        )
        node = result.to_kgx_node()

        # All should be normalized to lowercase prefix:id format
        assert "dsmz:13060" in node["xref"]
        assert "atcc:33596" in node["xref"]
        assert "jcm:2831" in node["xref"]

    def test_to_kgx_node_with_genome_accessions(self) -> None:
        """Test that genome accessions are included."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            genome_accessions_ncbi=["GCA_000022685.1"],
            genome_accessions_img=["2509276011"],
        )
        node = result.to_kgx_node()

        assert "GCA_000022685.1" in node["genome_accessions_ncbi"]
        assert "2509276011" in node["genome_accessions_img"]

    def test_to_kgx_node_with_synonyms(self) -> None:
        """Test that synonyms are returned as a list."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            synonyms=["M. extorquens", "Methylobacterium sp. AM1"],
        )
        node = result.to_kgx_node()

        assert "M. extorquens" in node["synonym"]
        assert isinstance(node["synonym"], list)  # Lists for KGX Sink

    def test_to_kgx_node_name_from_binomial_and_strain(self) -> None:
        """Test that name is constructed from binomial + strain."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            binomial_name="Methylobacterium extorquens",
            strain_designation="AM1",
        )
        node = result.to_kgx_node()

        assert node["name"] == "Methylobacterium extorquens AM1"

    def test_to_kgx_node_name_uses_explicit_name(self) -> None:
        """Test that explicit name takes precedence."""
        result = StrainResult(
            input_curie="bacdive:7142",
            canonical_id="bacdive:7142",
            name="Custom Name",
            binomial_name="Methylobacterium extorquens",
            strain_designation="AM1",
        )
        node = result.to_kgx_node()

        assert node["name"] == "Custom Name"


class TestSampleEntries:
    """Tests for sample_entries function."""

    def test_sample_n(self) -> None:
        """Test sampling N entries."""
        entries = [{"curie": f"bacdive:{i}"} for i in range(100)]
        sampled = sample_entries(entries, sample_n=10)

        assert len(sampled) == 10
        for entry in sampled:
            assert entry in entries

    def test_sample_n_larger_than_list(self) -> None:
        """Test sampling more than available."""
        entries = [{"curie": f"bacdive:{i}"} for i in range(5)]
        sampled = sample_entries(entries, sample_n=10)

        assert len(sampled) == 5

    def test_sample_fraction(self) -> None:
        """Test sampling by fraction."""
        entries = [{"curie": f"bacdive:{i}"} for i in range(100)]
        sampled = sample_entries(entries, sample_fraction=0.1)

        assert len(sampled) == 10

    def test_no_sampling(self) -> None:
        """Test that no sampling returns original list."""
        entries = [{"curie": f"bacdive:{i}"} for i in range(10)]
        sampled = sample_entries(entries)

        assert sampled == entries


class TestReadCuriesFromFile:
    """Tests for read_curies_from_file function."""

    def test_read_tsv_file(self, tmp_path: Path) -> None:
        """Test reading TSV file."""
        test_file = tmp_path / "strains.tsv"
        test_file.write_text("strain_id\tname\nbacdive:7142\tM. extorquens AM1\nNCBITaxon:408\tM. extorquens\n")

        entries = read_curies_from_file(test_file, "strain_id")

        assert len(entries) == 2
        assert entries[0]["curie"] == "bacdive:7142"
        assert entries[1]["curie"] == "NCBITaxon:408"

    def test_read_with_comments_field(self, tmp_path: Path) -> None:
        """Test reading with comments field."""
        test_file = tmp_path / "strains.tsv"
        test_file.write_text("strain_id\tnotes\nbacdive:7142\tModel organism\n")

        entries = read_curies_from_file(test_file, "strain_id", comments_field="notes")

        assert entries[0]["comments"] == "Model organism"

    def test_read_with_synonyms_field(self, tmp_path: Path) -> None:
        """Test reading with synonyms field."""
        test_file = tmp_path / "strains.tsv"
        test_file.write_text("strain_id\taliases\nbacdive:7142\tAM1|Pink pigmented facultative methylotroph\n")

        entries = read_curies_from_file(test_file, "strain_id", synonyms_field="aliases")

        assert entries[0]["synonyms"] == "AM1|Pink pigmented facultative methylotroph"

    def test_read_skips_empty_ids(self, tmp_path: Path) -> None:
        """Test that empty IDs are skipped."""
        test_file = tmp_path / "strains.tsv"
        test_file.write_text("strain_id\tname\nbacdive:7142\tAM1\n\tno_id\nNCBITaxon:408\textorquens\n")

        entries = read_curies_from_file(test_file, "strain_id")

        assert len(entries) == 2
        assert entries[0]["curie"] == "bacdive:7142"
        assert entries[1]["curie"] == "NCBITaxon:408"


class TestExportKgx:
    """Tests for export_kgx function."""

    def test_export_creates_files(self, tmp_path: Path) -> None:
        """Test that export_kgx creates both nodes and edges files."""
        results = [
            StrainResult(
                input_curie="bacdive:7142",
                canonical_id="bacdive:7142",
                binomial_name="Methylobacterium extorquens",
                strain_designation="AM1",
                species_taxon_id="382",
            )
        ]

        strain_count, species_count, edge_count = export_kgx(results, tmp_path)

        assert strain_count == 1
        assert edge_count == 1
        nodes_path = tmp_path / "strains_nodes.tsv"
        edges_path = tmp_path / "strains_edges.tsv"
        assert nodes_path.exists()
        assert edges_path.exists()

        nodes_content = nodes_path.read_text()
        assert "bacdive:7142" in nodes_content
        assert "Methylobacterium extorquens" in nodes_content

        edges_content = edges_path.read_text()
        assert "bacdive:7142" in edges_content
        assert "biolink:in_taxon" in edges_content

    def test_export_has_provenance(self, tmp_path: Path) -> None:
        """Test that edges have proper provenance fields."""
        results = [
            StrainResult(
                input_curie="bacdive:7142",
                canonical_id="bacdive:7142",
                species_taxon_id="382",
            )
        ]

        export_kgx(results, tmp_path)

        edges_content = (tmp_path / "strains_edges.tsv").read_text()
        assert "knowledge_assertion" in edges_content
        assert "manual_agent" in edges_content
        assert "infores:cmm-ai-automation" in edges_content

    def test_export_no_edges_without_species(self, tmp_path: Path) -> None:
        """Test that strains without species produce no edges."""
        results = [
            StrainResult(
                input_curie="bacdive:7142",
                canonical_id="bacdive:7142",
                species_taxon_id="",  # No species
            )
        ]

        strain_count, species_count, edge_count = export_kgx(results, tmp_path)

        assert edge_count == 0

    def test_export_no_self_loops(self, tmp_path: Path) -> None:
        """Test that self-loops are not created."""
        results = [
            StrainResult(
                input_curie="NCBITaxon:382",
                canonical_id="NCBITaxon:382",
                species_taxon_id="382",  # Same as canonical - would be self-loop
            )
        ]

        strain_count, species_count, edge_count = export_kgx(results, tmp_path)

        assert edge_count == 0
