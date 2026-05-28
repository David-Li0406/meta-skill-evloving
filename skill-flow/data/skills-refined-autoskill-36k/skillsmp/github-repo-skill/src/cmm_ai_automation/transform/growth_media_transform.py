"""
Transformation logic for growth media data.

This module provides functions to ground media names to established databases
(MediaDive, TogoMedium) and transform them into KGX nodes.

It includes:
- Mojibake cleaning for encoding artifacts
- MongoDB-backed verification for MediaDive IDs
- ChromaDB-backed semantic search for grounding
- KGX node generation using Biolink Model categories
"""

from __future__ import annotations

import logging
import re
from typing import Any, cast

from cmm_ai_automation.transform.kgx import KGXNode

logger = logging.getLogger(__name__)


def fix_mojibake(text: str) -> str:
    """
    Fix MacRoman <-> UTF-8 encoding artifacts.

    Parameters
    ----------
    text : str
        The potentially corrupted string

    Returns
    -------
    str
        The cleaned string

    Examples
    --------
    >>> fix_mojibake("normal text")
    'normal text'
    """
    if not text:
        return ""
    try:
        # The specific pattern observed implies UTF-8 bytes interpreted as MacRoman.
        return text.encode("mac_roman").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If it fails, return original
        return text


def normalize_medium_id(name: str) -> str:
    """
    Create a safe local ID from a medium name.

    Parameters
    ----------
    name : str
        The medium name

    Returns
    -------
    str
        Safe ID for CURIE local part

    Examples
    --------
    >>> normalize_medium_id("LB Medium")
    'lb-medium'
    >>> normalize_medium_id("MP-Methanol ")
    'mp-methanol'
    """
    safe = name.lower().strip()
    safe = re.sub(r"\s+", "-", safe)
    safe = re.sub(r"[^a-z0-9-]", "", safe)
    return safe


