# Monitoring and Observability Patterns

## Overview
This document describes monitoring patterns, observability practices, and alerting strategies for production systems. Effective monitoring enables fast issue detection, root cause analysis, and system optimization.

## The Three Pillars of Observability

### 1. Metrics
**What**: Numerical measurements aggregated over time
**When**: Understanding trends, capacity planning, alerting
**Tools**: Prometheus, CloudWatch, Datadog, New Relic

### 2. Logs
**What**: Discrete events and structured data
**When**: Debugging, audit trails, troubleshooting
**Tools**: ELK Stack, Loki, CloudWatch Logs, Splunk

### 3. Traces
**What**: Request flow through distributed systems
**When**: Distributed system debugging, performance optimization
**Tools**: Jaeger, Zipkin, AWS X-Ray, Datadog APM

## Metric Collection Patterns

### 1. RED Method (Request-Driven Services)

**Pattern:**
```yaml
R - Rate: Requests per second
E - Errors: Failed requests per second
D - Duration: Response time distribution (p50, p95, p99)
```

**When to use:**
- Web applications
- API services
- Request/response systems

**Implementation:**
```prometheus
# Rate
rate(http_requests_total[5m])

# Errors
rate(http_requests_total{status=~"5.."}[5m])

# Duration (p95)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Dashboard panels:**
```yaml
Panel 1: Request Rate
  - Total requests/sec
  - Breakdown by endpoint
  - Breakdown by status code

Panel 2: Error Rate
  - Percentage of requests failing
  - Absolute error count
  - Error rate by endpoint

Panel 3: Response Time
  - p50, p95, p99 latency
  - Latency by endpoint
  - Latency heatmap
```

### 2. USE Method (Resource Monitoring)

**Pattern:**
```yaml
U - Utilization: How busy is the resource (%)
S - Saturation: Queue depth, wait time
E - Errors: Error count and rate
```

**When to use:**
- Infrastructure monitoring
- Capacity planning
- Resource optimization

**Resources to monitor:**
```yaml
CPU:
  - Utilization: CPU usage percentage
  - Saturation: Run queue length
  - Errors: CPU throttling events

Memory:
  - Utilization: Memory usage percentage
  - Saturation: Swap usage, page faults
  - Errors: Out of memory kills

Disk:
  - Utilization: Disk space used
  - Saturation: Queue depth, wait time
  - Errors: I/O errors

Network:
  - Utilization: Bandwidth usage
  - Saturation: Packet queue depth
  - Errors: Packet drops, retransmits
```

**Implementation:**
```prometheus
# CPU Utilization
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Utilization
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Disk Utilization
100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)
```

### 3. Four Golden Signals (Google SRE)

**Pattern:**
```yaml
1. Latency: Time to service a request
2. Traffic: Demand on the system
3. Errors: Rate of failed requests
4. Saturation: How "full" the service is
```

**When to use:**
- Production services
- SLO/SLA tracking
- Service health monitoring

**Implementation:**
```yaml
Latency:
  - p50, p95, p99 response time
  - Broken down by endpoint
  - Success vs error latency

Traffic:
  - Requests per second
  - Bytes transferred
  - Active connections

Errors:
  - HTTP 5xx rate
  - HTTP 4xx rate (client errors)
  - Exception rate

Saturation:
  - CPU/Memory utilization
  - Queue depths
  - Connection pool usage
```

## Logging Patterns

### 1. Structured Logging

**Pattern:**
Use JSON format for all logs with consistent fields.

**Good example:**
```json
{
  "timestamp": "2025-12-09T10:30:00.123Z",
  "level": "error",
  "message": "Payment processing failed",
  "service": "payment-service",
  "version": "v1.2.3",
  "user_id": "user-12345",
  "transaction_id": "txn-abc-123",
  "error_type": "GatewayTimeout",
  "duration_ms": 5000,
  "trace_id": "abc123def456",
  "span_id": "def456"
}
```

**Bad example:**
```
[ERROR] Payment failed for user user-12345
```

**Standard fields:**
```yaml
Required:
  - timestamp (ISO 8601)
  - level (debug, info, warn, error, fatal)
  - message (human-readable)
  - service (service name)

Recommended:
  - trace_id (distributed tracing)
  - span_id (distributed tracing)
  - user_id (user context)
  - request_id (request context)
  - version (app version)
  - environment (dev, staging, prod)

Context-specific:
  - transaction_id
  - order_id
  - error_type
  - duration_ms
  - http_status
```

### 2. Log Levels

**Pattern:**
```yaml
DEBUG: Detailed diagnostic information
  - Use: Development, troubleshooting
  - Example: "Database query: SELECT * FROM users WHERE id=123"

