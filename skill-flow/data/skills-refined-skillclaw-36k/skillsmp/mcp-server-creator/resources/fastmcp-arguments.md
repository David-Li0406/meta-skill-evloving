# FastMCP Constructor Arguments

This document provides detailed information about all the arguments available in the FastMCP constructor.

## Constructor Signature

```python
from mcp.server.auth.provider import OAuthAuthorizationServerProvider
class FastMCP(Generic[LifespanResultT]):
    def __init__(  # noqa: PLR0913
        self,
        name: str | None = None,
        instructions: str | None = None,
        website_url: str | None = None,
        icons: list[Icon] | None = None,
        auth_server_provider: (OAuthAuthorizationServerProvider[Any, Any, Any] | None) = None,
        token_verifier: TokenVerifier | None = None,
        event_store: EventStore | None = None,
        retry_interval: int | None = None,
        *,
        tools: list[Tool] | None = None,
        debug: bool = False,
        log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
        host: str = "127.0.0.1",
        port: int = 8000,
        mount_path: str = "/",
        sse_path: str = "/sse",
        message_path: str = "/messages/",
        streamable_http_path: str = "/mcp",
        json_response: bool = False,
        stateless_http: bool = False,
        warn_on_duplicate_resources: bool = True,
        warn_on_duplicate_tools: bool = True,
        warn_on_duplicate_prompts: bool = True,
        dependencies: Collection[str] = (),
        lifespan: (Callable[[FastMCP[LifespanResultT]], AbstractAsyncContextManager[LifespanResultT]] | None) = None,
        auth: AuthSettings | None = None,
        transport_security: TransportSecuritySettings | None = None,
    ):
```

## Argument Details

### Basic Configuration
- **name** (`str | None`): Name of the MCP server instance (default: `None`)
- **instructions** (`str | None`): Instructions for the server, describing its capabilities (default: `None`)
- **website_url** (`str | None`): URL to the server's website (default: `None`)
- **icons** (`list[Icon] | None`): List of icons for the server (default: `None`)

### Authentication and Security
- **auth_server_provider** (`OAuthAuthorizationServerProvider | None`): OAuth provider for authentication (default: `None`)
- **token_verifier** (`TokenVerifier | None`): Token verifier for authentication (default: `None`)
- **auth** (`AuthSettings | None`): Authentication settings (default: `None`)
- **transport_security** (`TransportSecuritySettings | None`): Transport security settings (default: `None`)

### Tools and Resources
- **tools** (`list[Tool] | None`): Pre-defined tools for the server (default: `None`)
- **dependencies** (`Collection[str]`): Collection of dependencies (default: `()`)

### Event and Storage Configuration
- **event_store** (`EventStore | None`): Event store for storing events (default: `None`)
- **retry_interval** (`int | None`): Retry interval for operations (default: `None`)

### Debugging and Logging
- **debug** (`bool`): Enable debug mode (default: `False`)
- **log_level** (`Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]`): Logging level (default: `"INFO"`)

### Network Configuration
- **host** (`str`): Host address for the server (default: `"127.0.0.1"`)
- **port** (`int`): Port number for the server (default: `8000`)

### Path Configuration
- **mount_path** (`str`): Mount path for the server (default: `"/"`)
- **sse_path** (`str`): Path for Server-Sent Events (default: `"/sse"`)
- **message_path** (`str`): Path for messages (default: `"/messages/"`)
- **streamable_http_path** (`str`): Path for streamable HTTP (default: `"/mcp"`)

### Response and Behavior Configuration
- **json_response** (`bool`): Enable JSON response format (default: `False`)
- **stateless_http** (`bool`): Enable stateless HTTP mode (default: `False`)

### Warning Configuration
- **warn_on_duplicate_resources** (`bool`): Warn on duplicate resources (default: `True`)
- **warn_on_duplicate_tools** (`bool`): Warn on duplicate tools (default: `True`)
- **warn_on_duplicate_prompts** (`bool`): Warn on duplicate prompts (default: `True`)

### Lifespan Configuration
- **lifespan** (`Callable[[FastMCP[LifespanResultT]], AbstractAsyncContextManager[LifespanResultT]] | None`): Lifespan context manager (default: `None`)

## Usage Examples

### Basic Configuration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="my-mcp-server",
    instructions="A server for performing various operations",
    json_response=True
)
```

### Production Configuration
```python
mcp = FastMCP(
    name="production-server",
    instructions="Production MCP server with security",
    host="0.0.0.0",
    port=8000,
    debug=False,
    log_level="INFO",
    json_response=True
)
```

### With Authentication
```python
mcp = FastMCP(
    name="secure-server",
    auth_server_provider=oauth_provider,
    token_verifier=token_verifier,
    auth=auth_settings
)
```
