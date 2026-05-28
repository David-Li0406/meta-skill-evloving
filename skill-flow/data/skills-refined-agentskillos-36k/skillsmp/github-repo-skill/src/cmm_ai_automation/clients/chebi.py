"""ChEBI 2.0 REST API client.

A typed wrapper around the ChEBI 2.0 backend REST API for comprehensive
chemical entity lookups.

ChEBI is the authoritative source for ChEBI IDs, ontology relationships,
and biological/chemical roles.

This client uses the new ChEBI 2.0 REST API (launched October 2025) which
provides much richer data than the legacy SOAP service or OLS4.

References:
    - ChEBI: https://www.ebi.ac.uk/chebi/
    - API schema: https://www.ebi.ac.uk/chebi/backend/api/schema/
"""

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

import requests

logger = logging.getLogger(__name__)

# Rate limit: be conservative with external API
DEFAULT_RATE_LIMIT_DELAY = 0.2


@dataclass
class ChEBIRole:
    """A role classification from ChEBI.

    Roles can be biological, chemical, or application-related.
    """

    chebi_id: str
    name: str
    definition: str | None = None
    is_biological_role: bool = False
    is_chemical_role: bool = False
    is_application: bool = False


@dataclass
class ChEBIRelation:
    """An ontology relation from ChEBI."""

    relation_type: str  # e.g., "is a", "has role", "has functional parent"
    target_chebi_id: str
    target_name: str


@dataclass
class ChEBIDatabaseRef:
    """A database cross-reference from ChEBI."""

    database: str  # e.g., "CAS", "KEGG", "PubChem"
    accession: str
    source: str | None = None
    url: str | None = None


@dataclass
class ChEBICompound:
    """Complete compound information from ChEBI 2.0 API.

    ChEBI is the authoritative source for this data.

    Attributes:
        chebi_id: ChEBI accession (e.g., "CHEBI:17634")
        name: Primary name (may contain HTML)
        ascii_name: Clean ASCII name
        definition: Term definition
        stars: Curation level (1-3, 3 is most curated)
        formula: Molecular formula
        mass: Average molecular mass
        monoisotopic_mass: Monoisotopic mass
        charge: Formal charge
        inchi: InChI string (if available)
        inchikey: InChIKey (if available)
        smiles: SMILES string (if available)
        synonyms: List of synonym names
        secondary_ids: List of secondary ChEBI IDs
        roles: List of role classifications
        parents: List of parent relations (is_a)
        has_roles: List of has_role relations
        database_refs: Dictionary of database cross-references
        outgoing_relations: All outgoing ontology relations
        incoming_relations: All incoming ontology relations
    """

    chebi_id: str
    name: str
    ascii_name: str | None = None
    definition: str | None = None
    stars: int | None = None
    formula: str | None = None
    mass: float | None = None
    monoisotopic_mass: float | None = None
    charge: int | None = None
    inchi: str | None = None
    inchikey: str | None = None
    smiles: str | None = None
    synonyms: list[str] = field(default_factory=list)
    secondary_ids: list[str] = field(default_factory=list)
    roles: list[ChEBIRole] = field(default_factory=list)
    parents: list[ChEBIRelation] = field(default_factory=list)
    has_roles: list[ChEBIRelation] = field(default_factory=list)
    database_refs: dict[str, list[ChEBIDatabaseRef]] = field(default_factory=dict)
    outgoing_relations: list[ChEBIRelation] = field(default_factory=list)
    incoming_relations: list[ChEBIRelation] = field(default_factory=list)

    def get_cas_numbers(self) -> list[str]:
        """Get all CAS Registry Numbers."""
        cas_refs = self.database_refs.get("CAS", [])
        return list({ref.accession for ref in cas_refs})

    def get_biological_roles(self) -> list[ChEBIRole]:
        """Get biological roles only."""
        return [r for r in self.roles if r.is_biological_role]

    def get_chemical_roles(self) -> list[ChEBIRole]:
        """Get chemical roles only."""
        return [r for r in self.roles if r.is_chemical_role]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "chebi_id": self.chebi_id,
            "name": self.name,
            "ascii_name": self.ascii_name,
            "definition": self.definition,
            "stars": self.stars,
            "formula": self.formula,
            "mass": self.mass,
            "monoisotopic_mass": self.monoisotopic_mass,
            "charge": self.charge,
            "inchi": self.inchi,
            "inchikey": self.inchikey,
            "smiles": self.smiles,
            "synonyms": self.synonyms,
            "secondary_ids": self.secondary_ids,
            "roles": [
                {
                    "chebi_id": r.chebi_id,
                    "name": r.name,
                    "is_biological": r.is_biological_role,
                    "is_chemical": r.is_chemical_role,
                }
                for r in self.roles
            ],
            "cas_numbers": self.get_cas_numbers(),
        }


@dataclass
class ChEBISearchResult:
    """A search result from ChEBI text search."""

    chebi_id: str
    name: str
    ascii_name: str | None
    definition: str | None
    stars: int | None
    formula: str | None
    mass: float | None
    score: float  # Elasticsearch relevance score


