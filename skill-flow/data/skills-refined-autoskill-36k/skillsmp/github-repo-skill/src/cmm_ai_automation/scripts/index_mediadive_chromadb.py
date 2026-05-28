#!/usr/bin/env python3
"""Index MediaDive MongoDB data into ChromaDB for fuzzy/semantic search.

Creates lightweight searchable indexes of MediaDive data from MongoDB:
- mediadive_media: Media/solution names and alternative names
- mediadive_ingredients: Ingredient names, synonyms, chemical IDs
- mediadive_strains: Strain species and culture collection numbers

Usage:
    uv run python -m cmm_ai_automation.scripts.index_mediadive_chromadb
    uv run python -m cmm_ai_automation.scripts.index_mediadive_chromadb --test
"""

import logging
import re

import chromadb
import click
from pymongo import MongoClient
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

CHROMA_PATH = "data/chroma_mediadive"
MONGODB_URI = "mongodb://localhost:27017/"

# Test cases derived from Google Sheet TSVs
TEST_CASES = {
    "media": [
        # (query, expected_matches_substrings, description)
        ("LB medium", ["luria", "lysogeny", "lennox"], "LB alternative names"),
        ("Luria broth", ["lb", "luria"], "Luria broth -> LB"),
        ("AMS", ["ammonium mineral salts", "ams"], "AMS medium"),
        ("nitrate mineral salts", ["nms"], "NMS medium"),
        ("R2A", ["reasoner", "r2a"], "R2A medium"),
        ("PIPES minimal", ["pipes", "methylotroph"], "PIPES buffered medium"),
    ],
    "ingredients": [
        ("magnesium sulfate", ["magnesium", "sulfate"], "Magnesium sulfate search"),
        ("MgSO4", ["magnesium", "sulfate"], "MgSO4 formula search"),
        ("methanol", ["methanol", "ch3oh"], "Methanol search"),
        ("agar", ["agar"], "Agar search"),
        ("PIPES buffer", ["pipes"], "PIPES buffer search"),
        ("yeast extract", ["yeast"], "Yeast extract search"),
        ("glucose", ["glucose"], "Glucose search"),
        ("CHEBI:17790", ["methanol"], "ChEBI ID search"),
    ],
    "strains": [
        ("Methylobacterium extorquens", ["methylo", "extorquens"], "M. extorquens"),
        ("DSM 1", ["dsm"], "DSM culture collection"),
        ("ATCC", ["atcc"], "ATCC culture collection"),
        ("Pseudomonas", ["pseudomonas"], "Pseudomonas genus"),
        ("Paracoccus denitrificans", ["paracoccus", "denitrificans"], "P. denitrificans"),
    ],
}


def flatten_solution_doc(doc: dict, details: dict | None = None) -> tuple[str, dict]:
    """Flatten solution document for ChromaDB indexing.

    Combines basic solution data with optional details.
    Returns (searchable_text, metadata).
    """
    parts = []
    metadata = {}

    # Get solution ID (could be numeric or string like "J22", "1011a")
    solution_id = doc.get("id") or doc.get("_id", "")
    metadata["mediadive_id"] = str(solution_id)

    # Get name
    name = doc.get("name", "")
    if name:
        parts.append(f"Medium: {name}")
        metadata["name"] = name

    # Add details if available
    if details:
        # Sometimes details has alternative name info in description or elsewhere
        desc = details.get("description", "")
        if desc:
            parts.append(f"Description: {desc}")

    searchable_text = "\n".join(parts)
    return searchable_text, metadata


def flatten_ingredient_doc(doc: dict) -> tuple[str, dict]:
    """Flatten ingredient document for ChromaDB indexing.

    Returns (searchable_text, metadata).
    """
    parts = []
    metadata = {}

    # Ingredient name
    name = doc.get("name", "")
    if name:
        parts.append(f"Ingredient: {name}")
        metadata["name"] = name

    # Chemical identifiers
    chebi = doc.get("ChEBI", "")
    if chebi:
        parts.append(f"ChEBI: {chebi}")
        metadata["chebi"] = chebi

    cas_rn = doc.get("CAS-RN", "")
    if cas_rn:
        parts.append(f"CAS-RN: {cas_rn}")
        metadata["cas_rn"] = cas_rn

    pubchem = doc.get("PubChem", "")
    if pubchem:
        parts.append(f"PubChem: {pubchem}")
        metadata["pubchem"] = str(pubchem)

    # Synonyms
    synonyms = doc.get("synonyms", [])
    if synonyms:
        syn_text = "; ".join(str(s) for s in synonyms if s) if isinstance(synonyms, list) else str(synonyms)
        if syn_text:
            parts.append(f"Synonyms: {syn_text}")
            metadata["synonyms"] = syn_text

    # Chemical formula (if present)
    formula = doc.get("formula", "")
    if formula:
        parts.append(f"Formula: {formula}")
        metadata["formula"] = formula

    searchable_text = "\n".join(parts)
    return searchable_text, metadata


