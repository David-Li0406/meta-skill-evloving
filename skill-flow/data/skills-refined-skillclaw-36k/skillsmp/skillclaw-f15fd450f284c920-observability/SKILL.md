---
name: observability
description: Use this skill when implementing monitoring, debugging production issues, or setting up alerts through logging, metrics, and tracing.
---

# Observability Skill

## Three Pillars of Observability

### 1. Logs
- **What happened**: Discrete events with context
- **Use for**: Debugging, audit trails, error investigation
- **Challenge**: Volume and searchability

### 2. Metrics
- **How much/how often**: Numeric measurements over time
- **Use for**: Dashboards, alerting, capacity planning
- **Challenge**: Cardinality explosion

### 3. Traces
- **Where time was spent**: Request flow across services
- **Use for**: Latency analysis, dependency mapping
- **Challenge**: Sampling and storage

## Structured Logging

### Log Format
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "error",
  "message": "Payment failed",
  "service": "payment-service",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "user_789",
  "error": {
    "type": "PaymentDeclined",
    "code": "INSUFFICIENT_FUNDS"
  },
  "duration_ms": 234
}
```

### Log Levels
| Level | Use Case |
|-------|----------|
| ERROR | Failures requiring attention |
| WARN | Unexpected but recoverable |
| INFO | Business events, state changes |
| DEBUG | Development troubleshooting |
| TRACE | Fine-grained diagnostic |

### Best Practices
- Use structured JSON format
- Include correlation IDs (trace_id)
- Never log sensitive data (PII, secrets)
- Use consistent field names
- Set appropriate log levels

## Metrics Design

### Types of Metrics
| Type | Example | Use Case |
|------|---------|----------|
| Counter | requests_total | Monotonically increasing |
| Gauge | temperature_celsius | Value that goes up/down |
| Histogram | request_duration_seconds | Distribution of values |
| Summary | request_latency_quantiles | Quantile calculations |

### Naming Convention
```
<namespace>_<name>_<unit>

Examples:
- http_requests_total
- http_request_duration_seconds
- db_connections_active
- queue_messages_waiting
```

### RED Method (Services)
- **R**ate: Requests per second
- **E**rror: Error rate
- **D**uration: Latency distribution

### USE Method (Resources)
- **U**tilization: % time busy
- **S**aturation: Queue depth
- **E**rrors: Error count

### Golden Signals
1. Latency (response time)
2. Traffic (requests/sec)
3. Errors (error rate)
4. Saturation (resource utilization)

## Distributed Tracing

### Trace Structure
- Traces provide insights into the flow of requests through services, helping identify bottlenecks and performance issues.