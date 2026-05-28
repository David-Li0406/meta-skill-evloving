---
id: api-rest-design
name: "REST API Design"
domain: API
skill: faion-software-developer
category: "api-design"
---

## REST API Design

### Problem

APIs without consistent design lead to confusion, integration failures, and maintenance nightmares.

### Framework

**Resource-Oriented Design:**

```
/users                  # Collection
/users/{id}             # Singleton
/users/{id}/orders      # Sub-collection
/users/{id}/orders/{id} # Nested singleton
```

**HTTP Methods:**

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

**Standard Patterns:**

```
GET    /users              # List all users
GET    /users?status=active&limit=10  # Filtered list
GET    /users/{id}         # Get single user
POST   /users              # Create user
PUT    /users/{id}         # Replace user
PATCH  /users/{id}         # Update user fields
DELETE /users/{id}         # Delete user
```

**Status Codes:**

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate/state conflict |
| 422 | Unprocessable Entity | Semantic validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server failure |
| 503 | Service Unavailable | Maintenance/overload |

### HATEOAS (Hypermedia)

```json
{
  "id": "123",
  "name": "John Doe",
  "_links": {
    "self": { "href": "/users/123" },
    "orders": { "href": "/users/123/orders" },
    "update": { "href": "/users/123", "method": "PATCH" }
  }
}
```

### Best Practices

- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural names: `/users` not `/user`
- Use lowercase: `/user-profiles` not `/UserProfiles`
- Use hyphens for readability: `/user-profiles` not `/user_profiles`
- Nest for relationships: `/users/{id}/orders` for user's orders
- Use query params for filtering: `?status=active&sort=-created_at`
- Include `Location` header for 201 responses
- Return created/updated resource in response body

### Agent

faion-api-agent
