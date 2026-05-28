# Error Handling (AIP-193, AIP-194)

## Linter Rules

The following rules automatically check error handling:

| Rule ID                       | Severity   | What It Checks                                                                |
| ----------------------------- | ---------- | ----------------------------------------------------------------------------- |
| `aip193/schema-defined`       | warning    | Error schema exists in `components/schemas`                                   |
| `aip193/responses-documented` | suggestion | Operations have documented error responses                                    |
| `aip193/standard-codes`       | suggestion | Uses standard HTTP status codes (400, 401, 403, 404, 409, 422, 429, 500, 503) |

To skip a rule: `aip-review spec.yaml --skip-rules aip193/standard-codes`

## Standard Error Response Schema

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "details": [
      {
        "description": "Invalid email format",
        "field": "email",
        "type": "field_violation"
      }
    ],
    "message": "Human-readable error message",
    "request_id": "req_abc123"
  }
}
```

## Error Codes

Use consistent error codes that map to HTTP status:

| Code                  | HTTP | When to Use                                    |
| --------------------- | ---- | ---------------------------------------------- |
| `INVALID_ARGUMENT`    | 400  | Client sent invalid data                       |
| `FAILED_PRECONDITION` | 400  | Request valid but system not in required state |
| `OUT_OF_RANGE`        | 400  | Value outside acceptable range                 |
| `UNAUTHENTICATED`     | 401  | Missing or invalid credentials                 |
| `PERMISSION_DENIED`   | 403  | Valid credentials but insufficient permissions |
| `NOT_FOUND`           | 404  | Resource doesn't exist                         |
| `CONFLICT`            | 409  | Resource already exists or version conflict    |
| `RESOURCE_EXHAUSTED`  | 429  | Rate limit or quota exceeded                   |
| `CANCELLED`           | 499  | Client cancelled the request                   |
| `INTERNAL`            | 500  | Unexpected server error                        |
| `NOT_IMPLEMENTED`     | 501  | Method not supported                           |
| `UNAVAILABLE`         | 503  | Service temporarily unavailable                |
| `DEADLINE_EXCEEDED`   | 504  | Operation timed out                            |

## OpenAPI Schema Definition

```yaml
components:
  schemas:
    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
              enum: [INVALID_ARGUMENT, FAILED_PRECONDITION, ...]
            message:
              type: string
              description: Human-readable, localized message
            details:
              type: array
              items:
                $ref: '#/components/schemas/ErrorDetail'
            request_id:
              type: string
              description: Unique identifier for tracing

    ErrorDetail:
      type: object
      properties:
        type:
          type: string
          enum: [field_violation, quota_failure, precondition_failure]
        field:
          type: string
          description: JSONPath to problematic field
        description:
          type: string
```

## Field Violations

For validation errors, include specific field violations:

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "details": [
      {
        "description": "Must be greater than 0",
        "field": "$.order.items[0].quantity",
        "type": "field_violation"
      },
      {
        "description": "Invalid postal code format for country US",
        "field": "$.order.shipping_address.postal_code",
        "type": "field_violation"
      }
    ],
    "message": "Request contains invalid fields"
  }
}
```

## Retryable Errors (AIP-194)

Indicate retry guidance in response headers:

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 30
X-Retry-Reason: upstream_timeout
```

Retryable error codes:

- `UNAVAILABLE` - Always retry with backoff
- `RESOURCE_EXHAUSTED` - Retry after `Retry-After` duration
- `DEADLINE_EXCEEDED` - May retry, operation might have succeeded
- `INTERNAL` - May retry with backoff, but investigate

Non-retryable (client must fix):

- `INVALID_ARGUMENT`
- `FAILED_PRECONDITION`
- `PERMISSION_DENIED`
- `NOT_FOUND`

## NestJS Implementation

```typescript
// error.filter.ts
@Catch()
export class ApiExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const { status, error } = this.mapException(exception);

    response.status(status).json({
      error: {
        ...error,
        request_id: request.headers['x-request-id'] || uuid(),
      },
    });
  }

  private mapException(exception: unknown): {
    status: number;
    error: ApiError;
  } {
    if (exception instanceof BadRequestException) {
      return {
        status: 400,
        error: {
          code: 'INVALID_ARGUMENT',
          message: exception.message,
          details: this.extractValidationErrors(exception),
        },
      };
    }
    // ... map other exceptions
  }
}
```

## Fastify Implementation

```typescript
// error-handler.ts
fastify.setErrorHandler((error, request, reply) => {
  const apiError = mapToApiError(error);

  reply.status(apiError.status).send({
    error: {
      code: apiError.code,
      message: apiError.message,
      details: apiError.details,
      request_id: request.id,
    },
  });
});
```

## Common Mistakes

❌ **Leaking internal details**

```json
{ "error": "NullPointerException at UserService.java:142" }
```

✅ **User-actionable message**

```json
{
  "error": {
    "code": "INTERNAL",
    "message": "An unexpected error occurred. Please try again.",
    "request_id": "req_abc123"
  }
}
```

❌ **Generic 500 for everything**

✅ **Semantic status codes** - 400 for bad input, 404 for missing, etc.

❌ **Different error shapes per endpoint**

✅ **Consistent schema across all endpoints**
