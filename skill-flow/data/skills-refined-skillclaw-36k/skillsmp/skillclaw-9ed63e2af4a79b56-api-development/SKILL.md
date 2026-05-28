---
name: api-development
description: Use this skill when designing RESTful APIs, including creating endpoints, handling requests/responses, and implementing best practices for API structure and error handling.
---

# Skill body

## Overview

This skill provides best practices and design patterns for developing RESTful APIs. It covers endpoint creation, request/response handling, error responses, pagination, and versioning.

## When to Use

- Creating API endpoints
- Designing REST API structures
- Implementing backend routing
- Handling requests and responses
- Managing API versioning

## RESTful Design Principles

### URL Design

- **Resource Naming**: Use plural nouns for collections.
  ```
  GET    /api/v1/users           # Get user list
  GET    /api/v1/users/:id       # Get a single user
  POST   /api/v1/users           # Create a user
  PUT    /api/v1/users/:id       # Update a user (full replacement)
  PATCH  /api/v1/users/:id       # Update a user (partial update)
  DELETE /api/v1/users/:id       # Delete a user
  ```

- **Nested Resources**:
  ```
  GET    /api/v1/users/:id/orders           # User's orders
  GET    /api/v1/users/:id/orders/:orderId  # Specific order
  ```

### HTTP Method Semantics

| Method   | Description   | Idempotent | Safe |
|----------|---------------|------------|------|
| GET      | Retrieve data | ✅         | ✅   |
| POST     | Create data   | ❌         | ❌   |
| PUT      | Update data   | ✅         | ❌   |
| PATCH    | Partially update data | ❌   | ❌   |
| DELETE   | Remove data   | ✅         | ❌   |

### Unified Response Format

#### Success Response

```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```

#### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "age", "message": "Age must be greater than 0" }
    ]
  }
}
```

## API Versioning

- **Versioning in URL**: 
  ```
  /api/v1/users
  /api/v2/users
  ```

- **Version Strategy**:
  ```typescript
  // v1/routes.ts
  export async function v1Routes(app) {
    app.get('/users', getUsersV1);
    app.post('/users', createUserV1);
  }

  // v2/routes.ts
  export async function v2Routes(app) {
    app.get('/users', getUsersV2);  // Breaking change in response structure
    app.post('/users', createUserV2);
  }
  ```

## Additional References

- [Error Handling Best Practices](./references/error-responses.md)