def flatten_strain_doc(doc: dict) -> tuple[str, dict]:
    """Flatten strain document for ChromaDB indexing.

    Returns (searchable_text, metadata).
    """
    parts = []
    metadata = {}

    # Strain ID
    strain_id = doc.get("id") or doc.get("_id", "")
    metadata["mediadive_id"] = str(strain_id)

    # Species
    species = doc.get("species", "")
    if species:
        parts.append(f"Species: {species}")
        metadata["species"] = species

    # Culture collection number (key for BacDive linking)
    ccno = doc.get("ccno", "")
    if ccno:
        parts.append(f"Culture collection: {ccno}")
        metadata["ccno"] = ccno
        # Extract collection prefix (e.g., "DSM", "ATCC")
        match = re.match(r"([A-Za-z]+)", ccno)
        if match:
            metadata["collection_prefix"] = match.group(1).upper()

    searchable_text = "\n".join(parts)
    return searchable_text, metadata


def index_media(mongo_client: MongoClient, chroma_client, clear: bool = False) -> int:
    """Index media/solutions into ChromaDB."""
    logger.info("\n" + "=" * 50)
    logger.info("Indexing MediaDive Media/Solutions")
    logger.info("=" * 50)

    db = mongo_client["mediadive"]
    solutions = db["solutions"]
    solution_details = db["solution_details"]

    collection_name = "mediadive_media"

    if clear:
        try:
            chroma_client.delete_collection(collection_name)
            logger.info(f"Cleared existing collection '{collection_name}'")
        except Exception:
            # Collection may not exist yet; proceed with indexing
            pass

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "MediaDive media/solutions for semantic search"},
    )

    # Build details lookup
    details_by_id = {}
    for doc in solution_details.find({}):
        doc_id = doc.get("id") or doc.get("_id", "")
        details_by_id[str(doc_id)] = doc

    # Batch index solutions
    batch_ids = []
    batch_docs = []
    batch_metas = []
    batch_size = 500
    indexed = 0

    total = solutions.count_documents({})
    for doc in tqdm(solutions.find({}), total=total, desc="Media"):
        sol_id = doc.get("id") or doc.get("_id", "")
        if not sol_id:
            continue

        details = details_by_id.get(str(sol_id))
        searchable_text, metadata = flatten_solution_doc(doc, details)
        if not searchable_text.strip():
            continue

        batch_ids.append(f"MediaDive_Solution_{sol_id}")
        batch_docs.append(searchable_text)
        batch_metas.append(metadata)
        indexed += 1

        if len(batch_ids) >= batch_size:
            collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
            batch_ids, batch_docs, batch_metas = [], [], []

    # Final batch
    if batch_ids:
        collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

    logger.info(f"Indexed {indexed} media/solutions")
    logger.info(f"Collection count: {collection.count()}")
    return indexed


def index_ingredients(mongo_client: MongoClient, chroma_client, clear: bool = False) -> int:
    """Index ingredients into ChromaDB."""
    logger.info("\n" + "=" * 50)
    logger.info("Indexing MediaDive Ingredients")
    logger.info("=" * 50)

    db = mongo_client["mediadive"]
    ingredients = db["ingredient_details"]

    collection_name = "mediadive_ingredients"

    if clear:
        try:
            chroma_client.delete_collection(collection_name)
            logger.info(f"Cleared existing collection '{collection_name}'")
        except Exception:
            # Collection may not exist yet; proceed with indexing
            pass

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "MediaDive ingredients for semantic search"},
    )

    # Batch index ingredients
    batch_ids = []
    batch_docs = []
    batch_metas = []
    batch_size = 500
    indexed = 0

    total = ingredients.count_documents({})
    for doc in tqdm(ingredients.find({}), total=total, desc="Ingredients"):
        name = doc.get("name", "")
        if not name:
            continue

        searchable_text, metadata = flatten_ingredient_doc(doc)
        if not searchable_text.strip():
            continue

        # Use name as ID (sanitized)
        safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", name)[:100]
        batch_ids.append(f"MediaDive_Ingredient_{safe_id}")
        batch_docs.append(searchable_text)
        batch_metas.append(metadata)
        indexed += 1

        if len(batch_ids) >= batch_size:
            collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
            batch_ids, batch_docs, batch_metas = [], [], []

    # Final batch
    if batch_ids:
        collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

    logger.info(f"Indexed {indexed} ingredients")
    logger.info(f"Collection count: {collection.count()}")
    return indexed


def index_strains(mongo_client: MongoClient, chroma_client, clear: bool = False) -> int:
    """Index strains into ChromaDB."""
    logger.info("\n" + "=" * 50)
    logger.info("Indexing MediaDive Strains")
    logger.info("=" * 50)

    db = mongo_client["mediadive"]
    strains = db["strains"]

    collection_name = "mediadive_strains"

    if clear:
        try:
            chroma_client.delete_collection(collection_name)
            logger.info(f"Cleared existing collection '{collection_name}'")
        except Exception:
            # Collection may not exist yet; proceed with indexing
            pass

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "MediaDive strains for semantic search"},
    )

    # Batch index strains
    batch_ids = []
    batch_docs = []
    batch_metas = []
    batch_size = 500
    indexed = 0

    total = strains.count_documents({})
    for doc in tqdm(strains.find({}), total=total, desc="Strains"):
        strain_id = doc.get("id") or doc.get("_id", "")
        if not strain_id:
            continue

        searchable_text, metadata = flatten_strain_doc(doc)
        if not searchable_text.strip():
            continue

        batch_ids.append(f"MediaDive_Strain_{strain_id}")
        batch_docs.append(searchable_text)
        batch_metas.append(metadata)
        indexed += 1

        if len(batch_ids) >= batch_size:
            collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
            batch_ids, batch_docs, batch_metas = [], [], []

    # Final batch
    if batch_ids:
        collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

    logger.info(f"Indexed {indexed} strains")
    logger.info(f"Collection count: {collection.count()}")
    return indexed


