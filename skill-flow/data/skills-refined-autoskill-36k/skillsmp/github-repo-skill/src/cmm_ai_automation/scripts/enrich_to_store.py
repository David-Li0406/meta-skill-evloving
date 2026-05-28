#!/usr/bin/env python3
"""Multi-source enrichment pipeline that loads data into EnrichmentStore.

Reads ingredients and enriches them by querying:
- PubChem (chemical identifiers, structure)
- ChEBI (roles, ontology)
- CAS Common Chemistry (mixtures, additional identifiers)
- Node Normalization (identifier resolution)

All data is stored in a linkml-store backed DuckDB database with entity resolution
based on (InChIKey, CAS RN) composite keys. The store tracks data provenance,
handles conflicts, and can export to KGX format for knowledge graph integration.

Usage:
    uv run python -m cmm_ai_automation.scripts.enrich_to_store -i data/private/derived/ingredients.tsv
    uv run python -m cmm_ai_automation.scripts.enrich_to_store --dry-run
    uv run python -m cmm_ai_automation.scripts.enrich_to_store --export-kgx
"""

import csv
import logging
import sys
from pathlib import Path
from typing import Any

import click
from dotenv import load_dotenv

from cmm_ai_automation.clients.cas import CASResult, get_cas_client
from cmm_ai_automation.clients.chebi import ChEBIClient, ChEBICompound, ChEBISearchResult
from cmm_ai_automation.clients.node_normalization import NodeNormalizationClient, NormalizedNode
from cmm_ai_automation.clients.pubchem import CompoundResult, PubChemClient
from cmm_ai_automation.store.enrichment_store import EnrichmentStore

# Load environment variables
load_dotenv()

# Default paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "data" / "private" / "derived" / "ingredients.tsv"
DEFAULT_STORE = PROJECT_ROOT / "data" / "enrichment.duckdb"
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "kgx" / "ingredients"

logger = logging.getLogger(__name__)


def normalize_inchikey(inchikey: str | None) -> str | None:
    """Normalize InChIKey format by removing any prefix.

    CAS API returns 'InChIKey=XXXX' format, others return bare 'XXXX'.
    We standardize to bare format for consistent entity resolution.
    """
    if not inchikey:
        return None
    # Strip common prefixes
    for prefix in ("InChIKey=", "INCHIKEY:", "inchikey:"):
        if inchikey.startswith(prefix):
            return inchikey[len(prefix) :]
    return inchikey


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def pubchem_to_dict(result: CompoundResult, query: str) -> dict[str, Any]:
    """Convert PubChem result to enrichment dict."""
    return {
        "name": result.Title or query,
        "pubchem_cid": result.CID,
        "inchikey": normalize_inchikey(result.InChIKey),
        "smiles": result.CanonicalSMILES,
        "chemical_formula": result.MolecularFormula,
        "molecular_mass": result.MolecularWeight,
        "iupac_name": result.IUPACName,
    }


def chebi_to_dict(result: ChEBISearchResult, compound_data: dict[str, Any] | None = None) -> dict[str, Any]:
    """Convert ChEBI result to enrichment dict.

    Args:
        result: ChEBI search result
        compound_data: Optional full compound data from get_compound_by_id
    """
    data: dict[str, Any] = {
        "name": result.name or result.ascii_name,
        "chebi_id": result.chebi_id,
    }

    # Add full compound data if available
    if compound_data:
        if compound_data.get("inchikey"):
            data["inchikey"] = normalize_inchikey(compound_data["inchikey"])
        if compound_data.get("smiles"):
            data["smiles"] = compound_data["smiles"]
        # ChEBI returns formula, we store as chemical_formula
        if compound_data.get("formula"):
            data["chemical_formula"] = compound_data["formula"]
        if compound_data.get("mass"):
            data["molecular_mass"] = compound_data["mass"]
        if compound_data.get("monoisotopic_mass"):
            data["monoisotopic_mass"] = compound_data["monoisotopic_mass"]
        if compound_data.get("charge") is not None:
            data["charge"] = compound_data["charge"]
        if compound_data.get("inchi"):
            data["inchi"] = compound_data["inchi"]
        if compound_data.get("definition"):
            data["description"] = compound_data["definition"]
        if compound_data.get("synonyms"):
            data["synonyms"] = compound_data["synonyms"]

        # Add roles - ChEBICompound.to_dict() returns "roles" as list of dicts
        # with keys: chebi_id, name, is_biological, is_chemical
        roles = compound_data.get("roles", [])
        if roles:
            biological_roles = [r["chebi_id"] for r in roles if r.get("is_biological")]
            chemical_roles = [r["chebi_id"] for r in roles if r.get("is_chemical")]
            if biological_roles:
                data["biological_roles"] = biological_roles
            if chemical_roles:
                data["chemical_roles"] = chemical_roles

    return data


