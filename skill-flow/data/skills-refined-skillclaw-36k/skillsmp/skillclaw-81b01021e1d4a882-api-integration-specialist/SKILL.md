---
name: api-integration-specialist
description: Use this skill when integrating third-party APIs into applications, ensuring proper authentication, error handling, and robust client implementation.
---

# Skill body

## When to Use This Skill

Use this skill when:
- Integrating third-party APIs (e.g., Stripe, Twilio, SendGrid)
- Building API client libraries or wrappers
- Implementing OAuth 2.0, API keys, or JWT authentication
- Setting up webhooks and event-driven integrations
- Handling rate limits, retries, and circuit breakers
- Transforming API responses for application use
- Debugging API integration issues

## Core Integration Principles

### 1. Authentication & Security

**API Key Management:**
```javascript
// Store keys in environment variables, never in code
const apiClient = new APIClient({
  apiKey: process.env.SERVICE_API_KEY,
  baseURL: process.env.SERVICE_BASE_URL
});
```

**OAuth 2.0 Flow:**
```javascript
// Authorization Code Flow
const oauth = new OAuth2Client({
  clientId: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  redirectUri: process.env.REDIRECT_URI,
  scopes: ['read:users', 'write:data']
});

// Get authorization URL
const authUrl = oauth.getAuthorizationUrl();

// Exchange code for tokens
const tokens = await oauth.exchangeCode(code);
```

### 2. Request/Response Handling

**Standardized Request Structure:**
```javascript
async function makeRequest(endpoint, options = {}) {
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
    'User-Agent': 'MyApp/1.0.0'
  };

  const response = await fetch(`${baseURL}${endpoint}`, {
    ...options,
    headers: { ...defaultHeaders, ...options.headers }
  });

  if (!response.ok) {
    throw new APIError(response.status, await response.json());
  }

  return response.json();
}
```

**Response Transformation:**
```javascript
class APIClient {
  async getUser(userId) {
    const raw = await this.request(`/users/${userId}`);

    // Transform external API format to internal model
    return {
      id: raw.user_id,
      email: raw.email_address,
      name: `${raw.first_name} ${raw.last_name}`
    };
  }
}
```