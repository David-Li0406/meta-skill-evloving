---
name: nestjs-api-standards
description: Use this skill for standardizing API responses, pagination, and error handling in NestJS applications.
---

# NestJS API Standards & Common Patterns

## **Priority: P1 (OPERATIONAL)**

Standardized API response patterns and common NestJS conventions.

## Generic Response Wrapper

- **Concept**: Standardize all successful API responses.
- **Implementation**: Use `TransformInterceptor` to wrap data in `{ statusCode, data, meta }`.

## Pagination Standards (Pro)

- **DTOs**: Use strict `PageOptionsDto` (page/take/order) and `PageDto<T>` (data/meta).
- **Swagger Logic**: Generics require `ApiExtraModels` and schema path resolution.
- **Reference**: See [Pagination Wrapper Implementation](references/pagination-wrapper.md) for the complete `ApiPaginatedResponse` decorator code.

## Custom Error Response

- **Standard Error Object**:

  ```typescript
  export class ApiErrorResponse {
    @ApiProperty()
    statusCode: number;

    @ApiProperty()
    message: string;

    @ApiProperty()
    error: string;

    @ApiProperty()
    timestamp: string;

    @ApiProperty()
    path: string;
  }
  ```

- **Docs**: Apply `@ApiBadRequestResponse({ type: ApiErrorResponse })` globally or per controller.