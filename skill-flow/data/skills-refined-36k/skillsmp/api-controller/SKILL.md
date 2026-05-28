---
name: api-controller
description: Generate REST controller with full OpenAPI documentation, authentication decorators, and auto-translated error responses. Use when creating HTTP endpoints or exposing CRUD via REST API.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# API Controller

## Purpose

Generate a REST controller with full OpenAPI/Swagger documentation including API tags, operation summaries, response schemas, authentication decorators, and auto-translated error responses.

## When to Use

- Creating HTTP endpoints for features
- Adding new routes to existing controllers
- Generating Swagger documentation
- Exposing CRUD operations via REST API

## What It Generates

```
apps/api/src/modules/{feature}/{feature}.controller.ts
```

## Patterns Enforced

### OpenAPI Documentation

- `@ApiTags()` decorator for grouping endpoints
- `@ApiOperation()` with summary and description
- `@ApiResponse()` for all possible status codes
- `@ApiBearerAuth()` for protected endpoints
- `@ApiProperty()` on all DTO fields

### HTTP Status Codes

- `200 OK` - Successful GET
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing/invalid auth
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate/resource conflict
- `500 Internal Server Error` - Server errors

### Consistent Response Format

```typescript
{
  data?: T;
  error?: {
    code: string;
    message: string;
    locale?: string; // Auto-translated based on Accept-Language
    details?: any;
  };
}
```

### Error Responses with Auto-Translation

All error responses are automatically translated based on the request locale:

```typescript
// English (default)
{
  "error": {
    "code": "USER_001",
    "message": "User with ID 123 not found",
    "locale": "en"
  }
}

// Spanish (via Accept-Language: es)
{
  "error": {
    "code": "USER_001",
    "message": "Usuario con ID 123 no encontrado",
    "locale": "es"
  }
}
```

Auto-translation is handled by `GlobalExceptionFilter` using the `error.translated` getter.

## Usage Example

```bash
/skill api-controller --name=Product --operations='create,update,delete,getList,getOne'
```

## Related Files

- [Feature CQRS](../feature-cqrs/SKILL.md) - Complete CQRS feature with controller
- [API DTO](../api-dto/SKILL.md) - DTOs for request/response
