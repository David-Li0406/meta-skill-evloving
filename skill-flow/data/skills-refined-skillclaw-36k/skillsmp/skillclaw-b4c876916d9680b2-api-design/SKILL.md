---
name: api-design
description: Use this skill when designing, reviewing, or implementing RESTful and GraphQL APIs to ensure best practices and clear documentation.
---

# Skill body

## Core Concepts

### API Design Principles
- RESTful architecture
- Resource-oriented design
- Uniform interface
- Statelessness
- Cacheability
- Layered system

### API Styles
- REST (Representational State Transfer)
- GraphQL
- RPC (Remote Procedure Call)
- WebSocket
- Server-Sent Events (SSE)
- gRPC

### Key Considerations
- Versioning strategies
- Authentication and authorization
- Rate limiting
- Error handling
- Documentation
- Backward compatibility

## REST API Design Patterns

### Resource Naming
- Use nouns for resources (e.g., `/api/v1/users`).
- Avoid verbs in URLs (e.g., `/getUsers`).

### HTTP Methods
| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET    | Read    | Yes        | Yes  |
| POST   | Create  | No         | No   |
| PUT    | Replace | Yes        | No   |
| PATCH  | Update  | Yes        | No   |
| DELETE | Remove  | Yes        | No   |

### Response Codes
- **Success**: 
  - `200 OK` for successful GET, PUT, PATCH
  - `201 Created` for successful POST
  - `204 No Content` for successful DELETE
- **Client Errors**: 
  - `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Entity`
- **Server Errors**: 
  - `500 Internal Server Error`, `503 Service Unavailable`

### Standard Response Format
- **Success Response**:
  ```json
  {
    "data": {
      "id": "123",
      "type": "user",
      "attributes": {
        "name": "Frank",
        "email": "frank@frankx.ai"
      }
    },
    "meta": {
      "timestamp": "2026-01-23T12:00:00Z"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Email is required",
      "details": [
        { "field": "email", "message": "Required field" }
      ]
    }
  }
  ```

## API Documentation
- Create OpenAPI specifications.
- Document endpoints, request/response schemas, and provide examples.
- Include error handling documentation and versioning strategies.

## Example: RESTful API Design
1. **Analyze Requirements**: Understand use cases and identify resources.
2. **Design Resource Model**: Identify resources and relationships.
3. **Design Endpoints**: Create RESTful endpoints and request/response formats.
4. **Add Authentication**: Design authentication flow and authorization rules.
5. **Document API**: Write OpenAPI specifications and document endpoints.

This skill provides a comprehensive framework for designing robust, scalable APIs that adhere to industry best practices for both REST and GraphQL.