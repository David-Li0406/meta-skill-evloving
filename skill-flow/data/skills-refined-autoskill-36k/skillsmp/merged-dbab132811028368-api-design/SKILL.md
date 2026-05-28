---
name: api-design
description: Use this skill when designing, reviewing, or implementing RESTful APIs to ensure consistency, clarity, and comprehensive documentation.
---

# API Design

Design clear, consistent, and developer-friendly REST APIs.

## When to use this skill

- When designing new APIs or reviewing existing API designs.
- When establishing API standards for a project or organization.
- When implementing RESTful API endpoints, route handlers, or controllers.
- When documenting APIs using OpenAPI/Swagger specifications.

## Core Principles

### 1. Resource-Oriented Design
Design around resources (nouns), not actions (verbs).

```
✅ GET  /users/123/orders     → Get user's orders
✅ POST /orders               → Create order

❌ GET  /getUserOrders?id=123 → Action in URL
❌ POST /createOrder          → Verb in URL
```

### 2. Predictable Patterns
Consistent URL structure, response format, and behavior.

```
✅ All collections: GET /resources
✅ All items: GET /resources/{id}
✅ All creates: POST /resources
✅ All updates: PUT/PATCH /resources/{id}
✅ All deletes: DELETE /resources/{id}
```

### 3. Clear Contracts
Explicit request/response schemas, documented errors.

```
✅ Documented required fields
✅ Consistent error format
✅ Versioned endpoints
✅ OpenAPI specification
```

### 4. Developer Experience
Easy to understand, use, and debug.

```
✅ Meaningful error messages
✅ Helpful examples
✅ Logical defaults
✅ Self-documenting responses
```

## Design Process

```
┌─────────────────────────────────────────────────────────────┐
│                     API DESIGN PROCESS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. RESOURCES         2. OPERATIONS       3. CONTRACTS      │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │ Identify    │  →  │ Define CRUD │  →  │ Request/    │   │
│  │ entities    │     │ + actions   │     │ Response    │   │
│  │ & relations │     │ + methods   │     │ schemas     │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                             │
│  4. ERRORS            5. DOCS             6. REVIEW         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │ Status codes│  →  │ OpenAPI     │  →  │ Consistency │   │
│  │ Error format│     │ Examples    │     │ Usability   │   │
│  │ Edge cases  │     │ Descriptions│     │ Security    │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## HTTP Methods and Status Codes

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| GET    | Read resource(s) | Yes | Yes | No |
| POST   | Create resource | No | No | Yes |
| PUT    | Replace resource | Yes | No | Yes |
| PATCH  | Partial update | Yes* | No | Yes |
| DELETE | Remove resource | Yes | No | No |

### Common Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200  | OK | Successful GET, PUT, PATCH |
| 201  | Created | Successful POST |
| 204  | No Content | Successful DELETE |
| 400  | Bad Request | Validation error |
| 401  | Unauthorized | Missing/invalid auth |
| 403  | Forbidden | Insufficient permissions |
| 404  | Not Found | Resource doesn't exist |
| 409  | Conflict | Duplicate, state conflict |
| 422  | Unprocessable | Semantic validation error |
| 429  | Too Many Requests | Rate limited |
| 500  | Server Error | Unexpected error |

## Request/Response Patterns

### Standard Response Format

#### Success Response

```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2024-01-15T10:30:00Z"
    },
    "relationships": {
      "orders": {
        "links": { "related": "/users/123/orders" }
      }
    }
  }
}
```

#### Error Response

```json
{
  "error": {
    "status": 400,
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ],
    "requestId": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## API Versioning

**Choose one strategy and apply consistently:**

- URL path versioning (recommended for simplicity):
```
/v1/users
/v2/users
```

- Header versioning (for cleaner URLs):
```
Accept: application/vnd.api.v1+json
```

## Rate Limiting

**Include rate limit headers:**

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

Return `429 Too Many Requests` when limit exceeded.

## Documentation

**Document each endpoint:**

- Purpose and use case
- Request parameters and body schema
- Response schema and status codes
- Authentication requirements
- Rate limits
- Example requests/responses

Use OpenAPI/Swagger for machine-readable documentation.

## Design Checklist

- [ ] Resources are nouns, not verbs
- [ ] Plural names for collections
- [ ] Consistent naming convention
- [ ] Logical nesting depth
- [ ] Clear relationship modeling
- [ ] Correct HTTP methods for each operation
- [ ] Consistent error format
- [ ] OpenAPI specification
- [ ] Rate limits documented

## Anti-Patterns

### ❌ Verbs in URLs
```
❌ POST /createUser
❌ GET /getUsers
```

### ❌ Inconsistent Naming
```
❌ GET /users, GET /Order
```

### ❌ Wrong Status Codes
```
❌ 200 for created resource (should be 201)
```

---

**References:**
- [references/endpoints.md](references/endpoints.md) — URL design, HTTP methods, resource modeling
- [references/requests-responses.md](references/requests-responses.md) — Request/response formats, headers, content types
- [references/status-codes.md](references/status-codes.md) — HTTP status codes, error handling patterns
- [references/pagination-filtering.md](references/pagination-filtering.md) — Pagination, filtering, sorting, searching
- [references/versioning.md](references/versioning.md) — API versioning strategies
- [references/openapi.md](references/openapi.md) — OpenAPI specification, documentation
- [references/security.md](references/security.md) — Authentication, authorization, rate limiting