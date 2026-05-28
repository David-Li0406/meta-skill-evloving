"""Tests for strain KGX export script."""

from __future__ import annotations

from typing import Any

import pytest

from cmm_ai_automation.strains import StrainRecord
from cmm_ai_automation.strains.bacdive import extract_bacdive_data
from cmm_ai_automation.strains.enrichment import generate_query_variants
from cmm_ai_automation.strains.models import BIOLINK_CATEGORY, COLLECTION_PREFIX_MAP
from cmm_ai_automation.strains.ncbi import fetch_ncbi_synonyms


class TestStrainRecord:
    """Tests for StrainRecord dataclass."""

    def test_create_basic_record(self) -> None:
        """Test creating a basic strain record."""
        record = StrainRecord(
            source_sheet="strains.tsv",
            source_row=2,
            scientific_name="Methylobacterium aquaticum",
            strain_designation="GR16",
        )
        assert record.source_sheet == "strains.tsv"
        assert record.source_row == 2
        assert record.scientific_name == "Methylobacterium aquaticum"
        assert record.strain_designation == "GR16"
        assert record.culture_collection_ids == []
        assert record.synonyms == []

    def test_to_kgx_node_with_ncbi_taxon(self) -> None:
        """Test KGX node uses strain-specific NCBITaxon ID when no BacDive."""
        record = StrainRecord(
            source_sheet="strains.tsv",
            source_row=2,
            name="Methylobacterium aquaticum GR16",
            ncbi_taxon_id="270351",
            species_taxon_id="270350",  # Different from strain taxon - makes it strain-specific
            strain_designation="GR16",
        )
        node = record.to_kgx_node()
        assert node["id"] == "NCBITaxon:270351"
        assert node["category"] == BIOLINK_CATEGORY
        assert node["name"] == "Methylobacterium aquaticum GR16"
        assert node["ncbi_taxon_id"] == "270351"

    def test_to_kgx_node_with_bacdive_preferred(self) -> None:
        """Test KGX node prefers BacDive ID over NCBITaxon."""
        record = StrainRecord(
            source_sheet="strains.tsv",
            source_row=2,
            name="Unknown strain X",
            bacdive_id="12345",
            ncbi_taxon_id="408",
            species_taxon_id="382",  # Different species - confirms strain-level
        )
        node = record.to_kgx_node()
        assert node["id"] == "bacdive:12345"  # BacDive preferred even when NCBITaxon available
        assert node["bacdive_id"] == "bacdive:12345"

    def test_to_kgx_node_with_collection_fallback(self) -> None:
        """Test KGX node uses culture collection ID when no NCBITaxon or BacDive."""
        record = StrainRecord(
            source_sheet="strains.tsv",
            source_row=2,
            primary_collection_id="DSM:16371",
        )
        node = record.to_kgx_node()
        assert node["id"] == "dsmz:16371"

    def test_normalize_collection_curie_dsm(self) -> None:
        """Test DSM/DSMZ normalization to bioregistry prefix."""
        record = StrainRecord(source_sheet="test", source_row=1)

        # DSM -> dsmz
        assert record._normalize_collection_curie("DSM:16371") == "dsmz:16371"
        assert record._normalize_collection_curie("DSMZ:16371") == "dsmz:16371"

    def test_normalize_collection_curie_various_formats(self) -> None:
        """Test normalization of various input formats."""
        record = StrainRecord(source_sheet="test", source_row=1)

        # With colon separator
        assert record._normalize_collection_curie("ATCC:35073") == "atcc:35073"
        assert record._normalize_collection_curie("JCM:2831") == "jcm:2831"

        # With space separator (parses as prefix + local_id)
        assert record._normalize_collection_curie("DSM 16371") == "dsmz:16371"

        # With hyphen separator
        assert record._normalize_collection_curie("DSM-16371") == "dsmz:16371"

    def test_normalize_collection_curie_preserves_unknown(self) -> None:
        """Test that unknown prefixes are preserved (lowercased)."""
        record = StrainRecord(source_sheet="test", source_row=1)

        # LMG not in bioregistry but we map it
        assert record._normalize_collection_curie("LMG:2269") == "lmg:2269"

    def test_build_display_name(self) -> None:
        """Test display name construction."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            scientific_name="Methylobacterium aquaticum",
            strain_designation="GR16",
        )
        assert record._build_display_name() == "Methylobacterium aquaticum GR16"

        # Scientific name only
        record2 = StrainRecord(
            source_sheet="test",
            source_row=1,
            scientific_name="Methylobacterium aquaticum",
        )
        assert record2._build_display_name() == "Methylobacterium aquaticum"

        # Strain designation only
        record3 = StrainRecord(
            source_sheet="test",
            source_row=1,
            strain_designation="AM1",
        )
        assert record3._build_display_name() == "AM1"

        # Neither
        record4 = StrainRecord(source_sheet="test", source_row=1)
        assert record4._build_display_name() == "Unknown strain"

    def test_collect_xrefs_includes_culture_collections(self) -> None:
        """Test that xrefs include culture collection IDs."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            culture_collection_ids=["DSM:16371", "ATCC:35073"],
        )
        xrefs = record._collect_xrefs()
        assert "dsmz:16371" in xrefs
        assert "atcc:35073" in xrefs

    def test_collect_xrefs_includes_species_taxon(self) -> None:
        """Test that xrefs include species taxon when different from main."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            ncbi_taxon_id="12345",  # Strain-level taxon
            species_taxon_id="67890",  # Species-level taxon
        )
        xrefs = record._collect_xrefs()
        assert "NCBITaxon:67890" in xrefs

    def test_collect_xrefs_deduplicates(self) -> None:
        """Test that xrefs are deduplicated."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            xrefs=["NCBITaxon:67890"],
            species_taxon_id="67890",
        )
        xrefs = record._collect_xrefs()
        # Should only appear once
        assert xrefs.count("NCBITaxon:67890") == 1

    def test_synonyms_in_kgx_output(self) -> None:
        """Test that synonyms are included in KGX output."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            ncbi_taxon_id="12345",
            synonyms=["Old name", "Another name"],
        )
        node = record.to_kgx_node()
        assert node["synonyms"] == "Old name|Another name"


class TestGenerateQueryVariants:
    """Tests for generate_query_variants function."""

    def test_full_name_with_strain(self) -> None:
        """Test query generation with full name and strain."""
        queries = generate_query_variants(
            scientific_name="Methylobacterium aquaticum",
            strain_designation="GR16",
            culture_collection_ids=[],
        )
        assert "Methylobacterium aquaticum GR16" in queries
        assert "Methylobacterium aquaticum" in queries
        assert "GR16" in queries

    def test_with_culture_collection_ids(self) -> None:
        """Test query generation includes collection ID variants."""
        queries = generate_query_variants(
            scientific_name="Methylobacterium aquaticum",
            strain_designation=None,
            culture_collection_ids=["DSM:16371"],
        )
        assert "DSM 16371" in queries
        assert "DSM-16371" in queries
        assert "DSM16371" in queries
        assert "Methylobacterium aquaticum DSM 16371" in queries

    def test_deduplicates(self) -> None:
        """Test that duplicate queries are removed."""
        queries = generate_query_variants(
            scientific_name="Strain X",
            strain_designation="Strain X",  # Same as scientific name
            culture_collection_ids=[],
        )
        # Should only have each unique query once
        assert queries.count("Strain X") == 1

    def test_empty_inputs(self) -> None:
        """Test with no inputs."""
        queries = generate_query_variants(
            scientific_name=None,
            strain_designation=None,
            culture_collection_ids=[],
        )
        assert queries == []


class TestExtractBacdiveData:
    """Tests for extract_bacdive_data function."""

    def test_extract_basic_fields(self) -> None:
        """Test extraction of basic BacDive fields."""
        doc: dict[str, Any] = {
            "General": {
                "BacDive-ID": 7176,
                "NCBI tax id": {"NCBI tax id": 270351},
            },
            "Name and taxonomic classification": {
                "species": "Methylobacterium aquaticum",
                "strain designation": "GR16",
            },
        }
        result = extract_bacdive_data(doc)
        assert result["bacdive_id"] == 7176
        assert result["ncbi_taxon_id"] == 270351
        assert result["species"] == "Methylobacterium aquaticum"
        assert result["strain_designation"] == "GR16"

    def test_extract_culture_collections(self) -> None:
        """Test extraction of culture collection IDs (raw format)."""
        doc: dict[str, Any] = {
            "General": {"BacDive-ID": 7176},
            "Name and taxonomic classification": {},
            "External links": {
                "culture collection no.": "ATCC 35073, JCM 2831, NBRC 15690",
            },
        }
        result = extract_bacdive_data(doc)
        # Note: extract_bacdive_data returns raw IDs, not normalized CURIEs
        # Normalization happens later in enrich_strain_from_bacdive
        assert "ATCC 35073" in result["culture_collection_ids"]
        assert "JCM 2831" in result["culture_collection_ids"]
        assert "NBRC 15690" in result["culture_collection_ids"]

    def test_extract_lpsn_synonyms_array(self) -> None:
        """Test extraction of LPSN synonyms as array."""
        doc: dict[str, Any] = {
            "General": {"BacDive-ID": 7152},
            "Name and taxonomic classification": {
                "LPSN": {
                    "synonyms": [
                        {"synonym": "Methylobacterium radiora"},
                        {"synonym": "Pseudomonas radiora"},
                    ]
                }
            },
        }
        result = extract_bacdive_data(doc)
        assert "Methylobacterium radiora" in result["synonyms"]
        assert "Pseudomonas radiora" in result["synonyms"]

    def test_extract_lpsn_synonyms_single_object(self) -> None:
        """Test extraction of LPSN synonyms when it's a single object (not array)."""
        # BacDive schema allows synonyms to be either array or single object
        doc: dict[str, Any] = {
            "General": {"BacDive-ID": 97},
            "Name and taxonomic classification": {
                "LPSN": {"synonyms": {"@ref": 20215, "synonym": "Sapromyces laidlawi"}}
            },
        }
        result = extract_bacdive_data(doc)
        assert "Sapromyces laidlawi" in result["synonyms"]
        assert len(result["synonyms"]) == 1

    def test_extract_handles_missing_fields(self) -> None:
        """Test extraction handles missing fields gracefully."""
        doc: dict[str, Any] = {"General": {"BacDive-ID": 12345}}
        result = extract_bacdive_data(doc)
        assert result["bacdive_id"] == 12345
        assert result["ncbi_taxon_id"] is None
        assert result["species"] is None
        assert result["culture_collection_ids"] == []
        assert result["synonyms"] == []

    def test_extract_handles_nested_ncbi_id(self) -> None:
        """Test extraction handles nested NCBI tax id format."""
        # BacDive stores NCBI tax id as a nested dict
        doc: dict[str, Any] = {
            "General": {
                "BacDive-ID": 101,
                "NCBI tax id": {"NCBI tax id": 67890},
            },
        }
        result = extract_bacdive_data(doc)
        assert result["ncbi_taxon_id"] == 67890

    def test_extract_ignores_non_dict_ncbi_id(self) -> None:
        """Test extraction returns None when NCBI tax id is not a dict."""
        # Edge case: if NCBI tax id is not in expected format, return None
        doc: dict[str, Any] = {
            "General": {
                "BacDive-ID": 100,
                "NCBI tax id": 12345,  # Direct int, not expected format
            },
        }
        result = extract_bacdive_data(doc)
        # Current implementation only handles dict format
        assert result["ncbi_taxon_id"] is None