INFO: General informational messages
  - Use: Significant events, flow tracking
  - Example: "User logged in: user_id=123"

WARN: Warning messages, potential issues
  - Use: Degraded but functional state
  - Example: "Response time exceeded threshold: 2000ms"

ERROR: Error messages, failures
  - Use: Failed operations, exceptions
  - Example: "Payment processing failed: timeout"

FATAL: Critical errors, service unusable
  - Use: Service crashes, unrecoverable errors
  - Example: "Database connection pool exhausted"
```

**Production log levels:**
```yaml
Development: DEBUG
Staging: INFO
Production: WARN (or INFO with sampling)
```

### 3. What to Log

**Always log:**
```yaml
- Application startup/shutdown
- Authentication events (success/failure)
- Authorization failures
- Database connection issues
- External API failures
- Uncaught exceptions
- Business-critical operations
- Performance degradation
```

**Never log:**
```yaml
- Passwords or secrets
- Credit card numbers
- Social Security numbers
- Session tokens
- API keys
- Personally identifiable information (PII) - unless required and encrypted
```

**Sample appropriately:**
```yaml
High-frequency events:
  - Successful requests (sample at 1%)
  - Cache hits (sample at 0.1%)
  - Successful authentication (sample)

Always log:
  - Errors and failures (100%)
  - Security events (100%)
  - Business events (100%)
```

### 4. Log Aggregation Pattern

**Pattern:**
```yaml
Application → Log Shipper → Log Aggregator → Storage → Visualization

Components:
  - Log Shipper: Filebeat, Fluentd, Logstash
  - Aggregator: Logstash, Fluentd
  - Storage: Elasticsearch, Loki
  - Visualization: Kibana, Grafana
```

**Kubernetes logging:**
```yaml
Option 1: Sidecar pattern
  - Sidecar container collects logs
  - Ships to aggregator
  - Per-pod overhead

Option 2: DaemonSet pattern (recommended)
  - DaemonSet on each node
  - Collects from all pods
  - Lower overhead

Option 3: Direct to storage
  - Application logs directly to aggregator
  - No intermediate shipper
  - Application dependency
```

## Distributed Tracing Patterns

### 1. Trace Context Propagation

**Pattern:**
Propagate trace ID and span ID through all service calls.

**Implementation:**
```javascript
// Service A (entry point)
const trace = tracer.startSpan('handle_request');
const traceId = trace.context().traceId;
const spanId = trace.context().spanId;

// Pass to Service B
await axios.get('http://service-b/api', {
  headers: {
    'X-Trace-Id': traceId,
    'X-Span-Id': spanId
  }
});

// Service B (downstream)
const traceId = req.headers['x-trace-id'];
const parentSpanId = req.headers['x-span-id'];
const span = tracer.startSpan('process_request', {
  childOf: { traceId, spanId: parentSpanId }
});
```

**Standard headers:**
```yaml
- X-Trace-Id: Unique trace identifier
- X-Span-Id: Current span identifier
- X-Parent-Span-Id: Parent span identifier
- X-Sampled: Whether trace is sampled

Or use standard: W3C Trace Context
  - traceparent
  - tracestate
```

### 2. Sampling Patterns

**Pattern:**
Not all requests need tracing - sample based on volume and importance.

**Sampling strategies:**
```yaml
1. Fixed rate sampling:
   - Sample X% of all requests
   - Example: 1% for high-traffic services

2. Adaptive sampling:
   - Sample more when errors occur
   - Sample less for successful requests

3. Priority sampling:
   - Always sample errors
   - Always sample slow requests
   - Sample 1% of normal requests

4. Head-based sampling:
   - Decision made at entry point
   - Consistent sampling across trace

5. Tail-based sampling:
   - Decision made after trace completes
   - Sample interesting traces (errors, slow)
```

**Implementation:**
```javascript
// Priority sampling
function shouldSample(request, response) {
  // Always sample errors
  if (response.statusCode >= 500) return true;

  // Always sample slow requests
  if (response.duration > 1000) return true;

  // Sample 1% of normal requests
  return Math.random() < 0.01;
}
```

### 3. Span Tagging

**Pattern:**
Add context to spans for filtering and analysis.

**Standard tags:**
```yaml
HTTP:
  - http.method: GET, POST, etc.
  - http.url: Request URL
  - http.status_code: 200, 404, 500, etc.
  - http.request_size: Request body size
  - http.response_size: Response body size

Database:
  - db.type: postgres, mysql, mongodb
  - db.statement: SQL query
  - db.instance: Database name
  - db.user: Database user

RPC:
  - rpc.service: Service name
  - rpc.method: Method name
  - rpc.system: grpc, thrift, etc.

