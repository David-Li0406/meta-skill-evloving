"""Taxonomic rank inference for strain records.

This module provides functions to infer taxonomic rank when authoritative
NCBI rank data is not available.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmm_ai_automation.strains.models import StrainRecord

logger = logging.getLogger(__name__)


def infer_species_from_bacdive(records: list[StrainRecord]) -> int:
    """Use BacDive NCBI taxon ID as species_taxon_id for strains.

    BacDive typically provides species-level NCBI taxon IDs for strains.
    If a record has a bacdive_id but no species_taxon_id, and is at strain rank,
    use its ncbi_taxon_id as the species_taxon_id (since it came from BacDive).

    Args:
        records: List of strain records to update

    Returns:
        Number of records whose species_taxon_id was set from BacDive
    """
    inferred = 0
    for record in records:
        if (
            record.bacdive_id
            and record.ncbi_taxon_id
            and not record.species_taxon_id
            and record.has_taxonomic_rank == "strain"
        ):
            # BacDive NCBI taxon IDs are typically species-level
            record.species_taxon_id = record.ncbi_taxon_id.replace("NCBITaxon:", "")
            inferred += 1
    return inferred


def infer_species_from_self(records: list[StrainRecord]) -> int:
    """Infer species_taxon_id for species-level records.

    If a record is at species level (rank == 'species') and has an NCBI taxon ID
    but no species_taxon_id, use its own taxon ID as the species_taxon_id.

    This handles cases where NCBI LineageEx doesn't include the species
    when the taxon itself IS the species.

    Args:
        records: List of strain records to update

    Returns:
        Number of records whose species_taxon_id was set
    """
    inferred = 0
    for record in records:
        if record.ncbi_taxon_id and not record.species_taxon_id and record.has_taxonomic_rank == "species":
            record.species_taxon_id = record.ncbi_taxon_id.replace("NCBITaxon:", "")
            inferred += 1
    return inferred


def infer_taxonomic_rank(records: list[StrainRecord]) -> int:
    """Infer taxonomic rank for records that don't have NCBI rank data.

    NCBI's rank is the authoritative source. We only infer a rank when:
    - The record has no has_taxonomic_rank (no NCBI data)
    - We have evidence it's a strain (strain_designation or bacdive_id)

    If NCBI says it's a species, we trust that even if we have strain_designation.
    The strain_designation in that case refers to a type strain of the species,
    not a separate strain-level taxon.

    Args:
        records: List of strain records to update

    Returns:
        Number of records whose rank was inferred
    """
    inferred = 0
    for record in records:
        # Only infer rank if we don't already have one from NCBI
        if not record.has_taxonomic_rank:
            # Evidence that this is a strain, not just a species
            is_strain = bool(record.strain_designation) or bool(record.bacdive_id)

            if is_strain:
                record.has_taxonomic_rank = "strain"
                logger.debug(
                    f"Inferred rank for {record.name}: strain "
                    f"(has {'strain_designation' if record.strain_designation else 'bacdive_id'})"
                )
            else:
                # Default to species if no strain evidence
                record.has_taxonomic_rank = "species"
                logger.debug(f"Inferred rank for {record.name}: species (no strain evidence)")
            inferred += 1

    return inferred


def run_inference_pipeline(records: list[StrainRecord]) -> dict[str, int]:
    """Run all inference steps on strain records.

    This is a convenience function that runs all inference steps in order
    and returns counts of what was inferred.

    Args:
        records: List of strain records to update

    Returns:
        Dict with counts for each inference type
    """
    counts = {
        "taxonomic_rank": infer_taxonomic_rank(records),
        "species_from_bacdive": infer_species_from_bacdive(records),
        "species_from_self": infer_species_from_self(records),
    }

    total = sum(counts.values())
    if total > 0:
        logger.info(f"Inference complete: {total} total inferences")
        for key, count in counts.items():
            if count > 0:
                logger.info(f"  - {key}: {count}")

    return counts