def cas_to_dict(result: CASResult, query: str) -> dict[str, Any]:
    """Convert CAS result to enrichment dict."""
    data: dict[str, Any] = {
        "name": result.name or query,
        "cas_rn": result.rn,
        "is_mixture": result.is_mixture,
    }

    if result.inchikey:
        data["inchikey"] = normalize_inchikey(result.inchikey)
    if result.smiles:
        data["smiles"] = result.smiles
    if result.molecular_formula:
        data["chemical_formula"] = result.molecular_formula
    if result.molecular_mass:
        data["molecular_mass"] = result.molecular_mass
    if result.synonyms:
        data["synonyms"] = result.synonyms

    return data


def node_norm_to_dict(result: NormalizedNode) -> dict[str, Any]:
    """Convert Node Normalization result to enrichment dict."""
    data: dict[str, Any] = {}

    # Extract IDs from equivalent_ids using helper methods
    chebi_ids = result.get_chebi_ids()
    if chebi_ids:
        data["chebi_id"] = f"CHEBI:{chebi_ids[0]}"

    pubchem_cids = result.get_pubchem_cids()
    if pubchem_cids:
        data["pubchem_cid"] = pubchem_cids[0]

    if result.cas_rn:
        data["cas_rn"] = result.cas_rn
    if result.inchikey:
        data["inchikey"] = normalize_inchikey(result.inchikey)

    return data


def extract_all_curies(data: dict[str, Any]) -> set[str]:
    """Extract all CURIEs from enrichment data for normalization.

    Extracts CURIEs in the format: CHEBI:*, PUBCHEM.COMPOUND:*, CAS:*, etc.

    Args:
        data: Enrichment data dictionary

    Returns:
        Set of CURIE strings
    """
    curies = set()

    if data.get("chebi_id"):
        curies.add(data["chebi_id"])
    if data.get("pubchem_cid"):
        curies.add(f"PUBCHEM.COMPOUND:{data['pubchem_cid']}")
    if data.get("cas_rn"):
        curies.add(f"CAS:{data['cas_rn']}")
    if data.get("inchikey"):
        curies.add(f"INCHIKEY:{data['inchikey']}")

    return curies


def merge_synonyms(sources_data: dict[str, dict[str, Any]]) -> list[str]:
    """Merge and deduplicate synonyms from all sources.

    Args:
        sources_data: Dict mapping source name to data dict

    Returns:
        Deduplicated list of all synonyms, sorted alphabetically
    """
    all_synonyms = set()

    for data in sources_data.values():
        synonyms = data.get("synonyms")
        if not synonyms:
            continue

        # Handle both list and single string
        if isinstance(synonyms, list):
            all_synonyms.update(synonyms)
        elif isinstance(synonyms, str):
            all_synonyms.add(synonyms)

    # Sort for deterministic output
    return sorted(all_synonyms)


def determine_biolink_category(sources_data: dict[str, dict[str, Any]]) -> str:
    """Determine biolink category from source data.

    Uses CAS is_mixture field as authoritative source for classification.

    Args:
        sources_data: Dict mapping source name to data dict

    Returns:
        "biolink:SmallMolecule" or "biolink:ChemicalMixture"
    """
    # Check CAS data for mixture classification (authoritative)
    for source_name, data in sources_data.items():
        if source_name.startswith("cas"):
            is_mixture = data.get("is_mixture")
            if is_mixture is True:
                return "biolink:ChemicalMixture"
            elif is_mixture is False:
                return "biolink:SmallMolecule"

    # Default to SmallMolecule if no CAS data
    return "biolink:SmallMolecule"


