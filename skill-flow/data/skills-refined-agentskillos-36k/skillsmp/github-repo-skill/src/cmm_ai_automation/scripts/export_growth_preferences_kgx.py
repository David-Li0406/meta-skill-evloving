#!/usr/bin/env python3
"""Export growth preference edges to KGX JSON Lines format.

Reads growth preferences from a TSV file, links them to grounded media nodes
using the Hybrid Media TSV as a lookup, and exports KGX edges.

Usage:
    uv run python -m cmm_ai_automation.scripts.export_growth_preferences_kgx \
        --input "/home/mark/Downloads/BER-CMM-data-for-AI-normalized - growth_preferences.tsv" \
        --media-tsv output/kgx/cmm_grounded_media_hybrid.tsv
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import click

from cmm_ai_automation.transform.growth_preference_transform import (
    extract_placeholder_id,
    transform_preference_row,
)
from cmm_ai_automation.transform.writer import write_kgx_jsonl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "kgx"


def load_media_mapping(media_tsv: Path) -> dict[str, str]:
    """
    Build a mapping from placeholder IDs to grounded IDs.

    Reads the Hybrid TSV and maps e.g. '0000001' -> 'BER-CMM-MEDIUM:0000001'
    """
    mapping: dict[str, str] = {}
    if not media_tsv.exists():
        logger.error(f"Media hybrid TSV not found: {media_tsv}")
        return mapping

    with media_tsv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            # We need to find the placeholder ID from the original data
            # The hybrid TSV contains 'placeholder URI' column
            uri = row.get("placeholder URI", "").strip()
            placeholder = extract_placeholder_id(uri)
            grounded_id = row.get("grounded_id", "").strip()

            if placeholder and grounded_id:
                mapping[placeholder] = grounded_id

    logger.info(f"Loaded {len(mapping)} media mappings from {media_tsv}")
    return mapping


@click.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the growth_preferences.tsv file",
)
@click.option(
    "--media-tsv",
    "-m",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the grounded media hybrid TSV",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=DEFAULT_OUTPUT_DIR,
    help="Output directory for KGX files",
)
@click.option(
    "--basename",
    "-b",
    type=str,
    default="cmm_growth_preferences",
    help="Base name for output files",
)
def main(
    input: Path,
    media_tsv: Path,
    output: Path,
    basename: str,
) -> None:
    """Export growth preference edges from TSV to KGX."""
    logger.info("=== Growth Preferences → KGX Export ===")

    # 1. Load Mappings
    media_map = load_media_mapping(media_tsv)
    if not media_map:
        raise click.Abort()

    all_edges = []
    stats = {"total": 0, "exported": 0}

    # 2. Process TSV
    with input.open(newline="", encoding="utf-8") as f:
        # Sniff delimiter
        sample = f.read(2048)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        if dialect.delimiter not in ["\t", ","]:
            dialect.delimiter = "\t"

        reader = csv.DictReader(f, dialect=dialect)

        for row in reader:
            stats["total"] += 1
            try:
                edge = transform_preference_row(row, media_map)
                if edge:
                    all_edges.append(edge)
                    stats["exported"] += 1
            except Exception as e:
                logger.warning(f"Failed to process row {stats['total']}: {e}")

    logger.info(f"Processed {stats['total']} rows. Created {stats['exported']} edges.")

    # 3. Write KGX Output
    if all_edges:
        logger.info(f"Writing KGX output to {output}...")
        _, edges_file = write_kgx_jsonl(
            [],  # No nodes in this pass
            all_edges,
            output,
            basename,
            generate_ids=True,
        )
        logger.info(f"✅ Export complete! Edges: {edges_file}")
    else:
        logger.warning("No edges generated.")


if __name__ == "__main__":
    main()
