"""Tests for strains parsing functions."""

import csv
from pathlib import Path
from typing import Any

import pytest

from cmm_ai_automation.strains.parsing import (
    parse_growth_preferences_tsv,
    parse_strains_tsv,
    parse_taxa_and_genomes_tsv,
)


class TestParseStrainsTSV:
    """Tests for parse_strains_tsv()."""

    @pytest.fixture
    def tmp_strains_file(self, tmp_path: Path) -> Path:
        """Create a temporary strains.tsv file."""
        file_path = tmp_path / "strains.tsv"
        return file_path

    def write_strains_tsv(self, path: Path, rows: list[dict[str, Any]]) -> None:
        """Helper to write strains.tsv data."""
        fieldnames = [
            "strain_id",
            "culture_collection_ids",
            "scientific_name",
            "strain_designation",
            "species_taxon_id",
            "Name synonyms",
        ]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)

    def test_parse_empty_file(self, tmp_strains_file: Path) -> None:
        """Test parsing empty TSV file."""
        self.write_strains_tsv(tmp_strains_file, [])
        records = parse_strains_tsv(tmp_strains_file)
        assert records == []

    def test_parse_nonexistent_file(self, tmp_path: Path) -> None:
        """Test parsing non-existent file."""
        fake_path = tmp_path / "nonexistent.tsv"
        records = parse_strains_tsv(fake_path)
        assert records == []

    def test_parse_single_strain(self, tmp_strains_file: Path) -> None:
        """Test parsing single strain record."""
        rows = [
            {
                "strain_id": "DSM:16371",
                "culture_collection_ids": "",
                "scientific_name": "Methylobacterium extorquens",
                "strain_designation": "AM1",
                "species_taxon_id": "NCBITaxon:408",
                "Name synonyms": "",
            }
        ]
        self.write_strains_tsv(tmp_strains_file, rows)
        records = parse_strains_tsv(tmp_strains_file)

        assert len(records) == 1
        record = records[0]
        assert record.source_sheet == "strains.tsv"
        assert record.source_row == 2  # CSV row 2 (after header)
        assert record.scientific_name == "Methylobacterium extorquens"
        assert record.strain_designation == "AM1"
        assert record.species_taxon_id == "NCBITaxon:408"
        assert record.primary_collection_id == "DSM:16371"
        assert "DSM:16371" in record.culture_collection_ids
        assert record.name == "Methylobacterium extorquens AM1"

    def test_parse_strain_with_synonyms(self, tmp_strains_file: Path) -> None:
        """Test parsing strain with synonyms."""
        rows = [
            {
                "strain_id": "ATCC:700829",
                "culture_collection_ids": "",
                "scientific_name": "Pseudomonas putida",
                "strain_designation": "KT2440",
                "species_taxon_id": "NCBITaxon:303",
                "Name synonyms": "P. putida KT2440; ATCC 700829",
            }
        ]
        self.write_strains_tsv(tmp_strains_file, rows)
        records = parse_strains_tsv(tmp_strains_file)

        assert len(records) == 1
        assert len(records[0].synonyms) == 2
        assert "P. putida KT2440" in records[0].synonyms
        assert "ATCC 700829" in records[0].synonyms

    def test_parse_strain_with_additional_ids(self, tmp_strains_file: Path) -> None:
        """Test parsing strain with additional culture collection IDs."""
        rows = [
            {
                "strain_id": "DSM:16371",
                "culture_collection_ids": "ATCC:700829; JCM:12345",
                "scientific_name": "Test bacterium",
                "strain_designation": "TEST1",
                "species_taxon_id": "NCBITaxon:1",
                "Name synonyms": "",
            }
        ]
        self.write_strains_tsv(tmp_strains_file, rows)
        records = parse_strains_tsv(tmp_strains_file)

        assert len(records) == 1
        assert len(records[0].culture_collection_ids) == 3
        assert "DSM:16371" in records[0].culture_collection_ids
        assert "ATCC:700829" in records[0].culture_collection_ids
        assert "JCM:12345" in records[0].culture_collection_ids

    def test_parse_strain_without_designation(self, tmp_strains_file: Path) -> None:
        """Test parsing strain without designation."""
        rows = [
            {
                "strain_id": "",
                "culture_collection_ids": "",
                "scientific_name": "Escherichia coli",
                "strain_designation": "",
                "species_taxon_id": "NCBITaxon:562",
                "Name synonyms": "",
            }
        ]
        self.write_strains_tsv(tmp_strains_file, rows)
        records = parse_strains_tsv(tmp_strains_file)

        assert len(records) == 1
        assert records[0].name == "Escherichia coli"
        assert records[0].strain_designation is None

    def test_parse_multiple_strains(self, tmp_strains_file: Path) -> None:
        """Test parsing multiple strain records."""
        rows = [
            {
                "strain_id": "DSM:1",
                "culture_collection_ids": "",
                "scientific_name": "Bacterium one",
                "strain_designation": "A",
                "species_taxon_id": "NCBITaxon:1",
                "Name synonyms": "",
            },
            {
                "strain_id": "DSM:2",
                "culture_collection_ids": "",
                "scientific_name": "Bacterium two",
                "strain_designation": "B",
                "species_taxon_id": "NCBITaxon:2",
                "Name synonyms": "",
            },
            {
                "strain_id": "DSM:3",
                "culture_collection_ids": "",
                "scientific_name": "Bacterium three",
                "strain_designation": "C",
                "species_taxon_id": "NCBITaxon:3",
                "Name synonyms": "",
            },
        ]
        self.write_strains_tsv(tmp_strains_file, rows)
        records = parse_strains_tsv(tmp_strains_file)

        assert len(records) == 3
        assert records[0].strain_designation == "A"
        assert records[1].strain_designation == "B"
        assert records[2].strain_designation == "C"


