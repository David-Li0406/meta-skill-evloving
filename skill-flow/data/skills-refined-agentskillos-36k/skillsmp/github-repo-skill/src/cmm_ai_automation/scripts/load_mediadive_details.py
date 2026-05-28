#!/usr/bin/env python3
"""Fetch MediaDive detail endpoints and load into MongoDB.

Iterates through media, solutions, and ingredients collections to fetch
detailed information from the detail endpoints, then collects unique strains.

Detail endpoints:
- /medium/:id - Full medium recipe with solutions and steps
- /medium-composition/:id - Flattened ingredient composition
- /medium-strains/:id - Strains that grow on this medium
- /solution/:id - Solution recipe details
- /ingredient/:id - Ingredient details with synonyms, media usage

Usage:
    uv run python -m cmm_ai_automation.scripts.load_mediadive_details

Options:
    --skip-media       Skip fetching medium details
    --skip-solutions   Skip fetching solution details
    --skip-ingredients Skip fetching ingredient details
    --skip-strains     Skip fetching strain details
    --limit N          Only fetch first N items per collection (for testing)
"""

import argparse
import logging
import time
from typing import Any

import requests
from pymongo import MongoClient
from pymongo.collection import Collection

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://mediadive.dsmz.de/rest"
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "mediadive"

# Rate limiting - be conservative
REQUEST_DELAY = 0.1  # seconds between requests


def fetch_detail(endpoint: str) -> dict[str, Any] | None:
    """Fetch a single detail record from the API.

    Args:
        endpoint: API endpoint path (e.g., "medium/1")

    Returns:
        Data dict from API response, or None if not found
    """
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == 404:
            return None

        if data.get("status") != 200:
            logger.warning(f"API error for {endpoint}: {data.get('msg')}")
            return None

        detail_data: dict[str, Any] | None = data.get("data")
        return detail_data

    except requests.RequestException as e:
        logger.warning(f"Request failed for {endpoint}: {e}")
        return None


def fetch_and_store_details(
    source_collection: Collection[dict[str, Any]],
    target_collection: Collection[dict[str, Any]],
    endpoint_template: str,
    id_field: str = "id",
    limit: int | None = None,
) -> int:
    """Fetch details for all items in source collection and store in target.

    Args:
        source_collection: Collection containing IDs to fetch
        target_collection: Collection to store detailed records
        endpoint_template: Endpoint pattern with {id} placeholder
        id_field: Field name containing the ID in source documents
        limit: Optional limit on number of items to fetch

    Returns:
        Number of records successfully fetched
    """
    # Get all IDs from source collection
    cursor = source_collection.find({}, {id_field: 1})
    if limit:
        cursor = cursor.limit(limit)

    ids = [doc[id_field] for doc in cursor if id_field in doc]
    total = len(ids)

    logger.info(f"Fetching {total} records from {endpoint_template}...")

    # Drop and recreate target collection
    target_collection.drop()

    success_count = 0
    for i, item_id in enumerate(ids):
        if i > 0 and i % 100 == 0:
            logger.info(f"  Progress: {i}/{total} ({success_count} successful)")

        endpoint = endpoint_template.format(id=item_id)
        data = fetch_detail(endpoint)

        if data:
            # Add _id for MongoDB
            doc = data.copy() if isinstance(data, dict) else {"data": data}
            doc["_id"] = item_id
            target_collection.insert_one(doc)
            success_count += 1

        time.sleep(REQUEST_DELAY)

    logger.info(f"  Completed: {success_count}/{total} records fetched")
    return success_count


def fetch_medium_strains_and_collect(
    db: Any,
    limit: int | None = None,
) -> set[int]:
    """Fetch medium-strains for all media and collect unique strain IDs.

    Args:
        db: MongoDB database
        limit: Optional limit on number of media to process

    Returns:
        Set of unique strain IDs found
    """
    cursor = db.media.find({}, {"id": 1})
    if limit:
        cursor = cursor.limit(limit)

    media_ids = [doc["id"] for doc in cursor if "id" in doc]
    total = len(media_ids)

    logger.info(f"Fetching medium-strains for {total} media...")

    # Drop and recreate collection
    db.medium_strains.drop()

    strain_ids: set[int] = set()
    success_count = 0

    for i, medium_id in enumerate(media_ids):
        if i > 0 and i % 100 == 0:
            logger.info(f"  Progress: {i}/{total} ({len(strain_ids)} unique strains)")

        endpoint = f"medium-strains/{medium_id}"
        data = fetch_detail(endpoint)

        if data:
            # Store the medium-strains mapping
            doc = {"_id": medium_id, "strains": data}
            db.medium_strains.insert_one(doc)
            success_count += 1

            # Collect strain IDs
            if isinstance(data, list):
                for strain in data:
                    if isinstance(strain, dict) and "id" in strain:
                        strain_ids.add(strain["id"])

        time.sleep(REQUEST_DELAY)

    logger.info(f"  Completed: {success_count}/{total} media processed")
    logger.info(f"  Found {len(strain_ids)} unique strains")
    return strain_ids


