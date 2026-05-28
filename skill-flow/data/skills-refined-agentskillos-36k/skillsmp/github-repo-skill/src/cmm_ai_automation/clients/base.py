"""Base HTTP client with rate limiting and common configuration.

Provides shared functionality for all API clients:
- Rate limiting with configurable delay
- Session management with custom User-Agent
- Common GET/POST methods with timeout handling
- Generic Result/Error dataclass pattern

All clients should inherit from HTTPClientBase to reduce boilerplate.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

import requests

logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_RATE_LIMIT_DELAY = 0.2  # seconds between requests
DEFAULT_TIMEOUT = 30.0  # request timeout in seconds
DEFAULT_USER_AGENT = "cmm-ai-automation/0.1.0 (https://github.com/turbomam/cmm-ai-automation)"


@dataclass
class ClientError:
    """Error from a failed API request.

    Attributes:
        query: The query that was attempted
        error_code: Error code (e.g., \"HTTP_ERROR\", \"NOT_FOUND\", \"PARSE_ERROR\")
        error_message: Human-readable error message
        status_code: HTTP status code if available
    """

    query: str
    error_code: str
    error_message: str
    status_code: int | None = None


T = TypeVar("T")


@dataclass
class ClientResult(Generic[T]):
    """Successful result wrapper.

    Attributes:
        data: The result data
        query: The query that produced this result
    """

    data: T
    query: str


class HTTPClientBase:
    """Base class for HTTP API clients with rate limiting.

    Provides:
    - Session management with custom User-Agent
    - Rate limiting between requests
    - GET/POST methods with timeout handling
    - JSON response parsing

    Subclasses should:
    - Set BASE_URL class attribute
    - Override rate_limit_delay if needed
    - Add domain-specific methods

    Example:
        >>> class MyClient(HTTPClientBase):
        ...     BASE_URL = "https://api.example.com"
        ...
        ...     def get_item(self, item_id: str) -> dict | ClientError:
        ...         url = f"{self.BASE_URL}/items/{item_id}"
        ...         try:
        ...             return self._get_json(url)
        ...         except requests.HTTPError as e:
        ...             return ClientError(
        ...                 query=item_id,
        ...                 error_code="HTTP_ERROR",
        ...                 error_message=str(e),
        ...             )
    """

    BASE_URL: str = ""

    def __init__(
        self,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
    ):
        """Initialize the client.

        Args:
            rate_limit_delay: Seconds to wait between requests
            timeout: Request timeout in seconds
            user_agent: Custom User-Agent string (uses default if not provided)
        """
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self._last_request_time: float = 0
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": user_agent or DEFAULT_USER_AGENT,
            }
        )

    def _wait_for_rate_limit(self) -> None:
        """Wait if needed to respect rate limit."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _get(self, url: str, params: dict[str, Any] | None = None) -> requests.Response:
        """Make a GET request with rate limiting.

        Args:
            url: Full URL to fetch
            params: Query parameters

        Returns:
            Response object

        Raises:
            requests.RequestException: On network errors
        """
        self._wait_for_rate_limit()
        logger.debug(f"GET {url} params={params}")
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response

    def _get_json(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request and return parsed JSON.

        Args:
            url: Full URL to fetch
            params: Query parameters

        Returns:
            Parsed JSON response as dict

        Raises:
            requests.RequestException: On network errors
            json.JSONDecodeError: If response is not valid JSON
        """
        response = self._get(url, params)
        result: dict[str, Any] = response.json()
        return result

    def _post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Make a POST request with rate limiting.

        Args:
            url: Full URL to post to
            data: Form data
            json_data: JSON body data

        Returns:
            Response object

        Raises:
            requests.RequestException: On network errors
        """
        self._wait_for_rate_limit()
        logger.debug(f"POST {url}")
        response = self._session.post(url, data=data, json=json_data, timeout=self.timeout)
        response.raise_for_status()
        return response

    def _post_json(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request and return parsed JSON.

        Args:
            url: Full URL to post to
            data: Form data
            json_data: JSON body data

        Returns:
            Parsed JSON response as dict

        Raises:
            requests.RequestException: On network errors
            json.JSONDecodeError: If response is not valid JSON
        """
        response = self._post(url, data=data, json_data=json_data)
        result: dict[str, Any] = response.json()
        return result

    def close(self) -> None:
        """Close the underlying session."""
        self._session.close()

    def __enter__(self) -> "HTTPClientBase":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - close session."""
        self.close()
