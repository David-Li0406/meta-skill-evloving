#!/usr/bin/env python3
"""Generate KGX nodes and edges for strains from a file of CURIEs.

Takes an input file with a column containing bacdive: or NCBITaxon: CURIEs,
fetches strain data from BacDive MongoDB and/or NCBI API, and outputs
KGX-format nodes and edges files.

Supports:
- Random sampling (--sample-n or --sample-fraction)
- Optional comments/synonyms columns from input file
- Species node generation for taxonomic edges

Example usage:
    uv run python -m cmm_ai_automation.scripts.strains_kgx_from_curies \
        --input data/strains.tsv \
        --id-field strain_id \
        --output-dir data/output/

    # With sampling
    uv run python -m cmm_ai_automation.scripts.strains_kgx_from_curies \
        --input data/strains.tsv \
        --id-field strain_id \
        --sample-n 10 \
        --output-dir data/output/

    # With optional columns
    uv run python -m cmm_ai_automation.scripts.strains_kgx_from_curies \
        --input data/strains.tsv \
        --id-field strain_id \
        --comments-field notes \
        --synonyms-field aliases \
        --output-dir data/output/
"""

from __future__ import annotations

import csv
import logging
import random
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import click
from kgx.sink import TsvSink
from kgx.transformer import Transformer

