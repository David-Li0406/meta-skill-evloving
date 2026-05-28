# Workflow: Setup Monitoring and Observability

## Purpose
Establish comprehensive monitoring, logging, and alerting systems that provide visibility into application health, performance, and issues. This workflow creates production-grade observability following DevOps best practices.

## When to Use
- Setting up monitoring for a new application
- Adding observability to existing applications
- Improving monitoring coverage
- Implementing SLOs and error budgets
- Troubleshooting production issues

## Prerequisites
- Application is deployed and running
- Access to monitoring infrastructure (or cloud provider)
- Understanding of key application metrics
- On-call rotation established (or planned)

## Workflow Steps

### 1. Define Observability Strategy

**The Three Pillars of Observability:**
1. **Metrics** - Numerical measurements over time
2. **Logs** - Discrete events and messages
3. **Traces** - Request flow through distributed systems

**Ask clarifying questions:**
- "What are the critical user flows we need to monitor?"
- "What is the expected request rate and response time?"
- "What constitutes a service outage for this application?"
- "Who should be alerted when issues occur?"
- "What is the target uptime/availability?"

### 2. Identify Key Metrics

**RED Method (for request-driven services):**
- **Rate**: Requests per second
- **Errors**: Failed requests per second
- **Duration**: Response time distribution

**USE Method (for resource monitoring):**
- **Utilization**: How busy is the resource (CPU, memory, disk)
- **Saturation**: Queue depth, wait time
- **Errors**: Error count and rate

**Application-specific metrics:**
- Business metrics (signups, transactions, revenue)
- Custom application metrics
- Database query performance
- Cache hit rates
- Queue depths

**Load pattern metrics:**
```yaml
Standard metrics to collect:
- Request rate (per endpoint)
- Response time (p50, p95, p99)
- Error rate (by status code)
- CPU usage (per pod/instance)
- Memory usage (per pod/instance)
- Disk I/O
- Network I/O
- Database connection pool utilization
- Cache hit/miss ratio
```

### 3. Setup Metrics Collection

**For Prometheus (recommended):**

**Install Prometheus:**
```yaml
# Kubernetes (using Helm)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

**Configure application metrics:**
```yaml
# Add Prometheus client library to application
# Node.js: prom-client
# Python: prometheus_client
# Go: github.com/prometheus/client_golang

# Expose metrics endpoint at /metrics
# Configure Prometheus to scrape endpoint
```

**Example Prometheus configuration:**
```yaml
scrape_configs:
  - job_name: 'my-application'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: my-app
    scrape_interval: 15s
    scrape_timeout: 10s
```

**For cloud platforms:**
```yaml
# AWS CloudWatch
# GCP Cloud Monitoring
# Azure Monitor
# Use platform-native monitoring tools
# Configure metric collection and dashboards
```

### 4. Implement Application Instrumentation

**Add metrics to application code:**

**Request metrics:**
```javascript
// Example: Node.js with prom-client
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

// Instrument request handler
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.route, status_code: res.statusCode });
  });
  next();
});
```

**Custom business metrics:**
```javascript
const userSignups = new prometheus.Counter({
  name: 'user_signups_total',
  help: 'Total number of user signups'
});

// Increment on user signup
userSignups.inc();
```

**Database metrics:**
```javascript
const dbQueryDuration = new prometheus.Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query duration',
  labelNames: ['query_type']
});
```

### 5. Setup Logging

**Structured logging best practices:**

**Use structured log format (JSON):**
```json
{
  "timestamp": "2025-12-09T10:30:00Z",
  "level": "error",
  "message": "Failed to process payment",
  "user_id": "12345",
  "transaction_id": "abc-123",
  "error": "Payment gateway timeout",
  "duration_ms": 5000
}
```

**Log levels:**
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARN**: Warning messages, potential issues
- **ERROR**: Error messages, failures
- **FATAL**: Critical errors, service down

**What to log:**
- Request/response details
- Errors and exceptions
- Authentication events
- Database queries (with duration)
- External API calls
- Business events (signup, purchase, etc.)

**What NOT to log:**
- Passwords or secrets
- Personally identifiable information (PII)
- Credit card numbers
- Session tokens

**Log aggregation setup:**

**For Kubernetes (ELK Stack or Loki):**
```yaml
# Option 1: ELK Stack (Elasticsearch, Logstash, Kibana)
# Deploy Filebeat as DaemonSet to collect logs
# Send to Elasticsearch for indexing
# View in Kibana

