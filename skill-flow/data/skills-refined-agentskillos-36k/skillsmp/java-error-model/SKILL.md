---
name: java-error-model
description: Standardize API error responses using RFC 9457 Problem Details, stable error codes, and deterministic mapping rules. Use when clients struggle to handle errors, error payloads are inconsistent, or you need a consistent contract across services.
license: MIT
compatibility: JDK 17+ (recommended 21), any HTTP stack (Servlet/JAX-RS/Spring/Vert.x/Netty), OpenAPI 3.0+ or 3.1
metadata:
  owner: platform
  version: "1.0"
  tags: [java, api, rest, errors, rfc9457, openapi]
---

# Java Error Model (Problem Details + Error Codes)

## Scope

**In scope**

- A single, consistent error envelope for all non-2xx HTTP responses.
- RFC 9457 Problem Details (`application/problem+json`) payload shape.
- Stable `errorCode` taxonomy + mapping to HTTP status.
- Validation errors shape (field-level issues).
- Correlation identifiers to support support/debugging (e.g., `traceId`, `requestId`).
- OpenAPI components for error schemas + examples.
- Test strategy: contract tests + unit tests for mapping determinism.

**Out of scope**

- Business-specific domain modeling (handled by service/domain design).
- UI error rendering rules (client-specific).
- Security policy design (authn/authz is separate; we only define error outputs).

## Why this exists (core idea)

If every endpoint returns a different error payload, clients must implement brittle, per-endpoint logic. A stable error contract turns errors into a **first-class API surface**: machine-readable, consistent, and testable.

## Requirements (non-negotiable)

1. Every non-2xx response body MUST be a Problem Details object (RFC 9457) unless the endpoint explicitly documents otherwise.
2. `errorCode` MUST be present and stable across releases.
3. Human message MUST be helpful but MUST NOT leak secrets/PII.
4. Mapping from server exceptions -> HTTP status + `errorCode` MUST be deterministic and covered by tests.
5. Include at least one correlation identifier:
   - Prefer `traceId` if tracing exists; otherwise `requestId`.
6. Validation errors MUST include field-level details.

## Standard Error Envelope (Problem Details + extensions)

Content-Type:

- `application/problem+json` for JSON APIs.
- `application/problem+xml` if you support XML (optional).

Minimum payload:

- `type` (URI string identifying the problem type)
- `title` (short, human-readable summary)
- `status` (HTTP status code)
- `detail` (human-readable explanation; safe)
- `instance` (URI of the request; optional but helpful)

Recommended extensions (company-defined):

- `errorCode` (string, stable, machine-readable)
- `traceId` (string; from tracing context if available)
- `requestId` (string; if you have one; can match gateway ID)
- `timestamp` (ISO-8601)
- `errors` (array; for validation/multi-issue failures)
- `retryable` (boolean; indicates safe-to-retry semantics)
- `service` (string; service name)
- `path` (string; request path)

### Example: Generic server error (500)

```json
{
  "type": "https://errors.example.com/problems/internal",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "Unexpected error occurred. Please contact support if it persists.",
  "instance": "/v1/orders/123",
  "errorCode": "INTERNAL_ERROR",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "timestamp": "2026-01-20T16:20:00Z",
  "service": "orders",
  "retryable": false
}
```

# Example: Validation error (400) with field issues

```json
{
  "type": "https://errors.example.com/problems/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Request validation failed.",
  "instance": "/v1/orders",
  "errorCode": "VALIDATION_FAILED",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "timestamp": "2026-01-20T16:21:00Z",
  "errors": [
    { "field": "customerId", "reason": "must not be blank", "code": "NotBlank" },
    { "field": "items[0].quantity", "reason": "must be >= 1", "code": "Min" }
  ],
  "retryable": false
}
```

## ErrorCode taxonomy (recommendation)

### Principles

- Codes are **semantic**, not exception-class-based.
- Prefer a small stable set; avoid per-endpoint bespoke codes.
- Use UPPER_SNAKE_CASE and keep them stable.

### Suggested baseline catalog

**Client errors (4xx)**

