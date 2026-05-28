---
name: api-design
description:
  Design clean, consistent REST and GraphQL APIs. Use this skill when creating API endpoints,
  defining request/response schemas, handling errors, or versioning APIs. Covers REST conventions,
  status codes, pagination, and API documentation.
---

# API Design Best Practices

This skill provides guidance for designing clean, consistent, and developer-friendly APIs.

## When This Skill Applies

- Creating new API endpoints
- Defining request/response schemas
- Handling API errors
- Implementing pagination
- Versioning APIs
- Documenting APIs

## REST API Conventions

### URL Structure

```
GET    /users          # List users
POST   /users          # Create user
GET    /users/:id      # Get user
PUT    /users/:id      # Replace user
PATCH  /users/:id      # Update user
DELETE /users/:id      # Delete user

# Nested resources
GET    /users/:id/posts        # User's posts
POST   /users/:id/posts        # Create post for user

# Actions (when CRUD doesn't fit)
POST   /users/:id/verify       # Trigger verification
POST   /orders/:id/cancel      # Cancel order
```

### Naming Rules

- Use **nouns**, not verbs (`/users` not `/getUsers`)
- Use **plural** nouns (`/users` not `/user`)
- Use **kebab-case** for multi-word resources (`/user-profiles`)
- Use **lowercase** only
- Avoid deep nesting (max 2 levels)

### HTTP Methods

| Method | Purpose | Idempotent | Request Body |
| ------ | ------- | ---------- | ------------ |
| GET    | Read    | Yes        | No           |
| POST   | Create  | No         | Yes          |
| PUT    | Replace | Yes        | Yes          |
| PATCH  | Update  | Yes        | Yes          |
| DELETE | Delete  | Yes        | No           |

## HTTP Status Codes

### Success (2xx)

| Code | When to Use                  |
| ---- | ---------------------------- |
| 200  | Success with response body   |
| 201  | Resource created             |
| 204  | Success, no content (DELETE) |

### Client Errors (4xx)

| Code | When to Use                           |
| ---- | ------------------------------------- |
| 400  | Bad request (invalid syntax)          |
| 401  | Unauthorized (not authenticated)      |
| 403  | Forbidden (authenticated, no access)  |
| 404  | Resource not found                    |
| 409  | Conflict (e.g., duplicate)            |
| 422  | Validation error (semantically wrong) |
| 429  | Too many requests (rate limited)      |

### Server Errors (5xx)

| Code | When to Use           |
| ---- | --------------------- |
| 500  | Internal server error |
| 502  | Bad gateway           |
| 503  | Service unavailable   |
| 504  | Gateway timeout       |

## Request/Response Design

### Request Body

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "admin"
}
```

**Rules:**

- Use camelCase for field names
- Keep flat when possible
- Use ISO 8601 for dates (`2024-01-15T10:30:00Z`)
- Use enums for fixed values

### Response Body

```json
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

**Rules:**

- Include `id` in responses
- Include timestamps (`createdAt`, `updatedAt`)
- Use consistent field naming across endpoints
- Don't expose internal IDs if using UUIDs

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body is invalid",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

**Include:**

- Machine-readable error code
- Human-readable message
- Field-level details for validation errors
- Request ID for debugging (optional)

### Error Response Examples

**Validation Error (422):**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "age", "message": "Must be at least 18" }
    ]
  }
}
```

**Not Found (404):**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

## Pagination

### Offset-Based (Simple)

```
GET /users?limit=20&offset=40
```

Response:

```json
{
  "data": [...],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 40
  }
}
```

### Cursor-Based (Scalable)

```
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ
```

Response:

```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}
```

**Use cursor-based for:**

- Large datasets
- Real-time data (items added/removed frequently)
- Infinite scroll UIs

## Filtering, Sorting, and Fields

### Filtering

```
GET /users?status=active&role=admin
GET /orders?createdAt[gte]=2024-01-01
```

### Sorting

```
GET /users?sort=createdAt        # Ascending
GET /users?sort=-createdAt       # Descending
GET /users?sort=lastName,firstName
```

### Field Selection

```
GET /users?fields=id,name,email
```

## Versioning

### URL Path (Recommended)

```
GET /v1/users
GET /v2/users
```

**Pros:** Clear, easy to route, cacheable **Cons:** URL changes on version bump

### Header-Based

```
GET /users
Accept: application/vnd.api+json; version=2
```

**Pros:** Clean URLs **Cons:** Harder to test, less visible

## Authentication

### API Keys

```
Authorization: Bearer <api-key>
# or
X-API-Key: <api-key>
```

Use for: Server-to-server, simple integrations

### JWT (OAuth 2.0)

```
Authorization: Bearer <jwt-token>
```

Use for: User authentication, mobile apps

## Rate Limiting

Include headers in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

Return 429 when exceeded:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
```

## Documentation

Every endpoint should document:

1. **URL and method**
2. **Description** of what it does
3. **Authentication** required
4. **Request parameters** (path, query, body)
5. **Response format** with examples
6. **Error responses** possible
7. **Rate limits** if applicable

Use OpenAPI/Swagger for auto-generated docs.

## API Design Checklist

- [ ] Consistent URL naming (plural, kebab-case)
- [ ] Appropriate HTTP methods
- [ ] Correct status codes
- [ ] Consistent error format
- [ ] Pagination for lists
- [ ] Authentication documented
- [ ] Rate limiting implemented
- [ ] Versioning strategy defined
- [ ] Request validation
- [ ] Response examples in docs
