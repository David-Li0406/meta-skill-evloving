---
name: mcp-integration
description: |
  Configure and manage MCP (Model Context Protocol) servers for AI agent tooling.
  Use when adding MCP servers, configuring authentication (OAuth 2.1 or API keys),
  managing opencode.json, implementing token flows, or troubleshooting MCP connections.
  Covers registry patterns, PKCE authentication, and the Result-based service architecture.
version: 1.0.0
tags:
  - mcp
  - oauth
  - authentication
  - api-key
  - opencode
  - external-integrations
---

# MCP Integration Skill

## Overview

MCP (Model Context Protocol) servers provide external tool integrations for AI agents. ContextHarness implements a comprehensive MCP management system with:

1. **Server Registry**: Curated list of known MCP servers with metadata
2. **Configuration Management**: Add/remove servers via opencode.json
3. **Authentication**: API key and OAuth 2.1 with PKCE support
4. **Token Management**: Secure storage with automatic refresh

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI INTERFACE                            │
│  context-harness mcp add | list | auth                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                     SERVICES                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ MCPService   │    │ OAuthService │    │ ConfigService│   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    PRIMITIVES                                │
│  MCPServer │ MCPServerConfig │ MCPAuthType │ OAuthTokens    │
└─────────────────────────────────────────────────────────────┘
```

## Adding a New MCP Server

### Step 1: Register in MCP_REGISTRY

Add the server to `src/context_harness/services/mcp_service.py`:

```python
MCP_REGISTRY: List[Dict[str, Any]] = [
    # Existing servers...
    {
        "name": "new-server",
        "url": "https://mcp.example.com/mcp",
        "description": "Description of the server capabilities",
        "server_type": "remote",  # or "local" for stdio
        "auth_type": "api-key",   # or "oauth" or None
    },
]
```

### Step 2: Handle Authentication (if required)

For API key authentication, the service auto-handles headers:

```python
# In MCPService.add()
if api_key and server_info.auth_type == MCPAuthType.API_KEY:
    if server_name == "context7":
        headers = {"CONTEXT7_API_KEY": api_key}
    else:
        headers = {"Authorization": f"Bearer {api_key}"}
```

For OAuth, add provider config to `oauth_service.py`:

```python
OAUTH_PROVIDERS: Dict[str, OAuthConfig] = {
    "new-provider": OAuthConfig(
        service_name="new-provider",
        client_id="",  # From env or parameter
        auth_url="https://auth.example.com/authorize",
        token_url="https://auth.example.com/oauth/token",
        scopes=["read:data", "offline_access"],
        display_name="New Provider",
        setup_url="https://developer.example.com/apps/",
    ),
}
```

### Step 3: Use via CLI

```bash
# List available servers
context-harness mcp list

# Add without auth
context-harness mcp add exa

# Add with API key
context-harness mcp add context7 --api-key YOUR_KEY

# OAuth flow
context-harness mcp auth atlassian --client-id YOUR_CLIENT_ID
context-harness mcp add atlassian
```

## OAuth 2.1 with PKCE Flow

### Understanding the Flow

```
┌─────────┐                               ┌─────────────┐
│  CLI    │                               │ Auth Server │
└────┬────┘                               └──────┬──────┘
     │ 1. Generate PKCE challenge                │
     │    (code_verifier → SHA256 → challenge)   │
     │                                           │
     │ 2. Open browser with auth URL             │
     ├──────────────────────────────────────────►│
     │    ?code_challenge=...&state=...          │
     │                                           │
     │ 3. User authenticates                     │
     │                                           │
     │ 4. Callback with authorization code       │
     │◄──────────────────────────────────────────┤
     │    /callback?code=...&state=...           │
     │                                           │
     │ 5. Exchange code + verifier for tokens    │
     ├──────────────────────────────────────────►│
     │    POST /token {code, code_verifier}      │
     │                                           │
     │ 6. Receive access + refresh tokens        │
     │◄──────────────────────────────────────────┤
     │                                           │
