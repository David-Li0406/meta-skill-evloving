#!/usr/bin/env python3
"""Enrich ingredients with PubChem and optionally CAS Common Chemistry data.

Reads an ingredients TSV file and queries PubChem for each ingredient,
adding chemical identifiers like InChIKey, CID, and SMILES.

Optionally queries CAS Common Chemistry API if CAS_API_KEY is set in environment.
CAS is particularly good for undefined mixtures like peptone, yeast extract, etc.

Outputs one row per CID found, so ingredients with multiple matches
will have multiple rows in the output.

Uses a JSON cache to avoid re-querying APIs for compounds we've already looked up.
"""

import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any

import click
from dotenv import load_dotenv

from cmm_ai_automation.clients.cas import CASClient, CASLookupError, get_cas_client
from cmm_ai_automation.clients.pubchem import LookupError, PubChemClient

# Load environment variables from .env file
load_dotenv()

# Default paths relative to project root
# __file__ is src/cmm_ai_automation/scripts/enrich_ingredients.py
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "data" / "private" / "derived" / "ingredients.tsv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "private" / "derived" / "ingredients_enriched.tsv"
CACHE_ROOT = PROJECT_ROOT / "cache"
DEFAULT_CACHE = CACHE_ROOT / "pubchem" / "pubchem_cache.json"
DEFAULT_CAS_CACHE = CACHE_ROOT / "cas" / "cas_cache.json"

logger = logging.getLogger(__name__)


def load_cache(cache_file: Path) -> dict[str, Any]:
    """Load cache from JSON file."""
    if cache_file.exists():
        with cache_file.open(encoding="utf-8") as f:
            cache: dict[str, Any] = json.load(f)
            return cache
    return {}


