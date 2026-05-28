#!/usr/bin/env python3
"""Download MediaDive data and load into MongoDB.

Downloads media, solutions, and ingredients from the MediaDive REST API
and inserts them as documents into a local MongoDB database.

Usage:
    uv run python -m cmm_ai_automation.scripts.load_mediadive_mongodb

Requires:
    - MongoDB running locally on default port (27017)
    - pymongo package
"""

import logging
from typing import Any

import requests
from pymongo import MongoClient
from pymongo.collection import Collection

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://mediadive.dsmz.de/rest"
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "mediadive"


def fetch_endpoint(endpoint: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Fetch data from a MediaDive API endpoint.

    Args:
        endpoint: API endpoint path (e.g., "media", "solutions")
        params: Optional query parameters

    Returns:
        List of data records from the API response
    """
    url = f"{BASE_URL}/{endpoint}"
    logger.info(f"Fetching {url}")

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != 200:
        raise RuntimeError(f"API error: {data.get('msg', 'Unknown error')}")

    count = data.get("count", 0)
    records: list[dict[str, Any]] = data.get("data", [])
    logger.info(f"  Retrieved {count} records")

    return records


def load_collection(
    collection: Collection[dict[str, Any]],
    records: list[dict[str, Any]],
    id_field: str = "id",
) -> None:
    """Load records into a MongoDB collection.

    Drops the existing collection and inserts all records fresh.

    Args:
        collection: MongoDB collection to load into
        records: List of records to insert
        id_field: Field to use as the document _id
    """
    collection_name = collection.name

    # Drop existing collection
    collection.drop()
    logger.info(f"  Dropped existing '{collection_name}' collection")

    if not records:
        logger.warning(f"  No records to insert into '{collection_name}'")
        return

    # Add _id field based on the original id
    documents = []
    for record in records:
        doc = record.copy()
        if id_field in doc:
            doc["_id"] = doc[id_field]
        documents.append(doc)

    # Insert all documents
    result = collection.insert_many(documents)
    logger.info(f"  Inserted {len(result.inserted_ids)} documents into '{collection_name}'")


def main() -> None:
    """Download MediaDive data and load into MongoDB."""
    logger.info("Connecting to MongoDB...")
    client: MongoClient[dict[str, Any]] = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    logger.info(f"Using database: {DATABASE_NAME}")

    # Fetch and load media
    logger.info("\n=== Media ===")
    media_records = fetch_endpoint("media")
    load_collection(db.media, media_records)

    # Fetch and load solutions (with all=1 to get all solutions)
    logger.info("\n=== Solutions ===")
    solutions_records = fetch_endpoint("solutions", params={"all": "1"})
    load_collection(db.solutions, solutions_records)

    # Fetch and load ingredients
    logger.info("\n=== Ingredients ===")
    ingredients_records = fetch_endpoint("ingredients")
    load_collection(db.ingredients, ingredients_records)

    # Fetch and store stats
    logger.info("\n=== Stats ===")
    stats_response = requests.get(f"{BASE_URL}/stats", timeout=30)
    stats_response.raise_for_status()
    stats_data = stats_response.json()
    if stats_data.get("status") == 200:
        db.stats.drop()
        db.stats.insert_one({"_id": "current", **stats_data.get("data", {})})
        logger.info("  Stored stats document")

    # Print summary
    logger.info("\n=== Summary ===")
    logger.info(f"  Media: {db.media.count_documents({})}")
    logger.info(f"  Solutions: {db.solutions.count_documents({})}")
    logger.info(f"  Ingredients: {db.ingredients.count_documents({})}")

    client.close()
    logger.info("\nDone!")


if __name__ == "__main__":
    main()