# Option 2: Loki (lightweight alternative)
# Deploy Promtail as DaemonSet
# Send to Loki for storage
# View in Grafana
```

**For cloud platforms:**
```yaml
# AWS: CloudWatch Logs
# GCP: Cloud Logging
# Azure: Azure Monitor Logs
# Configure log forwarding from application
```

### 6. Setup Distributed Tracing (for microservices)

**When to implement tracing:**
- Multiple microservices
- Complex request flows
- Need to identify bottlenecks
- Debugging distributed failures

**Tracing solutions:**
- Jaeger
- Zipkin
- AWS X-Ray
- Google Cloud Trace

**Implement tracing:**
```javascript
// Example: Jaeger with Node.js
const initTracer = require('jaeger-client').initTracer;

const config = {
  serviceName: 'my-service',
  sampler: { type: 'const', param: 1 }
};

const tracer = initTracer(config);

// Instrument requests
app.use((req, res, next) => {
  const span = tracer.startSpan('http_request');
  span.setTag('http.method', req.method);
  span.setTag('http.url', req.url);

  res.on('finish', () => {
    span.setTag('http.status_code', res.statusCode);
    span.finish();
  });

  next();
});
```

### 7. Create Dashboards

**Setup Grafana dashboards:**

**Dashboard categories:**
1. **System Health Dashboard**
   - Overall service status
   - Request rate and error rate
   - Response time (p50, p95, p99)
   - Instance health

2. **Resource Utilization Dashboard**
   - CPU usage per instance
   - Memory usage and trends
   - Disk I/O
   - Network bandwidth

3. **Application Metrics Dashboard**
   - Business metrics
   - User activity
   - Feature usage
   - Database performance

4. **Error Tracking Dashboard**
   - Error rate by type
   - Failed requests by endpoint
   - Exception tracking
   - Alert status

**Dashboard best practices:**
- Use consistent color schemes
- Show trends over time (last 24h, 7d, 30d)
- Include comparison to baseline
- Highlight SLO thresholds
- Keep dashboards focused and readable

**Example dashboard panels:**
```yaml
Request Rate:
  - Query: rate(http_requests_total[5m])
  - Visualization: Time series graph

Error Rate:
  - Query: rate(http_requests_total{status=~"5.."}[5m])
  - Visualization: Time series with alert threshold

Response Time (p95):
  - Query: histogram_quantile(0.95, http_request_duration_seconds)
  - Visualization: Time series graph
```

### 8. Configure Alerting

**Alerting principles:**
- Alert on symptoms, not causes
- Reduce noise (avoid alert fatigue)
- Make alerts actionable
- Include context and runbook links
- Set appropriate thresholds and durations

**Define alert rules:**

**Critical alerts (page on-call):**
```yaml
# High error rate
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value | humanize }}% for 5 minutes"
    runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

