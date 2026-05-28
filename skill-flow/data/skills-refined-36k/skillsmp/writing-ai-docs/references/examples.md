---
title: "AI-Ready Documentation Examples"
description: "Complete before/after examples showing common anti-patterns and correct patterns for AI-readable documentation"
skill: writing-ai-docs
type: reference
created: 2025-10-20
lastUpdated: 2025-10-28
---

## Example 0: Complete Template

This example shows a complete, well-structured guide document that follows all AI-ready principles.

```markdown
---
title: "How to Authenticate API Requests"
description: "Step-by-step guide for authenticating with the API using Bearer tokens"
type: guide
difficulty: beginner
duration: "10 minutes"
created: 2025-10-20
lastUpdated: 2025-10-20
---

# How to Authenticate API Requests

Learn how to authenticate your API requests using Bearer tokens.

## What You'll Learn

- How to obtain an API key
- How to add authentication headers
- How to handle authentication errors

**Time required**: 10 minutes
**Difficulty**: Beginner

## Prerequisites

Before starting, ensure you have:

1. **An account** at https://dashboard.example.com
2. **API access enabled** (Settings > API Access > Enable)
3. **A tool to make HTTP requests** (curl, Postman, or code)

## Step 1: Get Your API Key

API keys authenticate your requests to the API.

**How to create an API key**:

1. Log in to https://dashboard.example.com
2. Navigate to Settings > API Keys
3. Click "Create New Key"
4. Copy the key (starts with `sk_live_` or `sk_test_`)

**Important**: Save your API key securely. It won't be shown again.

## Step 2: Add Authentication Header

Add your API key to the Authorization header in every request.

**Header format**:
```http
Authorization: Bearer YOUR_API_KEY
```

**Complete example**:

```bash
curl https://api.example.com/v2/users \
  -H "Authorization: Bearer sk_test_abc123" \
  -H "Content-Type: application/json"
```

**Expected response**:

```json
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ]
}
```

## Step 3: Handle Errors

Authentication errors return 401 status code.

**Common error**:

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid API key"
  }
}
```

**Solutions**:

- Verify API key is correct (check for typos)
- Confirm key hasn't been deleted in dashboard
- Ensure key starts with `sk_live_` or `sk_test_`
- Check key is for correct environment (test vs production)

## Verification

Your authentication is working correctly if:

✅ Request returns 200 status code
✅ Response contains expected data
✅ No "unauthorized" error messages

## Common Issues

### Issue: "Invalid API key" Error

**Symptoms**: 401 error with message "Invalid API key"

**Causes**:

- Typo in API key
- Using test key in production environment
- API key was deleted or expired

**Solution**:

```bash
# Verify your API key format
echo $API_KEY | grep -E '^sk_(test|live)_[a-zA-Z0-9]+'

# Create new key if needed
# Go to: https://dashboard.example.com/settings/api-keys
```

## Next Steps

- [Rate Limits](/docs/rate-limits) - Understand API rate limits
- [Error Handling](/docs/errors) - Handle all API errors
- [API Reference](/docs/api) - Explore available endpoints

```

**Why this works**:
- ✅ Complete frontmatter with all required fields including created/lastUpdated
- ✅ One H1, strict heading hierarchy (H1→H2→H3)
- ✅ Each section self-contained with context
- ✅ Explicit prerequisites stated upfront
- ✅ All code in fenced blocks with language tags
- ✅ Expected outputs shown
- ✅ Common issues section included
- ✅ Clear next steps provided
- ✅ Consistent terminology throughout
- ✅ No vague pronouns

---

## Example 1: API Documentation

### ❌ BAD: Multiple Anti-Patterns

```markdown
---
title: API docs
---

### Users Endpoint

You can get users from our API. Just call the endpoint and it will return them.

Use your key to authenticate. Add it to the header and make the request. If it doesn't work, check your credentials.

Example: curl https://api.example.com/users -H "Authorization: Bearer YOUR_KEY"

Errors: 401 means auth failed, 404 means not found
```

**Problems**:

1. ❌ Missing required frontmatter fields (description, type, created, lastUpdated)
2. ❌ Skipped heading level (no H1, starts with H3)
3. ❌ Vague pronouns ("it", "them", "your key")
4. ❌ Inline code mixed with prose
5. ❌ No code block language tags
6. ❌ Not self-contained (assumes prior knowledge)
7. ❌ Scattered information (auth mentioned but not explained)

### ✅ GOOD: Correct Pattern

```markdown
---
title: "GET /api/v2/users"
description: "Retrieve a list of all users in your organization with pagination support"
type: api-endpoint
method: GET
endpoint: /api/v2/users
authentication: required
created: 2025-10-20
lastUpdated: 2025-10-20
---

