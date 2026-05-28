---
name: api-design
description: Use this skill when designing REST or GraphQL APIs, defining endpoints, implementing pagination/filtering, handling API versioning, or establishing API documentation with OpenAPI/Swagger.
---

# API Design

RESTful and GraphQL API design patterns for building robust backend services. This skill covers best practices for API design, including principles, versioning, error handling, and documentation.

## Core Concepts

### API Design Principles
- Resources as nouns, actions as HTTP methods.
- Use plural nouns for collections (e.g., `/users`).
- Avoid verbs in URLs (e.g., use `/users` instead of `/getUsers`).
- Maintain consistent casing (e.g., lowercase, hyphens).

### HTTP Methods
| Method | Purpose | Idempotent | Example |
|--------|---------|------------|---------|
| GET    | Read    | Yes        | `GET /users/123` |
| POST   | Create  | No         | `POST /users` |
| PUT    | Replace | Yes        | `PUT /users/123` |
| PATCH  | Update  | Yes        | `PATCH /users/123` |
| DELETE | Remove  | Yes        | `DELETE /users/123` |

### Status Codes
| Code | Meaning | Usage |
|------|---------|-------|
| 200  | OK      | Successful GET/PUT/PATCH |
| 201  | Created | Successful POST |
| 204  | No Content | Successful DELETE |
| 400  | Bad Request | Validation error |
| 401  | Unauthorized | Missing/invalid auth |
| 403  | Forbidden | Insufficient permissions |
| 404  | Not Found | Resource doesn't exist |
| 409  | Conflict | Duplicate/conflict |
| 422  | Unprocessable | Semantic error |
| 500  | Server Error | Unexpected error |

## Pagination
### Offset Pagination
```
GET /users?page=2&pageSize=20
```
```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "page": 2,
    "pageSize": 20,
    "totalPages": 5
  }
}
```

### Cursor Pagination
```
GET /users?cursor=abc123&limit=20
```
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "def456",
    "prevCursor": "xyz789",
    "hasMore": true
  }
}
```

## Versioning
### URL Versioning (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
GET /users
Accept: application/vnd.api+json; version=2
```

## Error Handling
### Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## API Documentation
### OpenAPI (Swagger)
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

## Best Practices
- Use consistent naming conventions and response formats.
- Document error codes and messages clearly.
- Implement rate limiting to prevent abuse.
- Support filtering, sorting, and pagination in API responses.

## Anti-Patterns
- Using GET for state-changing operations.
- Returning inconsistent response formats.
- No versioning strategy.
- Breaking changes without versioning.

## Resources
- REST API Design Best Practices: https://restfulapi.net/
- OpenAPI Specification: https://swagger.io/specification/
- API Design Guide: https://cloud.google.com/apis/design
- Microsoft REST API Guidelines: https://github.com/microsoft/api-guidelines
- FastAPI: https://fastapi.tiangolo.com/