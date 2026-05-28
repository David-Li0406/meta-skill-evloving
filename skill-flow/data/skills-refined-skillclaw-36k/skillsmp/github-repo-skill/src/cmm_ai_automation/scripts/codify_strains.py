#!/usr/bin/env python3
"""Codify CMM strains using NCBITaxon ChromaDB semantic search.

For each strain in the CMM strains sheet, this script:
1. Looks up the species taxon document from ChromaDB to get synonyms
2. Queries ChromaDB with synonym + strain designation to find strain-level taxon IDs
3. Outputs matched strain taxon IDs

The OLS embeddings use text-embedding-3-small and concatenate label + synonyms,
so we need to use historical/canonical names from the species document to get
good matches (e.g., "Methylobacterium" instead of newer "Methylorubrum").

Usage:
    uv run python -m cmm_ai_automation.scripts.codify_strains

Options:
    --input PATH         Input TSV file (default: data/private/strains.tsv)
    --output PATH        Output TSV file (default: stdout)
    --chroma-path PATH   ChromaDB directory
    --limit N            Process only first N strains (for testing)
    --distance-threshold Maximum distance for confident matches (default: 0.3)
"""

import argparse
import contextlib
import csv
import logging
import os
import sys
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
import openai
from chromadb.config import Settings
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_INPUT = "./data/private/strains.tsv"
DEFAULT_CHROMA_PATH = "./data/chroma_ncbitaxon"
DEFAULT_COLLECTION_NAME = "ncbitaxon_embeddings"
DEFAULT_DISTANCE_THRESHOLD = 0.3
EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class StrainMatch:
    """Result of a strain codification attempt."""

    strain_id: str
    species_taxon_id: str
    scientific_name: str
    strain_designation: str
    matched_taxon_id: str | None
    matched_iri: str | None
    matched_document: str | None
    distance: float | None
    query_used: str | None
    match_quality: str  # "exact", "high", "medium", "low", "none"


def get_species_synonyms(
    collection: Any,
    taxon_id: str,
) -> list[str]:
    """Get synonyms for a species taxon from ChromaDB.

    Args:
        collection: ChromaDB collection
        taxon_id: NCBITaxon ID (just the number)

    Returns:
        List of synonym names from the document
    """
    iri = f"http://purl.obolibrary.org/obo/NCBITaxon_{taxon_id}"
    results = collection.get(
        where={"iri": iri},
        include=["documents"],
    )

    if not results["ids"]:
        return []

    # Document format: "name1; name2; name3; description text"
    document = results["documents"][0]
    # Split by semicolon and strip whitespace
    parts = [p.strip() for p in document.split(";")]
    # Filter out empty strings and very short entries
    return [p for p in parts if len(p) > 2]


