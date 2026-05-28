---
name: mcp-authentication
description: "MCP authentication patterns (API Key, JWT, OAuth 2.1). Use when asking 'MCP auth', 'authentication', 'API key', 'JWT mcp', 'OAuth mcp', or 'mcp security'."
---

# MCP Authentication Patterns

Secure MCP server connections with API keys, JWT tokens, and OAuth 2.1.

> **Skill Metadata**
> Category: `mcp`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`mcp-transports-quick`](mcp-transports-quick.md), [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)
> Related Subagents: `mcp-specialist` (security implementation, OAuth flows)

## Quick Reference

- **API Key**: Simple token-based authentication (headers or query params)
- **JWT**: Stateless token authentication with claims
- **OAuth 2.1**: Industry-standard delegated authorization
- **Security**: Always use HTTPS in production, rotate credentials regularly

## Authentication Patterns

### API Key Authentication

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime
import os

workflow = WorkflowBuilder()

# Header-based API key
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Search documents"}],
    "mcp_servers": [{
        "name": "docs",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            "X-API-Key": os.getenv("MCP_API_KEY"),
            "X-Tenant-ID": "tenant_123"
        }
    }]
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

**API Key Best Practices:**
- Store keys in environment variables (never hardcode)
- Use different keys for dev/staging/production
- Rotate keys regularly (90 days recommended)
- Monitor key usage for anomalies

### Bearer Token Authentication

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Get weather data"}],
    "mcp_servers": [{
        "name": "weather",
        "transport": "http",
        "url": "https://weather-api.com/mcp",
        "headers": {
            "Authorization": f"Bearer {os.getenv('WEATHER_TOKEN')}"
        }
    }]
})
```

### JWT Token Authentication

```python
import jwt
from datetime import datetime, timedelta

# Generate JWT token
def create_jwt_token(secret_key, user_id, tenant_id):
    payload = {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

# Use JWT in MCP request
jwt_token = create_jwt_token(
    secret_key=os.getenv("JWT_SECRET"),
    user_id="user_123",
    tenant_id="tenant_456"
)

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Process data"}],
    "mcp_servers": [{
        "name": "processor",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            "Authorization": f"Bearer {jwt_token}"
        }
    }]
})
```

**JWT Benefits:**
- Stateless (no server-side session storage)
- Contains user/tenant information
- Expires automatically
- Can be validated without database lookup

### OAuth 2.1 Authentication

```python
from requests_oauthlib import OAuth2Session

# OAuth 2.1 flow
def get_oauth_token(client_id, client_secret, token_url):
    """Obtain OAuth 2.1 access token."""
    from requests.auth import HTTPBasicAuth
    import requests

    response = requests.post(
        token_url,
        auth=HTTPBasicAuth(client_id, client_secret),
        data={"grant_type": "client_credentials"}
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"OAuth failed: {response.text}")

# Get token
oauth_token = get_oauth_token(
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    token_url="https://auth.company.com/oauth/token"
)

# Use OAuth token
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Access protected resource"}],
    "mcp_servers": [{
        "name": "protected",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            "Authorization": f"Bearer {oauth_token}"
        }
    }]
})
```

### Custom Authentication Headers

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Multi-factor auth"}],
    "mcp_servers": [{
        "name": "secure",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            "X-API-Key": os.getenv("API_KEY"),
            "X-User-ID": "user_123",
            "X-Tenant-ID": "tenant_456",
            "X-Session-Token": os.getenv("SESSION_TOKEN"),
            "X-HMAC-Signature": compute_hmac_signature()  # Custom HMAC
        }
    }]
})
```

## Multi-Tenant Authentication

### Tenant-Specific Tokens

```python
# Different tokens per tenant
tenant_tokens = {
    "tenant_a": os.getenv("TENANT_A_TOKEN"),
    "tenant_b": os.getenv("TENANT_B_TOKEN"),
    "tenant_c": os.getenv("TENANT_C_TOKEN")
}

def create_mcp_workflow(tenant_id):
    workflow = WorkflowBuilder()

    workflow.add_node("IterativeLLMAgentNode", "agent", {
        "provider": "openai",
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Get tenant data"}],
        "mcp_servers": [{
            "name": "data",
            "transport": "http",
            "url": "https://api.company.com/mcp",
            "headers": {
                "Authorization": f"Bearer {tenant_tokens[tenant_id]}",
                "X-Tenant-ID": tenant_id
            }
        }]
    })

    return workflow
```

## Token Refresh Patterns

### Automatic Token Refresh

