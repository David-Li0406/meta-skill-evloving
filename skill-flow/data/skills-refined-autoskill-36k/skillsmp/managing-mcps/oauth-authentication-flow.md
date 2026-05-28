# OAuth Authentication Flow for MCP Servers

Detailed OAuth setup for MCP servers requiring authentication.

## OAuth Overview

Some MCP servers require OAuth 2.0 authentication:
- GitHub MCP (GitHub API access)
- Sentry MCP (Sentry account access)
- Internal company MCPs (corporate authentication)
- Cloud service MCPs (API authentication)

## When Authentication Required

**Signs that server needs authentication:**
- Documentation mentions OAuth or API keys
- Server requires user credentials
- Server provides specific authorization endpoints
- Server returns 401/403 without authentication

## Authentication Methods

### Method 1: Via Claude Code /mcp Command (Recommended)

Simplest method for OAuth authentication.

**Step 1: Add Server**

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**Step 2: Authenticate**

In Claude Code conversation, type:

```
/mcp
```

Shows:
- Connected servers
- Authentication status for each
- Options to authenticate or clear authentication

**Step 3: Follow OAuth Flow**

Click "Authenticate" option:
1. Browser opens to OAuth provider
2. Log in with your account
3. Authorize access
4. Redirected back to Claude Code
5. Authentication complete (tokens stored securely)

**Step 4: Tokens Auto-Refresh**

Claude Code:
- Stores tokens securely
- Refreshes automatically before expiration
- Handles refresh token flow
- No manual token management needed

### Method 2: Via MCP Inspector (For Testing)

Using official MCP Inspector tool for detailed authentication flow.

**Step 1: Install Inspector**

```bash
npx @modelcontextprotocol/inspector
```

**Step 2: Launch Inspector**

```bash
npx @modelcontextprotocol/inspector
```

Opens web interface at http://localhost:...

**Step 3: Configure Server**

1. Select transport type: HTTP or SSE
2. Enter server URL
3. In "MCP Configuration" section, click "Open Auth Settings"

**Step 4: Quick OAuth Flow**

1. Click "Quick OAuth Flow"
2. Browser opens to OAuth provider
3. Login and authorize
4. Inspector shows auth progress steps
5. Click "Continue" through OAuth flow steps
6. "Authentication complete" message appears

**Step 5: Copy Access Token**

In "OAuth Flow Progress" section:
- Find `access_token` value
- Copy to clipboard

**Step 6: Use in Configuration**

Add token to Claude Code server configuration:

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
      }
    }
  }
}
```

## OAuth Token Management

### Token Storage

Claude Code stores tokens:
- **Location:** Secure storage (OS keychain/credentials manager)
- **Encryption:** Platform-level security
- **Automatic:** No manual storage needed
- **Per-server:** Each server's token stored separately

### Token Refresh

Claude Code automatically:
- Monitors token expiration
- Refreshes before expiration
- Uses refresh token if available
- Handles token rotation
- Maintains continuity

**You don't need to:**
- Manually refresh tokens
- Re-authenticate regularly
- Store or manage refresh tokens
- Handle token expiration

### Clear Authentication

To remove stored token:

```
/mcp
```

Select "Clear authentication" for specific server

Or via CLI:

```bash
claude mcp remove github
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
# Reauthenticate when prompted
```

## Common OAuth Patterns

### Pattern 1: GitHub Integration

Setup GitHub MCP with authentication:

```bash
# Add server
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# In conversation
/mcp
# Select "Authenticate" for GitHub
# Complete OAuth flow
# Start using GitHub tools
```

Use in conversation:

```
/mcp__github__list_prs
/mcp__github__pr_review 123
```

### Pattern 2: Sentry Error Monitoring

Setup Sentry MCP:

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Authenticate:

```
/mcp
# Authenticate with Sentry account
```

### Pattern 3: Internal Company MCP

Setup internal corporate MCP with OAuth:

```bash
claude mcp add --transport http company-api https://mcp-internal.company.com/mcp \
  --scope project
