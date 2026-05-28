"""
API Client Example

Demonstrates building a robust HTTP client with:
- Session management and connection pooling
- Error handling with retries
- Response parsing and validation
- Rate limiting
"""

import time
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Structured API response."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: int = 0


class APIClient:
    """
    Robust HTTP API client with built-in error handling and retries.
    
    Usage:
        client = APIClient("https://api.example.com", api_key="your-key")
        response = client.get("/users/123")
        if response.success:
            print(response.data)
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: tuple = (5, 30),
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = self._create_session(max_retries)
        
        if api_key:
            self.session.headers["X-API-Key"] = api_key
    
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create configured session with retry logic."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        session.headers.update({
            "User-Agent": "APIClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        return session
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> APIResponse:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        try:
            logger.info(f"{method} {url}")
            start_time = time.time()
            
            response = self.session.request(method, url, **kwargs)
            elapsed = time.time() - start_time
            
            logger.info(f"Response: {response.status_code} in {elapsed:.2f}s")
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "60")
                return APIResponse(
                    success=False,
                    error=f"Rate limited. Retry after {retry_after}s",
                    status_code=429
                )
            
            # Raise for 4xx/5xx errors
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json() if response.content else None
            return APIResponse(success=True, data=data, status_code=response.status_code)
            
        except requests.exceptions.Timeout:
            return APIResponse(success=False, error="Request timed out")
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Connection failed")
        except requests.exceptions.HTTPError as e:
            return APIResponse(
                success=False,
                error=str(e),
                status_code=e.response.status_code if e.response else 0
            )
        except ValueError:
            return APIResponse(success=False, error="Invalid JSON response")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> APIResponse:
        """Make GET request."""
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> APIResponse:
        """Make POST request."""
        return self._make_request("POST", endpoint, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> APIResponse:
        """Make PUT request."""
        return self._make_request("PUT", endpoint, json=data)
    
    def delete(self, endpoint: str) -> APIResponse:
        """Make DELETE request."""
        return self._make_request("DELETE", endpoint)


# Example usage
if __name__ == "__main__":
    # Create client
    client = APIClient("https://jsonplaceholder.typicode.com")
    
    # Make requests
    response = client.get("/posts/1")
    if response.success:
        print(f"Post title: {response.data['title']}")
    else:
        print(f"Error: {response.error}")