# GET /api/v2/users

Retrieve a list of all users in your organization.

## Quick Reference

**Endpoint**: `GET https://api.example.com/v2/users`
**Authentication**: Required (Bearer token)
**Rate Limit**: 100 requests/hour (free), 1000/hour (pro)

## Prerequisites

Before making requests to this endpoint:

1. **API key** from Settings > API Keys in dashboard
2. **Organization access** (admin or member role)
3. **Tool to make requests** (curl, Postman, or code)

## Request

### Headers

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | Yes | `Bearer YOUR_API_KEY` |
| `Content-Type` | Yes | `application/json` |

### Example Request

```bash
curl https://api.example.com/v2/users \
  -H "Authorization: Bearer sk_test_abc123" \
  -H "Content-Type: application/json"
```

```javascript
// JavaScript example
const response = await fetch('https://api.example.com/v2/users', {
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
});

const users = await response.json();
console.log('Users:', users);
```

## Response

### Success Response (200 OK)

```json
{
  "users": [
    {
      "id": "usr_123",
      "email": "alice@example.com",
      "name": "Alice Smith",
      "role": "admin",
      "created_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": "usr_456",
      "email": "bob@example.com",
      "name": "Bob Jones",
      "role": "member",
      "created_at": "2025-02-20T14:22:00Z"
    }
  ],
  "total": 2,
  "page": 1
}
```

### Error Responses

#### 401 Unauthorized

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or expired API key"
  }
}
```

**Cause**: API key is missing, invalid, or expired

**Solution**: Verify your API key at https://dashboard.example.com/settings/api-keys

#### 404 Not Found

```json
{
  "error": {
    "code": "not_found",
    "message": "Endpoint not found"
  }
}
```

**Cause**: Incorrect endpoint URL or HTTP method

**Solution**: Verify the endpoint is `GET https://api.example.com/v2/users` (note: `/v2/`, not `/v1/`)

## Related Endpoints

- [POST /api/v2/users](/docs/api/create-user) - Create a new user
- [GET /api/v2/users/:id](/docs/api/get-user) - Get specific user
- [DELETE /api/v2/users/:id](/docs/api/delete-user) - Delete a user

```

**Why it works**:
1. ✅ Complete frontmatter with all required fields
2. ✅ One H1, strict hierarchy (H1→H2→H3)
3. ✅ Self-contained with prerequisites
4. ✅ Explicit language (no vague pronouns)
5. ✅ All code in fenced blocks with language tags
6. ✅ Related information grouped together
7. ✅ Consistent terminology ("API key" throughout)

---

## Example 2: Tutorial Documentation

### ❌ BAD: Assumes Context

```markdown
---
title: OAuth Tutorial
description: Learn OAuth
---

# Setting Up OAuth

Install the packages and configure it.

```bash
npm install oauth
```

Then add your credentials to the config file and start the server. If something goes wrong, check the logs.

```

**Problems**:

1. ❌ Vague description
2. ❌ Missing type, created, lastUpdated
3. ❌ Assumes knowledge (which config file? which logs?)
4. ❌ No prerequisites listed
5. ❌ Code block missing language tag
6. ❌ Inline instructions mixed with commands
7. ❌ No verification steps

### ✅ GOOD: Complete Tutorial

```markdown
---
title: "How to Add OAuth Authentication"
description: "Step-by-step guide to implement OAuth 2.0 authentication in a Node.js application"
type: tutorial
difficulty: intermediate
duration: "20 minutes"
prerequisites:
  - Node.js 16+ installed
  - Basic OAuth 2.0 understanding
  - API credentials from dashboard
created: 2025-10-20
lastUpdated: 2025-10-20
---

# How to Add OAuth Authentication

Learn how to implement OAuth 2.0 authentication in your Node.js application.

## What You'll Build

By completing this tutorial, you'll have:
- Working OAuth login flow
- Secure token storage
- Automatic token refresh
- Error handling for auth failures

**Time required**: 20 minutes
**Difficulty**: Intermediate

## Prerequisites

Before starting, ensure you have:

1. **Node.js 16 or higher** installed
   - Check: `node --version` should show v16.x.x or higher
   - Install from: https://nodejs.org

2. **OAuth credentials** from dashboard
   - Log in to https://dashboard.example.com
   - Navigate to Settings > OAuth Applications
   - Create new application
   - Save Client ID and Client Secret

3. **Basic OAuth 2.0 knowledge**
   - Understand authorization code flow
   - Know what access tokens and refresh tokens are
   - If new to OAuth: Read [OAuth Basics](/docs/concepts/oauth-basics) first

## Step 1: Install Dependencies

Install the required packages for OAuth implementation:

