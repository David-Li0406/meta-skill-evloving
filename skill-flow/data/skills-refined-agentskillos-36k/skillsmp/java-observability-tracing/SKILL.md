---
name: java-observability-tracing
description: Implement distributed tracing with OpenTelemetry (context propagation, sampling, semantic conventions, span design) and integrate with logs/metrics. Use when debugging microservices latency, dependency failures, or request flow across async boundaries.
license: MIT
compatibility: JDK 17+ (recommended 21), OpenTelemetry SDK/agent, OTLP exporter, W3C Trace Context
metadata:
  owner: platform
  version: "1.0"
  tags: [java, opentelemetry, tracing, tracecontext, sampling, semconv]
---

# Java Observability Tracing (OpenTelemetry + Propagation + Sampling)

## Scope

**In scope**

- OpenTelemetry tracing setup (SDK or auto-instrumentation agent).
- Context propagation across services (W3C Trace Context, baggage policy).
- Span naming + attributes using semantic conventions (HTTP, DB, messaging).
- Sampling strategies that balance cost vs visibility.
- Correlation with logs (traceId/spanId) and metrics.

**Out of scope**

- Vendor-specific tracing UI configuration.
- Full service topology governance.

## Core mental model

Tracing answers: “Where did time go?” and “Which dependency caused failure?”  
A trace is a tree/graph of spans. Each span represents a unit of work and captures timing, attributes, and events.

## Propagation (must-have)

### Standard propagation: W3C Trace Context

- Use `traceparent` and `tracestate` headers for cross-service propagation.
- Ensure outbound HTTP and messaging producers inject propagation headers.
- Ensure inbound handlers extract propagation headers.

### Baggage policy

- Use baggage sparingly: it propagates everywhere and can increase cost.
- Never put secrets/PII in baggage.
- Define an allowlist of baggage keys if you enable it.

## Instrumentation approach (recommended default)

### Option A: Auto-instrumentation first

- Use the OpenTelemetry Java agent for fast baseline coverage:
  - inbound HTTP server spans
  - outbound HTTP client spans
  - common libraries (JDBC, messaging)
Pros: fastest adoption, fewer code changes.  
Cons: may need manual spans for domain-specific operations.

### Option B: Manual instrumentation for key domains

- Add explicit spans for:
  - business workflows
  - critical background jobs
  - complex async pipelines
- Use semantic attributes and stable span names.

## Span design rules

### Span naming

- Use low-cardinality names:
  - `HTTP GET /v1/orders/{id}`
  - `DB SELECT orders`
  - `MQ consume orders.created`
- Avoid embedding IDs in span names.

### Attributes (tagging)

- Use semantic conventions where available.
- Keep attributes bounded; avoid IDs in attributes unless necessary and approved.

### Events and errors

- Record exceptions as span events (but do not leak secrets).
- Use `status` to represent error outcome.

## Sampling strategy (cost vs value)

### Default recommended: Parent-based + TraceIdRatio

- Keep sampling consistent across services.
- Start with a low rate in prod (e.g., 1% to 10%), increase during incidents.
- Always sample errors if your system supports tail sampling (advanced).

### Operational knobs

- Support runtime configuration for sampling (env-based).
- Document how to temporarily increase sampling for debugging.

## Export and resource identity

- Export via OTLP (HTTP/gRPC) to your collector/backend.
- Set resource attributes:
  - `service.name`, `service.version`, `deployment.environment`.
These must be consistent across services to enable cross-service queries.

## Correlation with logs

- Inject `traceId` and `spanId` into logs:
  - via MDC or OpenTelemetry-aware logging appenders.
- This enables “logs <-> traces” pivoting during incidents.

## Key spans map (template)

A minimal “span map” for a typical backend request:

1. Inbound HTTP span:
   - name: `HTTP <method> <route>`
2. Authentication/authorization span (optional, internal):
   - name: `auth.verify`
3. DB span:
   - name: `DB <operation> <table>`
4. Outbound dependency call span:
   - name: `HTTP <method> <upstream>`
5. Business workflow span:
   - name: `orders.create` (manual)
6. Response finalize span events:
   - errors, retries, timeouts as span events

## Testing and validation

- Smoke test: confirm traces exported in staging.
- Propagation test: multi-service request produces a single trace.
- Attribute linting: reject forbidden high-cardinality attributes.
- Performance check: ensure overhead acceptable at target sampling rate.

## Outputs / artifacts

- `docs/tracing.md` (propagation, sampling, span naming)
- `observability/span-naming.md`
- `observability/attribute-policy.md`
- Code changes:
  - OTel agent config or SDK bootstrap
  - manual spans in critical workflows
  - log correlation integration
- Tests:
  - propagation tests
  - policy tests for forbidden attributes

## Definition of Done (DoD)

- [ ] Inbound and outbound requests generate spans.
- [ ] W3C propagation works across services.
- [ ] Sampling configured and documented.
- [ ] Resource identity set consistently.
- [ ] Logs include traceId/spanId for correlation.
- [ ] Attribute policy prevents cardinality/security issues.

## Guardrails (What NOT to do)

- Never propagate secrets/PII via baggage or attributes.
- Avoid high-cardinality attributes (IDs, full URLs, raw payloads).
- Do not create a span for every tiny function (noise and overhead).
- Avoid inconsistent sampling across services.

## Common failure modes & fixes

- Symptom: broken traces across services -> Fix: ensure `traceparent` extraction/injection on all hops.
- Symptom: tracing cost too high -> Fix: reduce sampling; tighten attribute policy; focus manual spans.
- Symptom: cannot find root cause -> Fix: add manual spans for domain workflows; record key events.

## References (see references/)

- `references/w3c-trace-context.md`
- `references/w3c-baggage-policy.md`
- `references/otel-java-agent.md`
- `references/otel-semconv-http.md`
- `references/sampling-playbook.md`
