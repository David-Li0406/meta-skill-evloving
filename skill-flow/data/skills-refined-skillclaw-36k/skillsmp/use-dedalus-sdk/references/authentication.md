# Authentication Reference

Secure credential handling with DAuth, Bearer Auth, and OAuth.

## DAuth (Dedalus Auth)

DAuth is Dedalus's managed OAuth 2.1 system with zero-trust credential isolation. Credentials never leave a sealed execution boundary.

### Key Properties

- OAuth 2.1 with PKCE
- Server-side token storage
- Automatic refresh handling
- Credential isolation (MCP servers never see raw secrets)

### Architecture

```
Client → MCP Server → DAuth → External API
         (opaque handles)  (decrypted secrets)
```

## Bearer Auth

For API keys, service accounts, and static tokens.

### MCPClient with Bearer Auth

```python
from dedalus_mcp.client import MCPClient, BearerAuth

client = await MCPClient.connect(
    "http://localhost:8000/mcp",
    auth=BearerAuth(access_token="your-token")
)
```

### With DedalusRunner (DAuth)

Define a Connection schema and bind at runtime:

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

# Define what secrets are needed
x_secrets = {
    "type": "bearer",
    "api_key": "your-x-api-key",
}

async def main():
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    response = await runner.run(
        input="Find trending topics",
        model="anthropic/claude-sonnet-4-20250514",
        mcp_servers=["windsor/x-api-mcp"],
        credentials=[x_secrets],
    )
```

## OAuth Flow

For user authentication with external providers.

### Flow Steps

1. **Request Without Token** - SDK calls MCP server
2. **401 Response** - Server returns `WWW-Authenticate` header
3. **Discovery** - SDK fetches `/.well-known/oauth-protected-resource`
4. **AuthenticationError** - SDK raises error with `connect_url`
5. **Browser Interaction** - User logs in and grants scopes
6. **Token Exchange** - Authorization code exchanged via PKCE
7. **Retry** - Request succeeds with valid credentials
8. **Auto-Refresh** - DAuth handles token refresh

### Handling OAuth Errors

```python
from dedalus_labs import AuthenticationError

try:
    result = await runner.run(
        input="Get my calendar events",
        model="openai/gpt-4o-mini",
        mcp_servers=["google/calendar-mcp"],
    )
except AuthenticationError as e:
    # Open browser for user to authenticate
    print(f"Please authenticate: {e.connect_url}")
    webbrowser.open(e.connect_url)
    
    # Wait for user to complete auth, then retry
    input("Press Enter after authenticating...")
    result = await runner.run(...)
```

## Using Your Own API Keys

While `DEDALUS_API_KEY` handles routing automatically, you can bring your own keys:

```bash
# Set provider-specific keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=AIza...
```

The SDK will use your keys when you specify models from that provider.

## Security Best Practices

1. **Never hardcode secrets** - Use environment variables or DAuth
2. **Use DEDALUS_API_KEY** - Simplest, most secure option
3. **Rotate credentials** - DAuth handles this automatically
4. **Least privilege** - Request only needed OAuth scopes
5. **Validate callbacks** - Always verify OAuth state parameters