General:
  - component: Component name
  - error: true/false
  - user_id: User identifier
  - tenant_id: Multi-tenant identifier
```

## Alerting Patterns

### 1. Symptom-Based Alerting

**Pattern:**
Alert on user-visible symptoms, not causes.

**Good alerts:**
```yaml
- High error rate (users seeing errors)
- Slow response time (users experiencing slowness)
- Service unavailable (users can't access service)
- High request queue (users will experience delays)
```

**Bad alerts:**
```yaml
- High CPU usage (not necessarily user-visible)
- Low disk space (not immediately user-visible)
- Process restarted (may be normal)
- Memory usage high (may be expected)
```

**Exception:**
Alert on causes if they predict imminent failure:
```yaml
- Disk will fill in 4 hours
- Memory leak detected (growing continuously)
- Certificate expires in 7 days
```

### 2. Alert Severity Levels

**Pattern:**
```yaml
Critical (page on-call):
  - Service completely down
  - Error rate > 5%
  - Data loss occurring
  - Security breach

  Action: Immediate response required
  Response time: < 5 minutes

Warning (notify team):
  - Elevated error rate (1-5%)
  - Slow response time
  - High resource usage
  - Approaching capacity limits

  Action: Investigate during business hours
  Response time: < 1 hour

Info (log only):
  - Deployments
  - Scaling events
  - Configuration changes
  - Recovered alerts

  Action: Awareness only
  Response time: None
```

### 3. Alert Timing

**Pattern:**
Use `for` duration to avoid alert fatigue.

**Implementation:**
```yaml
# Bad: Alert immediately
- alert: HighErrorRate
  expr: rate(errors[5m]) > 0.01

# Good: Alert after sustained issue
- alert: HighErrorRate
  expr: rate(errors[5m]) > 0.01
  for: 5m  # Must be true for 5 minutes
  labels:
    severity: warning
  annotations:
    summary: "Error rate elevated for 5 minutes"
```

**Timing guidelines:**
```yaml
Critical issues:
  - Short duration: 1-2 minutes
  - Need fast detection

Warning issues:
  - Medium duration: 5-15 minutes
  - Avoid transient spikes

Capacity issues:
  - Long duration: 30-60 minutes
  - Sustained trends matter
```

### 4. Alert Context

**Pattern:**
Include actionable information in alerts.

**Good alert:**
```yaml
- alert: HighErrorRate
  annotations:
    summary: "Error rate is {{ $value | humanizePercentage }}"
    description: |
      Error rate has been above 5% for 10 minutes
      Current value: {{ $value | humanizePercentage }}
      Affected service: {{ $labels.service }}
      Environment: {{ $labels.environment }}
    dashboard: "https://grafana.example.com/d/service-health"
    runbook: "https://wiki.example.com/runbooks/high-error-rate"
    logs: "https://kibana.example.com/app/discover?query=service:{{ $labels.service }}"
```

**Essential context:**
```yaml
- Current metric value
- Threshold that was breached
- Duration of issue
- Affected component/service
- Link to dashboard
- Link to runbook
- Link to relevant logs
```

### 5. Alert Routing

**Pattern:**
Route alerts based on severity and team ownership.

**Alertmanager configuration:**
```yaml
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

  routes:
    # Critical alerts → PagerDuty
    - match:
        severity: critical
      receiver: 'pagerduty'
      group_wait: 0s
      repeat_interval: 5m

    # Payment service → Payment team
    - match:
        service: payment
      receiver: 'payment-team-slack'

    # Warning alerts → Slack
    - match:
        severity: warning
      receiver: 'team-slack'

receivers:
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<key>'
        severity: '{{ .CommonLabels.severity }}'

  - name: 'team-slack'
    slack_configs:
      - api_url: '<webhook>'
        channel: '#alerts'
        text: '{{ .CommonAnnotations.summary }}'

  - name: 'payment-team-slack'
    slack_configs:
      - api_url: '<webhook>'
        channel: '#payment-alerts'
```

## Dashboard Patterns

### 1. Service Health Dashboard

**Panels:**
```yaml
Row 1: Overview
  - Service status (up/down)
  - Request rate
  - Error rate
  - Response time (p95)

Row 2: Traffic
  - Requests per second (total)
  - Requests by endpoint
  - Requests by status code

Row 3: Errors
  - Error rate percentage
  - Error count by type
  - Recent error logs

Row 4: Performance
  - Response time (p50, p95, p99)
  - Response time by endpoint
  - Slow request heatmap

Row 5: Resources
  - CPU usage
  - Memory usage
  - Active connections
  - Database connection pool
```

### 2. SLO Dashboard

**Panels:**
```yaml
SLO Tracking:
  - Availability (target: 99.9%)
  - Error budget remaining
  - Error budget burn rate
  - Time until budget exhausted

Current Period:
  - Successful requests %
  - Failed requests count
  - Downtime minutes
  - SLO compliance status

Historical:
  - SLO compliance over time
  - Error budget usage trends
  - Incident impact on SLO
```

### 3. Resource Utilization Dashboard

**Panels:**
```yaml
Compute:
  - CPU usage per instance
  - Memory usage per instance
  - Instance count
  - Auto-scaling events

Storage:
  - Disk usage by volume
  - Disk I/O by instance
  - IOPS usage

Network:
  - Bandwidth usage
  - Connection count
  - Packet loss rate

Database:
  - Connection count
  - Query performance
  - Replication lag
  - Cache hit rate
```

## Health Check Patterns

### 1. Liveness vs Readiness

**Liveness Probe:**
```yaml
Purpose: Is the application running?
Action if fails: Restart container

Check:
  - Process is running
  - Application is responsive
  - Not deadlocked

Kubernetes:
  livenessProbe:
    httpGet:
      path: /health/live
      port: 8080
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
```

**Readiness Probe:**
```yaml
Purpose: Is the application ready to serve traffic?
Action if fails: Remove from load balancer

Check:
  - Database connected
  - External dependencies available
  - Caches warmed
  - Application initialized

Kubernetes:
  readinessProbe:
    httpGet:
      path: /health/ready
      port: 8080
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 2
```

**Startup Probe:**
```yaml
Purpose: Has the application finished starting?
Action if fails: Restart container

Use for:
  - Slow-starting applications
  - Prevents liveness probe killing during startup

Kubernetes:
  startupProbe:
    httpGet:
      path: /health/startup
      port: 8080
    failureThreshold: 30
    periodSeconds: 10
```

### 2. Health Check Endpoint Implementation

**Pattern:**
```javascript
app.get('/health/live', (req, res) => {
  // Minimal check - is the process alive?
  res.status(200).json({ status: 'ok' });
});

app.get('/health/ready', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    checks: {}
  };

  // Check database
  try {
    await db.ping();
    health.checks.database = 'healthy';
  } catch (error) {
    health.checks.database = 'unhealthy';
    health.status = 'unhealthy';
  }

  // Check Redis
  try {
    await redis.ping();
    health.checks.redis = 'healthy';
  } catch (error) {
    health.checks.redis = 'degraded';
    // Don't mark overall as unhealthy for cache
  }

  // Check external API
  try {
    await externalAPI.ping();
    health.checks.externalAPI = 'healthy';
  } catch (error) {
    health.checks.externalAPI = 'unhealthy';
    health.status = 'degraded';
  }

  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

## SLO/SLI Patterns

### 1. Defining SLIs (Service Level Indicators)

**Pattern:**
```yaml
Availability SLI:
  - Percentage of successful requests
  - Calculation: (successful requests / total requests) × 100
  - Target: 99.9%

Latency SLI:
  - Percentage of requests faster than threshold
  - Calculation: (fast requests / total requests) × 100
  - Target: 95% of requests < 500ms

Error Rate SLI:
  - Percentage of requests without errors
  - Calculation: 100 - (errors / total requests) × 100
  - Target: 99.5%
```

### 2. Error Budget

**Pattern:**
```yaml
Error Budget = 100% - SLO

Example (99.9% availability SLO):
  - Error budget: 0.1%
  - Allowed downtime per month: 43.2 minutes
  - Allowed errors per 1M requests: 1000

Burn rate:
  - Current error rate vs budget
  - Time until budget exhausted
  - Alert if burning too fast
```

**Error budget policy:**
```yaml
If error budget > 50%:
  - Focus on new features
  - Take risks with deployments
  - Optimize for velocity

If error budget < 50%:
  - Focus on reliability
  - Slow down deployments
  - Fix stability issues

If error budget exhausted:
  - Feature freeze
  - All hands on reliability
  - No deployments except fixes
```

## Best Practices Summary

### Metrics
- Use RED method for services
- Use USE method for resources
- Set up SLO tracking
- Monitor error budgets
- Track deployment metrics

### Logs
- Use structured logging (JSON)
- Include trace context
- Log at appropriate levels
- Never log secrets
- Aggregate centrally

### Tracing
- Propagate trace context
- Sample appropriately
- Tag spans with context
- Use for distributed debugging

### Alerting
- Alert on symptoms, not causes
- Include runbook links
- Avoid alert fatigue
- Use appropriate severity
- Make alerts actionable

### Dashboards
- Create service health dashboards
- Track SLO compliance
- Monitor resource utilization
- Share dashboards with team

### Health Checks
- Implement liveness and readiness
- Check dependencies
- Return detailed status
- Use for load balancer routing
