---
skill: nexus-health-monitoring
description: Health checks, monitoring, metrics, and observability for Nexus platform
priority: HIGH
tags: [nexus, health, monitoring, metrics, observability]
---

# Nexus Health Monitoring

Monitor Nexus platform health, metrics, and performance.

## Basic Health Check

```python
from nexus import Nexus

app = Nexus()

# Check platform health
health = app.health_check()
print(f"Status: {health['status']}")
print(f"Workflows: {list(health['workflows'].keys())}")
```

## Health Endpoints

```bash
# Basic health check
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600,
  "workflows": 5,
  "active_sessions": 3
}

# Detailed health check
curl http://localhost:8000/health/detailed

# Response
{
  "status": "healthy",
  "components": {
    "api": {"status": "healthy", "latency": 12},
    "database": {"status": "healthy"},
    "cache": {"status": "healthy"}
  },
  "workflows": {
    "total": 5,
    "healthy": 5,
    "unhealthy": 0
  }
}
```

## Enable Monitoring

```python
app = Nexus(
    enable_monitoring=True,
    monitoring_interval=60  # Check every 60 seconds
)

# Configure monitoring backend
app.monitoring.backend = "prometheus"
app.monitoring.interval = 30
app.monitoring.metrics = ["requests", "latency", "errors"]
```

## Prometheus Metrics

```bash
# Prometheus metrics endpoint
curl http://localhost:8000/metrics

# Response (Prometheus format)
# HELP nexus_requests_total Total requests
# TYPE nexus_requests_total counter
nexus_requests_total{workflow="my-workflow"} 123

# HELP nexus_request_duration_seconds Request duration
# TYPE nexus_request_duration_seconds histogram
nexus_request_duration_seconds_bucket{le="0.1"} 50
nexus_request_duration_seconds_bucket{le="0.5"} 100
```

## Custom Health Checks

```python
# Add custom health check
@app.health_check_handler("database")
def check_database_health():
    try:
        # Check database connection
        db.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.health_check_handler("cache")
def check_cache_health():
    try:
        cache.ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## Workflow Health Monitoring

```python
class WorkflowHealthMonitor:
    def __init__(self, nexus_app):
        self.app = nexus_app

    def check_workflow_health(self, workflow_name):
        """Check if workflow is healthy"""
        try:
            # Test execution with minimal inputs
            result = self.app.execute_workflow(
                workflow_name,
                inputs={},
                timeout=5
            )
            return result['success']
        except:
            return False

    def get_all_workflow_health(self):
        """Get health status of all workflows"""
        health_status = {}
        for workflow_name in self.app.workflows:
            health_status[workflow_name] = self.check_workflow_health(workflow_name)
        return health_status

# Usage
monitor = WorkflowHealthMonitor(app)
status = monitor.get_all_workflow_health()
print(f"Workflow health: {status}")
```

## Alerting

```python
# Configure alerting
app.monitoring.enable_alerts = True
app.monitoring.alert_thresholds = {
    "error_rate": 0.05,  # 5% error rate
    "latency_p95": 1.0,  # 1 second p95 latency
    "availability": 0.99  # 99% availability
}

# Alert handlers
@app.on_alert("high_error_rate")
def handle_high_errors(alert):
    print(f"ALERT: High error rate: {alert.value}")
    # Send notification (email, Slack, PagerDuty, etc.)

@app.on_alert("high_latency")
def handle_high_latency(alert):
    print(f"ALERT: High latency: {alert.value}s")
```

## Logging

```python
import logging

# Configure logging
app = Nexus(
    log_level="INFO",
    log_format="json",
    log_file="nexus.log"
)

# Access logger
logger = app.logger
logger.info("Custom log message")
logger.error("Error occurred", extra={"workflow": "my-workflow"})
```

## Performance Metrics

```python
# Get performance metrics
metrics = app.get_metrics()

print(f"Total requests: {metrics['requests_total']}")
print(f"Avg latency: {metrics['latency_avg']}s")
print(f"Error rate: {metrics['error_rate']}%")
print(f"Success rate: {metrics['success_rate']}%")

# Per-workflow metrics
workflow_metrics = app.get_workflow_metrics("my-workflow")
print(f"Workflow executions: {workflow_metrics['executions']}")
print(f"Workflow success rate: {workflow_metrics['success_rate']}%")
```

## Best Practices

1. **Enable Monitoring in Production**
2. **Set Appropriate Alert Thresholds**
3. **Monitor All Components** (API, database, cache)
4. **Track Workflow-Specific Metrics**
5. **Use Structured Logging**
6. **Implement Graceful Degradation**
7. **Regular Health Checks**

## Key Takeaways

- Health checks available at /health endpoint
- Enable monitoring for production systems
- Custom health checks for components
- Prometheus metrics for observability
- Alerting for proactive monitoring
- Per-workflow health tracking

## Related Skills

- [nexus-enterprise-features](#) - Production features
- [nexus-production-deployment](#) - Deploy with monitoring
- [nexus-troubleshooting](#) - Fix health issues
