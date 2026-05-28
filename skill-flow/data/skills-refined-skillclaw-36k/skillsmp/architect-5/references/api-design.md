# REST API Design Principles

Design APIs that are consistent, predictable, and developer-friendly.

## Resource Naming

```
# Good - Nouns, plural, hierarchical
GET    /users
GET    /users/123
GET    /users/123/orders
POST   /users
PUT    /users/123
DELETE /users/123

# Bad - Verbs, actions in URL
GET    /getUsers
POST   /createUser
GET    /getUserOrders?userId=123
```

## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

## Status Codes

```
# Success
200 OK              - Successful GET, PUT, PATCH
201 Created         - Successful POST (include Location header)
204 No Content      - Successful DELETE

# Client Errors
400 Bad Request     - Invalid syntax, validation failed
401 Unauthorized    - Authentication required
403 Forbidden       - Authenticated but not authorized
404 Not Found       - Resource doesn't exist
409 Conflict        - State conflict (duplicate, version mismatch)
422 Unprocessable   - Semantic errors in valid syntax

# Server Errors
500 Internal Error  - Unexpected server error
503 Service Unavailable - Temporary outage
```

## Request/Response Patterns

### Collection Response

```json
{
  "data": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "last": "/users?page=5"
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## Versioning

```
# URL versioning (recommended for breaking changes)
GET /v1/users
GET /v2/users

# Header versioning
Accept: application/vnd.api+json; version=1

# Query parameter (avoid)
GET /users?version=1
```

## Filtering, Sorting, Pagination

```
# Filtering
GET /users?status=active&role=admin

# Sorting (prefix with - for descending)
GET /users?sort=name,-created_at

# Pagination
GET /users?page=2&per_page=20
GET /users?offset=20&limit=20
GET /users?cursor=abc123
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Verbs in URLs | Not RESTful | Use nouns, HTTP methods |
| 200 for errors | Hides errors | Use proper status codes |
| No pagination | Performance issues | Always paginate collections |
| Inconsistent naming | Hard to use | Follow conventions |
| No versioning | Breaking changes break clients | Version from start |
