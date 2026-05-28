"""Enrichment store using linkml-store for ingredient data management.

This module provides a schema-aware data store for enriched ingredients,
using linkml-store with DuckDB backend for local persistence.

Key features:
- (inchikey, cas_rn) tuple as primary key for entity resolution
- Source-specific authoritative IDs (each API owns its own ID type)
- Conflict detection and logging
- Provenance tracking per field

References:
    - linkml-store: https://linkml.io/linkml-store/
    - KGX format: https://github.com/biolink/kgx
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from linkml_store import Client
from linkml_store.api import Collection, Database

logger = logging.getLogger(__name__)

# Regex patterns for name cleaning and scoring
CAS_RN_PATTERN = re.compile(r"^\d{1,7}-\d{2}-\d$")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
SYSTEMATIC_PREFIXES = ("di", "tri", "tetra", "penta", "hexa", "hepta", "octa", "mono", "bis", "tris")


def clean_html_tags(text: str | None) -> str | None:
    """Remove HTML tags from text (e.g., <sub>, <sup>).

    Args:
        text: Input text that may contain HTML tags

    Returns:
        Cleaned text with HTML tags removed, or None if input is None
    """
    if not text:
        return text
    return HTML_TAG_PATTERN.sub("", text)


def is_cas_number(text: str) -> bool:
    """Check if a string looks like a CAS Registry Number.

    Args:
        text: String to check

    Returns:
        True if the string matches CAS RN format (e.g., 7732-18-5)
    """
    return bool(CAS_RN_PATTERN.match(text.strip()))


def score_name_quality(name: str) -> int:
    """Score a name for display quality (higher is better).

    Prefers common names that are short, readable, and meaningful
    to bacteriologists and laypeople.

    Args:
        name: Name to score

    Returns:
        Integer score (higher is better for display)
    """
    score = 100  # Start with base score

    # Penalize very long names (systematic names tend to be long)
    if len(name) > 50:
        score -= 30
    elif len(name) > 30:
        score -= 15

    # Penalize names with systematic chemistry prefixes
    name_lower = name.lower()
    for prefix in SYSTEMATIC_PREFIXES:
        if name_lower.startswith(prefix):
            score -= 10
            break

    # Penalize names with parenthetical formulas
    if "(" in name and any(c.isdigit() for c in name):
        score -= 15

    # Penalize names with semicolons (IUPAC convention)
    if ";" in name:
        score -= 20

    # Penalize all-uppercase names
    if name.isupper():
        score -= 5

    # Penalize names that look like CAS numbers
    if is_cas_number(name):
        score -= 100

    # Penalize HTML-looking content
    if "<" in name:
        score -= 25

    # Bonus for capitalized first letter (proper name)
    if name and name[0].isupper() and name[1:].islower():
        score += 5

    return score


def select_display_name(record: dict[str, Any]) -> str:
    """Select the best display name for an ingredient record.

    Priority order:
    1. Original query name (from source_records) - what bacteriologists use
    2. ChEBI name - well-curated
    3. Best-scoring name from available options
    4. IUPAC name - last resort

    Args:
        record: Ingredient record with name, iupac_name, synonyms, source_records

    Returns:
        Best display name for the record
    """
    import json

    candidates: list[tuple[str, int]] = []  # (name, priority_bonus)

    # Get source records - check both _sources (in-memory) and source_records (from DB)
    sources_raw = record.get("_sources") or record.get("source_records") or []

    # Parse JSON strings if needed (DuckDB stores them as JSON strings in a list)
    sources: list[dict[str, Any]] = []
    for item in sources_raw:
        if isinstance(item, dict):
            sources.append(item)
        elif isinstance(item, str):
            # Try to parse JSON strings (from DuckDB text storage)
            try:
                parsed = json.loads(item)
                if isinstance(parsed, dict):
                    sources.append(parsed)
            except (json.JSONDecodeError, TypeError):
                pass  # Skip malformed JSON strings; continue with valid sources

    # Extract query names from sources
    query_names = set()
    for source_record in sources:
        query = source_record.get("source_query")
        if query and isinstance(query, str):
            query_names.add(query)

    # Query names get highest priority bonus
    for qname in query_names:
        clean_name = clean_html_tags(qname)
        if clean_name:
            candidates.append((clean_name, 50))

    # Current name field
    if record.get("name"):
        clean_name = clean_html_tags(record["name"])
        if clean_name:
            # Check if this came from ChEBI (bonus)
            name_bonus = 20 if any(s.get("source_name", "").startswith("chebi") for s in sources) else 0
            candidates.append((clean_name, name_bonus))

    # Synonyms (lower priority)
    synonyms = record.get("synonyms", [])
    if isinstance(synonyms, list):
        for syn in synonyms[:20]:  # Limit to first 20
            if isinstance(syn, str):
                clean_syn = clean_html_tags(syn)
                if clean_syn and not is_cas_number(clean_syn):
                    candidates.append((clean_syn, 0))

    # IUPAC name (lowest priority)
    if record.get("iupac_name"):
        clean_iupac = clean_html_tags(record["iupac_name"])
        if clean_iupac:
            candidates.append((clean_iupac, -20))

    if not candidates:
        return str(record.get("name", "Unknown"))

    # Score all candidates and pick the best
    scored = []
    for name, bonus in candidates:
        quality_score = score_name_quality(name)
        total_score = quality_score + bonus
        scored.append((total_score, name))

    # Sort by score descending, return best
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][1]


# Schema path
SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "cmm_ai_automation.yaml"

# Default store path
DEFAULT_STORE_PATH = Path(__file__).parent.parent.parent.parent.parent / "data" / "enrichment.duckdb"

# Authoritative sources for each field type
AUTHORITATIVE_SOURCES = {
    # Each API is authoritative for its own primary ID
    "pubchem_cid": "pubchem",
    "chebi_id": "chebi",
    "cas_rn": "cas",
    "mediadive_id": "mediadive",
    # ChEBI is authoritative for roles
    "biological_roles": "chebi",
    "chemical_roles": "chebi",
    "application_roles": "chebi",
    # Chemical structure - first source wins
    "inchi": None,  # No single authoritative source
    "inchikey": None,
    "smiles": None,
}


def generate_composite_key(inchikey: str | None, cas_rn: str | None) -> str:
    """Generate a composite key from (inchikey, cas_rn) tuple.

    The composite key format is: {inchikey}|{cas_rn}
    Uses 'unknown' for missing parts (deterministic, not random).

    Args:
        inchikey: InChIKey string (may be None)
        cas_rn: CAS Registry Number (may be None)

    Returns:
        Composite key string
    """
    ik_part = inchikey if inchikey else "unknown"
    cas_part = cas_rn if cas_rn else "unknown"
    return f"{ik_part}|{cas_part}"


def parse_composite_key(key: str) -> tuple[str | None, str | None]:
    """Parse a composite key back to (inchikey, cas_rn) tuple.

    Args:
        key: Composite key string

    Returns:
        Tuple of (inchikey, cas_rn) - may contain None for missing parts
    """
    parts = key.split("|", 1)
    if len(parts) != 2:
        return (None, None)

    inchikey = None if parts[0] == "unknown" else parts[0]
    cas_rn = None if parts[1] == "unknown" else parts[1]
    return (inchikey, cas_rn)


class EnrichmentStore:
    """Store for enriched ingredient data using linkml-store.

    Uses (inchikey, cas_rn) tuple as primary key for entity resolution.
    Each API is authoritative for its own ID type.

    Example:
        >>> store = EnrichmentStore()
        >>> store.upsert_ingredient({
        ...     "inchikey": "CSNNHWWHGAXBCP-UHFFFAOYSA-L",
        ...     "cas_rn": "7487-88-9",
        ...     "name": "magnesium sulfate",
        ...     "pubchem_cid": 24083,
        ... }, source="pubchem")
        >>> ingredient = store.get_by_key("CSNNHWWHGAXBCP-UHFFFAOYSA-L", "7487-88-9")
    """

    def __init__(
        self,
        store_path: Path | str | None = None,
        schema_path: Path | str | None = None,
    ):
        """Initialize the enrichment store.

        Args:
            store_path: Path to DuckDB database file
            schema_path: Path to LinkML schema file
        """
        self.store_path = Path(store_path) if store_path else DEFAULT_STORE_PATH
        self.schema_path = Path(schema_path) if schema_path else SCHEMA_PATH

        # Ensure store directory exists
        self.store_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize linkml-store client
        self._client: Client | None = None
        self._db: Database | None = None
        self._collection: Collection | None = None

    def _get_client(self) -> Client:
        """Get or create the linkml-store client."""
        if self._client is None:
            self._client = Client()
        return self._client

    def _get_db(self) -> Database:
        """Get or create the database connection."""
        if self._db is None:
            client = self._get_client()
            # Use DuckDB backend
            db_url = f"duckdb:///{self.store_path}"
            self._db = client.attach_database(db_url, alias="enrichment")
        return self._db

    def _get_collection(self) -> Collection:
        """Get or create the enriched_ingredients collection."""
        if self._collection is None:
            db = self._get_db()
            # Create or get the collection with schema
            # Use EnrichedIngredient class from LinkML schema to define structure
            self._collection = db.create_collection(
                "enriched_ingredients",
                recreate_if_exists=False,
                class_name="EnrichedIngredient",
                schema_location=str(self.schema_path),
            )
        return self._collection

    def close(self) -> None:
        """Close the store connection."""
        self._collection = None
        self._db = None
        self._client = None

    def upsert_ingredient(
        self,
        data: dict[str, Any],
        source: str,
        query: str | None = None,
    ) -> str:
        """Insert or update an enriched ingredient.

        Uses entity resolution to find existing records by EITHER inchikey OR cas_rn.
        This ensures records from different sources are properly merged even if
        one source doesn't provide all identifiers.

        Args:
            data: Ingredient data dictionary
            source: Name of the data source (pubchem, chebi, cas, etc.)
            query: Original query used to retrieve this data

        Returns:
            The composite key of the upserted record
        """
        collection = self._get_collection()

        inchikey = data.get("inchikey")
        cas_rn = data.get("cas_rn")

        # Entity resolution: find existing record by EITHER inchikey OR cas_rn
        existing = None
        existing_key = None

        # First try to find by inchikey (most reliable identifier)
        if inchikey:
            matches = self.find_by_inchikey(inchikey)
            if matches:
                existing = matches[0]
                existing_key = existing.get("id")

        # If not found by inchikey, try by cas_rn
        if not existing and cas_rn:
            matches = self.find_by_cas(cas_rn)
            if matches:
                existing = matches[0]
                existing_key = existing.get("id")

        # Generate new composite key using best available identifiers
        # Prefer existing record's identifiers to fill gaps
        final_inchikey = inchikey or (existing.get("inchikey") if existing else None)
        final_cas_rn = cas_rn or (existing.get("cas_rn") if existing else None)
        composite_key = generate_composite_key(final_inchikey, final_cas_rn)

        if existing:
            # Merge with existing record
            merged = self._merge_records(existing, data, source, query)
            merged["id"] = composite_key
            merged["last_enriched"] = datetime.now().isoformat()
            # Delete existing record (may have different key) and insert merged
            # NOTE: This is not atomic - if insert fails after delete, data is lost.
            # linkml-store's DuckDB backend doesn't support transactions, so we log
            # the merged data on failure for manual recovery. A future improvement
            # could use a backup table or write-ahead log pattern.
            logger.debug(f"Updating ingredient {existing_key} -> {composite_key}: {merged}")
            try:
                # Delete by the OLD key (existing_key), not the new composite_key
                if existing_key:
                    collection.delete_where({"id": existing_key})
                collection.insert([merged])
                collection.commit()
                if existing_key != composite_key:
                    logger.info(f"Merged ingredient: {existing_key} -> {composite_key}")
                else:
                    logger.info(f"Updated ingredient: {composite_key}")
            except Exception as e:
                logger.error(f"Failed to update ingredient {composite_key}: {e}")
                logger.error(f"Merged data that was lost: {merged}")
                raise
        else:
            # New record
            data["id"] = composite_key
            data["last_enriched"] = datetime.now().isoformat()
            data["source_records"] = [
                {
                    "source_name": source,
                    "source_id": self._get_source_id(data, source),
                    "source_timestamp": datetime.now().isoformat(),
                    "source_query": query,
                    "source_fields": list(data.keys()),
                }
            ]
            data["conflicts"] = []
            collection.insert([data])
            logger.info(f"Inserted new ingredient: {composite_key}")

        return composite_key

    def _get_source_id(self, data: dict[str, Any], source: str) -> str | None:
        """Extract the relevant ID from data based on source."""
        source_id_fields = {
            "pubchem": "pubchem_cid",
            "chebi": "chebi_id",
            "cas": "cas_rn",
            "mediadive": "mediadive_id",
            "node_normalization": "chebi_id",
        }
        field = source_id_fields.get(source)
        if field:
            return str(data.get(field, ""))
        return None

    def _merge_records(
        self,
        existing: dict[str, Any],
        new_data: dict[str, Any],
        source: str,
        query: str | None,
    ) -> dict[str, Any]:
        """Merge new data into existing record with conflict detection.

        Primary APIs are authoritative for their own ID types.
        """
        merged = existing.copy()
        conflicts = list(existing.get("conflicts", []))
        source_records = list(existing.get("source_records", []))

        # Track fields updated by this source
        updated_fields = []

        for field, new_value in new_data.items():
            if field in ("id", "source_records", "conflicts", "last_enriched"):
                continue

            if new_value is None:
                continue

            existing_value = merged.get(field)

            if existing_value is None:
                # No existing value, use new one
                merged[field] = new_value
                updated_fields.append(field)
            elif existing_value != new_value:
                # Conflict detected - check authoritativeness
                authoritative_source = AUTHORITATIVE_SOURCES.get(field)

                if authoritative_source == source:
                    # This source is authoritative for this field - overwrite
                    merged[field] = new_value
                    updated_fields.append(field)
                    conflicts.append(
                        {
                            "field_name": field,
                            "primary_source": source,
                            "primary_value": str(new_value),
                            "conflicting_source": "previous",
                            "conflicting_value": str(existing_value),
                            "resolution": "primary_source_wins",
                            "resolution_notes": f"{source} is authoritative for {field}",
                        }
                    )
                elif authoritative_source is None:
                    # No authoritative source - keep existing value but log
                    conflicts.append(
                        {
                            "field_name": field,
                            "primary_source": "first_source",
                            "primary_value": str(existing_value),
                            "conflicting_source": source,
                            "conflicting_value": str(new_value),
                            "resolution": "unresolved",
                            "resolution_notes": "No authoritative source defined, keeping first value",
                        }
                    )
                else:
                    # Different authoritative source - log conflict
                    conflicts.append(
                        {
                            "field_name": field,
                            "primary_source": authoritative_source,
                            "primary_value": str(existing_value),
                            "conflicting_source": source,
                            "conflicting_value": str(new_value),
                            "resolution": "unresolved",
                            "resolution_notes": f"Authoritative source is {authoritative_source}, not {source}",
                        }
                    )

        # Add source record
        source_records.append(
            {
                "source_name": source,
                "source_id": self._get_source_id(new_data, source),
                "source_timestamp": datetime.now().isoformat(),
                "source_query": query,
                "source_fields": updated_fields,
            }
        )

        merged["conflicts"] = conflicts
        merged["source_records"] = source_records

        return merged

    def get_by_composite_key(self, composite_key: str) -> dict[str, Any] | None:
        """Get an ingredient by composite key.

        Args:
            composite_key: The composite key ({inchikey}|{cas_rn})

        Returns:
            Ingredient data dict or None if not found
        """
        collection = self._get_collection()
        results = collection.find({"id": composite_key})
        # QueryResult has a rows attribute containing list of dicts
        if results.rows:
            row: dict[str, Any] = results.rows[0]
            return row
        return None

    def get_by_key(self, inchikey: str | None, cas_rn: str | None) -> dict[str, Any] | None:
        """Get an ingredient by (inchikey, cas_rn) tuple.

        Args:
            inchikey: InChIKey string
            cas_rn: CAS Registry Number

        Returns:
            Ingredient data dict or None if not found
        """
        composite_key = generate_composite_key(inchikey, cas_rn)
        return self.get_by_composite_key(composite_key)

    def find_by_chebi(self, chebi_id: str) -> list[dict[str, Any]]:
        """Find ingredients by ChEBI ID.

        Args:
            chebi_id: ChEBI ID (e.g., "CHEBI:32599")

        Returns:
            List of matching ingredient records
        """
        collection = self._get_collection()
        results = collection.find({"chebi_id": chebi_id})
        return results.rows or []

    def find_by_pubchem(self, pubchem_cid: int) -> list[dict[str, Any]]:
        """Find ingredients by PubChem CID.

        Args:
            pubchem_cid: PubChem Compound ID

        Returns:
            List of matching ingredient records
        """
        collection = self._get_collection()
        results = collection.find({"pubchem_cid": pubchem_cid})
        return results.rows or []

    def find_by_cas(self, cas_rn: str) -> list[dict[str, Any]]:
        """Find ingredients by CAS Registry Number.

        Args:
            cas_rn: CAS Registry Number

        Returns:
            List of matching ingredient records
        """
        collection = self._get_collection()
        results = collection.find({"cas_rn": cas_rn})
        return results.rows or []

    def find_by_inchikey(self, inchikey: str) -> list[dict[str, Any]]:
        """Find ingredients by InChIKey.

        Args:
            inchikey: InChIKey string

        Returns:
            List of matching ingredient records
        """
        collection = self._get_collection()
        results = collection.find({"inchikey": inchikey})
        return results.rows or []

    def get_all_conflicts(self) -> list[dict[str, Any]]:
        """Get all records that have unresolved conflicts.

        Returns:
            List of records with conflicts
        """
        collection = self._get_collection()
        all_records = collection.find({})
        return [
            r
            for r in (all_records.rows or [])
            if r.get("conflicts") and any(c.get("resolution") == "unresolved" for c in r.get("conflicts", []))
        ]

    def get_stats(self) -> dict[str, Any]:
        """Get statistics about the enrichment store.

        Returns:
            Dict with counts and coverage statistics
        """
        collection = self._get_collection()
        all_records = collection.find({}).rows or []

        total = len(all_records)
        with_chebi = sum(1 for r in all_records if r.get("chebi_id"))
        with_pubchem = sum(1 for r in all_records if r.get("pubchem_cid"))
        with_cas = sum(1 for r in all_records if r.get("cas_rn"))
        with_inchikey = sum(1 for r in all_records if r.get("inchikey"))
        with_roles = sum(1 for r in all_records if r.get("biological_roles"))
        with_conflicts = sum(1 for r in all_records if r.get("conflicts"))

        return {
            "total_ingredients": total,
            "with_chebi_id": with_chebi,
            "with_pubchem_cid": with_pubchem,
            "with_cas_rn": with_cas,
            "with_inchikey": with_inchikey,
            "with_biological_roles": with_roles,
            "with_conflicts": with_conflicts,
            "coverage_chebi": with_chebi / total if total > 0 else 0,
            "coverage_pubchem": with_pubchem / total if total > 0 else 0,
            "coverage_cas": with_cas / total if total > 0 else 0,
        }

    def export_to_kgx(self, output_path: Path) -> tuple[int, int]:
        """Export enriched ingredients to KGX TSV format using KGX API.

        Uses the KGX TsvSink for proper KGX-compatible output.
        KGX format is used by KG-Microbe and other KG-Hub projects.

        Creates:
        - {output_path}_nodes.tsv - All ingredient nodes (biolink:SmallMolecule)
        - {output_path}_edges.tsv - Cross-reference relationships

        Args:
            output_path: Base path for output files (without _nodes.tsv suffix)

        Returns:
            Tuple of (nodes_exported, edges_exported)
        """
        from kgx.graph.nx_graph import NxGraph

        collection = self._get_collection()
        all_records = collection.find({}).rows or []

        # Consolidate records by ingredient (group by name, merge all data)
        # This ensures one node per ingredient in KGX output
        from collections import defaultdict

        by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in all_records:
            name = record.get("name")
            if name:
                name_key = name.lower().strip()
                if name_key and name_key != "_schema_init_":
                    by_name[name_key].append(record)

        # Merge records for each ingredient
        consolidated_records = []
        for _name, records in by_name.items():
            # Start with first record
            merged = records[0].copy()

            # Merge data from all records for this ingredient
            for record in records[1:]:
                for key, value in record.items():
                    if key in ("id", "last_enriched"):
                        continue  # Skip internal keys
                    if value is not None and not merged.get(key):
                        merged[key] = value
                    # Prefer clean formulas over HTML-formatted ones
                    elif key == "chemical_formula" and value and merged.get(key):
                        existing = merged[key]
                        # If existing has HTML but new value doesn't, prefer new value
                        if (
                            ("<sub>" in existing or "<sup>" in existing)
                            and "<sub>" not in value
                            and "<sup>" not in value
                        ):
                            merged[key] = value
                    # Merge source_records
                    if key == "source_records" and value:
                        existing_sources = merged.get("source_records", [])
                        for source_rec in value:
                            if source_rec not in existing_sources:
                                existing_sources.append(source_rec)
                        merged["source_records"] = existing_sources
                    # Merge conflicts
                    if key == "conflicts" and value:
                        existing_conflicts = merged.get("conflicts", [])
                        for conflict in value:
                            if conflict not in existing_conflicts:
                                existing_conflicts.append(conflict)
                        merged["conflicts"] = existing_conflicts
                    # Merge synonyms
                    if key == "synonyms" and value:
                        existing_synonyms = merged.get("synonyms", [])
                        if isinstance(value, list):
                            for syn in value:
                                if syn not in existing_synonyms:
                                    existing_synonyms.append(syn)
                        merged["synonyms"] = sorted(existing_synonyms)

            consolidated_records.append(merged)

        logger.info(f"Consolidated {len(all_records)} records into {len(consolidated_records)} ingredient nodes")

        # Create KGX graph
        graph = NxGraph()
        graph.name = "cmm-ai-automation"

        node_count = 0
        edge_count = 0

        for record in consolidated_records:
            # Determine best ID for node (prefer ChEBI > CAS > PubChem > InChIKey)
            node_id = None
            if record.get("chebi_id"):
                node_id = record["chebi_id"]
            elif record.get("cas_rn"):
                node_id = f"CAS:{record['cas_rn']}"
            elif record.get("pubchem_cid"):
                node_id = f"PUBCHEM.COMPOUND:{record['pubchem_cid']}"
            elif record.get("inchikey"):
                node_id = f"INCHIKEY:{record['inchikey']}"
            else:
                # Skip records without any identifiable ID
                logger.warning(f"Skipping record without identifiable ID: {record.get('id')}")
                continue

            # Build xrefs list (all IDs except the primary node_id)
            xrefs = []
            if record.get("chebi_id") and record["chebi_id"] != node_id:
                xrefs.append(record["chebi_id"])
            if record.get("pubchem_cid"):
                pubchem_id = f"PUBCHEM.COMPOUND:{record['pubchem_cid']}"
                if pubchem_id != node_id:
                    xrefs.append(pubchem_id)
            if record.get("cas_rn"):
                cas_id = f"CAS:{record['cas_rn']}"
                if cas_id != node_id:
                    xrefs.append(cas_id)
            if record.get("inchikey"):
                inchikey_id = f"INCHIKEY:{record['inchikey']}"
                if inchikey_id != node_id:
                    xrefs.append(inchikey_id)
            if record.get("kegg_id"):
                xrefs.append(f"KEGG.COMPOUND:{record['kegg_id']}")
            if record.get("mesh_id"):
                xrefs.append(f"MESH:{record['mesh_id']}")
            if record.get("drugbank_id"):
                xrefs.append(f"DRUGBANK:{record['drugbank_id']}")

            # Build node attributes with all available properties
            # Determine category from is_mixture field
            # Handle both boolean and string values from DuckDB
            is_mixture = record.get("is_mixture")
            if is_mixture is True or is_mixture == "true":
                category = ["biolink:ChemicalMixture"]
            elif is_mixture is False or is_mixture == "false":
                category = ["biolink:SmallMolecule"]
            else:
                # Default if unknown
                category = ["biolink:SmallMolecule"]

            node_attrs: dict[str, Any] = {
                "name": select_display_name(record),
                "category": category,
                "provided_by": ["cmm-ai-automation"],
            }

            # Add all enriched properties
            if record.get("description"):
                node_attrs["description"] = record["description"]
            if xrefs:
                node_attrs["xref"] = xrefs

            # Chemical identifiers
            if record.get("inchikey"):
                node_attrs["inchikey"] = record["inchikey"]
            if record.get("cas_rn"):
                node_attrs["cas_rn"] = record["cas_rn"]
            if record.get("chebi_id"):
                node_attrs["chebi_id"] = record["chebi_id"]
            if record.get("pubchem_cid"):
                node_attrs["pubchem_cid"] = record["pubchem_cid"]
            if record.get("kegg_id"):
                node_attrs["kegg_id"] = record["kegg_id"]
            if record.get("mesh_id"):
                node_attrs["mesh_id"] = record["mesh_id"]
            if record.get("drugbank_id"):
                node_attrs["drugbank_id"] = record["drugbank_id"]

            # Chemical structure
            if record.get("chemical_formula"):
                node_attrs["chemical_formula"] = record["chemical_formula"]
            if record.get("smiles"):
                node_attrs["smiles"] = record["smiles"]
            if record.get("inchi"):
                node_attrs["inchi"] = record["inchi"]
            if record.get("iupac_name"):
                node_attrs["iupac_name"] = clean_html_tags(record["iupac_name"])
            if record.get("synonyms"):
                # Clean synonyms: remove HTML tags and filter out CAS numbers
                clean_synonyms = []
                for syn in record["synonyms"]:
                    if isinstance(syn, str):
                        cleaned = clean_html_tags(syn)
                        if cleaned and not is_cas_number(cleaned):
                            clean_synonyms.append(cleaned)
                if clean_synonyms:
                    node_attrs["synonyms"] = clean_synonyms

            # Physical properties
            if record.get("molecular_mass"):
                node_attrs["molecular_mass"] = record["molecular_mass"]
            if record.get("monoisotopic_mass"):
                node_attrs["monoisotopic_mass"] = record["monoisotopic_mass"]
            if record.get("charge"):
                node_attrs["charge"] = record["charge"]

            # Biological annotations
            if record.get("biological_roles"):
                node_attrs["biological_roles"] = record["biological_roles"]
            if record.get("chemical_roles"):
                node_attrs["chemical_roles"] = record["chemical_roles"]
            if record.get("application_roles"):
                node_attrs["application_roles"] = record["application_roles"]

            # Mixture classification
            if record.get("is_mixture") is not None:
                node_attrs["is_mixture"] = record["is_mixture"]

            # Add node to graph
            graph.add_node(node_id, **node_attrs)
            node_count += 1

        # Write TSV files directly for better control over columns
        import csv

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write nodes TSV
        nodes_file = Path(str(output_path) + "_nodes.tsv")
        with nodes_file.open("w", newline="", encoding="utf-8") as f:
            # Collect all nodes with their attributes
            node_rows = []
            all_columns = {"id", "category", "name", "description", "provided_by"}
            for node_id, node_data in graph.nodes(data=True):
                row = {"id": node_id, **node_data}
                node_rows.append(row)
                all_columns.update(row.keys())

            # Sort columns for consistent output (id first, then alphabetical)
            sorted_columns = ["id", *sorted(c for c in all_columns if c != "id")]

            writer = csv.DictWriter(f, fieldnames=sorted_columns, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(node_rows)

        # Write edges TSV (empty for now since we don't need edges)
        edges_file = Path(str(output_path) + "_edges.tsv")
        with edges_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "subject", "predicate", "object", "category"], delimiter="\t")
            writer.writeheader()
            # No edges to write

        logger.info(f"Exported {node_count} nodes and {edge_count} edges to {output_path}")
        return (node_count, edge_count)

    def export_to_kgx_nodes(self, output_path: Path) -> int:
        """Export enriched ingredients to KGX nodes TSV format (legacy method).

        Deprecated: Use export_to_kgx() instead for proper KGX API usage.

        Args:
            output_path: Path to write nodes TSV file

        Returns:
            Number of nodes exported
        """
        # Convert to base path for new method
        base_path = output_path.parent / output_path.stem.replace("_nodes", "")
        nodes, _ = self.export_to_kgx(base_path)
        return nodes