def run_tests(chroma_client) -> tuple[int, int]:
    """Run test cases against indexed collections.

    Returns (passed, total).
    """
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING TEST CASES")
    logger.info("=" * 60)

    passed = 0
    total = 0

    test_configs = [
        ("mediadive_media", TEST_CASES["media"]),
        ("mediadive_ingredients", TEST_CASES["ingredients"]),
        ("mediadive_strains", TEST_CASES["strains"]),
    ]

    for collection_name, cases in test_configs:
        try:
            collection = chroma_client.get_collection(collection_name)
            logger.info(f"\n--- Testing {collection_name} ({collection.count()} docs) ---")
        except Exception as e:
            logger.warning(f"Collection {collection_name} not found: {e}")
            continue

        for query, expected_substrings, description in cases:
            total += 1
            try:
                results = collection.query(query_texts=[query], n_results=3)

                # Check if any result contains expected substrings
                found = False
                matched_text = ""
                for doc in results.get("documents", [[]])[0]:
                    doc_lower = doc.lower()
                    if any(sub.lower() in doc_lower for sub in expected_substrings):
                        found = True
                        matched_text = doc[:80] + "..." if len(doc) > 80 else doc
                        break

                if found:
                    passed += 1
                    logger.info(f"  PASS: '{query}' ({description})")
                    logger.info(f"        -> {matched_text}")
                else:
                    logger.warning(f"  FAIL: '{query}' ({description})")
                    logger.warning(f"        Expected substrings: {expected_substrings}")
                    if results.get("documents", [[]])[0]:
                        logger.warning(f"        Got: {results['documents'][0][0][:80]}...")

            except Exception as e:
                logger.warning(f"  ERROR: '{query}' - {e}")

    logger.info(f"\n{'=' * 60}")
    logger.info(f"TEST RESULTS: {passed}/{total} passed ({100 * passed / total:.1f}%)" if total > 0 else "No tests run")
    logger.info("=" * 60)

    return passed, total


def demo_searches(chroma_client) -> None:
    """Demonstrate search capabilities with realistic queries."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMO: MediaDive ChromaDB Search")
    logger.info("=" * 60)

    demo_queries = [
        ("mediadive_media", "LB agar plate", "Common media search"),
        ("mediadive_media", "minimal medium for methylotrophs", "Phenotype-based search"),
        ("mediadive_ingredients", "magnesium salt trace element", "Ingredient role search"),
        ("mediadive_ingredients", "carbon source sugar", "Ingredient function search"),
        ("mediadive_strains", "Methylobacterium", "Genus search"),
        ("mediadive_strains", "DSM 1337", "Culture collection search"),
    ]

    for collection_name, query, description in demo_queries:
        try:
            collection = chroma_client.get_collection(collection_name)
            logger.info(f"\n--- Query: '{query}' ({description}) ---")
            results = collection.query(query_texts=[query], n_results=3)

            for i, (_doc_id, dist, meta) in enumerate(
                zip(results["ids"][0], results["distances"][0], results["metadatas"][0], strict=False)
            ):
                name = meta.get("name") or meta.get("species") or "Unknown"
                logger.info(f"  {i + 1}. {name} - dist: {dist:.3f}")

        except Exception as e:
            logger.warning(f"Demo query '{query}' failed: {e}")


@click.command()
@click.option("--clear/--no-clear", default=True, help="Clear existing collections")
@click.option("--test/--no-test", default=False, help="Run test cases after indexing")
@click.option("--demo/--no-demo", default=False, help="Run demo searches after indexing")
@click.option("--test-only", is_flag=True, help="Only run tests (skip indexing)")
def main(clear: bool, test: bool, demo: bool, test_only: bool) -> None:
    """Index MediaDive MongoDB data into ChromaDB."""
    logger.info("=" * 60)
    logger.info("MediaDive ChromaDB Indexer")
    logger.info("=" * 60)

    mongo_client: MongoClient = MongoClient(MONGODB_URI)
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    if not test_only:
        index_media(mongo_client, chroma_client, clear=clear)
        index_ingredients(mongo_client, chroma_client, clear=clear)
        index_strains(mongo_client, chroma_client, clear=clear)

    if test or test_only:
        passed, total = run_tests(chroma_client)
        if total > 0 and passed < total:
            logger.warning(f"Some tests failed: {total - passed}/{total}")

    if demo:
        demo_searches(chroma_client)

    logger.info("\nDone!")


if __name__ == "__main__":
    main()
