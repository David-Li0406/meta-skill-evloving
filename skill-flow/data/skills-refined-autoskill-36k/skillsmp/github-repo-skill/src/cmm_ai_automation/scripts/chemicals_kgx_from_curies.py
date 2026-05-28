#!/usr/bin/env python3
"""Generate KGX nodes for chemicals from a file of CURIEs.

Takes an input file with a column containing CHEBI: or PUBCHEM.COMPOUND:
CURIEs, fetches chemical data from ChEBI and PubChem APIs, and outputs
a KGX-format nodes file.

Only processes actual chemical entity CURIEs (CHEBI, PUBCHEM.COMPOUND).
Non-chemical CURIEs (doi:, uuid:, etc.) are skipped.

Supports:
- Random sampling (--sample-n or --sample-fraction)
- ChEBI role annotations with names

Example usage:
    uv run python -m cmm_ai_automation.scripts.chemicals_kgx_from_curies \
        --input data/chemicals.tsv \
        --id-field id \
        --output-dir data/output/

    # With sampling
    uv run python -m cmm_ai_automation.scripts.chemicals_kgx_from_curies \
        --input data/chemicals.tsv \
        --id-field id \
        --sample-n 10 \
        --output-dir data/output/
"""

from __future__ import annotations

import csv
import logging
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

import click
from kgx.sink import TsvSink
from kgx.transformer import Transformer

