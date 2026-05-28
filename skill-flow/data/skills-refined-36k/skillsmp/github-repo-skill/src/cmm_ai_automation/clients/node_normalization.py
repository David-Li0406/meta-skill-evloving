"""NodeNormalization API client.

A thin, typed wrapper around the NCATS Translator NodeNormalization API for
resolving chemical identifiers across multiple databases.

NodeNormalization provides cross-references between:
- ChEBI
- PubChem
- MESH
- DrugBank
- CHEMBL
- UNII
- CAS Registry Numbers
- InChIKey
- UMLS
- RxNorm
- KEGG

References:
    - API docs: https://nodenormalization-sri.renci.org/docs
    - GitHub: https://github.com/NCATSTranslator/NodeNormalization
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any

import requests

logger = logging.getLogger(__name__)

# Rate limit: be conservative with external API
DEFAULT_RATE_LIMIT_DELAY = 0.2


@dataclass
class NormalizedNode:
    """Result from a NodeNormalization lookup.

    Contains the canonical identifier and all equivalent identifiers
    from various databases.

    Attributes:
        canonical_id: The canonical/preferred identifier (e.g., "CHEBI:32599")
        canonical_label: Preferred name for the entity
        query_id: The identifier that was queried
        equivalent_ids: Dict mapping prefix to list of IDs (e.g., {"PUBCHEM.COMPOUND": ["12345"]})
        inchikey: InChIKey if available
        cas_rn: CAS Registry Number if available
        all_labels: All known labels/names for this entity
    """

    canonical_id: str
    canonical_label: str | None
    query_id: str
    equivalent_ids: dict[str, list[str]] = field(default_factory=dict)
    inchikey: str | None = None
    cas_rn: str | None = None
    all_labels: list[str] = field(default_factory=list)

    def get_ids_for_prefix(self, prefix: str) -> list[str]:
        """Get all IDs for a given prefix.

        Args:
            prefix: ID prefix like "PUBCHEM.COMPOUND", "CHEBI", "DRUGBANK", etc.

        Returns:
            List of IDs (without prefix) or empty list if none found
        """
        return self.equivalent_ids.get(prefix, [])

    def get_pubchem_cids(self) -> list[int]:
        """Get all PubChem CIDs."""
        ids = self.get_ids_for_prefix("PUBCHEM.COMPOUND")
        return [int(i.split(":")[-1]) for i in ids if i]

    def get_chebi_ids(self) -> list[str]:
        """Get all ChEBI IDs (without prefix)."""
        ids = self.get_ids_for_prefix("CHEBI")
        return [i.split(":")[-1] for i in ids if i]

    def get_mesh_ids(self) -> list[str]:
        """Get all MESH IDs."""
        ids = self.get_ids_for_prefix("MESH")
        return [i.split(":")[-1] for i in ids if i]

    def get_drugbank_ids(self) -> list[str]:
        """Get all DrugBank IDs."""
        ids = self.get_ids_for_prefix("DRUGBANK")
        return [i.split(":")[-1] for i in ids if i]

    def get_kegg_ids(self) -> list[str]:
        """Get all KEGG compound IDs."""
        ids = self.get_ids_for_prefix("KEGG.COMPOUND")
        return [i.split(":")[-1] for i in ids if i]

    def get_chembl_ids(self) -> list[str]:
        """Get all CHEMBL IDs."""
        ids = self.get_ids_for_prefix("CHEMBL.COMPOUND")
        return [i.split(":")[-1] for i in ids if i]

    def get_unii(self) -> str | None:
        """Get UNII (FDA Unique Ingredient Identifier)."""
        ids = self.get_ids_for_prefix("UNII")
        return ids[0].split(":")[-1] if ids else None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "canonical_id": self.canonical_id,
            "canonical_label": self.canonical_label,
            "query_id": self.query_id,
            "equivalent_ids": self.equivalent_ids,
            "inchikey": self.inchikey,
            "cas_rn": self.cas_rn,
            "all_labels": self.all_labels,
        }


@dataclass
class NormalizationError:
    """Error from a failed NodeNormalization lookup.

    Attributes:
        query_id: The identifier that was queried
        error_code: Error code
        error_message: Human-readable error message
    """

    query_id: str
    error_code: str
    error_message: str


class NodeNormalizationClient:
    """Client for NCATS Translator NodeNormalization API.

    Example:
        >>> client = NodeNormalizationClient()
        >>> result = client.normalize("CHEBI:32599")
        >>> if isinstance(result, NormalizedNode):
        ...     print(f"Canonical: {result.canonical_id}")
        ...     print(f"PubChem CIDs: {result.get_pubchem_cids()}")
        ...     print(f"CAS: {result.cas_rn}")
    """

    BASE_URL = "https://nodenormalization-sri.renci.org"

    def __init__(
        self,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        timeout: float = 30.0,
    ):
        """Initialize NodeNormalization client.

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

    def normalize(self, curie: str) -> NormalizedNode | NormalizationError:
        """Normalize a CURIE to get all equivalent identifiers.

        Args:
            curie: A CURIE like "CHEBI:32599", "PUBCHEM.COMPOUND:5793",
                   "CAS:50-99-7", "INCHIKEY:WQZGKKKJIJFFOK-GASJEMHNSA-N"

        Returns:
            NormalizedNode on success, NormalizationError on failure
        """
        url = f"{self.BASE_URL}/get_normalized_nodes"
        params = {"curie": curie}

        try:
            data = self._get(url, params)
        except requests.HTTPError as e:
            return NormalizationError(
                query_id=curie,
                error_code="HTTP_ERROR",
                error_message=str(e),
            )
        except requests.RequestException as e:
            return NormalizationError(
                query_id=curie,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        # Parse response
        # Response format: {curie: {id: {...}, equivalent_identifiers: [...], type: [...]}}
        node_data = data.get(curie)
        if not node_data:
            return NormalizationError(
                query_id=curie,
                error_code="NOT_FOUND",
                error_message=f"No normalization found for {curie}",
            )

        return self._parse_node(curie, node_data)

    def normalize_batch(self, curies: list[str]) -> dict[str, NormalizedNode | NormalizationError]:
        """Normalize multiple CURIEs in a single request.

        Args:
            curies: List of CURIEs to normalize

        Returns:
            Dict mapping each CURIE to its result (NormalizedNode or NormalizationError)
        """
        if not curies:
            return {}

        url = f"{self.BASE_URL}/get_normalized_nodes"
        # API accepts multiple curie params
        params = [("curie", c) for c in curies]

        try:
            self._wait_for_rate_limit()
            logger.debug(f"GET {url} with {len(curies)} curies")
            response = self._session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            # Return errors for all curies
            return {
                c: NormalizationError(
                    query_id=c,
                    error_code="REQUEST_ERROR",
                    error_message=str(e),
                )
                for c in curies
            }

        results: dict[str, NormalizedNode | NormalizationError] = {}
        for curie in curies:
            node_data = data.get(curie)
            if not node_data:
                results[curie] = NormalizationError(
                    query_id=curie,
                    error_code="NOT_FOUND",
                    error_message=f"No normalization found for {curie}",
                )
            else:
                results[curie] = self._parse_node(curie, node_data)

        return results

    def _parse_node(self, query_id: str, node_data: dict[str, Any]) -> NormalizedNode:
        """Parse API response into NormalizedNode."""
        # Get canonical ID and label
        id_info = node_data.get("id", {})
        canonical_id = id_info.get("identifier", query_id)
        canonical_label = id_info.get("label")

        # Parse equivalent identifiers
        equiv_ids = node_data.get("equivalent_identifiers", [])
        equivalent_ids: dict[str, list[str]] = {}
        all_labels: list[str] = []
        inchikey: str | None = None
        cas_rn: str | None = None

        # If query was by CAS, InChI, or InChIKey, prefer that value
        if query_id.startswith("CAS:"):
            cas_rn = query_id.split(":", 1)[1]
        elif query_id.startswith("INCHIKEY:"):
            inchikey = query_id.split(":", 1)[1]

        for equiv in equiv_ids:
            identifier = equiv.get("identifier", "")
            label = equiv.get("label")

            if label:
                all_labels.append(label)

            # Extract prefix
            if ":" in identifier:
                prefix = identifier.split(":")[0]
                if prefix not in equivalent_ids:
                    equivalent_ids[prefix] = []
                equivalent_ids[prefix].append(identifier)

                # Extract special identifiers (only if not already set from query_id)
                if prefix == "INCHIKEY" and inchikey is None:
                    inchikey = identifier.split(":")[-1]
                elif prefix == "CAS" and cas_rn is None:
                    # Take the first CAS number if not queried by CAS
                    cas_rn = identifier.split(":")[-1]

        return NormalizedNode(
            canonical_id=canonical_id,
            canonical_label=canonical_label,
            query_id=query_id,
            equivalent_ids=equivalent_ids,
            inchikey=inchikey,
            cas_rn=cas_rn,
            all_labels=list(set(all_labels)),  # dedupe
        )

    def normalize_by_inchikey(self, inchikey: str) -> NormalizedNode | NormalizationError:
        """Normalize using an InChIKey.

        Args:
            inchikey: InChIKey string (27 characters, e.g., "WQZGKKKJIJFFOK-GASJEMHNSA-N")

        Returns:
            NormalizedNode on success, NormalizationError on failure
        """
        curie = f"INCHIKEY:{inchikey}"
        return self.normalize(curie)

    def normalize_by_cas(self, cas_rn: str) -> NormalizedNode | NormalizationError:
        """Normalize using a CAS Registry Number.

        Args:
            cas_rn: CAS Registry Number (e.g., "50-99-7")

        Returns:
            NormalizedNode on success, NormalizationError on failure
        """
        curie = f"CAS:{cas_rn}"
        return self.normalize(curie)

    def normalize_by_chebi(self, chebi_id: str | int) -> NormalizedNode | NormalizationError:
        """Normalize using a ChEBI ID.

        Args:
            chebi_id: ChEBI ID (e.g., "32599" or 32599, with or without "CHEBI:" prefix)

        Returns:
            NormalizedNode on success, NormalizationError on failure
        """
        # Handle various input formats
        chebi_str = str(chebi_id)
        curie = chebi_str.upper() if chebi_str.upper().startswith("CHEBI:") else f"CHEBI:{chebi_str}"
        return self.normalize(curie)

    def normalize_by_pubchem(self, cid: int) -> NormalizedNode | NormalizationError:
        """Normalize using a PubChem CID.

        Args:
            cid: PubChem Compound ID

        Returns:
            NormalizedNode on success, NormalizationError on failure
        """
        curie = f"PUBCHEM.COMPOUND:{cid}"
        return self.normalize(curie)
