---
name: api-design
description: Use this skill when designing REST or GraphQL APIs, creating OpenAPI specifications, or planning API architecture, including resource modeling and error handling.
---

# API Design Patterns

## Overview

This skill provides patterns and guidelines for designing robust RESTful and GraphQL APIs, ensuring they are scalable, developer-friendly, and well-documented.

## When to Use This Skill

- Designing new REST or GraphQL APIs
- Creating OpenAPI specifications
- Modeling resources and relationships
- Implementing API versioning strategies
- Designing pagination and filtering
- Standardizing error responses
- Planning authentication flows
- Documenting API contracts

## Core Workflow

1. **Analyze Domain**: Understand business requirements, data models, and client needs.
2. **Model Resources**: Identify resources, relationships, and operations.
3. **Design Endpoints**: Define URI patterns, HTTP methods, and request/response schemas.
4. **Specify Contract**: Create OpenAPI 3.1 specification with complete documentation.
5. **Plan Evolution**: Design versioning, deprecation, and backward compatibility strategies.

## REST API Design

### Resource Naming

| Pattern | Example | Description |
|---------|---------|-------------|
| Plural nouns | `/users`, `/orders` | Collections |
| Nested resources | `/users/{id}/orders` | Sub-resources |
| No verbs in URLs | `/users` not `/getUsers` | Actions via HTTP methods |
| Lowercase, hyphens | `/order-items` | Consistent casing |

### HTTP Methods

| Method | Purpose | Idempotent | Example |
|--------|---------|------------|---------|
| GET | Read | Yes | `GET /users/123` |
| POST | Create | No | `POST /users` |
| PUT | Replace | Yes | `PUT /users/123` |
| PATCH | Update | Yes | `PATCH /users/123` |
| DELETE | Remove | Yes | `DELETE /users/123` |

### Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate/conflict |
| 422 | Unprocessable | Semantic error |
| 500 | Server Error | Unexpected error |

### Request/Response Format

```json
// Successful response
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "requestId": "req_abc123"
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "requestId": "req_abc123"
  }
}

// List response
{
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "pageSize": 20,
    "totalPages": 5
  }
}
```

## Pagination

### Offset Pagination

```
GET /users?page=2&pageSize=20
```

### Error Handling

- Design proper error responses with clear messages and status codes.
- Follow standards such as RFC 7807 for error response formats.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| REST Patterns | `references/rest-patterns.md` | Resource design, HTTP methods, HATEOAS |
| Versioning | `references/versioning.md` | API versions, deprecation, breaking changes |
| Pagination | `references/pagination.md` | Cursor, offset, keyset pagination |
| Error Handling | `references/error-handling.md` | Error responses, status codes |
| OpenAPI | `references/openapi.md` | OpenAPI 3.1, documentation, code generation |

## Constraints

### MUST DO
- Follow REST principles (resource-oriented, proper HTTP methods).
- Use consistent naming conventions (snake_case or camelCase).
- Include comprehensive OpenAPI 3.1 specification.
- Design proper error responses with a clear structure.