from cmm_ai_automation.strains.bacdive import (
    extract_bacdive_data,
    get_bacdive_collection,
)
from cmm_ai_automation.strains.ncbi import (
    NcbiTaxonData,
    extract_genome_accessions_from_linkouts,
    extract_xrefs_from_linkouts,
    fetch_ncbi_batch,
    fetch_ncbi_linkouts,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# KGX constants
BIOLINK_ORGANISM_TAXON = "biolink:OrganismTaxon"
TAXONOMY_PREDICATE = "biolink:in_taxon"  # strain in_taxon species

# KGX edge provenance fields
KNOWLEDGE_LEVEL = "knowledge_assertion"
AGENT_TYPE = "manual_agent"
PRIMARY_KNOWLEDGE_SOURCE = "infores:cmm-ai-automation"

# TAXRANK mappings (verified against https://www.ebi.ac.uk/ols4/ontologies/taxrank)
RANK_TO_TAXRANK: dict[str, str] = {
    "species": "TAXRANK:0000006",
    "subspecies": "TAXRANK:0000023",
    "strain": "TAXRANK:0001001",
    "no rank": "",
}

# Culture collection prefix mappings (input format -> CURIE prefix)
COLLECTION_PREFIX_MAP: dict[str, str] = {
    "DSM": "dsmz",
    "DSMZ": "dsmz",
    "ATCC": "atcc",
    "JCM": "jcm",
    "NBRC": "nbrc",
    "NCIMB": "ncimb",
    "LMG": "lmg",
    "CIP": "cip",
    "CCM": "ccm",
    "CECT": "cect",
    "IAM": "iam",
    "IFO": "nbrc",  # IFO merged into NBRC
    "CCUG": "ccug",
    "VKM": "vkm",
    "BCRC": "bcrc",
    "IMET": "imet",
    "NCCB": "nccb",
    "NCIB": "ncimb",  # NCIB merged into NCIMB
}


def normalize_collection_curie(cc_id: str) -> str:
    """Normalize culture collection ID to CURIE format.

    Converts "DSM 1337" or "DSM-1337" to "dsmz:1337".

    Args:
        cc_id: Culture collection ID in various formats

    Returns:
        Normalized CURIE format
    """
    cc_id = cc_id.strip()

    # Already a CURIE with colon
    if ":" in cc_id and not cc_id[0].isdigit():
        parts = cc_id.split(":", 1)
        prefix = parts[0].strip().upper()
        local_id = parts[1].strip()
        canonical_prefix = COLLECTION_PREFIX_MAP.get(prefix, prefix.lower())
        return f"{canonical_prefix}:{local_id}"

    # Parse "DSM 1337" or "DSM-1337" format
    match = re.match(r"([A-Z]+)[\s\-]*(.+)", cc_id, re.IGNORECASE)
    if match:
        prefix = match.group(1).upper()
        local_id = match.group(2).strip()
        canonical_prefix = COLLECTION_PREFIX_MAP.get(prefix, prefix.lower())
        return f"{canonical_prefix}:{local_id}"

    return cc_id


@dataclass
class StrainResult:
    """Result of looking up a strain by CURIE."""

    input_curie: str
    canonical_id: str  # The ID to use in KGX output
    name: str = ""
    scientific_name: str = ""  # Full name including strain
    binomial_name: str = ""  # Pure species binomial (no strain designation)
    strain_designation: str = ""
    ncbi_taxon_id: str = ""
    species_taxon_id: str = ""
    parent_taxon_id: str = ""
    has_taxonomic_rank: str = ""
    bacdive_id: str = ""
    culture_collection_ids: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    xrefs: list[str] = field(default_factory=list)
    comments: str = ""
    # Genome accessions by source
    genome_accessions_ncbi: list[str] = field(default_factory=list)
    genome_accessions_img: list[str] = field(default_factory=list)
    genome_accessions_patric: list[str] = field(default_factory=list)
    genome_accessions_other: list[str] = field(default_factory=list)

    def to_kgx_node(self) -> dict:
        """Convert to KGX node dict for use with KGX Sink.write_node()."""
        # Build display name
        display_name = self.name
        if not display_name:
            parts = []
            if self.binomial_name:
                parts.append(self.binomial_name)
            elif self.scientific_name:
                parts.append(self.scientific_name)
            if self.strain_designation:
                parts.append(self.strain_designation)
            display_name = " ".join(parts) if parts else self.input_curie

        # Collect and normalize xrefs
        all_xrefs: list[str] = []
        for xref in self.xrefs:
            normalized = normalize_collection_curie(xref)
            if normalized not in all_xrefs:
                all_xrefs.append(normalized)
        for cc_id in self.culture_collection_ids:
            normalized = normalize_collection_curie(cc_id)
            if normalized not in all_xrefs:
                all_xrefs.append(normalized)

        # Determine taxonomic rank - BacDive entries are strains by definition
        rank = self.has_taxonomic_rank
        if self.bacdive_id:
            rank = "strain"  # Override any NCBI-derived rank for BacDive entries
        taxrank_curie = RANK_TO_TAXRANK.get(rank, "")

        node: dict = {
            "id": self.canonical_id,
            "category": [BIOLINK_ORGANISM_TAXON],  # KGX expects list for category
            "name": display_name,
        }

        # Only include non-empty optional fields
        if self.binomial_name:
            node["binomial_name"] = self.binomial_name
        if self.ncbi_taxon_id:
            node["ncbi_taxon_id"] = f"NCBITaxon:{self.ncbi_taxon_id}"
        if self.species_taxon_id:
            node["species_taxon_id"] = f"NCBITaxon:{self.species_taxon_id}"
        if self.parent_taxon_id:
            node["parent_taxon_id"] = f"NCBITaxon:{self.parent_taxon_id}"
        if taxrank_curie:
            node["has_taxonomic_rank"] = taxrank_curie
        if self.strain_designation:
            node["strain_designation"] = self.strain_designation
        if all_xrefs:
            node["xref"] = sorted(set(all_xrefs))
        if self.synonyms:
            node["synonym"] = sorted(set(self.synonyms))
        if self.genome_accessions_ncbi:
            node["genome_accessions_ncbi"] = sorted(self.genome_accessions_ncbi)
        if self.genome_accessions_img:
            node["genome_accessions_img"] = sorted(self.genome_accessions_img)
        if self.genome_accessions_patric:
            node["genome_accessions_patric"] = sorted(self.genome_accessions_patric)
        if self.genome_accessions_other:
            node["genome_accessions_other"] = sorted(self.genome_accessions_other)

        return node


def parse_curie(curie: str) -> tuple[str, str]:
    """Parse a CURIE into prefix and local ID.

    Args:
        curie: CURIE string like "bacdive:100" or "NCBITaxon:12345"

    Returns:
        Tuple of (prefix, local_id)

    Raises:
        ValueError: If CURIE format is invalid
    """
    curie = curie.strip()
    if ":" not in curie:
        raise ValueError(f"Invalid CURIE format (no colon): {curie}")

    prefix, local_id = curie.split(":", 1)
    return prefix.strip(), local_id.strip()


# Module-level MongoDB collection cache (set by main())
_bacdive_collection: Any = None


def lookup_bacdive_by_id(
    bacdive_id: int,
    database: str | None = None,
    collection: str | None = None,
) -> dict[str, Any] | None:
    """Look up a BacDive record by BacDive ID.

    Args:
        bacdive_id: BacDive numeric ID
        database: MongoDB database name (default: bacdive)
        collection: MongoDB collection name (default: strains)

    Returns:
        BacDive document or None
    """
    global _bacdive_collection

    # Use cached collection if available and no overrides specified
    if _bacdive_collection is not None and database is None and collection is None:
        mongo_coll = _bacdive_collection
    else:
        mongo_coll = get_bacdive_collection(database=database, collection=collection)

    if mongo_coll is None:
        logger.warning("BacDive MongoDB not available")
        return None

    # BacDive ID can be in _id or General.BacDive-ID
    doc: dict[str, Any] | None = mongo_coll.find_one({"General.BacDive-ID": bacdive_id})
    if doc is None:
        doc = mongo_coll.find_one({"_id": bacdive_id})
    return doc


def fetch_strain_from_bacdive(bacdive_id: str) -> StrainResult | None:
    """Fetch strain data from BacDive MongoDB.

    Args:
        bacdive_id: BacDive ID (numeric string)

    Returns:
        StrainResult or None if not found
    """
    try:
        bid = int(bacdive_id)
    except ValueError:
        logger.warning(f"Invalid BacDive ID: {bacdive_id}")
        return None

    doc = lookup_bacdive_by_id(bid)
    if doc is None:
        logger.warning(f"BacDive ID not found: {bacdive_id}")
        return None

    data = extract_bacdive_data(doc)

    # Get NCBI taxon ID - prefer strain-level if available
    ncbi_tax = doc.get("General", {}).get("NCBI tax id", {})
    ncbi_taxon_id = ""
    if isinstance(ncbi_tax, list):
        # Multiple taxon IDs - look for strain level first
        for entry in ncbi_tax:
            if isinstance(entry, dict) and entry.get("Matching level") == "strain":
                ncbi_taxon_id = str(entry.get("NCBI tax id", ""))
                break
        # Fall back to species level
        if not ncbi_taxon_id:
            for entry in ncbi_tax:
                if isinstance(entry, dict) and entry.get("NCBI tax id"):
                    ncbi_taxon_id = str(entry.get("NCBI tax id", ""))
                    break
    elif isinstance(ncbi_tax, dict):
        ncbi_taxon_id = str(ncbi_tax.get("NCBI tax id", ""))

    result = StrainResult(
        input_curie=f"bacdive:{bacdive_id}",
        canonical_id=f"bacdive:{bacdive_id}",
        scientific_name=data.get("species", ""),
        binomial_name=data.get("species", ""),  # Species binomial from BacDive
        strain_designation=data.get("strain_designation", ""),
        ncbi_taxon_id=ncbi_taxon_id,
        bacdive_id=bacdive_id,
        culture_collection_ids=data.get("culture_collection_ids", []),
        synonyms=data.get("synonyms", []),
        genome_accessions_ncbi=data.get("genome_accessions_ncbi", []),
        genome_accessions_img=data.get("genome_accessions_img", []),
        genome_accessions_patric=data.get("genome_accessions_patric", []),
        genome_accessions_other=data.get("genome_accessions_other", []),
    )

    return result


def fetch_strain_from_ncbi(taxon_id: str) -> StrainResult | None:
    """Fetch strain data from NCBI Taxonomy API.

    Args:
        taxon_id: NCBI Taxonomy ID (numeric string)

    Returns:
        StrainResult or None if not found
    """
    # Use batch fetch for efficiency (even for single ID)
    ncbi_data = fetch_ncbi_batch([taxon_id])
    if taxon_id not in ncbi_data:
        logger.warning(f"NCBITaxon ID not found: {taxon_id}")
        return None

    data: NcbiTaxonData = ncbi_data[taxon_id]

    # Fetch linkouts for xrefs and genome accessions
    linkouts = fetch_ncbi_linkouts([taxon_id])
    xrefs: list[str] = []
    genome_accessions_img: list[str] = []
    genome_accessions_other: list[str] = []

    if taxon_id in linkouts:
        xrefs = extract_xrefs_from_linkouts(linkouts[taxon_id])
        genome_data = extract_genome_accessions_from_linkouts(linkouts[taxon_id])
        genome_accessions_img = genome_data.get("genome_accessions_img", [])
        genome_accessions_other = genome_data.get("genome_accessions_other", [])

    # Keep input CURIE as canonical ID
    canonical_id = f"NCBITaxon:{taxon_id}"

    # Extract bacdive ID from xrefs if present (for metadata only)
    bacdive_id = ""
    for xref in xrefs:
        if xref.startswith("bacdive:"):
            bacdive_id = xref.replace("bacdive:", "")
            break

    # For NCBI, scientific_name is the full taxon name
    # binomial_name should be species binomial (without strain designation)
    scientific_name = data.get("scientific_name", "")
    binomial_name = scientific_name  # Will be refined by enrich_with_ncbi if species data available

    result = StrainResult(
        input_curie=f"NCBITaxon:{taxon_id}",
        canonical_id=canonical_id,
        name=scientific_name,
        scientific_name=scientific_name,
        binomial_name=binomial_name,
        ncbi_taxon_id=taxon_id,
        species_taxon_id=data.get("species_taxon_id", ""),
        parent_taxon_id=data.get("parent_taxon_id", ""),
        has_taxonomic_rank=data.get("rank", ""),
        bacdive_id=bacdive_id,
        synonyms=data.get("synonyms", []) + data.get("equivalent_names", []),
        xrefs=xrefs,
        genome_accessions_img=genome_accessions_img,
        genome_accessions_other=genome_accessions_other,
    )

    return result


def enrich_with_ncbi(result: StrainResult) -> None:
    """Enrich a StrainResult with NCBI data (for lineage info).

    Modifies result in place.
    """
    if not result.ncbi_taxon_id:
        return

    ncbi_data = fetch_ncbi_batch([result.ncbi_taxon_id])
    if result.ncbi_taxon_id not in ncbi_data:
        return

    data = ncbi_data[result.ncbi_taxon_id]

    # Only fill in missing fields
    if not result.species_taxon_id:
        result.species_taxon_id = data.get("species_taxon_id", "")
    if not result.parent_taxon_id:
        result.parent_taxon_id = data.get("parent_taxon_id", "")
    if not result.has_taxonomic_rank:
        result.has_taxonomic_rank = data.get("rank", "")

    # Add synonyms
    for syn in data.get("synonyms", []) + data.get("equivalent_names", []):
        if syn and syn not in result.synonyms:
            result.synonyms.append(syn)

    # Fetch and add xrefs from linkouts
    linkouts = fetch_ncbi_linkouts([result.ncbi_taxon_id])
    if result.ncbi_taxon_id in linkouts:
        xrefs = extract_xrefs_from_linkouts(linkouts[result.ncbi_taxon_id])
        for xref in xrefs:
            if xref not in result.xrefs:
                result.xrefs.append(xref)


def read_curies_from_file(
    input_path: Path,
    id_field: str,
    comments_field: str | None = None,
    synonyms_field: str | None = None,
) -> list[dict[str, str]]:
    """Read CURIEs and optional metadata from input file.

    Args:
        input_path: Path to TSV/CSV input file
        id_field: Column name containing CURIEs
        comments_field: Optional column name for comments
        synonyms_field: Optional column name for synonyms

    Returns:
        List of dicts with 'curie', 'comments', 'synonyms' keys
    """
    results: list[dict[str, str]] = []

    with input_path.open(newline="", encoding="utf-8") as f:
        # Detect delimiter
        sample = f.read(4096)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters="\t,")

        reader = csv.DictReader(f, dialect=dialect)

        if id_field not in (reader.fieldnames or []):
            raise click.ClickException(f"ID field '{id_field}' not found in input file. Available: {reader.fieldnames}")

        for row in reader:
            curie = row.get(id_field, "").strip()
            if not curie:
                continue

            entry: dict[str, str] = {"curie": curie, "comments": "", "synonyms": ""}

            if comments_field and comments_field in row:
                entry["comments"] = row[comments_field].strip()

            if synonyms_field and synonyms_field in row:
                entry["synonyms"] = row[synonyms_field].strip()

            results.append(entry)

    return results


