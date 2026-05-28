"""DSMZ MediaDive API client.

A typed wrapper around the MediaDive REST API for querying microbiology
cultivation media ingredients and solutions.

MediaDive is a database of cultivation media maintained by the Leibniz Institute
DSMZ - German Collection of Microorganisms and Cell Cultures.

References:
    - MediaDive: https://mediadive.dsmz.de/
    - API docs: https://mediadive.dsmz.de/doc/index.html
"""

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)

# MediaDive API base URL
BASE_URL = "https://mediadive.dsmz.de/rest"

# Rate limit delay (be conservative - no documented limits)
DEFAULT_RATE_LIMIT_DELAY = 0.25


@dataclass
class IngredientResult:
    """Result from a MediaDive ingredient lookup.

    Attributes:
        id: MediaDive ingredient ID
        name: Ingredient name
        cas_rn: CAS Registry Number (if available)
        chebi: ChEBI ID (if available)
        pubchem: PubChem CID (if available)
        kegg: KEGG Compound ID (if available)
        formula: Molecular formula (if available)
        mass: Molecular mass (if available)
        is_complex: True if this is a complex/undefined mixture
        synonyms: List of synonym names
        media_ids: List of media IDs that use this ingredient
    """

    id: int
    name: str
    cas_rn: str | None = None
    chebi: int | None = None
    pubchem: int | None = None
    kegg: str | None = None
    formula: str | None = None
    mass: float | None = None
    is_complex: bool = False
    synonyms: list[str] = field(default_factory=list)
    media_ids: list[str | int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "mediadive_id": self.id,
            "mediadive_name": self.name,
            "mediadive_cas_rn": self.cas_rn or "",
            "mediadive_chebi": str(self.chebi) if self.chebi else "",
            "mediadive_pubchem": str(self.pubchem) if self.pubchem else "",
            "mediadive_kegg": self.kegg or "",
            "mediadive_formula": self.formula or "",
            "mediadive_mass": str(self.mass) if self.mass else "",
            "mediadive_is_complex": "true" if self.is_complex else "false",
        }


@dataclass
class SolutionRecipeItem:
    """A single item in a solution recipe.

    Attributes:
        order: Recipe step order
        compound: Compound name
        compound_id: MediaDive compound ID (if ingredient)
        solution_id: MediaDive solution ID (if sub-solution)
        amount: Amount value
        unit: Unit of measurement
        g_l: Grams per liter (if applicable)
        mmol_l: Millimoles per liter (if applicable)
        condition: Special condition text
        attribute: Additional attribute text
        optional: Whether this ingredient is optional
    """

    order: int
    compound: str
    compound_id: int | None = None
    solution_id: int | None = None
    amount: float | None = None
    unit: str | None = None
    g_l: float | None = None
    mmol_l: float | None = None
    condition: str | None = None
    attribute: str | None = None
    optional: bool = False


@dataclass
class SolutionResult:
    """Result from a MediaDive solution lookup.

    Attributes:
        id: MediaDive solution ID
        name: Solution name
        volume: Total volume in ml
        recipe: List of recipe items
    """

    id: int
    name: str
    volume: float | None = None
    recipe: list[SolutionRecipeItem] = field(default_factory=list)


@dataclass
class MediaDiveLookupError:
    """Error from a failed MediaDive lookup.

    Attributes:
        query: The query we searched for
        error_code: Error code
        error_message: Human-readable error message
    """

    query: str
    error_code: str
    error_message: str