class TestParseTaxaAndGenomesTSV:
    """Tests for parse_taxa_and_genomes_tsv()."""

    @pytest.fixture
    def tmp_taxa_file(self, tmp_path: Path) -> Path:
        """Create a temporary taxa_and_genomes.tsv file."""
        file_path = tmp_path / "taxa_and_genomes.tsv"
        return file_path

    def write_taxa_tsv(self, path: Path, rows: list[dict[str, Any]]) -> None:
        """Helper to write taxa_and_genomes.tsv data."""
        fieldnames = [
            "NCBITaxon id",
            "Strain name",
            "Genome identifier (GenBank, IMG etc)",
        ]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)

    def test_parse_empty_file(self, tmp_taxa_file: Path) -> None:
        """Test parsing empty taxa file."""
        self.write_taxa_tsv(tmp_taxa_file, [])
        records = parse_taxa_and_genomes_tsv(tmp_taxa_file)
        assert records == []

    def test_parse_nonexistent_file(self, tmp_path: Path) -> None:
        """Test parsing non-existent file."""
        fake_path = tmp_path / "nonexistent.tsv"
        records = parse_taxa_and_genomes_tsv(fake_path)
        assert records == []

    def test_parse_single_record(self, tmp_taxa_file: Path) -> None:
        """Test parsing single taxa/genome record."""
        rows = [
            {
                "NCBITaxon id": "NCBITaxon:408",
                "Strain name": "Methylobacterium extorquens AM1",
                "Genome identifier (GenBank, IMG etc)": "GCA_000022685.1",
            }
        ]
        self.write_taxa_tsv(tmp_taxa_file, rows)
        records = parse_taxa_and_genomes_tsv(tmp_taxa_file)

        assert len(records) == 1
        record = records[0]
        assert record.source_sheet == "taxa_and_genomes.tsv"
        assert record.ncbi_taxon_id == "NCBITaxon:408"
        assert record.name == "Methylobacterium extorquens AM1"
        assert record.genome_accession == "GCA_000022685.1"

    def test_parse_without_genome(self, tmp_taxa_file: Path) -> None:
        """Test parsing record without genome accession."""
        rows = [
            {
                "NCBITaxon id": "NCBITaxon:562",
                "Strain name": "Escherichia coli",
                "Genome identifier (GenBank, IMG etc)": "",
            }
        ]
        self.write_taxa_tsv(tmp_taxa_file, rows)
        records = parse_taxa_and_genomes_tsv(tmp_taxa_file)

        assert len(records) == 1
        assert records[0].genome_accession is None

    def test_parse_multiple_records(self, tmp_taxa_file: Path) -> None:
        """Test parsing multiple taxa records."""
        rows = [
            {
                "NCBITaxon id": "NCBITaxon:1",
                "Strain name": "Strain A",
                "Genome identifier (GenBank, IMG etc)": "GCA_000000001.1",
            },
            {
                "NCBITaxon id": "NCBITaxon:2",
                "Strain name": "Strain B",
                "Genome identifier (GenBank, IMG etc)": "GCA_000000002.1",
            },
        ]
        self.write_taxa_tsv(tmp_taxa_file, rows)
        records = parse_taxa_and_genomes_tsv(tmp_taxa_file)

        assert len(records) == 2
        assert records[0].ncbi_taxon_id == "NCBITaxon:1"
        assert records[1].ncbi_taxon_id == "NCBITaxon:2"