def fetch_strains_by_id(
    db: Any,
    strain_ids: set[int],
    limit: int | None = None,
) -> int:
    """Fetch strain details by internal ID.

    Args:
        db: MongoDB database
        strain_ids: Set of strain IDs to fetch
        limit: Optional limit on number to fetch

    Returns:
        Number of strains successfully fetched
    """
    ids_list = sorted(strain_ids)
    if limit:
        ids_list = ids_list[:limit]

    total = len(ids_list)
    logger.info(f"Fetching {total} strain details...")

    # Drop and recreate collection
    db.strains.drop()

    success_count = 0
    for i, strain_id in enumerate(ids_list):
        if i > 0 and i % 100 == 0:
            logger.info(f"  Progress: {i}/{total} ({success_count} successful)")

        endpoint = f"strain/id/{strain_id}"
        data = fetch_detail(endpoint)

        if data:
            doc = data.copy() if isinstance(data, dict) else {"data": data}
            doc["_id"] = strain_id
            db.strains.insert_one(doc)
            success_count += 1

        time.sleep(REQUEST_DELAY)

    logger.info(f"  Completed: {success_count}/{total} strains fetched")
    return success_count


def main() -> None:
    """Fetch MediaDive detail endpoints and load into MongoDB."""
    parser = argparse.ArgumentParser(description="Fetch MediaDive details into MongoDB")
    parser.add_argument("--skip-media", action="store_true", help="Skip medium details")
    parser.add_argument("--skip-solutions", action="store_true", help="Skip solution details")
    parser.add_argument("--skip-ingredients", action="store_true", help="Skip ingredient details")
    parser.add_argument("--skip-strains", action="store_true", help="Skip strain details")
    parser.add_argument("--limit", type=int, help="Limit items per collection (for testing)")
    args = parser.parse_args()

    logger.info("Connecting to MongoDB...")
    client: MongoClient[dict[str, Any]] = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    # Check that base collections exist
    if db.media.count_documents({}) == 0:
        logger.error("No media in database. Run load_mediadive_mongodb.py first.")
        return

    # Fetch medium details (recipe with solutions)
    if not args.skip_media:
        logger.info("\n=== Medium Details ===")
        fetch_and_store_details(
            db.media,
            db.media_details,
            "medium/{id}",
            limit=args.limit,
        )

        logger.info("\n=== Medium Compositions ===")
        fetch_and_store_details(
            db.media,
            db.medium_compositions,
            "medium-composition/{id}",
            limit=args.limit,
        )

    # Fetch solution details
    if not args.skip_solutions:
        logger.info("\n=== Solution Details ===")
        fetch_and_store_details(
            db.solutions,
            db.solution_details,
            "solution/{id}",
            limit=args.limit,
        )

    # Fetch ingredient details
    if not args.skip_ingredients:
        logger.info("\n=== Ingredient Details ===")
        fetch_and_store_details(
            db.ingredients,
            db.ingredient_details,
            "ingredient/{id}",
            limit=args.limit,
        )

    # Fetch strains via medium-strains endpoint, then fetch strain details
    if not args.skip_strains:
        logger.info("\n=== Medium Strains ===")
        strain_ids = fetch_medium_strains_and_collect(db, limit=args.limit)

        logger.info("\n=== Strain Details ===")
        fetch_strains_by_id(db, strain_ids, limit=args.limit)

    # Print summary
    logger.info("\n=== Summary ===")
    for coll_name in [
        "media_details",
        "medium_compositions",
        "medium_strains",
        "solution_details",
        "ingredient_details",
        "strains",
    ]:
        count = db[coll_name].count_documents({})
        logger.info(f"  {coll_name}: {count}")

    client.close()
    logger.info("\nDone!")


if __name__ == "__main__":
    main()
