---
name: api-design
description: Use this skill when designing RESTful APIs and GraphQL services, focusing on best practices for endpoints, HTTP methods, and response structures.
---

# API Design Skill

## REST Design Principles

### Resource Naming
- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural for collections: `/users`, `/orders`
- Use kebab-case: `/user-profiles`
- Nest for relationships: `/users/{id}/orders`
- Maximum 3 levels deep

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes

```
2xx Success
  200 OK - General success
  201 Created - Resource created (return Location header)
  204 No Content - Success with no body (DELETE)

4xx Client Error
  400 Bad Request - Invalid input
  401 Unauthorized - Authentication required
  403 Forbidden - Authenticated but not permitted
  404 Not Found - Resource doesn't exist
  409 Conflict - State conflict (duplicate)
  422 Unprocessable Entity - Validation failed
  429 Too Many Requests - Rate limited

5xx Server Error
  500 Internal Server Error - Unexpected failure
  502 Bad Gateway - Upstream failure
  503 Service Unavailable - Temporary unavailability
```

### Response Structure

```json
// Success (single resource)
{
  "data": { "id": "<id>", "name": "<name>" },
  "meta": { "requestId": "<requestId>" }
}

// Success (collection)
{
  "data": [{ "id": "<id1>" }, { "id": "<id2>" }],
  "meta": { "total": <total>, "page": <page>, "perPage": <perPage> }
}

// Error
{
  "error": {
    "code": "<errorCode>",
    "message": "<errorMessage>",
    "details": [
      { "field": "<fieldName>", "message": "<errorDetail>" }
    ]
  }
}
```

### Pagination

```
# Offset-based (simple, not scalable)
GET /users?page=<page>&per_page=<perPage>

# Cursor-based (scalable, recommended)
GET /users?cursor=<cursor>&limit=<limit>
```

### Filtering & Sorting

```
# Filtering
GET /users?status=<status>&role=<role>

# Sorting
GET /users?sort=<field>:<order>

# Field selection
GET /users?fields=<field1>,<field2>
```

### Versioning

```
# URL versioning (recommended)
GET /v1/users

# Header versioning
Accept: application/vnd.api+json; version=<version>
```

## GraphQL Best Practices

### Schema Design
- Use specific types over generic ones
- Prefer nullable fields (explicit over implicit)
- Use enums for fixed sets
- Add descriptions to all types

### Query Patterns
```graphql
# Good: Specific query
query GetUserOrders($userId: ID!, $limit: Int = 10) {
  user(id: $userId) {
    orders(first: $limit) {
      edges {
        node { id, total, status }
      }
      pageInfo { hasNextPage, endCursor }
    }
  }
}
```

### Mutation Patterns
```graphql
# Good: Input types and payloads
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user { id, name }
    errors { field, message }
  }
}
```

## Rate Limiting

```
# Response headers
X-RateLimit-Limit: <limit>
X-RateLimit-Remaining: <remaining>
X-RateLimit-Reset: <resetTime>
Retry-After: <retryAfter>
```

## Authentication

- Use Bearer tokens in Authorization header
- Short-lived access tokens (15 min)
- Long-lived refresh tokens (7-30 days)
- Never pass tokens in URLs