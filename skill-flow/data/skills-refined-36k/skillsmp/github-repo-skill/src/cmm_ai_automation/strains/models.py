"""Domain models for strain data.

This module defines the core data structures used throughout the strain processing pipeline.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import bioregistry

# Biolink category for strains
BIOLINK_CATEGORY = "biolink:OrganismTaxon"

# NCBI rank string -> TAXRANK CURIE mapping
# See: http://purl.obolibrary.org/obo/taxrank.owl
RANK_TO_TAXRANK: dict[str, str] = {
    "domain": "TAXRANK:0000037",
    "superkingdom": "TAXRANK:0000037",  # NCBI uses superkingdom, maps to domain
    "phylum": "TAXRANK:0000003",
    "class": "TAXRANK:0000002",
    "order": "TAXRANK:0000017",
    "family": "TAXRANK:0000004",
    "genus": "TAXRANK:0000005",
    "species": "TAXRANK:0000006",
    "subspecies": "TAXRANK:0000023",
    "strain": "TAXRANK:0000060",
    # "no rank" has no direct TAXRANK equivalent - leave as empty string
}

# TAXRANK CURIE -> label mapping (for creating TaxonomicRank nodes)
TAXRANK_LABELS: dict[str, str] = {
    "TAXRANK:0000037": "domain",
    "TAXRANK:0000003": "phylum",
    "TAXRANK:0000002": "class",
    "TAXRANK:0000017": "order",
    "TAXRANK:0000004": "family",
    "TAXRANK:0000005": "genus",
    "TAXRANK:0000006": "species",
    "TAXRANK:0000023": "subspecies",
    "TAXRANK:0000060": "strain",
}

# Culture collection prefix mappings (input format -> bioregistry canonical)
COLLECTION_PREFIX_MAP = {
    "DSM": "dsmz",
    "DSMZ": "dsmz",
    "ATCC": "atcc",
    "JCM": "jcm",
    "NBRC": "nbrc",
    "NCIMB": "ncimb",  # Not in bioregistry but we'll use it
    "LMG": "lmg",  # Not in bioregistry
    "CIP": "cip",  # Not in bioregistry
    "CCM": "ccm",
    "CECT": "cect",
    "IAM": "iam",
    "IFO": "nbrc",  # IFO was merged into NBRC
    "CCUG": "ccug",
    "VKM": "vkm",
    "BCRC": "bcrc",
    "IMET": "imet",
}


@dataclass
class StrainRecord:
    """Consolidated strain record from multiple sources.

    This is the core domain model for strain data processing. It represents
    a single strain with all its identifying information from various sources.

    Attributes:
        source_sheet: Name of the source sheet
        source_row: Row number in the source sheet
        id: Canonical ID (NCBITaxon, bacdive, or collection)
        name: Full name with strain designation
        scientific_name: Binomial (genus species)
        strain_designation: e.g., AM1, KT2440, DSM 16371
        ncbi_taxon_id: NCBITaxon ID (species or strain level)
        species_taxon_id: Species-level NCBITaxon
        parent_taxon_id: Immediate parent in taxonomy
        culture_collection_ids: List of culture collection IDs
        primary_collection_id: e.g., DSM:16371
        bacdive_id: BacDive identifier
        genome_accession: GCA_* accession
        has_taxonomic_rank: e.g., species, strain, subspecies, no rank
        synonyms: List of synonyms
        xrefs: List of cross-references
    """

    # Source tracking
    source_sheet: str
    source_row: int

    # Identity
    id: str | None = None  # Canonical ID (NCBITaxon, bacdive, or collection)
    name: str | None = None  # Full name with strain designation
    scientific_name: str | None = None  # Binomial (genus species)
    strain_designation: str | None = None  # e.g., AM1, KT2440, DSM 16371

    # Taxonomic IDs
    ncbi_taxon_id: str | None = None  # NCBITaxon ID (species or strain level)
    species_taxon_id: str | None = None  # Species-level NCBITaxon
    parent_taxon_id: str | None = None  # Immediate parent in taxonomy

    # Culture collection IDs
    culture_collection_ids: list[str] = field(default_factory=list)
    primary_collection_id: str | None = None  # e.g., DSM:16371

    # BacDive
    bacdive_id: str | None = None

    # Genome
    genome_accession: str | None = None  # GCA_* accession

    # Taxonomic rank (Biolink-aligned)
    has_taxonomic_rank: str | None = None  # e.g., species, strain, subspecies, no rank

    # Additional
    synonyms: list[str] = field(default_factory=list)
    xrefs: list[str] = field(default_factory=list)

    def to_kgx_node(self) -> dict[str, str]:
        """Convert to KGX node row.

        Returns:
            Dictionary suitable for writing to KGX TSV format
        """
        # Determine canonical ID
        canonical_id = self._determine_canonical_id()

        # Build name
        display_name = self.name or self._build_display_name()

        # Build xrefs list
        all_xrefs = self._collect_xrefs()

        return {
            "id": canonical_id,
            "category": BIOLINK_CATEGORY,
            "name": display_name,
            "ncbi_taxon_id": self.ncbi_taxon_id or "",
            "species_taxon_id": self.species_taxon_id or "",
            "parent_taxon_id": self.parent_taxon_id or "",
            "has_taxonomic_rank": RANK_TO_TAXRANK.get(self.has_taxonomic_rank or "", ""),
            "strain_designation": self.strain_designation or "",
            "bacdive_id": f"bacdive:{self.bacdive_id}" if self.bacdive_id else "",
            "genome_accession": self.genome_accession or "",
            "xrefs": "|".join(all_xrefs) if all_xrefs else "",
            "synonyms": "|".join(self.synonyms) if self.synonyms else "",
            "source_sheet": self.source_sheet,
        }

    def _determine_canonical_id(self) -> str:
        """Determine canonical ID following priority rules.

        Priority:
        1. BacDive (always preferred when available)
        2. NCBITaxon (strain-level only, not species-level)
        3. Culture collection (prefer DSM)
        4. Generated from available info
        """
        # Priority 1: BacDive
        if self.bacdive_id:
            return f"bacdive:{self.bacdive_id}"

        # Priority 2: NCBITaxon (strain-level only)
        # Only use if ncbi_taxon_id differs from species_taxon_id (i.e., strain-specific)
        if self.ncbi_taxon_id and self.species_taxon_id and self.ncbi_taxon_id != self.species_taxon_id:
            taxon_id = self.ncbi_taxon_id
            if not taxon_id.startswith("NCBITaxon:"):
                taxon_id = f"NCBITaxon:{taxon_id}"
            return taxon_id

        # Priority 3: Culture collection (prefer DSM)
        if self.primary_collection_id:
            return self._normalize_collection_curie(self.primary_collection_id)

        # Fallback: generate from available info
        if self.strain_designation:
            return f"cmm:strain-{self.strain_designation.replace(' ', '-')}"

        return f"cmm:strain-unknown-{self.source_sheet}-{self.source_row}"

    def _build_display_name(self) -> str:
        """Build display name from components."""
        parts = []
        if self.scientific_name:
            parts.append(self.scientific_name)
        if self.strain_designation:
            parts.append(self.strain_designation)
        return " ".join(parts) if parts else "Unknown strain"

    def _collect_xrefs(self) -> list[str]:
        """Collect all cross-references."""
        xrefs = list(self.xrefs)

        # Add culture collection IDs as xrefs
        for cc_id in self.culture_collection_ids:
            curie = self._normalize_collection_curie(cc_id)
            if curie and curie not in xrefs:
                xrefs.append(curie)

        # Add species taxon if different from main taxon
        if self.species_taxon_id and self.species_taxon_id != self.ncbi_taxon_id:
            species_curie = f"NCBITaxon:{self.species_taxon_id}"
            if species_curie not in xrefs:
                xrefs.append(species_curie)

        return sorted(xrefs)

    def _normalize_collection_curie(self, cc_id: str) -> str:
        """Normalize culture collection ID to CURIE format.

        Args:
            cc_id: Culture collection ID in various formats

        Returns:
            Normalized CURIE format
        """
        if ":" in cc_id:
            prefix, local_id = cc_id.split(":", 1)
            prefix = prefix.strip().upper()
            local_id = local_id.strip()
        else:
            # Try to parse "DSM 16371" or "DSM-16371" format
            match = re.match(r"([A-Z]+)[\s-]*(.*)", cc_id.strip())
            if match:
                prefix = match.group(1)
                local_id = match.group(2)
            else:
                return cc_id

        # Map to bioregistry canonical prefix
        canonical_prefix = COLLECTION_PREFIX_MAP.get(prefix, prefix.lower())

        # Validate with bioregistry if available
        if bioregistry.get_resource(canonical_prefix):
            # Use bioregistry-validated format
            return f"{canonical_prefix}:{local_id}"
        else:
            # Use as-is for unregistered prefixes
            return f"{canonical_prefix}:{local_id}"
