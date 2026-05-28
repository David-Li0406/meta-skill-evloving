#!/usr/bin/env python3
"""Validate sheet data against authoritative sources.

Cross-checks field values in sheets against NCBI, BacDive, and other
authoritative sources to detect data quality issues.

Usage:
    uv run python -m cmm_ai_automation.scripts.validate_sheets
    uv run python -m cmm_ai_automation.scripts.validate_sheets --sheet strains.tsv
    uv run python -m cmm_ai_automation.scripts.validate_sheets --all --verbose
    uv run python -m cmm_ai_automation.scripts.validate_sheets --row 3 --sheet strains.tsv
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import click

from cmm_ai_automation.validation import (
    export_validation_report,
    list_validated_sheets,
    print_validation_report,
    validate_all_sheets,
    validate_row,
    validate_sheet,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Default paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_SHEETS_DIR = PROJECT_ROOT / "data" / "private"


@click.command()
@click.option(
    "--sheets-dir",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_SHEETS_DIR,
    help="Directory containing sheet TSV files",
)
@click.option(
    "--sheet",
    "-s",
    type=str,
    default=None,
    help="Validate specific sheet (e.g., strains.tsv)",
)
@click.option(
    "--all",
    "validate_all",
    is_flag=True,
    help="Validate all sheets with defined schemas",
)
@click.option(
    "--row",
    "-r",
    type=int,
    default=None,
    help="Validate specific row number (requires --sheet)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Export report to JSON file",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Include INFO-level issues in output",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging",
)
def main(
    sheets_dir: Path,
    sheet: str | None,
    validate_all: bool,
    row: int | None,
    output: Path | None,
    verbose: bool,
    debug: bool,
) -> None:
    """Validate sheet data against authoritative sources.

    Checks field values in sheets against NCBI Taxonomy, BacDive, and other
    authoritative sources to detect:

    \b
    - Invalid/nonexistent IDs
    - Name-ID mismatches
    - Bogus cross-references (IDs for unrelated organisms)
    - Missing strain-level taxon IDs
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate a specific row
    if row is not None:
        if sheet is None:
            raise click.UsageError("--row requires --sheet")

        sheet_path = sheets_dir / sheet
        if not sheet_path.exists():
            raise click.UsageError(f"Sheet not found: {sheet_path}")

        # Read the specific row
        with sheet_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row_num, row_data in enumerate(reader, start=2):
                if row_num == row:
                    click.echo(f"Validating {sheet} row {row}:")
                    click.echo()

                    # Show row contents
                    for col, val in row_data.items():
                        if val:
                            display_val = val[:60] + "..." if len(val) > 60 else val
                            click.echo(f"  {col}: {display_val}")
                    click.echo()

                    # Validate
                    report = validate_row(row_data, sheet, row)
                    print_validation_report(report, verbose=verbose)
                    return

            raise click.UsageError(f"Row {row} not found in {sheet}")

    # Validate specific sheet
    elif sheet is not None:
        sheet_path = sheets_dir / sheet
        if not sheet_path.exists():
            raise click.UsageError(f"Sheet not found: {sheet_path}")

        click.echo(f"Validating {sheet}...")
        report = validate_sheet(sheet_path)
        print_validation_report(report, verbose=verbose)

    # Validate all sheets
    elif validate_all:
        click.echo(f"Validating all sheets in {sheets_dir}...")
        click.echo(f"Sheets with schemas: {', '.join(list_validated_sheets())}")
        click.echo()

        report = validate_all_sheets(sheets_dir)
        print_validation_report(report, verbose=verbose)

    # Default: show help
    else:
        click.echo("Specify --sheet, --all, or --row. Use --help for options.")
        click.echo()
        click.echo("Available sheets with validation schemas:")
        for s in list_validated_sheets():
            sheet_path = sheets_dir / s
            status = "found" if sheet_path.exists() else "not found"
            click.echo(f"  - {s} ({status})")
        return

    # Export if requested
    if output is not None:
        export_validation_report(report, output)
        click.echo(f"\nExported report to {output}")


if __name__ == "__main__":
    main()