```

### PKCE Generation

```python
def _generate_pkce() -> PKCEChallenge:
    """Generate PKCE challenge pair using S256."""
    random_bytes = secrets.token_bytes(32)
    code_verifier = base64.urlsafe_b64encode(random_bytes).rstrip(b"=").decode()
    
    verifier_hash = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(verifier_hash).rstrip(b"=").decode()
    
    return PKCEChallenge(
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
```

### Token Storage

Tokens are stored securely in `~/.context-harness/tokens/`:

```python
class FileTokenStorage:
    SERVICE_PREFIX = "context-harness"
    TOKEN_DIR = ".context-harness/tokens"
    
    def save_tokens(self, service: str, tokens: OAuthTokens) -> None:
        token_path = self._get_token_path(service)
        token_path.write_text(json.dumps(tokens.to_dict()))
        token_path.chmod(0o600)  # Restrictive permissions
```

## Token Refresh and Expiration

### Check Token Validity

```python
# OAuthTokens.is_expired() with 60-second buffer
def is_expired(self, buffer_seconds: int = 60) -> bool:
    if self.expires_in is None:
        return False
    return time.time() > (self.issued_at + self.expires_in - buffer_seconds)
```

### Automatic Refresh

```python
def ensure_valid_token(self, service_name: str) -> Result[OAuthTokens]:
    """Get valid token, refreshing if expired."""
    tokens = self.storage.load_tokens(service_name)
    
    if not tokens.is_expired():
        return Success(value=tokens)
    
    # Token expired, try refresh
    if tokens.refresh_token:
        return self.refresh_tokens(service_name)
    
    return Failure(
        error="Token expired and no refresh token available",
        code=ErrorCode.TOKEN_EXPIRED,
    )
```

### Update MCP Config After OAuth

```python
def update_auth(
    self,
    server_name: str,
    bearer_token: str,
    project_path: Optional[Path] = None,
) -> Result[MCPServerConfig]:
    """Update auth header for configured server."""
    config_dict["headers"] = {"Authorization": f"Bearer {bearer_token}"}
    return self.config_service.update_mcp(server_name, config_dict, project_path)
```

## opencode.json Configuration

### Structure

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "your-api-key"
      }
    },
    "atlassian": {
      "type": "remote",
      "url": "https://mcp.atlassian.com/v1/mcp",
      "headers": {
        "Authorization": "Bearer <oauth-token>"
      }
    }
  }
}
```

### Server Types

| Type | Fields | Example |
|------|--------|---------|
| `remote` | url, headers | HTTP/SSE servers |
| `local` | command, args, env | stdio processes |

## Quick Reference

### MCPService Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `list_available()` | `Result[List[MCPServer]]` | Get registry servers |
| `list_configured(path)` | `Result[Dict[str, MCPServerConfig]]` | Get configured servers |
| `get_server_info(name)` | `Result[MCPServer]` | Get server details |
| `add(name, path, api_key)` | `Result[MCPServerConfig]` | Add to opencode.json |
| `remove(name, path)` | `Result[bool]` | Remove from config |
| `requires_auth(name)` | `Result[MCPAuthType]` | Check auth requirement |
| `update_auth(name, token)` | `Result[MCPServerConfig]` | Update bearer token |
| `validate_config(name)` | `Result[bool]` | Validate configuration |

### OAuthService Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `list_providers()` | `Result[List[OAuthProvider]]` | Available OAuth providers |
| `get_status(service)` | `Result[AuthStatus]` | Check auth status |
| `authenticate(service)` | `Result[OAuthTokens]` | Run OAuth flow |
| `refresh_tokens(service)` | `Result[OAuthTokens]` | Refresh access token |
| `ensure_valid_token(service)` | `Result[OAuthTokens]` | Get valid token |
| `get_bearer_token(service)` | `Result[str]` | Get access token string |
| `logout(service)` | `Result[bool]` | Remove stored tokens |

### CLI Commands

```bash
# Server management
context-harness mcp list                    # List configured servers
context-harness mcp add                     # Interactive picker
context-harness mcp add context7            # Add specific server
context-harness mcp add context7 -k KEY     # With API key

# OAuth authentication
context-harness mcp auth atlassian          # Start OAuth flow
context-harness mcp auth atlassian --status # Check status
context-harness mcp auth atlassian --logout # Remove tokens
```

## Troubleshooting

### Common Errors

| Error Code | Cause | Solution |
|------------|-------|----------|
| `NOT_FOUND` | Unknown server name | Check `mcp list` for available servers |
| `AUTH_REQUIRED` | Missing authentication | Run `mcp auth` or add `--api-key` |
| `TOKEN_EXPIRED` | OAuth token expired | Re-run `mcp auth` to refresh |
| `CONFIG_MISSING` | No opencode.json | Run `context-harness init` first |
| `TIMEOUT` | OAuth callback not received | Check browser, retry flow |

### OAuth Setup Issues

**"Client ID not configured"**
```bash
# Option 1: Environment variable
export ATLASSIAN_CLIENT_ID=your_client_id
context-harness mcp auth atlassian

# Option 2: CLI flag
context-harness mcp auth atlassian --client-id your_client_id
```

**"State mismatch - possible CSRF attack"**
- Browser returned to wrong callback
- Multiple auth flows running
- Solution: Close extra browser tabs, retry

**"No refresh token available"**
- Provider didn't return refresh token
- Missing `offline_access` scope
- Solution: Re-authenticate with proper scopes

### Token Location

```bash
# Tokens stored in home directory
ls ~/.context-harness/tokens/
# atlassian.json  context7.json

# Check token permissions (should be 600)
ls -la ~/.context-harness/tokens/
```

## Common Pitfalls

### ❌ Don't: Store tokens in opencode.json

```json
{
  "mcp": {
    "atlassian": {
      "oauth_tokens": { "access_token": "..." }  
    }
  }
}
```

### ✅ Do: Use Authorization header with token from storage

```json
{
  "mcp": {
    "atlassian": {
      "headers": { "Authorization": "Bearer <from-token-storage>" }
    }
  }
}
```

### ❌ Don't: Hardcode API keys

```python
headers = {"CONTEXT7_API_KEY": "abc123"}  # ❌ Hardcoded
```

### ✅ Do: Use environment variables or CLI input

```python
api_key = os.environ.get("CONTEXT7_API_KEY")  # ✅ From environment
```

### ❌ Don't: Skip auth validation

```python
result = service.add("atlassian", path)  # ❌ No auth check
```

### ✅ Do: Check auth requirements first

```python
auth_result = service.requires_auth("atlassian")
if isinstance(auth_result, Success) and auth_result.value == MCPAuthType.OAUTH:
    # Run OAuth flow first
    oauth_service.authenticate("atlassian")
```

## Testing MCP Integration

### Unit Test Pattern

```python
def test_add_server_with_api_key(tmp_path: Path) -> None:
    """Should add server with API key header."""
    service = MCPService()
    result = service.add("context7", tmp_path, api_key="test-key")
    
    assert isinstance(result, Success)
    assert "CONTEXT7_API_KEY" in result.value.headers
```

### Mock Token Storage

```python
from context_harness.services.oauth_service import MemoryTokenStorage

def test_oauth_status() -> None:
    storage = MemoryTokenStorage()
    tokens = OAuthTokens(access_token="test", expires_in=3600)
    storage.save_tokens("atlassian", tokens)
    
    service = OAuthService(token_storage=storage)
    result = service.get_status("atlassian")
    
    assert result.value == AuthStatus.AUTHENTICATED
```

## References

- [mcp_service.py](../../../src/context_harness/services/mcp_service.py) - MCPService implementation
- [oauth_service.py](../../../src/context_harness/services/oauth_service.py) - OAuth flow implementation
- [primitives/mcp.py](../../../src/context_harness/primitives/mcp.py) - MCP primitives
- [primitives/oauth.py](../../../src/context_harness/primitives/oauth.py) - OAuth primitives
- [mcp_cmd.py](../../../src/context_harness/interfaces/cli/mcp_cmd.py) - CLI commands
- [opencode.json](../../../opencode.json) - Configuration example

---

_Skill: mcp-integration v1.0.0 | Last updated: 2025-12-31_