def spider_enrich_ingredient(
    name: str,
    pubchem_client: PubChemClient | None,
    chebi_client: ChEBIClient | None,
    cas_client: Any | None,  # CASClient type
    node_norm_client: NodeNormalizationClient,
    max_iterations: int = 5,
) -> dict[str, dict[str, Any]]:
    """Enrich ingredient using iterative spidering.

    Phase 1: Query all APIs by name
    Phase 2: Iteratively normalize IDs and query discovered sources
    Phase 3: Consolidate synonyms and determine biolink category

    Args:
        name: Ingredient name to enrich
        pubchem_client: PubChem API client
        chebi_client: ChEBI API client
        cas_client: CAS API client
        node_norm_client: Node Normalization client
        max_iterations: Maximum spider iterations (safety limit)

    Returns:
        Dict mapping source name to enrichment data
    """
    sources_data: dict[str, dict[str, Any]] = {}

    # Track queried IDs to prevent re-querying (infinite loop prevention)
    queried_ids: set[str] = set()

    iteration = 0

    # Phase 1: Initial discovery by name
    click.echo("  Phase 1: Initial discovery by name")

    # Query PubChem by name
    if pubchem_client:
        click.echo("    → PubChem (by name): ", nl=False)
        try:
            results = pubchem_client.get_compounds_by_name(name)
            if isinstance(results, list) and results:
                click.echo(f"Found {len(results)} compound(s)")
                result = results[0]
                sources_data["pubchem_name"] = pubchem_to_dict(result, name)

                # Extract synonyms (optional - continue without if fetch fails)
                try:
                    synonyms = pubchem_client.get_synonyms(result.CID)
                    if isinstance(synonyms, list):
                        sources_data["pubchem_name"]["synonyms"] = synonyms
                except Exception as e:
                    logger.debug(
                        "Failed to fetch PubChem synonyms for CID %s: %s",
                        getattr(result, "CID", "unknown"),
                        e,
                    )  # Synonyms are optional; continue enrichment

                # Mark as queried
                queried_ids.add(f"PUBCHEM.COMPOUND:{result.CID}")
            else:
                click.echo("No results")
        except Exception as e:
            click.echo(f"ERROR: {e}")

    # Query ChEBI by name
    if chebi_client:
        click.echo("    → ChEBI (by name): ", nl=False)
        try:
            chebi_result = chebi_client.search_exact(name)
            if isinstance(chebi_result, ChEBISearchResult):
                click.echo(f"Found {chebi_result.chebi_id}")
                try:
                    compound = chebi_client.get_compound(chebi_result.chebi_id)
                    compound_dict = compound.to_dict() if isinstance(compound, ChEBICompound) else None
                    sources_data["chebi_name"] = chebi_to_dict(chebi_result, compound_dict)
                    queried_ids.add(chebi_result.chebi_id)
                except Exception:
                    # Compound details failed; use search result without full compound data
                    sources_data["chebi_name"] = chebi_to_dict(chebi_result, None)
                    queried_ids.add(chebi_result.chebi_id)
            else:
                click.echo("No exact match")
        except Exception as e:
            click.echo(f"ERROR: {e}")

    # Query CAS by name
    if cas_client:
        click.echo("    → CAS (by name): ", nl=False)
        try:
            cas_results = cas_client.search_by_name(name)
            if isinstance(cas_results, list) and cas_results:
                cas_result = cas_results[0]
                click.echo(f"Found {cas_result.rn} (mixture={cas_result.is_mixture})")
                sources_data["cas_name"] = cas_to_dict(cas_result, name)
                queried_ids.add(f"CAS:{cas_result.rn}")
            else:
                click.echo("No results")
        except Exception as e:
            click.echo(f"ERROR: {e}")

    # Phase 2: Spider loop
    click.echo(f"  Phase 2: Iterative spidering (max {max_iterations} iterations)")

    while iteration < max_iterations:
        iteration += 1
        click.echo(f"    Iteration {iteration}:")

        # Collect all CURIEs from current data
        all_curies = set()
        for data in sources_data.values():
            all_curies.update(extract_all_curies(data))

        # Find new IDs to query
        new_ids = all_curies - queried_ids

        if not new_ids:
            click.echo("      No new IDs discovered, stopping spider")
            break

        click.echo(f"      Found {len(new_ids)} new IDs to normalize")

        # Normalize all new IDs in batch
        try:
            norm_results = node_norm_client.normalize_batch(list(new_ids))
        except Exception as e:
            click.echo(f"      ERROR normalizing IDs: {e}")
            break

        new_discoveries = set()

        for curie, norm_result in norm_results.items():
            if not isinstance(norm_result, NormalizedNode):
                continue

            # Mark as queried
            queried_ids.add(curie)

            # Store normalization data
            sources_data[f"node_norm_{curie}"] = node_norm_to_dict(norm_result)

            # Extract discovered IDs from equivalent_ids
            if hasattr(norm_result, "equivalent_ids") and norm_result.equivalent_ids:
                for prefix, id_list in norm_result.equivalent_ids.items():
                    if isinstance(id_list, list):
                        for id_val in id_list:
                            # Construct full CURIE
                            if ":" in str(id_val):
                                new_discoveries.add(str(id_val))
                            else:
                                new_discoveries.add(f"{prefix}:{id_val}")

        # Query APIs for newly discovered IDs
        ids_to_query = new_discoveries - queried_ids

        if not ids_to_query:
            click.echo("      No new API queries needed")
            continue

        click.echo(f"      Querying {len(ids_to_query)} IDs from APIs")

        # Query ChEBI IDs
        chebi_ids = [id for id in ids_to_query if id.startswith("CHEBI:")]
        if chebi_ids and chebi_client:
            click.echo(f"        → ChEBI: {len(chebi_ids)} IDs ", nl=False)
            successes = 0
            for chebi_id in chebi_ids:
                try:
                    compound = chebi_client.get_compound(chebi_id)
                    if isinstance(compound, ChEBICompound):
                        compound_dict = compound.to_dict()
                        # Create a search result for chebi_to_dict
                        search_result = ChEBISearchResult(
                            chebi_id=chebi_id,
                            name=compound.name or "",
                            ascii_name=compound.ascii_name or "",
                            definition=compound.definition or "",
                            stars=compound.stars or 0,
                            formula=compound.formula or "",
                            mass=compound.mass or 0.0,
                            score=0.0,
                        )
                        sources_data[f"chebi_{chebi_id}"] = chebi_to_dict(search_result, compound_dict)
                        queried_ids.add(chebi_id)
                        successes += 1
                except Exception:
                    pass  # Skip failed IDs; continue spidering remaining identifiers
            click.echo(f"({successes} succeeded)")

        # Query PubChem CIDs
        pubchem_ids = [id for id in ids_to_query if id.startswith("PUBCHEM.COMPOUND:")]
        if pubchem_ids and pubchem_client:
            click.echo(f"        → PubChem: {len(pubchem_ids)} CIDs ", nl=False)
            successes = 0
            for pc_id in pubchem_ids:
                try:
                    cid = int(pc_id.split(":")[1])
                    result = pubchem_client.get_compound_by_cid(cid)  # type: ignore[assignment]
                    if isinstance(result, CompoundResult):
                        sources_data[f"pubchem_{cid}"] = pubchem_to_dict(result, name)

                        # Get synonyms (optional - continue without if fetch fails)
                        try:
                            synonyms = pubchem_client.get_synonyms(cid)
                            if isinstance(synonyms, list):
                                sources_data[f"pubchem_{cid}"]["synonyms"] = synonyms
                        except Exception:
                            pass  # Synonyms are optional; continue enrichment without them

                        queried_ids.add(pc_id)
                        successes += 1
                except Exception:
                    pass  # Skip failed IDs; continue spidering remaining identifiers
            click.echo(f"({successes} succeeded)")

        # Query CAS RNs
        cas_ids = [id for id in ids_to_query if id.startswith("CAS:")]
        if cas_ids and cas_client:
            click.echo(f"        → CAS: {len(cas_ids)} RNs ", nl=False)
            successes = 0
            for cas_id in cas_ids:
                try:
                    rn = cas_id.split(":")[1]
                    result = cas_client.get_by_rn(rn)
                    if isinstance(result, CASResult):
                        sources_data[f"cas_{rn}"] = cas_to_dict(result, name)
                        queried_ids.add(cas_id)
                        successes += 1
                except Exception:
                    pass  # Skip failed IDs; continue spidering remaining identifiers
            click.echo(f"({successes} succeeded)")

    if iteration >= max_iterations:
        click.echo(f"      Reached maximum iterations ({max_iterations}), stopping")

    # Phase 3: Consolidate
    click.echo("  Phase 3: Consolidation")
    click.echo(f"    Total sources: {len(sources_data)}")
    click.echo(f"    Total IDs queried: {len(queried_ids)}")

    # Merge synonyms across all sources
    all_synonyms = merge_synonyms(sources_data)
    if all_synonyms:
        # Add merged synonyms to a consolidated record
        sources_data["_consolidated_synonyms"] = {"synonyms": all_synonyms}
        click.echo(f"    Total unique synonyms: {len(all_synonyms)}")

    # Determine biolink category
    category = determine_biolink_category(sources_data)
    sources_data["_consolidated_category"] = {"biolink_category": category}
    click.echo(f"    Biolink category: {category}")

    return sources_data


