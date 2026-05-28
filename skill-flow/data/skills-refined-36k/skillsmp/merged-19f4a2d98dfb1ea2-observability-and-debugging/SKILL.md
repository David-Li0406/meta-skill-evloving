---
name: observability-and-debugging
description: Use this skill when diagnosing operation failures, debugging service connectivity issues, or investigating data loading problems in distributed systems.
---

# Observability & Debugging Common Issues

Load this skill when:
- Diagnosing operation failures, stuck operations, or slow operations
- Troubleshooting host service connectivity
- Debugging data loading issues
- Investigating worker selection or service communication problems
- Working with Jaeger traces or Grafana dashboards

## First Rule: Check Observability Before Logs

When users report issues with operations, use Jaeger first — not logs. KTRDR has comprehensive OpenTelemetry instrumentation that provides complete visibility into distributed operations.

This enables **first-response diagnosis** instead of iterative detective work.

---

## Debugging Priority

1. **Check Grafana dashboards** — Quick visual diagnostics
2. **Query Jaeger** — For operation-specific issues
3. **Check logs** — Only if observability doesn't have the answer

---

## Grafana Dashboards (First Stop)

**URL**: http://localhost:3000

| Dashboard | Path | Use Case |
|-----------|------|----------|
| System Overview | `/d/ktrdr-system-overview` | Service health, error rates, latency |
| Worker Status | `/d/ktrdr-worker-status` | Worker capacity, resource usage |
| Operations | `/d/ktrdr-operations` | Operation counts, success rates |

### Quick Checks

- **"Is it working?"** → System Overview: Healthy Services count
- **"Why is it slow?"** → System Overview: P95 Latency panel
- **"Workers missing?"** → Worker Status: Healthy Workers and Health Matrix
- **"Operations failing?"** → Operations: Success Rate and Status Distribution

---

## When to Query Jaeger

Query Jaeger when user reports:

| Symptom | What Jaeger Shows |
|---------|-------------------|
| "Operation stuck" | Which phase is stuck and why |
| "Operation failed" | Exact error with full context |
| "Operation slow" | Bottleneck span immediately |
| "No workers selected" | Worker selection decision |
| "Missing data" | Data flow from IB to cache |
| "Service not responding" | HTTP call attempt and result |

### Quick Start Workflow

1. **Get operation ID** from CLI output or API response (e.g., `op_training_20251113_123456_abc123`).
2. **Query Jaeger API**:
   ```bash
   OPERATION_ID="op_training_20251113_123456_abc123"
   curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID&limit=1" | jq
   ```
3. **Analyze trace structure**:
   ```bash
   curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID" | jq '
     .data[0].spans[] |
     {
       span: .operationName,
       service: .process.serviceName,
       duration_ms: (.duration / 1000),
       error: ([.tags[] | select(.key == "error" and .value == "true")] | length > 0)
     }' | jq -s 'sort_by(.duration_ms) | reverse'
   ```

---

## Common Diagnostic Patterns

### Pattern 1: Operation Stuck

```bash
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  select(.operationName == "worker_registry.select_worker") |
  .tags[] |
  select(.key | startswith("worker_registry.")) |
  {key: .key, value: .value}'
```

### Pattern 2: Operation Failed

```bash
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  select(.tags[] | select(.key == "error" and .value == "true")) |
  {
    span: .operationName,
    service: .process.serviceName,
    exception_type: (.tags[] | select(.key == "exception.type") | .value),
    exception_message: (.tags[] | select(.key == "exception.message") | .value)
  }'
```

### Pattern 3: Operation Slow

```bash
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  {
    span: .operationName,
    duration_ms: (.duration / 1000)
  }' | jq -s 'sort_by(.duration_ms) | reverse | .[0]'
```

### Pattern 4: Service Communication Failure

```bash
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  select(.operationName | startswith("POST") or startswith("GET")) |
  {
    http_call: .operationName,
    url: (.tags[] | select(.key == "http.url") | .value),
    status: (.tags[] | select(.key == "http.status_code") | .value),
    error: (.tags[] | select(.key == "error.type") | .value)
  }'
```

---

## Host Services Not Working

### Check if services are running

```bash
lsof -i :5001  # IB Host Service
lsof -i :5002  # Training Host Service
```

### Test connectivity from Docker

```bash
docker exec ktrdr-backend curl http://host.docker.internal:5001/health
docker exec ktrdr-backend curl http://host.docker.internal:5002/health
```

### Check logs

```bash
tail -f ib-host-service/logs/ib-host-service.log
tail -f training-host-service/logs/training-host-service.log
```

### Common issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Connection refused | Service not running | Start the service |
| Timeout | Wrong URL or firewall | Check `host.docker.internal` works |
| 500 errors | Service crashed | Check service logs |

---

## Data Loading Issues

### Common root causes

1. **IB Gateway not running** (port 4002)
   ```bash
   lsof -i :4002
   ```

2. **IB Host Service not started**
   ```bash
   curl http://localhost:5001/health
   ```

3. **Symbol format incorrect**
   - Use IB format: `AAPL` not `AAPL.US`

4. **Date range outside available data**
   - Check IB has data for the requested range

5. **Timeframe not supported**
   - IB supports specific timeframes only

### Debug data flow

```bash
ktrdr data get-range AAPL 1d
ktrdr ib test-connection
ktrdr ib check-status
```

---

## Async/Await Issues

### "Function not working in async context"

**Wrong** — Wrap in try/except and return None:
```python
try:
    result = await something()
except:
    return None  # Hides the real problem
```

**Right** — Ensure proper async/await chain:
```python
async def caller():
    result = await async_function()  # Must be awaited
    return result
```

### Common async mistakes

- Forgetting `await` on async functions
- Mixing sync and async code incorrectly
- Not using `asyncio.to_thread()` for blocking operations

---

## Test Failures

### Unit tests failing

```bash
make test-unit PYTEST_ARGS="-v"
```

### Integration tests failing

```bash
docker-compose ps
make test-integration PYTEST_ARGS="-v -s"
```

### Common test issues

- Missing fixtures → Check `conftest.py`
- Database state → Tests may need isolation
- Async issues → Ensure `@pytest.mark.asyncio` decorator

---

## Quick Diagnostic Commands

```bash
docker-compose ps
curl http://localhost:8000/health | jq
curl http://localhost:8000/api/v1/workers | jq
curl http://localhost:8000/api/v1/operations | jq
docker-compose logs --tail=100 backend
docker stats --no-stream
```

---

## Response Template

When diagnosing with observability, use this structure:

```
🔍 **Trace Analysis for operation_id: {operation_id}**

**Trace Summary**:
- Trace ID: {trace_id}
- Total Duration: {duration_ms}ms
- Services: {list of services}
- Status: {OK/ERROR}

**Execution Flow**:
1. {span_name} ({service}) - {duration_ms}ms
2. {span_name} ({service}) - {duration_ms}ms
...

**Diagnosis**:
{identified_issue_with_evidence_from_spans}

**Root Cause**:
{root_cause_explanation_with_span_attributes}

**Solution**:
{recommended_fix_with_commands}
```

---

## Full Documentation

For comprehensive workflows and scenarios:
[docs/debugging/observability-debugging-workflows.md](docs/debugging/observability-debugging-workflows.md)