class MediaGrounder:
    """
    Grounds media names to external databases.

    Priority:
    1. Local Registry (if provided)
    2. Manual Mappings (TSV)
    3. Verified ID (if provided and exists in DB)
    4. Exact Name Match in DB
    5. Semantic Search (ChromaDB)
    6. Fallback to temporary local BER-CMM-MEDIUM ID (should avoid)
    """

    def __init__(
        self,
        local_registry: dict[str, dict] | None = None,
        manual_mappings: dict[str, dict] | None = None,
        mongo_db: Any = None,
        togo_collection: Any = None,
        dive_collection: Any = None,
        togo_threshold: float = 0.4,
        dive_threshold: float = 0.4,
    ):
        self.local_registry = local_registry or {}
        self.manual_mappings = manual_mappings or {}
        self.mongo_db = mongo_db
        self.togo_collection = togo_collection
        self.dive_collection = dive_collection
        self.togo_threshold = togo_threshold
        self.dive_threshold = dive_threshold

    def check_mediadive_mongo(self, media_id: str | int) -> dict[str, Any] | None:
        """Verify if a MediaDive ID exists in MongoDB."""
        if self.mongo_db is None or not media_id:
            return None

        # Clean the ID
        clean_id = str(media_id).replace("medium:", "").replace("mediadive:", "").strip()

        # Try integer lookup
        if clean_id.isdigit():
            doc = self.mongo_db.media_details.find_one({"_id": int(clean_id)})
            if doc:
                return cast("dict[str, Any]", doc)

        # Try string lookup (e.g. "1a")
        doc = self.mongo_db.media_details.find_one({"_id": clean_id})
        if doc:
            return cast("dict[str, Any]", doc)

        return None

    def ground(self, name: str, provided_id: str | None = None) -> dict[str, Any]:
        """
        Attempt to ground a medium.

        Returns
        -------
        dict
            Grounding result with 'id', 'source', 'confidence', 'method', 'meta'
        """
        name_lower = name.lower().strip()

        # 0. Check Local Registry (Stable BER-CMM-MEDIUM IDs)
        for reg_name, reg_entry in self.local_registry.items():
            if name_lower == reg_name.lower().strip():
                return {
                    "id": reg_entry["local_id"],
                    "source": "local_registry",
                    "confidence": 1.0,
                    "method": "local_registry_match",
                    "meta": reg_entry,
                }

        # Normalize name for mapping lookup (e.g. "LB medium (Luria-Bertani)" -> "lb")
        name_normalized = re.split(r"[\s\(\-]", name_lower)[0]
        # Also try "dsmz:88" style if name contains numbers
        name_with_number = re.sub(r"\s+", ":", name_lower) if ":" not in name_lower else name_lower

        # 1. Check Manual Mappings
        lookup_keys = [name_lower, name_normalized, name_with_number]
        for key in lookup_keys:
            for m_key, m in self.manual_mappings.items():
                if (key == m_key or key.startswith(m_key + ":")) and m.get("confidence", 0) > 0:
                    # If source is DOI, we use a local ID but attach the DOI
                    if m["source"] == "doi":
                        local_id = f"BER-CMM-MEDIUM:{normalize_medium_id(name)}"
                        return {
                            "id": local_id,
                            "source": "local",
                            "confidence": m.get("confidence", 1.0),
                            "method": f"manual_mapping_ref ({m_key})",
                            "meta": {"name": name, "doi": m["id"]},
                        }

                    return {
                        "id": f"{m['source']}:{m['id']}" if ":" not in m["id"] else m["id"],
                        "source": m["source"],
                        "confidence": m.get("confidence", 1.0),
                        "method": f"manual_mapping ({m_key})",
                        "meta": {"name": name},
                    }

        # 2. Verify Provided ID
        if provided_id and provided_id.strip() not in ["-", ""]:
            ids_to_check = [i.strip() for i in provided_id.split(";") if i.strip()]
            for pid in ids_to_check:
                if "mediadive" in pid.lower() or "medium:" in pid.lower() or pid.isdigit():
                    doc = self.check_mediadive_mongo(pid)
                    if doc:
                        return {
                            "id": f"mediadive:{doc['_id']}",
                            "source": "mediadive",
                            "confidence": 1.0,
                            "method": "verified_id_match",
                            "meta": doc.get("medium", {}),
                        }

        # 3. Exact Name Match in MediaDive Mongo
        if self.mongo_db is not None:
            doc = self.mongo_db.media_details.find_one(
                {"medium.name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}}
            )
            if not doc:
                doc = self.mongo_db.media_details.find_one(
                    {"medium.name": {"$regex": f"^{re.escape(name_normalized)}$", "$options": "i"}}
                )

            if doc:
                return {
                    "id": f"mediadive:{doc['_id']}",
                    "source": "mediadive",
                    "confidence": 0.95,
                    "method": "exact_name_match_mongo",
                    "meta": doc.get("medium", {}),
                }

        # 4. Semantic Search: TogoMedium
        if self.togo_collection:
            results = self.togo_collection.query(query_texts=[name], n_results=1)
            if results["ids"][0]:
                dist = results["distances"][0][0]
                meta = results["metadatas"][0][0]
                if dist < self.togo_threshold:
                    return {
                        "id": f"togomedium:{meta.get('togomedium_id')}",
                        "source": "togomedium",
                        "confidence": 1.0 - dist,
                        "method": "semantic_search",
                        "meta": meta,
                    }

        # 5. Semantic Search: MediaDive
        if self.dive_collection:
            results = self.dive_collection.query(query_texts=[name], n_results=1)
            if results["ids"][0]:
                dist = results["distances"][0][0]
                meta = results["metadatas"][0][0]
                if dist < self.dive_threshold:
                    return {
                        "id": f"mediadive:{meta.get('mediadive_id')}",
                        "source": "mediadive",
                        "confidence": 1.0 - dist,
                        "method": "semantic_search",
                        "meta": meta,
                    }

        # 6. Fallback
        local_id = f"BER-CMM-MEDIUM:{normalize_medium_id(name)}"
        return {
            "id": local_id,
            "source": "local",
            "confidence": 0.0,
            "method": "fallback",
            "meta": {},
        }


def parse_publications(row: dict[str, str], meta: dict[str, Any]) -> list[str]:
    """Parse publications/references from row and metadata."""
    pubs = set()

    # From grounding metadata
    if "doi" in meta:
        doi = str(meta["doi"]).strip()
        if doi.startswith("10."):
            pubs.add(f"doi:{doi}")
        else:
            pubs.add(doi)

    # From source reference field
    if "source_ref" in meta and meta["source_ref"].startswith("doi:"):
        pubs.add(meta["source_ref"])

    # From TSV references column
    raw_refs = row.get("references", "").strip()
    if raw_refs:
        # Split by comma or semicolon
        ref_parts = re.split(r"[,;]", raw_refs)
        for ref in ref_parts:
            ref = ref.strip()
            if not ref:
                continue

            # Check for DOI patterns
            doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", ref, re.I)
            if doi_match:
                pubs.add(f"doi:{doi_match.group(0)}")
            else:
                pubs.add(ref)

    return sorted(pubs)


def transform_media_row(row: dict[str, str], grounder: MediaGrounder) -> tuple[KGXNode, dict]:
    """
    Transform a media row from TSV to a KGX node.

    Parameters
    ----------
    row : dict[str, str]
        Row from growth_media.tsv
    grounder : MediaGrounder
        The grounder instance to use

    Returns
    -------
    tuple[KGXNode, dict]
        The created node and a grounding report/hybrid row entry
    """
    # Clean inputs
    name = fix_mojibake(row.get("media_name", "")).strip()
    provided_id = row.get("kg_microbe_nodes", "").strip() or row.get("target_id", "").strip()
    description = fix_mojibake(row.get("description", "")).strip()

    if not name:
        raise ValueError("Missing media_name in row")

    # Ground
    result = grounder.ground(name, provided_id)

    # Use Numeric ID from placeholder URI if it exists and we are local
    final_id = result["id"]
    if result["source"] == "local":
        placeholder_uri = row.get("placeholder URI", "")
        match = re.search(r"/media/(\d{7})", placeholder_uri)
        if match:
            final_id = f"BER-CMM-MEDIUM:{match.group(1)}"

    # Create Node
    node_data = {
        "id": final_id,
        "category": ["biolink:ChemicalMixture"],
        "name": name,
        "provided_by": ["infores:cmm-ai-automation"],
        "description": description,
    }

    # Enrich Node Source
    if result["source"] not in ["local", "local_registry"]:
        node_data["provided_by"].append(f"infores:{result['source']}")
        # Add matched name to description if different
        db_name = result["meta"].get("name", "")
        if db_name and db_name.lower() != name.lower():
            if node_data["description"]:
                node_data["description"] += f" | Matched to: {db_name}"
            else:
                node_data["description"] = f"Matched to: {db_name}"

    # Handle Publications
    pubs = parse_publications(row, result["meta"])
    if pubs:
        node_data["publications"] = pubs

    # Handle Synonyms
    alt_names = row.get("alternative_names", "").strip()
    if alt_names:
        # Split and clean
        synonyms = [s.strip() for s in re.split(r"[,;]", alt_names) if s.strip()]
        if synonyms:
            node_data["synonym"] = synonyms

    # Handle Xrefs (from registry or grounding)
    xrefs = set()
    if "xref" in result["meta"] and result["meta"]["xref"]:
        xrefs.add(result["meta"]["xref"])
    if "original_id" in result["meta"] and result["meta"]["original_id"]:
        xrefs.add(f"{result['source']}:{result['meta']['original_id']}")

    # Preserve kg_microbe_nodes as xrefs if they look like IDs
    if provided_id:
        for pid in re.split(r"[,;]", provided_id):
            pid = pid.strip()
            if pid and ":" in pid:  # Simple heuristic for CURIE
                xrefs.add(pid)

    if xrefs:
        node_data["xref"] = sorted(xrefs)

    # Handle Custom/Optional fields
    if row.get("ph"):
        node_data["ph"] = row["ph"]
    if row.get("media_type"):
        node_data["media_type"] = row["media_type"]
    if row.get("sterilization_method"):
        node_data["sterilization_method"] = row["sterilization_method"]
    if row.get("target_organisms"):
        node_data["target_organisms"] = row["target_organisms"]
    if row.get("notes"):
        node_data["notes"] = row["notes"]
    if row.get("source"):
        node_data["source"] = row["source"]

    node = KGXNode(**node_data)

    # Create Hybrid Output Row (Original + New fields)
    hybrid_row = row.copy()
    hybrid_row.update(
        {
            "grounded_id": final_id,
            "grounded_source": result["source"],
            "grounded_name": result["meta"].get("name", ""),
            "grounded_confidence": f"{result['confidence']:.2f}",
            "grounded_method": result["method"],
            "cleaned_name": name,
            "cleaned_description": description,
        }
    )

    return node, hybrid_row
