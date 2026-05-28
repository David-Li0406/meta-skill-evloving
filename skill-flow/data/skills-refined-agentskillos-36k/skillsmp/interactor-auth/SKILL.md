---
name: interactor-auth
version: 1.1.0
description: Setup Interactor platform authentication with OAuth client credentials. Use when integrating with Interactor for credential management, AI agents, or workflows. Covers account registration, OAuth client creation, token management, and secret rotation.
author: Interactor Integration Guide
requires:
  - Bash (for curl commands and verification scripts)
  - Write (for environment file creation)
  - Read (for verifying configuration)
---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-21 | Added: Token revocation, distributed caching, webhook verification, observability, SRE runbook, FAQ. Fixed: Issuer consistency, rate limit scope. |
| 1.0.0 | 2026-01-20 | Initial release |


# Interactor Setup and Authentication Skill

Configure authentication for the Interactor platform to enable credential management, AI agents, and workflow automation.

## When to Use

- **Initial Setup**: Setting up a new integration with Interactor platform
- **OAuth Client Management**: Creating, listing, or rotating OAuth client credentials
- **Token Management**: Implementing token caching, refresh, and error handling
- **Secret Rotation**: Rotating client secrets without service interruption
- **Backend Authentication**: Connecting your backend to Interactor APIs

## When NOT to Use

- **Frontend Authentication**: Never use client credentials in browser/mobile apps. See `interactor-sdk` for frontend auth patterns.
- **End-User Authentication**: Interactor doesn't manage your end users. Use your own auth system for that.
- **Already Integrated**: If your backend already has working Interactor authentication, use the specific skill for your task (credentials, agents, workflows, etc.).
- **Testing Only**: For quick API exploration, use the Interactor dashboard instead of setting up full OAuth.

## Prerequisites

Before using this skill, understand the Interactor architecture:

```
┌─────────────────────────────────────────────────────────────────────┐
│  YOUR APPLICATION                                                    │
│                                                                      │
│  Your Users ──────> Your Backend ──────> INTERACTOR                 │
│  (you manage auth)  (client_credentials)  (platform APIs)           │
│                     (namespaces per user)                           │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Insight**: Interactor does NOT manage your end users. Your backend authenticates to Interactor and calls APIs on behalf of your users using namespaces.

## Base URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Account Server** | `https://auth.interactor.com/api/v1` | Authentication, user/org management |
| **Interactor API** | `https://core.interactor.com/api/v1` | Core platform APIs |
| **JWKS Endpoint** | `https://auth.interactor.com/oauth/jwks` | Public keys for JWT verification |

> **Project Security Rules**: This skill implements the "Use Interactor Authentication" section of `.claude/rules/i/security.md`. See that file for project-wide authentication requirements.

---

## Instructions

### Step 1: Register Your Organization

Create an account with the Account Server:

```bash
curl -X POST https://auth.interactor.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@yourcompany.com",
    "password": "SecureP@ssw0rd!",
    "organization_name": "Your Company Inc"
  }'
```

**Response (Success):**
```json
{
  "data": {
    "id": "acc_abc123",
    "email": "developer@yourcompany.com",
    "organization_id": "org_xyz789",
    "organization_name": "Your Company Inc",
    "email_verified": false
  }
}
```

**Password Requirements:**
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

After registration, check your email and click the verification link to set `email_verified: true`.

### Step 2: Login to Get User Token

```bash
curl -X POST https://auth.interactor.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@yourcompany.com",
    "password": "SecureP@ssw0rd!"
  }'
```

**Response:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

Save this `access_token` - you'll need it to create OAuth client credentials.

### Step 3: Create OAuth Client Credentials

Create credentials for your backend to authenticate with Interactor:

```bash
curl -X POST https://auth.interactor.com/api/v1/account/oauth-clients \
  -H "Authorization: Bearer <user_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Production Backend"}'
```

**Response:**
```json
{
  "data": {
    "client_id": "client_abc123",
    "client_secret": "secret_xyz789_SAVE_THIS",
    "name": "My Production Backend"
  }
}
```

> **CRITICAL**: Save `client_secret` securely - it's only shown once and cannot be retrieved later!

#### OAuth Client Scopes and Permissions

By default, OAuth clients have full access to your organization's resources. You can restrict access using scopes:

```bash
curl -X POST https://auth.interactor.com/api/v1/account/oauth-clients \
  -H "Authorization: Bearer <user_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Limited Access Backend",
    "scopes": ["credentials:read", "agents:read"]
  }'
```

**Available Scopes:**

| Scope | Description |
|-------|-------------|
| `credentials:read` | Read credential configurations |
| `credentials:write` | Create/update/delete credentials |
| `agents:read` | Read AI agent configurations |
| `agents:write` | Create/update/delete agents |
| `agents:execute` | Execute agent conversations |
| `workflows:read` | Read workflow definitions |
| `workflows:write` | Create/update/delete workflows |
| `workflows:execute` | Trigger workflow executions |
| `webhooks:read` | Read webhook configurations |
| `webhooks:write` | Create/update/delete webhooks |
| `*` | Full access (default if no scopes specified) |

**Grant Types:**

Interactor OAuth clients support these grant types:

| Grant Type | Use Case |
|------------|----------|
| `client_credentials` | Backend-to-backend authentication (default, always enabled) |

> **Note**: Authorization code and refresh token grants are not supported for OAuth clients. User authentication uses a separate flow via the Account Server.

### Step 4: Configure Environment Variables

Add credentials to your backend's environment:

```bash
# .env (DO NOT commit this file)
INTERACTOR_CLIENT_ID=client_abc123
INTERACTOR_CLIENT_SECRET=secret_xyz789_SAVE_THIS
```

```bash
# .env.example (commit this template)
INTERACTOR_CLIENT_ID=your_client_id_here
INTERACTOR_CLIENT_SECRET=your_client_secret_here
```

### Step 5: Exchange Credentials for Access Token

Your backend exchanges client credentials for an access token:

```bash
curl -X POST https://auth.interactor.com/api/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "client_abc123",
    "client_secret": "secret_xyz789_SAVE_THIS"
  }'
```

**Response:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

### Step 6: Call Interactor APIs

Use the access token to call any Interactor API:

```bash
curl https://core.interactor.com/api/v1/credentials/summary \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."
```

---

## Token Management Implementation

Access tokens expire after **15 minutes**. Implement caching and proactive refresh.

### TypeScript Implementation

```typescript
import axios from 'axios';

interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

interface ApiResponse<T> {
  data: T;
}

export class InteractorClient {
  private clientId: string;
  private clientSecret: string;
  private accessToken: string | null = null;
  private tokenExpiry: Date | null = null;

  constructor(clientId?: string, clientSecret?: string) {
    this.clientId = clientId || process.env.INTERACTOR_CLIENT_ID!;
    this.clientSecret = clientSecret || process.env.INTERACTOR_CLIENT_SECRET!;

    if (!this.clientId || !this.clientSecret) {
      throw new Error('INTERACTOR_CLIENT_ID and INTERACTOR_CLIENT_SECRET are required');
    }
  }

  /**
   * Get a valid access token, refreshing if necessary.
   * Refreshes 60 seconds before expiry to avoid edge cases.
   */
  async getToken(): Promise<string> {
    // Return cached token if still valid (with 60s buffer)
    if (this.accessToken && this.tokenExpiry && this.tokenExpiry > new Date()) {
      return this.accessToken;
    }

    try {
      const response = await axios.post<ApiResponse<TokenResponse>>(
        'https://auth.interactor.com/api/v1/oauth/token',
        {
          grant_type: 'client_credentials',
          client_id: this.clientId,
          client_secret: this.clientSecret
        },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );

      this.accessToken = response.data.data.access_token;
      // Refresh 60 seconds before actual expiry
      this.tokenExpiry = new Date(Date.now() + (response.data.data.expires_in - 60) * 1000);

      return this.accessToken;
    } catch (error: any) {
      if (error.response?.data?.error) {
        throw new Error(`Token exchange failed: ${error.response.data.error.message}`);
      }
      throw error;
    }
  }

  /**
   * Make an authenticated request to Interactor API.
   */
  async request<T>(method: string, path: string, data?: any): Promise<T> {
    const token = await this.getToken();

    const response = await axios.request<ApiResponse<T>>({
      method,
      url: `https://core.interactor.com/api/v1${path}`,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data
    });

    return response.data.data;
  }

  /**
   * Force token refresh (useful after secret rotation).
   */
  invalidateToken(): void {
    this.accessToken = null;
    this.tokenExpiry = null;
  }
}

// Usage
const interactor = new InteractorClient();

// All API calls automatically handle token management
const credentials = await interactor.request('GET', '/credentials?namespace=user_123');
```

### Python Implementation

```python
import os
import requests
from datetime import datetime, timedelta
from typing import Optional, Any, Dict

class InteractorClient:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = client_id or os.environ.get('INTERACTOR_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('INTERACTOR_CLIENT_SECRET')

        if not self.client_id or not self.client_secret:
            raise ValueError('INTERACTOR_CLIENT_ID and INTERACTOR_CLIENT_SECRET are required')

        self.access_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.auth_url = 'https://auth.interactor.com/api/v1'
        self.api_url = 'https://core.interactor.com/api/v1'

    def get_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        # Return cached token if still valid (with 60s buffer)
        if self.access_token and self.token_expiry and self.token_expiry > datetime.now():
            return self.access_token

        response = requests.post(
            f'{self.auth_url}/oauth/token',
            json={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            },
            headers={'Content-Type': 'application/json'}
        )

        if not response.ok:
            error = response.json().get('error', {})
            raise Exception(f"Token exchange failed: {error.get('message', response.text)}")

        data = response.json()['data']
        self.access_token = data['access_token']
        # Refresh 60 seconds before actual expiry
        self.token_expiry = datetime.now() + timedelta(seconds=data['expires_in'] - 60)

        return self.access_token

    def request(self, method: str, path: str, data: Optional[Dict] = None) -> Any:
        """Make an authenticated request to Interactor API."""
        token = self.get_token()

        response = requests.request(
            method,
            f'{self.api_url}{path}',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json=data
        )

        if not response.ok:
            error = response.json().get('error', {})
            raise Exception(f"API request failed: {error.get('message', response.text)}")

        return response.json().get('data')

    def invalidate_token(self) -> None:
        """Force token refresh (useful after secret rotation)."""
        self.access_token = None
        self.token_expiry = None


# Usage
interactor = InteractorClient()

# All API calls automatically handle token management
credentials = interactor.request('GET', '/credentials?namespace=user_123')
```

### Elixir Implementation

```elixir
defmodule MyApp.Interactor.Client do
  @moduledoc """
  Interactor API client with automatic token management.
  """

  use GenServer
  require Logger

  @auth_url "https://auth.interactor.com/api/v1"
  @api_url "https://core.interactor.com/api/v1"
  @token_buffer_seconds 60

  # Client API

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Make an authenticated request to Interactor API.
  """
  def request(method, path, body \\ nil) do
    GenServer.call(__MODULE__, {:request, method, path, body})
  end

  @doc """
  Force token refresh.
  """
  def invalidate_token do
    GenServer.cast(__MODULE__, :invalidate_token)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    client_id = Application.fetch_env!(:my_app, :interactor_client_id)
    client_secret = Application.fetch_env!(:my_app, :interactor_client_secret)

    {:ok, %{
      client_id: client_id,
      client_secret: client_secret,
      access_token: nil,
      token_expiry: nil
    }}
  end

  @impl true
  def handle_call({:request, method, path, body}, _from, state) do
    case get_valid_token(state) do
      {:ok, token, new_state} ->
        result = make_request(method, path, body, token)
        {:reply, result, new_state}

      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end

  @impl true
  def handle_cast(:invalidate_token, state) do
    {:noreply, %{state | access_token: nil, token_expiry: nil}}
  end

  # Private Functions

  defp get_valid_token(%{access_token: token, token_expiry: expiry} = state)
       when not is_nil(token) and not is_nil(expiry) do
    if DateTime.compare(expiry, DateTime.utc_now()) == :gt do
      {:ok, token, state}
    else
      refresh_token(state)
    end
  end

  defp get_valid_token(state), do: refresh_token(state)

  defp refresh_token(%{client_id: client_id, client_secret: client_secret} = state) do
    body = Jason.encode!(%{
      grant_type: "client_credentials",
      client_id: client_id,
      client_secret: client_secret
    })

    case HTTPoison.post("#{@auth_url}/oauth/token", body, [{"Content-Type", "application/json"}]) do
      {:ok, %{status_code: 200, body: response_body}} ->
        %{"data" => %{"access_token" => token, "expires_in" => expires_in}} = Jason.decode!(response_body)

        expiry = DateTime.utc_now() |> DateTime.add(expires_in - @token_buffer_seconds, :second)
        new_state = %{state | access_token: token, token_expiry: expiry}

        {:ok, token, new_state}

      {:ok, %{body: response_body}} ->
        error = Jason.decode!(response_body)
        Logger.error("Token exchange failed: #{inspect(error)}")
        {:error, :token_exchange_failed}

      {:error, reason} ->
        Logger.error("Token exchange error: #{inspect(reason)}")
        {:error, :network_error}
    end
  end

  defp make_request(method, path, body, token) do
    headers = [
      {"Authorization", "Bearer #{token}"},
      {"Content-Type", "application/json"}
    ]

    url = "#{@api_url}#{path}"
    body_json = if body, do: Jason.encode!(body), else: ""

    case HTTPoison.request(method, url, body_json, headers) do
      {:ok, %{status_code: code, body: response_body}} when code in 200..299 ->
        {:ok, Jason.decode!(response_body)["data"]}

      {:ok, %{status_code: code, body: response_body}} ->
        {:error, %{status: code, body: Jason.decode!(response_body)}}

      {:error, reason} ->
        {:error, reason}
    end
  end
end
```

> **Note on HTTP Clients**: This example uses HTTPoison for broad compatibility. For new Phoenix 1.7+ projects, consider using [`Req`](https://hex.pm/packages/req) (simpler API) or [`Finch`](https://hex.pm/packages/finch) (better performance) instead. The token management logic remains the same.

---

## Distributed Token Caching

For multi-instance deployments (Kubernetes, load-balanced servers), use a shared cache to avoid redundant token requests across instances.

### Redis Implementation (TypeScript)

```typescript
import Redis from 'ioredis';
import axios from 'axios';

interface TokenData {
  access_token: string;
  expires_at: number; // Unix timestamp in milliseconds
}

export class DistributedInteractorClient {
  private redis: Redis;
  private clientId: string;
  private clientSecret: string;
  private cacheKey: string;

  constructor(redisUrl: string, clientId?: string, clientSecret?: string) {
    this.redis = new Redis(redisUrl);
    this.clientId = clientId || process.env.INTERACTOR_CLIENT_ID!;
    this.clientSecret = clientSecret || process.env.INTERACTOR_CLIENT_SECRET!;
    this.cacheKey = `interactor:token:${this.clientId}`;

    if (!this.clientId || !this.clientSecret) {
      throw new Error('INTERACTOR_CLIENT_ID and INTERACTOR_CLIENT_SECRET are required');
    }
  }

  async getToken(): Promise<string> {
    // Try to get from Redis first
    const cached = await this.redis.get(this.cacheKey);
    if (cached) {
      const data: TokenData = JSON.parse(cached);
      // Check if still valid (with 60s buffer)
      if (data.expires_at > Date.now() + 60000) {
        return data.access_token;
      }
    }

    // Use Redis lock to prevent thundering herd
    const lockKey = `${this.cacheKey}:lock`;
    const lockAcquired = await this.redis.set(lockKey, '1', 'EX', 10, 'NX');

    if (!lockAcquired) {
      // Another instance is refreshing, wait and retry
      await new Promise(resolve => setTimeout(resolve, 1000));
      return this.getToken();
    }

    try {
      // Fetch new token
      const response = await axios.post(
        'https://auth.interactor.com/api/v1/oauth/token',
        {
          grant_type: 'client_credentials',
          client_id: this.clientId,
          client_secret: this.clientSecret
        },
        { headers: { 'Content-Type': 'application/json' } }
      );

      const { access_token, expires_in } = response.data.data;
      const expiresAt = Date.now() + (expires_in * 1000);

      // Store in Redis with TTL slightly longer than token expiry
      const tokenData: TokenData = {
        access_token,
        expires_at: expiresAt
      };
      await this.redis.set(
        this.cacheKey,
        JSON.stringify(tokenData),
        'PX',
        expires_in * 1000
      );

      return access_token;
    } finally {
      await this.redis.del(lockKey);
    }
  }

  async invalidateToken(): Promise<void> {
    await this.redis.del(this.cacheKey);
  }

  async close(): Promise<void> {
    await this.redis.quit();
  }
}

// Usage
const client = new DistributedInteractorClient(process.env.REDIS_URL!);
const token = await client.getToken();
```

### Redis Implementation (Python)

```python
import os
import json
import time
import redis
import requests
from typing import Optional

class DistributedInteractorClient:
    def __init__(
        self,
        redis_url: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ):
        self.redis = redis.from_url(redis_url)
        self.client_id = client_id or os.environ.get('INTERACTOR_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('INTERACTOR_CLIENT_SECRET')
        self.cache_key = f'interactor:token:{self.client_id}'

        if not self.client_id or not self.client_secret:
            raise ValueError('INTERACTOR_CLIENT_ID and INTERACTOR_CLIENT_SECRET are required')

    def get_token(self) -> str:
        # Try cache first
        cached = self.redis.get(self.cache_key)
        if cached:
            data = json.loads(cached)
            # Check if still valid (with 60s buffer)
            if data['expires_at'] > (time.time() * 1000) + 60000:
                return data['access_token']

        # Use Redis lock to prevent thundering herd
        lock_key = f'{self.cache_key}:lock'
        lock_acquired = self.redis.set(lock_key, '1', ex=10, nx=True)

        if not lock_acquired:
            time.sleep(1)
            return self.get_token()

        try:
            response = requests.post(
                'https://auth.interactor.com/api/v1/oauth/token',
                json={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                },
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            data = response.json()['data']
            expires_at = (time.time() * 1000) + (data['expires_in'] * 1000)

            token_data = {
                'access_token': data['access_token'],
                'expires_at': expires_at
            }
            self.redis.set(
                self.cache_key,
                json.dumps(token_data),
                px=data['expires_in'] * 1000
            )

            return data['access_token']
        finally:
            self.redis.delete(lock_key)

    def invalidate_token(self) -> None:
        self.redis.delete(self.cache_key)
```

### Cache Key Strategy

| Strategy | Cache Key Pattern | Use When |
|----------|------------------|----------|
| Per-client | `interactor:token:{client_id}` | Single OAuth client per service |
| Per-environment | `interactor:token:{env}:{client_id}` | Same Redis shared across environments |
| Per-namespace | `interactor:token:{client_id}:{namespace}` | Different tokens per tenant |

### Cache Invalidation Events

Invalidate the distributed cache when:
- Secret rotation occurs
- Token revocation is triggered
- Authentication errors (401) are received
- Manual cache clear is requested

```typescript
// Example: Invalidate on 401 error
async function requestWithCacheInvalidation<T>(
  client: DistributedInteractorClient,
  fn: () => Promise<T>
): Promise<T> {
  try {
    return await fn();
  } catch (error: any) {
    if (error.response?.status === 401) {
      await client.invalidateToken();
      // Retry once with fresh token
      return await fn();
    }
    throw error;
  }
}
```

---

## JWT Verification (Advanced)

For scenarios where you need to verify Interactor JWTs locally (e.g., validating tokens passed from other services), use the JWKS endpoint.

### Required Dependencies

Install the JWT verification libraries for your language:

```bash
# TypeScript/Node.js
npm install jwks-rsa jsonwebtoken
npm install -D @types/jsonwebtoken

# Python
pip install PyJWT[crypto] cryptography

# Elixir (add to mix.exs deps)
# {:jose, "~> 1.11"}
# {:httpoison, "~> 2.0"}  # or {:req, "~> 0.4"}
```

### TypeScript Implementation

```typescript
import jwksClient from 'jwks-rsa';
import jwt, { JwtHeader, SigningKeyCallback } from 'jsonwebtoken';

const client = jwksClient({
  jwksUri: 'https://auth.interactor.com/oauth/jwks',
  cache: true,
  cacheMaxAge: 600000, // 10 minutes
  rateLimit: true,
  jwksRequestsPerMinute: 10
});

function getKey(header: JwtHeader, callback: SigningKeyCallback): void {
  client.getSigningKey(header.kid, (err, key) => {
    if (err) {
      callback(err);
      return;
    }
    const signingKey = key?.getPublicKey();
    callback(null, signingKey);
  });
}

interface InteractorTokenPayload {
  sub: string;           // Account UUID
  iss: string;           // https://auth.interactor.com
  aud: string;           // Audience
  exp: number;           // Expiration timestamp
  iat: number;           // Issued at timestamp
  scope?: string;        // OAuth scopes
  organization_id?: string;
}

export async function verifyInteractorToken(token: string): Promise<InteractorTokenPayload> {
  return new Promise((resolve, reject) => {
    jwt.verify(
      token,
      getKey,
      {
        algorithms: ['RS256'],
        issuer: 'https://auth.interactor.com',
      },
      (err, decoded) => {
        if (err) {
          reject(new Error(`Token verification failed: ${err.message}`));
          return;
        }
        resolve(decoded as InteractorTokenPayload);
      }
    );
  });
}

// Usage
async function validateRequest(token: string): Promise<void> {
  try {
    const payload = await verifyInteractorToken(token);
    console.log('Token valid for account:', payload.sub);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    console.error('Invalid token:', message);
  }
}
```

### Python Implementation

```python
import jwt
from jwt import PyJWKClient
from typing import Dict, Any

JWKS_URL = 'https://auth.interactor.com/oauth/jwks'
ISSUER = 'https://auth.interactor.com'

# Create a cached JWKS client
jwks_client = PyJWKClient(JWKS_URL, cache_keys=True, lifespan=600)

def verify_interactor_token(token: str) -> Dict[str, Any]:
    """
    Verify an Interactor JWT token using JWKS.

    Returns the decoded payload if valid, raises exception otherwise.
    """
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            issuer=ISSUER,
            options={'require': ['exp', 'iss', 'sub']}
        )

        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidIssuerError:
        raise ValueError('Invalid token issuer')
    except jwt.InvalidTokenError as e:
        raise ValueError(f'Token verification failed: {str(e)}')


# Usage
def validate_request(token: str) -> None:
    try:
        payload = verify_interactor_token(token)
        print(f"Token valid for account: {payload['sub']}")
    except ValueError as e:
        print(f"Invalid token: {e}")


# Example: validate a token from request headers
# token = request.headers.get('Authorization', '').replace('Bearer ', '')
# validate_request(token)
```

### Elixir Implementation

```elixir
defmodule MyApp.Interactor.TokenVerifier do
  @moduledoc """
  Verify Interactor JWT tokens using JWKS.
  """

  use GenServer
  require Logger

  @jwks_url "https://auth.interactor.com/oauth/jwks"
  @issuer "https://auth.interactor.com"
  @cache_ttl_ms 600_000  # 10 minutes

  # Client API

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Verify an Interactor JWT token.
  Returns {:ok, claims} or {:error, reason}.
  """
  def verify(token) do
    GenServer.call(__MODULE__, {:verify, token})
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    {:ok, %{jwks: nil, jwks_fetched_at: nil}}
  end

  @impl true
  def handle_call({:verify, token}, _from, state) do
    case get_jwks(state) do
      {:ok, jwks, new_state} ->
        result = verify_token(token, jwks)
        {:reply, result, new_state}

      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end

  # Private Functions

  defp get_jwks(%{jwks: jwks, jwks_fetched_at: fetched_at} = state) do
    if jwks && fetched_at && DateTime.diff(DateTime.utc_now(), fetched_at, :millisecond) < @cache_ttl_ms do
      {:ok, jwks, state}
    else
      fetch_jwks(state)
    end
  end

  defp fetch_jwks(state) do
    case HTTPoison.get(@jwks_url) do
      {:ok, %{status_code: 200, body: body}} ->
        jwks = Jason.decode!(body)
        new_state = %{state | jwks: jwks, jwks_fetched_at: DateTime.utc_now()}
        {:ok, jwks, new_state}

      {:ok, %{status_code: status}} ->
        Logger.error("JWKS fetch failed with status #{status}")
        {:error, :jwks_fetch_failed}

      {:error, reason} ->
        Logger.error("JWKS fetch error: #{inspect(reason)}")
        {:error, :network_error}
    end
  end

  defp verify_token(token, jwks) do
    # Using JOSE library for JWT verification
    case JOSE.JWT.peek_protected(token) do
      %JOSE.JWS{fields: %{"kid" => kid}} ->
        case find_key(jwks, kid) do
          {:ok, jwk} ->
            case JOSE.JWT.verify_strict(jwk, ["RS256"], token) do
              {true, %JOSE.JWT{fields: claims}, _} ->
                validate_claims(claims)

              {false, _, _} ->
                {:error, :invalid_signature}
            end

          {:error, reason} ->
            {:error, reason}
        end

      _ ->
        {:error, :invalid_token_format}
    end
  end

  defp find_key(%{"keys" => keys}, kid) do
    case Enum.find(keys, &(&1["kid"] == kid)) do
      nil -> {:error, :key_not_found}
      key -> {:ok, JOSE.JWK.from_map(key)}
    end
  end

  defp validate_claims(%{"iss" => @issuer, "exp" => exp, "sub" => sub} = claims) do
    if exp > DateTime.to_unix(DateTime.utc_now()) do
      {:ok, claims}
    else
      {:error, :token_expired}
    end
  end

  defp validate_claims(_), do: {:error, :invalid_claims}
end
```

> **Note**: The Elixir implementation requires the `jose` hex package for JWT verification.

### JWKS Caching and Key Rotation

Interactor rotates signing keys periodically for security. Your JWKS client must handle this gracefully.

**Key Rotation Schedule**:
- Keys rotate approximately every 90 days
- Old keys remain valid for 30 days after rotation (overlapping validity)
- New keys are added to JWKS before they're used for signing

**Caching Recommendations**:

| Setting | Value | Rationale |
|---------|-------|-----------|
| Cache TTL | 10 minutes | Balance freshness vs. performance |
| Max cache entries | 10 keys | Support overlapping rotation periods |
| Retry on miss | Yes | Handle race during rotation |

**Handling Key Rotation**:

```typescript
async function verifyWithRetry(token: string): Promise<TokenPayload> {
  try {
    return await verifyInteractorToken(token);
  } catch (error: any) {
    // If key not found, the JWKS cache may be stale
    if (error.message?.includes('key not found') || error.message?.includes('no matching key')) {
      // Force JWKS refresh and retry once
      jwksClient.cache.clear();
      return await verifyInteractorToken(token);
    }
    throw error;
  }
}
```

**JWKS Response Structure**:

```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "key-2026-01",
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    },
    {
      "kty": "RSA",
      "kid": "key-2025-10",
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    }
  ]
}
```

**Best Practices**:
1. Always match by `kid` (key ID) from the JWT header
2. Never hardcode key IDs; they change with rotation
3. Implement cache refresh on signature verification failure
4. Monitor for elevated verification failures (may indicate rotation issues)

### When to Use JWT Verification

| Scenario | Use Token Exchange | Use JWT Verification |
|----------|-------------------|---------------------|
| Your backend calling Interactor APIs | ✅ | ❌ |
| Validating tokens from other services | ❌ | ✅ |
| Microservice-to-microservice auth | ❌ | ✅ |
| Webhook signature verification | ❌ | ✅ |

---

## Webhook Signature Verification

Interactor signs webhook payloads to ensure authenticity. Always verify signatures before processing webhooks.

### Webhook Headers

Interactor sends these headers with each webhook:

| Header | Description |
|--------|-------------|
| `X-Interactor-Signature` | HMAC-SHA256 signature of the payload |
| `X-Interactor-Timestamp` | Unix timestamp when webhook was sent |
| `X-Interactor-Webhook-Id` | Unique ID for idempotency |

### Signature Format

```
X-Interactor-Signature: sha256=<hex-encoded-hmac>
```

The signature is computed as:
```
HMAC-SHA256(webhook_secret, timestamp + "." + raw_body)
```

### TypeScript Verification

```typescript
import crypto from 'crypto';

interface WebhookVerificationResult {
  valid: boolean;
  error?: string;
}

export function verifyWebhookSignature(
  payload: string | Buffer,
  signature: string,
  timestamp: string,
  webhookSecret: string,
  toleranceSeconds = 300 // 5 minutes
): WebhookVerificationResult {
  // Check timestamp to prevent replay attacks
  const timestampNum = parseInt(timestamp, 10);
  const now = Math.floor(Date.now() / 1000);

  if (isNaN(timestampNum)) {
    return { valid: false, error: 'Invalid timestamp' };
  }

  if (Math.abs(now - timestampNum) > toleranceSeconds) {
    return { valid: false, error: 'Timestamp outside tolerance window' };
  }

  // Compute expected signature
  const signedPayload = `${timestamp}.${payload}`;
  const expectedSignature = crypto
    .createHmac('sha256', webhookSecret)
    .update(signedPayload)
    .digest('hex');

  // Parse received signature
  const receivedSignature = signature.replace('sha256=', '');

  // Constant-time comparison to prevent timing attacks
  const valid = crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(receivedSignature)
  );

  return { valid };
}

// Express middleware example
import { Request, Response, NextFunction } from 'express';

export function webhookMiddleware(webhookSecret: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const signature = req.headers['x-interactor-signature'] as string;
    const timestamp = req.headers['x-interactor-timestamp'] as string;

    if (!signature || !timestamp) {
      return res.status(401).json({ error: 'Missing webhook signature headers' });
    }

    const result = verifyWebhookSignature(
      req.body, // Must be raw body, not parsed JSON
      signature,
      timestamp,
      webhookSecret
    );

    if (!result.valid) {
      return res.status(401).json({ error: result.error || 'Invalid signature' });
    }

    next();
  };
}

// Usage with Express (important: use raw body parser for webhook routes)
import express from 'express';

const app = express();

// Webhook route needs raw body for signature verification
app.post(
  '/webhooks/interactor',
  express.raw({ type: 'application/json' }),
  webhookMiddleware(process.env.INTERACTOR_WEBHOOK_SECRET!),
  (req, res) => {
    const event = JSON.parse(req.body.toString());
    console.log('Received webhook:', event);
    res.status(200).send('OK');
  }
);
```

### Python Verification

```python
import hmac
import hashlib
import time
from typing import Tuple

def verify_webhook_signature(
    payload: bytes,
    signature: str,
    timestamp: str,
    webhook_secret: str,
    tolerance_seconds: int = 300
) -> Tuple[bool, str | None]:
    """
    Verify Interactor webhook signature.
    Returns (is_valid, error_message).
    """
    # Check timestamp
    try:
        timestamp_num = int(timestamp)
    except ValueError:
        return False, 'Invalid timestamp'

    now = int(time.time())
    if abs(now - timestamp_num) > tolerance_seconds:
        return False, 'Timestamp outside tolerance window'

    # Compute expected signature
    signed_payload = f'{timestamp}.{payload.decode("utf-8")}'
    expected_signature = hmac.new(
        webhook_secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Parse received signature
    received_signature = signature.replace('sha256=', '')

    # Constant-time comparison
    if hmac.compare_digest(expected_signature, received_signature):
        return True, None
    else:
        return False, 'Invalid signature'


# Flask example
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/interactor', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-Interactor-Signature', '')
    timestamp = request.headers.get('X-Interactor-Timestamp', '')
    webhook_secret = os.environ['INTERACTOR_WEBHOOK_SECRET']

    is_valid, error = verify_webhook_signature(
        request.get_data(),
        signature,
        timestamp,
        webhook_secret
    )

    if not is_valid:
        return jsonify({'error': error}), 401

    event = request.get_json()
    print(f"Received webhook: {event}")
    return 'OK', 200
```

### Webhook Secret Management

1. **Get your webhook secret** from the Interactor dashboard under Settings → Webhooks
2. **Store it securely** in environment variables (never commit to code)
3. **Rotate periodically** using the dashboard; old secrets remain valid for 24 hours

```bash
# .env
INTERACTOR_WEBHOOK_SECRET=whsec_abc123...
```

### Idempotency

Use `X-Interactor-Webhook-Id` to handle duplicate deliveries:

```typescript
const processedWebhooks = new Set<string>(); // Use Redis in production

app.post('/webhooks/interactor', webhookMiddleware(secret), (req, res) => {
  const webhookId = req.headers['x-interactor-webhook-id'] as string;

  if (processedWebhooks.has(webhookId)) {
    return res.status(200).send('Already processed');
  }

  // Process webhook...
  processedWebhooks.add(webhookId);

  res.status(200).send('OK');
});
```

---

## Managing OAuth Clients

### List OAuth Clients

```bash
curl https://auth.interactor.com/api/v1/account/oauth-clients \
  -H "Authorization: Bearer <user_access_token>"
```

**Response:**
```json
{
  "data": {
    "clients": [
      {
        "client_id": "client_abc123",
        "name": "My Production Backend",
        "created_at": "2026-01-20T12:00:00Z"
      },
      {
        "client_id": "client_def456",
        "name": "Staging Backend",
        "created_at": "2026-01-15T10:00:00Z"
      }
    ]
  }
}
```

### Update OAuth Client

Update the display name of an OAuth client:

```bash
curl -X PATCH https://auth.interactor.com/api/v1/account/oauth-clients/<client_id> \
  -H "Authorization: Bearer <user_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Backend Name"}'
```

**Response:**
```json
{
  "data": {
    "client_id": "client_abc123",
    "name": "Updated Backend Name",
    "updated_at": "2026-01-20T14:00:00Z"
  }
}
```

> **Note**: Only the `name` field can be updated. To change the secret, use the rotation endpoint. To change permissions, delete and recreate the client.

### Delete OAuth Client

```bash
curl -X DELETE https://auth.interactor.com/api/v1/account/oauth-clients/<client_id> \
  -H "Authorization: Bearer <user_access_token>"
```

**Response:** `204 No Content` on success.

> **Warning**: Deletion is immediate and irreversible. Any services using this client will immediately lose access.

---

## Secret Rotation

Rotate your client secret without service interruption:

```bash
curl -X POST https://auth.interactor.com/api/v1/account/oauth-clients/<client_id>/rotate-secret \
  -H "Authorization: Bearer <user_access_token>" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "data": {
    "client_id": "client_abc123",
    "client_secret": "secret_NEW_SECRET_HERE",
    "previous_secret_expires_at": "2026-01-21T12:00:00Z"
  }
}
```

**Both old and new secrets work for 24 hours** during rotation.

### Rotation Procedure

1. **Call rotate endpoint** - Get new secret
2. **Update configuration** - Deploy new secret to your backend
3. **Invalidate cached tokens** - Call `invalidateToken()` in your client
4. **Verify** - Confirm new secret works
5. **Wait** - Old secret expires automatically after 24 hours

### Rotation Script Example

```bash
#!/bin/bash
# rotate-interactor-secret.sh

set -e

USER_TOKEN="$1"
CLIENT_ID="${INTERACTOR_CLIENT_ID}"

if [ -z "$USER_TOKEN" ]; then
  echo "Usage: $0 <user_access_token>"
  exit 1
fi

echo "Rotating secret for client: $CLIENT_ID"

RESPONSE=$(curl -s -X POST \
  "https://auth.interactor.com/api/v1/account/oauth-clients/$CLIENT_ID/rotate-secret" \
  -H "Authorization: Bearer $USER_TOKEN")

NEW_SECRET=$(echo $RESPONSE | jq -r '.data.client_secret')
EXPIRES_AT=$(echo $RESPONSE | jq -r '.data.previous_secret_expires_at')

if [ "$NEW_SECRET" == "null" ]; then
  echo "Error: $(echo $RESPONSE | jq -r '.error.message')"
  exit 1
fi

echo ""
echo "=== NEW CREDENTIALS ==="
echo "Client ID: $CLIENT_ID"
echo "New Secret: $NEW_SECRET"
echo "Old secret expires: $EXPIRES_AT"
echo ""
echo "Update your environment variables now!"
echo "You have 24 hours before the old secret stops working."
```

---

## Token Revocation

Revoke access tokens when a user logs out, a session is compromised, or during security incidents.

### Revoke a Specific Token

```bash
curl -X POST https://auth.interactor.com/api/v1/oauth/revoke \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJSUzI1NiIs...",
    "token_type_hint": "access_token"
  }'
```

**Response:** `200 OK` on success (empty body per RFC 7009).

> **Note**: Token revocation is idempotent - revoking an already-revoked or expired token returns success.

### Revoke All Tokens for an OAuth Client

Use this during security incidents or when decommissioning a service:

```bash
curl -X POST https://auth.interactor.com/api/v1/oauth/revoke-all \
  -H "Authorization: Bearer <user_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client_abc123"
  }'
```

**Response:**
```json
{
  "data": {
    "revoked_count": 15,
    "client_id": "client_abc123"
  }
}
```

### Implementation Example

```typescript
export class InteractorClient {
  // ... existing methods ...

  /**
   * Revoke the current access token.
   * Call this when user logs out or session ends.
   */
  async revokeToken(): Promise<void> {
    if (!this.accessToken) {
      return; // No token to revoke
    }

    try {
      await axios.post(
        'https://auth.interactor.com/api/v1/oauth/revoke',
        {
          token: this.accessToken,
          token_type_hint: 'access_token'
        },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );
    } finally {
      // Always clear local token, even if revocation fails
      this.invalidateToken();
    }
  }
}

// Usage: Clean logout
async function logout(client: InteractorClient): Promise<void> {
  await client.revokeToken();
  // Clear any other session state
}
```

### When to Revoke Tokens

| Scenario | Action |
|----------|--------|
| User logout | Revoke current token |
| Password change | Revoke all tokens for user |
| Security incident | Revoke all tokens for affected client |
| OAuth client deletion | Tokens auto-revoked |
| Secret rotation | Tokens remain valid; no revocation needed |

---

## Error Handling

### Authentication Errors

| Error Code | HTTP Status | Cause | Solution |
|------------|-------------|-------|----------|
| `invalid_client` | 401 | Wrong client_id or client_secret | Verify credentials in environment |
| `unauthorized_client` | 401 | Client not authorized for grant type | Ensure client_credentials grant is enabled |
| `invalid_grant` | 401 | Credentials expired or revoked | Create new OAuth client |
| `invalid_request` | 400 | Missing required parameters | Check request body format |
| `invalid_scope` | 400 | Requested scope not allowed | Request only permitted scopes |
| `server_error` | 500 | Interactor internal error | Retry with exponential backoff |

### API Errors

| Error Code | HTTP Status | Cause | Retry? | Solution |
|------------|-------------|-------|--------|----------|
| `not_found` | 404 | Resource doesn't exist | No | Verify resource ID/path |
| `already_exists` | 409 | Duplicate resource | No | Use existing or update |
| `validation_error` | 400 | Invalid request data | No | Fix request payload |
| `permission_denied` | 403 | Insufficient scopes | No | Request additional scopes |
| `rate_limited` | 429 | Too many requests | Yes | Wait for X-RateLimit-Reset |
| `quota_exceeded` | 402 | Plan limit reached | No | Upgrade plan or reduce usage |
| `service_unavailable` | 503 | Temporary outage | Yes | Retry with backoff |
| `internal_error` | 500 | Server error | Yes | Retry with backoff |
| `bad_gateway` | 502 | Upstream error | Yes | Retry with backoff |
| `gateway_timeout` | 504 | Request timeout | Yes | Retry with backoff |

### Error Code to Action Mapping

```typescript
type RetryAction = 'retry' | 'refresh_token' | 'fail' | 'wait';

function getErrorAction(statusCode: number, errorCode?: string): RetryAction {
  // 5xx errors: retry with backoff
  if (statusCode >= 500) return 'retry';

  // Rate limit: wait then retry
  if (statusCode === 429) return 'wait';

  // Auth errors
  if (statusCode === 401) {
    if (errorCode === 'invalid_client') return 'fail'; // Credentials wrong
    return 'refresh_token'; // Token expired
  }

  // Client errors: don't retry
  if (statusCode >= 400 && statusCode < 500) return 'fail';

  return 'fail';
}
```

### Error Response Format

```json
{
  "error": {
    "code": "invalid_client",
    "message": "Client authentication failed",
    "details": {
      "reason": "Invalid client_id or client_secret"
    }
  }
}
```

### Handling Token Expiry

```typescript
async function callWithRetry<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (error: any) {
    const status = error.response?.status;

    if (status === 401) {
      // Token expired or invalid, refresh and retry once
      console.warn('Token expired, refreshing...');
      interactorClient.invalidateToken();
      return await fn();
    }

    if (status === 403) {
      // Authorization failed - don't retry, this is a permissions issue
      const message = error.response?.data?.error?.message || 'Permission denied';
      throw new Error(`Authorization failed: ${message}`);
    }

    throw error;
  }
}

// Usage
try {
  const result = await callWithRetry(() =>
    interactorClient.request('GET', '/credentials')
  );
} catch (error) {
  console.error('API call failed:', error);
}
```

---

## Rate Limits

### Limits by Endpoint

| Endpoint Category | Limit | Scope |
|-------------------|-------|-------|
| Authentication (`/oauth/token`) | 10/minute | Per OAuth client |
| Read operations | 100/minute | Per OAuth client |
| Write operations | 50/minute | Per OAuth client |
| JWKS (`/oauth/jwks`) | 100/minute | Per IP address |

### Rate Limit Scope

Rate limits are applied **per OAuth client**, not per account or namespace:

- **Per OAuth Client**: Each `client_id` has its own rate limit bucket
- **Shared Across Instances**: Multiple backend instances using the same client share the limit
- **Independent Clients**: Creating separate OAuth clients gives you independent limits

**Example**: If you have 3 backend services using 1 OAuth client:
- Total combined: 100 read requests/minute
- Solution: Create separate OAuth clients per service for independent limits

**Multi-tenant considerations**:
- Namespaces do NOT have separate rate limits
- All namespace operations count against the OAuth client's limit
- For high-volume multi-tenant apps, consider request queuing or client partitioning

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705665600
```

### Handling Rate Limits

```typescript
async function requestWithRateLimitRetry<T>(
  client: InteractorClient,
  method: string,
  path: string,
  data?: any,
  maxRetries = 3
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await client.request(method, path, data);
    } catch (error: any) {
      if (error.response?.status === 429 && attempt < maxRetries - 1) {
        const resetTime = error.response.headers['x-ratelimit-reset'];
        const waitMs = resetTime
          ? (parseInt(resetTime) * 1000 - Date.now())
          : Math.pow(2, attempt) * 1000;

        await new Promise(resolve => setTimeout(resolve, Math.max(waitMs, 1000)));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## Troubleshooting

### Common Issues and Solutions

#### "invalid_client" Error

**Symptoms**: Token exchange fails with `invalid_client` error.

**Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| Wrong `client_id` | Verify the client ID matches exactly (check for copy/paste errors) |
| Wrong `client_secret` | Re-check the secret; if lost, rotate to get a new one |
| Trailing whitespace | Trim environment variables: `INTERACTOR_CLIENT_ID=$(echo $INTERACTOR_CLIENT_ID | tr -d '[:space:]')` |
| Secret expired after rotation | You're using the old secret after the 24-hour grace period; update to new secret |

#### "invalid_client" After Secret Rotation

**Symptoms**: Authentication worked before rotation, now fails.

**Solution**:
1. Ensure you're using the NEW secret, not the old one
2. Call `invalidateToken()` in your client to clear cached tokens
3. Verify the 24-hour grace period hasn't expired
4. Check that your deployment actually picked up the new environment variables

```bash
# Verify environment variable is updated
echo "Client ID: $INTERACTOR_CLIENT_ID"
echo "Secret (first 10 chars): ${INTERACTOR_CLIENT_SECRET:0:10}..."
```

#### Token Works Locally, Fails in Production

**Symptoms**: Authentication works in development but fails in staging/production.

**Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| Environment variables not set | Verify with `printenv | grep INTERACTOR` |
| Using wrong OAuth client | Create separate clients per environment |
| Network/firewall issues | Ensure outbound HTTPS to `*.interactor.com` is allowed |
| Clock skew | JWT validation fails if server clock is >5 minutes off; sync with NTP |

```bash
# Check if you can reach Interactor services from production
curl -s https://auth.interactor.com/health | jq .   # Auth server
curl -s https://core.interactor.com/health | jq .   # Core API
```

#### Token Expires Too Quickly

**Symptoms**: Frequent 401 errors, tokens seem to expire before 15 minutes.

**Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| Not caching tokens | Implement token caching (see Token Management section) |
| Cache not working | Verify your caching mechanism is functioning |
| Clock skew | Server time ahead of Interactor's; sync with NTP |
| Buffer too large | Reduce the 60-second buffer if needed (but keep some buffer) |

#### Rate Limit Errors (429)

**Symptoms**: Requests fail with HTTP 429 Too Many Requests.

**Solutions**:
1. Implement token caching to reduce `/oauth/token` calls
2. Add exponential backoff retry logic (see Rate Limits section)
3. Review your architecture - are you creating too many clients?
4. Contact Interactor support if legitimate use exceeds limits

```bash
# Check rate limit headers in response (use -v for verbose output)
curl -v -X POST https://auth.interactor.com/api/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"...","client_secret":"..."}' \
  2>&1 | grep -i "x-ratelimit"

# Look for:
# < X-RateLimit-Limit: 10
# < X-RateLimit-Remaining: 0
# < X-RateLimit-Reset: 1737417600
```

#### JWKS Verification Fails

**Symptoms**: Local JWT verification fails even with valid tokens.

**Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| JWKS endpoint unreachable | Check network access to `https://auth.interactor.com/oauth/jwks` |
| Key rotation | Keys rotate periodically; ensure your JWKS client caches with TTL |
| Wrong algorithm | Interactor uses RS256; ensure your verifier allows it |
| Missing `kid` | Token must have a `kid` header matching a JWKS key |

### Debug Mode

Enable detailed logging to troubleshoot issues:

```typescript
// TypeScript - Enable axios request logging
import axios from 'axios';

axios.interceptors.request.use(request => {
  console.log('Starting Request:', {
    url: request.url,
    method: request.method,
    headers: { ...request.headers, Authorization: '[REDACTED]' }
  });
  return request;
});

axios.interceptors.response.use(
  response => {
    console.log('Response:', {
      status: response.status,
      headers: response.headers
    });
    return response;
  },
  error => {
    console.error('Request Failed:', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers
    });
    return Promise.reject(error);
  }
);
```

```python
# Python - Enable requests logging
import logging
import http.client

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
```

```elixir
# Elixir - Add logging to client (modify refresh_token in MyApp.Interactor.Client)
defp refresh_token(%{client_id: client_id, client_secret: client_secret} = state) do
  Logger.debug("Refreshing Interactor token for client: #{client_id}")

  body = Jason.encode!(%{
    grant_type: "client_credentials",
    client_id: client_id,
    client_secret: client_secret
  })

  case HTTPoison.post("#{@auth_url}/oauth/token", body, [{"Content-Type", "application/json"}]) do
    {:ok, %{status_code: 200, body: response_body}} ->
      %{"data" => %{"access_token" => token, "expires_in" => expires_in}} = Jason.decode!(response_body)
      Logger.info("Token refreshed successfully, expires in #{expires_in}s")

      expiry = DateTime.utc_now() |> DateTime.add(expires_in - @token_buffer_seconds, :second)
      {:ok, token, %{state | access_token: token, token_expiry: expiry}}

    {:ok, %{status_code: status, body: response_body}} ->
      Logger.error("Token exchange failed with status #{status}: #{response_body}")
      {:error, :token_exchange_failed}

    {:error, reason} ->
      Logger.error("Token exchange network error: #{inspect(reason)}")
      {:error, :network_error}
  end
end
```

### Getting Help

If issues persist after troubleshooting:

1. **Check service status**: https://status.interactor.com
2. **Review API documentation**: https://docs.interactor.com
3. **Contact support**: Include your `client_id` (never the secret), error messages, and request IDs

---

## SRE Incident Runbook

Quick reference for on-call engineers handling Interactor-related incidents.

### Incident: Authentication Failures (High 401 Rate)

**Severity**: P1 if affecting >10% of requests

**Symptoms**:
- Spike in `interactor.token.refresh.errors`
- Increased 401 responses from Interactor
- Users unable to access Interactor-dependent features

**Diagnostic Steps**:

```bash
# 1. Check Interactor service status
curl -s https://status.interactor.com/api/v2/status.json | jq '.status.indicator'

# 2. Verify credentials are valid (from a known-good environment)
curl -s -X POST https://auth.interactor.com/api/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"'$INTERACTOR_CLIENT_ID'","client_secret":"'$INTERACTOR_CLIENT_SECRET'"}' \
  | jq '.error // "OK"'

# 3. Check if secret was recently rotated
# Review deployment logs and secret manager audit logs

# 4. Verify environment variables in running pods/containers
kubectl exec -it <pod> -- printenv | grep INTERACTOR
```

**Remediation**:

| Root Cause | Action |
|------------|--------|
| Interactor outage | Wait for resolution, enable degraded mode |
| Secret rotation not deployed | Deploy latest secrets |
| Credentials revoked | Create new OAuth client |
| Clock skew | Sync NTP on affected servers |

### Incident: Rate Limit Exhaustion (429 Errors)

**Severity**: P2

**Symptoms**:
- 429 responses from Interactor
- `X-RateLimit-Remaining: 0` headers
- Features degraded or unavailable

**Diagnostic Steps**:

```bash
# 1. Check current rate limit status
curl -v -s https://auth.interactor.com/api/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"...","client_secret":"..."}' \
  2>&1 | grep -i "x-ratelimit"

# 2. Review request patterns
# Check logs for unusual request volume
# grep 'interactor' /var/log/app.log | wc -l

# 3. Check if token caching is working
# Look for repeated token refresh calls
```

**Remediation**:

| Root Cause | Action |
|------------|--------|
| Token caching disabled | Enable/fix token caching |
| Thundering herd | Implement distributed locking |
| Legitimate high volume | Request limit increase from Interactor |
| Loop/bug causing retries | Fix application bug |

### Incident: High Latency

**Severity**: P2 if p99 > 5s

**Symptoms**:
- Increased `interactor.api.request.latency`
- Timeouts in downstream services
- User-visible slowness

**Diagnostic Steps**:

```bash
# 1. Check Interactor status for performance issues
curl -s https://status.interactor.com/api/v2/summary.json | jq '.components[] | select(.name | contains("API"))'

# 2. Test latency from your infrastructure
time curl -s https://core.interactor.com/health

# 3. Check network path
traceroute core.interactor.com
mtr -c 10 core.interactor.com
```

**Remediation**:

| Root Cause | Action |
|------------|--------|
| Interactor performance issue | Wait, implement caching |
| Network latency | Review routing, consider regional deployment |
| Large response payloads | Implement pagination, reduce scope |

### Incident: Secret Compromise

**Severity**: P0 (Security)

**Immediate Actions**:

```bash
# 1. Rotate secret immediately
curl -X POST https://auth.interactor.com/api/v1/account/oauth-clients/<client_id>/rotate-secret \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json"

# 2. Deploy new secret to all environments
# Update secrets manager
# Trigger deployment

# 3. Invalidate all existing tokens
# Restart all services using the client

# 4. Review audit logs for unauthorized access
# Check Interactor dashboard for suspicious activity
```

**Post-Incident**:
1. Determine how secret was compromised
2. Review secret storage and access controls
3. Update rotation schedule if needed
4. Document in incident report

### Escalation Contacts

| Level | Contact | When |
|-------|---------|------|
| L1 | On-call engineer | Initial response |
| L2 | Platform team lead | P1 incidents, >30min resolution |
| L3 | Interactor support | Confirmed Interactor-side issue |

---

## Observability & Telemetry

Implement monitoring to track Interactor integration health and performance.

### Key Metrics to Track

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `interactor.token.refresh.count` | Counter | Token refresh operations | N/A (baseline) |
| `interactor.token.refresh.latency` | Histogram | Token exchange latency | p99 > 2s |
| `interactor.token.refresh.errors` | Counter | Failed token exchanges | > 3/minute |
| `interactor.api.request.count` | Counter | API requests by endpoint | N/A (baseline) |
| `interactor.api.request.latency` | Histogram | API request latency | p99 > 5s |
| `interactor.api.request.errors` | Counter | API errors by status code | 5xx > 1/minute |
| `interactor.rate_limit.remaining` | Gauge | Remaining rate limit | < 10 |
| `interactor.cache.hit_rate` | Gauge | Token cache hit percentage | < 90% |

### OpenTelemetry Integration (TypeScript)

```typescript
import { trace, metrics, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('interactor-client');
const meter = metrics.getMeter('interactor-client');

// Metrics
const tokenRefreshCounter = meter.createCounter('interactor.token.refresh.count');
const tokenRefreshLatency = meter.createHistogram('interactor.token.refresh.latency');
const apiRequestCounter = meter.createCounter('interactor.api.request.count');
const apiRequestLatency = meter.createHistogram('interactor.api.request.latency');
const apiErrorCounter = meter.createCounter('interactor.api.request.errors');

export class ObservableInteractorClient extends InteractorClient {
  async getToken(): Promise<string> {
    return tracer.startActiveSpan('interactor.token.refresh', async (span) => {
      const start = Date.now();
      try {
        const token = await super.getToken();
        tokenRefreshCounter.add(1, { status: 'success' });
        span.setStatus({ code: SpanStatusCode.OK });
        return token;
      } catch (error) {
        tokenRefreshCounter.add(1, { status: 'error' });
        apiErrorCounter.add(1, { operation: 'token_refresh' });
        span.setStatus({ code: SpanStatusCode.ERROR, message: String(error) });
        throw error;
      } finally {
        tokenRefreshLatency.record(Date.now() - start);
        span.end();
      }
    });
  }

  async request<T>(method: string, path: string, data?: any): Promise<T> {
    return tracer.startActiveSpan('interactor.api.request', async (span) => {
      span.setAttribute('http.method', method);
      span.setAttribute('http.path', path);

      const start = Date.now();
      try {
        const result = await super.request<T>(method, path, data);
        apiRequestCounter.add(1, { method, path, status: 'success' });
        span.setStatus({ code: SpanStatusCode.OK });
        return result;
      } catch (error: any) {
        const statusCode = error.response?.status || 'unknown';
        apiRequestCounter.add(1, { method, path, status: 'error' });
        apiErrorCounter.add(1, { method, path, status_code: statusCode });
        span.setAttribute('http.status_code', statusCode);
        span.setStatus({ code: SpanStatusCode.ERROR, message: String(error) });
        throw error;
      } finally {
        apiRequestLatency.record(Date.now() - start, { method, path });
        span.end();
      }
    });
  }
}
```

### Structured Logging

Include these fields in all Interactor-related logs:

```typescript
interface InteractorLogContext {
  client_id: string;          // OAuth client identifier
  request_id?: string;        // From X-Request-Id header
  operation: string;          // token_refresh, api_call, etc.
  endpoint?: string;          // API path
  latency_ms?: number;        // Request duration
  status_code?: number;       // HTTP status
  rate_limit_remaining?: number;
  error_code?: string;        // Interactor error code
}

// Example log output (JSON)
{
  "timestamp": "2026-01-20T12:00:00.000Z",
  "level": "info",
  "message": "Interactor API request completed",
  "client_id": "client_abc123",
  "request_id": "req_xyz789",
  "operation": "api_call",
  "endpoint": "/credentials",
  "latency_ms": 145,
  "status_code": 200,
  "rate_limit_remaining": 95
}
```

### Dashboard Recommendations

Create dashboards with these panels:

1. **Authentication Health**
   - Token refresh success/failure rate
   - Token refresh latency (p50, p95, p99)
   - Cache hit rate

2. **API Health**
   - Request rate by endpoint
   - Error rate by status code
   - Latency by endpoint

3. **Rate Limits**
   - Current usage vs. limits
   - Rate limit exhaustion events

4. **Alerts**
   - Token refresh failures > 3/min
   - API error rate > 5%
   - Rate limit remaining < 10%
   - p99 latency > 5s

---

## Health Check

Verify Interactor service availability (no authentication required):

```bash
# Check Core API (main platform)
curl https://core.interactor.com/health

# Check Auth Server (authentication)
curl https://auth.interactor.com/health
```

**Response (both endpoints):**
```json
{
  "status": "ok",
  "timestamp": "2026-01-20T12:00:00Z"
}
```

> **Tip**: Monitor both endpoints in production. Auth server issues prevent new token acquisition; Core API issues affect all platform operations.

---

## Security Best Practices

### Network Security & Egress

Configure your firewall/security groups to allow outbound connections to Interactor:

**Required Egress Rules:**

| Destination | Port | Protocol | Purpose |
|-------------|------|----------|---------|
| `auth.interactor.com` | 443 | HTTPS | OAuth token exchange, JWKS |
| `core.interactor.com` | 443 | HTTPS | Platform API calls |
| `*.interactor.com` | 443 | HTTPS | Future-proof wildcard (optional) |

**IP Allowlisting:**

If your security policy requires IP allowlisting (not recommended due to potential IP changes):

```bash
# Get current IP addresses (these may change)
dig +short auth.interactor.com
dig +short core.interactor.com
```

> **Warning**: Interactor IPs may change without notice. Use DNS-based rules where possible. Subscribe to status.interactor.com for infrastructure change notifications.

**TLS Requirements:**
- Minimum TLS version: 1.2
- Recommended: TLS 1.3
- Certificate validation: Always enabled (never disable in production)

**Proxy Configuration:**

If your backend requires an HTTP proxy for egress:

```typescript
import { HttpsProxyAgent } from 'https-proxy-agent';
import axios from 'axios';

const proxyAgent = new HttpsProxyAgent(process.env.HTTPS_PROXY!);

const client = axios.create({
  httpsAgent: proxyAgent,
  proxy: false // Use agent instead of axios proxy
});
```

### DO

- **Store secrets in environment variables** - Never hardcode credentials
- **Use separate clients per environment** - Create different OAuth clients for dev/staging/production
- **Rotate secrets regularly** - Use the rotation endpoint quarterly
- **Monitor OAuth client usage** - Review access logs for unauthorized access
- **Cache tokens appropriately** - Reduce authentication requests
- **Use HTTPS only** - All Interactor endpoints require TLS

### DON'T

- **Never expose client_secret in frontend code** - Only use credentials in your backend
- **Never commit credentials to version control** - Use `.env` files excluded from git
- **Never share credentials between services** - Each service should have its own OAuth client
- **Never ignore token expiry** - Always implement proper refresh logic

### Environment File Template

```bash
# .env.example - Commit this template
INTERACTOR_CLIENT_ID=your_client_id_here
INTERACTOR_CLIENT_SECRET=your_client_secret_here

# .gitignore - Ensure .env is excluded
.env
.env.local
.env.*.local
```

### Secret Storage Patterns

For production deployments, use a dedicated secrets manager instead of environment files:

