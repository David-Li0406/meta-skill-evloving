#!/usr/bin/env python3
"""Test species search with synonym handling.

Usage:
    uv run python -m cmm_ai_automation.scripts.test_species_search_with_synonyms
    uv run python -m cmm_ai_automation.scripts.test_species_search_with_synonyms --species "Sinorhizobium meliloti"
"""

from __future__ import annotations

import click

from cmm_ai_automation.strains import get_bacdive_collection, search_species_with_synonyms

# Test cases: old names that have been reclassified
TEST_CASES = [
    # (search_name, expected_current_name)
    ("Sinorhizobium meliloti", "Ensifer meliloti"),
    ("Methylobacterium extorquens", "Methylorubrum extorquens"),
    ("Methylobrum nodulans", "Methylobacterium nodulans"),  # Typo variant
    ("Methylobacterium nodulans", "Methylobacterium nodulans"),  # Correct spelling
    ("Ensifer meliloti", "Ensifer meliloti"),  # Already current
    ("Methylorubrum extorquens", "Methylorubrum extorquens"),  # Already current
]


@click.command()
@click.option(
    "--species",
    "-s",
    type=str,
    help="Search for a specific species name",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed information",
)
def main(species: str | None, verbose: bool) -> None:
    """Test species search with synonym handling."""
    collection = get_bacdive_collection()
    if collection is None:
        click.echo("ERROR: Could not connect to BacDive MongoDB", err=True)
        raise SystemExit(1)

    if species:
        # Search for specific species
        click.echo("=" * 80)
        click.echo(f"Searching for: {species}")
        click.echo("=" * 80)
        click.echo()

        doc = search_species_with_synonyms(collection, species)

        if doc:
            click.secho("✓ FOUND", fg="green")
            print_species_info(doc, verbose)
        else:
            click.secho("✗ NOT FOUND", fg="red")

    else:
        # Run test cases
        click.echo("=" * 80)
        click.echo("Testing Species Search with Synonym Handling")
        click.echo("=" * 80)
        click.echo()

        found_count = 0
        failed = []

        for search_name, expected_name in TEST_CASES:
            doc = search_species_with_synonyms(collection, search_name)

            if doc:
                found_count += 1
                current_name = doc.get("Name and taxonomic classification", {}).get("species", "Unknown")

                is_synonym = search_name != current_name
                status_icon = "✓"
                status_color = "green"

                if expected_name and current_name != expected_name:
                    status_icon = "⚠"
                    status_color = "yellow"

                click.secho(f"{status_icon} {search_name:40} → FOUND", fg=status_color)
                click.echo(f"  Current name:     {current_name}")

                if is_synonym:
                    click.echo("  Match type:       synonym")
                else:
                    click.echo("  Match type:       current name")

                bacdive_id = doc.get("General", {}).get("BacDive-ID")
                dsm_number = doc.get("General", {}).get("DSM-Number", "N/A")
                click.echo(f"  BacDive ID:       {bacdive_id}")
                click.echo(f"  DSM Number:       {dsm_number}")

                if verbose:
                    # Show all synonyms
                    synonyms = []
                    lpsn = doc.get("Name and taxonomic classification", {}).get("LPSN", {})
                    syn_list = lpsn.get("synonyms", [])
                    if isinstance(syn_list, list):
                        for syn_entry in syn_list:
                            if isinstance(syn_entry, dict) and "synonym" in syn_entry:
                                synonyms.append(syn_entry["synonym"])

                    if synonyms:
                        click.echo(f"  All synonyms:     {', '.join(synonyms)}")

                click.echo()
            else:
                failed.append(search_name)
                click.secho(f"✗ {search_name:40} → NOT FOUND", fg="red")
                click.echo()

        click.echo("=" * 80)
        click.echo(f"Summary: {found_count}/{len(TEST_CASES)} found ({len(failed)} not found)")
        click.echo("=" * 80)

        if failed:
            click.echo()
            click.secho("Failed searches:", fg="red")
            for name in failed:
                click.echo(f"  - {name}")


def print_species_info(doc: dict, verbose: bool = False) -> None:
    """Print information about a species."""
    taxonomy = doc.get("Name and taxonomic classification", {})
    general = doc.get("General", {})
    lpsn = taxonomy.get("LPSN", {})

    click.echo(f"BacDive ID:       {general.get('BacDive-ID')}")
    click.echo(f"DSM Number:       {general.get('DSM-Number', 'N/A')}")
    click.echo(f"Current species:  {taxonomy.get('species', 'N/A')}")
    click.echo(f"LPSN species:     {lpsn.get('species', 'N/A')}")
    click.echo(f"Genus:            {taxonomy.get('genus', 'N/A')}")
    click.echo(f"Family:           {taxonomy.get('family', 'N/A')}")
    click.echo(f"Type strain:      {taxonomy.get('type strain', 'N/A')}")

    # NCBI taxon
    ncbi_tax = general.get("NCBI tax id", {})
    if isinstance(ncbi_tax, dict):
        ncbi_id = ncbi_tax.get("NCBI tax id", "N/A")
        matching = ncbi_tax.get("Matching level", "N/A")
        click.echo(f"NCBI Taxon:       {ncbi_id} ({matching})")

    # Synonyms
    synonyms = []
    syn_list = lpsn.get("synonyms", [])
    if isinstance(syn_list, list):
        for syn_entry in syn_list:
            if isinstance(syn_entry, dict) and "synonym" in syn_entry:
                synonyms.append(syn_entry["synonym"])

    if synonyms:
        click.echo(f"Synonyms:         {', '.join(synonyms)}")

    if verbose:
        click.echo()
        click.echo("Full scientific name:")
        click.echo(f"  {taxonomy.get('full scientific name', 'N/A')}")


if __name__ == "__main__":
    main()
