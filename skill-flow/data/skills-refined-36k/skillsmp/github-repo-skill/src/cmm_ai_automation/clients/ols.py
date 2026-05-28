"""OLS4 (Ontology Lookup Service) API client.

A thin, typed wrapper around the EBI OLS4 API for ChEBI and other ontology lookups.
OLS4 is the authoritative source for ChEBI term information.

References:
    - OLS4 API docs: https://www.ebi.ac.uk/ols4/api
    - ChEBI: https://www.ebi.ac.uk/chebi/
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote

import requests

logger = logging.getLogger(__name__)

# Rate limit: be conservative with external API
DEFAULT_RATE_LIMIT_DELAY = 0.2

# ChEBI ontology ID in OLS
CHEBI_ONTOLOGY_ID = "chebi"


@dataclass
class ChEBITerm:
    """Result from a ChEBI term lookup via OLS4.

    ChEBI is the authoritative source for ChEBI IDs and functional classifications.

    Attributes:
        chebi_id: ChEBI ID (e.g., "CHEBI:17634")
        label: Primary/preferred name
        description: Term description/definition
        synonyms: List of synonym strings
        inchikey: InChIKey if available
        inchi: InChI string if available
        smiles: SMILES string if available
        formula: Molecular formula if available
        mass: Molecular mass if available
        charge: Formal charge if available
        star: ChEBI star rating (1-3, indicates curation level)
        is_obsolete: Whether the term is obsolete
        parent_ids: Parent ChEBI IDs (is_a relationships)
        has_role: List of role ChEBI IDs (has_role relationships)
        has_functional_parent: List of functional parent ChEBI IDs
        xrefs: Cross-references to other databases
    """

    chebi_id: str
    label: str | None = None
    description: str | None = None
    synonyms: list[str] = field(default_factory=list)
    inchikey: str | None = None
    inchi: str | None = None
    smiles: str | None = None
    formula: str | None = None
    mass: float | None = None
    charge: int | None = None
    star: int | None = None
    is_obsolete: bool = False
    parent_ids: list[str] = field(default_factory=list)
    has_role: list[str] = field(default_factory=list)
    has_functional_parent: list[str] = field(default_factory=list)
    xrefs: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "chebi_id": self.chebi_id,
            "label": self.label,
            "description": self.description,
            "synonyms": self.synonyms,
            "inchikey": self.inchikey,
            "inchi": self.inchi,
            "smiles": self.smiles,
            "formula": self.formula,
            "mass": self.mass,
            "charge": self.charge,
            "star": self.star,
            "is_obsolete": self.is_obsolete,
            "parent_ids": self.parent_ids,
            "has_role": self.has_role,
            "has_functional_parent": self.has_functional_parent,
            "xrefs": self.xrefs,
        }


@dataclass
class OLSSearchResult:
    """A search result from OLS4."""

    iri: str
    label: str | None
    short_form: str  # e.g., "CHEBI_17634"
    ontology_name: str  # e.g., "chebi"
    description: str | None = None
    is_obsolete: bool = False

    @property
    def curie(self) -> str:
        """Get CURIE format (e.g., CHEBI:17634)."""
        return self.short_form.replace("_", ":")


@dataclass
class OLSLookupError:
    """Error from a failed OLS lookup.

    Attributes:
        query: The query that was made
        error_code: Error code
        error_message: Human-readable error message
    """

    query: str
    error_code: str
    error_message: str


class OLSClient:
    """Client for EBI OLS4 API.

    Primary use is for ChEBI lookups, which is the authoritative source
    for ChEBI term information.

    Example:
        >>> client = OLSClient()
        >>> result = client.get_chebi_term("CHEBI:17634")
        >>> if isinstance(result, ChEBITerm):
        ...     print(f"Label: {result.label}")
        ...     print(f"Roles: {result.has_role}")
    """

    BASE_URL = "https://www.ebi.ac.uk/ols4/api"

    def __init__(
        self,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        timeout: float = 30.0,
    ):
        """Initialize OLS client.

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
        """Make a GET request with rate limiting.

        Args:
            url: Full URL to fetch
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            requests.RequestException: On network errors
        """
        self._wait_for_rate_limit()
        logger.debug(f"GET {url} params={params}")
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def get_chebi_term(self, chebi_id: str | int) -> ChEBITerm | OLSLookupError:
        """Look up a ChEBI term by ID.

        ChEBI/OLS4 is authoritative for ChEBI term information.

        Args:
            chebi_id: ChEBI ID (e.g., "CHEBI:17634", "17634", or 17634)

        Returns:
            ChEBITerm on success, OLSLookupError on failure
        """
        # Normalize the ChEBI ID
        chebi_str = str(chebi_id).upper()
        chebi_numeric = chebi_str.split(":")[1] if chebi_str.startswith("CHEBI:") else chebi_str

        # Construct the IRI for the ChEBI term
        iri = f"http://purl.obolibrary.org/obo/CHEBI_{chebi_numeric}"
        encoded_iri = quote(quote(iri, safe=""), safe="")

        url = f"{self.BASE_URL}/ontologies/{CHEBI_ONTOLOGY_ID}/terms/{encoded_iri}"

        try:
            data = self._get(url)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return OLSLookupError(
                    query=f"CHEBI:{chebi_numeric}",
                    error_code="NOT_FOUND",
                    error_message=f"ChEBI term CHEBI:{chebi_numeric} not found",
                )
            return OLSLookupError(
                query=f"CHEBI:{chebi_numeric}",
                error_code="HTTP_ERROR",
                error_message=str(e),
            )
        except requests.RequestException as e:
            return OLSLookupError(
                query=f"CHEBI:{chebi_numeric}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        return self._parse_chebi_term(f"CHEBI:{chebi_numeric}", data)

    def _parse_chebi_term(self, chebi_id: str, data: dict[str, Any]) -> ChEBITerm:
        """Parse OLS4 response into ChEBITerm."""
        # Get basic info
        label = data.get("label")
        description_list = data.get("description", [])
        description = description_list[0] if description_list else None
        synonyms = data.get("synonyms", [])
        is_obsolete = data.get("is_obsolete", False)

        # Get annotation properties
        annotation = data.get("annotation", {})

        # Extract chemical properties from annotations
        inchikey = _get_first(annotation.get("inchikey", []))
        inchi = _get_first(annotation.get("inchi", []))
        smiles = _get_first(annotation.get("smiles", []))
        formula = _get_first(annotation.get("formula", []))

        mass_str = _get_first(annotation.get("mass", []))
        mass = _to_float(mass_str) if mass_str else None

        charge_str = _get_first(annotation.get("charge", []))
        charge = _to_int(charge_str) if charge_str else None

        star_str = _get_first(annotation.get("star", []))
        star = _to_int(star_str) if star_str else None

        # Extract relationships from linked entities
        # Note: OLS4 structure may vary; we'll parse what's available
        parent_ids: list[str] = []
        has_role: list[str] = []
        has_functional_parent: list[str] = []
        xrefs: dict[str, list[str]] = {}

        # Try to get cross-references from annotation
        for key, values in annotation.items():
            if key.startswith("database_cross_reference"):
                for val in values:
                    if ":" in val:
                        prefix = val.split(":")[0]
                        if prefix not in xrefs:
                            xrefs[prefix] = []
                        xrefs[prefix].append(val)

        # Get hierarchical relations if available
        links = data.get("_links", {})
        if "hierarchicalParents" in links:
            # Would need additional API call to resolve parents
            pass

        return ChEBITerm(
            chebi_id=chebi_id,
            label=label,
            description=description,
            synonyms=synonyms,
            inchikey=inchikey,
            inchi=inchi,
            smiles=smiles,
            formula=formula,
            mass=mass,
            charge=charge,
            star=star,
            is_obsolete=is_obsolete,
            parent_ids=parent_ids,
            has_role=has_role,
            has_functional_parent=has_functional_parent,
            xrefs=xrefs,
        )

    def search_chebi(
        self,
        query: str,
        exact: bool = False,
        include_obsolete: bool = False,
        rows: int = 10,
    ) -> list[OLSSearchResult] | OLSLookupError:
        """Search ChEBI terms by name/label.

        Args:
            query: Search query (name, synonym, etc.)
            exact: If True, require exact match
            include_obsolete: If True, include obsolete terms
            rows: Maximum number of results to return

        Returns:
            List of OLSSearchResult on success, OLSLookupError on failure
        """
        url = f"{self.BASE_URL}/search"
        params: dict[str, Any] = {
            "q": query,
            "ontology": CHEBI_ONTOLOGY_ID,
            "rows": rows,
        }

        if exact:
            params["exact"] = "true"

        if not include_obsolete:
            params["obsoletes"] = "false"

        try:
            data = self._get(url, params)
        except requests.HTTPError as e:
            return OLSLookupError(
                query=query,
                error_code="HTTP_ERROR",
                error_message=str(e),
            )
        except requests.RequestException as e:
            return OLSLookupError(
                query=query,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        # Parse search results
        results: list[OLSSearchResult] = []
        response = data.get("response", {})
        docs = response.get("docs", [])

        for doc in docs:
            iri = doc.get("iri", "")
            label = doc.get("label")
            short_form = doc.get("short_form", "")
            ontology = doc.get("ontology_name", "")
            desc_list = doc.get("description", [])
            description = desc_list[0] if desc_list else None
            is_obsolete = doc.get("is_obsolete", False)

            results.append(
                OLSSearchResult(
                    iri=iri,
                    label=label,
                    short_form=short_form,
                    ontology_name=ontology,
                    description=description,
                    is_obsolete=is_obsolete,
                )
            )

        return results

    def search_chebi_exact(self, name: str) -> OLSSearchResult | None | OLSLookupError:
        """Search for an exact ChEBI term match by name.

        Args:
            name: Exact name to search for

        Returns:
            OLSSearchResult if found, None if not found, OLSLookupError on failure
        """
        result = self.search_chebi(name, exact=True, rows=1)
        if isinstance(result, OLSLookupError):
            return result
        return result[0] if result else None

    def get_chebi_parents(self, chebi_id: str | int) -> list[str] | OLSLookupError:
        """Get parent terms for a ChEBI ID (is_a relationships).

        Args:
            chebi_id: ChEBI ID

        Returns:
            List of parent ChEBI IDs, or OLSLookupError on failure
        """
        # Normalize the ChEBI ID
        chebi_str = str(chebi_id).upper()
        chebi_numeric = chebi_str.split(":")[1] if chebi_str.startswith("CHEBI:") else chebi_str

        iri = f"http://purl.obolibrary.org/obo/CHEBI_{chebi_numeric}"
        encoded_iri = quote(quote(iri, safe=""), safe="")

        url = f"{self.BASE_URL}/ontologies/{CHEBI_ONTOLOGY_ID}/terms/{encoded_iri}/hierarchicalParents"

        try:
            data = self._get(url)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return OLSLookupError(
                    query=f"CHEBI:{chebi_numeric}",
                    error_code="NOT_FOUND",
                    error_message=f"ChEBI term CHEBI:{chebi_numeric} not found",
                )
            return OLSLookupError(
                query=f"CHEBI:{chebi_numeric}",
                error_code="HTTP_ERROR",
                error_message=str(e),
            )
        except requests.RequestException as e:
            return OLSLookupError(
                query=f"CHEBI:{chebi_numeric}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        # Parse parent terms
        parents: list[str] = []
        embedded = data.get("_embedded", {})
        terms = embedded.get("terms", [])

        for term in terms:
            short_form = term.get("short_form", "")
            if short_form.startswith("CHEBI_"):
                parents.append(short_form.replace("_", ":"))

        return parents


def _get_first(values: list[Any]) -> Any | None:
    """Get first element of list or None if empty."""
    return values[0] if values else None


def _to_float(value: Any) -> float | None:
    """Safely convert to float."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _to_int(value: Any) -> int | None:
    """Safely convert to int."""
    if value is None:
        return None
    try:
        return int(float(value))  # Handle "3.0" style strings
    except (ValueError, TypeError):
        return None
