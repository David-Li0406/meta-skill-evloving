# API Design Patterns

## REST Conventions

```
GET    /resources          → List (paginated)
GET    /resources/:id      → Get one
POST   /resources          → Create
PUT    /resources/:id      → Full update
PATCH  /resources/:id      → Partial update
DELETE /resources/:id      → Delete
```

### Response Codes

| Code | When |
|------|------|
| 200 | Success with body |
| 201 | Created (return created resource + Location header) |
| 204 | Success, no body (DELETE) |
| 400 | Validation error (return field errors) |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Unprocessable (valid syntax, invalid semantics) |
| 429 | Rate limited |
| 500 | Server error (log details, return generic message) |

### Pagination

```json
GET /users?page=2&per_page=20

{
  "data": [...],
  "meta": {
    "page": 2,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### Filtering & Sorting

```
GET /products?status=active&category=electronics
GET /products?sort=-created_at,name    # - prefix = descending
```

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {"field": "email", "message": "Invalid email format"},
      {"field": "age", "message": "Must be positive"}
    ]
  }
}
```

## GraphQL Patterns

```graphql
type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

# Relay-style pagination
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}
```

### N+1 Prevention

Use DataLoader pattern:

```
# Instead of: fetch user → fetch posts (N queries)
# Do: batch user IDs → single query for all posts
```

## Versioning

```
# URL versioning (simplest)
/api/v1/users
/api/v2/users

# Header versioning
Accept: application/vnd.api+json; version=2
```

## Rate Limiting Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
Retry-After: 60  # on 429
```