from cmm_ai_automation.clients.chebi import (
    ChEBIClient,
    ChEBICompound,
    ChEBILookupError,
)
from cmm_ai_automation.clients.pubchem import (
    CompoundResult,
    PubChemClient,
)
from cmm_ai_automation.clients.pubchem import (
    LookupError as PubChemLookupError,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# KGX constants
BIOLINK_CHEMICAL_ENTITY = "biolink:ChemicalEntity"
BIOLINK_CHEMICAL_ROLE = "biolink:ChemicalRole"

# Predicate for chemical roles
HAS_ROLE_PREDICATE = "biolink:has_role"

# KGX edge provenance fields
KNOWLEDGE_LEVEL = "knowledge_assertion"
AGENT_TYPE = "manual_agent"
PRIMARY_KNOWLEDGE_SOURCE = "infores:cmm-ai-automation"


@dataclass
class ChemicalResult:
    """Result of looking up a chemical by CURIE."""

    input_curie: str
    canonical_id: str  # The ID to use in KGX output
    name: str = ""
    category: str = BIOLINK_CHEMICAL_ENTITY
    formula: str = ""
    mass: float | None = None
    inchikey: str = ""
    synonyms: list[str] = field(default_factory=list)
    xrefs: list[str] = field(default_factory=list)
    cas_numbers: list[str] = field(default_factory=list)
    chebi_roles: list[tuple[str, str]] = field(default_factory=list)  # (ChEBI ID, name) tuples
    comments: str = ""

    def to_kgx_node(self) -> dict:
        """Convert to KGX node dict for use with KGX Sink.write_node()."""
        # Collect xrefs with proper CURIE formatting
        all_xrefs: list[str] = list(self.xrefs)

        # Add CAS numbers as xrefs
        for cas in self.cas_numbers:
            cas_curie = f"casrn:{cas}"
            if cas_curie not in all_xrefs:
                all_xrefs.append(cas_curie)

        node: dict = {
            "id": self.canonical_id,
            "category": [self.category],  # KGX expects list for category
            "name": self.name,
        }

        # Only include non-empty optional fields
        if self.formula:
            node["formula"] = self.formula
        if self.mass is not None:
            node["mass"] = str(self.mass)
        if self.inchikey:
            node["inchikey"] = self.inchikey
        if all_xrefs:
            node["xref"] = sorted(set(all_xrefs))
        if self.synonyms:
            node["synonym"] = sorted(set(self.synonyms))
        if self.comments:
            node["comments"] = self.comments

        return node


def parse_curie(curie: str) -> tuple[str, str]:
    """Parse a CURIE into prefix and local ID.

    Args:
        curie: CURIE string like "CHEBI:17790" or "PUBCHEM.COMPOUND:16217523"

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


def fetch_chemical_from_chebi(chebi_id: str) -> ChemicalResult | None:
    """Fetch chemical data from ChEBI API.

    Args:
        chebi_id: ChEBI ID (numeric string, e.g., "17790")

    Returns:
        ChemicalResult or None if not found
    """
    client = ChEBIClient()
    result = client.get_compound(f"CHEBI:{chebi_id}")

    if isinstance(result, ChEBILookupError):
        logger.warning(f"ChEBI lookup failed for CHEBI:{chebi_id}: {result.error_message}")
        return None

    compound: ChEBICompound = result

    # Extract xrefs from database_refs
    xrefs: list[str] = []
    cas_numbers: list[str] = []

    for db_name, refs in compound.database_refs.items():
        for ref in refs:
            if db_name == "CAS":
                cas_numbers.append(ref.accession)
            elif db_name == "PubChem":
                xrefs.append(f"PUBCHEM.COMPOUND:{ref.accession}")
            elif db_name == "KEGG COMPOUND":
                xrefs.append(f"KEGG.COMPOUND:{ref.accession}")
            elif db_name == "KEGG DRUG":
                xrefs.append(f"KEGG.DRUG:{ref.accession}")
            elif db_name == "MetaCyc":
                xrefs.append(f"MetaCyc:{ref.accession}")
            elif db_name == "Wikipedia":
                xrefs.append(f"wikipedia.en:{ref.accession}")
            elif db_name == "DrugBank":
                xrefs.append(f"DrugBank:{ref.accession}")
            elif db_name == "HMDB":
                xrefs.append(f"HMDB:{ref.accession}")

    # Extract role ChEBI IDs with names
    chebi_roles = [(role.chebi_id, role.name) for role in compound.roles]

    return ChemicalResult(
        input_curie=f"CHEBI:{chebi_id}",
        canonical_id=compound.chebi_id,
        name=compound.ascii_name or compound.name,
        formula=compound.formula or "",
        mass=compound.mass,
        inchikey=compound.inchikey or "",
        synonyms=compound.synonyms,
        xrefs=xrefs,
        cas_numbers=cas_numbers,
        chebi_roles=chebi_roles,
    )


def fetch_chemical_from_pubchem(cid: str) -> ChemicalResult | None:
    """Fetch chemical data from PubChem API.

    Args:
        cid: PubChem Compound ID (numeric string)

    Returns:
        ChemicalResult or None if not found
    """
    client = PubChemClient()

    try:
        cid_int = int(cid)
    except ValueError:
        logger.warning(f"Invalid PubChem CID: {cid}")
        return None

    result = client.get_compound_by_cid(cid_int)

    if isinstance(result, PubChemLookupError):
        logger.warning(f"PubChem lookup failed for CID {cid}: {result.error_message}")
        return None

    compound: CompoundResult = result

    # Get xrefs (CAS, ChEBI, Wikidata)
    xrefs_data = client.get_xrefs(cid_int)
    xrefs: list[str] = []
    cas_numbers: list[str] = []

    if cas_val := xrefs_data.get("CAS"):
        cas_numbers.append(str(cas_val))
    if chebi_val := xrefs_data.get("ChEBI"):
        xrefs.append(f"CHEBI:{chebi_val}")
    if wikidata_val := xrefs_data.get("Wikidata"):
        xrefs.append(f"wikidata:{wikidata_val}")

    # Get synonyms
    synonyms_result = client.get_synonyms(cid_int)
    synonyms = synonyms_result if isinstance(synonyms_result, list) else []
    # Limit synonyms to first 20 to avoid bloat
    synonyms = synonyms[:20]

    return ChemicalResult(
        input_curie=f"PUBCHEM.COMPOUND:{cid}",
        canonical_id=f"PUBCHEM.COMPOUND:{cid}",
        name=compound.Title or compound.IUPACName or f"CID:{cid}",
        formula=compound.MolecularFormula or "",
        mass=compound.MolecularWeight,
        inchikey=compound.InChIKey or "",
        synonyms=synonyms,
        xrefs=xrefs,
        cas_numbers=cas_numbers,
    )


def read_chemicals_from_file(
    input_path: Path,
    id_field: str,
    name_field: str | None = None,
    category_field: str | None = None,
    comments_field: str | None = None,
) -> list[dict[str, str]]:
    """Read CURIEs and metadata from input file.

    Args:
        input_path: Path to TSV/CSV input file
        id_field: Column name containing CURIEs
        name_field: Optional column name for names
        category_field: Optional column name for category
        comments_field: Optional column name for comments

    Returns:
        List of dicts with curie, name, category, comments keys
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

            entry: dict[str, str] = {
                "curie": curie,
                "name": "",
                "category": BIOLINK_CHEMICAL_ENTITY,
                "comments": "",
            }

            if name_field and name_field in row:
                entry["name"] = row[name_field].strip()

            if category_field and category_field in row:
                entry["category"] = row[category_field].strip()

            if comments_field and comments_field in row:
                entry["comments"] = row[comments_field].strip()

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


def export_kgx(results: list[ChemicalResult], output_dir: Path) -> tuple[int, int]:
    """Export chemical nodes and edges using KGX Sink classes.

    Args:
        results: List of ChemicalResult objects
        output_dir: Output directory for KGX files

    Returns:
        Tuple of (nodes_count, edges_count)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect unique roles from all results for role nodes
    unique_roles: dict[str, str] = {}  # role_id -> role_name
    for result in results:
        for role_id, role_name in result.chebi_roles:
            if role_id not in unique_roles:
                unique_roles[role_id] = role_name

    # Create KGX transformer and sink
    transformer = Transformer()

    # Specify which properties to include in output
    node_props = {"id", "category", "name", "formula", "mass", "inchikey", "xref", "synonym", "comments"}
    edge_props = {"subject", "predicate", "object", "knowledge_level", "agent_type", "primary_knowledge_source"}

    output_base = output_dir / "chemicals"
    sink = TsvSink(
        owner=transformer,
        filename=str(output_base),
        format="tsv",
        node_properties=node_props,
        edge_properties=edge_props,
    )

    # Write chemical nodes
    for result in results:
        sink.write_node(result.to_kgx_node())

    # Write role nodes
    for role_id, role_name in sorted(unique_roles.items()):
        sink.write_node(
            {
                "id": role_id,
                "category": [BIOLINK_CHEMICAL_ROLE],
                "name": role_name,
            }
        )

    # Write has_role edges
    edge_count = 0
    for result in results:
        for role_id, _role_name in result.chebi_roles:
            sink.write_edge(
                {
                    "subject": result.canonical_id,
                    "predicate": HAS_ROLE_PREDICATE,
                    "object": role_id,
                    "knowledge_level": KNOWLEDGE_LEVEL,
                    "agent_type": AGENT_TYPE,
                    "primary_knowledge_source": PRIMARY_KNOWLEDGE_SOURCE,
                }
            )
            edge_count += 1

    # Finalize to flush and close files
    sink.finalize()

    total_nodes = len(results) + len(unique_roles)
    logger.info(f"Wrote {len(results)} chemical nodes and {len(unique_roles)} role nodes to {output_base}_nodes.tsv")
    logger.info(f"Wrote {edge_count} edges to {output_base}_edges.tsv")

    return total_nodes, edge_count


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
    help="Column name containing CURIEs (CHEBI:, PUBCHEM.COMPOUND:, etc.)",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output/kgx/chemicals_from_curies"),
    help="Output directory for KGX files",
)
@click.option(
    "--name-field",
    "-n",
    default="name",
    help="Column name for chemical names (default: name)",
)
@click.option(
    "--category-field",
    "-g",
    default="category",
    help="Column name for biolink category (default: category)",
)
@click.option(
    "--comments-field",
    "-c",
    default="comments",
    help="Column name for comments (default: comments)",
)
@click.option(
    "--sample-n",
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
def main(
    input_path: Path,
    id_field: str,
    output_dir: Path,
    name_field: str,
    category_field: str,
    comments_field: str,
    sample_n: int | None,
    sample_fraction: float | None,
    seed: int | None,
    dry_run: bool,
) -> None:
    """Generate KGX nodes for chemicals from CURIEs.

    Reads CURIEs from the specified column in the input file, fetches
    chemical data from ChEBI and PubChem APIs, and outputs a KGX nodes file.

    Only processes actual chemical CURIEs. Non-chemical CURIEs (doi:, uuid:,
    etc.) are skipped.

    Supported CURIE prefixes:
    - CHEBI: (e.g., CHEBI:17790) - fetches from ChEBI 2.0 API
    - PUBCHEM.COMPOUND: (e.g., PUBCHEM.COMPOUND:16217523) - fetches from PubChem API
    """
    if seed is not None:
        random.seed(seed)

    # Read input
    click.echo(f"Reading CURIEs from {input_path}, column '{id_field}'")
    entries = read_chemicals_from_file(input_path, id_field, name_field, category_field, comments_field)
    click.echo(f"Found {len(entries)} CURIEs")

    # Sample if requested
    if sample_n is not None or sample_fraction is not None:
        entries = sample_entries(entries, sample_n, sample_fraction)
        click.echo(f"Sampled {len(entries)} CURIEs")

    if dry_run:
        click.echo("\nDry run - would fetch:")
        chebi_count = 0
        pubchem_count = 0
        skipped_count = 0
        invalid_count = 0

        for entry in entries:
            try:
                prefix, local_id = parse_curie(entry["curie"])
                if prefix == "CHEBI":
                    chebi_count += 1
                elif prefix == "PUBCHEM.COMPOUND":
                    pubchem_count += 1
                else:
                    skipped_count += 1
            except ValueError as e:
                click.echo(f"  Invalid: {e}")
                invalid_count += 1

        click.echo(f"\n  ChEBI lookups: {chebi_count}")
        click.echo(f"  PubChem lookups: {pubchem_count}")
        if skipped_count:
            click.echo(f"  Skipped (non-chemical CURIEs): {skipped_count}")
        if invalid_count:
            click.echo(f"  Invalid: {invalid_count}")
        return

    # Process CURIEs
    results: list[ChemicalResult] = []
    errors: list[str] = []

    with click.progressbar(entries, label="Fetching chemicals") as bar:
        for entry in bar:
            try:
                prefix, local_id = parse_curie(entry["curie"])
            except ValueError as e:
                errors.append(str(e))
                continue

            result: ChemicalResult | None = None

            if prefix == "CHEBI":
                result = fetch_chemical_from_chebi(local_id)
                # Override name if input had one
                if result and entry.get("name") and not result.name:
                    result.name = entry["name"]

            elif prefix == "PUBCHEM.COMPOUND":
                result = fetch_chemical_from_pubchem(local_id)
                # Override name if input had one
                if result and entry.get("name") and not result.name:
                    result.name = entry["name"]

            else:
                # Skip non-chemical CURIEs (doi:, uuid:, etc.)
                continue

            if result:
                # Merge user-provided comments
                if entry.get("comments") and not result.comments:
                    result.comments = entry["comments"]

                results.append(result)

    # Report results
    click.echo(f"\nSuccessfully processed: {len(results)}")
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
    nodes_count, edges_count = export_kgx(results, output_dir)

    click.echo(f"\nOutput written to {output_dir}/")
    click.echo(f"  - {nodes_count} nodes (chemicals + roles)")
    click.echo(f"  - {edges_count} edges (has_role relationships)")


if __name__ == "__main__":
    main()
