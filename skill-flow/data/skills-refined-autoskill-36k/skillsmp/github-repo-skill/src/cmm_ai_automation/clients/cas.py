"""CAS Common Chemistry API client.

A thin, typed wrapper around the CAS Common Chemistry API for compound lookups.
This API is particularly good at handling undefined mixtures like peptone, yeast extract, etc.

References:
    - API docs: https://commonchemistry.cas.org/api
    - API signup: https://www.cas.org/services/commonchemistry-api
"""

import contextlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import requests

logger = logging.getLogger(__name__)

# CAS API base URL
BASE_URL = "https://commonchemistry.cas.org/api"

# Rate limit delay (be conservative)
DEFAULT_RATE_LIMIT_DELAY = 0.5

# Regex pattern for HTML tags (CAS API returns formulas with <sub> tags)
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass
class CASResult:
    """Result from a CAS Common Chemistry lookup.

    Attributes:
        rn: CAS Registry Number (e.g., "50-99-7" for glucose)
        name: Primary name
        name_queried: The name we searched for (not from CAS)
        molecular_formula: Chemical formula (may be "Unspecified" for mixtures)
        molecular_mass: Molecular mass (may be None for mixtures)
        inchi: InChI string (if available)
        inchikey: InChIKey (if available)
        smiles: SMILES string (if available)
        synonyms: List of synonym names
        is_mixture: True if this is an undefined mixture
    """

    rn: str
    name: str
    name_queried: str
    molecular_formula: str | None = None
    molecular_mass: float | None = None
    inchi: str | None = None
    inchikey: str | None = None
    smiles: str | None = None
    synonyms: list[str] | None = None
    is_mixture: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "cas_rn": self.rn,
            "cas_name": self.name,
            "name_queried": self.name_queried,
            "cas_molecular_formula": self.molecular_formula,
            "cas_molecular_mass": self.molecular_mass,
            "cas_inchi": self.inchi,
            "cas_inchikey": self.inchikey,
            "cas_smiles": self.smiles,
            "cas_is_mixture": self.is_mixture,
        }


@dataclass
class CASLookupError:
    """Error from a failed CAS lookup.

    Attributes:
        name_queried: The name we searched for
        error_code: Error code
        error_message: Human-readable error message
    """

    name_queried: str
    error_code: str
    error_message: str


class CASClient:
    """Client for CAS Common Chemistry API.

    Requires an API key, obtained from:
    https://www.cas.org/services/commonchemistry-api

    The API key should be set in the environment variable CAS_API_KEY
    or passed directly to the constructor.

    Example:
        >>> client = CASClient()
        >>> result = client.search_by_name("glucose")
        >>> if isinstance(result, list) and result:
        ...     print(f"CAS RN: {result[0].rn}")
        CAS RN: 50-99-7
    """

    def __init__(
        self,
        api_key: str | None = None,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        timeout: float = 30.0,
    ):
        """Initialize CAS client.

        Args:
            api_key: CAS API key. If None, reads from CAS_API_KEY environment variable.
            rate_limit_delay: Seconds to wait between requests (default: 0.5)
            timeout: Request timeout in seconds (default: 30)

        Raises:
            ValueError: If no API key is provided or found in environment
        """
        self.api_key = api_key or os.environ.get("CAS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CAS API key required. Set CAS_API_KEY environment variable or pass api_key to constructor."
            )

        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self._last_request_time: float = 0
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "X-API-KEY": self.api_key,
                "User-Agent": "cmm-ai-automation/0.1.0 (https://github.com/turbomam/cmm-ai-automation)",
            }
        )

    def _wait_for_rate_limit(self) -> None:
        """Wait if needed to respect rate limit."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _get(self, url: str) -> dict[str, Any]:
        """Make a GET request with rate limiting.

        Args:
            url: Full URL to fetch

        Returns:
            Parsed JSON response

        Raises:
            requests.RequestException: On network errors
        """
        self._wait_for_rate_limit()
        logger.debug(f"GET {url}")
        response = self._session.get(url, timeout=self.timeout)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def search_by_name(self, name: str) -> list[CASResult] | CASLookupError:
        """Search for compounds by name.

        Args:
            name: Chemical name to search (e.g., "glucose", "peptone")

        Returns:
            List of CASResult on success (may be empty), CASLookupError on failure
        """
        encoded_name = quote(name)
        url = f"{BASE_URL}/search?q={encoded_name}"

        try:
            data = self._get(url)
        except requests.HTTPError as e:
            try:
                error_data = e.response.json()
                return CASLookupError(
                    name_queried=name,
                    error_code=str(e.response.status_code),
                    error_message=error_data.get("message", str(e)),
                )
            except (json.JSONDecodeError, AttributeError):
                return CASLookupError(
                    name_queried=name,
                    error_code="HTTP_ERROR",
                    error_message=str(e),
                )
        except requests.RequestException as e:
            return CASLookupError(
                name_queried=name,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        # Parse search results
        results = data.get("results", [])
        if not results:
            return []

        # Fetch details for each result
        cas_results = []
        for item in results:
            rn = item.get("rn")
            if rn:
                detail = self.get_by_rn(rn)
                if isinstance(detail, CASResult):
                    detail.name_queried = name
                    cas_results.append(detail)

        return cas_results

    def get_by_rn(self, rn: str) -> CASResult | CASLookupError:
        """Get compound details by CAS Registry Number.

        Args:
            rn: CAS Registry Number (e.g., "50-99-7")

        Returns:
            CASResult on success, CASLookupError on failure
        """
        url = f"{BASE_URL}/detail?cas_rn={rn}"

        try:
            data = self._get(url)
        except requests.HTTPError as e:
            try:
                error_data = e.response.json()
                return CASLookupError(
                    name_queried=rn,
                    error_code=str(e.response.status_code),
                    error_message=error_data.get("message", str(e)),
                )
            except (json.JSONDecodeError, AttributeError):
                return CASLookupError(
                    name_queried=rn,
                    error_code="HTTP_ERROR",
                    error_message=str(e),
                )
        except requests.RequestException as e:
            return CASLookupError(
                name_queried=rn,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        # Parse detail response
        # CAS API returns HTML-formatted formulas (e.g., "C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>")
        # Strip HTML tags to get plain formula (e.g., "C6H12O6")
        raw_formula = data.get("molecularFormula")
        formula = HTML_TAG_PATTERN.sub("", raw_formula) if raw_formula else None
        is_mixture = formula == "Unspecified" or formula is None

        # Extract molecular mass
        mass_str = data.get("molecularMass")
        mass = None
        if mass_str and mass_str != "Unspecified":
            with contextlib.suppress(ValueError, TypeError):
                mass = float(mass_str)

        return CASResult(
            rn=data.get("rn", rn),
            name=data.get("name", ""),
            name_queried=rn,
            molecular_formula=formula if formula != "Unspecified" else None,
            molecular_mass=mass,
            inchi=data.get("inchi"),
            inchikey=data.get("inchiKey"),
            smiles=data.get("smile"),
            synonyms=data.get("synonyms"),
            is_mixture=is_mixture,
        )


def get_cas_client() -> CASClient | None:
    """Get a CAS client if API key is available, otherwise return None.

    This is a convenience function for optional CAS lookups.
    """
    try:
        return CASClient()
    except ValueError:
        return None
