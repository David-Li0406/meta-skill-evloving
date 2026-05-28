# MCP Server Security Best Practices

This document outlines security best practices for production MCP servers.

## Authentication and Authorization

### API Key Authentication
For simple authentication, use API key validation:

```python
import os
import secrets

def validate_api_key(auth_header: str) -> bool:
    """Validate API key from Authorization header."""
    if not auth_header:
        return False

    # Expected format: "Bearer YOUR_API_KEY"
    parts = auth_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return False

    expected_key = os.getenv("MCP_SERVER_TOKEN")
    return secrets.compare_digest(parts[1], expected_key)

# Example tool with authentication
@mcp.tool()
def authenticated_tool(data: str, auth_header: str = None) -> str:
    """Tool that requires authentication."""
    if not validate_api_key(auth_header):
        raise PermissionError("Invalid or missing API key")

    return process_data(data)
```

### OAuth Integration
For enterprise scenarios, integrate with OAuth providers:

```python
# This would be implemented using the mcp-use OAuth features
# Example structure (syntax may vary based on actual implementation):
from mcp_use.server import oauthAuth0Provider

server = MCPServer(
    name="secure-server",
    oauth=oauthAuth0Provider({
        "domain": os.getenv("AUTH0_DOMAIN"),
        "audience": os.getenv("AUTH0_AUDIENCE"),
    })
)

@mcp.tool()
async def secure_tool(data: str, ctx: Context) -> str:
    """Tool that accesses authenticated user context."""
    user = ctx.auth  # Contains authenticated user info
    if "admin" not in user.roles:
        raise PermissionError("Admin role required")

    return process_admin_data(user.user_id, data)
```

## Input Validation and Sanitization

### Parameter Validation
Always validate input parameters:

```python
from typing import Literal

@mcp.tool()
def validated_tool(
    operation: Literal["read", "write", "delete"],
    path: str,
    max_depth: int = 3
) -> dict:
    """Tool with strict input validation."""

    # Validate operation
    if operation not in ["read", "write", "delete"]:
        raise ValueError(f"Invalid operation: {operation}")

    # Validate path
    if not path or ".." in path or path.startswith("/"):
        raise ValueError("Invalid path")

    # Validate depth
    if not 1 <= max_depth <= 10:
        raise ValueError("Depth must be between 1 and 10")

    # Sanitize path
    sanitized_path = sanitize_path(path)

    return perform_operation(operation, sanitized_path, max_depth)
```

### Content Filtering
Filter content to prevent injection attacks:

```python
import re

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal."""
    # Remove any directory traversal sequences
    filename = re.sub(r'\.\./', '', filename)
    filename = re.sub(r'\.\.\\', '', filename)

    # Only allow alphanumeric, dots, hyphens, and underscores
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    return filename

def sanitize_sql_query(query: str) -> str:
    """Basic SQL sanitization (use proper parameterized queries instead)."""
    # Remove potentially dangerous SQL keywords
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE"]
    upper_query = query.upper()

    for keyword in dangerous_keywords:
        if keyword in upper_query:
            raise ValueError(f"Dangerous SQL keyword '{keyword}' detected")

    return query
```

## Rate Limiting and Resource Management

### Request Rate Limiting
Implement rate limiting to prevent abuse:

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60, burst_limit: int = 10):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> tuple[bool, str]:
        """Check if client is allowed to make a request."""
        now = time.time()

        # Remove requests older than 1 minute
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < 60
        ]

        # Check burst limit
        if len(self.requests[client_id]) >= self.burst_limit:
            return False, f"Burst limit exceeded ({self.burst_limit}/minute)"

        # Check sustained rate
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False, f"Rate limit exceeded ({self.requests_per_minute}/minute)"

        # Record this request
        self.requests[client_id].append(now)
        return True, ""

rate_limiter = RateLimiter()

@mcp.tool()
def rate_limited_tool(client_id: str, data: str) -> str:
    """Tool with rate limiting."""
    allowed, message = rate_limiter.is_allowed(client_id)
    if not allowed:
        raise PermissionError(message)

    return process_data(data)
```

### Resource Limits
Enforce resource limits to prevent exhaustion:

```python
import os
import psutil
from contextlib import contextmanager

