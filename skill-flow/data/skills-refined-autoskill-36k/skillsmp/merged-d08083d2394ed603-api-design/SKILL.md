---
name: api-design
description: Design clear, consistent, and maintainable RESTful APIs following industry best practices and conventions.
---

# API Design

## Purpose
Design robust, maintainable, and user-friendly REST APIs.

## When to Use
- Designing new API endpoints
- Refactoring existing APIs
- Creating integration interfaces
- Planning service-to-service communication

## Key Capabilities
1. **REST Principles** - Apply RESTful design patterns correctly.
2. **Resource Modeling** - Design clear resource hierarchies.
3. **Error Responses** - Define consistent error handling.
4. **Versioning** - Implement proper versioning strategies.
5. **Documentation** - Provide comprehensive API documentation.

## REST Principles
- Use nouns for resources, verbs for actions.
- Follow HTTP method semantics (GET, POST, PUT, DELETE).
- Return appropriate status codes.
- Support content negotiation.

## URL Design
- Use plural nouns for collections (e.g., `/users`, `/posts`).
- Nest resources logically (e.g., `/users/123/posts`).
- Use query parameters for filtering and pagination.
- Keep URLs readable and predictable.

## Response Format
- Use consistent JSON structure.
- Include metadata for collections (total, page, etc.).
- Provide helpful error messages.
- Support partial responses when needed.

### Success Response Example
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

### Error Response Example
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
  },
  "metadata": {
    "timestamp": "2026-01-06T12:00:00Z",
    "request_id": "abc-123"
  }
}
```

## Versioning
- Include version in URL or header.
- Maintain backward compatibility.
- Document breaking changes clearly.
- Deprecate gracefully with notice periods.

## Security
- Use HTTPS everywhere.
- Implement proper authentication.
- Validate all inputs.
- Rate limit API endpoints.
- Log security-relevant events.

## Documentation
- Provide OpenAPI/Swagger specs.
- Include request/response examples.
- Document error codes and meanings.
- Keep documentation updated with changes.

## Pagination
- Use offset-based or cursor-based pagination strategies.
- Include pagination metadata in responses.

## Rate Limiting
- Implement rate limiting to control API usage.
- Use headers to communicate rate limit status.

## Best Practices
- Use plural nouns for resources.
- Return created/updated resource in responses.
- Document with OpenAPI.
- Version from day one.
- Avoid using verbs in resource names.

## API Design Checklist
- [ ] RESTful resource naming
- [ ] Consistent response format
- [ ] Proper status codes
- [ ] Pagination for lists
- [ ] Error responses with codes
- [ ] Versioning strategy
- [ ] OpenAPI documentation
- [ ] Rate limiting headers