def sample_entries(
    entries: list[dict[str, str]],
    sample_n: int | None = None,
    sample_fraction: float | None = None,
) -> list[dict[str, str]]:
    """Sample entries randomly.

    Args:
        entries: List of entries to sample from
        sample_n: Number of entries to sample
        sample_fraction: Fraction of entries to sample (0.0-1.0)

    Returns:
        Sampled list of entries
    """
    if sample_n is not None:
        n = min(sample_n, len(entries))
        return random.sample(entries, n)

    if sample_fraction is not None:
        n = max(1, int(len(entries) * sample_fraction))
        return random.sample(entries, n)

    return entries


def export_kgx(results: list[StrainResult], output_dir: Path) -> tuple[int, int, int]:
    """Export strain nodes and edges using KGX Sink classes.

    Args:
        results: List of StrainResult objects
        output_dir: Output directory for KGX files

    Returns:
        Tuple of (strain_nodes_count, species_nodes_count, edges_count)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect unique species taxon IDs for species nodes
    species_ids: set[str] = set()
    for result in results:
        if result.species_taxon_id:
            species_ids.add(result.species_taxon_id)

    # Remove any that are already strain canonical IDs
    strain_ids = {r.canonical_id for r in results}
    species_ids = {sid for sid in species_ids if f"NCBITaxon:{sid}" not in strain_ids}

    # Fetch species data from NCBI if needed
    species_data: dict = {}
    species_linkouts: dict = {}
    if species_ids:
        species_id_list = list(species_ids)
        species_data = fetch_ncbi_batch(species_id_list)
        species_linkouts = fetch_ncbi_linkouts(species_id_list)

    # Create KGX transformer and sink
    transformer = Transformer()

    # Specify which properties to include in output
    node_props = {
        "id",
        "category",
        "name",
        "binomial_name",
        "ncbi_taxon_id",
        "species_taxon_id",
        "parent_taxon_id",
        "has_taxonomic_rank",
        "strain_designation",
        "xref",
        "synonym",
        "genome_accessions_ncbi",
        "genome_accessions_img",
        "genome_accessions_patric",
        "genome_accessions_other",
    }
    edge_props = {"subject", "predicate", "object", "knowledge_level", "agent_type", "primary_knowledge_source"}

    output_base = output_dir / "strains"
    sink = TsvSink(
        owner=transformer,
        filename=str(output_base),
        format="tsv",
        node_properties=node_props,
        edge_properties=edge_props,
    )

    # Write strain nodes
    for result in results:
        sink.write_node(result.to_kgx_node())

    # Write species nodes
    species_count = 0
    for species_id, data in species_data.items():
        # Get xrefs and genome accessions from linkouts
        xrefs: list[str] = []
        genome_accessions_img: list[str] = []
        genome_accessions_other: list[str] = []

        if species_id in species_linkouts:
            xrefs = extract_xrefs_from_linkouts(species_linkouts[species_id])
            xrefs = [normalize_collection_curie(x) for x in xrefs]
            genome_data = extract_genome_accessions_from_linkouts(species_linkouts[species_id])
            genome_accessions_img = genome_data.get("genome_accessions_img", [])
            genome_accessions_other = genome_data.get("genome_accessions_other", [])

        scientific_name = data.get("scientific_name", "")

        species_node: dict = {
            "id": f"NCBITaxon:{species_id}",
            "category": [BIOLINK_ORGANISM_TAXON],
            "name": scientific_name,
            "binomial_name": scientific_name,
            "ncbi_taxon_id": f"NCBITaxon:{species_id}",
            "species_taxon_id": f"NCBITaxon:{species_id}",
        }

        if data.get("parent_taxon_id"):
            species_node["parent_taxon_id"] = f"NCBITaxon:{data['parent_taxon_id']}"
        if data.get("rank"):
            species_node["has_taxonomic_rank"] = RANK_TO_TAXRANK.get(data["rank"], "")
        if xrefs:
            species_node["xref"] = sorted(set(xrefs))
        if data.get("synonyms"):
            species_node["synonym"] = data["synonyms"]
        if genome_accessions_img:
            species_node["genome_accessions_img"] = sorted(genome_accessions_img)
        if genome_accessions_other:
            species_node["genome_accessions_other"] = sorted(genome_accessions_other)

        sink.write_node(species_node)
        species_count += 1

    # Write in_taxon edges
    edge_count = 0
    for result in results:
        if not result.species_taxon_id:
            continue

        subject_id = result.canonical_id
        object_id = f"NCBITaxon:{result.species_taxon_id}"

        # Don't create self-loops
        if subject_id == object_id:
            continue

        sink.write_edge(
            {
                "subject": subject_id,
                "predicate": TAXONOMY_PREDICATE,
                "object": object_id,
                "knowledge_level": KNOWLEDGE_LEVEL,
                "agent_type": AGENT_TYPE,
                "primary_knowledge_source": PRIMARY_KNOWLEDGE_SOURCE,
            }
        )
        edge_count += 1

    # Finalize to flush and close files
    sink.finalize()

    logger.info(f"Wrote {len(results)} strain nodes and {species_count} species nodes to {output_base}_nodes.tsv")
    logger.info(f"Wrote {edge_count} edges to {output_base}_edges.tsv")

    return len(results), species_count, edge_count


@click.command()
@click.option(
    "--input",
    "-i",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Input TSV/CSV file containing CURIEs",
)
@click.option(
    "--id-field",
    "-f",
    required=True,
    help="Column name containing CURIEs (bacdive: or NCBITaxon:)",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("data/private/strains_kgx_output"),
    help="Output directory for KGX files",
)
@click.option(
    "--comments-field",
    "-c",
    default=None,
    help="Optional column name for comments to merge into output",
)
@click.option(
    "--synonyms-field",
    "-s",
    default=None,
    help="Optional column name for synonyms to merge into output",
)
@click.option(
    "--sample-n",
    "-n",
    type=int,
    default=None,
    help="Randomly sample N CURIEs from input",
)
@click.option(
    "--sample-fraction",
    type=float,
    default=None,
    help="Randomly sample fraction (0.0-1.0) of CURIEs from input",
)
@click.option(
    "--seed",
    type=int,
    default=None,
    help="Random seed for reproducible sampling",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be fetched without making API calls",
)
@click.option(
    "--database",
    type=str,
    default=None,
    help="MongoDB database name for BacDive lookups (default: bacdive)",
)
@click.option(
    "--collection",
    type=str,
    default=None,
    help="MongoDB collection name for BacDive lookups (default: strains)",
)
def main(
    input_path: Path,
    id_field: str,
    output_dir: Path,
    comments_field: str | None,
    synonyms_field: str | None,
    sample_n: int | None,
    sample_fraction: float | None,
    seed: int | None,
    dry_run: bool,
    database: str | None,
    collection: str | None,
) -> None:
    """Generate KGX nodes and edges for strains from CURIEs.

    Reads CURIEs from the specified column in the input file, fetches
    strain data from BacDive MongoDB and/or NCBI API, and outputs
    KGX-format nodes and edges files.

    Supported CURIE prefixes:
    - bacdive: (e.g., bacdive:100) - looks up in local BacDive MongoDB
    - NCBITaxon: (e.g., NCBITaxon:12345) - fetches from NCBI Taxonomy API

    # Future: For name-based lookups, consider using:
    # - ChromaDB semantic search (see codify_strains.py)
    # - BacDive MongoDB text search (see strains/bacdive.py)
    """
    if seed is not None:
        random.seed(seed)

    # Initialize BacDive MongoDB collection (cached for efficiency)
    global _bacdive_collection
    db_name = database or "bacdive"
    coll_name = collection or "strains"
    _bacdive_collection = get_bacdive_collection(database=database, collection=collection)
    if _bacdive_collection is not None:
        click.echo(f"Connected to BacDive MongoDB ({db_name}.{coll_name})")
    else:
        click.echo(f"Warning: BacDive MongoDB ({db_name}.{coll_name}) not available")

    # Read input
    click.echo(f"Reading CURIEs from {input_path}, column '{id_field}'")
    entries = read_curies_from_file(input_path, id_field, comments_field, synonyms_field)
    click.echo(f"Found {len(entries)} CURIEs")

    # Sample if requested
    if sample_n is not None or sample_fraction is not None:
        entries = sample_entries(entries, sample_n, sample_fraction)
        click.echo(f"Sampled {len(entries)} CURIEs")

    if dry_run:
        click.echo("\nDry run - would fetch:")
        bacdive_count = 0
        ncbi_count = 0
        invalid_count = 0

        for entry in entries:
            try:
                prefix, local_id = parse_curie(entry["curie"])
                if prefix.lower() == "bacdive":
                    bacdive_count += 1
                elif prefix == "NCBITaxon":
                    ncbi_count += 1
                else:
                    click.echo(f"  Unknown prefix: {entry['curie']}")
                    invalid_count += 1
            except ValueError as e:
                click.echo(f"  Invalid: {e}")
                invalid_count += 1

        click.echo(f"\n  BacDive lookups: {bacdive_count}")
        click.echo(f"  NCBI lookups: {ncbi_count}")
        if invalid_count:
            click.echo(f"  Invalid/unknown: {invalid_count}")
        return

    # Process CURIEs
    results: list[StrainResult] = []
    errors: list[str] = []

    with click.progressbar(entries, label="Fetching strains") as bar:
        for entry in bar:
            try:
                prefix, local_id = parse_curie(entry["curie"])
            except ValueError as e:
                errors.append(str(e))
                continue

            result: StrainResult | None = None

            if prefix.lower() == "bacdive":
                result = fetch_strain_from_bacdive(local_id)
                if result:
                    # Enrich with NCBI data for lineage
                    enrich_with_ncbi(result)

            elif prefix == "NCBITaxon":
                result = fetch_strain_from_ncbi(local_id)

            else:
                errors.append(f"Unknown CURIE prefix: {prefix}")
                continue

            if result:
                # Merge user-provided comments and synonyms
                if entry.get("comments"):
                    if result.comments:
                        result.comments = f"{entry['comments']}; {result.comments}"
                    else:
                        result.comments = entry["comments"]

                if entry.get("synonyms"):
                    user_synonyms = [s.strip() for s in entry["synonyms"].split("|") if s.strip()]
                    for syn in user_synonyms:
                        if syn not in result.synonyms:
                            result.synonyms.insert(0, syn)

                results.append(result)

    # Report results
    click.echo(f"\nSuccessfully fetched: {len(results)}")
    if errors:
        click.echo(f"Errors: {len(errors)}")
        for err in errors[:5]:
            click.echo(f"  - {err}")
        if len(errors) > 5:
            click.echo(f"  ... and {len(errors) - 5} more")

    if not results:
        click.echo("No results to export")
        sys.exit(1)

    # Write outputs using KGX sink
    strain_count, species_count, edge_count = export_kgx(results, output_dir)

    click.echo(f"\nOutput written to {output_dir}/")
    click.echo(f"  - {strain_count} strain nodes")
    click.echo(f"  - {species_count} species nodes")
    click.echo(f"  - {edge_count} edges (in_taxon relationships)")


if __name__ == "__main__":
    main()
