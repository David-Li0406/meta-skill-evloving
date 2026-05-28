---
name: api-design
description: Use this skill when designing robust, consistent RESTful APIs that adhere to best practices for usability, versioning, and documentation.
---

# Skill: API Design

## Overview

Design robust, maintainable, and user-friendly RESTful APIs following best practices.

## 1. RESTful Conventions

### Resource Naming
- Use plural nouns for resources (e.g., `/users`, `/posts`).
- Use verbs for actions only when necessary (e.g., `/auth/login`).

### HTTP Methods
| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| GET    | /users | List all users | 200 + array |
| GET    | /users/:id | Get specific user | 200 / 404 |
| POST   | /users | Create user | 201 + created |
| PUT    | /users/:id | Replace user | 200 / 404 |
| PATCH  | /users/:id | Update user | 200 / 404 |
| DELETE | /users/:id | Delete user | 204 / 404 |

### Nested Resources
- Example: 
  - `GET /users/:userId/orders` - Get user's orders
  - `POST /users/:userId/orders` - Create order for user

## 2. Versioning Strategies
- **URL Path**: `/api/v1/users` (most common, clear)
- **Header**: `Accept: application/vnd.api+json;version=1` (clean URLs)
- **Query**: `/users?version=1` (simple but messy)

## 3. Response Format

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
  }
}
```

## 4. HTTP Status Codes
| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | No/invalid auth |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (e.g., duplicate email) |
| 422 | Unprocessable | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Server unavailable |

## 5. Documentation
- Provide OpenAPI/Swagger specs.
- Include request/response examples.
- Document error codes and meanings.
- Keep documentation updated with changes.