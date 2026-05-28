# Monitoring Setup Template

**Document ID:** P8-MON-{XXX}  
  
**Service:** {Service Name}  
**Author:** {SRE Lead}  

---

## 1. Monitoring Strategy

### 1.1 Monitoring Objectives

| Objective | Description |
|-----------|-------------|
| Availability | Detect service outages within 1 minute |
| Performance | Track latency and throughput |
| Errors | Alert on error rate spikes |
| Saturation | Monitor resource utilization |

### 1.2 Four Golden Signals

| Signal | Metrics |
|--------|---------|
| **Latency** | Request duration, DB query time |
| **Traffic** | Requests/second, active users |
| **Errors** | HTTP 5xx, exception count |
| **Saturation** | CPU%, Memory%, Queue depth |

---

## 2. Metrics Configuration

### 2.1 Application Metrics

| Metric | Type | Labels | Alert Threshold |
|--------|------|--------|-----------------|
| http_requests_total | Counter | method, path, status | N/A |
| http_request_duration_seconds | Histogram | method, path | p95 > 500ms |
| active_connections | Gauge | - | > 1000 |
| error_count | Counter | type, service | > 100/min |

### 2.2 Infrastructure Metrics

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| CPU utilization | Node exporter | > 80% for 5min |
| Memory utilization | Node exporter | > 85% |
| Disk usage | Node exporter | > 80% |
| Network I/O | Node exporter | > 80% capacity |

### 2.3 Business Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| orders_created | Orders per minute | < 10/min (low) |
| payment_success_rate | Payment success % | < 95% |
| user_signups | New registrations | Anomaly detection |

---

## 3. Alert Configuration

### 3.1 Alert Rules

```yaml
# High Error Rate
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: High error rate detected
    description: Error rate is {{ $value | printf "%.2f" }}%

# High Latency
- alert: HighLatency
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: High latency detected
    description: P95 latency is {{ $value | printf "%.2f" }}s

# Service Down
- alert: ServiceDown
  expr: up{job="api-server"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: Service is down
    description: {{ $labels.instance }} is unreachable
```

### 3.2 Alert Routing

| Severity | Channel | Notification | Hours |
|----------|---------|--------------|-------|
| Critical | PagerDuty | Page + Slack | 24/7 |
| Warning | Slack | Slack only | 24/7 |
| Info | Slack | Slack only | Business hours |

---

## 4. Dashboard Configuration

### 4.1 Overview Dashboard

**Panels:**
1. Service Health Status
2. Request Rate (requests/second)
3. Error Rate (%)
4. Latency Distribution (p50, p95, p99)
5. Active Users
6. Resource Utilization (CPU, Memory, Disk)

### 4.2 Dashboard JSON

```json
{
  "title": "Service Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(http_requests_total[5m])",
          "legendFormat": "{{method}} {{path}}"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "singlestat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
        }
      ],
      "thresholds": "1,5"
    }
  ]
}
```

---

## 5. Log Configuration

### 5.1 Log Format

```json
{
  "timestamp": "2026-01-21T10:30:00.000Z",
  "level": "INFO",
  "service": "api-server",
  "trace_id": "abc123",
  "span_id": "def456",
  "message": "Request processed",
  "method": "GET",
  "path": "/api/products",
  "status": 200,
  "duration_ms": 45,
  "user_id": "usr_123"
}
```

### 5.2 Log Levels

| Level | Usage | Retention |
|-------|-------|-----------|
| ERROR | Errors requiring attention | 90 days |
| WARN | Potential issues | 30 days |
| INFO | Normal operations | 14 days |
| DEBUG | Detailed debugging | 7 days |

### 5.3 Important Log Queries

```
# Errors in last hour
level:ERROR AND @timestamp:[now-1h TO now]

# Slow requests
duration_ms:>1000 AND @timestamp:[now-1h TO now]

# Specific user activity
user_id:"usr_123" AND @timestamp:[now-24h TO now]

# Failed authentications
message:"authentication failed" AND @timestamp:[now-1h TO now]
```

---

## 6. Tracing Configuration

### 6.1 Tracing Setup

| Component | Instrumentation |
|-----------|-----------------|
| HTTP Server | Auto-instrumented |
| Database | Query tracing enabled |
| External APIs | Propagate context |
| Message queues | Producer/consumer spans |

### 6.2 Sampling Rules

| Condition | Sample Rate |
|-----------|-------------|
| Error responses | 100% |
| Slow requests (> 1s) | 100% |
| Normal requests | 1% |

---

## 7. Health Checks

### 7.1 Endpoints

| Endpoint | Purpose | Frequency |
|----------|---------|-----------|
| /health | Basic liveness | 10s |
| /ready | Readiness check | 10s |
| /health/detailed | Full health with deps | 30s |

### 7.2 Health Check Response

```json
{
  "status": "healthy",
  "timestamp": "2026-01-21T10:30:00Z",
  "version": "1.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "latency_ms": 5
    },
    "cache": {
      "status": "healthy",
      "latency_ms": 1
    },
    "external_api": {
      "status": "healthy",
      "latency_ms": 50
    }
  }
}
```

---

## 8. On-Call Setup

### 8.1 Rotation Schedule

| Day | Primary | Secondary |
|-----|---------|-----------|
| Mon-Tue | {Name A} | {Name B} |
| Wed-Thu | {Name B} | {Name C} |
| Fri-Sun | {Name C} | {Name A} |

### 8.2 Escalation Policy

| Level | Wait Time | Contact |
|-------|-----------|---------|
| L1 | 0 min | Primary on-call |
| L2 | 15 min | Secondary on-call |
| L3 | 30 min | Engineering Manager |
| L4 | 60 min | VP Engineering |

---

## 9. Maintenance Windows

| Window | Time (UTC) | Frequency | Purpose |
|--------|------------|-----------|---------|
| Patch Tuesday | Tue 02:00-04:00 | Weekly | Security patches |
| Database maintenance | Sun 03:00-05:00 | Monthly | Vacuum, reindex |
| Full DR test | First Sat 02:00-06:00 | Quarterly | DR validation |

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