```bash
npm install express @example/oauth-sdk dotenv
```

**What each package does**:

- `express` - Web framework for handling OAuth callbacks
- `@example/oauth-sdk` - Official OAuth client library
- `dotenv` - Loads environment variables from .env file

**Verify installation**:

```bash
npm list --depth=0 | grep -E "(express|oauth-sdk|dotenv)"
```

Should show all three packages installed.

## Step 2: Configure Environment Variables

Create a `.env` file in your project root:

```bash
touch .env
```

Add your OAuth credentials:

```env
# OAuth Configuration
CLIENT_ID=your_client_id_from_dashboard
CLIENT_SECRET=your_client_secret_from_dashboard
REDIRECT_URI=http://localhost:3000/callback

# App Configuration
PORT=3000
```

**Security notes**:

- Never commit `.env` to version control
- Add `.env` to your `.gitignore` file immediately
- Use different credentials for development and production

**Create .gitignore**:

```bash
echo ".env" >> .gitignore
```

## Step 3: Create OAuth Client

Create `auth.js` in your project root:

```javascript
// auth.js
// OAuth client configuration for authentication flow
// Prerequisites: .env file with CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

require('dotenv').config();
const { OAuthClient } = require('@example/oauth-sdk');

// Initialize OAuth client with credentials from environment
const oauthClient = new OAuthClient({
  clientId: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  redirectUri: process.env.REDIRECT_URI,
  scopes: ['read:user', 'read:email']  // Requested permissions
});

module.exports = oauthClient;
```

## Step 4: Implement OAuth Flow

Create `server.js` to handle the OAuth flow:

```javascript
// server.js
// OAuth authentication server implementation

require('dotenv').config();
const express = require('express');
const oauthClient = require('./auth');

const app = express();
const PORT = process.env.PORT || 3000;

// Step 1: User clicks "Login" - redirect to OAuth provider
app.get('/login', (req, res) => {
  const authUrl = oauthClient.getAuthorizationUrl();
  res.redirect(authUrl);
});

// Step 2: OAuth provider redirects back with code
app.get('/callback', async (req, res) => {
  const { code } = req.query;

  if (!code) {
    return res.status(400).send('Missing authorization code');
  }

  try {
    // Exchange authorization code for access token
    const tokens = await oauthClient.exchangeCode(code);

    // Store tokens securely (in production, use database or encrypted session)
    console.log('Access Token:', tokens.access_token);
    console.log('Refresh Token:', tokens.refresh_token);

    res.send('Authentication successful! Check console for tokens.');
  } catch (error) {
    console.error('OAuth error:', error.message);
    res.status(500).send('Authentication failed');
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Login at: http://localhost:${PORT}/login`);
});
```

## Step 5: Test the Flow

Start your server:

```bash
node server.js
```

**Expected output**:

```text
Server running on http://localhost:3000
Login at: http://localhost:3000/login
```

Test the authentication flow:

1. Open browser to http://localhost:3000/login
2. You'll be redirected to OAuth provider
3. Log in and authorize the application
4. You'll be redirected back to `/callback`
5. Check terminal for access token and refresh token

## OAuth Verification

Your OAuth implementation is working correctly if:

✅ `/login` redirects to OAuth provider login page
✅ After authorization, you're redirected to `/callback`
✅ Terminal shows access token and refresh token
✅ No error messages in console

## OAuth Common Issues

### Issue: "ECONNREFUSED" Error

**Symptoms**: Server crashes with "Error: connect ECONNREFUSED"

**Cause**: OAuth provider endpoint is unreachable or CLIENT_ID is incorrect

**Solution**:

```bash
# Verify environment variables are loaded
node -e "require('dotenv').config(); console.log('CLIENT_ID:', process.env.CLIENT_ID)"

# Should show your CLIENT_ID, not undefined
```

If undefined, verify `.env` file exists and has correct format.

### Issue: "Invalid redirect_uri" Error

**Symptoms**: OAuth provider shows error "redirect_uri mismatch"

**Cause**: REDIRECT_URI in `.env` doesn't match dashboard configuration

**Solution**:

1. Check `.env`: `REDIRECT_URI=http://localhost:3000/callback`
2. Verify dashboard settings match exactly (including port and `/callback` path)
3. Ensure no trailing slash differences

## OAuth Next Steps

Now that you have basic OAuth working:

1. **Add token refresh** - See [Token Refresh Guide](/docs/guides/oauth-refresh)
2. **Secure token storage** - Use encrypted database instead of console.log
3. **Add logout** - Properly revoke tokens on logout
4. **Production deployment** - Use HTTPS and production OAuth credentials

## Related Documentation

