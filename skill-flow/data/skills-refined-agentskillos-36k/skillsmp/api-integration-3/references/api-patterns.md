# API Integration Patterns

## HTTP Client Setup

### Using Requests

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session(base_url: str, timeout: tuple = (5, 30)) -> requests.Session:
    """Create a configured requests session with retry logic."""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set default headers
    session.headers.update({
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    
    return session
```

### Using httpx (Async)

```python
import httpx

async def create_async_client(base_url: str) -> httpx.AsyncClient:
    """Create a configured async HTTP client."""
    return httpx.AsyncClient(
        base_url=base_url,
        timeout=httpx.Timeout(10.0, connect=5.0),
        headers={"User-Agent": "MyApp/1.0"},
        follow_redirects=True
    )
```

## Authentication Patterns

### API Key Authentication

```python
# Header-based API key
session.headers["X-API-Key"] = "your-api-key"

# Query parameter API key
params = {"api_key": "your-api-key", **other_params}
response = session.get(url, params=params)
```

### OAuth 2.0 Bearer Token

```python
def get_oauth_token(client_id: str, client_secret: str, token_url: str) -> str:
    """Obtain OAuth 2.0 access token using client credentials."""
    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]

# Use the token
session.headers["Authorization"] = f"Bearer {token}"
```

### JWT Authentication

```python
import jwt
from datetime import datetime, timedelta

def create_jwt_token(secret: str, payload: dict, expires_in: int = 3600) -> str:
    """Create a JWT token with expiration."""
    payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_in)
    payload["iat"] = datetime.utcnow()
    return jwt.encode(payload, secret, algorithm="HS256")
```

## Error Handling and Retries

### Custom Exception Classes

```python
class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    pass

class AuthenticationError(APIError):
    """Raised when authentication fails."""
    pass
```

### Retry with Exponential Backoff

```python
import time
from functools import wraps

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException, APIError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
```

## Rate Limiting

### Token Bucket Implementation

```python
import time
from threading import Lock

class RateLimiter:
    """Simple token bucket rate limiter."""
    
    def __init__(self, requests_per_second: float):
        self.rate = requests_per_second
        self.tokens = requests_per_second
        self.last_update = time.monotonic()
        self.lock = Lock()
    
    def acquire(self):
        """Wait until a token is available."""
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.rate, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            if self.tokens < 1:
                sleep_time = (1 - self.tokens) / self.rate
                time.sleep(sleep_time)
                self.tokens = 0
            else:
                self.tokens -= 1
```

### Handling 429 Responses

```python
def handle_rate_limit(response: requests.Response) -> float:
    """Extract retry delay from rate limit response."""
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            return float(retry_after)
        return 60.0  # Default wait time
    return 0
```

