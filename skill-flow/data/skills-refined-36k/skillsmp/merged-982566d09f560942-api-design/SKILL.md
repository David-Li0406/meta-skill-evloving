---
name: api-design
description: Design consistent, robust RESTful APIs with best practices for versioning, documentation, error handling, and security.
---

# API Design

Expert guidance for designing clean, consistent REST APIs.

## Overview

Design consistent, RESTful APIs with proper versioning, documentation, and error handling.

## REST Principles
- Use nouns for resources, verbs for actions.
- Follow HTTP method semantics (GET, POST, PUT, DELETE).
- Return appropriate status codes.
- Support content negotiation.

## URL Design
- Use plural nouns for collections (e.g., `/users`, `/posts`).
- Nest resources logically (e.g., `/users/123/posts`).
- Use query parameters for filtering and pagination.
- Keep URLs readable and predictable.

## Response Format
- Use consistent JSON structure.
- Include metadata for collections (total, page, etc.).
- Provide helpful error messages.
- Support partial responses when needed.

### Success Response
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "email": "user@example.com",
    "name": "John Doe"
  },
  "metadata": {
    "timestamp": "2026-01-06T12:00:00Z",
    "version": "1.0.0"
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "metadata": {
    "timestamp": "2026-01-06T12:00:00Z",
    "request_id": "abc-123"
  }
}
```

## Versioning
- Include version in URL or header.
- Maintain backward compatibility.
- Document breaking changes clearly.
- Deprecate gracefully with notice periods.

## Status Codes
| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | No/invalid auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource missing |
| 409 | Conflict | Duplicate/state conflict |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Unexpected error |

## Pagination
- Use offset-based or cursor-based pagination.
- Include pagination metadata in responses.

### Offset-based Example
```
GET /users?page=2&page_size=20
```

### Cursor-based Example
```
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
```

## Rate Limiting
- Implement rate limiting to control API usage.
- Use headers to communicate limits and remaining requests.

## Documentation
- Provide OpenAPI/Swagger specs.
- Include request/response examples.
- Document error codes and meanings.
- Keep documentation updated with changes.

## Best Practices
### Do's
- Use plural nouns for resources.
- Return created/updated resource.
- Include pagination metadata.
- Document with OpenAPI.
- Version from day one.

### Don'ts
- Use verbs in resource names.
- Return different formats per endpoint.
- Expose internal IDs/structures.
- Ignore backward compatibility.
- Skip error code standards.

---

**Version:** 1.0.0 | **Last Updated:** 2025-11-28