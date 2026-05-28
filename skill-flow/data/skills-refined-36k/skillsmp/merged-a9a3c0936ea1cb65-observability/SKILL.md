---
name: observability
description: Set up comprehensive observability for integrations with metrics, traces, and alerts. Use when implementing monitoring for operations, setting up dashboards, or configuring alerting for integration health.
---

# Observability

## Overview
Implement comprehensive observability for integrations including metrics, distributed tracing, logging, and alerting.

## Prerequisites
- Prometheus or compatible metrics backend
- OpenTelemetry SDK installed
- Grafana or similar dashboarding tool
- AlertManager configured

## Observability Pillars

| Pillar | Tool | Purpose |
|--------|------|---------|
| Metrics | Prometheus | Performance & usage tracking |
| Traces | OpenTelemetry | Request flow visibility |
| Logs | Structured JSON | Debugging & audit |
| Alerts | AlertManager | Incident notification |

## Instructions

### Step 1: Set Up Metrics Collection
Implement Prometheus counters, histograms, and gauges for key operations.

### Step 2: Add Distributed Tracing
Integrate OpenTelemetry for end-to-end request tracing.

### Step 3: Configure Structured Logging
Set up JSON logging with consistent field names.

### Step 4: Create Alert Rules
Define alerting rules for error rates and latency.

## Metrics Collection

### Key Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `<integration>_requests_total` | Counter | Total API requests |
| `<integration>_request_duration_seconds` | Histogram | Request latency |
| `<integration>_errors_total` | Counter | Error count by type |
| `<integration>_rate_limit_remaining` | Gauge | Rate limit headroom |

### Prometheus Metrics Example
```typescript
import { Registry, Counter, Histogram, Gauge } from 'prom-client';

const registry = new Registry();

const requestCounter = new Counter({
  name: '<integration>_requests_total',
  help: 'Total <integration> API requests',
  labelNames: ['method', 'status'],
  registers: [registry],
});

const requestDuration = new Histogram({
  name: '<integration>_request_duration_seconds',
  help: '<integration> request duration',
  labelNames: ['method'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [registry],
});

const errorCounter = new Counter({
  name: '<integration>_errors_total',
  help: '<integration> errors by type',
  labelNames: ['error_type'],
  registers: [registry],
});
```

### Instrumented Client Example
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

## Distributed Tracing Example
```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('<integration>-client');

async function tracedIntegrationCall<T>(
  operationName: string,
  operation: () => Promise<T>
): Promise<T> {
  return tracer.startActiveSpan(`<integration>.${operationName}`, async (span) => {
    try {
      const result = await operation();
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error: any) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

## Logging Strategy Example
```typescript
import pino from 'pino';

const logger = pino({
  name: '<integration>',
  level: process.env.LOG_LEVEL || 'info',
});

function logIntegrationOperation(
  operation: string,
  data: Record<string, any>,
  duration: number
) {
  logger.info({
    service: '<integration>',
    operation,
    duration_ms: duration,
    ...data,
  });
}
```

## Alert Configuration Example
```yaml
# <integration>_alerts.yaml
groups:
  - name: <integration>_alerts
    rules:
      - alert: <Integration>HighErrorRate
        expr: |
          rate(<integration>_errors_total[5m]) /
          rate(<integration>_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "<Integration> error rate > 5%"

      - alert: <Integration>HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(<integration>_request_duration_seconds_bucket[5m])
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "<Integration> P95 latency > 2s"

      - alert: <Integration>Down
        expr: up{job="<integration>"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "<Integration> integration is down"
```

## Dashboard Example
```json
{
  "panels": [
    {
      "title": "<Integration> Request Rate",
      "targets": [{
        "expr": "rate(<integration>_requests_total[5m])"
      }]
    },
    {
      "title": "<Integration> Latency P50/P95/P99",
      "targets": [{
        "expr": "histogram_quantile(0.5, rate(<integration>_request_duration_seconds_bucket[5m]))"
      }]
    }
  ]
}
```

## Resources
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Integration Observability Guide](https://docs.integration.com/observability)

## Next Steps
For incident response, see `<integration>-incident-runbook`.