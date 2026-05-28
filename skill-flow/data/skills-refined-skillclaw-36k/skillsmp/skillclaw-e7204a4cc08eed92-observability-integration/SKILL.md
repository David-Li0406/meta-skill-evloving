---
name: observability-integration
description: Use this skill when setting up comprehensive observability for integrations with metrics, traces, and alerts, applicable to various platforms like Groq and PostHog.
---

# Observability Integration

## Overview
Set up comprehensive observability for integrations, including metrics collection, distributed tracing, and alerting.

## Prerequisites
- Prometheus or compatible metrics backend
- OpenTelemetry SDK installed
- Grafana or similar dashboarding tool
- AlertManager configured

## Metrics Collection

### Key Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `requests_total` | Counter | Total API requests |
| `request_duration_seconds` | Histogram | Request latency |
| `errors_total` | Counter | Error count by type |
| `rate_limit_remaining` | Gauge | Rate limit headroom |

### Prometheus Metrics

```typescript
import { Registry, Counter, Histogram, Gauge } from 'prom-client';

const registry = new Registry();

const requestCounter = new Counter({
  name: 'requests_total',
  help: 'Total API requests',
  labelNames: ['method', 'status'],
  registers: [registry],
});

const requestDuration = new Histogram({
  name: 'request_duration_seconds',
  help: 'Request duration',
  labelNames: ['method'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [registry],
});

const errorCounter = new Counter({
  name: 'errors_total',
  help: 'Errors by type',
  labelNames: ['error_type'],
  registers: [registry],
});
```

### Instrumented Client

```typescript
async function instrumentedRequest<T>(
  method: string,
  operation: () => Promise<T>
): Promise<T> {
  const timer = requestDuration.startTimer({ method });

  try {
    const result = await operation();
    requestCounter.inc({ method, status: 'success' });
    return result;
  } catch (error: any) {
    requestCounter.inc({ method, status: 'error' });
    errorCounter.inc({ error_type: error.code || 'unknown' });
    throw error;
  } finally {
    timer();
  }
}
```

## Distributed Tracing

### OpenTelemetry Setup

```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('integration-client');

// Example of tracing a request
async function tracedRequest(method: string, operation: () => Promise<any>) {
  const span = tracer.startSpan('tracedRequest', { attributes: { method } });
  try {
    const result = await operation();
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    throw error;
  } finally {
    span.end();
  }
}
```