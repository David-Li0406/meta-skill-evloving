---
name: debugging-and-observability
description: Use this skill when troubleshooting service connectivity, diagnosing operation failures, or investigating performance issues in distributed systems using Grafana and Jaeger.
---

# Skill body

## When to Use This Skill

Load this skill when:
- Troubleshooting host service connectivity
- Diagnosing operation failures, stuck operations, or slow operations
- Debugging data loading issues
- Investigating worker selection or service communication problems
- Working with Grafana dashboards or Jaeger traces

## Debugging Common Issues

### Step 1: Check Grafana Dashboards

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

### Step 2: Check Host Services

#### Check if services are running

```bash
lsof -i :5001  # IB Host Service
lsof -i :5002  # Training Host Service
```

#### Test connectivity from Docker

```bash
docker exec ktrdr-backend curl http://host.docker.internal:5001/health
docker exec ktrdr-backend curl http://host.docker.internal:5002/health
```

#### Check logs

```bash
tail -f ib-host-service/logs/ib-host-service.log
tail -f training-host-service/logs/training-host-service.log
```

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Connection refused | Service not running | Start the service |
| Timeout | Wrong URL or firewall | Check `host.docker.internal` works |
| 500 errors | Service crashed | Check service logs |

## Observability Workflow

### Step 1: Get Operation ID

From CLI output or API response (e.g., `op_training_20251113_123456_abc123`)

### Step 2: Query Jaeger API

```bash
OPERATION_ID="op_training_20251113_123456_abc123"
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID&limit=1" | jq
```

### Step 3: Analyze Trace Structure

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

### Step 4: Extract Relevant Attributes

```bash
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID" | jq '
  .data[0].spans[] |
  {
    span: .operationName,
    attributes: (.tags | map({key: .key, value: .value}) | from_entries)
  }'
```

## Environment Variable Issues

### Check What's Set in Docker Container

```bash
docker exec ktrdr-backend env | grep -E "(IB|TRAINING)"
```

### Common Problems

- `USE_IB_HOST_SERVICE` not set → Falls back to local