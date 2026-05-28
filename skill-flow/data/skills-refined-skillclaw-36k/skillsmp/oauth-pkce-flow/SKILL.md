---
name: oauth-pkce-flow
description: |
  Implement OAuth 2.1 with PKCE for secure authentication flows in CLI applications.
  This skill provides comprehensive guidance for implementing browser-based OAuth flows
  with local callback servers, token management with automatic refresh, and secure
  credential storage. Use this skill when adding new OAuth providers, implementing
  authentication commands, handling token expiration, or debugging OAuth-related issues.
version: 1.0.0
tags:
  - authentication
  - oauth
  - pkce
  - security
  - mcp
  - cli
---

# OAuth 2.1 with PKCE Flow

## Overview

This skill provides comprehensive guidance for implementing OAuth 2.1 authentication flows with PKCE (Proof Key for Code Exchange) in CLI applications. The context-harness project implements a provider-agnostic OAuth system following the three-layer architecture: **Primitives** (data structures) → **Services** (business logic) → **Interfaces** (CLI/SDK).

Key security features:
- **PKCE with S256**: Mandatory SHA-256 code challenge method per OAuth 2.1
- **State parameter**: CSRF protection via random state verification
- **Secure token storage**: System keyring with file-based fallback (0o600 permissions)
- **Automatic refresh**: Token refresh with 60-second expiration buffer

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERFACES                           │
│  ┌─────────────────┐           ┌─────────────────┐         │
│  │ CLI (mcp auth)  │           │ SDK OAuthClient │         │
│  └────────┬────────┘           └────────┬────────┘         │
└───────────┼─────────────────────────────┼──────────────────┘
            │                             │
            ▼                             ▼
┌─────────────────────────────────────────────────────────────┐
│                        OAuthService                         │
│  authenticate() → refresh_tokens() → ensure_valid_token()  │
│  └── TokenStorageProtocol (FileTokenStorage/MemoryStorage) │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                        PRIMITIVES                           │
│  PKCEChallenge │ OAuthTokens │ OAuthConfig │ AuthStatus    │
└─────────────────────────────────────────────────────────────┘
```

## OAuth Primitives

### PKCEChallenge

Immutable data structure for PKCE code verifier and challenge pair:

```python
from context_harness.primitives import PKCEChallenge

# Created by OAuthService internally
challenge = PKCEChallenge(
    code_verifier="dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk",
    code_challenge="E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
    code_challenge_method="S256",  # Always S256 for OAuth 2.1
)
```

### OAuthTokens

Token storage with expiration tracking:

```python
from context_harness.primitives import OAuthTokens
import time

tokens = OAuthTokens(
    access_token="eyJhbGciOi...",
    token_type="Bearer",
    expires_in=3600,
    refresh_token="dGhpcyBpcyBhIHJlZnJlc2g...",
    scope="read:jira-work offline_access",
    issued_at=time.time(),
)

# Check expiration with 60-second buffer
if tokens.is_expired(buffer_seconds=60):
    # Token needs refresh
    pass

# Serialize for storage
token_dict = tokens.to_dict()
restored = OAuthTokens.from_dict(token_dict)

# Create from OAuth token response
tokens = OAuthTokens.from_response(response_data)
```

### OAuthConfig and OAuthProvider

Provider configuration with template pattern:

```python
from context_harness.primitives import OAuthConfig, OAuthProvider

# OAuthProvider: Template without credentials
GITHUB_PROVIDER = OAuthProvider(
    service_name="github",
    auth_url="https://github.com/login/oauth/authorize",
    token_url="https://github.com/login/oauth/access_token",
    scopes=["repo", "user"],
    display_name="GitHub",
    setup_url="https://github.com/settings/developers",
)

# OAuthConfig: Runtime configuration with credentials
config = GITHUB_PROVIDER.to_config(
    client_id="your-client-id",
    client_secret="your-client-secret",  # Optional for public clients
)
```

### AuthStatus

Authentication state enumeration:

```python
from context_harness.primitives import AuthStatus

# Possible states
AuthStatus.NOT_AUTHENTICATED  # No tokens stored
AuthStatus.AUTHENTICATED      # Valid tokens available
AuthStatus.TOKEN_EXPIRED      # Tokens expired, need refresh
AuthStatus.TOKEN_REFRESH_FAILED  # Refresh attempted and failed
```

## Using OAuthService

### Basic Authentication Flow

```python
from context_harness.services import OAuthService
from context_harness.primitives import AuthStatus, Success, Failure

service = OAuthService()

# Check current status
status = service.get_status("atlassian")
if isinstance(status, Success):
    if status.value == AuthStatus.NOT_AUTHENTICATED:
        # Run authentication flow
        result = service.authenticate(
            "atlassian",
            client_id="your-client-id",  # Or set ATLASSIAN_CLIENT_ID env var
            open_browser=True,
        )
        if isinstance(result, Success):
            print(f"Authenticated! Token: {result.value.access_token[:20]}...")
        else:
            print(f"Auth failed: {result.error}")
```

### Getting Valid Tokens

```python
# Ensure valid token (auto-refreshes if expired)
result = service.ensure_valid_token("atlassian")
if isinstance(result, Success):
    tokens = result.value
    # Use tokens.access_token for API calls
else:
    if result.code == ErrorCode.AUTH_REQUIRED:
        # Need to authenticate first
        pass
    elif result.code == ErrorCode.TOKEN_EXPIRED:
        # No refresh token available
        pass

# Simple bearer token retrieval
bearer_result = service.get_bearer_token("atlassian")
if isinstance(bearer_result, Success):
    headers = {"Authorization": f"Bearer {bearer_result.value}"}
```

### Token Refresh

```python
# Manual refresh
result = service.refresh_tokens("atlassian")
if isinstance(result, Failure):
    if result.code == ErrorCode.TOKEN_REFRESH_FAILED:
        # User needs to re-authenticate
        print("Please run 'context-harness mcp auth atlassian'")
```

## Using SDK OAuthClient

The SDK provides a convenient wrapper around OAuthService:

```python
from context_harness.interfaces.sdk import create_client
from context_harness.primitives import AuthStatus, Success

client = create_client()

# Check status
status = client.oauth.get_status("atlassian")
if isinstance(status, Success) and status.value == AuthStatus.AUTHENTICATED:
    # Get tokens
    tokens = client.oauth.get_tokens("atlassian")
    if isinstance(tokens, Success):
        print(f"Access token: {tokens.value.access_token[:20]}...")

# Ensure valid token (with auto-refresh)
valid = client.oauth.ensure_valid("atlassian")
if isinstance(valid, Success):
    # Use valid.value.access_token
    pass

# Authenticate if needed
result = client.oauth.authenticate("atlassian", open_browser=True)

# Logout
client.oauth.logout("atlassian")
```

## Adding a New OAuth Provider

### Step 1: Define Provider Template

Add to `src/context_harness/services/oauth_service.py`:

```python
OAUTH_PROVIDERS: Dict[str, OAuthConfig] = {
    # Existing providers...
    "github": OAuthConfig(
        service_name="github",
        client_id="",  # Populated at runtime
        auth_url="https://github.com/login/oauth/authorize",
        token_url="https://github.com/login/oauth/access_token",
        scopes=["repo", "read:user"],
        display_name="GitHub",
        setup_url="https://github.com/settings/developers",
    ),
}
```

### Step 2: Handle Provider-Specific Requirements

Some providers require additional parameters:

```python
# Provider with audience (like Atlassian)
"atlassian": OAuthConfig(
    service_name="atlassian",
    client_id="",
    auth_url="https://auth.atlassian.com/authorize",
    token_url="https://auth.atlassian.com/oauth/token",
    scopes=["read:jira-work", "offline_access"],
    audience="api.atlassian.com",  # Required by Atlassian
    resources_url="https://api.atlassian.com/oauth/token/accessible-resources",
    display_name="Atlassian",
),

# Provider with extra auth params
"custom": OAuthConfig(
    service_name="custom",
    client_id="",
    auth_url="https://auth.custom.com/oauth/authorize",
    token_url="https://auth.custom.com/oauth/token",
    scopes=["read", "write"],
    extra_auth_params={"prompt": "consent"},  # Extra params
),
```

### Step 3: Register Callback URL

Configure your OAuth app with callback URL:
- **Development**: `http://localhost:8080/callback`
- **Alternative ports**: 3000, 57548 (tried in order)

### Step 4: Set Environment Variables

```bash
export GITHUB_CLIENT_ID="your-client-id"
export GITHUB_CLIENT_SECRET="your-client-secret"  # Optional for public clients
```

### Step 5: Test Authentication

```bash
context-harness mcp auth github
```

## Token Storage Architecture

### Storage Protocol

```python
class TokenStorageProtocol(Protocol):
    """Protocol for OAuth token storage backends."""
    
    def save_tokens(self, service: str, tokens: OAuthTokens) -> None: ...
    def load_tokens(self, service: str) -> Optional[OAuthTokens]: ...
    def delete_tokens(self, service: str) -> bool: ...
```

### FileTokenStorage (Default)