```

Authenticate via `/mcp` command, OAuth redirects to company identity provider.

## Troubleshooting OAuth

### Browser Doesn't Open for OAuth

**Problem:** Clicking authenticate doesn't open browser

**Solutions:**
1. MCP Inspector method: Can see OAuth URL to copy/paste
2. Manual token: Obtain token separately, use `--header` flag
3. Check firewall: Ensure port 5000 (or shown port) not blocked

### "Invalid Token" Error

**Problem:** Server rejects token even after authentication

**Solutions:**
1. Clear authentication: Remove and re-add server
2. Re-authenticate: `/mcp` → "Clear authentication" → re-authenticate
3. Check scope: Token may not have required scope (see server docs)
4. Token expiration: If very old token, may have expired in storage

### Token Expired

**Problem:** "Token expired" or "Unauthorized" after not using for a while

**Solutions:**
1. Usually Claude Code refreshes automatically - no action needed
2. If still failing: Clear and re-authenticate
3. Check if server revoked access (revoke from server's web interface)

### Can't Access Specific Resource

**Problem:** OAuth succeeded but accessing resource returns permission error

**Solutions:**
1. Check OAuth scope: Token may not have scope for that resource
2. Check user permissions: Your account may not have access
3. Verify resource exists and is accessible via web interface
4. If internal server: Confirm VPN/network access active

### OAuth URL Not Reachable

**Problem:** Browser shows "Server unreachable" during OAuth

**Solutions:**
1. Check server URL is accessible
2. Verify network/firewall allows HTTPS
3. Confirm server is running and responding
4. Try OAuth URL manually in browser to diagnose

## OAuth Integration Examples

### Example 1: GitHub API Access

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "Show me my open PRs"
        }
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://api.githubcopilot.com/mcp/",
            "name": "github",
            "authorization_token": "github_oauth_token"  # OAuth token
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "github"
        }
    ],
    betas=["mcp-client-2025-11-20"]
)
```

### Example 2: Sentry Integration

```python
# Add Sentry MCP with OAuth
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What are recent errors in production?"
        }
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://mcp.sentry.dev/mcp",
            "name": "sentry",
            "authorization_token": "sentry_oauth_token"  # OAuth token
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "sentry"
        }
    ],
    betas=["mcp-client-2025-11-20"]
)
```

## Security Best Practices

### Token Storage

✅ **Do:**
- Use Claude Code's built-in secure token storage
- Let Claude Code handle token refresh
- Clear authentication when no longer needed
- Revoke access from server's web interface if compromised

❌ **Don't:**
- Hardcode tokens in .mcp.json
- Store tokens in plain text files
- Share tokens via email or chat
- Commit tokens to version control

### Scope Minimization

When authenticating:
- Request only necessary scopes (read vs write, specific resources)
- Avoid overly broad scopes
- Check what access is being requested before authorizing

### Account Security

- Use strong passwords on OAuth provider accounts
- Enable 2FA on accounts with OAuth access
- Monitor authorized applications in account settings
- Revoke access to unused MCP servers regularly

## OAuth Revocation

To revoke MCP server access:

**Via Claude Code:**
```
/mcp
# Select "Clear authentication" for specific server
```

**Via Server's Web Interface:**
1. Go to server's web interface (GitHub.com, Sentry.com, etc.)
2. Settings → Applications or Connected Apps
3. Find Claude Code or MCP app
4. Revoke access

**Via CLI:**
```bash
claude mcp remove github
```

## Getting Help with OAuth

**If authentication issues:**
1. Check MCP server documentation for OAuth requirements
2. Use MCP Inspector to diagnose OAuth flow
3. Verify network connectivity and firewall
4. Test with different OAuth scope if available
5. Ask for documentation via skill if unclear
