# Observability

This guideline establishes observability practices using metrics, logs, and traces (the three pillars of observability).

## Metrics Collection

Collect and expose key performance indicators (response time, error rate, throughput).

## Distributed Tracing

Implement tracing to follow requests across microservices.

## Health Checks

Provide health and readiness endpoints for monitoring and orchestration.

## Service Level Objectives (SLO)

Define and monitor SLIs/SLOs/SLAs to ensure service reliability.

---

## Detailed Examples

### Metrics with Prometheus

<details>
<summary>Instrumenting Node.js Application</summary>

```typescript
import client from 'prom-client';
import express from 'express';

// Enable default metrics (CPU, memory, etc.)
client.collectDefaultMetrics({ prefix: 'app_' });

// Custom metrics
const httpRequestDuration = new client.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
});

const httpRequestTotal = new client.Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status_code']
});

const activeConnections = new client.Gauge({
    name: 'active_connections',
    help: 'Number of active connections'
});

const dbQueryDuration = new client.Summary({
    name: 'db_query_duration_seconds',
    help: 'Database query duration',
    labelNames: ['operation', 'table'],
    percentiles: [0.5, 0.9, 0.95, 0.99]
});

// Middleware to track metrics
app.use((req, res, next) => {
    const start = Date.now();

    activeConnections.inc();

    res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        const labels = {
            method: req.method,
            route: req.route?.path || req.path,
            status_code: res.statusCode
        };

        httpRequestDuration.observe(labels, duration);
        httpRequestTotal.inc(labels);
        activeConnections.dec();
    });

    next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', client.register.contentType);
    res.end(await client.register.metrics());
});

// Usage in application code
async function queryUser(id: string) {
    const end = dbQueryDuration.startTimer({ operation: 'SELECT', table: 'users' });
    try {
        const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
        return user;
    } finally {
        end();
    }
}
```
</details>

<details>
<summary>Python with Prometheus Client</summary>

```python
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest
from flask import Flask, Response
import time

app = Flask(__name__)

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

active_requests = Gauge(
    'active_requests',
    'Number of active requests'
)

@app.before_request
def before_request():
    active_requests.inc()
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    http_request_duration.labels(
        method=request.method,
        endpoint=request.endpoint
    ).observe(duration)

    http_requests_total.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()

    active_requests.dec()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```
</details>

### Distributed Tracing with OpenTelemetry

<details>
<summary>OpenTelemetry Setup</summary>

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

// Configure OpenTelemetry
const sdk = new NodeSDK({
    resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: 'user-service',
        [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV
    }),
    traceExporter: new OTLPTraceExporter({
        url: 'http://localhost:4318/v1/traces'
    }),
    instrumentations: [getNodeAutoInstrumentations()]
});

sdk.start();

// Manual span creation
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('user-service');

async function processOrder(orderId: string) {
    const span = tracer.startSpan('processOrder');
    span.setAttribute('order.id', orderId);

    try {
        // Create child span
        const validateSpan = tracer.startSpan('validateOrder', {
            parent: span
        });
        await validateOrder(orderId);
        validateSpan.end();

        // Another child span
        const paymentSpan = tracer.startSpan('processPayment');
        await processPayment(orderId);
        paymentSpan.end();

        span.setStatus({ code: SpanStatusCode.OK });
    } catch (error) {
        span.setStatus({
            code: SpanStatusCode.ERROR,
            message: error.message
        });
        span.recordException(error);
        throw error;
    } finally {
        span.end();
    }
}
```
</details>

### Health Checks

<details>
<summary>Kubernetes-style Health Endpoints</summary>

```typescript
// Health check endpoints
app.get('/health/live', (req, res) => {
    // Liveness probe - is the app running?
    res.status(200).json({ status: 'ok' });
});

app.get('/health/ready', async (req, res) => {
    // Readiness probe - is the app ready to serve traffic?
    const checks = {
        database: await checkDatabase(),
        redis: await checkRedis(),
        externalApi: await checkExternalApi()
    };

    const allHealthy = Object.values(checks).every(check => check.healthy);

    res.status(allHealthy ? 200 : 503).json({
        status: allHealthy ? 'ready' : 'not ready',
        checks
    });
});

async function checkDatabase(): Promise<HealthCheck> {
    try {
        await db.query('SELECT 1');
        return { healthy: true, message: 'Database connected' };
    } catch (error) {
        return { healthy: false, message: error.message };
    }
}

async function checkRedis(): Promise<HealthCheck> {
    try {
        await redis.ping();
        return { healthy: true, message: 'Redis connected' };
    } catch (error) {
        return { healthy: false, message: error.message };
    }
}

interface HealthCheck {
    healthy: boolean;
    message: string;
}
```

```yaml
# Kubernetes deployment with health checks
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  template:
    spec:
      containers:
      - name: app
        image: user-service:1.0.0
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
```
</details>

### Service Level Objectives

<details>
<summary>Defining and Monitoring SLOs</summary>

```typescript
// SLI/SLO/SLA Definitions

// SLI (Service Level Indicator) - Measurable metrics
const SLIs = {
    availability: 'Percentage of successful requests',
    latency: '95th percentile response time',
    errorRate: 'Percentage of failed requests'
};

// SLO (Service Level Objective) - Internal targets
const SLOs = {
    availability: 99.9,  // 99.9% of requests should succeed
    latencyP95: 200,     // 95% of requests < 200ms
    errorRate: 0.1       // < 0.1% error rate
};

// SLA (Service Level Agreement) - Contractual commitments
const SLAs = {
    availability: 99.5,  // Guaranteed 99.5% uptime
    support: '24/7 with 1-hour response time for critical issues'
};

// Monitoring SLOs
class SLOMonitor {
    private successCount = 0;
    private totalCount = 0;
    private latencies: number[] = [];

    recordRequest(success: boolean, latency: number) {
        this.totalCount++;
        if (success) this.successCount++;
        this.latencies.push(latency);
    }

    getMetrics() {
        const availability = (this.successCount / this.totalCount) * 100;
        const sortedLatencies = this.latencies.sort((a, b) => a - b);
        const p95Index = Math.floor(this.latencies.length * 0.95);
        const latencyP95 = sortedLatencies[p95Index];

        return {
            availability: {
                current: availability,
                target: SLOs.availability,
                met: availability >= SLOs.availability
            },
            latencyP95: {
                current: latencyP95,
                target: SLOs.latencyP95,
                met: latencyP95 <= SLOs.latencyP95
            }
        };
    }

    getErrorBudget() {
        // Error budget = 1 - SLO
        const allowedErrors = this.totalCount * (1 - SLOs.availability / 100);
        const actualErrors = this.totalCount - this.successCount;
        const remainingBudget = allowedErrors - actualErrors;

        return {
            allowed: allowedErrors,
            consumed: actualErrors,
            remaining: remainingBudget,
            percentageRemaining: (remainingBudget / allowedErrors) * 100
        };
    }
}
```
</details>
