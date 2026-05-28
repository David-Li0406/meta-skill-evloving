"""
Credential Broker and Base HTTP Client for Research Tools

Handles credential loading from multiple sources and provides
a base HTTP client with retry logic.
"""

import os
import time
import httpx
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass
from functools import lru_cache


# ============================================================================
# Credential Management
# ============================================================================

@dataclass
class Credential:
    """Represents a credential with metadata."""
    key: str
    value: str
    source: str  # 'env', '1password', 'aws_secrets'
    expires_at: Optional[str] = None


class CredentialBroker:
    """
    Central credential management for all research tools.
    
    Priority order:
    1. Environment variables
    2. .env file
    3. Future: 1Password, AWS Secrets Manager
    
    Usage:
        broker = CredentialBroker()
        api_key = broker.get("firecrawl", "api_key")
    """
    
    def __init__(self, env_file: Optional[str] = None):
        self._cache: dict[str, Credential] = {}
        self._load_env_file(env_file)
    
    def _load_env_file(self, env_file: Optional[str] = None):
        """Load .env file if it exists."""
        if env_file:
            env_path = Path(env_file)
        else:
            # Look for .env in current dir and parent dirs
            for path in [Path(".env"), Path("../.env"), Path("../../.env")]:
                if path.exists():
                    env_path = path
                    break
            else:
                return
        
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
    
    def get(self, service: str, key: str) -> str:
        """
        Get a credential for a service.
        
        Args:
            service: Service name (e.g., 'firecrawl', 'apollo')
            key: Credential key (e.g., 'api_key')
        
        Returns:
            Credential value
        
        Raises:
            ValueError: If credential not found
        """
        cache_key = f"{service}:{key}"
        
        # Check cache first
        if cache_key in self._cache:
            return self._cache[cache_key].value
        
        # Try environment variable
        env_key = f"{service.upper()}_{key.upper()}"
        value = os.environ.get(env_key)
        
        if not value:
            # Try alternate formats
            alt_keys = [
                f"{service.upper()}_API_KEY",
                f"{service.upper()}_KEY",
                f"{service.upper()}_TOKEN",
            ]
            for alt in alt_keys:
                value = os.environ.get(alt)
                if value:
                    break
        
        if not value:
            raise ValueError(
                f"Missing credential: {env_key}\n"
                f"Add to .env file or environment:\n"
                f"  {env_key}=your_key_here"
            )
        
        # Cache and return
        self._cache[cache_key] = Credential(
            key=env_key,
            value=value,
            source="env"
        )
        
        return value
    
    def has(self, service: str, key: str = "api_key") -> bool:
        """Check if a credential exists without raising."""
        try:
            self.get(service, key)
            return True
        except ValueError:
            return False


# Global broker instance
_broker: Optional[CredentialBroker] = None

def get_broker() -> CredentialBroker:
    """Get or create the global credential broker."""
    global _broker
    if _broker is None:
        _broker = CredentialBroker()
    return _broker


def get_credential(service: str, key: str = "api_key") -> str:
    """Convenience function to get a credential."""
    return get_broker().get(service, key)


def has_credential(service: str, key: str = "api_key") -> bool:
    """Convenience function to check if credential exists."""
    return get_broker().has(service, key)


def has_robynn_connection() -> bool:
    """Check if the agent is connected to the Robynn platform."""
    return os.environ.get("ROBYNN_API_KEY") is not None


def get_robynn_context() -> Optional[dict[str, Any]]:
    """Fetch brand context from Robynn platform if connected."""
    if not has_robynn_connection():
        return None
    
    # Lazy import to avoid circular dependencies
    from tools.robynn import RobynnClient
    client = RobynnClient()
    return client.fetch_context()


# ============================================================================
# Base HTTP Client
# ============================================================================

class BaseAPIClient:
    """
    Base HTTP client with retry logic and error handling.
    
    Subclass this for each API integration.
    """
    
    BASE_URL: str = ""
    DEFAULT_TIMEOUT: float = 30.0
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    def __init__(self):
        self.broker = get_broker()
        self._client: Optional[httpx.Client] = None
    
    @property
    def client(self) -> httpx.Client:
        """Lazy-initialize HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.BASE_URL,
                timeout=self.DEFAULT_TIMEOUT,
                headers=self._get_headers()
            )
        return self._client
    
    def _get_headers(self) -> dict[str, str]:
        """Override in subclass to add auth headers."""
        return {
            "Content-Type": "application/json",
            "User-Agent": "CMO-Agent/1.0"
        }
    
    def _request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> dict[str, Any]:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: URL path
            **kwargs: Additional arguments to pass to httpx
        
        Returns:
            JSON response data
        
        Raises:
            httpx.HTTPError: On request failure after retries
        """
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.request(method, path, **kwargs)
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limited
                    retry_after = int(e.response.headers.get("Retry-After", self.RETRY_DELAY * (attempt + 1)))
                    time.sleep(retry_after)
                    last_error = e
                elif e.response.status_code >= 500:  # Server error
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                    last_error = e
                else:
                    raise
            
            except httpx.RequestError as e:
                time.sleep(self.RETRY_DELAY * (attempt + 1))
                last_error = e
        
        if last_error:
            raise last_error
        
        raise RuntimeError("Request failed with no error captured")
    
    def get(self, path: str, **kwargs) -> dict[str, Any]:
        """Make GET request."""
        return self._request("GET", path, **kwargs)
    
    def post(self, path: str, **kwargs) -> dict[str, Any]:
        """Make POST request."""
        return self._request("POST", path, **kwargs)
    
    def close(self):
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# ============================================================================
# Utility Functions
# ============================================================================

def clean_url(url: str) -> str:
    """Ensure URL has protocol."""
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    return url.rstrip("/")


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    from urllib.parse import urlparse
    url = clean_url(url)
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain
