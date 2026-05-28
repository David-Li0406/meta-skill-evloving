---
name: interactor-credentials
description: Implement OAuth flows and manage credentials for external services (Google, Slack, Salesforce, etc.) through Interactor. Use when connecting users to third-party services, handling OAuth authorization, retrieving access tokens, or monitoring credential status.
author: Interactor Integration Guide
---

# Interactor Credential Management Skill

Securely store and manage OAuth tokens and API keys for external services through the Interactor platform.

## When to Use

- **Connecting External Services**: When users need to connect Google, Slack, Salesforce, or other OAuth services
- **OAuth Flow Implementation**: Initiating and completing OAuth authorization flows
- **Token Retrieval**: Getting access tokens to call external APIs on behalf of users
- **Token Refresh**: Handling automatic or manual token refresh
- **Credential Monitoring**: Tracking credential status and handling revocations
- **Custom OAuth Apps**: Configuring your own OAuth app credentials for better branding
- **API Key Storage**: Securely storing API keys for services that don't support OAuth (see [API Key Credentials](#api-key-credentials-non-oauth))

## When NOT to Use

- **Internal service authentication**: This skill is for external third-party services (Google, Slack, etc.), not Interactor-to-Interactor authentication
- **One-time API calls**: If you don't need persistent access, consider direct OAuth without credential storage
- **Client-side usage**: All Interactor API calls must be made from your backend (see [Backend-Only Execution Model](#backend-only-execution-model))

## Prerequisites

- Interactor authentication configured (see `interactor-auth` skill)
- Understanding of OAuth 2.0 flows
- Namespace strategy for multi-tenant isolation

## Overview

Interactor handles credential complexity for both OAuth tokens and API keys:

| Feature | Description |
|---------|-------------|
| **Token Storage** | Encrypted storage of access tokens, refresh tokens, and API keys |
| **Automatic Refresh** | OAuth tokens are refreshed before expiry |
| **Multi-tenant Isolation** | Namespaces separate different users' credentials |
| **Revocation Handling** | Detects when users revoke OAuth access |
| **Unified Interface** | Same API for OAuth and API key credentials |

---

## Architecture Concepts

### Backend-Only Execution Model

> **Critical**: All Interactor API calls must be made from your backend server.

Interactor does **not** authenticate your end users directly. Your application:

1. Authenticates users through your own auth system
2. Makes Interactor API calls on behalf of authenticated users
3. Never exposes Interactor tokens or credential IDs to the client

**Never expose to client-side code:**
- Interactor access tokens (your JWT)
- Credential IDs (`cred_abc`)
- External service access tokens (e.g., Google OAuth tokens)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Browser/App   │     │   Your Backend  │     │   Interactor    │
│   (Frontend)    │     │   (Server)      │     │   API           │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │ User action           │                       │
         │──────────────────────>│                       │
         │                       │                       │
         │                       │ API call with JWT     │
         │                       │──────────────────────>│
         │                       │                       │
         │                       │ Credential/token      │
         │                       │<──────────────────────│
         │                       │                       │
         │ Response (no tokens)  │                       │
         │<──────────────────────│                       │
```

### Namespace Patterns

Namespaces provide multi-tenant isolation for credentials. Interactor supports several strategies:

| Pattern | Namespace Value | Use Case |
|---------|-----------------|----------|
| **Per-user** | `user_123` | Each user has their own credentials |
| **Per-organization** | `org_456` | Shared credentials within an organization |
| **Shared/Global** | `shared` or `default` | Company-wide credentials (e.g., shared Slack bot) |
| **Account-level** | *(omit parameter)* | Credentials accessible to all API calls |

**Namespace behavior:**

```javascript
// Per-user credential (isolated)
{ namespace: "user_123", service_id: "google_calendar" }

// Shared credential (accessible by multiple users)
{ namespace: "shared", service_id: "slack" }

// Account-level credential (omit namespace)
{ service_id: "salesforce" }  // Accessible to all API calls
```

**Important**: If `namespace` is omitted, credentials are created at the **account level** and are accessible to all API calls using that account's authentication.

**Hybrid patterns:**
- Shared read-only credentials + user-specific write credentials
- Organization-level defaults + user overrides
- Environment-based namespaces (`prod_user_123`, `staging_user_123`)

### Credential Access Control

> **Note**: Fine-grained access control (role-based permissions, credential-to-workflow binding) is managed at the account level through Interactor's admin interface. The API does not currently expose permission management endpoints.

Credentials within a namespace are accessible to any authenticated request that includes that namespace. For granular control:
- Use separate namespaces for different access levels
- Implement access control in your application layer
- Use Interactor's admin interface for account-level restrictions

---

## Instructions

### Step 1: List All Credentials

Get all credentials in your account:

```bash
curl https://core.interactor.com/api/v1/credentials \
  -H "Authorization: Bearer <token>"
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | string | Filter by namespace (e.g., `user_123`) |
| `service_id` | string | Filter by service (e.g., `google_calendar`) |
| `status` | string | Filter by status: `active`, `expired`, `revoked` |

**Example - List credentials for a specific user:**

```bash
curl "https://core.interactor.com/api/v1/credentials?namespace=user_123" \
  -H "Authorization: Bearer <token>"
```

**Response** *(structure inferred from credential object pattern)*:
```json
{
  "data": {
    "credentials": [
      {
        "id": "cred_abc",
        "service_id": "google_calendar",
        "service_name": "Google Calendar",
        "namespace": "user_123",
        "status": "active",
        "scopes": ["calendar.readonly", "calendar.events"],
        "created_at": "2026-01-15T10:00:00Z",
        "expires_at": "2026-02-01T00:00:00Z"
      }
    ]
  }
}
```

### Step 2: Get Credentials Summary

Get a high-level summary grouped by namespace:

```bash
curl https://core.interactor.com/api/v1/credentials/summary \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "namespaces": {
      "user_123": [
        {
          "id": "cred_abc",
          "service_id": "google_calendar",
          "service_name": "Google Calendar",
          "status": "active",
          "scopes": ["calendar.readonly", "calendar.events"],
          "expires_at": "2026-02-01T00:00:00Z"
        }
      ],
      "user_456": [
        {
          "id": "cred_def",
          "service_id": "slack",
          "service_name": "Slack",
          "status": "active",
          "scopes": ["channels:read", "chat:write"]
        }
      ]
    },
    "total_count": 2
  }
}
```

### Step 3: Get a Specific Credential

```bash
curl https://core.interactor.com/api/v1/credentials/cred_abc \
  -H "Authorization: Bearer <token>"
```

**Response** *(structure inferred from credential object pattern)*:
```json
{
  "data": {
    "id": "cred_abc",
    "service_id": "google_calendar",
    "service_name": "Google Calendar",
    "namespace": "user_123",
    "status": "active",
    "scopes": ["calendar.readonly", "calendar.events"],
    "metadata": {
      "email": "user@gmail.com"
    },
    "created_at": "2026-01-15T10:00:00Z",
    "last_refreshed_at": "2026-01-20T11:00:00Z",
    "expires_at": "2026-02-01T00:00:00Z"
  }
}
```

### Step 4: Get Access Token for External API

Retrieve the current access token. Automatically refreshes if expired.

```bash
curl https://core.interactor.com/api/v1/credentials/cred_abc/token \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "access_token": "ya29.a0AfH6SM...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

Use this token to call the external service's API directly:

```bash
# Example: Call Google Calendar API
curl "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer ya29.a0AfH6SM..."
```

### Step 5: Force Token Refresh

Manually trigger a token refresh:

```bash
curl -X POST https://core.interactor.com/api/v1/credentials/cred_abc/refresh \
  -H "Authorization: Bearer <token>"
```

**Response** *(structure inferred)*:
```json
{
  "data": {
    "id": "cred_abc",
    "status": "active",
    "last_refreshed_at": "2026-01-20T12:00:00Z"
  }
}
```

### Step 6: Delete a Credential

Delete a credential (revokes OAuth tokens if applicable):

```bash
curl -X DELETE https://core.interactor.com/api/v1/credentials/cred_abc \
  -H "Authorization: Bearer <token>"
```

**Response**: `204 No Content` on success.

---

## OAuth Flow Implementation

### Initiate OAuth Authorization

Start an OAuth flow to connect an external service:

```bash
curl -X POST https://core.interactor.com/api/v1/oauth/initiate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "google_calendar",
    "namespace": "user_123",
    "scopes": ["calendar.readonly", "calendar.events"],
    "redirect_uri": "https://yourapp.com/oauth/callback"
  }'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `service_id` | string | Yes | Service identifier (e.g., `google_calendar`, `slack`) |
| `namespace` | string | Yes | User namespace for data isolation (or omit for account-level) |
| `scopes` | array | No | OAuth scopes to request (defaults to service's default scopes) |
| `redirect_uri` | string | Yes | Where to redirect after authorization |

**Scope Validation & Mapping:**

Interactor validates and maps scopes at different stages:

| Stage | Validation |
|-------|------------|
| `/oauth/initiate` | Basic validation against service's known scopes |
| Authorization | Provider validates scopes; user may grant subset |
| Token exchange | Final granted scopes stored with credential |

Interactor uses **simplified scope identifiers** that map to provider-specific OAuth URLs:

```
calendar.readonly  →  https://www.googleapis.com/auth/calendar.readonly
channels:read      →  https://api.slack.com/scopes/channels:read
```

If you request scopes not in the service catalog, you'll receive an `invalid_scopes` error at initiation time. If the user denies specific scopes during authorization, the credential will be created with only the granted scopes.

**Response:**
```json
{
  "data": {
    "flow_id": "flow_xyz",
    "authorization_url": "https://accounts.google.com/o/oauth2/auth?client_id=...&redirect_uri=...&scope=...",
    "expires_at": "2026-01-20T12:15:00Z"
  }
}
```

### Integration Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your App      │     │   Interactor    │     │ External Service│
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │ POST /oauth/initiate  │                       │
         │──────────────────────>│                       │
         │                       │                       │
         │ { authorization_url } │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │ Redirect user ────────────────────────────────>
         │                       │                       │
         │                       │  User authorizes      │
         │                       │<──────────────────────│
         │                       │                       │
         │                       │  Callback with code   │
         │                       │<──────────────────────│
         │                       │                       │
         │                       │  Exchange for tokens  │
         │                       │──────────────────────>│
         │                       │                       │
         │ Redirect to your app  │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │ GET /oauth/status     │                       │
         │──────────────────────>│                       │
         │                       │                       │
         │ { credential_id }     │                       │
         │<──────────────────────│                       │
```

### Check OAuth Flow Status

Poll or check after redirect:

```bash
curl https://core.interactor.com/api/v1/oauth/status/flow_xyz \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "flow_id": "flow_xyz",
    "status": "completed",
    "credential_id": "cred_abc"
  }
}
```

**Status Values:**

| Status | Description |
|--------|-------------|
| `pending` | User hasn't completed authorization yet |
| `completed` | Authorization successful, credential created |
| `failed` | Authorization failed (user denied or error) |
| `expired` | Flow expired (15 minutes timeout) |

---

## Complete OAuth Flow Implementation

> **Note**: The implementations below use an `InteractorClient` class for HTTP requests.
> Configure this client per the `interactor-auth` skill, which handles JWT authentication
> and request signing for Interactor API calls.

### TypeScript Implementation

```typescript
import { InteractorClient } from './interactor-client';

export class CredentialManager {
  private client: InteractorClient;

  constructor(client: InteractorClient) {
    this.client = client;
  }

  /**
   * Start OAuth flow for a user to connect an external service.
   */
  async initiateOAuth(
    userId: string,
    serviceId: string,
    redirectUri: string,
    scopes?: string[]
  ): Promise<{ flowId: string; authorizationUrl: string }> {
    const result = await this.client.request<{
      flow_id: string;
      authorization_url: string;
    }>('POST', '/oauth/initiate', {
      service_id: serviceId,
      namespace: `user_${userId}`,
      redirect_uri: redirectUri,
      scopes
    });

    return {
      flowId: result.flow_id,
      authorizationUrl: result.authorization_url
    };
  }

  /**
   * Check OAuth flow status and get credential ID if completed.
   */
  async checkOAuthStatus(flowId: string): Promise<{
    status: 'pending' | 'completed' | 'failed' | 'expired';
    credentialId?: string;
    error?: string;
  }> {
    const result = await this.client.request<{
      status: string;
      credential_id?: string;
      error?: string;
    }>('GET', `/oauth/status/${flowId}`);

    return {
      status: result.status as any,
      credentialId: result.credential_id,
      error: result.error
    };
  }

  /**
   * Wait for OAuth flow to complete with polling.
   */
  async waitForOAuthCompletion(
    flowId: string,
    timeoutMs: number = 300000, // 5 minutes
    pollIntervalMs: number = 2000
  ): Promise<string> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      const status = await this.checkOAuthStatus(flowId);

      if (status.status === 'completed' && status.credentialId) {
        return status.credentialId;
      }

      if (status.status === 'failed') {
        throw new Error(`OAuth failed: ${status.error || 'Unknown error'}`);
      }

      if (status.status === 'expired') {
        throw new Error('OAuth flow expired');
      }

      await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
    }

    throw new Error('OAuth flow timed out');
  }

  /**
   * Get all credentials for a user.
   */
  async listUserCredentials(userId: string): Promise<Credential[]> {
    const result = await this.client.request<{
      credentials: Credential[];
    }>('GET', `/credentials?namespace=user_${userId}`);
    return result.credentials ?? [];
  }

  /**
   * Get access token to call external API.
   */
  async getAccessToken(credentialId: string): Promise<{
    accessToken: string;
    tokenType: string;
    expiresIn: number;
  }> {
    const result = await this.client.request<{
      access_token: string;
      token_type: string;
      expires_in: number;
    }>('GET', `/credentials/${credentialId}/token`);

    return {
      accessToken: result.access_token,
      tokenType: result.token_type,
      expiresIn: result.expires_in
    };
  }

  /**
   * Delete a credential.
   */
  async deleteCredential(credentialId: string): Promise<void> {
    await this.client.request('DELETE', `/credentials/${credentialId}`);
  }

  /**
   * Force refresh a credential's token.
   */
  async refreshCredential(credentialId: string): Promise<void> {
    await this.client.request('POST', `/credentials/${credentialId}/refresh`);
  }
}

