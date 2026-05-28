---
name: java-logging-structured
description: Implement structured logging (JSON/logfmt), correlation IDs, and safe log policies (levels, redaction, sampling). Use when incident response is slow, tracing request flows is hard, or logs are inconsistent across services.
license: MIT
compatibility: JDK 17+ (recommended 21), SLF4J-compatible logging, any HTTP stack
metadata:
  owner: platform
  version: "1.0"
  tags: [java, logging, structured-logging, mdc, correlation, security]
---

# Java Structured Logging (JSON/logfmt + Correlation + Safety)

## Scope

**In scope**

- Structured log format: JSON (preferred) or logfmt.
- Field schema: consistent keys across services.
- Correlation: `traceId`, `spanId`, `requestId`, `correlationId`.
- Log levels policy, sampling, and noise control.
- Redaction rules for secrets/PII.
- Minimal integration patterns for HTTP entrypoints and background jobs.

**Out of scope**

- Choosing a vendor-specific logging pipeline (ELK/Datadog/etc).
- Full SIEM design.

## Goals

- Make logs queryable and joinable with metrics/traces.
- Make incident response faster by standardizing fields and policies.
- Prevent accidental leakage of secrets/PII.

## Format and schema

### Preferred format: JSON

Every log record should be a single JSON object with stable keys.

### Recommended baseline fields

- `timestamp` (ISO-8601)
- `level` (TRACE/DEBUG/INFO/WARN/ERROR)
- `logger` (class/category)
- `thread`
- `message`
- `service.name`
- `service.version`
- `deployment.environment` (dev/staging/prod)
- `traceId` (if tracing enabled)
- `spanId` (if tracing enabled)
- `requestId` (if available)
- `correlationId` (if you use a custom correlation id)
- `http.method`, `http.path`, `http.status` (for request logs)
- `event.name` (semantic event label; stable)
- `error.type`, `error.message` (safe), `error.stack` (internal-only, never to clients)

### Field stability rules

- Do not rename fields without migration plan.
- Prefer adding new fields rather than changing meaning.
- Avoid high-cardinality fields unless explicitly needed:
  - Never log raw user identifiers; hash or redact.
  - Never log full request/response bodies by default.

## Correlation strategy

### What identifiers to use

1. Prefer `traceId`/`spanId` (from tracing context).
2. Also include a `requestId` (gateway id or generated at ingress).
3. For async flows, propagate correlation through message headers:
   - include `traceparent` (W3C) and optional `correlationId`.

### How to implement (Java pattern)

- Use MDC (Mapped Diagnostic Context) to attach correlation fields per thread/request.
- At request entry:
  - extract incoming `traceparent` / `requestId` if present
  - otherwise generate `requestId`
  - set MDC keys: `traceId`, `spanId`, `requestId`
- Ensure MDC cleanup at request end.

### Async and thread hops

- MDC is thread-local by default. For executors:
  - wrap `Runnable/Callable` to copy MDC context
  - or use framework/otel context propagation when available.

## Logging policy (levels)

### Default guidance

- INFO: business milestones (state transitions), start/stop, essential events.
- WARN: recoverable anomalies, retries, degraded mode.
- ERROR: failures requiring attention, request failed.
- DEBUG/TRACE: development-only, guarded by config; never enable globally in prod.

### Anti-pattern: "log everything at INFO"

This creates noise, cost, and hides signals.

## Security and privacy

### Redaction rules (must-have)

- Redact credentials: Authorization headers, tokens, API keys.
- Redact secrets: passwords, private keys, session cookies.
- Redact or hash PII: email, phone, address, national id.
- Never log full JWTs; at most log token fingerprint (hash).

### Safe exception logging

- Log error class and sanitized message.
- Store full stack traces only in internal logs with restricted access, or sample them.

## Sampling and rate limiting

- For high-volume endpoints:
  - sample INFO request logs (e.g., 1%)
  - always keep WARN/ERROR
- Rate limit repetitive error logs to avoid log storms.

## Standard log events (recommended)

- `event.name=request.received`
- `event.name=request.completed`
- `event.name=dependency.call`
- `event.name=dependency.failed`
- `event.name=job.started`
- `event.name=job.completed`
- `event.name=security.auth.failed` (without leaking details)

## Outputs / artifacts

- `docs/logging.md` (schema + policies)
- `logging/log-schema.json` (optional JSON schema)
- `logging/redaction-rules.md`
- Code changes:
  - ingress filter/middleware for MDC
  - JSON encoder configuration
  - unit tests for redaction and MDC cleanup

## Definition of Done (DoD)

- [ ] Logs are structured (JSON/logfmt) and consistent.
- [ ] Correlation identifiers present for requests and background jobs.
- [ ] Redaction rules applied and tested.
- [ ] Sampling/rate-limiting strategy documented.
- [ ] No secret/PII leakage found in test logs.

## Guardrails (What NOT to do)

- Never log raw secrets or tokens.
- Never dump full request/response by default.
- Avoid unbounded string concatenation in hot paths (use lazy logging).
- Avoid logging in tight loops without rate limiting.

## Common failure modes & fixes

- Symptom: cannot correlate logs with traces -> Fix: include `traceId` and propagate context; add MDC.
- Symptom: log storms during incidents -> Fix: add sampling + rate limiting; reduce noisy INFO logs.
- Symptom: leaked secrets -> Fix: redaction filters; code review checklist; scanners.

## References (see references/)

- `references/owasp-logging-rules.md`
- `references/log-schema-fields.md`
- `references/mdc-propagation.md`
