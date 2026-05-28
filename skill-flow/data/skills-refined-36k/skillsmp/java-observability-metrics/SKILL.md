---
name: java-observability-metrics
description: Design and implement service metrics (counters, gauges, timers, histograms) with strict label/cardinality rules and SLO-ready signals. Use when adding KPIs/SLOs, building dashboards, or preventing metrics cardinality incidents.
license: MIT
compatibility: JDK 17+ (recommended 21), Prometheus/OpenTelemetry-compatible metrics systems, any framework
metadata:
  owner: platform
  version: "1.0"
  tags: [java, observability, metrics, prometheus, micrometer, cardinality, slo]
---

# Java Observability Metrics (Design + Cardinality + SLO Readiness)

## Scope

**In scope**

- Metric taxonomy: counters, gauges, timers, histograms/distribution.
- Naming conventions and dimensional model (labels/tags).
- Cardinality budgets and enforcement rules.
- SLO/SLI-focused metrics design (latency, traffic, errors, saturation).
- Implementation patterns and test strategy.

**Out of scope**

- Full SRE SLO policy for your org (we provide adaptable templates).
- Vendor-specific dashboards (we provide principles).

## Core principles (non-negotiable)

1. Metrics must be designed for aggregation (global questions).
2. Labels/tags must be bounded (cardinality control).
3. Prefer a small set of high-signal metrics over many low-signal metrics.

## Metric types: when to use what

- **Counter**: monotonic count (requests_total, errors_total).
- **Gauge**: instantaneous value (queue_depth, memory_used).
- **Timer**: duration measurements (request_latency).
- **Histogram/Distribution**: latency/size distributions suitable for percentile-ish analysis.
- **Summary** (if your backend supports): use carefully; often harder to aggregate across instances.

## Golden signals (recommended baseline)

1. **Traffic**: `http_server_requests_total`
2. **Errors**: `http_server_errors_total` or `http_server_requests_total{outcome="error"}`
3. **Latency**: `http_server_request_duration_seconds` (histogram)
4. **Saturation**: thread pool utilization, queue size, DB pool usage

## Naming conventions (Prometheus-friendly)

- Use `snake_case`.
- Base unit in name if needed:
  - `_seconds`, `_bytes`, `_total`.
- Prefer a consistent prefix/domain:
  - `http_server_*`, `db_*`, `cache_*`, `mq_*`.

## Label/tag rules (cardinality guardrails)

### Allowed labels for HTTP server metrics

- `method` (bounded)
- `route` (bounded; avoid raw path)
- `status` (bounded)
- `outcome` (bounded: success/error)
- `service`, `env` (bounded; usually from resource labels)

### Forbidden labels (common cardinality bombs)

- `userId`, `email`, `ip`, `sessionId`
- `requestId`, `traceId`
- raw URL path, query string
- exception messages

### Route normalization

- Use templated route names: `/v1/orders/{id}` not `/v1/orders/123`.
- If your framework does not provide route templates, implement normalization.

## Histograms and timers (latency best practice)

- Prefer histograms for latency:
  - enable bucketed distributions suitable for SLOs.
- Choose buckets that match SLO thresholds:
  - e.g., 50ms, 100ms, 200ms, 500ms, 1s, 2s, 5s.
- Avoid per-endpoint custom histograms unless truly needed.

## Instrumentation plan (step-by-step)

1. Define the questions:
   - "What is p95 latency for /orders in prod?"
   - "What is error rate for dependency X?"
2. Define the minimal metric set to answer them.
3. Define label set and enforce boundedness.
4. Implement instrumentation:
   - inbound HTTP
   - outbound HTTP clients
   - DB calls
   - cache
   - messaging consumers/producers
5. Validate on a staging environment:
   - confirm label cardinality is bounded
   - confirm naming conventions
6. Add dashboards and alerts:
   - SLO burn rate alerts (if used)
   - saturation alerts

## Testing strategy

- Unit tests for route normalization.
- “Metrics snapshot” tests for presence of required metric names.
- Cardinality budget tests (fail if new labels explode).
- Load test sanity check to observe series count growth.

## Outputs / artifacts

- `docs/metrics.md` (metric catalog + labels + intent)
- `metrics/metric-catalog.yml` (machine-readable inventory)
- `metrics/cardinality-budget.md`
- Code changes:
  - instrumentation wrappers
  - timers/histograms config
  - tests for bounded labels

## Definition of Done (DoD)

- [ ] Baseline golden-signal metrics exist.
- [ ] Label sets documented and bounded.
- [ ] Cardinality budget validated in staging.
- [ ] Dashboards and alerts (at least basic) updated.
- [ ] Regression tests prevent accidental cardinality bombs.

## Guardrails (What NOT to do)

- Never add high-cardinality labels.
- Never label metrics with IDs or raw error messages.
- Avoid duplicating the same metric under many names.

## Common failure modes & fixes

- Symptom: Prometheus/metrics backend memory spikes -> Fix: remove high-cardinality labels, normalize routes.
- Symptom: metrics not aggregatable -> Fix: avoid instance-specific dimensions; use consistent naming.
- Symptom: percentiles inconsistent -> Fix: use histograms with defined buckets; avoid per-instance summaries.

## References (see references/)

- `references/prometheus-cardinality.md`
- `references/micrometer-timers-histograms.md`
- `references/metric-catalog-template.yml`
