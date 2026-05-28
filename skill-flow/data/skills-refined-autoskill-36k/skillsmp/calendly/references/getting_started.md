# Calendly API - Getting Started

## Overview

Calendly provides three APIs for integration:

### API v2 (Current & Recommended)
REST-based API with predictable resource-oriented URLs. Uses JSON for request/response bodies and standard HTTP methods, authentication, and response codes.

**Key capabilities:**
- Retrieve scheduling links for users and event types
- Access scheduled event data
- Manage organization memberships
- Sync meeting data with external systems

### Embed API
Add Calendly scheduling pages directly to your website using JavaScript widgets.

**Options:**
- Inline embed (embedded in page)
- Popup widget (modal overlay)
- Badge widget (floating button)

### Webhook API
Receive real-time notifications when scheduling events occur (created, canceled, rescheduled).

## Authentication

### Personal Access Tokens

Best for internal applications used only by your team.

**Generation Steps:**
1. Log in to your Calendly account
2. Navigate to Integrations Page
3. Select API & Webhooks
4. Click Generate Token
5. Name your token descriptively
6. Copy immediately - tokens are not stored and cannot be retrieved later

**Security Notes:**
- Create separate tokens for different integrations
- Never share tokens publicly or in repositories
- Tokens are revoked if you change email, password, or login method

**Usage:**
```bash
curl -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  https://api.calendly.com/users/me
```

### OAuth 2.0

Recommended for public applications serving multiple Calendly users.

**Flow:**
1. Redirect user to authorization URL
2. User grants permission
3. Receive authorization code
4. Exchange code for access token
5. Use access token for API calls

**Authorization URL:**
```
https://auth.calendly.com/oauth/authorize
  ?client_id=YOUR_CLIENT_ID
  &response_type=code
  &redirect_uri=YOUR_REDIRECT_URI
```

**Token Exchange:**
```bash
POST https://auth.calendly.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=AUTHORIZATION_CODE
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&redirect_uri=YOUR_REDIRECT_URI
```

## First API Call

After obtaining authentication, make your first call to get user information:

```bash
curl -X GET "https://api.calendly.com/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "resource": {
    "uri": "https://api.calendly.com/users/AAAAAAAAAAAAAAAA",
    "name": "John Doe",
    "slug": "johndoe",
    "email": "john@example.com",
    "scheduling_url": "https://calendly.com/johndoe",
    "timezone": "America/New_York",
    "avatar_url": "https://...",
    "created_at": "2019-01-02T03:04:05.678Z",
    "updated_at": "2019-08-07T06:05:04.321Z",
    "current_organization": "https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB"
  }
}
```

## Key URIs

Many API calls require URIs as parameters:

- **User URI**: From `users/me` response (`uri` field)
- **Organization URI**: From `users/me` response (`current_organization` field)
- **Event Type URI**: From event type listing
- **Scheduled Event URI**: From scheduled events listing

## Subscription Access

| Plan | API Access | Webhook Access |
|------|-----------|----------------|
| Free | Most GET/POST endpoints | No |
| Standard | Full API access | Yes |
| Teams | Full API access + admin endpoints | Yes |
| Enterprise | Full access + enterprise endpoints | Yes |

## Next Steps

1. Set up authentication (Personal Token or OAuth)
2. Make test calls to `/users/me`
3. Explore event types and scheduled events
4. Set up webhooks for real-time notifications
5. Implement embed widgets for scheduling pages
