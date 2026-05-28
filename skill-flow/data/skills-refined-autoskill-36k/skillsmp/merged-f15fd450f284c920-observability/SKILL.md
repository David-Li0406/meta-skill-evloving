---
name: observability
description: Use this skill when implementing monitoring, debugging production issues, or setting up alerts through logging, metrics, tracing, and alerting patterns.
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
  "timestamp": "<timestamp>",
  "level": "<log_level>",
  "message": "<log_message>",
  "service": "<service_name>",
  "trace_id": "<trace_id>",
  "span_id": "<span_id>",
  "user_id": "<user_id>",
  "error": {
    "type": "<error_type>",
    "code": "<error_code>"
  },
  "duration_ms": <duration>
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
| Counter | <metric_name>_total | Monotonically increasing |
| Gauge | <metric_name> | Value that goes up/down |
| Histogram | <metric_name> | Distribution of values |
| Summary | <metric_name> | Quantile calculations |

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
```
Trace (trace_id: <trace_id>)
├── Span: HTTP Request (span_id: <span_id>, parent: null)
│   ├── Span: Auth Check (span_id: <span_id>, parent: <parent_span_id>)
│   ├── Span: DB Query (span_id: <span_id>, parent: <parent_span_id>)
│   │   └── Span: Connection Pool (span_id: <span_id>, parent: <parent_span_id>)
│   └── Span: External API (span_id: <span_id>, parent: <parent_span_id>)
```

### Context Propagation
```
# HTTP Headers
traceparent: <traceparent>
tracestate: <tracestate>
```

### Sampling Strategies
| Strategy | Use Case |
|----------|----------|
| Always sample | Development, low traffic |
| Probabilistic | Production (1-10%) |
| Rate limiting | Control volume |
| Tail-based | Capture errors/slow requests |

## Alerting

### Alert Design
```yaml
# Good alert
name: <alert_name>
expr: <alert_expression>
for: <duration>
severity: <severity_level>
annotations:
  summary: "<alert_summary>"
  runbook: "<runbook_url>"
```

### Alert Quality
- **Actionable**: Clear remediation steps
- **Relevant**: Indicates real problems
- **Timely**: Fast enough to matter
- **Not noisy**: Avoid alert fatigue

### SLOs and Error Budgets
```
SLI: <SLI_description>
SLO: <SLO_description>
Error Budget: <error_budget>
```

## Dashboards

### Layout Principles
1. **Overview first**: Key metrics at top
2. **Then details**: Drill-down sections
3. **Time alignment**: Consistent time ranges
4. **Annotations**: Mark deployments/incidents

### Essential Panels
- Request rate (traffic)
- Error rate (errors)
- Latency percentiles (P50, P95, P99)
- Resource utilization (CPU, memory)
- Queue depths (saturation)