# HTTPX Client Patterns

Central HTTP client for external API calls with logging and standardization.

## Core Client (core/httpx.py)

```python
from typing import Any, Optional
import httpx
from httpx import AsyncClient, Response
from core.logging import get_logger
from middleware.conversation import get_conversation_id

logger = get_logger(__name__)

class HTTPClient:
    """Central HTTP client with standardized configuration."""
    
    def __init__(
        self,
        base_url: str = "",
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Optional[dict[str, str]] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = headers or {}
        self._client: Optional[AsyncClient] = None
    
    async def get_client(self) -> AsyncClient:
        """Get or create client."""
        if self._client is None:
            self._client = AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self.default_headers,
            )
        return self._client
    
    async def close(self) -> None:
        """Close client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def _add_conversation_header(self, headers: Optional[dict[str, str]]) -> dict[str, str]:
        """Add conversation ID to headers."""
        headers = headers or {}
        conversation_id = get_conversation_id()
        if conversation_id:
            headers["X-Conversation-ID"] = conversation_id
        return headers
    
    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Make HTTP request with logging."""
        client = await self.get_client()
        
        # Add conversation ID
        if "headers" in kwargs:
            kwargs["headers"] = self._add_conversation_header(kwargs["headers"])
        else:
            kwargs["headers"] = self._add_conversation_header(None)
        
        logger.info("External API request", method=method, url=url, base_url=self.base_url)
        
        try:
            response = await client.request(method, url, **kwargs)
            
            logger.info(
                "External API response",
                method=method,
                url=url,
                status_code=response.status_code,
            )
            
            response.raise_for_status()
            return response
            
        except httpx.HTTPStatusError as e:
            logger.error(
                "External API error",
                method=method,
                url=url,
                status_code=e.response.status_code,
                error=str(e),
            )
            raise
        except Exception as e:
            logger.error("External API request failed", method=method, url=url, error=str(e))
            raise
    
    async def get(self, url: str, **kwargs: Any) -> Response:
        return await self.request("GET", url, **kwargs)
    
    async def post(self, url: str, **kwargs: Any) -> Response:
        return await self.request("POST", url, **kwargs)
    
    async def put(self, url: str, **kwargs: Any) -> Response:
        return await self.request("PUT", url, **kwargs)
    
    async def delete(self, url: str, **kwargs: Any) -> Response:
        return await self.request("DELETE", url, **kwargs)
```

## Usage

### Load Config from YAML

```python
from core.config import load_yaml_config, ExternalAPIConfig

# Load from config/development.yml or config/production.yml
api_config_dict = load_yaml_config("external_api")
api_config = ExternalAPIConfig(**api_config_dict)

# Create client
external_client = HTTPClient(
    base_url=api_config.base_url,
    timeout=api_config.timeout,
    headers={"Authorization": f"Bearer {api_config.api_key}"}
)
```

### Make Requests

```python
# GET request
response = await external_client.get("/users/123")
user_data = response.json()

# POST request
response = await external_client.post(
    "/users",
    json={"name": "John", "email": "john@example.com"}
)

# With query parameters
response = await external_client.get("/users", params={"limit": 10, "offset": 0})

# With custom headers
response = await external_client.get("/users", headers={"X-Custom": "value"})
```

### Cleanup

```python
# In app shutdown
await external_client.close()
```

## Automatic Features

1. **Conversation ID propagation**: Added to all requests
2. **Request/Response logging**: All calls logged with structlog
3. **Error handling**: Standardized error logging
4. **Timeouts**: Configurable per client
5. **Base URL**: Consistent endpoint prefix

## Multiple Clients

```python
# Payment gateway
payment_client = HTTPClient(
    base_url="https://api.payment.com",
    headers={"Authorization": f"Bearer {payment_key}"}
)

# Analytics API
analytics_client = HTTPClient(
    base_url="https://analytics.example.com",
    headers={"X-API-Key": analytics_key}
)
```

## Next Steps

- [Configuration Patterns](configuration-patterns.md) - YAML config for APIs
- [Logging Patterns](logging-patterns.md) - Request/response logs
- [Observability Patterns](observability-patterns.md) - Tracing external calls
