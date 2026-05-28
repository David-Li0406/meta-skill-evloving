# Calendly API v1 to v2 Migration Guide

## Timeline

**Important**: Support for API v1 and v1 Webhooks will begin phasing out in **May 2025**.

While v1 is still supported until then, Calendly recommends migrating to v2 for:
- Better security (OAuth 2.0)
- More endpoints and capabilities
- Long-term support
- Enhanced data compliance

## Key Differences

### Authentication

| Aspect | API v1 | API v2 |
|--------|--------|--------|
| Method | API Key | Personal Access Token or OAuth 2.0 |
| Security | Basic | Enhanced (OAuth scopes) |
| Multi-user | Limited | Full support via OAuth |

### API Structure

**v1 Base URL**: `https://calendly.com/api/v1/`

**v2 Base URL**: `https://api.calendly.com/`

### Data Format

API v2 responses are **not backwards compatible** with v1. The data structure has fundamentally changed.

**v1 User Response:**
```json
{
  "data": {
    "type": "users",
    "id": "AAAAAA",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "url": "https://calendly.com/johndoe"
    }
  }
}
```

**v2 User Response:**
```json
{
  "resource": {
    "uri": "https://api.calendly.com/users/AAAAAAA",
    "name": "John Doe",
    "email": "john@example.com",
    "scheduling_url": "https://calendly.com/johndoe",
    "current_organization": "https://api.calendly.com/organizations/BBB"
  }
}
```

## Migration Steps

### 1. Update Authentication

**From v1 API Key:**
```bash
# Old v1 approach
curl -H "X-TOKEN: your-api-key" \
  https://calendly.com/api/v1/users/me
```

**To v2 Personal Access Token:**
```bash
# New v2 approach
curl -H "Authorization: Bearer your-personal-access-token" \
  https://api.calendly.com/users/me
```

**Or OAuth 2.0:**
```bash
curl -H "Authorization: Bearer your-oauth-access-token" \
  https://api.calendly.com/users/me
```

### 2. Update Endpoint URLs

| v1 Endpoint | v2 Endpoint |
|-------------|-------------|
| `/api/v1/users/me` | `/users/me` |
| `/api/v1/users/:id/event_types` | `/event_types?user=:uri` |
| `/api/v1/events` | `/scheduled_events` |
| `/api/v1/hooks` | `/webhook_subscriptions` |

### 3. Update Response Parsing

**v1 Collection:**
```json
{
  "data": [
    { "type": "events", "id": "...", "attributes": {...} }
  ]
}
```

**v2 Collection:**
```json
{
  "collection": [
    { "uri": "...", "name": "...", ... }
  ],
  "pagination": {
    "count": 20,
    "next_page_token": "..."
  }
}
```

### 4. Update Identifier References

v1 used numeric IDs. v2 uses full URIs.

**v1:**
```json
{ "user_id": "12345" }
```

**v2:**
```json
{ "user": "https://api.calendly.com/users/AAAAA-BBBBB-CCCCC" }
```

### 5. Update Webhook Subscriptions

**v1 Webhook Creation:**
```bash
POST /api/v1/hooks
{
  "url": "https://example.com/webhook",
  "events": ["invitee.created"]
}
```

**v2 Webhook Creation:**
```bash
POST /webhook_subscriptions
{
  "url": "https://example.com/webhook",
  "events": ["invitee.created"],
  "organization": "https://api.calendly.com/organizations/ORG_UUID",
  "scope": "organization"
}
```

**Key differences:**
- v2 requires `organization` parameter
- v2 requires `scope` (organization or user)
- v2 supports signing keys for verification

### 6. Update Webhook Payload Parsing

Payload structures have changed. Update your webhook handlers to parse v2 format.

**v2 Payload Structure:**
```json
{
  "event": "invitee.created",
  "created_at": "2023-01-15T10:30:00.000000Z",
  "created_by": "https://api.calendly.com/users/...",
  "payload": {
    "uri": "https://api.calendly.com/scheduled_events/.../invitees/...",
    "email": "invitee@example.com",
    "name": "John Doe",
    "event": "https://api.calendly.com/scheduled_events/...",
    "tracking": {
      "utm_source": "...",
      "utm_campaign": "..."
    }
  }
}
```

## Code Migration Example

### Python v1 to v2

**v1 Code:**
```python
import requests

API_KEY = "your-api-key"
BASE_URL = "https://calendly.com/api/v1"

def get_user():
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={"X-TOKEN": API_KEY}
    )
    data = response.json()
    return data["data"]["attributes"]

def get_events():
    response = requests.get(
        f"{BASE_URL}/users/me/events",
        headers={"X-TOKEN": API_KEY}
    )
    data = response.json()
    return [e["attributes"] for e in data["data"]]
```

**v2 Code:**
```python
import requests

ACCESS_TOKEN = "your-personal-access-token"
BASE_URL = "https://api.calendly.com"

def get_user():
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )
    data = response.json()
    return data["resource"]

def get_events(user_uri):
    response = requests.get(
        f"{BASE_URL}/scheduled_events",
        params={"user": user_uri},
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )
    data = response.json()
    return data["collection"]
```

## New v2 Capabilities

### Features not available in v1:
- **OAuth 2.0**: Secure multi-user access
- **Organization management**: Full admin capabilities
- **Enhanced webhooks**: Signing keys, organization scope
- **More endpoints**: Availability schedules, busy times, routing forms
- **Better pagination**: Cursor-based with page tokens
- **UTM tracking**: Built-in marketing attribution

## Testing Your Migration

1. **Set up test environment** with v2 credentials
2. **Run parallel** v1 and v2 calls to compare
3. **Validate data mapping** between v1 and v2 formats
4. **Test webhooks** with v2 subscription format
5. **Monitor** for any missing data or errors
6. **Gradual rollout** to production

## Support

For migration assistance:
- Documentation: https://developer.calendly.com/
- Email: support+developer@calendly.com