class TestCollectionPrefixMap:
    """Tests for COLLECTION_PREFIX_MAP constant."""

    def test_dsm_mappings(self) -> None:
        """Test DSM/DSMZ both map to dsmz."""
        assert COLLECTION_PREFIX_MAP["DSM"] == "dsmz"
        assert COLLECTION_PREFIX_MAP["DSMZ"] == "dsmz"

    def test_ifo_maps_to_nbrc(self) -> None:
        """Test IFO maps to NBRC (merged collections)."""
        assert COLLECTION_PREFIX_MAP["IFO"] == "nbrc"

    def test_major_collections_present(self) -> None:
        """Test major culture collections are mapped."""
        expected = ["DSM", "ATCC", "JCM", "NBRC", "LMG", "CIP"]
        for prefix in expected:
            assert prefix in COLLECTION_PREFIX_MAP


class TestIdPriorityRules:
    """Tests for ID priority rules in _determine_canonical_id."""

    def test_bacdive_highest_priority(self) -> None:
        """BacDive should be used when available, even with other IDs."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            ncbi_taxon_id="12345",
            species_taxon_id="12300",  # Different - makes NCBITaxon strain-specific
            bacdive_id="67890",
            primary_collection_id="DSM:16371",
        )
        node = record.to_kgx_node()
        assert node["id"] == "bacdive:67890"

    def test_ncbi_taxon_second_priority(self) -> None:
        """Strain-specific NCBITaxon should be used when no BacDive but collection available."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            ncbi_taxon_id="67890",
            species_taxon_id="67800",  # Different - makes it strain-specific
            primary_collection_id="DSM:16371",
        )
        node = record.to_kgx_node()
        assert node["id"] == "NCBITaxon:67890"

    def test_collection_third_priority(self) -> None:
        """Culture collection should be used as last resort."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            primary_collection_id="DSM:16371",
        )
        node = record.to_kgx_node()
        assert node["id"] == "dsmz:16371"

    def test_fallback_uses_strain_designation(self) -> None:
        """Fallback should use strain designation when nothing else available."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            strain_designation="AM1",
        )
        node = record.to_kgx_node()
        assert node["id"] == "cmm:strain-AM1"

    def test_fallback_handles_spaces_in_designation(self) -> None:
        """Fallback should replace spaces with hyphens."""
        record = StrainRecord(
            source_sheet="test",
            source_row=1,
            strain_designation="DSM 16371",
        )
        node = record.to_kgx_node()
        assert node["id"] == "cmm:strain-DSM-16371"


