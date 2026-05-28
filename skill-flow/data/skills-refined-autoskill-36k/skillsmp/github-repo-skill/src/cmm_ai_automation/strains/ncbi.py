"""NCBI Entrez API functions for strain enrichment.

This module provides functions to fetch data from NCBI Taxonomy using
the Entrez E-utilities API.

Supports NCBI API key via NCBI_API_KEY environment variable to increase
rate limit from 3 requests/second to 10 requests/second.

Implements file-based caching to avoid redundant API calls.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, TypedDict, cast

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# NCBI Entrez settings
NCBI_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
NCBI_ELINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
NCBI_REQUEST_TIMEOUT = 10  # seconds

# API key for higher rate limits (10 req/sec with key vs 3 req/sec without)
NCBI_API_KEY = os.getenv("NCBI_API_KEY")

# Cache directory for NCBI responses (project-relative for portability)
CACHE_DIR = Path(__file__).parent.parent.parent.parent / "cache" / "ncbi"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class NcbiTaxonData(TypedDict):
    """Type for NCBI Taxonomy data returned from efetch."""

    scientific_name: str  # Primary scientific name from NCBI
    synonyms: list[str]
    equivalent_names: list[str]
    includes: list[str]
    misspellings: list[str]
    authority: list[str]
    rank: str
    species_taxon_id: str  # Species-level ancestor from lineage
    parent_taxon_id: str  # Immediate parent taxon from lineage


class NcbiLinkout(TypedDict):
    """External linkout from NCBI."""

    provider: str  # e.g., "BacDive", "BioCyc"
    url: str
    name: str


def _get_cache_path(cache_type: str, key: str) -> Path:
    """Get cache file path for a given cache type and key.

    Args:
        cache_type: Type of cache (e.g., "synonyms", "linkouts")
        key: Unique key for the cached item (e.g., taxon ID)

    Returns:
        Path to cache file
    """
    # Create hash of key to handle special characters
    key_hash = hashlib.md5(key.encode(), usedforsecurity=False).hexdigest()
    cache_subdir = CACHE_DIR / cache_type
    cache_subdir.mkdir(exist_ok=True)
    return cache_subdir / f"{key_hash}.json"


def _load_from_cache(cache_type: str, key: str) -> dict[str, Any] | list[Any] | None:
    """Load data from cache file if it exists.

    Args:
        cache_type: Type of cache (e.g., "synonyms", "linkouts")
        key: Unique key for the cached item

    Returns:
        Cached data (dict or list) or None if not cached
    """
    cache_path = _get_cache_path(cache_type, key)
    if cache_path.exists():
        try:
            with cache_path.open() as f:
                return json.load(f)  # type: ignore[return-value, no-any-return]
        except (json.JSONDecodeError, OSError) as e:
            logger.debug(f"Failed to load cache for {cache_type}:{key}: {e}")
    return None


def _save_to_cache(cache_type: str, key: str, data: dict[str, Any] | list[Any]) -> None:
    """Save data to cache file.

    Args:
        cache_type: Type of cache (e.g., "synonyms", "linkouts")
        key: Unique key for the cached item
        data: Data to cache (dict or list)
    """
    cache_path = _get_cache_path(cache_type, key)
    try:
        with cache_path.open("w") as f:
            json.dump(data, f)
    except (OSError, TypeError) as e:
        logger.debug(f"Failed to save cache for {cache_type}:{key}: {e}")


def _make_request(
    url: str,
    params: dict,
    max_retries: int = 3,
) -> requests.Response | None:
    """Make NCBI API request with retry logic and API key support.

    Args:
        url: API endpoint URL
        params: Query parameters
        max_retries: Maximum number of retry attempts for rate limiting

    Returns:
        Response object or None if all retries failed
    """
    # Add API key if available (increases rate limit from 3 to 10 req/sec)
    if NCBI_API_KEY:
        params = {**params, "api_key": NCBI_API_KEY}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=NCBI_REQUEST_TIMEOUT)

            if response.status_code == 429:
                # Rate limited - wait and retry with exponential backoff
                wait_time = 2**attempt  # 1, 2, 4 seconds
                logger.warning(f"Rate limited (429), waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                wait_time = 2**attempt
                logger.warning(f"Rate limited, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue
            logger.debug(f"HTTP error fetching from NCBI: {e}")
            return None
        except requests.RequestException as e:
            logger.debug(f"Request error fetching from NCBI: {e}")
            return None

    logger.warning(f"Failed to fetch from NCBI after {max_retries} retries (rate limited)")
    return None


def fetch_ncbi_synonyms(taxon_id: int | str) -> NcbiTaxonData:
    """Fetch synonyms, related names, rank, and lineage from NCBI Taxonomy.

    Uses file-based caching to avoid redundant API calls.

    Args:
        taxon_id: NCBI Taxonomy ID (integer or string)

    Returns:
        NcbiTaxonData with synonyms, equivalent_names, includes, misspellings, authority (lists),
        rank (string, e.g., 'species', 'strain', 'subspecies'),
        species_taxon_id (species-level ancestor from lineage),
        and parent_taxon_id (immediate parent in taxonomy).
    """
    taxon_id_str = str(taxon_id)

    result: NcbiTaxonData = {
        "scientific_name": "",
        "synonyms": [],
        "equivalent_names": [],
        "includes": [],
        "misspellings": [],
        "authority": [],
        "rank": "",
        "species_taxon_id": "",
        "parent_taxon_id": "",
    }

    # Check cache first
    cached = _load_from_cache("synonyms", taxon_id_str)
    if cached is not None:
        logger.debug(f"Using cached NCBI synonyms for {taxon_id_str}")
        return cached  # type: ignore

    try:
        response = _make_request(
            NCBI_EFETCH_URL,
            params={"db": "taxonomy", "id": taxon_id_str, "retmode": "xml"},
        )
        if response is None:
            return result

        root = ET.fromstring(response.content)
        taxon = root.find(".//Taxon")
        if taxon is None:
            return result

        # Extract scientific name
        sci_name_elem = taxon.find("ScientificName")
        if sci_name_elem is not None and sci_name_elem.text:
            result["scientific_name"] = sci_name_elem.text

        # Extract taxonomic rank
        rank_elem = taxon.find("Rank")
        if rank_elem is not None and rank_elem.text:
            result["rank"] = rank_elem.text

        # Extract parent taxon ID
        parent_id_elem = taxon.find("ParentTaxId")
        if parent_id_elem is not None and parent_id_elem.text:
            result["parent_taxon_id"] = parent_id_elem.text

        # Extract species-level ancestor from LineageEx
        # LineageEx contains all ancestors with their ranks
        lineage_ex = taxon.find("LineageEx")
        if lineage_ex is not None:
            for ancestor in lineage_ex.findall("Taxon"):
                ancestor_rank = ancestor.find("Rank")
                ancestor_id = ancestor.find("TaxId")
                if (
                    ancestor_rank is not None
                    and ancestor_rank.text == "species"
                    and ancestor_id is not None
                    and ancestor_id.text
                ):
                    result["species_taxon_id"] = ancestor_id.text
                    break  # Take the first (most specific) species ancestor

        # If taxon itself is at species level or below, use its own ID as species_taxon_id
        # (unless we already found a species ancestor, which means this is subspecies/strain)
        if not result["species_taxon_id"] and result["rank"] == "species":
            result["species_taxon_id"] = str(taxon_id)

        other_names = taxon.find("OtherNames")
        if other_names is None:
            return result

        # Extract different name types
        for synonym in other_names.findall("Synonym"):
            if synonym.text:
                result["synonyms"].append(synonym.text)

        for equiv in other_names.findall("EquivalentName"):
            if equiv.text:
                result["equivalent_names"].append(equiv.text)

        for includes in other_names.findall("Includes"):
            if includes.text:
                result["includes"].append(includes.text)

        # Extract from Name elements with ClassCDE
        for name_elem in other_names.findall("Name"):
            class_cde = name_elem.find("ClassCDE")
            disp_name = name_elem.find("DispName")
            if class_cde is not None and disp_name is not None and disp_name.text:
                if class_cde.text == "misspelling":
                    result["misspellings"].append(disp_name.text)
                elif class_cde.text == "authority":
                    result["authority"].append(disp_name.text)

        # Save to cache
        _save_to_cache("synonyms", taxon_id_str, cast("dict[str, Any]", result))

    except ET.ParseError as e:
        logger.debug(f"Failed to parse NCBI synonyms for {taxon_id_str}: {e}")

    return result


def fetch_ncbi_batch(taxon_ids: list[str], batch_size: int = 50) -> dict[str, NcbiTaxonData]:
    """Fetch NCBI Taxonomy data for multiple taxa in batch.

    Args:
        taxon_ids: List of NCBI Taxonomy IDs
        batch_size: Number of IDs per request (default 50)

    Returns:
        Dictionary mapping taxon_id -> NcbiTaxonData
    """
    results: dict[str, NcbiTaxonData] = {}

    # Process in batches
    for i in range(0, len(taxon_ids), batch_size):
        batch = taxon_ids[i : i + batch_size]
        ids_param = ",".join(batch)

        try:
            response = _make_request(
                NCBI_EFETCH_URL,
                params={"db": "taxonomy", "id": ids_param, "retmode": "xml"},
            )
            if response is None:
                logger.warning(f"Failed to fetch NCBI batch starting at {i}")
                continue

            root = ET.fromstring(response.content)

            # Parse each Taxon element (direct children of TaxaSet)
            for taxon in root.findall("Taxon"):
                taxid_elem = taxon.find("TaxId")
                if taxid_elem is None or not taxid_elem.text:
                    continue

                taxid = taxid_elem.text
                data: NcbiTaxonData = {
                    "scientific_name": "",
                    "synonyms": [],
                    "equivalent_names": [],
                    "includes": [],
                    "misspellings": [],
                    "authority": [],
                    "rank": "",
                    "species_taxon_id": "",
                    "parent_taxon_id": "",
                }

                # Extract rank
                rank_elem = taxon.find("Rank")
                if rank_elem is not None and rank_elem.text:
                    data["rank"] = rank_elem.text

                # Extract parent taxon ID
                parent_elem = taxon.find("ParentTaxId")
                if parent_elem is not None and parent_elem.text:
                    data["parent_taxon_id"] = parent_elem.text

                # Extract scientific name
                sci_name_elem = taxon.find("ScientificName")
                if sci_name_elem is not None and sci_name_elem.text:
                    data["scientific_name"] = sci_name_elem.text

                # Extract species from lineage
                lineage_ex = taxon.find("LineageEx")
                if lineage_ex is not None:
                    for ancestor in lineage_ex.findall("Taxon"):
                        ancestor_rank = ancestor.find("Rank")
                        ancestor_id = ancestor.find("TaxId")
                        if (
                            ancestor_rank is not None
                            and ancestor_rank.text == "species"
                            and ancestor_id is not None
                            and ancestor_id.text
                        ):
                            data["species_taxon_id"] = ancestor_id.text
                            break

                # If taxon is species level, use its own ID
                if not data["species_taxon_id"] and data["rank"] == "species":
                    data["species_taxon_id"] = taxid

                # Extract synonyms from OtherNames
                other_names = taxon.find("OtherNames")
                if other_names is not None:
                    for syn in other_names.findall("Synonym"):
                        if syn.text:
                            data["synonyms"].append(syn.text)
                    for equiv in other_names.findall("EquivalentName"):
                        if equiv.text:
                            data["equivalent_names"].append(equiv.text)
                    for incl in other_names.findall("Includes"):
                        if incl.text:
                            data["includes"].append(incl.text)
                    for name_elem in other_names.findall("Name"):
                        class_cde = name_elem.find("ClassCDE")
                        disp_name = name_elem.find("DispName")
                        if class_cde is not None and disp_name is not None and disp_name.text:
                            if class_cde.text == "misspelling":
                                data["misspellings"].append(disp_name.text)
                            elif class_cde.text == "authority":
                                data["authority"].append(disp_name.text)

                results[taxid] = data

            # Small delay between batches to be nice to NCBI
            if i + batch_size < len(taxon_ids):
                time.sleep(0.5)

        except (requests.RequestException, ET.ParseError) as e:
            logger.warning(f"Failed to fetch NCBI batch starting at {i}: {e}")

    return results


def fetch_ncbi_linkouts(taxon_ids: list[str], batch_size: int = 20) -> dict[str, list[NcbiLinkout]]:
    """Fetch external linkouts from NCBI for multiple taxa.

    Uses the elink API with cmd=llinkslib to get external database links
    like BacDive, BioCyc, LPSN, etc.

    Uses file-based caching to avoid redundant API calls.

    Args:
        taxon_ids: List of NCBI Taxonomy IDs
        batch_size: Number of IDs per request (default 20, smaller for elink)

    Returns:
        Dictionary mapping taxon_id -> list of NcbiLinkout
    """
    results: dict[str, list[NcbiLinkout]] = {}

    # Check cache for each taxon ID
    uncached_ids = []
    for taxon_id in taxon_ids:
        cached = _load_from_cache("linkouts", taxon_id)
        if cached is not None:
            logger.debug(f"Using cached NCBI linkouts for {taxon_id}")
            results[taxon_id] = cached  # type: ignore
        else:
            uncached_ids.append(taxon_id)

    # Fetch uncached IDs in batches
    for i in range(0, len(uncached_ids), batch_size):
        batch = uncached_ids[i : i + batch_size]
        ids_param = ",".join(batch)

        try:
            response = _make_request(
                NCBI_ELINK_URL,
                params={"dbfrom": "taxonomy", "id": ids_param, "cmd": "llinkslib"},
                max_retries=3,
            )
            if response is None:
                continue

            root = ET.fromstring(response.content)

            # Parse each IdUrlSet
            for id_url_set in root.findall(".//IdUrlSet"):
                id_elem = id_url_set.find("Id")
                if id_elem is None or not id_elem.text:
                    continue

                taxid = id_elem.text
                linkouts: list[NcbiLinkout] = []

                for obj_url in id_url_set.findall("ObjUrl"):
                    url_elem = obj_url.find("Url")
                    name_elem = obj_url.find("LinkName")
                    provider_elem = obj_url.find("Provider/Name")

                    if url_elem is not None and url_elem.text:
                        url = url_elem.text
                        # Skip placeholder URLs
                        if "&base.url;" in url:
                            continue

                        linkout: NcbiLinkout = {
                            "provider": provider_elem.text or "" if provider_elem is not None else "",
                            "url": url,
                            "name": name_elem.text or "" if name_elem is not None else "",
                        }
                        linkouts.append(linkout)

                results[taxid] = linkouts
                # Save each taxon's linkouts to cache
                _save_to_cache("linkouts", taxid, linkouts)

            # Rate limit between batches
            if i + batch_size < len(uncached_ids):
                time.sleep(0.5)

        except ET.ParseError as e:
            logger.warning(f"Failed to parse NCBI linkouts batch starting at {i}: {e}")

    return results


def fetch_ncbi_entrez_links(taxon_ids: list[str], batch_size: int = 50) -> dict[str, dict[str, list[str]]]:
    """Fetch Entrez links to other NCBI databases for multiple taxa.

    Uses the elink API with cmd=acheck to find links to Assembly, BioProject, etc.

    Args:
        taxon_ids: List of NCBI Taxonomy IDs
        batch_size: Number of IDs per request

    Returns:
        Dictionary mapping taxon_id -> {db_name: [linked_ids]}
    """
    results: dict[str, dict[str, list[str]]] = {}

    # Databases we're interested in
    target_dbs = {"assembly", "bioproject", "biosample", "nuccore", "genome"}

    for i in range(0, len(taxon_ids), batch_size):
        batch = taxon_ids[i : i + batch_size]

        for taxid in batch:
            if taxid in results:
                continue

            try:
                response = _make_request(
                    NCBI_ELINK_URL,
                    params={"dbfrom": "taxonomy", "id": taxid, "cmd": "acheck"},
                )
                if response is None:
                    continue

                root = ET.fromstring(response.content)
                links: dict[str, list[str]] = {}

                for link_info in root.findall(".//LinkInfo"):
                    db_to = link_info.find("DbTo")
                    if db_to is not None and db_to.text in target_dbs and db_to.text not in links:
                        links[db_to.text] = []

                results[taxid] = links

            except ET.ParseError as e:
                logger.debug(f"Failed to parse Entrez links for {taxid}: {e}")

        # Rate limit between batches
        if i + batch_size < len(taxon_ids):
            time.sleep(0.3)

    return results


def extract_xrefs_from_linkouts(linkouts: list[NcbiLinkout]) -> list[str]:
    """Extract structured xrefs from NCBI linkouts.

    Parses URLs to extract database identifiers in CURIE format.

    Args:
        linkouts: List of NcbiLinkout from fetch_ncbi_linkouts

    Returns:
        List of xref CURIEs (e.g., "bacdive:13546", "biocyc:GCF_000346065")
    """
    xrefs: list[str] = []

    for linkout in linkouts:
        provider = linkout["provider"].lower()
        url = linkout["url"]

        # BacDive: https://bacdive.dsmz.de/strain/13546
        if "bacdive" in provider or "bacdive.dsmz.de" in url:
            match = re.search(r"/strain/(\d+)", url)
            if match:
                xrefs.append(f"bacdive:{match.group(1)}")

        # BioCyc: http://biocyc.org/organism-summary?object=GCF_000346065
        elif "biocyc" in provider:
            match = re.search(r"object=(GCF_\d+)", url)
            if match:
                xrefs.append(f"biocyc:{match.group(1)}")
            match = re.search(r"object=(\d+)", url)
            if match:
                xrefs.append(f"biocyc:taxon:{match.group(1)}")

        # LPSN: List of Prokaryotic names with Standing in Nomenclature
        elif "lpsn" in provider.lower() or "lpsn.dsmz.de" in url:
            # Extract species name from URL
            match = re.search(r"/species/([^/]+)", url)
            if match:
                xrefs.append(f"lpsn:{match.group(1)}")

    return list(set(xrefs))  # Deduplicate


def extract_genome_accessions_from_linkouts(linkouts: list[NcbiLinkout]) -> dict[str, list[str]]:
    """Extract genome accessions from NCBI linkouts.

    Parses URLs to extract genome database identifiers.

    Args:
        linkouts: List of NcbiLinkout from fetch_ncbi_linkouts

    Returns:
        Dictionary with keys: genome_accessions_img, genome_accessions_other
        Each value is a list of genome IDs
    """
    img_genomes: list[str] = []
    other_genomes: list[str] = []

    for linkout in linkouts:
        provider = linkout["provider"].lower()
        url = linkout["url"]

        # IMG: https://img.jgi.doe.gov/genome.php?id=2829760844
        if "integrated microbial genomes" in provider or "img.jgi.doe.gov" in url:
            match = re.search(r"[?&]id=(\d+)", url)
            if match:
                img_genomes.append(match.group(1))

        # GOLD: https://gold.jgi.doe.gov/organisms?...
        elif "genomes on line database" in provider or "gold.jgi.doe.gov" in url:
            match = re.search(r"Go\d+", url)
            if match:
                other_genomes.append(match.group(0))

    return {
        "genome_accessions_img": img_genomes,
        "genome_accessions_other": other_genomes,
    }