def save_cache(cache_file: Path, cache: dict[str, Any]) -> None:
    """Save cache to JSON file."""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open("w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


@click.command()
@click.option(
    "--input",
    "-i",
    "input_file",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_INPUT,
    help="Input TSV file with ingredients",
)
@click.option(
    "--output",
    "-o",
    "output_file",
    type=click.Path(path_type=Path),
    default=DEFAULT_OUTPUT,
    help="Output TSV file with enriched data",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.option(
    "--cache",
    "-c",
    "cache_file",
    type=click.Path(path_type=Path),
    default=DEFAULT_CACHE,
    help="JSON cache file for PubChem lookups",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Disable cache (always query PubChem)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making API calls",
)
@click.option(
    "--cas-cache",
    "cas_cache_file",
    type=click.Path(path_type=Path),
    default=DEFAULT_CAS_CACHE,
    help="JSON cache file for CAS lookups",
)
@click.option(
    "--no-cas",
    is_flag=True,
    help="Disable CAS lookups even if API key is available",
)
def main(
    input_file: Path,
    output_file: Path,
    verbose: bool,
    cache_file: Path,
    no_cache: bool,
    dry_run: bool,
    cas_cache_file: Path,
    no_cas: bool,
) -> None:
    """Enrich ingredients with PubChem and optionally CAS data.

    Reads ingredients from a TSV file, queries PubChem for each one,
    and writes enriched data with chemical identifiers.

    If CAS_API_KEY is set, also queries CAS Common Chemistry for additional
    data (particularly useful for undefined mixtures like peptone).

    Outputs one row per CID found. Ingredients with multiple PubChem
    matches will have multiple rows in the output.
    """
    setup_logging(verbose)

    # Read input file
    click.echo(f"Reading ingredients from: {input_file}")
    with input_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        ingredients = list(reader)

    click.echo(f"Found {len(ingredients)} ingredients")

    # Validate required columns
    if ingredients:
        required_columns = ["ingredient_name"]
        missing_columns = [col for col in required_columns if col not in ingredients[0]]
        if missing_columns:
            click.echo(f"ERROR: Input file is missing required columns: {', '.join(missing_columns)}")
            sys.exit(1)

    if dry_run:
        click.echo("\n[DRY RUN] Would query PubChem for:")
        for ing in ingredients:
            click.echo(f"  - {ing.get('ingredient_name', 'UNKNOWN')}")
        return

    # Load caches
    cache: dict[str, Any] = {}
    if not no_cache:
        cache = load_cache(cache_file)
        click.echo(f"Loaded {len(cache)} cached PubChem entries from: {cache_file}")

    cas_cache: dict[str, Any] = {}
    cas_client: CASClient | None = None
    if not no_cas:
        cas_client = get_cas_client()
        if cas_client:
            if not no_cache:
                cas_cache = load_cache(cas_cache_file)
                click.echo(f"Loaded {len(cas_cache)} cached CAS entries from: {cas_cache_file}")
            click.echo("CAS Common Chemistry API enabled")
        else:
            click.echo("CAS API key not found, skipping CAS lookups")

    # Create PubChem client
    client = PubChemClient()

    # Helper to get CAS data for an ingredient
    def get_cas_data(name: str) -> dict[str, str]:
        """Look up CAS data for an ingredient name."""
        empty_cas = {
            "cas_rn": "",
            "cas_name": "",
            "cas_inchi": "",
            "cas_inchikey": "",
            "cas_smiles": "",
            "cas_is_mixture": "",
            "cas_error": "",
        }

        if not cas_client:
            return empty_cas

        # Check CAS cache first
        if not no_cache and name in cas_cache:
            cached_cas: dict[str, str] = cas_cache[name]
            click.echo(f"  CAS: CACHED (RN:{cached_cas.get('cas_rn', 'N/A')})")
            return cached_cas

        # Query CAS
        click.echo("  CAS: ", nl=False)
        cas_results = cas_client.search_by_name(name)

        if isinstance(cas_results, list) and cas_results:
            # Take the first result
            cas_result = cas_results[0]
            click.echo(f"RN:{cas_result.rn} (mixture={cas_result.is_mixture})")
            cas_data = {
                "cas_rn": cas_result.rn,
                "cas_name": cas_result.name,
                "cas_inchi": cas_result.inchi or "",
                "cas_inchikey": cas_result.inchikey or "",
                "cas_smiles": cas_result.smiles or "",
                "cas_is_mixture": "true" if cas_result.is_mixture else "false",
                "cas_error": "",
            }
            cas_cache[name] = cas_data
            return cas_data
        elif isinstance(cas_results, CASLookupError):
            click.echo(f"ERROR: {cas_results.error_code}")
            cas_data = {**empty_cas, "cas_error": cas_results.error_message}
            cas_cache[name] = cas_data
            return cas_data
        else:
            click.echo("No results")
            cas_cache[name] = empty_cas
            return empty_cas

    # Process ingredients
    enriched = []
    success_count = 0
    error_count = 0
    cache_hit_count = 0
    multi_match_count = 0

    for ing in ingredients:
        name = ing["ingredient_name"]

        # Check cache first
        if not no_cache and name in cache:
            cached = cache[name]
            if isinstance(cached, list):
                # Multiple results cached
                click.echo(f"Looking up: {name}... CACHED ({len(cached)} CIDs)")
                # Get CAS data (may also be cached)
                cas_data = get_cas_data(name) if cas_client else {}
                for result_dict in cached:
                    enriched.append({**ing, **result_dict, **cas_data})
                success_count += 1
                if len(cached) > 1:
                    multi_match_count += 1
            else:
                # Single result or error cached (old format or error)
                cid_display = cached.get("pubchem_cid", "N/A") or "ERROR"
                click.echo(f"Looking up: {name}... CACHED (CID:{cid_display})")
                # Get CAS data (may also be cached)
                cas_data = get_cas_data(name) if cas_client else {}
                enriched.append({**ing, **cached, **cas_data})
                if cached.get("pubchem_error"):
                    error_count += 1
                else:
                    success_count += 1
            cache_hit_count += 1
            continue

        # Query PubChem for all matching compounds
        click.echo(f"Looking up: {name}... ", nl=False)
        results = client.get_compounds_by_name(name)

        # Get CAS data (if enabled)
        cas_data = {}
        if cas_client:
            click.echo("")  # Newline before CAS lookup
            cas_data = get_cas_data(name)

        if isinstance(results, list):
            cids = [r.CID for r in results]
            if not cas_client:
                click.echo(f"{len(results)} CID(s): {', '.join(map(str, cids))}")
            else:
                click.echo(f"  PubChem: {len(results)} CID(s): {', '.join(map(str, cids))}")

            result_dicts = []
            for result in results:
                result_dict = {
                    "pubchem_cid": str(result.CID),
                    "pubchem_inchikey": result.InChIKey or "",
                    "pubchem_canonical_smiles": result.CanonicalSMILES or "",
                    "pubchem_molecular_formula": result.MolecularFormula or "",
                    "pubchem_iupac_name": result.IUPACName or "",
                    "pubchem_title": result.Title or "",
                    "pubchem_error": "",
                }
                enriched.append({**ing, **result_dict, **cas_data})
                result_dicts.append(result_dict)

            cache[name] = result_dicts
            success_count += 1
            if len(results) > 1:
                multi_match_count += 1

        elif isinstance(results, LookupError):
            if not cas_client:
                click.echo(f"ERROR: {results.error_code}")
            else:
                click.echo(f"  PubChem: ERROR: {results.error_code}")
            result_dict = {
                "pubchem_cid": "",
                "pubchem_inchikey": "",
                "pubchem_canonical_smiles": "",
                "pubchem_molecular_formula": "",
                "pubchem_iupac_name": "",
                "pubchem_title": "",
                "pubchem_error": f"{results.error_code}: {results.error_message}",
            }
            enriched.append({**ing, **result_dict, **cas_data})
            cache[name] = result_dict
            error_count += 1

    # Save caches
    if not no_cache:
        save_cache(cache_file, cache)
        click.echo(f"Saved {len(cache)} entries to PubChem cache: {cache_file}")
        if cas_client and cas_cache:
            save_cache(cas_cache_file, cas_cache)
            click.echo(f"Saved {len(cas_cache)} entries to CAS cache: {cas_cache_file}")

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    click.echo(f"\nWriting enriched data to: {output_file}")

    fieldnames = [
        "ingredient_uuid",
        "ingredient_name",
        "pubchem_cid",
        "pubchem_inchikey",
        "pubchem_canonical_smiles",
        "pubchem_molecular_formula",
        "pubchem_iupac_name",
        "pubchem_title",
        "pubchem_error",
        "cas_rn",
        "cas_name",
        "cas_inchi",
        "cas_inchikey",
        "cas_smiles",
        "cas_is_mixture",
        "cas_error",
    ]

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched)

    # Summary
    click.echo()
    click.echo("Summary:")
    click.echo(f"  Ingredients queried: {len(ingredients)}")
    click.echo(f"  Success:             {success_count}")
    click.echo(f"  Errors:              {error_count}")
    click.echo(f"  Multi-match:         {multi_match_count}")
    click.echo(f"  Cache hits:          {cache_hit_count}")
    click.echo(f"  Output rows:         {len(enriched)}")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