class TestParseGrowthPreferencesTSV:
    """Tests for parse_growth_preferences_tsv()."""

    @pytest.fixture
    def tmp_prefs_file(self, tmp_path: Path) -> Path:
        """Create a temporary growth_preferences.tsv file."""
        file_path = tmp_path / "growth_preferences.tsv"
        return file_path

    def write_prefs_tsv(self, path: Path, rows: list[dict[str, Any]]) -> None:
        """Helper to write growth_preferences.tsv data."""
        fieldnames = [
            "strain id",
            "Growth Media",
            "growth_temp_min",
            "growth_temp_max",
            "growth_ph_min",
            "growth_ph_max",
        ]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)

    def test_parse_empty_file(self, tmp_prefs_file: Path) -> None:
        """Test parsing empty preferences file."""
        self.write_prefs_tsv(tmp_prefs_file, [])
        records = parse_growth_preferences_tsv(tmp_prefs_file)
        assert records == []

    def test_parse_nonexistent_file(self, tmp_path: Path) -> None:
        """Test parsing non-existent file."""
        fake_path = tmp_path / "nonexistent.tsv"
        records = parse_growth_preferences_tsv(fake_path)
        assert records == []

    def test_parse_single_record(self, tmp_prefs_file: Path) -> None:
        """Test parsing single growth preference record."""
        rows = [
            {
                "strain id": "DSM:16371",
                "Growth Media": "Methylobacterium medium",
                "growth_temp_min": "25",
                "growth_temp_max": "37",
                "growth_ph_min": "6.5",
                "growth_ph_max": "8.0",
            }
        ]
        self.write_prefs_tsv(tmp_prefs_file, rows)
        records = parse_growth_preferences_tsv(tmp_prefs_file)

        assert len(records) == 1
        record = records[0]
        assert record.source_sheet == "growth_preferences.tsv"
        assert record.primary_collection_id == "DSM:16371"

    def test_parse_multiple_records(self, tmp_prefs_file: Path) -> None:
        """Test parsing multiple growth preference records."""
        rows = [
            {
                "strain id": "DSM:1",
                "Growth Media": "Medium 1",
                "growth_temp_min": "20",
                "growth_temp_max": "30",
                "growth_ph_min": "6.0",
                "growth_ph_max": "7.0",
            },
            {
                "strain id": "DSM:2",
                "Growth Media": "Medium 2",
                "growth_temp_min": "15",
                "growth_temp_max": "25",
                "growth_ph_min": "5.5",
                "growth_ph_max": "6.5",
            },
        ]
        self.write_prefs_tsv(tmp_prefs_file, rows)
        records = parse_growth_preferences_tsv(tmp_prefs_file)

        assert len(records) == 2
        assert records[0].primary_collection_id == "DSM:1"
        assert records[1].primary_collection_id == "DSM:2"
