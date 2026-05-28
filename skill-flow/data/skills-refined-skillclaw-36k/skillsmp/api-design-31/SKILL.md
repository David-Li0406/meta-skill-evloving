---
name: api-design
description: "REST/GraphQL API design patterns, error handling, and versioning. Use when designing APIs, handling errors, or making API architecture decisions."
---

# API Design Patterns

## Overview

Decision guide for API design focusing on REST patterns, error handling, and consistent responses.

## REST Resource Design

### URL Structure

```
# Resources (nouns, plural)
GET    /users           # List users
POST   /users           # Create user
GET    /users/:id       # Get user
PATCH  /users/:id       # Update user
DELETE /users/:id       # Delete user

# Nested resources
GET    /users/:id/posts         # User's posts
POST   /users/:id/posts         # Create post for user

# Actions (when CRUD doesn't fit)
POST   /users/:id/verify        # Trigger verification
POST   /orders/:id/cancel       # Cancel order
```

### HTTP Methods

| Method | Purpose | Idempotent | Request Body |
|--------|---------|------------|--------------|
| GET | Read | Yes | No |
| POST | Create | No | Yes |
| PUT | Replace | Yes | Yes |
| PATCH | Update | Yes | Yes |
| DELETE | Remove | Yes | No |

## Response Structure

### Success Response

```typescript
// Single resource
{
  "data": { "id": "123", "name": "John" },
  "success": true
}

// Collection with pagination
{
  "data": [{ "id": "123" }, { "id": "456" }],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  },
  "success": true
}
```

### Error Response

```typescript
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": {
      "field": "email",
      "constraint": "required"
    }
  },
  "success": false
}
```

## Status Codes

| Code | When to Use |
|------|-------------|
| 200 | Success (GET, PATCH) |
| 201 | Created (POST) |
| 204 | No content (DELETE) |
| 400 | Bad request (validation) |
| 401 | Unauthorized (no auth) |
| 403 | Forbidden (no permission) |
| 404 | Not found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable (business logic) |
| 429 | Rate limited |
| 500 | Server error |

## Error Handling Pattern

```typescript
// lib/api-error.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
  }
}

// Error handler
export function handleError(error: unknown): Response {
  if (error instanceof ApiError) {
    return Response.json(
      { error: { code: error.code, message: error.message }, success: false },
      { status: error.statusCode }
    );
  }

  console.error('Unhandled:', error);
  return Response.json(
    { error: { code: 'INTERNAL_ERROR', message: 'Unexpected error' }, success: false },
    { status: 500 }
  );
}

// Usage
throw new ApiError(404, 'User not found', 'NOT_FOUND', { userId });
```

## Pagination Patterns

```typescript
// Offset pagination (simple, skip/limit)
GET /users?page=2&pageSize=20

// Cursor pagination (for large datasets)
GET /users?cursor=abc123&limit=20

// Implementation
async function paginate<T>(query: Query, page: number, pageSize: number) {
  const [items, total] = await Promise.all([
    query.skip((page - 1) * pageSize).take(pageSize).findMany(),
    query.count(),
  ]);

  return {
    data: items,
    pagination: { page, pageSize, total, totalPages: Math.ceil(total / pageSize) },
  };
}
```

## Validation Pattern

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).default('user'),
});

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = createUserSchema.parse(body);
    const user = await db.user.create({ data });
    return Response.json({ data: user, success: true }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: error.errors,
        },
        success: false,
      }, { status: 422 });
    }
    return handleError(error);
  }
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Verbs in URLs | `/getUser`, `/createUser` | Use HTTP methods |
| Inconsistent responses | Hard to parse | Standardize structure |
| Exposing internal errors | Security risk | Generic client messages |
| No validation | Crashes, security | Validate all input |
| Status 200 for errors | Breaks clients | Use appropriate codes |

## Rate Limiting

```typescript
// Headers to include
{
  'X-RateLimit-Limit': '100',
  'X-RateLimit-Remaining': '95',
  'X-RateLimit-Reset': '1609459200'
}

// 429 response
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests",
    "details": { "retryAfter": 60 }
  }
}
```

## Red Flags

- Different response shapes for success vs error
- Status 200 with `{ "error": true }`
- Internal error messages exposed to client
- No input validation
- Pagination without total count
- No rate limiting on public APIs

## Quick Reference

```typescript
// Standard error codes
const ErrorCode = {
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  CONFLICT: 'CONFLICT',
  RATE_LIMITED: 'RATE_LIMITED',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
} as const;

// Always return consistent shape
return Response.json({ data, success: true });
return Response.json({ error: { code, message }, success: false });
```