interface Credential {
  id: string;
  service_id: string;
  service_name: string;
  namespace: string;
  status: 'pending' | 'active' | 'expired' | 'revoked';
  scopes: string[];
  metadata?: Record<string, string>;
  created_at: string;
  last_refreshed_at?: string;
  expires_at?: string;
}
```

### Python Implementation

```python
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Credential:
    id: str
    service_id: str
    service_name: str
    namespace: str
    status: str  # 'pending' | 'active' | 'expired' | 'revoked'
    scopes: List[str]
    created_at: str
    metadata: Optional[Dict[str, str]] = None
    last_refreshed_at: Optional[str] = None
    expires_at: Optional[str] = None

@dataclass
class OAuthStatus:
    status: str
    credential_id: Optional[str] = None
    error: Optional[str] = None

class CredentialManager:
    def __init__(self, client):
        self.client = client

    def initiate_oauth(
        self,
        user_id: str,
        service_id: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Start OAuth flow for a user to connect an external service."""
        result = self.client.request('POST', '/oauth/initiate', {
            'service_id': service_id,
            'namespace': f'user_{user_id}',
            'redirect_uri': redirect_uri,
            'scopes': scopes
        })

        return {
            'flow_id': result['flow_id'],
            'authorization_url': result['authorization_url']
        }

    def check_oauth_status(self, flow_id: str) -> OAuthStatus:
        """Check OAuth flow status and get credential ID if completed."""
        result = self.client.request('GET', f'/oauth/status/{flow_id}')

        return OAuthStatus(
            status=result['status'],
            credential_id=result.get('credential_id'),
            error=result.get('error')
        )

    def wait_for_oauth_completion(
        self,
        flow_id: str,
        timeout_seconds: int = 300,
        poll_interval_seconds: int = 2
    ) -> str:
        """Wait for OAuth flow to complete with polling."""
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            status = self.check_oauth_status(flow_id)

            if status.status == 'completed' and status.credential_id:
                return status.credential_id

            if status.status == 'failed':
                raise Exception(f'OAuth failed: {status.error or "Unknown error"}')

            if status.status == 'expired':
                raise Exception('OAuth flow expired')

            time.sleep(poll_interval_seconds)

        raise Exception('OAuth flow timed out')

    def list_user_credentials(self, user_id: str) -> List[Credential]:
        """Get all credentials for a user."""
        result = self.client.request('GET', f'/credentials?namespace=user_{user_id}')
        credentials_data = result.get('credentials', [])
        return [
            Credential(
                id=cred['id'],
                service_id=cred['service_id'],
                service_name=cred['service_name'],
                namespace=cred['namespace'],
                status=cred['status'],
                scopes=cred['scopes'],
                created_at=cred['created_at'],
                metadata=cred.get('metadata'),
                last_refreshed_at=cred.get('last_refreshed_at'),
                expires_at=cred.get('expires_at')
            )
            for cred in credentials_data
        ]

    def get_access_token(self, credential_id: str) -> Dict[str, Any]:
        """Get access token to call external API."""
        result = self.client.request('GET', f'/credentials/{credential_id}/token')
        return {
            'access_token': result['access_token'],
            'token_type': result['token_type'],
            'expires_in': result['expires_in']
        }

    def delete_credential(self, credential_id: str) -> None:
        """Delete a credential."""
        self.client.request('DELETE', f'/credentials/{credential_id}')

    def refresh_credential(self, credential_id: str) -> None:
        """Force refresh a credential's token."""
        self.client.request('POST', f'/credentials/{credential_id}/refresh')
```

### Elixir Implementation

```elixir
defmodule MyApp.Interactor.CredentialManager do
  @moduledoc """
  Manage OAuth credentials through Interactor.
  """

  alias MyApp.Interactor.Client

  @doc """
  Start OAuth flow for a user to connect an external service.
  """
  def initiate_oauth(user_id, service_id, redirect_uri, scopes \\ nil) do
    case Client.request(:post, "/oauth/initiate", %{
      service_id: service_id,
      namespace: "user_#{user_id}",
      redirect_uri: redirect_uri,
      scopes: scopes
    }) do
      {:ok, %{"flow_id" => flow_id, "authorization_url" => url}} ->
        {:ok, %{flow_id: flow_id, authorization_url: url}}

      {:error, reason} ->
        {:error, reason}
    end
  end

  @doc """
  Check OAuth flow status.
  """
  def check_oauth_status(flow_id) do
    case Client.request(:get, "/oauth/status/#{flow_id}") do
      {:ok, result} ->
        {:ok, %{
          status: result["status"],
          credential_id: result["credential_id"],
          error: result["error"]
        }}

      {:error, reason} ->
        {:error, reason}
    end
  end

  @doc """
  Wait for OAuth flow to complete with polling.
  """
  def wait_for_oauth_completion(flow_id, opts \\ []) do
    timeout_ms = Keyword.get(opts, :timeout_ms, 300_000)
    poll_interval_ms = Keyword.get(opts, :poll_interval_ms, 2_000)

    deadline = System.monotonic_time(:millisecond) + timeout_ms
    do_wait_for_completion(flow_id, deadline, poll_interval_ms)
  end

  defp do_wait_for_completion(flow_id, deadline, poll_interval_ms) do
    if System.monotonic_time(:millisecond) > deadline do
      {:error, :timeout}
    else
      case check_oauth_status(flow_id) do
        {:ok, %{status: "completed", credential_id: cred_id}} when not is_nil(cred_id) ->
          {:ok, cred_id}

        {:ok, %{status: "failed", error: error}} ->
          {:error, {:oauth_failed, error}}

        {:ok, %{status: "expired"}} ->
          {:error, :oauth_expired}

        {:ok, %{status: "pending"}} ->
          Process.sleep(poll_interval_ms)
          do_wait_for_completion(flow_id, deadline, poll_interval_ms)

        {:error, reason} ->
          {:error, reason}
      end
    end
  end

  @doc """
  List all credentials for a user.
  """
  def list_user_credentials(user_id) do
    case Client.request(:get, "/credentials?namespace=user_#{user_id}") do
      {:ok, %{"credentials" => credentials}} ->
        {:ok, credentials}

      {:ok, %{}} ->
        {:ok, []}

      {:error, reason} ->
        {:error, reason}
    end
  end

  @doc """
  Get access token for calling external API.
  """
  def get_access_token(credential_id) do
    case Client.request(:get, "/credentials/#{credential_id}/token") do
      {:ok, %{"access_token" => token, "token_type" => type, "expires_in" => expires}} ->
        {:ok, %{access_token: token, token_type: type, expires_in: expires}}

      {:error, reason} ->
        {:error, reason}
    end
  end

  @doc """
  Delete a credential.
  """
  def delete_credential(credential_id) do
    Client.request(:delete, "/credentials/#{credential_id}")
  end

  @doc """
  Force refresh a credential's token.
  """
  def refresh_credential(credential_id) do
    Client.request(:post, "/credentials/#{credential_id}/refresh")
  end
end
```

> **Production Recommendation**: The `waitForOAuthCompletion` polling functions above are
> shown for simplicity. In production, prefer using **webhooks** to receive `credential.created`
> events instead of polling. Webhooks are more efficient and provide real-time notifications.
> See the `interactor-webhooks` skill for setup.

> **Timeout Note**: OAuth flows expire after **15 minutes** (`expires_at` in the initiate response).
> The example polling timeout of 5 minutes is intentionally shorter—if the user hasn't completed
> authorization within 5 minutes, they likely abandoned the flow. You can extend the polling
> timeout up to 15 minutes, but consider providing user feedback for long waits.

---

## Custom OAuth Apps

By default, Interactor uses platform OAuth credentials. Configure your own for better branding and higher rate limits.

### List OAuth Client Configs

```bash
curl https://core.interactor.com/api/v1/oauth-client-configs \
  -H "Authorization: Bearer <token>"
```

### Create Custom OAuth Config

```bash
curl -X POST https://core.interactor.com/api/v1/oauth-client-configs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "auth_provider": "google",
    "client_id": "your-google-client-id.apps.googleusercontent.com",
    "client_secret": "your-google-client-secret",
    "enabled": true
  }'
