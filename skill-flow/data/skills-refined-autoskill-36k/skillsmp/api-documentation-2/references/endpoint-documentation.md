# Endpoint Documentation Standards

Standards for documenting API endpoints clearly and consistently.

## Endpoint Documentation Template

```markdown
## [HTTP Method] [Path]

[One-sentence description of what this endpoint does]

### Authentication

[Required/Optional] - [Auth type]

### Request

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource identifier |

#### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| per_page | integer | No | 20 | Items per page (max 100) |

#### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Resource name (1-255 chars) |
| email | string | Yes | Valid email address |

**Example Request:**
```json
{
  "name": "Example",
  "email": "example@test.com"
}
```

### Response

#### Success (200/201)
```json
{
  "id": "res_123",
  "name": "Example",
  "email": "example@test.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Error Responses
| Status | Description | Example |
|--------|-------------|---------|
| 400 | Invalid request | `{"error": "bad_request"}` |
| 401 | Not authenticated | `{"error": "unauthorized"}` |
| 404 | Not found | `{"error": "not_found"}` |
| 422 | Validation error | `{"error": "validation_error", "details": [...]}` |

### Code Examples

#### cURL
```bash
curl -X POST https://api.example.com/resources \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Example", "email": "example@test.com"}'
```

#### Python
```python
import requests

response = requests.post(
    "https://api.example.com/resources",
    headers={"Authorization": f"Bearer {token}"},
    json={"name": "Example", "email": "example@test.com"}
)
```
```

## Field Documentation Guidelines

### Type Descriptions

| Type | Format | Description | Example |
|------|--------|-------------|---------|
| string | - | Plain text | "hello" |
| string | email | Email address | "user@example.com" |
| string | uri | URL | "https://example.com" |
| string | date | ISO 8601 date | "2024-01-15" |
| string | date-time | ISO 8601 datetime | "2024-01-15T10:30:00Z" |
| string | uuid | UUID v4 | "550e8400-e29b-41d4-a716-446655440000" |
| integer | int32 | 32-bit integer | 42 |
| integer | int64 | 64-bit integer | 9223372036854775807 |
| number | float | Decimal number | 99.99 |
| boolean | - | True/false | true |
| array | - | List of items | [1, 2, 3] |
| object | - | JSON object | {"key": "value"} |

### Constraint Documentation

Always document constraints:

```markdown
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| name | string | 1-255 chars | Display name |
| quantity | integer | 1-100 | Item quantity |
| price | number | > 0 | Price in cents |
| status | string | enum: pending, active, closed | Current status |
| tags | array | max 10 items | List of tags |
```

### Required vs Optional

Clearly distinguish required and optional fields:

```markdown
#### Required Fields
- `email` - User's email address
- `password` - Minimum 8 characters

#### Optional Fields
- `name` - Display name (defaults to email prefix)
- `avatar_url` - Profile picture URL
```

## Response Documentation

### Success Response Fields

Document every field in the response:

```markdown
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (format: `usr_[a-z0-9]{10}`) |
| email | string | User's email address |
| name | string | Display name |
| status | string | Account status: `active`, `pending`, `suspended` |
| created_at | string | ISO 8601 timestamp of account creation |
| updated_at | string | ISO 8601 timestamp of last update |
```

### Error Response Format

Document error response structure:

```markdown
### Error Response Format

All errors return this structure:

```json
{
  "error": "error_code",
  "message": "Human-readable description",
  "details": [
    {
      "field": "field_name",
      "message": "Specific field error"
    }
  ],
  "request_id": "req_abc123"
}
```

| Field | Type | Description |
|-------|------|-------------|
| error | string | Machine-readable error code |
| message | string | Human-readable error message |
| details | array | Field-specific errors (for validation) |
| request_id | string | Request ID for support |
```

### Common Error Codes

```markdown
| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| bad_request | 400 | Malformed request syntax |
| unauthorized | 401 | Missing or invalid auth |
| forbidden | 403 | Valid auth but no permission |
| not_found | 404 | Resource doesn't exist |
| conflict | 409 | Resource state conflict |
| validation_error | 422 | Invalid field values |
| rate_limited | 429 | Too many requests |
| internal_error | 500 | Server error |
```

## Pagination Documentation

### Standard Pagination

```markdown
### Pagination

All list endpoints support pagination:

#### Query Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (starts at 1) |
| per_page | integer | 20 | Items per page (max: 100) |

#### Response Meta
```json
{
  "data": [...],
  "meta": {
    "total": 150,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  },
  "links": {
    "self": "/orders?page=1",
    "next": "/orders?page=2",
    "last": "/orders?page=8"
  }
}
```
```

### Cursor Pagination

```markdown
### Cursor Pagination

For large datasets, cursor pagination is recommended:

#### Query Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| cursor | string | Cursor from previous response |
| limit | integer | Items to return (max: 100) |

#### Response
```json
{
  "data": [...],
  "cursor": {
    "next": "eyJpZCI6MTAwfQ==",
    "has_more": true
  }
}
```

Use `cursor.next` in subsequent requests until `has_more` is false.
```

## Rate Limiting Documentation

```markdown
### Rate Limits

| Plan | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 60 | 1,000 |
| Pro | 600 | 50,000 |
| Enterprise | Custom | Custom |

#### Rate Limit Headers
| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | Maximum requests per window |
| X-RateLimit-Remaining | Remaining requests in window |
| X-RateLimit-Reset | Unix timestamp when window resets |

#### Rate Limit Response (429)
```json
{
  "error": "rate_limited",
  "message": "Too many requests",
  "retry_after": 30
}
```
```

## Versioning Documentation

```markdown
### API Versioning

The API version is specified in the URL path:

```
https://api.example.com/v1/orders
https://api.example.com/v2/orders
```

#### Version Lifecycle
| Version | Status | Sunset Date |
|---------|--------|-------------|
| v2 | Current | - |
| v1 | Deprecated | 2024-12-31 |

#### Deprecation Notices
Deprecated endpoints return a `Deprecation` header:

```
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```
```
