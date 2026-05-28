# MCP Server Architecture

This document outlines the architecture patterns for production-ready MCP servers.

## Core Components

### Server Instance
The main server instance manages the lifecycle and configuration of your MCP server using the official SDK:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="my-server",
    json_response=True
)
```

### Transport Protocols

MCP servers support multiple transport protocols:

- **stdio**: Standard input/output, typically used for local development and Claude integration
- **streamable-http**: HTTP-based transport, recommended for production deployments
- **sse**: Server-sent events (deprecated, use streamable-http instead)

For production deployments, use streamable-http with appropriate host and port configuration:

```python
mcp.run(
    transport="streamable-http"
)
```

## Tool Architecture

MCP tools are the primary interface for external systems to interact with your server:

### Synchronous Tools
```python
@mcp.tool()
def my_sync_tool(param1: str, param2: int) -> dict:
    """Description of what this tool does."""
    # Perform synchronous operations
    result = process_data(param1, param2)
    return {"result": result}
```

### Asynchronous Tools
```python
@mcp.tool()
async def my_async_tool(param1: str) -> str:
    """Async tool for operations that benefit from async/await."""
    # Perform async operations
    result = await async_process_data(param1)
    return result
```

### Tools with Context
Tools can accept a Context parameter to access advanced MCP features:

```python
from mcp_use.server import Context

@mcp.tool()
async def tool_with_context(query: str, ctx: Context) -> str:
    """Tool that uses MCP context for advanced features."""
    # Log progress to client
    await ctx.log('info', f'Starting to process query: {query}')

    # Perform operation
    result = await process_with_llm_assistance(query, ctx)

    # Return result
    return result
```

## Request Handling

### Input Validation
All tools should validate their inputs to prevent security vulnerabilities:

```python
@mcp.tool()
def secure_tool(user_input: str) -> str:
    """Tool with input validation."""
    # Validate input length
    if len(user_input) > 1000:
        raise ValueError("Input too long")

    # Validate content
    if contains_dangerous_patterns(user_input):
        raise ValueError("Invalid input pattern detected")

    # Process safe input
    return process_safe_input(user_input)
```

### Error Handling
Proper error handling ensures the server remains stable:

```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def robust_tool(data: str) -> str:
    """Tool with comprehensive error handling."""
    try:
        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")

        # Process data
        result = process_data(data)
        return result

    except ValueError as e:
        # Log validation errors
        logger.warning(f"Validation error: {e}")
        raise  # Re-raise to send to client

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in robust_tool: {e}", exc_info=True)
        raise RuntimeError("An error occurred processing your request")
```

## Security Considerations

### Authentication
Implement authentication at the transport layer or within individual tools:

```python
import os
from functools import wraps

def require_auth(func):
    """Decorator to require authentication."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = get_auth_header()  # Implementation depends on transport
        expected_token = os.getenv("MCP_SERVER_TOKEN")

        if not auth_header or auth_header != f"Bearer {expected_token}":
            raise PermissionError("Invalid or missing authentication")

        return func(*args, **kwargs)
    return wrapper

@mcp.tool()
@require_auth
def protected_tool(data: str) -> str:
    """Tool that requires authentication."""
    return process_data(data)
```

### Rate Limiting
Implement rate limiting to prevent abuse:

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute=60, burst_limit=10):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> tuple[bool, str]:
        now = time.time()
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < 60
        ]

        # Check burst limit
        if len(self.requests[client_id]) >= self.burst_limit:
            return False, "Rate limit exceeded (burst)"

        # Check sustained rate
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False, "Rate limit exceeded (sustained)"

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

## Monitoring and Observability

### Health Checks
Provide a health check endpoint to monitor server status:

```python
from starlette.responses import JSONResponse
from starlette.requests import Request

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    """Health check endpoint for the server."""
    # Add checks for critical dependencies
    checks = {}

    # Example: Check database connection
    # try:
    #     await db.ping()
    #     checks["database"] = "healthy"
    # except Exception as e:
    #     checks["database"] = f"unhealthy: {str(e)}"

    status = "healthy" if all(check == "healthy" for check in checks.values()) else "degraded"

    return JSONResponse({
        "status": status,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "service": "my-server",
        "version": "1.0.0",
        "checks": checks
    })
```

### Metrics
Collect metrics for monitoring server performance:

```python
from collections import Counter
import time

class MetricsCollector:
    def __init__(self):
        self.request_counts = Counter()
        self.request_durations = []

    def record_request(self, tool_name: str, status: str, duration: float):
        """Record metrics for a completed request."""
        self.request_counts[(tool_name, status)] += 1
        self.request_durations.append(duration)

    def get_metrics(self):
        """Get current metrics snapshot."""
        avg_duration = sum(self.request_durations) / len(self.request_durations) if self.request_durations else 0
        return {
            "request_counts": dict(self.request_counts),
            "avg_duration_seconds": avg_duration,
            "total_requests": sum(self.request_counts.values())
        }

metrics = MetricsCollector()

@mcp.tool()
def instrumented_tool(data: str) -> str:
    """Tool with metrics collection."""
    start_time = time.time()
    try:
        result = process_data(data)
        duration = time.time() - start_time
        metrics.record_request("instrumented_tool", "success", duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        metrics.record_request("instrumented_tool", "error", duration)
        raise
```

## Lifecycle Management

### Graceful Shutdown
Handle shutdown signals to clean up resources:

```python
import signal
import asyncio

class ServerManager:
    def __init__(self, mcp_instance):
        self.mcp = mcp_instance
        self.shutdown_event = asyncio.Event()
        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signal."""
        print(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_event.set()

    async def run_with_graceful_shutdown(self, **config):
        """Run server with graceful shutdown handling."""
        # Start server in background
        server_task = asyncio.create_task(self.mcp.run(**config))

        # Wait for shutdown signal
        await self.shutdown_event.wait()

        print("Shutting down server...")
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

        print("Server shut down gracefully")
```

This architecture provides a solid foundation for building production-ready MCP servers that are secure, observable, and maintainable.