def search_strain(
    collection: Any,
    query: str,
    n_results: int = 10,
) -> list[dict[str, Any]]:
    """Search ChromaDB for a strain query.

    Args:
        collection: ChromaDB collection
        query: Query text (e.g., "Methylobacterium extorquens AM1")
        n_results: Number of results to return

    Returns:
        List of result dicts with taxon_id, iri, document, distance
    """
    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    matches = []
    for i in range(len(results["ids"][0])):
        iri = results["metadatas"][0][i].get("iri", "")
        taxon_id = iri.split("/")[-1].replace("NCBITaxon_", "")
        matches.append(
            {
                "taxon_id": taxon_id,
                "iri": iri,
                "document": results["documents"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return matches


def classify_match_quality(distance: float | None, threshold: float) -> str:
    """Classify match quality based on distance."""
    if distance is None:
        return "none"
    if distance < 0.1:
        return "exact"
    if distance < 0.2:
        return "high"
    if distance < threshold:
        return "medium"
    return "low"


def normalize_strain_designation(strain: str) -> str:
    """Normalize strain designation for matching.

    NCBITaxon documents often use no hyphen (AM1 vs AM-1),
    so we normalize by removing hyphens.
    """
    return strain.replace("-", "")


def prioritize_synonyms(synonyms: list[str]) -> list[str]:
    """Prioritize synonyms for better matching.

    Prefers names starting with "Methylobacterium" (canonical old name)
    over newer names like "Methylorubrum" since OLS embeddings often
    use the older names.
    """
    # Separate into preferred (old names) and others
    preferred = []
    others = []
    for syn in synonyms:
        # Skip very long entries (likely descriptions) or single words
        if len(syn) > 100 or " " not in syn:
            continue
        # Prefer Methylobacterium over Methylorubrum for bacterial names
        if syn.startswith("Methylobacterium"):
            preferred.append(syn)
        else:
            others.append(syn)
    return preferred + others


def codify_strain(
    collection: Any,
    strain_id: str,
    species_taxon_id: str,
    scientific_name: str,
    strain_designation: str,
    distance_threshold: float,
) -> StrainMatch:
    """Attempt to codify a single strain.

    Strategy:
    1. If species_taxon_id is provided, look up synonyms from that document
    2. Try querying with each synonym + strain designation (normalized)
    3. If no species_taxon_id, try scientific_name + strain_designation
    4. Return best match under threshold

    Args:
        collection: ChromaDB collection
        strain_id: Strain identifier (e.g., "DSM:1337")
        species_taxon_id: Species NCBITaxon ID
        scientific_name: Scientific name from sheet
        strain_designation: Strain designation (e.g., "AM-1")
        distance_threshold: Maximum distance for a valid match

    Returns:
        StrainMatch result
    """
    best_match: dict[str, Any] | None = None
    best_query: str | None = None

    # Normalize strain designation (e.g., "AM-1" -> "AM1")
    normalized_strain = normalize_strain_designation(strain_designation)

    # Build list of queries to try
    queries_to_try: list[str] = []

    # If we have a species taxon ID, get synonyms and build queries
    if species_taxon_id:
        synonyms = get_species_synonyms(collection, species_taxon_id)
        if synonyms and normalized_strain:
            # Prioritize and filter synonyms
            prioritized = prioritize_synonyms(synonyms)
            # Try top synonyms with strain designation
            for syn in prioritized[:8]:  # Use more synonyms for better coverage
                queries_to_try.append(f"{syn} {normalized_strain}")

    # Also try the scientific name from the sheet
    if scientific_name:
        if normalized_strain:
            queries_to_try.append(f"{scientific_name} {normalized_strain}")
        else:
            # No strain designation - just search for species
            queries_to_try.append(scientific_name)

    # Try each query and keep best result
    for query in queries_to_try:
        results = search_strain(collection, query, n_results=5)
        if results:
            top = results[0]
            if best_match is None or top["distance"] < best_match["distance"]:
                best_match = top
                best_query = query

    # Build result
    if best_match and best_match["distance"] <= distance_threshold:
        return StrainMatch(
            strain_id=strain_id,
            species_taxon_id=species_taxon_id,
            scientific_name=scientific_name,
            strain_designation=strain_designation,
            matched_taxon_id=best_match["taxon_id"],
            matched_iri=best_match["iri"],
            matched_document=best_match["document"][:100],  # Truncate
            distance=best_match["distance"],
            query_used=best_query,
            match_quality=classify_match_quality(best_match["distance"], distance_threshold),
        )

    return StrainMatch(
        strain_id=strain_id,
        species_taxon_id=species_taxon_id,
        scientific_name=scientific_name,
        strain_designation=strain_designation,
        matched_taxon_id=None,
        matched_iri=None,
        matched_document=None,
        distance=best_match["distance"] if best_match else None,
        query_used=best_query,
        match_quality="none",
    )


def main() -> None:
    """Codify CMM strains using NCBITaxon ChromaDB."""
    parser = argparse.ArgumentParser(description="Codify CMM strains using NCBITaxon ChromaDB semantic search")
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Input TSV file",
    )
    parser.add_argument(
        "--output",
        help="Output TSV file (default: stdout)",
    )
    parser.add_argument(
        "--chroma-path",
        default=DEFAULT_CHROMA_PATH,
        help="ChromaDB directory",
    )
    parser.add_argument(
        "--collection-name",
        default=DEFAULT_COLLECTION_NAME,
        help="ChromaDB collection name",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Process only first N strains",
    )
    parser.add_argument(
        "--distance-threshold",
        type=float,
        default=DEFAULT_DISTANCE_THRESHOLD,
        help="Maximum distance for confident matches",
    )
    parser.add_argument(
        "--env-file",
        help="Path to .env file with OPENAI_API_KEY",
    )
    args = parser.parse_args()

    # Load environment
    if args.env_file:
        load_dotenv(args.env_file)
    else:
        load_dotenv()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found. Set it or use --env-file")
        sys.exit(1)

    openai.api_key = api_key

    # Connect to ChromaDB
    logger.info(f"Connecting to ChromaDB at {args.chroma_path}")
    client = chromadb.PersistentClient(
        path=args.chroma_path,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_collection(name=args.collection_name)
    logger.info(f"Collection '{args.collection_name}' has {collection.count()} entries")

    # Read input strains
    logger.info(f"Reading strains from {args.input}")
    strains: list[dict[str, str]] = []
    with Path(args.input).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            strains.append(row)

    if args.limit:
        strains = strains[: args.limit]

    logger.info(f"Processing {len(strains)} strains...")

    # Process each strain
    results: list[StrainMatch] = []
    for i, strain in enumerate(strains):
        if i > 0 and i % 10 == 0:
            logger.info(f"  Progress: {i}/{len(strains)}")

        match = codify_strain(
            collection=collection,
            strain_id=strain.get("strain_id", ""),
            species_taxon_id=strain.get("species_taxon_id", ""),
            scientific_name=strain.get("scientific_name", ""),
            strain_designation=strain.get("strain_designation", ""),
            distance_threshold=args.distance_threshold,
        )
        results.append(match)

    # Output results
    fieldnames = [
        "strain_id",
        "species_taxon_id",
        "scientific_name",
        "strain_designation",
        "matched_taxon_id",
        "matched_iri",
        "distance",
        "match_quality",
        "query_used",
        "matched_document",
    ]

    @contextlib.contextmanager
    def get_output_file() -> Generator[Any, None, None]:
        """Get output file handle, using stdout if no output path specified."""
        if args.output:
            with Path(args.output).open("w", newline="", encoding="utf-8") as f:
                yield f
        else:
            yield sys.stdout

    with get_output_file() as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for match in results:
            writer.writerow(
                {
                    "strain_id": match.strain_id,
                    "species_taxon_id": match.species_taxon_id,
                    "scientific_name": match.scientific_name,
                    "strain_designation": match.strain_designation,
                    "matched_taxon_id": match.matched_taxon_id or "",
                    "matched_iri": match.matched_iri or "",
                    "distance": f"{match.distance:.4f}" if match.distance else "",
                    "match_quality": match.match_quality,
                    "query_used": match.query_used or "",
                    "matched_document": match.matched_document or "",
                }
            )

    # Summary
    quality_counts: dict[str, int] = {}
    for r in results:
        quality_counts[r.match_quality] = quality_counts.get(r.match_quality, 0) + 1

    logger.info("\n=== Summary ===")
    logger.info(f"  Total strains: {len(results)}")
    for quality in ["exact", "high", "medium", "low", "none"]:
        count = quality_counts.get(quality, 0)
        pct = 100 * count / len(results) if results else 0
        logger.info(f"  {quality}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
