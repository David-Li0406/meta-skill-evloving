#!/usr/bin/env python3
"""Test and demonstrate culture collection search functionality.

Usage:
    uv run python -m cmm_ai_automation.scripts.test_culture_collection_search
    uv run python -m cmm_ai_automation.scripts.test_culture_collection_search --id "DSM:1337"
    uv run python -m cmm_ai_automation.scripts.test_culture_collection_search --all
"""

from __future__ import annotations

from typing import Any

import click
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from cmm_ai_automation.strains.culture_collection import (
    batch_search_culture_collections,
    reconcile_culture_collection_id,
)

# Test IDs from strains.tsv
TEST_IDS = [
    "DSM:1337",  # Should find Methylorubrum extorquens AM1
    "DSM:1338",  # Should find Methylorubrum extorquens (different strain)
    "ATCC:43883",  # Should find Methylorubrum zatmanii
    "ATCC:47054",  # Should find Pseudomonas putida KT2440
    "NCIMB:13946",  # May not be found
    "INVALID:99999",  # Should not be found
]


def get_bacdive_collection() -> Any:
    """Connect to BacDive MongoDB."""
    try:
        client: MongoClient = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        return client["bacdive"]["strains"]
    except ConnectionFailure as e:
        click.echo(f"ERROR: Could not connect to MongoDB: {e}", err=True)
        raise SystemExit(1) from e


def print_reconciliation_result(result: dict[str, Any]) -> None:
    """Pretty-print reconciliation result."""
    cc_id = str(result["input_id"])

    if result["found"]:
        click.secho(f"✓ {cc_id:20} → FOUND", fg="green")
        click.echo(f"  Search method:   {result['search_method']}")
        click.echo(f"  BacDive ID:      {result['bacdive_id']}")
        click.echo(f"  DSM Number:      {result['dsm_number'] or 'N/A'}")
        click.echo(f"  NCBI Taxon:      {result['ncbi_taxon_id'] or 'N/A'}")
        click.echo(f"  Species:         {result['species'] or 'Unknown'}")
        click.echo(f"  Designation:     {result['strain_designation'] or 'N/A'}")

        # Show first 5 culture collection IDs
        all_cc = result["all_culture_collections"]
        if all_cc:
            cc_display = ", ".join(all_cc[:5])
            if len(all_cc) > 5:
                cc_display += f" ... (+{len(all_cc) - 5} more)"
            click.echo(f"  All CC IDs:      {cc_display}")
        click.echo()
    else:
        click.secho(f"✗ {cc_id:20} → NOT FOUND", fg="red")
        click.echo()


@click.command()
@click.option(
    "--id",
    "single_id",
    type=str,
    help="Search for a single culture collection ID",
)
@click.option(
    "--all",
    "test_all",
    is_flag=True,
    help="Test all predefined IDs",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show full document",
)
def main(single_id: str | None, test_all: bool, verbose: bool) -> None:
    """Test culture collection search functionality."""
    # Connect to MongoDB
    try:
        from cmm_ai_automation.strains.bacdive import get_bacdive_collection

        collection = get_bacdive_collection()
        if collection is None:
            click.echo("ERROR: Could not connect to MongoDB", err=True)
            raise SystemExit(1)
    except Exception as e:
        click.echo(f"ERROR: {e}", err=True)
        raise SystemExit(1) from e

    if single_id:
        # Search for single ID
        click.echo("=" * 80)
        click.echo(f"Searching for: {single_id}")
        click.echo("=" * 80)
        click.echo()

        result = reconcile_culture_collection_id(collection, single_id)
        print_reconciliation_result(result)

        if verbose and result["document"]:
            import json

            click.echo("Full document:")
            click.echo(json.dumps(result["document"], indent=2, default=str))

    elif test_all:
        # Test all predefined IDs
        click.echo("=" * 80)
        click.echo("Testing Culture Collection Search")
        click.echo("=" * 80)
        click.echo()

        found_count = 0
        for cc_id in TEST_IDS:
            result = reconcile_culture_collection_id(collection, cc_id)
            print_reconciliation_result(result)
            if result["found"]:
                found_count += 1

        click.echo("=" * 80)
        click.echo(f"Summary: {found_count}/{len(TEST_IDS)} found ({len(TEST_IDS) - found_count} not found)")
        click.echo("=" * 80)

    else:
        # Default: demonstrate key functionality
        click.echo("=" * 80)
        click.echo("Culture Collection Search Demo")
        click.echo("=" * 80)
        click.echo()

        # Test 1: DSM:1337 (should use DSM-Number field)
        click.echo("Test 1: DSM:1337 (fast path via DSM-Number field)")
        result = reconcile_culture_collection_id(collection, "DSM:1337")
        print_reconciliation_result(result)

        # Test 2: ATCC:43883 (should use aggregation)
        click.echo("Test 2: ATCC:43883 (aggregation with word boundaries)")
        result = reconcile_culture_collection_id(collection, "ATCC:43883")
        print_reconciliation_result(result)

        # Test 3: Not found
        click.echo("Test 3: INVALID:99999 (should not be found)")
        result = reconcile_culture_collection_id(collection, "INVALID:99999")
        print_reconciliation_result(result)

        # Test 4: Batch search
        click.echo("Test 4: Batch search")
        batch_ids = ["DSM:1337", "ATCC:43883", "NCIMB:13946"]
        results = batch_search_culture_collections(collection, batch_ids)
        for cc_id, doc in results.items():
            if doc:
                bacdive_id = doc.get("General", {}).get("BacDive-ID")
                click.echo(f"  ✓ {cc_id:20} → BacDive:{bacdive_id}")
            else:
                click.echo(f"  ✗ {cc_id:20} → NOT FOUND")
        click.echo()

        click.echo("Use --help to see all options")


if __name__ == "__main__":
    main()
