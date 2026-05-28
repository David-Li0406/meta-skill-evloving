---
name: api-design
description: Use this skill when designing REST or GraphQL APIs, creating OpenAPI specifications, or planning API architecture, including resource modeling, versioning strategies, pagination patterns, and error handling standards.
---

# API Design Patterns

## Overview

Design patterns for building robust RESTful and GraphQL APIs, focusing on scalability, developer-friendliness, and comprehensive documentation.

## Core Workflow

1. **Analyze Domain** - Understand business requirements, data models, and client needs.
2. **Model Resources** - Identify resources, relationships, and operations.
3. **Design Endpoints** - Define URI patterns, HTTP methods, and request/response schemas.
4. **Specify Contract** - Create OpenAPI 3.1 specifications with complete documentation.
5. **Plan Evolution** - Design versioning, deprecation, and backward compatibility strategies.

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

Better for large datasets and real-time data.

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

## Filtering and Sorting

### Query Parameters

```
GET /users?status=active&role=admin    # Filtering
GET /users?sort=name&order=asc         # Sorting
GET /users?fields=id,name,email        # Field selection
GET /users?search=john                 # Search
```

### Complex Filters

```
GET /orders?created_gte=2024-01-01&created_lte=2024-12-31
GET /products?price_min=10&price_max=100
GET /users?tags=premium,verified
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

## Authentication

### Bearer Token

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key

```
X-API-Key: your-api-key
// or in query param (less secure)
GET /users?api_key=your-api-key
```

## Rate Limiting

### Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

### 429 Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
```

## GraphQL Patterns

### Schema Design

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  orders: [Order!]!
}

type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: Pagination): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input UserFilter {
  status: UserStatus
  role: UserRole
  search: String
}

input Pagination {
  first: Int
  after: String
  last: Int
  before: String
}
```

### Error Handling

```graphql
type MutationResult {
  success: Boolean!
  errors: [Error!]
  user: User
}

type Error {
  code: String!
  message: String!
  field: String
}

type Mutation {
  createUser(input: CreateUserInput!): MutationResult!
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

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
```

## Best Practices

### 1. Consistency

- Same response format across all endpoints
- Consistent naming conventions
- Predictable behavior

### 2. Error Messages

- Clear, actionable messages
- Include error codes for programmatic handling
- Don't expose internal details

### 3. Idempotency

- Support idempotency keys for POST requests
- Safe to retry without side effects

```
POST /orders
Idempotency-Key: unique-request-id-123
```

### 4. HATEOAS (Hypermedia)

Include links to related resources:

```json
{
  "data": {
    "id": "123",
    "name": "John"
  },
  "links": {
    "self": "/users/123",
    "orders": "/users/123/orders"
  }
}
```

## Constraints

### MUST DO
- Follow REST principles (resource-oriented, proper HTTP methods)
- Use consistent naming conventions (snake_case or camelCase)
- Include comprehensive OpenAPI 3.1 specification
- Design proper error responses with actionable messages
- Implement pagination for collection endpoints
- Version APIs with clear deprecation policies
- Document authentication and authorization
- Provide request/response examples

### MUST NOT DO
- Use verbs in resource URIs (use `/users/{id}`, not `/getUser/{id}`)
- Return inconsistent response structures
- Skip error code documentation
- Ignore HTTP status code semantics
- Design APIs without versioning strategy
- Expose implementation details in API
- Create breaking changes without migration path
- Omit rate limiting considerations

## Knowledge Reference

REST architecture, OpenAPI 3.1, GraphQL, HTTP semantics, JSON:API, HATEOAS, OAuth 2.0, JWT, RFC 7807 Problem Details, API versioning patterns, pagination strategies, rate limiting, webhook design, SDK generation

## Related Skills

- **GraphQL Architect** - GraphQL-specific API design
- **FastAPI Expert** - Python API implementation
- **NestJS Expert** - TypeScript API implementation
- **Spring Boot Engineer** - Java API implementation
- **Security Reviewer** - API security assessment