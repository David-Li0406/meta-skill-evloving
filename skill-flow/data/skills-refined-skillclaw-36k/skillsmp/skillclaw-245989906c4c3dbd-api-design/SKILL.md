---
name: api-design
description: Use this skill when you need to design, review, and document APIs, ensuring they follow best practices and are properly versioned.
---

# Skill body

## API Design Philosophy

This skill answers five critical questions:

| Question | Deliverable |
|----------|-------------|
| **What does this API do?** | Clear purpose, resource definition |
| **How should it be used?** | Request/response examples, error handling |
| **Is it consistent?** | Naming conventions, patterns alignment |
| **Is it documented?** | OpenAPI spec, usage examples |
| **Will it break clients?** | Versioning strategy, deprecation plan |

## Coverage Scope

| API Type | Coverage Level | Notes |
|----------|---------------|-------|
| REST API | Full | Primary focus, complete templates |
| GraphQL | Partial | Schema design principles only, Resolver implementation is out of scope |
| gRPC | Out of scope | Protocol Buffers require separate expertise |
| WebSocket | Partial | Event design, message format |

## API DESIGN PRINCIPLES

### RESTful Design Checklist

| Principle | Check | Example |
|-----------|-------|---------|
| **Resource-oriented** | URLs represent nouns, not verbs | `/users`, not `/getUsers` |
| **HTTP methods** | Use correct verbs | GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove) |
| **Plural resources** | Collections use plural | `/users`, `/orders` |
| **Nested resources** | Show relationships | `/users/{id}/orders` |
| **Query parameters** | For filtering/sorting | `?status=active&sort=created_at` |
| **Consistent naming** | camelCase or snake_case | Pick one, stick to it |
| **HTTP status codes** | Meaningful responses | 200, 201, 400, 401, 403, 404, 500 |

### URL Design Patterns

```
# Good patterns
GET    /api/v1/users              # List users
POST   /api/v1/users              # Create user
GET    /api/v1/users/{id}         # Get user
PUT    /api/v1/users/{id}         # Replace user
PATCH  /api/v1/users/{id}         # Update user
DELETE /api/v1/users/{id}         # Delete user
```

This skill consolidates the principles and practices of API design, ensuring quality and consistency across REST and GraphQL APIs.