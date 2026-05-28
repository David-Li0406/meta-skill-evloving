"""Strain record deduplication and merging.

This module provides functions to consolidate and deduplicate strain records
from multiple sources.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmm_ai_automation.strains.models import StrainRecord

logger = logging.getLogger(__name__)


def merge_records(target: StrainRecord, source: StrainRecord) -> None:
    """Merge source record into target, filling in missing fields.

    This function modifies the target record in place, adding any
    information from source that target is missing.

    Args:
        target: Record to merge into
        source: Record to merge from
    """
    if not target.name and source.name:
        target.name = source.name
    if not target.scientific_name and source.scientific_name:
        target.scientific_name = source.scientific_name
    if not target.strain_designation and source.strain_designation:
        target.strain_designation = source.strain_designation
    if not target.ncbi_taxon_id and source.ncbi_taxon_id:
        target.ncbi_taxon_id = source.ncbi_taxon_id
    if not target.species_taxon_id and source.species_taxon_id:
        target.species_taxon_id = source.species_taxon_id
    if not target.parent_taxon_id and source.parent_taxon_id:
        target.parent_taxon_id = source.parent_taxon_id
    if not target.bacdive_id and source.bacdive_id:
        target.bacdive_id = source.bacdive_id
    if not target.genome_accession and source.genome_accession:
        target.genome_accession = source.genome_accession
    if not target.has_taxonomic_rank and source.has_taxonomic_rank:
        target.has_taxonomic_rank = source.has_taxonomic_rank

    # Merge collection IDs
    for cc_id in source.culture_collection_ids:
        if cc_id not in target.culture_collection_ids:
            target.culture_collection_ids.append(cc_id)

    # Merge synonyms
    for syn in source.synonyms:
        if syn not in target.synonyms:
            target.synonyms.append(syn)

    # Merge xrefs
    for xref in source.xrefs:
        if xref not in target.xrefs:
            target.xrefs.append(xref)


def consolidate_strains(all_records: list[StrainRecord]) -> list[StrainRecord]:
    """Consolidate duplicate strain records.

    Merges records that appear to refer to the same strain based on:
    - Matching NCBITaxon IDs
    - Matching culture collection IDs
    - Matching names (case-insensitive)

    Uses both primary key lookup AND secondary name-based lookup to catch
    cases where one sheet has an ID and another has the same entity by name only.

    Args:
        all_records: List of strain records from all sources

    Returns:
        Deduplicated list of consolidated records
    """
    consolidated: dict[str, StrainRecord] = {}
    # Secondary index: name -> primary key (to find records by name even when they have IDs)
    name_to_key: dict[str, str] = {}

    for record in all_records:
        # Generate primary key for deduplication
        primary_key = None
        if record.ncbi_taxon_id:
            primary_key = f"ncbi:{record.ncbi_taxon_id}"
        elif record.primary_collection_id:
            primary_key = f"cc:{record.primary_collection_id}"
        elif record.name:
            primary_key = f"name:{record.name.lower()}"
        else:
            primary_key = f"row:{record.source_sheet}:{record.source_row}"

        # Also check if we can find this record by name (secondary lookup)
        name_key = record.name.lower() if record.name else None
        existing_key = None

        # First try primary key match
        if primary_key in consolidated:
            existing_key = primary_key
        # Then try secondary name lookup (catches mismatched ID vs name-only records)
        elif name_key and name_key in name_to_key:
            existing_key = name_to_key[name_key]
            logger.debug(f"Found by name lookup: '{record.name}' matches existing record with key {existing_key}")

        if existing_key:
            # Merge into existing record
            existing = consolidated[existing_key]
            merge_records(existing, record)

            # Check if incoming record's name points to a DIFFERENT record
            # (e.g., strains.tsv created record by name, taxa_and_genomes.tsv has same name + ncbi_id
            # pointing to different record - need to merge both)
            if name_key and name_key in name_to_key and name_to_key[name_key] != existing_key:
                other_key = name_to_key[name_key]
                if other_key in consolidated:
                    other_record = consolidated[other_key]
                    logger.debug(f"Cross-merge: '{record.name}' links {other_key} to {existing_key}")
                    merge_records(existing, other_record)
                    del consolidated[other_key]
                    # Update name index to point to surviving record
                    name_to_key[name_key] = existing_key

            # Register incoming record's name in name index
            if name_key and name_key not in name_to_key:
                name_to_key[name_key] = existing_key
        else:
            consolidated[primary_key] = record
            # Register in name index
            if name_key:
                name_to_key[name_key] = primary_key

    result = list(consolidated.values())
    logger.info(f"Consolidated {len(all_records)} records into {len(result)} unique strains")
    return result


def deduplicate_by_canonical_id(records: list[StrainRecord]) -> list[StrainRecord]:
    """Deduplicate records by their canonical ID after enrichment.

    This runs after BacDive/NCBI enrichment when records may have acquired
    new identifiers that reveal they are the same entity.

    Args:
        records: List of enriched strain records

    Returns:
        Deduplicated list with merged records
    """
    # Group by canonical ID
    by_canonical: dict[str, list[StrainRecord]] = {}

    for record in records:
        # Compute canonical ID using the same logic as to_kgx_node
        canonical_id = record._determine_canonical_id()
        if canonical_id not in by_canonical:
            by_canonical[canonical_id] = []
        by_canonical[canonical_id].append(record)

    # Merge duplicates
    deduplicated: list[StrainRecord] = []
    merged_count = 0

    for _canonical_id, group in by_canonical.items():
        if len(group) == 1:
            deduplicated.append(group[0])
        else:
            # Merge all records in the group into the first one
            target = group[0]
            for source in group[1:]:
                merge_records(target, source)
                merged_count += 1
            deduplicated.append(target)

    if merged_count > 0:
        logger.info(f"Post-enrichment deduplication merged {merged_count} records")

    return deduplicated