- [OAuth Concepts](/docs/concepts/oauth) - Understand OAuth 2.0 in depth
- [Security Best Practices](/docs/guides/security) - Secure your OAuth implementation
- [API Reference](/docs/api/oauth) - Complete OAuth API documentation

```

**Why it works**:
1. ✅ Complete prerequisites with verification commands
2. ✅ Each step is self-contained
3. ✅ Explicit file names and paths
4. ✅ Complete, tested code examples
5. ✅ Expected output shown
6. ✅ Verification checklist
7. ✅ Troubleshooting for common issues
8. ✅ Clear next steps

---

## Example 3: Concept Explanation

### ❌ BAD: Scattered and Vague

```markdown
# Rate Limiting

We use rate limiting. It prevents abuse.

Different tiers have different limits. Check the header to see your limit.

If you exceed it, wait and try again.
```

**Problems**:

1. ❌ No frontmatter
2. ❌ Scattered information (definition, usage, error handling separated)
3. ❌ Vague ("it", "your limit", "different limits")
4. ❌ No concrete examples
5. ❌ Missing details (what header? how long to wait?)

### ✅ GOOD: Complete Explanation

```markdown
---
title: "Understanding API Rate Limits"
description: "How rate limiting works, checking your quota, and handling rate limit errors"
type: concept
audience: developers
created: 2025-10-20
lastUpdated: 2025-10-20
---

# Understanding API Rate Limits

Rate limiting controls the number of API requests you can make per hour to prevent abuse and ensure fair usage.

## How Rate Limits Work

The API tracks requests per API key and resets the counter every hour.

**Rate limits by tier**:
- Free tier: 100 requests per hour
- Pro tier: 1,000 requests per hour
- Enterprise tier: Custom limits (contact support)

**Reset schedule**: Rate limits reset at the top of each hour (e.g., 10:00:00, 11:00:00, 12:00:00)

## Checking Your Quota

Every API response includes rate limit headers showing your current status.

**Response headers**:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1698768000
```

**Header meanings**:

- `X-RateLimit-Limit` - Total requests allowed per hour for your tier
- `X-RateLimit-Remaining` - Requests remaining in current hour
- `X-RateLimit-Reset` - Unix timestamp when limit resets

**Check quota in code**:

```javascript
const response = await fetch('https://api.example.com/v2/users', {
  headers: { 'Authorization': `Bearer ${apiKey}` }
});

const remaining = response.headers.get('X-RateLimit-Remaining');
const reset = response.headers.get('X-RateLimit-Reset');

console.log(`Remaining requests: ${remaining}`);
console.log(`Resets at: ${new Date(reset * 1000).toISOString()}`);
```

## When You Exceed the Limit

Requests beyond your rate limit fail with 429 status code.

**Error response**:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 3600 seconds",
    "retry_after": 3600
  }
}
```

**How to handle rate limit errors**:

```javascript
try {
  const response = await fetch('https://api.example.com/v2/users', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });

  if (response.status === 429) {
    const data = await response.json();
    const retryAfter = data.error.retry_after;

    console.log(`Rate limited. Wait ${retryAfter} seconds`);

    // Wait and retry
    await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
    return fetch(url, options);  // Retry request
  }

  return response.json();
} catch (error) {
  console.error('Request failed:', error);
}
```

## Best Practices

**Monitor your usage**:

- Check `X-RateLimit-Remaining` header in each response
- Alert when remaining quota drops below 10%
- Track usage patterns to optimize request frequency

**Implement exponential backoff**:

- Wait longer between retries after each failure
- Don't retry immediately on 429 errors
- Respect the `retry_after` value in error response

**Upgrade if needed**:

- If you consistently hit limits, upgrade to Pro tier
- Enterprise tier offers custom limits for high-volume applications

## Rate Limiting Resources

- [Error Handling](/docs/guides/errors) - Handle all API errors
- [Authentication](/docs/guides/auth) - Authenticate API requests
- [Pricing](/pricing) - Compare tier limits and pricing

```

**Why it works**:
1. ✅ Complete frontmatter with audience specified
2. ✅ All related information in one section
3. ✅ Explicit language (specific header names, exact values)
4. ✅ Complete code examples with error handling
5. ✅ Concrete numbers and timestamps
6. ✅ Best practices section
7. ✅ Related documentation links

---

## Key Takeaways from Examples

**Structure wins**:
- Complete frontmatter sets context
- Strict heading hierarchy helps AI navigation
- Self-contained sections work when chunked

**Clarity beats brevity**:
- Explicit language > vague pronouns
- Repeat context > assume prior knowledge
- Complete examples > partial snippets

**Grouping matters**:
- Keep related info together (definition + usage + errors)
- Don't scatter concepts across sections
- One complete section > multiple partial sections