@pytest.mark.integration
class TestFetchNcbiSynonyms:
    """Tests for fetch_ncbi_synonyms function."""

    def test_returns_dict_structure(self) -> None:
        """Test that function returns expected dict structure."""
        # Use a real taxon ID for integration test
        result = fetch_ncbi_synonyms(31998)  # Methylobacterium radiotolerans

        assert isinstance(result, dict)
        assert "synonyms" in result
        assert "equivalent_names" in result
        assert "includes" in result
        assert "misspellings" in result
        assert "authority" in result
        assert "rank" in result

        # List fields should be lists
        assert isinstance(result["synonyms"], list)
        assert isinstance(result["equivalent_names"], list)
        assert isinstance(result["includes"], list)
        assert isinstance(result["misspellings"], list)
        assert isinstance(result["authority"], list)

        # Rank should be a string
        assert isinstance(result["rank"], str)

    def test_extracts_synonyms(self) -> None:
        """Test that synonyms are extracted from NCBI."""
        # Methylobacterium radiotolerans has known synonyms
        result = fetch_ncbi_synonyms(31998)

        # Should have at least one name variant (synonyms, equivalent_names, or authority)
        # NCBI API sometimes returns these in different fields
        # Skip test if NCBI API returns no data (rate limiting, network issues)
        total_names = (
            len(result["synonyms"])
            + len(result["equivalent_names"])
            + len(result["authority"])
            + len(result["includes"])
        )

        if total_names == 0:
            pytest.skip("NCBI API returned no name data (possible rate limiting or network issue)")

        # At least one of these should contain the known synonym
        all_names = (
            result["synonyms"]
            + result["equivalent_names"]
            + [name for name in result["authority"] if "radiora" in name.lower()]
        )
        assert any("Pseudomonas radiora" in name or "radiora" in name.lower() for name in all_names)

    def test_handles_invalid_taxon_id(self) -> None:
        """Test that invalid taxon IDs return empty results."""
        result = fetch_ncbi_synonyms(999999999)  # Non-existent ID

        # Should return empty lists, not raise exception
        assert result["synonyms"] == []
        assert result["equivalent_names"] == []

    def test_extracts_equivalent_names(self) -> None:
        """Test that equivalent names are extracted."""
        # Methylobacterium radiotolerans has an equivalent name
        result = fetch_ncbi_synonyms(31998)

        # May have equivalent names like "Methylobacterium radiitolerans"
        # Just check structure is correct (may be empty for some taxa)
        assert isinstance(result["equivalent_names"], list)
