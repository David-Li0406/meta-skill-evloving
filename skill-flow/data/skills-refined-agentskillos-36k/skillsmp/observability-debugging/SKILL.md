---
name: observability-debugging
description: Debug and troubleshoot SEA-Forge™ services using OpenTelemetry traces, metrics, and logs. Use for investigating performance issues, distributed tracing, log analysis, and production incident response. Integrates with OTel Collector, OpenObserve, and Logfire.
license: Complete terms in LICENSE.txt
---

# Observability & Debugging

Debug SEA-Forge™ services using unified telemetry (traces, metrics, logs) with OpenTelemetry. This skill covers distributed tracing, performance investigation, and log analysis.

**For reference:** [Observability Handbook](../../../docs/handbooks/Observability_Handbook/README.md) | [SDS-030: Semantic Observability](../../../docs/specs/shared/sds/030-semantic-observability.md)

---

## When to Use This Skill

1. **Performance Issues**: Slow requests, high latency
2. **Errors/Failures**: 500 errors, exceptions, crashes
3. **Distributed Tracing**: Track requests across services
4. **Production Incidents**: Real-time troubleshooting
5. **Optimization**: Identify bottlenecks

---

## Quick Reference

### View Traces

```bash
# OpenObserve UI
http://localhost:5080

# Query traces with specific service
curl -X POST http://localhost:5080/api/v1/traces \
  -d '{"serviceName": "case-management"}'
```

### Query Metrics

```bash
# Counter metrics
cmmn_cases_active_total{type="research"}

# Histogram metrics
http_request_duration_seconds_bucket{le="0.5"}

# Gauge metrics
knowledge_graph_triples_total
```

### Search Logs

```bash
# Logfire structured logs
SELECT * FROM logs
WHERE level='ERROR'
  AND service='artifact-engine'
  AND timestamp > NOW() - INTERVAL '1 hour'
```

---

## Debugging Workflows

### 1. Slow Request Investigation

**Symptoms**: User reports slow page load

**Steps**:
1. Find trace ID from logs or HTTP headers
2. Query OpenObserve for trace
3. Identify slowest spans
4. Check for N+1 queries, external API calls
5. Correlate with metrics (CPU, memory)

### 2. Error Root Cause Analysis

**Symptoms**: 500 error reported

**Steps**:
1. Search logs for error message
2. Get trace ID from error context
3. Visualize full trace to see failure point
4. Check span attributes for exception details
5. Correlate with recent deployments

### 3. Performance Regression

**Symptoms**: Latency increased after deployment

**Steps**:
1. Compare p95 latency metrics before/after
2. Identify services with increased latency
3. Diff traces from both periods
4. Check for new database queries or API calls

---

## Integration with SEA-Forge™

### Semantic Envelope (SDS-030)

Every telemetry signal includes semantic context:

```python
# Traces include semantic refs
with tracer.start_as_current_span("generate_artifact") as span:
    span.set_attribute("sea.conceptId", "sea:CognitiveArtifact")
    span.set_attribute("sea.caseId", "case-2026-001")
    span.set_attribute("sea.boundedContext", "cognitive-extension")
```

### Case Management Correlation

Link observability to CMMN cases:

```python
# Log with case context
logger.info(
    "Task activated",
    extra={
        "caseId": "case-2026-001",
        "taskId": "task-003",
        "stageId": "whitelabeling"
    }
)
```

---

## References

- [Observability Handbook](../../../docs/handbooks/Observability_Handbook/README.md)
- [SDS-030: Semantic Observability](../../../docs/specs/shared/sds/030-semantic-observability.md)
- [Debugging Runbook](../../../docs/handbooks/Observability_Handbook/Runbooks/trace_debugging.md)
