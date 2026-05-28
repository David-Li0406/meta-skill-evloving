---
id: prometheus-monitoring
name: "Prometheus Monitoring"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Prometheus Monitoring

## Overview

Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability. It collects metrics via a pull model, stores them in a time-series database, and provides powerful querying with PromQL. It's the de facto standard for Kubernetes monitoring.

## When to Use

- Kubernetes cluster monitoring
- Microservices observability
- Custom application metrics
- Infrastructure monitoring
- Alert management with Alertmanager

## Key Concepts

| Concept | Description |
|---------|-------------|
| Metric | Numeric measurement with timestamp |
| Label | Key-value pair for metric dimensions |
| Scrape | Process of collecting metrics from targets |
| Target | Endpoint exposing metrics |
| PromQL | Query language for Prometheus |
| Alert | Condition triggering notifications |
| Recording Rule | Pre-computed query stored as new metric |

### Metric Types

| Type | Description | Use Case |
|------|-------------|----------|
| Counter | Monotonically increasing value | Request count, errors |
| Gauge | Value that can go up and down | Temperature, queue size |
| Histogram | Samples in configurable buckets | Request duration |
| Summary | Quantiles over sliding window | Request duration (client-side) |

## Implementation

### Prometheus Stack Installation (Helm)

```yaml
# prometheus-values.yaml
prometheus:
  prometheusSpec:
    replicas: 2
    retention: 30d
    retentionSize: 50GB

    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi

    resources:
      requests:
        cpu: 500m
        memory: 2Gi
      limits:
        cpu: 2000m
        memory: 8Gi

    # External labels for federation
    externalLabels:
      cluster: production
      region: eu-central-1

    # Remote write for long-term storage
    remoteWrite:
      - url: https://thanos-receive.example.com/api/v1/receive
        writeRelabelConfigs:
          - sourceLabels: [__name__]
            regex: 'go_.*'
            action: drop

    # Additional scrape configs
    additionalScrapeConfigs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__

    # Rule selector
    ruleSelector:
      matchLabels:
        prometheus: main

alertmanager:
  alertmanagerSpec:
    replicas: 3
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 10Gi

  config:
    global:
      resolve_timeout: 5m
      slack_api_url: 'https://hooks.slack.com/services/xxx'

    route:
      group_by: ['alertname', 'namespace']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'slack-notifications'
      routes:
        - match:
            severity: critical
          receiver: 'pagerduty-critical'
          continue: true
        - match:
            severity: warning
          receiver: 'slack-warnings'
        - match_re:
            namespace: 'team-.*'
          receiver: 'team-notifications'
          group_by: ['alertname', 'namespace', 'team']

    receivers:
      - name: 'slack-notifications'
        slack_configs:
          - channel: '#alerts'
            send_resolved: true
            title: '{{ template "slack.title" . }}'
            text: '{{ template "slack.text" . }}'

      - name: 'slack-warnings'
        slack_configs:
          - channel: '#alerts-warning'
            send_resolved: true

      - name: 'pagerduty-critical'
        pagerduty_configs:
          - service_key: '<pagerduty-key>'
            send_resolved: true

      - name: 'team-notifications'
        slack_configs:
          - channel: '#team-{{ .GroupLabels.team }}-alerts'
            send_resolved: true

    templates:
      - '/etc/alertmanager/config/*.tmpl'

grafana:
  enabled: true
  adminPassword: ${GRAFANA_ADMIN_PASSWORD}

  persistence:
    enabled: true
    size: 10Gi

  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-prometheus:9090
          isDefault: true
        - name: Loki
          type: loki
          url: http://loki:3100

  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'default'
          folder: ''
          type: file
          options:
            path: /var/lib/grafana/dashboards/default

kubeStateMetrics:
  enabled: true

nodeExporter:
  enabled: true

prometheusOperator:
  enabled: true
```

### ServiceMonitor

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  namespace: production
  labels:
    prometheus: main
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s
      honorLabels: true
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'go_gc_.*'
          action: drop
  namespaceSelector:
    matchNames:
      - production
      - staging
```

### PodMonitor

```yaml
# podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: myapp-sidecar
  namespace: production
  labels:
    prometheus: main
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  podMetricsEndpoints:
    - port: sidecar-metrics
      path: /metrics
      interval: 15s
  namespaceSelector:
    matchNames:
      - production
```

### PrometheusRule

```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  namespace: production
  labels:
    prometheus: main
spec:
  groups:
    - name: myapp.rules
      interval: 30s
      rules:
        # Recording rules
        - record: myapp:request_rate:5m
          expr: sum(rate(http_requests_total{app="myapp"}[5m])) by (method, status)

        - record: myapp:error_rate:5m
          expr: |
            sum(rate(http_requests_total{app="myapp",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{app="myapp"}[5m]))

        - record: myapp:latency_p99:5m
          expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{app="myapp"}[5m])) by (le))

    - name: myapp.alerts
      rules:
        # High error rate
        - alert: MyAppHighErrorRate
          expr: myapp:error_rate:5m > 0.05
          for: 5m
          labels:
            severity: critical
            team: backend
          annotations:
            summary: "High error rate for MyApp"
            description: "Error rate is {{ $value | humanizePercentage }} (>5%)"
            runbook_url: https://runbooks.example.com/myapp-high-error-rate

        # High latency
        - alert: MyAppHighLatency
          expr: myapp:latency_p99:5m > 1
          for: 10m
          labels:
            severity: warning
            team: backend
          annotations:
            summary: "High P99 latency for MyApp"
            description: "P99 latency is {{ $value | humanizeDuration }}"

        # Pod restarts
        - alert: MyAppPodRestarts
          expr: increase(kube_pod_container_status_restarts_total{namespace="production",container="myapp"}[1h]) > 3
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "MyApp pod restarting frequently"
            description: "Pod {{ $labels.pod }} has restarted {{ $value }} times in the last hour"

        # Memory usage
        - alert: MyAppHighMemory
          expr: |
            container_memory_working_set_bytes{namespace="production",container="myapp"}
            / container_spec_memory_limit_bytes{namespace="production",container="myapp"}
            > 0.85
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "MyApp memory usage high"
            description: "Memory usage is {{ $value | humanizePercentage }} of limit"

        # CPU throttling
        - alert: MyAppCPUThrottling
          expr: |
            sum(increase(container_cpu_cfs_throttled_periods_total{namespace="production",container="myapp"}[5m]))
            /
            sum(increase(container_cpu_cfs_periods_total{namespace="production",container="myapp"}[5m]))
            > 0.25
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "MyApp CPU throttling detected"
            description: "CPU throttling at {{ $value | humanizePercentage }}"