```python
class FileTokenStorage:
    SERVICE_PREFIX = "context-harness"
    TOKEN_DIR = ".context-harness/tokens"
    
    # Stores tokens at: ~/.context-harness/tokens/{service}.json
    # Directory permissions: 0o700
    # File permissions: 0o600
    
    # Uses system keyring when available (more secure)
    # Falls back to file storage if keyring unavailable
```

### MemoryTokenStorage (Testing)

```python
from context_harness.services.oauth_service import MemoryTokenStorage

# Use for testing without file I/O
storage = MemoryTokenStorage()
service = OAuthService(token_storage=storage)
```

## Quick Reference

| Component | Location | Purpose |
|-----------|----------|---------|
| `PKCEChallenge` | `primitives/oauth.py` | PKCE verifier/challenge pair |
| `OAuthTokens` | `primitives/oauth.py` | Token storage with expiration |
| `OAuthConfig` | `primitives/oauth.py` | Runtime provider config |
| `OAuthProvider` | `primitives/oauth.py` | Provider template |
| `AuthStatus` | `primitives/oauth.py` | Auth state enumeration |
| `OAuthService` | `services/oauth_service.py` | Business logic |
| `FileTokenStorage` | `services/oauth_service.py` | Secure file storage |
| `OAuthClient` | `interfaces/sdk/client.py` | SDK wrapper |

## Error Handling

All methods return `Result[T]` types:

| ErrorCode | Meaning | Resolution |
|-----------|---------|------------|
| `AUTH_REQUIRED` | Not authenticated | Run authenticate() |
| `AUTH_FAILED` | Auth flow failed | Check credentials |
| `AUTH_CANCELLED` | User denied access | User action required |
| `TOKEN_EXPIRED` | Access token expired | Use ensure_valid_token() |
| `TOKEN_REFRESH_FAILED` | Refresh failed | Re-authenticate |
| `CONFIG_MISSING` | Client ID not set | Set env var or provide client_id |
| `NOT_FOUND` | Unknown provider | Check provider name |
| `TIMEOUT` | Callback timeout | User didn't complete flow |
| `NETWORK_ERROR` | Network issue | Check connectivity |

## Troubleshooting

### "Client ID not configured"

```bash
# Set environment variable
export ATLASSIAN_CLIENT_ID="your-client-id"

# Or provide directly
service.authenticate("atlassian", client_id="your-client-id")
```

### "Token expired and no refresh token"

Ensure `offline_access` scope is included for providers that support refresh tokens:

```python
scopes=["read:jira-work", "offline_access"],  # Include offline_access
```

### "State mismatch - possible CSRF attack"

This indicates the state parameter didn't match. Usually caused by:
- Multiple auth flows running simultaneously
- Browser caching old auth URLs

**Solution**: Restart the authentication flow.

### "OAuth callback not received within X seconds"

- Ensure browser opened the auth URL
- Check if port (8080, 3000, or 57548) is available
- Verify callback URL is registered with OAuth provider

### Token file permission issues

```bash
# Check/fix permissions
chmod 700 ~/.context-harness/tokens
chmod 600 ~/.context-harness/tokens/*.json
```

## Common Pitfalls

### ❌ Don't: Store tokens in code

```python
# WRONG - hardcoded tokens
tokens = OAuthTokens(access_token="eyJhbG...")
```

### ✅ Do: Use OAuthService for token management

```python
# CORRECT - service handles storage
result = service.get_tokens("atlassian")
```

### ❌ Don't: Ignore expiration

```python
# WRONG - token might be expired
tokens = service.get_tokens("atlassian").value
use_token(tokens.access_token)  # May fail!
```

### ✅ Do: Use ensure_valid_token

```python
# CORRECT - auto-refreshes if needed
result = service.ensure_valid_token("atlassian")
if isinstance(result, Success):
    use_token(result.value.access_token)
```

### ❌ Don't: Skip error handling

```python
# WRONG - assumes success
tokens = service.authenticate("atlassian").value
```

### ✅ Do: Handle Result types

```python
# CORRECT - explicit error handling
result = service.authenticate("atlassian")
if isinstance(result, Success):
    tokens = result.value
else:
    handle_error(result.error, result.code)
```

## References

- [OAuth primitives](../../../src/context_harness/primitives/oauth.py) - Data structures
- [OAuthService](../../../src/context_harness/services/oauth_service.py) - Business logic
- [OAuthClient](../../../src/context_harness/interfaces/sdk/client.py) - SDK wrapper
- [OAuth tests](../../../tests/unit/services/test_oauth_service.py) - Test examples
- [OAuth 2.1 Spec](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) - RFC reference
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636) - PKCE specification

---

_Skill: oauth-pkce-flow v1.0.0 | Last updated: 2025-12-31_
