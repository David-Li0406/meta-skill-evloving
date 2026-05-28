---
title: "API Documentation Patterns"
description: "Standard structure and formatting patterns for API endpoint documentation"
skill: writing-ai-docs
type: reference
created: 2025-10-28
lastUpdated: 2025-10-28
---

# API Documentation Patterns

## Standard API Endpoint Structure

For API endpoints, use extreme consistency:

````markdown
---
title: POST /api/v2/users
type: api-endpoint
method: POST
endpoint: /api/v2/users
---

## POST /api/v2/users

Create a new user account.

### Request

**Endpoint:** `POST https://api.example.com/v2/users`

**Headers:**
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Body Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | User email address |
| `name` | string | Yes | Full name |
| `role` | string | No | User role (default: "user") |

**Example Request:**

```bash
curl -X POST https://api.example.com/v2/users \
  -H "Authorization: Bearer sk_test_..." \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

### Response

**Success Response (201 Created):**

```json
{
  "id": "usr_1234567",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid API key
- `409 Conflict`: User already exists

### Related Endpoints

- [GET /api/v2/users](/docs/api/get-users)
- [DELETE /api/v2/users/:id](/docs/api/delete-user)
````

## Key Pattern Elements

### Endpoint Frontmatter

Required fields for API endpoints:

```yaml
---
title: "POST /api/v2/users"
description: "Create a new user account with email and profile information"
type: api-endpoint
method: POST
endpoint: /api/v2/users
authentication: required | optional | none
category: api-reference
tags:
  - users
  - authentication
  - rest-api
status: published | draft | deprecated
version: "2.1.0"
created: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
---
```

### Request Section Structure

**Components:**

1. Endpoint URL with HTTP method
2. Required and optional headers (as table)
3. Body parameters (as table with type, required, description)
4. Complete example request (with curl and/or code)

**Headers table format:**

```markdown
| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | Yes | `Bearer YOUR_API_KEY` |
| `Content-Type` | Yes | `application/json` |
```

**Parameters table format:**

```markdown
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | User email address |
| `name` | string | Yes | Full name |
| `role` | string | No | User role (default: "user") |
```

### Response Section Structure

**Components:**

1. Success response with status code
2. Complete JSON example
3. Error responses with status codes
4. Explanation of each error case

**Format:**

```markdown
### Response

**Success Response (200 OK):**

```json
{
  "id": "usr_123",
  "email": "user@example.com"
}
```

**Error Responses:**

#### 401 Unauthorized

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid API key"
  }
}
```

**Cause**: API key is missing or invalid

**Solution**: Verify API key at dashboard
```

### Code Examples

**Always include:**

- curl example (primary)
- Language-specific example (JavaScript, Python, etc.)
- Complete, runnable code
- Expected output shown

**Example:**

```bash
# curl example
curl -X GET https://api.example.com/v2/users \
  -H "Authorization: Bearer sk_test_abc123"
```

```javascript
// JavaScript example
const response = await fetch('https://api.example.com/v2/users', {
  headers: {
    'Authorization': `Bearer ${apiKey}`
  }
});

const users = await response.json();
console.log('Users:', users);
```

### Related Endpoints Section

Link to conceptually related endpoints:

```markdown
### Related Endpoints

- [POST /api/v2/users](/docs/api/create-user) - Create a new user
- [GET /api/v2/users/:id](/docs/api/get-user) - Get specific user
- [DELETE /api/v2/users/:id](/docs/api/delete-user) - Delete a user
```

## Consistency Rules

### HTTP Methods

Use consistent method names:

- GET (not Get, get)
- POST (not Post, post)
- PUT (not Put, put)
- PATCH (not Patch, patch)
- DELETE (not Delete, delete)

### Status Codes

Always include status code with response type:

- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict
- 429 Too Many Requests
- 500 Internal Server Error

### Parameter Types

Use consistent type names:

- string (not String, str, text)
- number (not Number, int, integer, float)
- boolean (not Boolean, bool)
- array (not Array, list)
- object (not Object, dict, hash)

### Authentication Headers

Standard format:

```http
Authorization: Bearer YOUR_API_KEY
```

Not:

- `Authorization: YOUR_API_KEY`
- `X-API-Key: YOUR_API_KEY`
- `Token: YOUR_API_KEY`

Unless your API specifically uses different format.

## Quick Reference Checklist

Before publishing API documentation:

- [ ] Title format: `METHOD /endpoint/path`
- [ ] Frontmatter includes method and endpoint fields
- [ ] Request section includes endpoint URL
- [ ] Headers shown as table
- [ ] Parameters shown as table with type/required/description
- [ ] curl example included and tested
- [ ] Success response includes status code
- [ ] Error responses include status codes and explanations
- [ ] Related endpoints linked at bottom
- [ ] All code blocks have language tags
- [ ] Consistent terminology throughout

## Template Usage

Use the api-endpoint template:

```bash
python scripts/create_from_template.py api-endpoint docs/api/your-endpoint.md
```

This ensures all required sections and formatting are included.
