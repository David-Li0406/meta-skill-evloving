#!/usr/bin/env python3
"""Export BacDive strain data from MongoDB to KGX JSON Lines format.

Reads bacterial strain documents from BacDive MongoDB collection and transforms
them into Biolink Model-compliant KGX nodes and edges.

Output format: JSON Lines (least lossy KGX serialization)
- {basename}_nodes.jsonl - One node per line
- {basename}_edges.jsonl - One edge per line

Features:
- Automatic node deduplication (merges duplicate species taxonomy nodes)
- Deterministic edge ID generation (SHA256-based)
- Preserves all BacDive fields including custom properties
- Handles BacDive's heterogeneous JSON structure

Usage:
    # Export all strains
    uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx

    # Export first 100 strains (for testing)
    uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx --limit 100

    # Export random sample of 50 strains (diverse subset)
    uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx --sample 50

    # Export specific strains by BacDive ID
    uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx --ids 7142,7143,7152

    # Custom output directory
    uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx --output output/kgx

    # Disable deduplication
    uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx --no-deduplicate
"""

from __future__ import annotations

import logging
from pathlib import Path

import click
from dotenv import load_dotenv

from cmm_ai_automation.strains.bacdive import get_bacdive_collection
from cmm_ai_automation.transform import (
    flatten_results,
    query_all_strains,
    query_bacdive_by_ids,
    query_random_sample,
    write_kgx_jsonl,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Default paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "kgx" / "bacdive"
DEFAULT_BASENAME = "cmm_strains_bacdive"


@click.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=DEFAULT_OUTPUT_DIR,
    help="Output directory for KGX JSON Lines files",
)
@click.option(
    "--basename",
    "-b",
    type=str,
    default=DEFAULT_BASENAME,
    help="Base name for output files (without extension)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=None,
    help="Maximum number of strains to process (for testing)",
)
@click.option(
    "--sample",
    "-s",
    type=int,
    default=None,
    help="Random sample of N strains (mutually exclusive with --limit and --ids)",
)
@click.option(
    "--ids",
    type=str,
    default=None,
    help="Comma-separated list of BacDive IDs to export (e.g., '7142,7143,7152')",
)
@click.option(
    "--no-deduplicate",
    is_flag=True,
    help="Disable node deduplication (keeps duplicate species nodes)",
)
@click.option(
    "--no-generate-ids",
    is_flag=True,
    help="Disable automatic edge ID generation",
)
@click.option(
    "--database",
    type=str,
    default=None,
    help="MongoDB database name (default: bacdive)",
)
@click.option(
    "--collection",
    type=str,
    default=None,
    help="MongoDB collection name (default: strains)",
)
def main(
    output: Path,
    basename: str,
    limit: int | None,
    sample: int | None,
    ids: str | None,
    no_deduplicate: bool,
    no_generate_ids: bool,
    database: str | None,
    collection: str | None,
) -> None:
    """Export BacDive strains from MongoDB to KGX JSON Lines."""
    logger.info("=== BacDive → KGX Export ===")

    # Validate mutually exclusive options
    exclusive_count = sum([bool(limit), bool(sample), bool(ids)])
    if exclusive_count > 1:
        logger.error("Options --limit, --sample, and --ids are mutually exclusive. Please specify only one.")
        return

    # Connect to MongoDB
    db_name = database or "bacdive"
    coll_name = collection or "strains"
    logger.info(f"Connecting to BacDive MongoDB ({db_name}.{coll_name})...")
    mongo_collection = get_bacdive_collection(database=database, collection=collection)

    if mongo_collection is None:
        logger.error("Failed to connect to MongoDB. Check MONGODB_URI environment variable.")
        return

    # Query strains
    if ids:
        # Parse comma-separated IDs
        bacdive_ids = [int(id_str.strip()) for id_str in ids.split(",")]
        logger.info(f"Querying {len(bacdive_ids)} specific BacDive IDs: {bacdive_ids}")
        results = query_bacdive_by_ids(mongo_collection, bacdive_ids)
    elif sample:
        # Random sample
        logger.info(f"Sampling {sample} random BacDive strains...")
        results = query_random_sample(mongo_collection, sample_size=sample)
    else:
        # Query all or limited
        if limit:
            logger.info(f"Querying first {limit} BacDive strains...")
        else:
            logger.info("Querying ALL BacDive strains...")
        results = query_all_strains(mongo_collection, limit=limit)

    if not results:
        logger.warning("No strains found in MongoDB")
        return

    logger.info(f"Found {len(results)} strain documents")

    # Flatten results
    logger.info("Transforming to KGX...")
    all_nodes, all_edges = flatten_results(results)

    logger.info(f"Generated {len(all_nodes)} nodes and {len(all_edges)} edges (before deduplication)")

    # Write to JSON Lines
    logger.info(f"Writing to {output / basename}_*.jsonl")
    nodes_file, edges_file = write_kgx_jsonl(
        all_nodes,
        all_edges,
        output,
        basename,
        deduplicate=not no_deduplicate,
        generate_ids=not no_generate_ids,
    )

    logger.info("✅ Export complete!")
    logger.info(f"  Nodes: {nodes_file}")
    logger.info(f"  Edges: {edges_file}")


if __name__ == "__main__":
    main()
