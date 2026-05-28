---
name: observability-for-integrations
description: Use this skill when setting up comprehensive observability for integrations, including metrics, traces, and alerts for various services.
---

# Observability for Integrations

## Overview
Implement comprehensive observability for integrations, including metrics collection, distributed tracing, structured logging, and alerting.

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

#### Example Metrics
```typescript
import { Registry, Counter, Histogram, Gauge, collectDefaultMetrics } from 'prom-client';

const registry = new Registry();
collectDefaultMetrics({ register: registry });

// Request counters
const requestCounter = new Counter({
  name: 'integration_requests_total',
  help: 'Total API requests',
  labelNames: ['service', 'status'],
  registers: [registry],
});

// Latency histogram
const requestDuration = new Histogram({
  name: 'integration_request_duration_seconds',
  help: 'Request duration in seconds',
  labelNames: ['service'],
  buckets: [0.1, 0.5, 1, 2, 5, 10],
  registers: [registry],
});

// Error counter
const errorCounter = new Counter({
  name: 'integration_errors_total',
  help: 'Total errors by type',
  labelNames: ['service', 'error_type'],
  registers: [registry],
});
```

### Step 2: Add Distributed Tracing
Integrate OpenTelemetry for end-to-end request tracing.

### Step 3: Configure Structured Logging
Set up JSON logging with consistent field names.

### Step 4: Create Alert Rules
Define alerting rules for error rates and latency.

## Instrumented Client Example
```typescript
async function instrumentedRequest<T>(
  service: string,
  operation: () => Promise<T>
): Promise<T> {
  const timer = requestDuration.startTimer({ service });

  try {
    const result = await operation();
    requestCounter.inc({ service, status: 'success' });
    return result;
  } catch (error: any) {
    requestCounter.inc({ service, status: 'error' });
    errorCounter.inc({ service, error_type: error.code || 'unknown' });
    throw error;
  } finally {
    timer();
  }
}
```