"""TSV parsing functions for strain data.

This module provides functions to parse strain data from various TSV files.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path  # noqa: TC003 - Path is used at runtime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmm_ai_automation.strains.models import StrainRecord

logger = logging.getLogger(__name__)


def parse_strains_tsv(path: Path) -> list[StrainRecord]:
    """Parse strains.tsv and return StrainRecord list.

    Expected columns:
    - strain_id: Primary culture collection ID
    - culture_collection_ids: Additional semicolon-separated IDs
    - scientific_name: Binomial name
    - strain_designation: Strain designation
    - species_taxon_id: Species-level NCBI taxon ID
    - Name synonyms: Semicolon-separated synonyms

    Args:
        path: Path to strains.tsv file

    Returns:
        List of StrainRecord objects
    """
    # Import here to avoid circular imports
    from cmm_ai_automation.strains.models import StrainRecord

    records: list[StrainRecord] = []
    if not path.exists():
        logger.warning(f"File not found: {path}")
        return records

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row_num, row in enumerate(reader, start=2):
            # Parse culture collection IDs from both columns
            cc_ids = []
            primary_id = row.get("strain_id", "").strip()
            if primary_id:
                cc_ids.append(primary_id)

            # Additional IDs from culture_collection_ids column
            additional = row.get("culture_collection_ids", "")
            if additional:
                for part in additional.split(";"):
                    part = part.strip()
                    if part and part not in cc_ids:
                        cc_ids.append(part)

            record = StrainRecord(
                source_sheet="strains.tsv",
                source_row=row_num,
                scientific_name=row.get("scientific_name", "").strip() or None,
                strain_designation=row.get("strain_designation", "").strip() or None,
                species_taxon_id=row.get("species_taxon_id", "").strip() or None,
                culture_collection_ids=cc_ids,
                primary_collection_id=primary_id or None,
                synonyms=[s.strip() for s in row.get("Name synonyms", "").split(";") if s.strip()],
            )

            # Build name from scientific_name + strain_designation
            if record.scientific_name:
                if record.strain_designation:
                    record.name = f"{record.scientific_name} {record.strain_designation}"
                else:
                    record.name = record.scientific_name

            records.append(record)

    logger.info(f"Parsed {len(records)} records from strains.tsv")
    return records


def parse_taxa_and_genomes_tsv(path: Path) -> list[StrainRecord]:
    """Parse taxa_and_genomes.tsv and return StrainRecord list.

    Expected columns:
    - Strain name: Full strain name (may include designation)
    - NCBITaxon id: NCBI Taxonomy ID
    - Genome identifier (GenBank, IMG etc): Genome accession

    Args:
        path: Path to taxa_and_genomes.tsv file

    Returns:
        List of StrainRecord objects
    """
    from cmm_ai_automation.strains.models import StrainRecord

    records: list[StrainRecord] = []
    if not path.exists():
        logger.warning(f"File not found: {path}")
        return records

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row_num, row in enumerate(reader, start=2):
            strain_name = row.get("Strain name", "").strip()
            ncbi_taxon = row.get("NCBITaxon id", "").strip()
            genome_id = row.get("Genome identifier (GenBank, IMG etc)", "").strip()

            if not strain_name and not ncbi_taxon:
                continue

            # Parse strain name to extract scientific name and designation
            scientific_name = None
            strain_designation = None
            if strain_name:
                # Try to split "Genus species strain_designation"
                parts = strain_name.split()
                if len(parts) >= 2:
                    scientific_name = " ".join(parts[:2])  # Genus species
                    if len(parts) > 2:
                        strain_designation = " ".join(parts[2:])

            record = StrainRecord(
                source_sheet="taxa_and_genomes.tsv",
                source_row=row_num,
                name=strain_name or None,
                scientific_name=scientific_name,
                strain_designation=strain_designation,
                ncbi_taxon_id=ncbi_taxon or None,
                genome_accession=genome_id or None,
            )

            records.append(record)

    logger.info(f"Parsed {len(records)} records from taxa_and_genomes.tsv")
    return records


def parse_growth_preferences_tsv(path: Path) -> list[StrainRecord]:
    """Parse growth_preferences.tsv for additional strain references.

    Expected columns:
    - strain id: Strain identifier (may be culture collection ID)
    - scientific name with strain id: Full strain name

    Args:
        path: Path to growth_preferences.tsv file

    Returns:
        List of StrainRecord objects (deduplicated within file)
    """
    from cmm_ai_automation.strains.models import StrainRecord

    records: list[StrainRecord] = []
    if not path.exists():
        logger.warning(f"File not found: {path}")
        return records

    seen_strains: set[str] = set()

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row_num, row in enumerate(reader, start=2):
            strain_id = row.get("strain id", "").strip()
            full_name = row.get("scientific name with strain id", "").strip()

            # Skip empty or duplicate
            key = strain_id or full_name
            if not key or key in seen_strains:
                continue
            seen_strains.add(key)

            # Parse the full name
            scientific_name = None
            strain_designation = None
            cc_ids: list[str] = []

            if strain_id:
                # Could be "DSM:1337" or "KT2440"
                if ":" in strain_id:
                    cc_ids.append(strain_id)
                else:
                    strain_designation = strain_id

            if full_name:
                parts = full_name.split()
                if len(parts) >= 2:
                    scientific_name = " ".join(parts[:2])
                    if len(parts) > 2:
                        strain_designation = " ".join(parts[2:])

            record = StrainRecord(
                source_sheet="growth_preferences.tsv",
                source_row=row_num,
                name=full_name or None,
                scientific_name=scientific_name,
                strain_designation=strain_designation,
                culture_collection_ids=cc_ids,
                primary_collection_id=cc_ids[0] if cc_ids else None,
            )

            records.append(record)

    logger.info(f"Parsed {len(records)} unique strains from growth_preferences.tsv")
    return records


def parse_all_strain_sources(
    strains_path: Path,
    taxa_genomes_path: Path,
    growth_prefs_path: Path,
) -> list[StrainRecord]:
    """Parse all strain source files and return combined list.

    This is a convenience function that parses all three standard
    strain source files.

    Args:
        strains_path: Path to strains.tsv
        taxa_genomes_path: Path to taxa_and_genomes.tsv
        growth_prefs_path: Path to growth_preferences.tsv

    Returns:
        Combined list of StrainRecord objects from all sources
    """
    all_records: list[StrainRecord] = []

    # Parse each source
    all_records.extend(parse_strains_tsv(strains_path))
    all_records.extend(parse_taxa_and_genomes_tsv(taxa_genomes_path))
    all_records.extend(parse_growth_preferences_tsv(growth_prefs_path))

    logger.info(f"Parsed {len(all_records)} total records from all sources")
    return all_records