class MediaDiveClient:
    """Client for DSMZ MediaDive REST API.

    MediaDive provides information about microbiology cultivation media,
    including ingredients, solutions, and complete media recipes.

    No API key is required.

    Supports optional JSON file caching to avoid redundant API calls.

    Example:
        >>> client = MediaDiveClient()
        >>> result = client.get_ingredient(1)
        >>> if isinstance(result, IngredientResult):
        ...     print(f"Name: {result.name}, CAS: {result.cas_rn}")
        Name: Peptone, CAS: 73049-73-7

    Example with caching:
        >>> client = MediaDiveClient(cache_file=Path("mediadive_cache.json"))
        >>> result = client.get_ingredient(1)  # Fetches from API
        >>> result = client.get_ingredient(1)  # Returns cached result
    """

    def __init__(
        self,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        timeout: float = 30.0,
        cache_file: Path | None = None,
    ):
        """Initialize MediaDive client.

        Args:
            rate_limit_delay: Seconds to wait between requests (default: 0.25)
            timeout: Request timeout in seconds (default: 30)
            cache_file: Optional path to JSON cache file
        """
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self.cache_file = cache_file
        self._cache: dict[str, Any] = {}
        self._last_request_time: float = 0
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "cmm-ai-automation/0.1.0 (https://github.com/turbomam/cmm-ai-automation)",
            }
        )

        # Load cache from file if provided
        if cache_file and cache_file.exists():
            self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from JSON file."""
        if self.cache_file and self.cache_file.exists():
            try:
                with self.cache_file.open(encoding="utf-8") as f:
                    self._cache = json.load(f)
                logger.debug(f"Loaded {len(self._cache)} cached entries from {self.cache_file}")
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load cache from {self.cache_file}: {e}")
                self._cache = {}

    def save_cache(self) -> None:
        """Save cache to JSON file."""
        if self.cache_file:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with self.cache_file.open("w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2)
            logger.debug(f"Saved {len(self._cache)} entries to cache: {self.cache_file}")

    def _wait_for_rate_limit(self) -> None:
        """Wait if needed to respect rate limit."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _get(self, endpoint: str) -> dict[str, Any]:
        """Make a GET request with rate limiting.

        Args:
            endpoint: API endpoint (relative to BASE_URL)

        Returns:
            Parsed JSON response

        Raises:
            requests.RequestException: On network errors
        """
        url = f"{BASE_URL}/{endpoint}"
        self._wait_for_rate_limit()
        logger.debug(f"GET {url}")
        response = self._session.get(url, timeout=self.timeout)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def get_ingredient(self, ingredient_id: int) -> IngredientResult | MediaDiveLookupError:
        """Get an ingredient by its MediaDive ID.

        Results are cached if a cache_file was provided to the client.

        Args:
            ingredient_id: MediaDive ingredient ID

        Returns:
            IngredientResult on success, MediaDiveLookupError on failure
        """
        cache_key = f"ingredient:{ingredient_id}"

        # Check cache first
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if cached.get("_error"):
                return MediaDiveLookupError(
                    query=f"ingredient/{ingredient_id}",
                    error_code=cached.get("error_code", "CACHED_ERROR"),
                    error_message=cached.get("error_message", "Cached error"),
                )
            return self._parse_ingredient(cached)

        try:
            data = self._get(f"ingredient/{ingredient_id}")
        except requests.HTTPError as e:
            error = MediaDiveLookupError(
                query=f"ingredient/{ingredient_id}",
                error_code=str(e.response.status_code),
                error_message=str(e),
            )
            # Cache errors too (to avoid repeated failed lookups)
            self._cache[cache_key] = {
                "_error": True,
                "error_code": error.error_code,
                "error_message": error.error_message,
            }
            return error
        except requests.RequestException as e:
            return MediaDiveLookupError(
                query=f"ingredient/{ingredient_id}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        if data.get("status") == 404:
            error = MediaDiveLookupError(
                query=f"ingredient/{ingredient_id}",
                error_code="NOT_FOUND",
                error_message=data.get("msg", "Ingredient not found"),
            )
            self._cache[cache_key] = {
                "_error": True,
                "error_code": error.error_code,
                "error_message": error.error_message,
            }
            return error

        # Cache the successful result
        ingredient_data = data.get("data", {})
        self._cache[cache_key] = ingredient_data

        return self._parse_ingredient(ingredient_data)

    def get_solution(self, solution_id: int) -> SolutionResult | MediaDiveLookupError:
        """Get a solution by its MediaDive ID.

        Results are cached if a cache_file was provided to the client.

        Args:
            solution_id: MediaDive solution ID

        Returns:
            SolutionResult on success, MediaDiveLookupError on failure
        """
        cache_key = f"solution:{solution_id}"

        # Check cache first
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if cached.get("_error"):
                return MediaDiveLookupError(
                    query=f"solution/{solution_id}",
                    error_code=cached.get("error_code", "CACHED_ERROR"),
                    error_message=cached.get("error_message", "Cached error"),
                )
            return self._parse_solution(cached)

        try:
            data = self._get(f"solution/{solution_id}")
        except requests.HTTPError as e:
            error = MediaDiveLookupError(
                query=f"solution/{solution_id}",
                error_code=str(e.response.status_code),
                error_message=str(e),
            )
            self._cache[cache_key] = {
                "_error": True,
                "error_code": error.error_code,
                "error_message": error.error_message,
            }
            return error
        except requests.RequestException as e:
            return MediaDiveLookupError(
                query=f"solution/{solution_id}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        if data.get("status") == 404:
            error = MediaDiveLookupError(
                query=f"solution/{solution_id}",
                error_code="NOT_FOUND",
                error_message=data.get("msg", "Solution not found"),
            )
            self._cache[cache_key] = {
                "_error": True,
                "error_code": error.error_code,
                "error_message": error.error_message,
            }
            return error

        # Cache the successful result
        solution_data = data.get("data", {})
        self._cache[cache_key] = solution_data

        return self._parse_solution(solution_data)

    def search_ingredients_by_name(self, name: str) -> list[IngredientResult] | MediaDiveLookupError:
        """Search for ingredients by name.

        Note: MediaDive doesn't have a search endpoint, so this checks
        the KNOWN_INGREDIENTS mapping first, then returns an error if
        not found.

        Args:
            name: Ingredient name to search for

        Returns:
            List of matching IngredientResult, or MediaDiveLookupError on failure
        """
        # Check known ingredients first
        ingredient_id = get_known_ingredient_id(name)
        if ingredient_id is not None:
            result = self.get_ingredient(ingredient_id)
            if isinstance(result, IngredientResult):
                return [result]
            return result

        # MediaDive doesn't have a search API endpoint
        return MediaDiveLookupError(
            query=name,
            error_code="NO_SEARCH_API",
            error_message=(
                "MediaDive does not provide a search API. "
                "Use https://mediadive.dsmz.de/ingredients to find ingredient IDs, "
                "then use get_ingredient(id) to fetch details."
            ),
        )

    def _parse_ingredient(self, data: dict[str, Any]) -> IngredientResult:
        """Parse ingredient data from API response."""
        return IngredientResult(
            id=data.get("id", 0),
            name=data.get("name", ""),
            cas_rn=data.get("CAS-RN"),
            chebi=data.get("ChEBI"),
            pubchem=data.get("PubChem"),
            kegg=data.get("KEGG-Compound"),
            formula=data.get("formula"),
            mass=data.get("mass"),
            is_complex=bool(data.get("complex_compound")),
            synonyms=data.get("synonyms", []),
            media_ids=data.get("media", []),
        )

    def _parse_solution(self, data: dict[str, Any]) -> SolutionResult:
        """Parse solution data from API response."""
        recipe_items = []
        for item in data.get("recipe", []):
            recipe_items.append(
                SolutionRecipeItem(
                    order=item.get("recipe_order", 0),
                    compound=item.get("compound", ""),
                    compound_id=item.get("compound_id"),
                    solution_id=item.get("solution_id"),
                    amount=item.get("amount"),
                    unit=item.get("unit"),
                    g_l=item.get("g_l"),
                    mmol_l=item.get("mmol_l"),
                    condition=item.get("condition"),
                    attribute=item.get("attribute"),
                    optional=bool(item.get("optional")),
                )
            )

        return SolutionResult(
            id=data.get("id", 0),
            name=data.get("name", ""),
            volume=data.get("volume"),
            recipe=recipe_items,
        )


# Well-known MediaDive ingredient IDs for common media components
# These can be used for direct lookups without searching
KNOWN_INGREDIENTS = {
    "peptone": 1,
    "yeast extract": 16,
    "tryptone": 17,
    "casamino acids": 101,
    "proteose peptone": 208,
    "fe(iii)-edta": 952,
    "iron(iii) edta": 952,
    "ferric edta": 952,
}

# Well-known MediaDive solution IDs for trace element solutions
KNOWN_SOLUTIONS = {
    "trace element solution sl-6": 25,
    "trace element solution sl-10": 3527,
    "trace element solution sl-4": 26,
    "trace element solution sl-7": 2386,
    "trace element solution sl-8": 2250,
}


def get_known_ingredient_id(name: str) -> int | None:
    """Get the MediaDive ingredient ID for a known ingredient name.

    Args:
        name: Ingredient name (case-insensitive)

    Returns:
        MediaDive ingredient ID if known, None otherwise
    """
    return KNOWN_INGREDIENTS.get(name.lower())


def get_known_solution_id(name: str) -> int | None:
    """Get the MediaDive solution ID for a known solution name.

    Args:
        name: Solution name (case-insensitive)

    Returns:
        MediaDive solution ID if known, None otherwise
    """
    return KNOWN_SOLUTIONS.get(name.lower())