- `VALIDATION_FAILED` (400)
- `MALFORMED_REQUEST` (400)
- `UNAUTHENTICATED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `CONFLICT` (409)
- `PRECONDITION_FAILED` (412)
- `RATE_LIMITED` (429)
- `UNSUPPORTED_MEDIA_TYPE` (415)

**Server / dependency errors (5xx)**

- `INTERNAL_ERROR` (500)
- `NOT_IMPLEMENTED` (501)
- `BAD_GATEWAY` (502)
- `SERVICE_UNAVAILABLE` (503)
- `GATEWAY_TIMEOUT` (504)
- `DEPENDENCY_FAILURE` (502/503; choose consistently)

## Mapping rules (Exception -> HTTP status + Problem)

### Deterministic mapping table (example)

- Validation exception -> 400 / `VALIDATION_FAILED`
- JSON parse error -> 400 / `MALFORMED_REQUEST`
- Auth required -> 401 / `UNAUTHENTICATED`
- Authz denied -> 403 / `FORBIDDEN`
- Resource missing -> 404 / `NOT_FOUND`
- Unique constraint / optimistic lock -> 409 / `CONFLICT`
- Throttled -> 429 / `RATE_LIMITED` (and include `Retry-After` header)
- Downstream timeout -> 504 / `GATEWAY_TIMEOUT`
- Downstream unavailable -> 503 / `SERVICE_UNAVAILABLE`
- Everything else -> 500 / `INTERNAL_ERROR`

### Retry semantics

- `retryable=true` only when the client can safely retry without side effects.
- Prefer deriving this from known conditions:
  - 503/504 are often retryable.
  - 409 is usually NOT retryable unless you provide guidance.

## Transport-level details (headers)

- Always include `Content-Type: application/problem+json`.
- For tracing/correlation:
  - If using W3C Trace Context, propagate `traceparent` downstream.
  - Optionally echo `traceId` in `X-Trace-Id` header (org choice).
- For 429, include `Retry-After`.

## Implementation notes (Java, framework-agnostic)

### Core components (recommendation)

1. `ErrorCatalog`: mapping from `errorCode` -> `type`, `title`, `defaultStatus`.
2. `ProblemFactory`: build problem payload, attach safe `detail`, extensions.
3. `ExceptionMapper` / `GlobalErrorHandler`: catch exceptions, call mapping, return response.
4. `CorrelationProvider`: retrieves `traceId` (from tracing) or generates `requestId`.
5. `Sanitizer`: redacts secrets/PII from messages and stack traces.

### Pseudocode sketch

- On exception:
  - classify -> `ErrorDescriptor(status, errorCode, type, title)`
  - build Problem object
  - attach correlation fields
  - attach validation `errors` if applicable
  - return response

## OpenAPI contract (recommended)

- Define components:
  - `ProblemDetails`
  - `ValidationProblemDetails`
- Every operation references:
  - `default` response: `ProblemDetails`
  - 400: `ValidationProblemDetails`
  - 401/403/404/409/429: `ProblemDetails` with examples

## Testing strategy (must-have)

1. **Contract test**: validate error response schema for representative failures.
2. **Mapping test**: each exception classification returns expected (status, errorCode).
3. **Safety test**: ensure no secrets/PII appear in `detail` or extensions.
4. **Golden examples**: store example payloads and compare snapshots.

## Definition of Done (DoD)

- [ ]  All non-2xx endpoints return `application/problem+json`.
- [ ]  Error mapping table implemented and covered by unit tests.
- [ ]  Validation errors include field-level `errors[]`.
- [ ]  Correlation identifier present in responses (traceId/requestId).
- [ ]  OpenAPI updated with error schemas + examples.
- [ ]  Security review: ensure safe messages, no stack traces to clients.

## Guardrails (What NOT to do)

- Never return raw stack traces to clients.
- Never embed secrets, credentials, tokens, or full PII in `detail`.
- Avoid per-endpoint unique payload shapes.
- Avoid changing `errorCode` once published (treat as a breaking change).

## Common failure modes & fixes

- Symptom: clients cannot parse errors -> Fix: enforce `application/problem+json` everywhere.
- Symptom: inconsistent statuses -> Fix: centralize mapping; add mapping tests.
- Symptom: “helpful” detail leaks data -> Fix: sanitizer + safety tests; keep detail generic.

## References (see references/)

- `references/problem-details.md`
- `references/error-catalog-template.yml`
- `references/openapi-components.yml`
- `references/testing-checklist.md`