```

**Supported Providers:**
- `google`
- `slack`
- `microsoft`
- `salesforce`
- `github`
- `dropbox`

### Get Config by Provider

```bash
curl https://core.interactor.com/api/v1/oauth-client-configs/provider/google \
  -H "Authorization: Bearer <token>"
```

### Update Config

```bash
curl -X PUT https://core.interactor.com/api/v1/oauth-client-configs/config_123 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "client_secret": "new-client-secret"
  }'
```

### Toggle Config (Enable/Disable)

```bash
curl -X POST https://core.interactor.com/api/v1/oauth-client-configs/config_123/toggle \
  -H "Authorization: Bearer <token>"
```

### Delete Config

```bash
curl -X DELETE https://core.interactor.com/api/v1/oauth-client-configs/config_123 \
  -H "Authorization: Bearer <token>"
```

---

## API Key Credentials (Non-OAuth)

Interactor can securely store API keys for services that don't support OAuth (e.g., SendGrid, Twilio, custom APIs).

### Differences from OAuth Credentials

| Aspect | OAuth Credentials | API Key Credentials |
|--------|-------------------|---------------------|
| **Creation** | OAuth flow (`/oauth/initiate`) | Direct API call |
| **Refresh lifecycle** | Automatic token refresh | No refresh needed |
| **Status values** | `pending`, `active`, `expired`, `revoked` | `active` only (until deleted) |
| **Token retrieval** | `/credentials/{id}/token` returns access token | `/credentials/{id}/token` returns API key |
| **Expiration** | Token-based expiration | No expiration (unless service invalidates) |

### Store an API Key

```bash
curl -X POST https://core.interactor.com/api/v1/credentials \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "sendgrid",
    "namespace": "user_123",
    "auth_type": "api_key",
    "api_key": "SG.xxxxxxxxxxxx",
    "metadata": {
      "label": "Production SendGrid"
    }
  }'
