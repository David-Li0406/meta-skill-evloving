#!/usr/bin/env python3
"""Download all tabs from BER CMM Google Sheet as TSV files.

Saves to data/private/ which is gitignored to protect private data.
"""

import re
from pathlib import Path

import click

from cmm_ai_automation.gsheets import get_sheet_data, list_worksheets


def sanitize_filename(name: str) -> str:
    r"""Replace whitespace and the characters / \ : * ? " < > | with underscores."""
    return re.sub(r"[\s/\\:*?\"<>|]", "_", name)


# Default output directory (gitignored)
# __file__ is src/cmm_ai_automation/scripts/download_sheets.py
# .parent x4 gets to project root
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "data" / "private"


@click.command()
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=DEFAULT_OUTPUT_DIR,
    help="Output directory for TSV files (default: data/private/)",
)
@click.option(
    "--spreadsheet",
    "-s",
    default="BER CMM Data for AI - for editing",
    help="Spreadsheet name or ID",
)
@click.option(
    "--tabs",
    "-t",
    multiple=True,
    help="Specific tab(s) to download. If not specified, downloads all tabs.",
)
def main(output_dir: Path, spreadsheet: str, tabs: tuple[str, ...]) -> None:
    """Download Google Sheet tabs as TSV files to data/private/."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get list of tabs to download
    all_tabs = list_worksheets(spreadsheet)
    tabs_to_download = list(tabs) if tabs else all_tabs

    click.echo(f"Spreadsheet: {spreadsheet}")
    click.echo(f"Output directory: {output_dir}")
    click.echo(f"Tabs to download: {len(tabs_to_download)}")
    click.echo()

    for tab_name in tabs_to_download:
        if tab_name not in all_tabs:
            click.echo(f"  SKIP: {tab_name} (not found)")
            continue

        safe_name = sanitize_filename(tab_name)
        output_file = output_dir / f"{safe_name}.tsv"
        try:
            df = get_sheet_data(spreadsheet, tab_name)
            df.to_csv(output_file, sep="\t", index=False)
            click.echo(f"  OK: {tab_name} ({len(df)} rows) -> {output_file.name}")
        except Exception as e:
            click.echo(f"  ERROR: {tab_name} - {e}")

    click.echo()
    click.echo(f"Done. Files saved to {output_dir}")


if __name__ == "__main__":
    main()