```

### Application Instrumentation (Python)

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from functools import wraps
import time

# Metrics definitions
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'HTTP requests in progress',
    ['method', 'endpoint']
)

DB_CONNECTIONS = Gauge(
    'db_connections_active',
    'Active database connections'
)

APP_INFO = Info(
    'app',
    'Application information'
)

# Initialize app info
APP_INFO.info({
    'version': '1.0.0',
    'environment': 'production'
})


def track_request(method, endpoint):
    """Decorator to track request metrics"""
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
            start_time = time.time()

            try:
                result = await f(*args, **kwargs)
                status = getattr(result, 'status_code', 200)
                return result
            except Exception as e:
                status = 500
                raise
            finally:
                duration = time.time() - start_time
                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=endpoint,
                    status=status
                ).inc()
                REQUEST_LATENCY.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(duration)
                IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()

        return wrapper
    return decorator


# FastAPI integration
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/api/users")
@track_request("GET", "/api/users")
async def get_users():
    # ... implementation
    pass
```

### Application Instrumentation (Node.js)

```javascript
// metrics.js
const promClient = require('prom-client');

// Enable default metrics
promClient.collectDefaultMetrics({
  prefix: 'nodejs_',
  gcDurationBuckets: [0.001, 0.01, 0.1, 1, 2, 5],
});

// Custom metrics
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

const httpRequestsInProgress = new promClient.Gauge({
  name: 'http_requests_in_progress',
  help: 'HTTP requests in progress',
  labelNames: ['method', 'route'],
});

const dbConnectionsActive = new promClient.Gauge({
  name: 'db_connections_active',
  help: 'Active database connections',
});

// Express middleware
const metricsMiddleware = (req, res, next) => {
  const start = Date.now();
  const route = req.route?.path || req.path;

  httpRequestsInProgress.labels(req.method, route).inc();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;

    httpRequestsTotal.labels(req.method, route, res.statusCode).inc();
    httpRequestDuration.labels(req.method, route).observe(duration);
    httpRequestsInProgress.labels(req.method, route).dec();
  });

  next();
};

// Express setup
const express = require('express');
const app = express();

app.use(metricsMiddleware);

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

module.exports = {
  httpRequestsTotal,
  httpRequestDuration,
  dbConnectionsActive,
  register: promClient.register,
};
```

### Common PromQL Queries

```promql
# Request rate
sum(rate(http_requests_total[5m])) by (method, status)

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))
* 100

# P50, P90, P99 latency
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# CPU usage percentage
sum(rate(container_cpu_usage_seconds_total{namespace="production"}[5m])) by (pod)
/ sum(container_spec_cpu_quota{namespace="production"}/container_spec_cpu_period{namespace="production"}) by (pod)
* 100

# Memory usage percentage
container_memory_working_set_bytes{namespace="production"}
/ container_spec_memory_limit_bytes{namespace="production"}
* 100

# Pod restarts in last hour
increase(kube_pod_container_status_restarts_total[1h])

# Available replicas
kube_deployment_status_replicas_available{namespace="production"}

# Node CPU available
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) * 100

# Disk usage percentage
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# Network traffic
sum(rate(container_network_receive_bytes_total[5m])) by (pod)
sum(rate(container_network_transmit_bytes_total[5m])) by (pod)
```

## Best Practices

1. **Use recording rules** - Pre-compute expensive queries for dashboards
2. **Define SLIs/SLOs** - Measure service level indicators
3. **Label carefully** - High cardinality labels cause performance issues
4. **Set retention appropriately** - Balance storage vs history needs
5. **Use federation** - Aggregate metrics from multiple Prometheus instances
6. **Implement remote write** - Long-term storage with Thanos/Cortex
7. **Alert on symptoms** - Focus on user-facing impact, not causes
8. **Use histograms** - Prefer over summaries for aggregation
9. **Scrape consistently** - Standard intervals across all targets
10. **Document metrics** - Clear HELP strings for all metrics

## Common Pitfalls

1. **High cardinality labels** - Labels like user_id create millions of time series. Use bounded labels only.

2. **Alerting on causes not symptoms** - Alert on error rate, not individual errors.

3. **No recording rules** - Dashboard queries are slow. Pre-compute with recording rules.

4. **Inconsistent naming** - Follow naming conventions: `<namespace>_<name>_<unit>_total|bucket|sum|count`.

5. **Missing labels** - Insufficient context for debugging. Include relevant dimensions.

6. **No retention policy** - Disk fills up. Set retention time and size limits.

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Metric Naming](https://prometheus.io/docs/practices/naming/)
