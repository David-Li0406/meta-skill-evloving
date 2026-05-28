---
name: observability-with-opentelemetry
description: Use this skill when implementing observability in distributed systems through OpenTelemetry, focusing on tracing, metrics, and structured logging.
---

# Observability with OpenTelemetry

Apply these observability principles to ensure comprehensive visibility into distributed systems and microservices using OpenTelemetry.

## Core Observability Principles

- Develop idiomatic, maintainable, and high-performance code with built-in observability.
- Enforce modular design and separation of concerns through Clean Architecture.
- Promote test-driven development and robust observability from the start.

## OpenTelemetry Integration

- Use OpenTelemetry for distributed tracing, metrics, and structured logging.
- Start and propagate tracing spans across all service boundaries.
- Use `otel.Tracer` for creating spans and `otel.Meter` for collecting metrics.
- Export data to OpenTelemetry Collector, Jaeger, or Prometheus.
- Configure appropriate sampling rates for production environments.

## Distributed Tracing

- Trace all incoming requests and propagate context through internal calls.
- Use middleware to instrument HTTP and gRPC endpoints automatically.
- Include trace context in all downstream service calls.
- Create child spans for significant operations within a service.
- Add relevant attributes to spans for debugging and analysis.

## Metrics Collection

Monitor these key metrics across all services:

- **Request latency**: Track p50, p90, p95, and p99 percentiles.
- **Throughput**: Measure requests per second by endpoint.
- **Error rate**: Track 4xx and 5xx responses separately.
- **Resource usage**: Monitor CPU, memory, disk, and network utilization.
- **Custom business metrics**: Track domain-specific KPIs.

## Structured Logging

- Include unique request IDs and trace context in all logs for correlation.
- Use structured logging formats (e.g., JSON) for machine parseability.
- Include relevant context: timestamp, service name, trace ID, span ID.
- Log at appropriate levels: DEBUG, INFO, WARN, ERROR.
- Avoid logging sensitive information (PII, credentials).

## Architecture Patterns

- Apply Clean Architecture with handlers, services, repositories, and domain models.
- Use domain-driven design principles for clear boundaries.
- Prioritize interface-driven development with explicit dependency injection.
- Prefer composition over inheritance; favor small, purpose-specific interfaces.

## Correlation and Context

- Propagate context through the entire request lifecycle.
- Use correlation IDs for request tracking across services.
- Include service version and deployment information in telemetry.
- Tag traces with relevant business context for filtering.
- Enable trace-to-log and log-to-trace correlation.

## Alerting and Dashboards

- Create dashboards for service health and business metrics.
- Set up alerts based on SLOs and error budgets.
- Use anomaly detection for proactive issue identification.
- Document runbooks for common alert scenarios.
- Review and tune alerts regularly to reduce noise.

## Instrumentation Best Practices

- Instrument at service boundaries (entry/exit points).
- Add custom spans for database operations and external calls.
- Include relevant attributes (user ID, request type, etc.).
- Avoid over-instrumentation that creates noise.
- Use semantic conventions for consistent attribute naming.

## Production Considerations

- Configure appropriate sampling rates to balance visibility and cost.
- Use head-based sampling for consistent trace capture.
- Implement tail-based sampling for capturing errors.
- Set retention policies based on debugging needs.
- Monitor observability infrastructure health.

## Quick Start

1. Set `service.name` and other resource attributes.
2. Add auto-instrumentation.
3. Export OTLP via an OpenTelemetry Collector.
4. Correlate logs with trace IDs.

## References

- `references/concepts.md` — traces/metrics/logs, context propagation, sampling, semantic conventions.
- `references/collector-and-otlp.md` — Collector pipelines, processors, deployment patterns, tail sampling.
- `references/instrumentation-and-troubleshooting.md` — manual spans, propagation pitfalls, cardinality, debugging.