```python
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.token = None
        self.expires_at = None

    def get_token(self):
        """Get valid token, refreshing if needed."""
        if not self.token or datetime.now() >= self.expires_at:
            self.refresh_token()
        return self.token

    def refresh_token(self):
        """Refresh OAuth token."""
        import requests
        from requests.auth import HTTPBasicAuth

        response = requests.post(
            self.token_url,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"}
        )

        data = response.json()
        self.token = data["access_token"]
        self.expires_at = datetime.now() + timedelta(seconds=data["expires_in"] - 60)

# Use token manager
token_manager = TokenManager(
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    token_url="https://auth.company.com/oauth/token"
)

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "api",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            "Authorization": f"Bearer {token_manager.get_token()}"
        }
    }]
})
```

## Security Best Practices

### Environment-Based Configuration

```python
# .env file
# API_KEY=your_api_key_here
# JWT_SECRET=your_jwt_secret
# OAUTH_CLIENT_ID=client_id
# OAUTH_CLIENT_SECRET=client_secret

from dotenv import load_dotenv
import os

load_dotenv()

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "secure",
        "transport": "http",
        "url": os.getenv("MCP_URL"),
        "headers": {
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }
    }]
})
```

### HMAC Signature Authentication

```python
import hmac
import hashlib
import time

def compute_hmac_signature(secret, payload):
    """Compute HMAC signature for request payload."""
    timestamp = str(int(time.time()))
    message = f"{timestamp}.{payload}"

    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return {
        "X-Timestamp": timestamp,
        "X-Signature": signature
    }

# Use HMAC authentication
secret = os.getenv("HMAC_SECRET")
payload = '{"action": "search", "query": "documents"}'
auth_headers = compute_hmac_signature(secret, payload)

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "hmac_protected",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            **auth_headers,
            "Content-Type": "application/json"
        }
    }]
})
```

## Authentication Error Handling

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Get data"}],
    "mcp_servers": [{
        "name": "api",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {
            "Authorization": f"Bearer {os.getenv('API_TOKEN')}"
        },
        "retry_config": {
            "max_retries": 3,
            "retry_on": [401, 403],  # Retry on auth failures
            "backoff_factor": 2.0
        }
    }]
})

# IterativeLLMAgentNode handles 401/403 by retrying or graceful fallback
```

## Common Patterns

### Pattern 1: Multi-Environment Auth

```python
auth_config = {
    "development": {
        "url": "http://localhost:8000/mcp",
        "headers": {"X-Dev-Token": "dev_token"}
    },
    "staging": {
        "url": "https://staging-api.com/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('STAGING_TOKEN')}"}
    },
    "production": {
        "url": "https://api.company.com/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('PROD_TOKEN')}"}
    }
}

env = os.getenv("ENV", "development")
config = auth_config[env]

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{"name": "api", "transport": "http", **config}]
})
```

### Pattern 2: Credential Rotation

```python
# Rotate credentials automatically
class CredentialRotator:
    def __init__(self):
        self.primary_key = os.getenv("API_KEY_PRIMARY")
        self.secondary_key = os.getenv("API_KEY_SECONDARY")
        self.use_primary = True

    def get_key(self):
        return self.primary_key if self.use_primary else self.secondary_key

    def rotate(self):
        self.use_primary = not self.use_primary

rotator = CredentialRotator()

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "api",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "headers": {"X-API-Key": rotator.get_key()}
    }]
})
```

## When to Use Each Method

| Method | Use When | Security Level |
|--------|----------|----------------|
| **API Key** | Simple services, internal APIs | Medium |
| **Bearer Token** | Short-lived access | Medium-High |
| **JWT** | Stateless auth, microservices | High |
| **OAuth 2.1** | Third-party access, delegated auth | Very High |
| **HMAC** | Request integrity verification | Very High |

## Related Patterns

- **Transport Configuration**: [`mcp-transports-quick`](mcp-transports-quick.md)
- **MCP Integration**: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)

## When to Escalate to Subagent

Use `mcp-specialist` subagent when:
- Implementing OAuth 2.1 authorization flows
- Setting up custom authentication schemes
- Integrating with enterprise identity providers (LDAP, Active Directory)
- Implementing certificate-based authentication
- Troubleshooting authentication failures

## Quick Tips

- Always use environment variables for credentials
- Use HTTPS in production (never HTTP)
- Implement token refresh for long-running workflows
- Monitor authentication failures for security threats
- Rotate credentials regularly (90 days for API keys)

## Version Notes

- **v0.9.25+**: Enhanced authentication support in MCP transports
- **v0.6.5+**: Real MCP tool execution with auth headers

<!-- Trigger Keywords: MCP auth, authentication, API key, JWT, OAuth, mcp security, bearer token, mcp credentials, oauth 2.1, mcp authorization, token authentication -->