def check_system_resources(min_memory_mb: int = 100) -> bool:
    """Check if system has sufficient resources."""
    memory_available_mb = psutil.virtual_memory().available / 1024 / 1024
    return memory_available_mb > min_memory_mb

@contextmanager
def resource_limiter(max_memory_mb: int = 100):
    """Context manager to enforce memory limits."""
    initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

    try:
        yield
    finally:
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        if final_memory - initial_memory > max_memory_mb:
            raise MemoryError(f"Memory usage exceeded limit of {max_memory_mb}MB")

@mcp.tool()
def resource_conscious_tool(large_data: str) -> str:
    """Tool that respects resource limits."""
    if not check_system_resources():
        raise RuntimeError("Insufficient system resources")

    with resource_limiter(max_memory_mb=50):
        result = process_large_data(large_data)

    return result
```

## Secure File Operations

### Restricted File Access
When accessing files, implement strict access controls:

```python
import os
from pathlib import Path

class SecureFileSystem:
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory).resolve()

    def validate_path(self, requested_path: str) -> Path:
        """Validate that requested path is within allowed directory."""
        requested_abs = (self.base_directory / requested_path).resolve()

        # Ensure the resolved path is within the base directory
        if not str(requested_abs).startswith(str(self.base_directory)):
            raise PermissionError("Path traversal detected")

        return requested_abs

    def read_file(self, relative_path: str) -> str:
        """Securely read a file."""
        file_path = self.validate_path(relative_path)

        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Additional checks: file size, extension, etc.
        if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("File too large")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

# Usage
secure_fs = SecureFileSystem("/safe/data/directory")

@mcp.tool()
def read_safe_file(filename: str) -> str:
    """Securely read a file."""
    return secure_fs.read_file(filename)
```

## Network Security

### Allowed Domains
Restrict network access to trusted domains:

```python
import re
from urllib.parse import urlparse

class NetworkValidator:
    def __init__(self, allowed_domains: list[str]):
        self.allowed_domains = set(domain.lower().strip() for domain in allowed_domains)

    def is_url_allowed(self, url: str) -> bool:
        """Check if URL is in allowed domains."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Handle domains with ports (e.g., "api.example.com:8080")
            if ':' in domain:
                domain = domain.split(':')[0]

            return domain in self.allowed_domains
        except Exception:
            return False

validator = NetworkValidator([
    "api.trusted-service.com",
    "internal.company.com"
])

@mcp.tool()
async def secure_fetch_data(url: str) -> str:
    """Securely fetch data from allowed domains only."""
    if not validator.is_url_allowed(url):
        raise ValueError(f"URL not in allowed domains: {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

## Error Handling and Logging

### Secure Error Messages
Don't expose sensitive information in error messages:

```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def secure_tool_with_logging(sensitive_data: str) -> str:
    """Tool with secure error handling."""
    try:
        # Log the operation without sensitive data
        logger.info("Processing secure operation")

        # Process the sensitive data
        result = process_sensitive_data(sensitive_data)

        # Log success without sensitive data
        logger.info("Secure operation completed successfully")
        return result

    except ValueError as e:
        # Log the full error for debugging
        logger.error(f"Validation error in secure_tool: {e}", exc_info=True)
        # Return generic error to client
        raise ValueError("Invalid input provided")

    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Unexpected error in secure_tool: {e}", exc_info=True)
        # Return generic error to client
        raise RuntimeError("An error occurred processing your request")
```

## Configuration Security

### Environment Variable Handling
Properly handle sensitive configuration:

```python
import os
from typing import Optional

class SecureConfig:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.api_key = os.getenv("API_KEY")
        self.jwt_secret = os.getenv("JWT_SECRET")

        # Validate required secrets are present
        if not all([self.db_url, self.api_key, self.jwt_secret]):
            raise ValueError("Missing required environment variables")

    def get_db_connection_string(self) -> str:
        """Get database connection string safely."""
        # Never log or return the full connection string with password
        return self._mask_sensitive_parts(self.db_url)

    def _mask_sensitive_parts(self, value: str) -> str:
        """Mask sensitive parts of a string."""
        import re
        # Mask password in connection strings: postgresql://user:pass@host/db -> postgresql://user:***@host/db
        return re.sub(r':([^@]*)@', r':***@', value)

config = SecureConfig()
```

These security practices ensure that your MCP server is protected against common vulnerabilities while maintaining functionality.