# Service down
- alert: ServiceDown
  expr: up{job="my-service"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Service is down"
    description: "{{ $labels.instance }} has been down for 1 minute"
```

**Warning alerts (notify, don't page):**
```yaml
# Elevated error rate
- alert: ElevatedErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "Elevated error rate detected"
    description: "Error rate is {{ $value | humanize }}% for 15 minutes"

# High memory usage
- alert: HighMemoryUsage
  expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.8
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "High memory usage"
    description: "Memory usage is {{ $value | humanizePercentage }} for 10 minutes"
```

**Configure alert routing:**
```yaml
# Prometheus Alertmanager configuration
route:
  group_by: ['alertname', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'team-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<key>'
  - name: 'slack'
    slack_configs:
      - api_url: '<webhook-url>'
        channel: '#alerts'
```

### 9. Implement Health Checks

**Application health endpoint:**
```javascript
// Express.js example
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    checks: {}
  };

  // Database check
  try {
    await db.ping();
    health.checks.database = 'healthy';
  } catch (error) {
    health.checks.database = 'unhealthy';
    health.status = 'unhealthy';
  }

  // External API check
  try {
    await externalAPI.ping();
    health.checks.externalAPI = 'healthy';
  } catch (error) {
    health.checks.externalAPI = 'degraded';
  }

  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

**Kubernetes probes:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2
```

### 10. Document Monitoring Setup

**Create monitoring documentation:**
```markdown
# Monitoring Documentation

## Dashboards
- [Service Health](link-to-grafana-dashboard)
- [Resource Utilization](link-to-grafana-dashboard)
- [Application Metrics](link-to-grafana-dashboard)

## Key Metrics
- Request rate: Normal range 100-500 req/s
- Error rate: Target < 1%
- Response time p95: Target < 500ms
- CPU usage: Normal range 30-60%
- Memory usage: Normal range 40-70%

## Alerts
- Critical: Page on-call engineer
- Warning: Post to Slack #alerts channel

## Runbooks
- [High Error Rate Runbook](link)
- [Service Down Runbook](link)
- [High Memory Usage Runbook](link)

## Troubleshooting
[Common monitoring issues and solutions]
```

## Deliverables

**Monitoring infrastructure:**
- Prometheus/monitoring system deployed and configured
- Grafana dashboards created
- Log aggregation system operational
- Alerting configured and tested

**Application instrumentation:**
- Metrics endpoint exposing key metrics
- Structured logging implemented
- Health check endpoints created
- Distributed tracing (if applicable)

**Documentation:**
- Monitoring setup guide
- Dashboard descriptions
- Alert runbooks
- Troubleshooting guide

## Validation Checklist

Before completing this workflow:
- [ ] Metrics are being collected and visible
- [ ] Dashboards display current data
- [ ] Logs are aggregated and searchable
- [ ] Alerts fire when thresholds breached (test!)
- [ ] Health checks respond correctly
- [ ] On-call receives test alert
- [ ] Runbooks are accessible and actionable
- [ ] Team trained on monitoring tools
- [ ] SLOs defined and tracked
- [ ] Documentation is complete

## Common Patterns

**Reference these context files:**
- `context/patterns/monitoring-patterns.md` - Monitoring approaches and best practices

## Troubleshooting

**Metrics not appearing:**
- Verify Prometheus can reach metrics endpoint
- Check application is exposing /metrics
- Review Prometheus scrape configuration
- Check for network/firewall issues

**Dashboards showing no data:**
- Verify Prometheus is collecting metrics
- Check Grafana data source configuration
- Verify query syntax is correct
- Check time range selection

**Alerts not firing:**
- Test alert rule manually in Prometheus
- Verify Alertmanager is running
- Check alert routing configuration
- Verify notification channels are configured

**Logs not appearing:**
- Verify log shipper is running
- Check log format is parsable
- Verify network connectivity to log aggregator
- Check for log volume limits

## Success Metrics

A successful monitoring setup achieves:
- **Complete visibility** - All key metrics tracked
- **Fast detection** - Issues detected in < 5 minutes
- **Actionable alerts** - Each alert has clear runbook
- **Low noise** - Alert fatigue avoided (< 5 alerts/day)
- **Comprehensive logging** - All errors logged and searchable
- **Performance tracking** - SLOs defined and measured
- **Team confidence** - Team can troubleshoot using monitoring
