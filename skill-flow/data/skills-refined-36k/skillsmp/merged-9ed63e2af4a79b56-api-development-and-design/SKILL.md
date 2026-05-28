---
name: api-development-and-design
description: Use this skill when designing and developing RESTful APIs, including best practices for endpoints, error handling, pagination, and versioning.
---

# API Development and Design

This skill provides best practices and design patterns for creating RESTful APIs, focusing on consistent structure, error handling, resource patterns, and implementation strategies.

## When to Use

- Creating API endpoints
- Designing REST APIs
- Implementing backend routing
- Handling requests and responses
- Managing API versioning

## RESTful Design Principles

### URL Design

Use consistent, predictable URL patterns:

```
# Collection resources (plural nouns)
GET    /api/v1/users              # List users
POST   /api/v1/users              # Create user
GET    /api/v1/users/:id          # Get user
PUT    /api/v1/users/:id          # Update user (full)
PATCH  /api/v1/users/:id          # Update user (partial)
DELETE /api/v1/users/:id          # Delete user

# Nested resources
GET    /api/v1/users/:userId/posts          # List user's posts
POST   /api/v1/users/:userId/posts          # Create post for user
GET    /api/v1/users/:userId/posts/:postId  # Get specific post
```

### HTTP Method Semantics

| Method   | Semantics     | Idempotent | Safe |
| -------- | ------------- | ---------- | ---- |
| GET      | Read resource | ✅         | ✅   |
| POST     | Create resource | ❌       | ❌   |
| PUT      | Full update   | ✅         | ❌   |
| PATCH    | Partial update| ❌         | ❌   |
| DELETE   | Delete resource | ✅       | ❌   |

### Unified Response Format

#### Success Response

```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

#### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "age", "message": "Age must be greater than 0" }
    ]
  }
}
```

## API Versioning

Version APIs in the URL path:

```
/api/v1/users
/api/v2/users
```

### Version Control Implementation

```typescript
// v1/routes.ts
export async function v1Routes(app) {
  app.get('/users', getUsersV1);
  app.post('/users', createUserV1);
}

// v2/routes.ts
export async function v2Routes(app) {
  app.get('/users', getUsersV2);  // Breaking change in response structure
  app.post('/users', createUserV2);
}
```

## Pagination

Use cursor-based pagination for large datasets:

```typescript
// Request
GET /api/v1/posts?limit=20&cursor=pst_01h455vb4pex5vsknk084sn02q

// Response
{
  "items": [
    { "id": "pst_01h455w3x8k5z9y7q1m0n2b3c4", ... },
    { "id": "pst_01h455x2y9l6a0z8r2n1o3c5d6", ... }
  ],
  "nextCursor": "pst_01h455z1a0m7b8y9s3o2p4d6e7",
  "hasMore": true
}
```

## Error Handling

### RFC 7807 Problem Details

Standardized error response format:

```json
{
  "type": "NOT_FOUND",
  "status": 404,
  "title": "Not Found",
  "detail": "User with ID usr_01h455vb4pex5vsknk084sn02q not found",
  "instance": "/api/v1/users/usr_01h455vb4pex5vsknk084sn02q",
  "traceId": "req_abc123xyz"
}
```

### Best Practices

1. **Use plural nouns** - Collections should use plural resource names.
2. **Lowercase with hyphens** - Multi-word resources should be formatted with hyphens.
3. **Version in URL** - Use `/api/v1/`, `/api/v2/` for breaking changes.
4. **Standardized error responses** - Follow RFC 7807 for error handling.
5. **Cursor pagination** - Prefer cursor-based pagination for large datasets.
6. **Query parameters** - Use for filtering, sorting, and pagination.
7. **Consistent HTTP status codes** - Use appropriate status codes for responses.
8. **ISO 8601 timestamps** - Use `.toISOString()` for date formatting.
9. **Idempotency keys** - Implement for non-idempotent operations.
10. **Avoid unnecessary response envelopes** - Return resources directly unless pagination is needed.

## Implementation Examples

### Next.js API Route Example

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  // Implementation for fetching users
}

export async function POST(request: NextRequest) {
  // Implementation for creating a user
}
```

### FastAPI Example

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def list_users():
    # Implementation for listing users
```

### Express.js Example

```typescript
// routes/users.ts
import { Router } from "express";

const router = Router();

router.get("/", async (req, res) => {
  // Implementation for listing users
});
```

This skill provides a comprehensive guide for developing and designing RESTful APIs, ensuring best practices are followed for maintainability and consistency.