```

**Response** *(structure inferred)*:
```json
{
  "data": {
    "id": "cred_xyz",
    "service_id": "sendgrid",
    "namespace": "user_123",
    "auth_type": "api_key",
    "status": "active",
    "metadata": {
      "label": "Production SendGrid"
    },
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### Retrieve an API Key

Use the same `/token` endpoint as OAuth credentials:

```bash
curl https://core.interactor.com/api/v1/credentials/cred_xyz/token \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "access_token": "SG.xxxxxxxxxxxx",
    "token_type": "api_key"
  }
}
```

### API Key Lifecycle

```
┌─────────────────┐
│     active      │──────────────────┐
└─────────────────┘                  │
        │                            │
        │ DELETE /credentials/{id}   │ Service invalidates key
        │                            │ (detected on use)
        ▼                            ▼
┌─────────────────┐          ┌─────────────────┐
│    (deleted)    │          │    (invalid)    │
└─────────────────┘          └─────────────────┘
```

> **Note**: Unlike OAuth credentials, API keys don't have automatic status updates.
> If an external service invalidates a key, you'll discover this when the key fails.
> Consider implementing health checks for critical API key credentials.

---

## Discovering Supported Services

Interactor maintains a catalog of supported services and their capabilities.

### List Available Services

```bash
curl https://core.interactor.com/api/v1/services \
  -H "Authorization: Bearer <token>"
```

**Response** *(structure inferred)*:
```json
{
  "data": {
    "services": [
      {
        "service_id": "google_calendar",
        "name": "Google Calendar",
        "auth_type": "oauth",
        "available_scopes": [
          "calendar.readonly",
          "calendar.events",
          "calendar.events.readonly"
        ],
        "default_scopes": ["calendar.readonly"]
      },
      {
        "service_id": "slack",
        "name": "Slack",
        "auth_type": "oauth",
        "available_scopes": [
          "channels:read",
          "chat:write",
          "users:read"
        ]
      },
      {
        "service_id": "sendgrid",
        "name": "SendGrid",
        "auth_type": "api_key",
        "available_scopes": null
      }
    ]
  }
}
```

### Service Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `service_id` | string | Unique identifier used in API calls |
| `name` | string | Human-readable service name |
| `auth_type` | string | `oauth` or `api_key` |
| `available_scopes` | array | Valid scopes for OAuth services (null for API key services) |
| `default_scopes` | array | Scopes requested if none specified |

> **Tip**: Cache the service catalog on your backend. It changes infrequently
> and caching reduces API calls during OAuth flow initiation.

---

## Credential Status Lifecycle

```
                    ┌─────────────┐
                    │   pending   │
                    └──────┬──────┘
                           │ OAuth completes
                           ▼
                    ┌─────────────┐
           ┌───────>│   active    │<──────┐
           │        └──────┬──────┘       │
           │               │              │
   refresh │    token      │    user      │ re-authorize
  succeeds │   expires     │   revokes    │
           │               │              │
           │        ┌──────┴──────┐       │
           └────────│   expired   │       │
                    └─────────────┘       │
                           │              │
                           ▼              │
                    ┌─────────────┐       │
                    │   revoked   │───────┘
                    └─────────────┘
```

### Status Descriptions

| Status | Description | Action |
|--------|-------------|--------|
| `pending` | OAuth flow initiated but not completed | Wait for user to complete authorization |
| `active` | Token valid and working | Use normally |
| `expired` | Token expired and refresh failed | Re-initiate OAuth flow |
| `revoked` | User revoked access in external service | Re-initiate OAuth flow |

---

## Error Handling

### Credential-Specific Errors

| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| `credential_not_found` | 404 | Credential doesn't exist | Check credential ID |
| `credential_expired` | 400 | OAuth token expired and refresh failed | Re-initiate OAuth flow |
| `credential_revoked` | 400 | User revoked access | Re-initiate OAuth flow |
| `invalid_scopes` | 400 | Requested scopes not available | Check service documentation |
| `oauth_flow_expired` | 400 | OAuth flow timed out (15 min) | Start new OAuth flow |
| `oauth_flow_not_found` | 404 | Flow ID doesn't exist | Start new OAuth flow |

### Error Handling Example

```typescript
async function getExternalApiToken(credentialId: string): Promise<string> {
  try {
    const { accessToken } = await credentialManager.getAccessToken(credentialId);
    return accessToken;
  } catch (error: any) {
    const code = error.response?.data?.error?.code;

    switch (code) {
      case 'credential_expired':
      case 'credential_revoked':
        // Token is no longer valid, need to re-authorize
        throw new ReauthorizationRequiredError(
          'Please reconnect your account',
          credentialId
        );

      case 'credential_not_found':
        throw new CredentialNotFoundError(
          'Credential not found',
          credentialId
        );

      default:
        throw error;
    }
  }
}
```

---

## Webhook Events

Subscribe to credential events for real-time updates:

| Event | Description | When Triggered |
|-------|-------------|----------------|
| `credential.created` | New credential created | OAuth flow completed |
| `credential.refreshed` | Token successfully refreshed | Automatic or manual refresh |
| `credential.expired` | Token expired (refresh failed) | Refresh token invalid |
| `credential.revoked` | User revoked access | User revoked in external service |

See `interactor-webhooks` skill for webhook setup.

### Webhook Payload Example

```json
{
  "id": "evt_abc123",
  "type": "credential.expired",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "credential_id": "cred_abc",
    "service_id": "google_calendar",
    "namespace": "user_123",
    "reason": "refresh_token_invalid"
  }
}
```

---

## Security Considerations

| Concern | Recommendation |
|---------|----------------|
| **Token Logging** | Never log access tokens - they grant access to user data in external services |
| **Namespace Isolation** | Each user MUST have a unique namespace (e.g., `user_{id}`) to prevent cross-user access |
| **Credential ID Exposure** | Treat credential IDs as sensitive; avoid exposing them in client-side code or URLs |
| **Webhook Verification** | Always verify webhook signatures before processing credential events |
| **Scope Minimization** | Request only the OAuth scopes your application actually needs |
| **Token Storage** | Let Interactor handle token storage; never store access/refresh tokens in your own database |
| **Error Messages** | Don't expose credential details in error messages shown to users |

---

## Rate Limits & Token Caching

### API Rate Limits

Interactor applies rate limits to protect service stability. Monitor these headers in API responses:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests per window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

**Rate limit categories:**

| Category | Typical Limit | Endpoints |
|----------|---------------|-----------|
| Credential reads | High | `GET /credentials`, `GET /credentials/{id}` |
| Token retrieval | High | `GET /credentials/{id}/token` |
| OAuth flows | Moderate | `POST /oauth/initiate`, `GET /oauth/status` |
| Credential writes | Lower | `POST /credentials`, `DELETE /credentials/{id}` |

### Handling Rate Limits

When you receive a `429 Too Many Requests` response:

```typescript
async function requestWithRetry(fn: () => Promise<Response>, maxRetries = 3): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await fn();

    if (response.status === 429) {
      const resetTime = parseInt(response.headers.get('X-RateLimit-Reset') || '0');
      const waitMs = Math.max(1000, (resetTime * 1000) - Date.now());

      // Exponential backoff with jitter
      const backoff = Math.min(waitMs, 1000 * Math.pow(2, attempt) + Math.random() * 1000);
      await new Promise(resolve => setTimeout(resolve, backoff));
      continue;
    }

    return response;
  }
  throw new Error('Rate limit exceeded after retries');
}
```

### Token Caching Strategy

The `/credentials/{id}/token` endpoint automatically refreshes expired tokens, but caching reduces API calls:

```typescript
interface CachedToken {
  accessToken: string;
  expiresAt: number; // Unix timestamp
}

const tokenCache = new Map<string, CachedToken>();

async function getToken(credentialId: string): Promise<string> {
  const cached = tokenCache.get(credentialId);

  // Use cached token if valid for at least 5 more minutes
  if (cached && cached.expiresAt > Date.now() + 5 * 60 * 1000) {
    return cached.accessToken;
  }

  // Fetch fresh token
  const { accessToken, expiresIn } = await credentialManager.getAccessToken(credentialId);

  tokenCache.set(credentialId, {
    accessToken,
    expiresAt: Date.now() + (expiresIn * 1000)
  });

  return accessToken;
}
```

**Recommended cache TTLs:**

| Data | Cache Duration | Reason |
|------|----------------|--------|
| Access tokens | `expires_in - 5 minutes` | Buffer for refresh |
| Service catalog | 24 hours | Changes infrequently |
| Credential metadata | 5-15 minutes | May change (scopes, status) |

---

## Best Practices

### DO

- **Use namespaces per user** - Isolate each user's credentials with `user_{id}` namespace
- **Handle revocation gracefully** - Prompt users to re-authorize when credentials are revoked
- **Request minimal scopes** - Only request the OAuth permissions you actually need
- **Use custom OAuth apps for production** - Provides better branding and higher rate limits
- **Monitor credential health** - Subscribe to webhook events for proactive handling
- **Cache tokens appropriately** - The `/token` endpoint handles refresh, but cache to reduce calls

### DON'T

- **Don't store external tokens in your database** - Let Interactor handle secure storage
- **Don't ignore credential status** - Always check status before assuming tokens are valid
- **Don't request excessive scopes** - Users are less likely to authorize broad permissions
- **Don't poll excessively** - Use webhooks instead of polling for status changes

---

## Troubleshooting

### OAuth flow returns `expired` immediately
- OAuth flow URLs expire after **15 minutes**
- Ensure the user completes authorization promptly after redirect
- If users consistently timeout, consider UX improvements to guide them faster

### Token refresh keeps failing
- Check if the user revoked access in the external service's settings
- Verify your OAuth app credentials (client_id/client_secret) are still valid
- For custom OAuth apps, ensure the refresh token hasn't been invalidated

### `invalid_scopes` error
- The external service may have deprecated or renamed scopes
- Check the provider's current OAuth documentation for valid scope names
- Some scopes require app verification (e.g., Google sensitive scopes)

### `credential_not_found` after successful OAuth
- Ensure you're using the correct `credential_id` from the OAuth flow completion
- Check that the namespace matches what was used during initiation
- Verify the credential wasn't deleted by another process

### Webhook events not being received
- Verify your webhook endpoint is publicly accessible
- Check that you've subscribed to credential events (see `interactor-webhooks` skill)
- Ensure webhook signature verification isn't rejecting valid requests

### External API returns 401 despite valid credential
- The access token may have just expired; call `/credentials/{id}/token` to get a fresh one
- Some services require re-authorization after certain account changes
- Check if the user's account in the external service is still active

---

## Common Services and Scopes

> **Note**: The scope names shown below are Interactor's simplified identifiers.
> Interactor automatically maps these to the provider's full OAuth scope URLs
> (e.g., `calendar.readonly` → `https://www.googleapis.com/auth/calendar.readonly`).
> Refer to each provider's OAuth documentation for the complete list of available scopes.

### Google Calendar

```javascript
{
  service_id: "google_calendar",
  scopes: [
    "calendar.readonly",      // Read calendars
    "calendar.events",        // Read/write events
    "calendar.events.readonly" // Read events only
  ]
}
```

### Google Drive

```javascript
{
  service_id: "google_drive",
  scopes: [
    "drive.readonly",         // Read all files
    "drive.file",             // Access files created by app
    "drive.metadata.readonly" // Read file metadata
  ]
}
```

### Slack

```javascript
{
  service_id: "slack",
  scopes: [
    "channels:read",          // View channels
    "chat:write",             // Send messages
    "users:read",             // View users
    "files:read"              // Access files
  ]
}
```

### Microsoft 365

```javascript
{
  service_id: "microsoft",
  scopes: [
    "Calendars.Read",         // Read calendars
    "Mail.Read",              // Read email
    "Files.Read",             // Read OneDrive files
    "User.Read"               // Read user profile
  ]
}
```

---

## Output Format

When implementing credential management, provide this summary:

```markdown
## Credential Management Implementation Report

**Date**: YYYY-MM-DD
**User/Namespace**: user_123

### OAuth Flow Status
| Step | Status |
|------|--------|
| Initiate OAuth | ✓ Completed |
| User Authorization | ✓ Completed |
| Token Exchange | ✓ Completed |
| Credential Created | ✓ cred_abc |

### Connected Services
| Service | Status | Scopes |
|---------|--------|--------|
| Google Calendar | Active | calendar.readonly, calendar.events |
| Slack | Active | channels:read, chat:write |

### Implementation Checklist
- [ ] OAuth flow initiation endpoint
- [ ] OAuth callback handling
- [ ] Token retrieval for API calls
- [ ] Credential status monitoring
- [ ] Webhook handlers for credential events
- [ ] Re-authorization flow for expired/revoked credentials

### Next Steps
1. Use credentials with AI agents (see `interactor-agents` skill)
2. Set up credential webhooks (see `interactor-webhooks` skill)
```

---

## Related Skills

- **interactor-auth**: Setup authentication (prerequisite)
- **interactor-agents**: AI agents can use credentials to access external services
- **interactor-workflows**: Automate tasks using stored credentials
- **interactor-webhooks**: Get notified of credential status changes