#### AWS Secrets Manager

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getInteractorCredentials(): Promise<{ clientId: string; clientSecret: string }> {
  const command = new GetSecretValueCommand({ SecretId: 'interactor/production' });
  const response = await client.send(command);
  const secret = JSON.parse(response.SecretString!);
  return {
    clientId: secret.INTERACTOR_CLIENT_ID,
    clientSecret: secret.INTERACTOR_CLIENT_SECRET
  };
}
```

#### HashiCorp Vault

```typescript
import Vault from 'node-vault';

const vault = Vault({ endpoint: process.env.VAULT_ADDR, token: process.env.VAULT_TOKEN });

async function getInteractorCredentials(): Promise<{ clientId: string; clientSecret: string }> {
  const { data } = await vault.read('secret/data/interactor/production');
  return {
    clientId: data.data.client_id,
    clientSecret: data.data.client_secret
  };
}
```

#### Google Cloud Secret Manager

```typescript
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

const client = new SecretManagerServiceClient();

async function getInteractorCredentials(): Promise<{ clientId: string; clientSecret: string }> {
  const projectId = process.env.GCP_PROJECT_ID;

  const [clientIdVersion] = await client.accessSecretVersion({
    name: `projects/${projectId}/secrets/interactor-client-id/versions/latest`
  });
  const [clientSecretVersion] = await client.accessSecretVersion({
    name: `projects/${projectId}/secrets/interactor-client-secret/versions/latest`
  });

  return {
    clientId: clientIdVersion.payload!.data!.toString(),
    clientSecret: clientSecretVersion.payload!.data!.toString()
  };
}
```

#### Kubernetes Secrets

```yaml
# interactor-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: interactor-credentials
type: Opaque
stringData:
  INTERACTOR_CLIENT_ID: client_abc123
  INTERACTOR_CLIENT_SECRET: secret_xyz789
---
# deployment.yaml
spec:
  containers:
    - name: app
      envFrom:
        - secretRef:
            name: interactor-credentials
```

| Platform | Best For | Rotation Support |
|----------|----------|------------------|
| AWS Secrets Manager | AWS-native apps | Automatic rotation with Lambda |
| HashiCorp Vault | Multi-cloud, on-prem | Dynamic secrets, leases |
| GCP Secret Manager | GCP-native apps | Version-based rotation |
| Kubernetes Secrets | K8s workloads | External Secrets Operator |
| Azure Key Vault | Azure-native apps | Automatic rotation policies |

---

## Integration Verification

### Verify Setup

Run this script to verify your Interactor authentication is working:

```bash
#!/bin/bash
# verify-interactor-auth.sh

set -e

# Check dependencies
command -v curl >/dev/null 2>&1 || { echo "Error: curl is required but not installed."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "Error: jq is required but not installed. Install with: brew install jq (macOS) or apt install jq (Linux)"; exit 1; }

CLIENT_ID="${INTERACTOR_CLIENT_ID}"
CLIENT_SECRET="${INTERACTOR_CLIENT_SECRET}"

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
  echo "Error: INTERACTOR_CLIENT_ID and INTERACTOR_CLIENT_SECRET must be set"
  echo "  export INTERACTOR_CLIENT_ID=your_client_id"
  echo "  export INTERACTOR_CLIENT_SECRET=your_client_secret"
  exit 1
fi

echo "1. Testing health endpoint..."
curl -s https://core.interactor.com/health | jq . || { echo "Error: Cannot reach health endpoint"; exit 1; }

echo ""
echo "2. Exchanging credentials for token..."
TOKEN_RESPONSE=$(curl -s -X POST https://auth.interactor.com/api/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d "{
    \"grant_type\": \"client_credentials\",
    \"client_id\": \"$CLIENT_ID\",
    \"client_secret\": \"$CLIENT_SECRET\"
  }")

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.data.access_token')

if [ "$ACCESS_TOKEN" == "null" ]; then
  echo "Error: $(echo $TOKEN_RESPONSE | jq -r '.error.message')"
  exit 1
fi

echo "Token received: ${ACCESS_TOKEN:0:20}..."

echo ""
echo "3. Testing API access..."
curl -s https://core.interactor.com/api/v1/credentials/summary \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo ""
echo "=== Authentication setup verified successfully! ==="
```

---

## Output Format

When setting up Interactor authentication, provide this summary:

```markdown
## Interactor Authentication Setup Report

**Date**: YYYY-MM-DD
**Environment**: [Development | Staging | Production]

### Credentials Created
| Item | Value |
|------|-------|
| Client ID | `client_xxx` (stored in INTERACTOR_CLIENT_ID) |
| Client Secret | `***` (stored in INTERACTOR_CLIENT_SECRET) |
| OAuth Client Name | [Name] |

### Verification Results
| Check | Status |
|-------|--------|
| Health endpoint | ✓ PASS |
| Token exchange | ✓ PASS |
| API access | ✓ PASS |

### Implementation Status
- [ ] Environment variables configured
- [ ] Token management implemented (caching + refresh)
- [ ] Error handling implemented
- [ ] Rate limit handling implemented
- [ ] Health check monitoring configured

### Next Steps
1. Implement credential management (see `interactor-credentials` skill)
2. Set up AI agents (see `interactor-agents` skill)
3. Configure workflows (see `interactor-workflows` skill)
4. Set up webhooks (see `interactor-webhooks` skill)
```

---

## Frequently Asked Questions

### General

**Q: Can I use the same OAuth client for multiple environments (dev/staging/prod)?**

A: You can, but you shouldn't. Create separate OAuth clients per environment for:
- Independent rate limits
- Environment-specific secret rotation
- Better audit trails
- Isolated blast radius if credentials are compromised

**Q: How do I test Interactor integration locally?**

A: Options in order of preference:
1. Use a dedicated "development" OAuth client with limited scopes
2. Use the Interactor dashboard for quick API exploration
3. Mock the Interactor API using tools like WireMock or MSW

**Q: Do access tokens work across all Interactor services?**

A: Yes. A token obtained from auth.interactor.com works for both auth.interactor.com and core.interactor.com APIs.

### Token Management

**Q: Why does my token expire before 15 minutes?**

A: Common causes:
- Clock skew between your server and Interactor (sync NTP)
- Not accounting for network latency when checking expiry
- The 60-second buffer in your code might be too aggressive

**Q: Should I refresh tokens proactively or on-demand?**

A: Proactive refresh (60 seconds before expiry) is recommended because:
- Avoids request latency from synchronous token refresh
- Reduces risk of race conditions in high-throughput systems
- Better user experience (no unexpected delays)

**Q: How do I handle token refresh in serverless functions?**

A: For AWS Lambda, Vercel, or similar:
1. Store tokens in a shared cache (Redis, DynamoDB)
2. Check cache at start of each invocation
3. Refresh if expired or missing
4. Use distributed locking to prevent thundering herd

### Secret Management

**Q: What happens if I lose my client_secret?**

A: You cannot retrieve it. You must:
1. Rotate the secret using the rotation endpoint (if you still have the old one)
2. Or delete and recreate the OAuth client (if old secret is completely lost)

**Q: How often should I rotate secrets?**

A: Recommendations:
- **Minimum**: Quarterly (every 90 days)
- **Better**: Monthly
- **After incidents**: Immediately if compromise suspected

**Q: Can I have multiple active secrets during rotation?**

A: Yes, both old and new secrets work for 24 hours after rotation. This allows zero-downtime deployments.

### Multi-Tenancy

**Q: How do namespaces relate to OAuth clients?**

A: OAuth clients and namespaces are independent:
- **OAuth client**: Identifies YOUR backend to Interactor
- **Namespace**: Identifies which end-user's data to access

One OAuth client can access any namespace. Namespaces don't provide separate rate limits.

**Q: Should I create one OAuth client per tenant?**

A: Generally no. Use namespaces within a single OAuth client. Create separate clients only if you need:
- Independent rate limits per tenant
- Different permission scopes per tenant
- Separate audit trails

### Security

**Q: Is it safe to include client_id in logs?**

A: Yes, client_id is not sensitive. Never log client_secret.

**Q: Can I restrict which IPs can use my OAuth client?**

A: Not currently. Use secret rotation and monitoring instead. Contact Interactor support if you have specific compliance requirements.

**Q: What happens if someone gets my client_secret?**

A: They can make API calls as your organization. Immediately:
1. Rotate the secret
2. Review audit logs for unauthorized access
3. Revoke any suspicious tokens

---

## Related Skills

- **interactor-credentials**: Manage OAuth tokens for external services (Google, Slack, etc.)
- **interactor-agents**: Create AI assistants with tools and data sources
- **interactor-workflows**: Build state-machine based automation
- **interactor-webhooks**: Set up event notifications and streaming
- **interactor-sdk**: Complete SDK implementation examples
