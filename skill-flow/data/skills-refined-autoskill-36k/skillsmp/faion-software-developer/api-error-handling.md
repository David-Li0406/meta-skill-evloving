---
id: api-error-handling
name: "Error Handling"
domain: API
skill: faion-software-developer
category: "api-design"
---

## Error Handling

### Problem

Inconsistent error responses make debugging difficult. Need standardized error format.

### Framework

**RFC 7807 (Problem Details):**

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request body contains invalid fields",
  "instance": "/users/create",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address"
    },
    {
      "field": "age",
      "code": "out_of_range",
      "message": "Must be between 18 and 120"
    }
  ],
  "traceId": "abc-123-xyz"
}
```

**Error Response Schema:**

```yaml
components:
  schemas:
    ProblemDetail:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
          description: URI identifying the problem type
        title:
          type: string
          description: Short summary of the problem
        status:
          type: integer
          description: HTTP status code
        detail:
          type: string
          description: Detailed explanation
        instance:
          type: string
          format: uri
          description: URI of the specific occurrence
        traceId:
          type: string
          description: Request trace ID for debugging
        errors:
          type: array
          items:
            $ref: '#/components/schemas/FieldError'

    FieldError:
      type: object
      properties:
        field:
          type: string
        code:
          type: string
        message:
          type: string
```

### Error Codes

```python
class ErrorCode:
    # Client Errors (4xx)
    VALIDATION_ERROR = "validation_error"
    INVALID_FORMAT = "invalid_format"
    MISSING_FIELD = "missing_field"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    RATE_LIMITED = "rate_limited"

    # Server Errors (5xx)
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    TIMEOUT = "timeout"
```

### Implementation

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import uuid

class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    trace_id: str | None = None
    errors: list[dict] | None = None

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=ProblemDetail(
            type="https://api.example.com/errors/validation-error",
            title="Validation Error",
            status=400,
            detail="Request validation failed",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4()),
            errors=[
                {"field": e["loc"][-1], "code": e["type"], "message": e["msg"]}
                for e in exc.errors()
            ]
        ).model_dump()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the full exception for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content=ProblemDetail(
            type="https://api.example.com/errors/internal-error",
            title="Internal Server Error",
            status=500,
            detail="An unexpected error occurred",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4())
        ).model_dump()
    )
```

### Error Messages

| Type | Bad | Good |
|------|-----|------|
| Generic | "Error occurred" | "User not found with ID 'abc123'" |
| Technical | "NullPointerException" | "Required field 'email' is missing" |
| Actionable | "Invalid input" | "Email must be in format user@domain.com" |

### Best Practices

- Always include trace ID for debugging
- Use consistent error format across all endpoints
- Never expose internal errors to users
- Log detailed errors server-side
- Provide actionable error messages
- Document all error codes in API docs
- Include links to documentation in error type

### Agent

faion-api-agent