@dataclass
class ChEBILookupError:
    """Error from a failed ChEBI lookup."""

    query: str
    error_code: str
    error_message: str


class ChEBIClient:
    """Client for ChEBI 2.0 REST API.

    ChEBI is the authoritative source for ChEBI term information,
    ontology relationships, and biological/chemical roles.

    Example:
        >>> client = ChEBIClient()
        >>> result = client.get_compound("CHEBI:17634")
        >>> if isinstance(result, ChEBICompound):
        ...     print(f"Name: {result.ascii_name}")
        ...     print(f"Roles: {[r.name for r in result.roles]}")
        ...     print(f"CAS: {result.get_cas_numbers()}")

        >>> # Search by name
        >>> results = client.search("glucose")
        >>> for r in results[:5]:
        ...     print(f"{r.chebi_id}: {r.ascii_name}")
    """

    BASE_URL = "https://www.ebi.ac.uk/chebi/backend/api"

    def __init__(
        self,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        timeout: float = 30.0,
    ):
        """Initialize ChEBI client.

        Args:
            rate_limit_delay: Seconds to wait between requests (default: 0.2)
            timeout: Request timeout in seconds (default: 30)
        """
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self._last_request_time: float = 0
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "cmm-ai-automation/0.1.0 (https://github.com/turbomam/cmm-ai-automation)",
            }
        )

    def _wait_for_rate_limit(self) -> None:
        """Wait if needed to respect rate limit."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request with rate limiting."""
        self._wait_for_rate_limit()
        logger.debug(f"GET {url} params={params}")
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def get_compound(self, chebi_id: str | int) -> ChEBICompound | ChEBILookupError:
        """Get complete compound information by ChEBI ID.

        ChEBI is authoritative for this data.

        Args:
            chebi_id: ChEBI ID (e.g., "CHEBI:17634", "17634", or 17634)

        Returns:
            ChEBICompound on success, ChEBILookupError on failure
        """
        # Normalize the ChEBI ID
        chebi_str = str(chebi_id).upper()
        chebi_numeric = chebi_str.split(":")[1] if chebi_str.startswith("CHEBI:") else chebi_str

        url = f"{self.BASE_URL}/public/compound/{chebi_numeric}/"

        try:
            data = self._get(url)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return ChEBILookupError(
                    query=f"CHEBI:{chebi_numeric}",
                    error_code="NOT_FOUND",
                    error_message=f"ChEBI compound CHEBI:{chebi_numeric} not found",
                )
            return ChEBILookupError(
                query=f"CHEBI:{chebi_numeric}",
                error_code="HTTP_ERROR",
                error_message=str(e),
            )
        except requests.RequestException as e:
            return ChEBILookupError(
                query=f"CHEBI:{chebi_numeric}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        return self._parse_compound(data)

    def search(
        self,
        query: str,
        page: int = 1,
        size: int = 20,
    ) -> list[ChEBISearchResult] | ChEBILookupError:
        """Search ChEBI by name, synonym, formula, InChI, SMILES, etc.

        Args:
            query: Search term (name, synonym, formula, ID, InChI, SMILES)
            page: Page number (1-indexed)
            size: Results per page (max ~100)

        Returns:
            List of ChEBISearchResult on success, ChEBILookupError on failure
        """
        url = f"{self.BASE_URL}/public/es_search/"
        params = {
            "term": query,
            "page": page,
            "size": size,
        }

        try:
            data = self._get(url, params)
        except requests.HTTPError as e:
            # Extract HTTP status code if available
            status_code = e.response.status_code if e.response is not None else None
            return ChEBILookupError(
                query=query,
                error_code=str(status_code) if status_code else "HTTP_ERROR",
                error_message=str(e),
            )
        except requests.RequestException as e:
            return ChEBILookupError(
                query=query,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        results = []
        for hit in data.get("results", []):
            source = hit.get("_source", {})
            results.append(
                ChEBISearchResult(
                    chebi_id=source.get("chebi_accession", ""),
                    name=source.get("name", ""),
                    ascii_name=source.get("ascii_name"),
                    definition=source.get("definition"),
                    stars=source.get("stars"),
                    formula=source.get("formula"),
                    mass=source.get("mass"),
                    score=hit.get("_score", 0.0),
                )
            )

        return results

    def search_exact(self, name: str) -> ChEBISearchResult | None | ChEBILookupError:
        """Search for an exact name match.

        Args:
            name: Exact name to search for

        Returns:
            ChEBISearchResult if found with exact match, None if not found,
            ChEBILookupError on failure (network errors, API errors, etc., but not "not found")
        """
        # Try searching with the exact name first
        results = self.search(name, size=20)
        if isinstance(results, ChEBILookupError):
            # If it's a 404 "not found", treat as None (no results)
            if results.error_code == "404":
                return None
            # Other errors (network, API) should be returned as errors
            return results

        # Look for exact match (case-insensitive)
        name_lower = name.lower()
        for result in results:
            if result.ascii_name and result.ascii_name.lower() == name_lower:
                return result
            if result.name and _strip_html(result.name).lower() == name_lower:
                return result

        # If no exact match found with specific term, try a broader search
        # by removing stereochemistry prefixes (D-, L-, etc.)
        if name.startswith(("D-", "L-", "d-", "l-")):
            broader_name = name[2:]
            results = self.search(broader_name, size=20)
            if isinstance(results, ChEBILookupError):
                # Again, treat 404 as no results
                if results.error_code == "404":
                    return None
                return results

            # Look for exact match in broader results
            for result in results:
                if result.ascii_name and result.ascii_name.lower() == name_lower:
                    return result
                if result.name and _strip_html(result.name).lower() == name_lower:
                    return result

        return None

    def get_compounds_batch(self, chebi_ids: list[str | int]) -> dict[str, ChEBICompound | ChEBILookupError]:
        """Get multiple compounds (makes individual requests).

        Args:
            chebi_ids: List of ChEBI IDs

        Returns:
            Dict mapping each ID to its result
        """
        results = {}
        for chebi_id in chebi_ids:
            normalized = _normalize_chebi_id(chebi_id)
            results[normalized] = self.get_compound(chebi_id)
        return results

    def _parse_compound(self, data: dict[str, Any]) -> ChEBICompound:
        """Parse API response into ChEBICompound."""
        chebi_id = data.get("chebi_accession", "")

        # Parse chemical data
        chem_data = data.get("chemical_data") or {}
        formula = chem_data.get("formula")
        mass = _to_float(chem_data.get("mass"))
        monoisotopic_mass = _to_float(chem_data.get("monoisotopic_mass"))
        charge = chem_data.get("charge")

        # Parse names/synonyms
        synonyms = []
        names_data = data.get("names") or {}
        for _name_type, name_list in names_data.items():
            for name_entry in name_list:
                ascii_name = name_entry.get("ascii_name")
                if ascii_name:
                    synonyms.append(ascii_name)

        # Parse roles
        roles = []
        for role_data in data.get("roles_classification") or []:
            roles.append(
                ChEBIRole(
                    chebi_id=f"CHEBI:{role_data.get('id', '')}",
                    name=_strip_html(role_data.get("name", "")),
                    definition=role_data.get("definition"),
                    is_biological_role=role_data.get("biological_role", False),
                    is_chemical_role=role_data.get("chemical_role", False),
                    is_application=role_data.get("application", False),
                )
            )

        # Parse database references
        database_refs: dict[str, list[ChEBIDatabaseRef]] = {}
        for db_type, ref_list in (data.get("database_accessions") or {}).items():
            database_refs[db_type] = []
            for ref in ref_list:
                database_refs[db_type].append(
                    ChEBIDatabaseRef(
                        database=db_type,
                        accession=ref.get("accession_number", ""),
                        source=ref.get("source_name"),
                        url=ref.get("url"),
                    )
                )

        # Parse ontology relations
        outgoing_relations = []
        incoming_relations = []
        parents = []
        has_roles = []

        ont_data = data.get("ontology_relations") or {}
        for rel in ont_data.get("outgoing_relations", []):
            relation = ChEBIRelation(
                relation_type=rel.get("relation_type", ""),
                target_chebi_id=f"CHEBI:{rel.get('final_id', '')}",
                target_name=_strip_html(rel.get("final_name", "")),
            )
            outgoing_relations.append(relation)

            if rel.get("relation_type") == "is a":
                parents.append(relation)
            elif rel.get("relation_type") == "has role":
                has_roles.append(relation)

        for rel in ont_data.get("incoming_relations", []):
            incoming_relations.append(
                ChEBIRelation(
                    relation_type=rel.get("relation_type", ""),
                    target_chebi_id=f"CHEBI:{rel.get('init_id', '')}",
                    target_name=_strip_html(rel.get("init_name", "")),
                )
            )

        return ChEBICompound(
            chebi_id=chebi_id,
            name=data.get("name", ""),
            ascii_name=data.get("ascii_name"),
            definition=data.get("definition"),
            stars=data.get("stars"),
            formula=formula,
            mass=mass,
            monoisotopic_mass=monoisotopic_mass,
            charge=charge,
            synonyms=list(set(synonyms)),  # dedupe
            secondary_ids=data.get("secondary_ids", []),
            roles=roles,
            parents=parents,
            has_roles=has_roles,
            database_refs=database_refs,
            outgoing_relations=outgoing_relations,
            incoming_relations=incoming_relations,
        )


def _strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r"<[^>]+>", "", text)


def _to_float(value: Any) -> float | None:
    """Safely convert to float."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _normalize_chebi_id(chebi_id: str | int) -> str:
    """Normalize a ChEBI ID to CHEBI:XXXXX format."""
    chebi_str = str(chebi_id).upper()
    if chebi_str.startswith("CHEBI:"):
        return chebi_str
    return f"CHEBI:{chebi_str}"
