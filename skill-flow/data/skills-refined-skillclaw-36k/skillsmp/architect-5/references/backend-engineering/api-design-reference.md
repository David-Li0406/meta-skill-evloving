# API Design Reference

## REST API Design

### Resource Naming
- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural nouns: `/users` not `/user`
- Use lowercase with hyphens: `/order-items` not `/orderItems`
- Limit nesting: max 2-3 levels

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Update resource | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes

**Success:**
- 200 OK - Successful GET/PUT/PATCH
- 201 Created - Successful POST
- 204 No Content - Successful DELETE

**Client Errors:**
- 400 Bad Request - Malformed request
- 401 Unauthorized - Auth required
- 403 Forbidden - Auth failed
- 404 Not Found - Resource missing
- 422 Unprocessable Entity - Validation failed
- 429 Too Many Requests - Rate limited

**Server Errors:**
- 500 Internal Server Error
- 503 Service Unavailable

### Response Format

**Success:**
```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Error:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [
      {"field": "email", "message": "Invalid format"}
    ]
  }
}
```

### Pagination

**Offset-based:**
```
GET /users?limit=20&offset=40
```

**Cursor-based:**
```
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ
```

### Versioning

**URL path (recommended):**
```
/api/v1/users
```

## GraphQL Design

### Schema Design
- Use nullable by default, add `!` only when guaranteed
- Use Connection pattern for pagination
- Create dedicated input types for mutations
- Return payload types with errors

### Example Schema
```graphql
type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

### N+1 Prevention
Use DataLoader to batch database queries:
```javascript
const userLoader = new DataLoader(ids => db.users.findByIds(ids));
```

## Database Design

### Normalization Guidelines
- 1NF: Atomic values, no repeating groups
- 2NF: No partial dependencies
- 3NF: No transitive dependencies

### When to Denormalize
- Read-heavy workloads
- Complex joins hurting performance
- Data rarely changes

### Indexing Rules
- Always index foreign keys
- Index columns in WHERE, JOIN, ORDER BY
- Consider composite indexes for multi-column queries
- Don't over-index (slows writes)

### Query Optimization
- Use EXPLAIN ANALYZE to understand query plans
- Avoid SELECT * - list needed columns
- Paginate large result sets
- Use connection pooling

## Security

### Authentication
- Use standard protocols (OAuth2, OIDC)
- Short-lived access tokens (15 min)
- Secure refresh token storage (httpOnly cookies)
- Validate all tokens server-side

### Authorization
- Check permissions on every request
- Implement at API layer, not just UI
- Use role-based (RBAC) or attribute-based (ABAC)
- Audit authorization decisions

### Input Validation
- Validate type, format, range
- Sanitize for output context (SQL, HTML)
- Never trust client-side validation
- Use parameterized queries (prevent SQL injection)

### Rate Limiting
- Implement per-user/API key limits
- Return 429 with Retry-After header
- Use token bucket or sliding window
- Consider tiered limits by plan

## Error Handling

### Error Response Structure
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 123 not found",
    "details": {},
    "request_id": "req_abc123"
  }
}
```

### Error Codes
Define application-specific codes:
- VALIDATION_ERROR
- RESOURCE_NOT_FOUND
- RESOURCE_EXISTS
- UNAUTHORIZED
- FORBIDDEN
- RATE_LIMITED
- INTERNAL_ERROR

### Logging
- Log all errors with stack traces
- Include request ID for correlation
- Never log sensitive data (passwords, tokens)
- Structure logs for searchability

## Caching

### HTTP Caching
```
Cache-Control: public, max-age=300
ETag: "abc123"
```

### Application Caching
- Cache expensive computations
- Cache database queries
- Use appropriate TTL
- Implement cache invalidation

### Caching Strategy
- Cache-aside: App manages cache
- Read-through: Cache manages reads
- Write-through: Cache manages writes
- Write-behind: Async cache writes