@click.command()
@click.option(
    "--input",
    "-i",
    "input_file",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_INPUT,
    help="Input TSV file with normalized ingredients",
)
@click.option(
    "--store",
    "-s",
    "store_path",
    type=click.Path(path_type=Path),
    default=DEFAULT_STORE,
    help="Path to DuckDB enrichment store",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making API calls",
)
@click.option(
    "--export-kgx",
    is_flag=True,
    help="Export to KGX TSV format after enrichment",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(path_type=Path),
    default=DEFAULT_OUTPUT,
    help="Base path for KGX output (creates {path}_nodes.tsv and {path}_edges.tsv)",
)
@click.option(
    "--limit",
    "-n",
    type=int,
    help="Limit number of ingredients to process (for testing)",
)
@click.option(
    "--no-pubchem",
    is_flag=True,
    help="Skip PubChem lookups",
)
@click.option(
    "--no-chebi",
    is_flag=True,
    help="Skip ChEBI lookups",
)
@click.option(
    "--no-cas",
    is_flag=True,
    help="Skip CAS lookups",
)
@click.option(
    "--no-node-norm",
    is_flag=True,
    help="Skip Node Normalization lookups",
)
@click.option(
    "--max-spider-iterations",
    type=int,
    default=5,
    help="Maximum spider iterations for iterative enrichment (default: 5)",
)
def main(
    input_file: Path,
    store_path: Path,
    verbose: bool,
    dry_run: bool,
    export_kgx: bool,
    output_path: Path,
    limit: int | None,
    no_pubchem: bool,
    no_chebi: bool,
    no_cas: bool,
    no_node_norm: bool,
    max_spider_iterations: int,
) -> None:
    """Multi-source enrichment pipeline with EnrichmentStore.

    Enriches ingredients by querying multiple APIs and storing results
    in a linkml-store backed database with entity resolution and provenance.

    Example:
        # Enrich all ingredients
        uv run python -m cmm_ai_automation.scripts.enrich_to_store

        # Test with first 5 ingredients
        uv run python -m cmm_ai_automation.scripts.enrich_to_store --limit 5 --verbose

        # Enrich and export to KGX
        uv run python -m cmm_ai_automation.scripts.enrich_to_store --export-kgx
    """
    setup_logging(verbose)

    # Read input ingredients
    click.echo(f"Reading ingredients from: {input_file}")
    with input_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        ingredients = list(reader)

    if limit:
        ingredients = ingredients[:limit]
        click.echo(f"Limited to first {limit} ingredients")

    click.echo(f"Found {len(ingredients)} ingredients to process")

    # Validate required columns
    if ingredients:
        required_columns = ["ingredient_name"]
        missing = [col for col in required_columns if col not in ingredients[0]]
        if missing:
            click.echo(f"ERROR: Missing required columns: {', '.join(missing)}")
            sys.exit(1)

    if dry_run:
        click.echo("\n[DRY RUN] Would enrich ingredients:")
        for ing in ingredients:
            name = ing.get("ingredient_name", "UNKNOWN")
            click.echo(f"  - {name}")
            if not no_pubchem:
                click.echo("    → PubChem: search by name")
            if not no_chebi:
                click.echo("    → ChEBI: search by name")
            if not no_cas:
                click.echo("    → CAS: search by name")
            if not no_node_norm:
                click.echo("    → Node Normalization: resolve IDs")
        return

    # Initialize store
    click.echo(f"\nInitializing enrichment store: {store_path}")
    store = EnrichmentStore(store_path=store_path)

    # Ensure schema includes all fields by inserting a dummy record with all fields
    # This forces linkml-store to create all columns in DuckDB
    # We'll delete this immediately after
    if (store_path.exists() and store_path.stat().st_size == 0) or not store_path.exists():
        click.echo("Initializing database schema with all fields...")
        dummy_record = {
            "name": "_schema_init_",
            "inchikey": "DUMMY",
            "cas_rn": "0-00-0",
            "chebi_id": "CHEBI:0",
            "pubchem_cid": 0,
            "mediadive_id": 0,
            "kegg_id": "C00000",
            "mesh_id": "D000000",
            "drugbank_id": "DB00000",
            "chemical_formula": "X",
            "smiles": "C",
            "inchi": "InChI=1S/X",
            "molecular_mass": 0.0,
            "monoisotopic_mass": 0.0,
            "charge": 0,
            "iupac_name": "dummy",
            "synonyms": ["dummy"],
            "biological_roles": ["dummy"],
            "chemical_roles": ["dummy"],
            "application_roles": ["dummy"],
            "is_mixture": False,
        }
        store.upsert_ingredient(dummy_record, source="_schema_init_", query="_init_")
        # Delete the dummy record
        collection = store._get_collection()
        collection.delete_where({"id": "DUMMY|0-00-0"})
        click.echo("Schema initialized")

    # Initialize API clients
    pubchem_client = PubChemClient() if not no_pubchem else None
    chebi_client = ChEBIClient() if not no_chebi else None
    cas_client = get_cas_client() if not no_cas else None
    node_norm_client = NodeNormalizationClient() if not no_node_norm else None

    if cas_client:
        click.echo("CAS Common Chemistry API enabled")
    elif not no_cas:
        click.echo("CAS API key not found, skipping CAS lookups")

    # Track statistics
    stats = {
        "processed": 0,
        "pubchem_success": 0,
        "chebi_success": 0,
        "cas_success": 0,
        "node_norm_success": 0,
        "errors": 0,
    }

    # Process each ingredient
    for idx, ing in enumerate(ingredients, 1):
        name = ing["ingredient_name"]
        click.echo(f"\n[{idx}/{len(ingredients)}] Processing: {name}")

        stats["processed"] += 1

        try:
            # Use spider enrichment to iteratively discover and query all related IDs
            sources_data = spider_enrich_ingredient(
                name=name,
                pubchem_client=pubchem_client if not no_pubchem else None,
                chebi_client=chebi_client if not no_chebi else None,
                cas_client=cas_client if not no_cas else None,
                node_norm_client=node_norm_client,  # type: ignore[arg-type]
                max_iterations=max_spider_iterations,
            )

            # Update stats based on sources found
            if any(k.startswith("pubchem") for k in sources_data):
                stats["pubchem_success"] += 1
            if any(k.startswith("chebi") for k in sources_data):
                stats["chebi_success"] += 1
            if any(k.startswith("cas") for k in sources_data):
                stats["cas_success"] += 1
            if any(k.startswith("node_norm") for k in sources_data):
                stats["node_norm_success"] += 1

            # Store all source data with provenance
            if sources_data:
                # Merge all fields from all sources
                merged_data: dict[str, Any] = {}

                for source, data in sources_data.items():
                    # Skip internal consolidation records during merging
                    if source.startswith("_consolidated"):
                        continue

                    for key, value in data.items():
                        if value is not None and key not in merged_data:
                            merged_data[key] = value

                # Add consolidated synonyms to merged_data
                if "_consolidated_synonyms" in sources_data:
                    merged_synonyms = sources_data["_consolidated_synonyms"].get("synonyms")
                    if merged_synonyms:
                        merged_data["synonyms"] = merged_synonyms

                # Upsert for each source to track provenance
                for source, data in sources_data.items():
                    # Skip internal consolidation records
                    if source.startswith("_consolidated"):
                        continue

                    data_with_keys = {**data}
                    # Add composite key fields from merged data
                    if "inchikey" not in data_with_keys and merged_data.get("inchikey"):
                        data_with_keys["inchikey"] = merged_data["inchikey"]
                    if "cas_rn" not in data_with_keys and merged_data.get("cas_rn"):
                        data_with_keys["cas_rn"] = merged_data["cas_rn"]
                    # Add consolidated synonyms to each record
                    if "synonyms" not in data_with_keys and merged_data.get("synonyms"):
                        data_with_keys["synonyms"] = merged_data["synonyms"]

                    store.upsert_ingredient(data_with_keys, source=source, query=name)

        except Exception as e:
            click.echo(f"  ERROR during enrichment: {e}")
            logger.debug(f"Enrichment error for {name}", exc_info=True)
            stats["errors"] += 1

    # Print statistics
    click.echo("\n" + "=" * 60)
    click.echo("Enrichment Statistics:")
    click.echo("=" * 60)
    click.echo(f"  Ingredients processed:    {stats['processed']}")
    click.echo(f"  PubChem successes:        {stats['pubchem_success']}")
    click.echo(f"  ChEBI successes:          {stats['chebi_success']}")
    click.echo(f"  CAS successes:            {stats['cas_success']}")
    click.echo(f"  Node Norm successes:      {stats['node_norm_success']}")
    click.echo(f"  Errors encountered:       {stats['errors']}")

    # Get store statistics
    store_stats = store.get_stats()
    click.echo("\n" + "=" * 60)
    click.echo("EnrichmentStore Statistics:")
    click.echo("=" * 60)
    click.echo(f"  Total ingredients:        {store_stats['total_ingredients']}")
    click.echo(f"  With ChEBI ID:            {store_stats['with_chebi_id']} ({store_stats['coverage_chebi']:.1%})")
    click.echo(f"  With PubChem CID:         {store_stats['with_pubchem_cid']} ({store_stats['coverage_pubchem']:.1%})")
    click.echo(f"  With CAS RN:              {store_stats['with_cas_rn']} ({store_stats['coverage_cas']:.1%})")
    click.echo(f"  With InChIKey:            {store_stats['with_inchikey']}")
    click.echo(f"  With biological roles:    {store_stats['with_biological_roles']}")
    click.echo(f"  With conflicts:           {store_stats['with_conflicts']}")

    # Export to KGX if requested
    if export_kgx:
        click.echo("\n" + "=" * 60)
        click.echo("Exporting to KGX format...")
        click.echo("=" * 60)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        nodes_count, edges_count = store.export_to_kgx(output_path)
        click.echo(f"\n✓ Exported {nodes_count} nodes and {edges_count} edges")
        click.echo(f"  Nodes: {output_path}_nodes.tsv")
        click.echo(f"  Edges: {output_path}_edges.tsv")

    store.close()

    if stats["errors"] > 0:
        click.echo(f"\n⚠ Completed with {stats['errors']} error(s)")
        sys.exit(1)
    else:
        click.echo("\n✓ Enrichment completed successfully!")


if __name__ == "__main__":
    main()
