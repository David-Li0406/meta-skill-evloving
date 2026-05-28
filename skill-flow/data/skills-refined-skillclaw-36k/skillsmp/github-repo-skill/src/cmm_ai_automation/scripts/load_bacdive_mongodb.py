#!/usr/bin/env python3
"""Download BacDive strain data and load into MongoDB.

Primary approach: iterate over ID range 1 to max-id with batched fetches.
Fallback: SPARQL endpoint to discover IDs (often stale, use --use-sparql).

Usage:
    # Fetch all strains up to ID 200000 (default)
    uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb

    # Fetch with custom max ID
    uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb --max-id 180000

    # Use SPARQL discovery instead (may be stale)
    uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb --use-sparql

Options:
    --max-id N           Maximum BacDive ID to fetch (default: 200000)
    --min-id N           Minimum BacDive ID to fetch (default: 1)
    --batch-size N       IDs per API batch (default: 100)
    --database NAME      MongoDB database name (default: bacdive)
    --collection NAME    MongoDB collection name (default: strains)
    --use-sparql         Use SPARQL to discover IDs instead of range iteration
    --env-file PATH      Path to .env file with credentials
    --dry-run            Test without downloading
    --limit N            Limit number of IDs to fetch (for testing)
"""

import argparse
import logging
import os
import time
from typing import Any

import bacdive  # type: ignore[import-untyped]
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from tqdm import tqdm  # type: ignore[import-untyped]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

SPARQL_ENDPOINT = "https://sparql.dsmz.de/api/bacdive"
MONGODB_URI = "mongodb://localhost:27017"
DEFAULT_DATABASE = "bacdive"
DEFAULT_COLLECTION = "strains"
DEFAULT_MAX_ID = 200000
DEFAULT_MIN_ID = 1

# Rate limiting - be polite
REQUEST_DELAY = 0.1  # seconds between requests

