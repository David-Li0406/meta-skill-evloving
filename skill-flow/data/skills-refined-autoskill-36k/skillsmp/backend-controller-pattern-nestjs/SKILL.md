---
name: backend-controller-pattern-nestjs
description: Provides shared NestJS Controller patterns and principles. This skill should be used when implementing controllers in NestJS to ensure consistency and use of shared utilities.
---

# NestJS Controller Patterns (General)

This skill covers the **shared principles and common utilities** applicable to ALL controller types in `erify_api`.

## Specialized Patterns

For module-specific controller implementation, refer to:

- **[Admin Controllers](backend-controller-pattern-admin/SKILL.md)**: For `admin/*` endpoints (System Admins).
- **[User (Me) Controllers](backend-controller-pattern-me/SKILL.md)**: For `me/*` endpoints (Authenticated Users).
- **[Backdoor Controllers](backend-controller-pattern-backdoor/SKILL.md)**: For `backdoor/*` endpoints (Service-to-Service).
- **[Integration Controllers](backend-controller-pattern-integration/SKILL.md)**: For `google-sheets/*`, webhooks, etc.

## Shared Principles

The following patterns apply across all controller types.

### 1. Response Serialization

ALL endpoints must use Zod for response serialization to ensure no internal data (like database IDs) leaks.

- Use `@ZodResponse(Schema, Status)` for standard responses.
- Use `@ZodPaginatedResponse(Schema)` for list endpoints.

```typescript
@Get(':id')
@ZodResponse(UserDto)
async getUser(...)
```

### 2. Validation Pipes

Always use `UidValidationPipe` for validating `uid` parameters.

```typescript
@Param('id', new UidValidationPipe(UserService.UID_PREFIX, 'User'))
id: string
```

### 3. DTO Standards

- **Request DTOs**: Define validation rules using `zod`.
- **Response DTOs**: Define output shape, excluding sensitive fields.
- **Pagination**: Use `PaginationQueryDto` from `@/lib/pagination/pagination.schema`.

### 4. HTTP Status Codes

| Method   | Success Code   | Decorator Implementation                         |
| :------- | :------------- | :----------------------------------------------- |
| `GET`    | 200 OK         | Default / `@ZodResponse(S, HttpStatus.OK)`       |
| `POST`   | 201 Created    | `@ZodResponse(S, HttpStatus.CREATED)`            |
| `PATCH`  | 200 OK         | `@ZodResponse(S, HttpStatus.OK)`                 |
| `DELETE` | 204 No Content | `@ZodResponse(undefined, HttpStatus.NO_CONTENT)` |

## Checklist

- [ ] Choose the correct specialized pattern (`Admin`, `Me`, `Backdoor`, `Integration`).
- [ ] Use Zod serialization for ALL outputs.
- [ ] Use `UidValidationPipe` for all UIDs.
- [ ] Document all endpoints with Swagger/OpenAPI decorators (handled via `@ZodResponse` automatically where possible).
