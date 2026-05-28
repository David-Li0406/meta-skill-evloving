#!/usr/bin/env python3
"""Export grounded media nodes to KGX JSON Lines format and Hybrid TSV.

Reads growth media data from a TSV file, cleans encoding artifacts (Mojibake),
grounds names to established databases (MediaDive, TogoMedium), and exports:
1. Biolink-compliant KGX nodes (JSONL)
2. Enriched Hybrid TSV (Original data + Grounding columns)

Usage:
    uv run python -m cmm_ai_automation.scripts.export_grounded_media_kgx \
        -i "/home/mark/Downloads/BER-CMM-data-for-AI-normalized - growth_media.tsv"
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any

import chromadb
import click
from dotenv import load_dotenv
from pymongo import MongoClient

from cmm_ai_automation.transform.growth_media_transform import (
    MediaGrounder,
    transform_media_row,
)
from cmm_ai_automation.transform.writer import write_kgx_jsonl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_TOGOMEDIUM = DATA_DIR / "chroma_togomedium"
CHROMA_MEDIADIVE = DATA_DIR / "chroma_mediadive"
MAPPINGS_FILE = DATA_DIR / "media_grounding_mappings.tsv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "kgx"
MONGODB_URI = "mongodb://localhost:27017/"


def load_manual_mappings(mapping_file: Path) -> dict[str, dict]:
    """Load manual grounding mappings from TSV."""
    mappings: dict[str, dict] = {}
    if not mapping_file.exists():
        logger.warning(f"Mapping file not found: {mapping_file}")
        return mappings

    with mapping_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            sheet_medium = row.get("sheet_medium", "").strip().lower()
            if not sheet_medium:
                continue

            mappings[sheet_medium] = {
                "source": row.get("target_system", "").strip(),
                "id": row.get("target_id", "").strip(),
                "confidence": float(row.get("confidence", 0.0)),
                "match_type": row.get("match_type", ""),
            }
    logger.info(f"Loaded {len(mappings)} manual mappings")
    return mappings


def get_chroma_collection(path: Path, name: str) -> Any:
    """Get ChromaDB collection if it exists."""
    if not path.exists():
        return None
    try:
        client = chromadb.PersistentClient(path=str(path))
        return client.get_collection(name)
    except Exception as e:
        logger.warning(f"Failed to load collection {name} from {path}: {e}")
        return None


@click.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the growth_media.tsv file",
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
    default="cmm_grounded_media",
    help="Base name for output files (without extension)",
)
def main(
    input: Path,
    output: Path,
    basename: str,
) -> None:
    """Export grounded media nodes from TSV to KGX and Hybrid TSV."""
    logger.info("=== Grounded Media → KGX Export ===")
    logger.info(f"Input: {input}")

    # Initialize resources
    logger.info("Connecting to MongoDB...")
    mongo_client = MongoClient(MONGODB_URI)
    mediadive_db = mongo_client["mediadive"]

    logger.info("Loading ChromaDB indices...")
    togo_col = get_chroma_collection(CHROMA_TOGOMEDIUM, "togomedium_media")
    dive_col = get_chroma_collection(CHROMA_MEDIADIVE, "mediadive_media")

    logger.info("Loading manual mappings...")
    mappings = load_manual_mappings(MAPPINGS_FILE)

    # Initialize Grounder (No local registry file anymore)
    grounder = MediaGrounder(
        local_registry={},  # Empty registry
        manual_mappings=mappings,
        mongo_db=mediadive_db,
        togo_collection=togo_col,
        dive_collection=dive_col,
    )

    all_nodes = []
    hybrid_rows = []
    stats = {"total": 0, "mojibake_fixed": 0}

    # Process TSV
    with input.open(newline="", encoding="utf-8") as f:
        # Detect delimiter
        sample = f.read(1024)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        if dialect.delimiter not in ["\t", ","]:
            dialect.delimiter = "\t"

        reader = csv.DictReader(f, dialect=dialect)

        for row in reader:
            stats["total"] += 1
            original_name = row.get("media_name", "").strip()

            try:
                node, hybrid_row = transform_media_row(row, grounder)

                if node.name != original_name:
                    stats["mojibake_fixed"] += 1

                all_nodes.append(node)
                hybrid_rows.append(hybrid_row)

            except Exception as e:
                logger.warning(f"Failed to process row {stats['total']} ({original_name}): {e}")

    logger.info(f"Processed {stats['total']} rows. Fixed {stats['mojibake_fixed']} mojibake issues.")

    # Write KGX Output
    logger.info(f"Writing KGX output to {output}...")
    nodes_file, _ = write_kgx_jsonl(
        all_nodes,
        [],  # No edges for now
        output,
        basename,
        deduplicate=True,
    )

    # Write Hybrid TSV
    hybrid_file = output / f"{basename}_hybrid.tsv"
    logger.info(f"Writing hybrid TSV to {hybrid_file}...")

    if hybrid_rows:
        fieldnames = hybrid_rows[0].keys()
        with hybrid_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(hybrid_rows)

    logger.info("✅ Export complete!")
    logger.info(f"  Nodes: {nodes_file}")
    logger.info(f"  Hybrid TSV: {hybrid_file}")


if __name__ == "__main__":
    main()
