---
name: nestjs-observability
description: Use this skill for implementing structured logging and metrics monitoring in NestJS applications.
---

# Observability Standards

## Structured Logging

- **Standard**: Use `nestjs-pino` for high-performance JSON logging.
  - **Why**: Node's built-in `console.log` is blocking and unstructured.
- **Configuration**:
  - **Redaction**: Mandatory masking of sensitive fields (`password`, `token`, `email`).
  - **Context**: Always inject `Logger` and set the context (e.g., `LoginService`).

## Tracing (Correlation)

- **Request ID**: Every log line **must** include a `reqId` (Request ID).
  - `nestjs-pino` handles this automatically using `AsyncLocalStorage`.
  - **Propagation**: Pass `x-request-id` to downstream microservices/database queries to trace flows.

## Metrics

- **Exposure**: Use `@willsoto/nestjs-prometheus` to expose `/metrics` for Prometheus scraping.
- **Key Metrics**:
  1. `http_request_duration_seconds` (Histogram)
  2. `db_query_duration_seconds` (Histogram)
  3. `memory_usage_bytes` (Gauge)

## Health Checks

- **Terminus**: Implement explicit logic for "Liveness" (I'm alive) vs "Readiness" (I can take traffic).
  - **DB Check**: Use `TypeOrmHealthIndicator` or `PrismaHealthIndicator`.
  - **Memory Check**: Fail if Heap > 300MB (to prevent crash loops).