# SPARQL prefixes
SPARQL_PREFIXES = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX d3o: <https://purl.dsmz.de/schema/>
PREFIX bd: <https://purl.dsmz.de/bacdive/>
"""


def sparql_query(query: str, max_retries: int = 3) -> list[dict[str, Any]]:
    """Execute a SPARQL query and return results.

    Args:
        query: SPARQL query string
        max_retries: Number of retries on failure

    Returns:
        List of result bindings as dicts
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(
                SPARQL_ENDPOINT,
                params={"query": query},
                headers={"Accept": "application/sparql-results+json"},
                timeout=300,
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            results: dict[str, Any] = data.get("results", {})
            bindings: list[dict[str, Any]] = results.get("bindings", [])
            return bindings
        except (requests.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                logger.warning(f"SPARQL query failed (attempt {attempt + 1}): {e}")
                time.sleep(2**attempt)
            else:
                logger.error(f"SPARQL query failed after {max_retries} attempts: {e}")
                return []
    return []


def get_bacdive_ids_via_sparql() -> list[int]:
    """Get all valid BacDive IDs via SPARQL (may be stale).

    Returns:
        Sorted list of all BacDive strain IDs
    """
    logger.info("Fetching BacDive IDs via SPARQL (may be stale)...")

    query = f"""{SPARQL_PREFIXES}
SELECT ?bacdiveId
WHERE {{
  ?strain a d3o:Strain ;
          d3o:hasBacDiveID ?bacdiveId .
}}
ORDER BY ?bacdiveId
"""
    results = sparql_query(query)

    ids = []
    for row in results:
        try:
            ids.append(int(row["bacdiveId"]["value"]))
        except (KeyError, ValueError):
            continue

    logger.info(f"Found {len(ids):,} BacDive IDs via SPARQL")
    return sorted(ids)


def get_bacdive_ids_via_range(min_id: int, max_id: int) -> list[int]:
    """Generate list of BacDive IDs from a range.

    Args:
        min_id: Minimum ID (inclusive)
        max_id: Maximum ID (inclusive)

    Returns:
        List of IDs in range
    """
    ids = list(range(min_id, max_id + 1))
    logger.info(f"Generated {len(ids):,} IDs from range {min_id} to {max_id}")
    return ids


def load_bacdive_to_mongodb(
    client: bacdive.BacdiveClient,
    collection: Collection[dict[str, Any]],
    bacdive_ids: list[int],
    batch_size: int,
) -> tuple[int, int, int]:
    """Load BacDive entries into MongoDB using official bacdive package.

    Args:
        client: Authenticated BacDive client
        collection: MongoDB collection
        bacdive_ids: List of BacDive IDs to fetch
        batch_size: Number of IDs per batch

    Returns:
        Tuple of (total_fetched, total_stored, total_missing)
    """
    total_fetched = 0
    total_stored = 0
    total_missing = 0

    logger.info(f"Fetching {len(bacdive_ids):,} IDs in batches of {batch_size}")

    with tqdm(total=len(bacdive_ids), desc="Fetching strains") as pbar:
        for i in range(0, len(bacdive_ids), batch_size):
            batch_ids = bacdive_ids[i : i + batch_size]
            batch_found = 0

            try:
                # Build semicolon-separated ID string for API
                id_str = ";".join(str(bid) for bid in batch_ids)

                # Use do_api_call to fetch batch
                result = client.do_api_call(f"fetch/{id_str}")

                if not result or "results" not in result:
                    # Empty batch - all IDs in this batch don't exist (or API error)
                    logger.debug(f"Batch {batch_ids[0]}-{batch_ids[-1]}: no results returned")
                    total_missing += len(batch_ids)
                    pbar.update(len(batch_ids))
                    time.sleep(REQUEST_DELAY)
                    continue

                # Results is a dict keyed by ID
                results_dict = result["results"]

                for key, strain_data in results_dict.items():
                    if not isinstance(strain_data, dict):
                        continue

                    # Get BacDive ID from General section or use key
                    bacdive_id = None
                    if "General" in strain_data:
                        bacdive_id = strain_data["General"].get("BacDive-ID")
                    if bacdive_id is None:
                        # Fall back to key (which is the ID)
                        try:
                            bacdive_id = int(key)
                        except (ValueError, TypeError):
                            continue

                    total_fetched += 1
                    batch_found += 1

                    # Add bacdive_id at top level for compatibility
                    strain_data["bacdive_id"] = bacdive_id
                    # Use bacdive_id as MongoDB _id
                    strain_data["_id"] = bacdive_id

                    try:
                        collection.replace_one(
                            {"_id": bacdive_id},
                            strain_data,
                            upsert=True,
                        )
                        total_stored += 1
                    except Exception as e:
                        logger.warning(f"Failed to store BacDive {bacdive_id}: {e}")

                # Count missing IDs in this batch
                total_missing += len(batch_ids) - batch_found

            except Exception as e:
                logger.warning(f"Batch fetch failed for IDs {batch_ids[0]}-{batch_ids[-1]}: {e}")
                total_missing += len(batch_ids)

            pbar.update(len(batch_ids))
            time.sleep(REQUEST_DELAY)

    return total_fetched, total_stored, total_missing


def main() -> None:
    """Download BacDive strain data and load into MongoDB."""
    parser = argparse.ArgumentParser(
        description="Download BacDive strain data into MongoDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch all strains up to ID 200000
  uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb

  # Fetch only new strains (IDs 180000+)
  uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb --min-id 180000

  # Use different database/collection
  uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb --database mydb --collection mystrains
""",
    )
    parser.add_argument(
        "--max-id",
        type=int,
        default=DEFAULT_MAX_ID,
        help=f"Maximum BacDive ID to fetch (default: {DEFAULT_MAX_ID})",
    )
    parser.add_argument(
        "--min-id",
        type=int,
        default=DEFAULT_MIN_ID,
        help=f"Minimum BacDive ID to fetch (default: {DEFAULT_MIN_ID})",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="IDs per batch (default: 100)",
    )
    parser.add_argument(
        "--database",
        default=DEFAULT_DATABASE,
        help=f"MongoDB database name (default: {DEFAULT_DATABASE})",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help=f"MongoDB collection name (default: {DEFAULT_COLLECTION})",
    )
    parser.add_argument(
        "--use-sparql",
        action="store_true",
        help="Use SPARQL to discover IDs instead of range (may be stale)",
    )
    parser.add_argument(
        "--env-file",
        help="Path to .env file with credentials",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test without downloading",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of IDs to fetch (for testing)",
    )
    args = parser.parse_args()

    # Load environment
    if args.env_file:
        load_dotenv(args.env_file)
    else:
        load_dotenv()

    # Get credentials
    email = os.environ.get("BACDIVE_EMAIL")
    password = os.environ.get("BACDIVE_PASSWORD")

    if not email or not password:
        logger.error("BACDIVE_EMAIL and BACDIVE_PASSWORD must be set in environment or .env file")
        return

    # Step 1: Get IDs to fetch
    if args.use_sparql:
        all_ids = get_bacdive_ids_via_sparql()
        if not all_ids:
            logger.error("Failed to get BacDive IDs from SPARQL")
            return
    else:
        all_ids = get_bacdive_ids_via_range(args.min_id, args.max_id)

    # Apply limit if specified
    if args.limit:
        all_ids = all_ids[: args.limit]
        logger.info(f"Limited to {len(all_ids)} IDs")

    if args.dry_run:
        logger.info(f"[DRY RUN] Would fetch {len(all_ids):,} IDs")
        logger.info(f"  ID range: {min(all_ids)} to {max(all_ids)}")
        logger.info(f"  Database: {args.database}.{args.collection}")
        return

    # Step 2: Authenticate with BacDive using official package
    logger.info("Authenticating with BacDive...")
    try:
        bacdive_client = bacdive.BacdiveClient(email, password)
        logger.info("BacDive authentication successful")
    except Exception as e:
        logger.error(f"BacDive authentication failed: {e}")
        return

    # Step 3: Connect to MongoDB
    logger.info(f"Connecting to MongoDB {args.database}.{args.collection}...")
    mongo_client: MongoClient[dict[str, Any]] = MongoClient(MONGODB_URI)
    db = mongo_client[args.database]
    collection = db[args.collection]

    # Create indexes
    collection.create_index("bacdive_id")
    collection.create_index("General.species")
    collection.create_index("Name and taxonomic classification.species")
    collection.create_index("General.DSM-Number")

    # Get current count
    existing_count = collection.count_documents({})
    logger.info(f"Existing documents in MongoDB: {existing_count}")

    # Step 4: Fetch and store via official bacdive package
    total_fetched, total_stored, total_missing = load_bacdive_to_mongodb(
        client=bacdive_client,
        collection=collection,
        bacdive_ids=all_ids,
        batch_size=args.batch_size,
    )

    # Summary
    final_count = collection.count_documents({})
    logger.info("\n=== Summary ===")
    logger.info(f"  IDs attempted: {len(all_ids):,}")
    logger.info(f"  Strains found: {total_fetched:,}")
    logger.info(f"  Strains stored: {total_stored:,}")
    logger.info(f"  IDs missing (no data): {total_missing:,}")
    logger.info(f"  Final count in MongoDB: {final_count:,}")

    mongo_client.close()
    logger.info("Done!")


if __name__ == "__main__":
    main()
