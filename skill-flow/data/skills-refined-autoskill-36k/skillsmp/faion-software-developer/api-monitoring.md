# API Monitoring

**ID:** api-monitoring

## Problem

APIs fail silently without monitoring. Need visibility into health, performance, and errors.

## Framework

**Key Metrics:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Availability | 99.9% | < 99% |
| Response Time (p50) | < 100ms | > 200ms |
| Response Time (p95) | < 500ms | > 1s |
| Response Time (p99) | < 1s | > 2s |
| Error Rate | < 0.1% | > 1% |
| Rate Limit Hits | Low | Sudden spike |

## Health Check Endpoints

```python
from fastapi import FastAPI, Response
from datetime import datetime
import asyncpg
import aioredis

app = FastAPI()

@app.get("/health")
async def health_check():
    """Simple liveness probe."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health/ready")
async def readiness_check():
    """Comprehensive readiness probe."""
    checks = {}

    # Database
    try:
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            await pool.fetchval("SELECT 1")
        checks["database"] = {"status": "ok"}
    except Exception as e:
        checks["database"] = {"status": "error", "error": str(e)}

    # Redis
    try:
        redis = await aioredis.from_url(REDIS_URL)
        await redis.ping()
        checks["redis"] = {"status": "ok"}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)}

    # External API
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.stripe.com/health", timeout=5)
            checks["stripe"] = {"status": "ok" if r.status_code == 200 else "degraded"}
    except Exception as e:
        checks["stripe"] = {"status": "error", "error": str(e)}

    all_ok = all(c["status"] == "ok" for c in checks.values())

    return Response(
        content=json.dumps({
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }),
        status_code=200 if all_ok else 503,
        media_type="application/json"
    )
```

## Metrics Collection

```python
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
import time

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method
        status = response.status_code

        REQUEST_COUNT.labels(method, endpoint, status).inc()
        REQUEST_LATENCY.labels(method, endpoint).observe(latency)

        return response

app.add_middleware(MetricsMiddleware)

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## Logging

```python
import structlog
import uuid

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    log = logger.bind(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host
    )

    log.info("request_started")
    start = time.time()

    try:
        response = await call_next(request)
        log.info(
            "request_completed",
            status=response.status_code,
            duration_ms=round((time.time() - start) * 1000, 2)
        )
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        log.error("request_failed", error=str(e))
        raise
```

## Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency above 1s"

      - alert: HighRateLimitHits
        expr: rate(rate_limit_exceeded_total[5m]) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High rate of rate limit hits"
```

## Best Practices

- Implement both liveness and readiness probes
- Use structured logging (JSON)
- Include request ID in all logs
- Set up dashboards for key metrics
- Configure alerts for SLO breaches
- Monitor downstream dependencies
- Track business metrics alongside technical

## Agent

faion-api-agent
