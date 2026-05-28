"""Sheet validation schemas.

Maps sheet columns to their validators and validation options.
"""

from __future__ import annotations

from typing import Any

# Schema format:
# {
#     "sheet_name.tsv": {
#         "column_name": ("validator_name", {options}),
#         ...
#     }
# }
#
# Validator names correspond to registered validators in the engine.
# Options are passed to the validator constructor.

SHEET_SCHEMAS: dict[str, dict[str, tuple[str, dict[str, Any]]]] = {
    "strains.tsv": {
        # Primary species-level taxon ID
        "species_taxon_id": (
            "ncbi_taxon",
            {"check_rank": "species"},
        ),
        # Cross-references to kg-microbe nodes (semicolon-separated NCBITaxon IDs)
        "kg_microbe_nodes": (
            "ncbi_taxon_list",
            {"species_field": "species_taxon_id"},
        ),
        # Culture collection IDs (semicolon-separated)
        # TODO: Add culture_collection_list validator
        # "culture_collection_ids": (
        #     "culture_collection_list",
        #     {},
        # ),
        # Scientific name - cross-check against species_taxon_id
        # TODO: Add scientific_name validator
        # "scientific_name": (
        #     "scientific_name",
        #     {"taxon_field": "species_taxon_id"},
        # ),
        # Primary strain ID
        # TODO: Add culture_collection validator
        # "strain_id": (
        #     "culture_collection",
        #     {},
        # ),
    },
    "taxa_and_genomes.tsv": {
        # NCBITaxon ID (may be strain or species level)
        "NCBITaxon id": (
            "ncbi_taxon",
            {},
        ),
        # Genome accession
        # TODO: Add genome_accession validator
        # "Genome identifier (GenBank, IMG etc)": (
        #     "genome_accession",
        #     {},
        # ),
        # Strain name - cross-check against NCBITaxon id
        # TODO: Add scientific_name validator
        # "Strain name": (
        #     "scientific_name",
        #     {"taxon_field": "NCBITaxon id"},
        # ),
    },
    "growth_preferences.tsv": {
        # Strain ID - may be culture collection ID or designation
        # TODO: Add culture_collection validator
        # "strain id": (
        #     "culture_collection",
        #     {"allow_designation": True},
        # ),
        # Growth media reference
        # TODO: Add growth_medium validator
        # "Growth Media": (
        #     "growth_medium",
        #     {},
        # ),
    },
}


def get_schema_for_sheet(sheet_name: str) -> dict[str, tuple[str, dict[str, Any]]]:
    """Get validation schema for a sheet.

    Args:
        sheet_name: Name of the sheet (e.g., "strains.tsv")

    Returns:
        Dict mapping column names to (validator_name, options) tuples.
        Returns empty dict if no schema defined.
    """
    return SHEET_SCHEMAS.get(sheet_name, {})


def list_validated_sheets() -> list[str]:
    """List all sheets with defined validation schemas."""
    return list(SHEET_SCHEMAS.keys())


def list_validated_columns(sheet_name: str) -> list[str]:
    """List all columns with validators for a sheet."""
    schema = get_schema_for_sheet(sheet_name)
    return list(schema.keys())
