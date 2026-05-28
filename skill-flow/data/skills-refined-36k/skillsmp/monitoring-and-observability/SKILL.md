---
name: Monitoring and Observability
description: This skill should be used when the user asks to "set up monitoring", "configure alerts", "add logging", "implement observability", "set up Prometheus", "configure Grafana", "application monitoring", "infrastructure monitoring", "log aggregation", "metrics collection", or needs help with monitoring, alerting, and observability systems.
version: 1.0.0
---

# Monitoring and Observability

Comprehensive guidance for implementing monitoring, logging, and observability across applications and infrastructure.

## Three Pillars of Observability

| Pillar | Purpose | Tools |
|--------|---------|-------|
| **Metrics** | Quantitative measurements over time | Prometheus, Datadog, CloudWatch |
| **Logs** | Detailed event records | ELK Stack, Loki, CloudWatch Logs |
| **Traces** | Request flow across services | Jaeger, Zipkin, AWS X-Ray |

## Metrics Collection

### Prometheus Setup

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - 'alerts/*.yml'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Application Metrics

```python
# Python with prometheus_client
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

# Use in code
@app.route('/api/users')
def get_users():
    with REQUEST_LATENCY.labels(method='GET', endpoint='/api/users').time():
        # ... handler logic
        REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status=200).inc()
```

```javascript
// Node.js with prom-client
const client = require('prom-client');

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.route?.path, status_code: res.statusCode });
  });
  next();
});
```

### Key Metrics (RED Method)

| Metric | Description | Example |
|--------|-------------|---------|
| **Rate** | Requests per second | `rate(http_requests_total[5m])` |
| **Errors** | Error rate | `rate(http_requests_total{status=~"5.."}[5m])` |
| **Duration** | Response time | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` |

### USE Method (Resources)

| Metric | Description | Example |
|--------|-------------|---------|
| **Utilization** | % time busy | `avg(rate(node_cpu_seconds_total{mode!="idle"}[5m]))` |
| **Saturation** | Queue depth | `node_load1` |
| **Errors** | Error count | `rate(node_disk_io_time_weighted_seconds_total[5m])` |

## Logging

### Structured Logging

```python
# Python with structlog
import structlog

logger = structlog.get_logger()

logger.info(
    "user_login",
    user_id=user.id,
    ip_address=request.remote_addr,
    user_agent=request.headers.get('User-Agent')
)
```

```javascript
// Node.js with pino
const pino = require('pino');
const logger = pino({ level: 'info' });

logger.info({
  event: 'user_login',
  userId: user.id,
  ipAddress: req.ip,
  userAgent: req.headers['user-agent']
});
```

### Log Levels

| Level | When to Use |
|-------|-------------|
| `ERROR` | Failures requiring immediate attention |
| `WARN` | Potentially harmful situations |
| `INFO` | Important business events |
| `DEBUG` | Detailed diagnostic information |
| `TRACE` | Very detailed tracing |

### ELK Stack Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - 9200:9200

  logstash:
    image: logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:8.11.0
    ports:
      - 5601:5601
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
```

### Loki Configuration

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
  filesystem:
    directory: /loki/chunks
```

## Distributed Tracing

### OpenTelemetry Setup

```python
# Python with OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Use in code
@tracer.start_as_current_span("process_order")
def process_order(order_id):
    span = trace.get_current_span()
    span.set_attribute("order_id", order_id)
    # ... processing logic
```

### Trace Context Propagation

```python
# Propagate context to downstream services
from opentelemetry.propagate import inject

headers = {}
inject(headers)
response = requests.get("http://service-b/api", headers=headers)
```

## Grafana Dashboards

### Dashboard JSON Structure

```json
{
  "title": "Application Dashboard",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(http_requests_total[5m])",
          "legendFormat": "{{method}} {{endpoint}}"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
        }
      ]
    }
  ]
}
```

### Useful PromQL Queries

```promql
# Request rate by endpoint
sum by (endpoint) (rate(http_requests_total[5m]))

# 95th percentile latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Error percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# CPU usage by container
sum(rate(container_cpu_usage_seconds_total[5m])) by (container_name)

# Memory usage
container_memory_usage_bytes / container_spec_memory_limit_bytes * 100
```

## Alerting

### Prometheus Alerting Rules

```yaml
# alerts/application.yml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: Error rate is {{ $value | humanizePercentage }}

      - alert: HighLatency
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
          description: 95th percentile latency is {{ $value }}s

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: Service {{ $labels.job }} is down
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  slack_api_url: 'https://hooks.slack.com/services/...'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<service-key>'
```

## Health Checks

```python
@app.route('/health')
def health():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'external_api': check_external_api()
    }
    healthy = all(checks.values())
    return jsonify(checks), 200 if healthy else 503

@app.route('/ready')
def ready():
    # Check if app is ready to receive traffic
    return 'OK', 200

@app.route('/live')
def live():
    # Check if app is alive
    return 'OK', 200
```

## Additional Resources

### Reference Files

- **`references/promql-cheatsheet.md`** - PromQL query reference
- **`references/dashboard-templates.md`** - Grafana dashboard templates

### Example Files

- **`examples/prometheus-stack.yml`** - Complete Prometheus stack
- **`examples/otel-config.yaml`** - OpenTelemetry configuration
