# Temporal Python Production Deployment Guide

## Table of Contents
1. [Pre-Production Checklist](#pre-production-checklist)
2. [Worker Configuration](#worker-configuration)
3. [Scalability Strategy](#scalability-strategy)
4. [Monitoring and Observability](#monitoring-and-observability)
5. [Error Handling in Production](#error-handling-in-production)
6. [Deployment Strategies](#deployment-strategies)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)
9. [Disaster Recovery](#disaster-recovery)

---

## Pre-Production Checklist

### Code Quality

- [ ] All workflows tested with replay using production history
- [ ] Unit tests cover all workflow paths
- [ ] Integration tests with real activities passing
- [ ] No determinism violations in workflow code
- [ ] All activities are idempotent
- [ ] Activity timeouts configured appropriately
- [ ] Retry policies defined for all activities
- [ ] Search attributes configured for common queries
- [ ] Signals and queries documented
- [ ] Workflow versioning strategy in place

### Configuration

- [ ] Production Temporal server deployed and tested
- [ ] Task queues defined and documented
- [ ] Worker pools configured
- [ ] Metrics collection enabled
- [ ] Structured logging configured
- [ ] Alerting rules defined
- [ ] Graceful shutdown implemented
- [ ] Resource limits set (CPU, memory)
- [ ] Connection pooling configured
- [ ] TLS/mTLS enabled for secure connections

---

## Worker Configuration

### Basic Worker Setup

```python
from temporalio.worker import Worker
from temporalio.client import Client
from temporalio.runtime import Runtime, TelemetryConfig

# Configure runtime with metrics
runtime = Runtime(
    telemetry=TelemetryConfig(
        metrics=PrometheusConfig(
            bind_address="0.0.0.0:9090"
        ),
        logging=LoggingConfig(
            forward_to=[logging.getLogger()]
        )
    )
)

async def run_worker():
    client = await Client.connect(
        "temporal.production.example.com:7233",
        namespace="production",
        runtime=runtime
    )

    worker = Worker(
        client,
        task_queue="production-queue",
        workflows=[MyWorkflows],
        activities=[MyActivities],
        # Production worker settings
        max_concurrent_activities=50,
        max_concurrent_workflow_tasks=20,
        max_concurrent_local_activities=100,
        # Sticky queue settings
        sticky_queue_schedule_to_close_timeout=timedelta(seconds=10)
    )

    await worker.run()
```

### Worker Pools by Type

```python
# Workflow-only workers (stateless, scalable)
workflow_worker = Worker(
    client,
    task_queue="workflow-tasks",
    workflows=[AllMyWorkflows],
    activities=[],
    max_concurrent_workflow_tasks=50,
    max_concurrent_activities=0
)

# Activity workers (can be scaled independently)
activity_worker = Worker(
    client,
    task_queue="activity-tasks",
    workflows=[],
    activities=[IOIntensiveActivities],
    max_concurrent_workflow_tasks=5,
    max_concurrent_activities=100
)

# High-priority workers (for critical workflows)
priority_worker = Worker(
    client,
    task_queue="high-priority-tasks",
    workflows=[CriticalWorkflows],
    activities=[FastActivities],
    # Lower concurrency for faster response
    max_concurrent_workflow_tasks=10,
    max_concurrent_activities=20
)
```

### Graceful Shutdown

```python
import asyncio
import signal

class WorkerManager:
    def __init__(self, worker: Worker):
        self.worker = worker
        self.shutdown_event = asyncio.Event()

    async def run(self):
        # Set up signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, self._handle_signal)

        # Run worker until shutdown
        await self.worker.run_until(self.shutdown_event.is_set)

        # Graceful shutdown
        logger.info("Shutting down worker gracefully...")
        await self.worker.shutdown()
        logger.info("Worker shutdown complete")

    def _handle_signal(self, signum, frame):
        logger.info(f"Received signal {signum}, initiating shutdown")
        self.shutdown_event.set()

# Usage
manager = WorkerManager(worker)
await manager.run()
```

---

## Scalability Strategy

### Horizontal Scaling

```yaml
# Kubernetes Deployment Example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: temporal-activity-workers
spec:
  replicas: 10  # Scale based on load
  selector:
    matchLabels:
      app: temporal-activity-worker
  template:
    metadata:
      labels:
        app: temporal-activity-worker
    spec:
      containers:
      - name: worker
        image: my-temporal-worker:latest
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "2000m"
            memory: "2Gi"
        env:
        - name: TASK_QUEUE
          value: "production-activities"
```

### Auto-scaling Based on Queue Depth

```python
import kubernetes
from prometheus_client import Gauge

# Monitor task queue depth
queue_depth_gauge = Gauge(
    'temporal_task_queue_depth',
    'Task queue depth',
    ['task_queue']
)

async def scale_workers_based_on_queue():
    while True:
        # Get queue metrics
        stats = await client.get_task_queue_stats(
            "production-activities"
        )

        queue_depth = stats.backlog_count
        queue_depth_gauge.labels(
            task_queue="production-activities"
        ).set(queue_depth)

        # Scale workers based on depth
        if queue_depth > 1000:
            await scale_up_workers(target_replicas=20)
        elif queue_depth < 100:
            await scale_down_workers(target_replicas=5)

        await asyncio.sleep(60)
```

### Multi-Region Deployment

```python
# Regional workers
regions = ["us-east-1", "us-west-2", "eu-west-1"]

workers = []
for region in regions:
    # Connect to regional Temporal server
    client = await Client.connect(
        f"temporal.{region}.example.com:7233",
        namespace="production"
    )

    # Start regional workers
    worker = Worker(
        client,
        task_queue=f"{region}-tasks",
        workflows=[MyWorkflows],
        activities=[regional_activities]
    )

    workers.append(worker)

# Run all workers
await asyncio.gather(*[w.run() for w in workers])
```

---

## Monitoring and Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Custom workflow metrics
workflow_duration = Histogram(
    'temporal_workflow_duration_seconds',
    'Workflow execution duration',
    ['workflow_type', 'status']
)

activity_attempts = Counter(
    'temporal_activity_attempts_total',
    'Total activity attempts',
    ['activity_type', 'status']
)

active_workflows = Gauge(
    'temporal_active_workflows',
    'Currently active workflows',
    ['workflow_type']
)

# Use in workflows/activities
@workflow.defn
class MonitoredWorkflow:
    @workflow.run
    async def run(self, input_data: str) -> str:
        start_time = time.time()

        try:
            result = await workflow.execute_activity(
                monitored_activity,
                input_data,
                start_to_close_timeout=timedelta(seconds=30)
            )

            workflow_duration.labels(
                workflow_type="MonitoredWorkflow",
                status="success"
            ).observe(time.time() - start_time)

            return result

        except Exception as e:
            workflow_duration.labels(
                workflow_type="MonitoredWorkflow",
                status="error"
            ).observe(time.time() - start_time)
            raise
```

### Structured Logging

```python
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Use in workflows
@workflow.defn
class LoggedWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> None:
        log = workflow.logger.bind(
            workflow="LoggedWorkflow",
            order_id=order_id
        )

        log.info("Workflow started")

        try:
            await workflow.execute_activity(
                process_order,
                order_id,
                start_to_close_timeout=timedelta(seconds=30)
            )

            log.info("Order processed successfully")
        except Exception as e:
            log.error("Order processing failed", error=str(e))
            raise
```

### Distributed Tracing

```python
from temporalio.runtime import Runtime, OpenTelemetryConfig

# Configure OpenTelemetry tracing
runtime = Runtime(
    telemetry=TelemetryConfig(
        tracing=OpenTelemetryConfig(
            url="http://jaeger:4317",
            headers={"Authorization": "Bearer token"}
        )
    )
)

client = await Client.connect(
    "temporal.production:7233",
    runtime=runtime
)
```

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
- name: temporal_alerts
  rules:
  - alert: HighWorkflowFailureRate
    expr: |
      rate(temporal_workflow_failed_total[5m]) /
      rate(temporal_workflow_completed_total[5m]) > 0.05
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High workflow failure rate"

  - alert: HighActivityLatency
    expr: |
      histogram_quantile(0.95,
        rate(temporal_activity_execution_duration_seconds_bucket[5m])
      ) > 60
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "95th percentile activity latency > 60s"

  - alert: WorkerDown
    expr: up{job="temporal-worker"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Temporal worker is down"
```

---

## Error Handling in Production

### Application Errors vs. System Errors

```python
from temporalio.common import ApplicationError

@activity.defn
async def production_activity(input_data: dict) -> dict:
    try:
        result = await external_service.call(input_data)

        if result.is_client_error:
            # Client error - don't retry
            raise ApplicationError(
                f"Client error: {result.error}",
                type="ClientError",
                non_retryable=True
            )

        return result.data

    except TemporaryError as e:
        # Temporary error - retry with backoff
        raise ApplicationError(
            f"Temporary error: {e}",
            type="TemporaryError"
        )
```

### Deadlock Detection

```python
@workflow.defn
class SafeWorkflow:
    @workflow.run
    async def run(self, data: str) -> None:
        # Set timeout for entire workflow
        deadline = workflow.now() + timedelta(hours=1)

        while workflow.now() < deadline:
            try:
                result = await asyncio.wait_for(
                    workflow.execute_activity(
                        potentially_slow_activity,
                        data,
                        start_to_close_timeout=timedelta(minutes=5)
                    ),
                    timeout=timedelta(minutes=10)
                )

                if result.is_complete:
                    return result

            except asyncio.TimeoutError:
                workflow.logger.warning("Activity timeout, retrying")

        # Deadline exceeded
        raise ApplicationError("Workflow deadline exceeded")
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int, timeout: timedelta):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, activity_func, *args):
        if self.state == "open":
            if workflow.now() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise ApplicationError("Circuit breaker is open")

        try:
            result = await activity_func(*args)

            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0

            return result

        except Exception as e:
            self.failures += 1
            self.last_failure_time = workflow.now()

            if self.failures >= self.failure_threshold:
                self.state = "open"

            raise
```

---

## Deployment Strategies

### Blue-Green Deployment

```python
# 1. Deploy new version to green environment
green_client = await Client.connect("temporal-green:7233")
green_worker = Worker(
    green_client,
    task_queue="green-tasks",
    workflows=[NewVersionWorkflow],
    activities=[NewActivities]
)

# 2. Test new version
await test_green_environment(green_client)

# 3. Gradually shift traffic
shift_percentage = 0.0
while shift_percentage < 1.0:
    shift_percentage += 0.1

    await client.update_workflow_execution(
        "my-workflow-id",
        task_queue=f"ramped-tasks-{shift_percentage}"
    )

    await asyncio.sleep(300)  # Wait 5 minutes

# 4. Full cutover to green
# 5. Decommission blue environment
```

### Workflow Versioning Strategy

```python
@workflow.defn
class VersionedWorkflow:
    @workflow.run
    async def run(self, input_data: str) -> str:
        # Get workflow version
        version = await workflow.get_version(
            "feature-xyz",
            min_supported=1,
            max_supported=3
        )

        if version == 1:
            return await self._process_v1(input_data)
        elif version == 2:
            return await self._process_v2(input_data)
        else:  # version == 3
            return await self._process_v3(input_data)

    async def _process_v1(self, input_data: str) -> str:
        # Old implementation
        return await workflow.execute_activity(
            legacy_activity,
            input_data
        )

    async def _process_v2(self, input_data: str) -> str:
        # Middle implementation
        return await workflow.execute_activity(
            improved_activity,
            input_data
        )

    async def _process_v3(self, input_data: str) -> str:
        # New implementation
        return await workflow.execute_activity(
            optimized_activity,
            input_data
        )
```

---

## Performance Optimization

### Activity Worker Pool Tuning

```python
worker = Worker(
    client,
    task_queue="production-queue",
    workflows=[MyWorkflows],
    activities=[MyActivities],
    # Tune based on activity type
    max_concurrent_activities=100,  # For I/O-bound activities
    max_concurrent_workflow_tasks=20,
    max_concurrent_local_activities=200,  # For fast local activities
    # Worker thread pool
    max_worker_activities=50  # Internal worker threads
)
```

### Cache Frequently Accessed Data

```python
@workflow.defn
class CachedWorkflow:
    def __init__(self):
        self.cache = {}

    @workflow.run
    async def run(self, item_ids: list[str]) -> dict:
        results = {}

        for item_id in item_ids:
            # Check cache first
            if item_id in self.cache:
                results[item_id] = self.cache[item_id]
            else:
                # Fetch and cache
                result = await workflow.execute_activity(
                    get_item,
                    item_id,
                    start_to_close_timeout=timedelta(seconds=5)
                )

                self.cache[item_id] = result
                results[item_id] = result

        return results
```

### Use Local Activities for Fast Operations

```python
@workflow.defn
class OptimizedWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # Fast local operations (< 1 second)
        validated = await workflow.execute_local_activity(
            validate_data,
            data,
            start_to_close_timeout=timedelta(seconds=1)
        )

        transformed = await workflow.execute_local_activity(
            transform_data,
            validated,
            start_to_close_timeout=timedelta(seconds=1)
        )

        # Slow external operations
        result = await workflow.execute_activity(
            persist_to_database,
            transformed,
            start_to_close_timeout=timedelta(seconds=30)
        )

        return result
```

---

## Security Considerations

### TLS/mTLS Configuration

```python
from temporalio.client import TLSConfig

# Configure TLS
tls_config = TLSConfig(
    client_cert=open("client.pem", "rb").read(),
    client_private_key=open("client.key", "rb").read(),
    server_root_ca_cert=open("ca.pem", "rb").read(),
    domain="temporal.production.example.com"
)

client = await Client.connect(
    "temporal.production.example.com:7233",
    tls=tls_config,
    namespace="production"
)
```

### Namespace Isolation

```python
# Separate namespaces for different environments
prod_client = await Client.connect(
    "temporal.example.com:7233",
    namespace="production"
)

staging_client = await Client.connect(
    "temporal.example.com:7233",
    namespace="staging"
)

dev_client = await Client.connect(
    "temporal.example.com:7233",
    namespace="development"
)
```

### Activity Secrets Management

```python
import os
from cryptography.fernet import Fernet

@activity.defn
async def secure_activity(data: str) -> str:
    # Get secrets from secure environment
    api_key = os.getenv("API_KEY")  # From Kubernetes secrets
    encryption_key = os.getenv("ENCRYPTION_KEY")

    # Decrypt sensitive data
    fernet = Fernet(encryption_key)
    decrypted_data = fernet.decrypt(data)

    # Process with secure API
    result = await secure_api_call(api_key, decrypted_data)

    # Encrypt result
    encrypted_result = fernet.encrypt(result)

    return encrypted_result
```

---

## Disaster Recovery

### Workflow History Backup

```bash
# Backup Temporal database
pg_dump temporal_db > temporal_backup_$(date +%Y%m%d).sql

# Or use Temporal's built-in backup
temporal-cli cluster backup \
  --namespace production \
  --output s3://backups/temporal/$(date +%Y%m%d)/
```

### Worker Restart Strategy

```python
class ResilientWorkerManager:
    def __init__(self, worker_factory, max_restarts=5):
        self.worker_factory = worker_factory
        self.max_restarts = max_restarts
        self.restart_count = 0

    async def run_with_restart(self):
        while self.restart_count < self.max_restarts:
            try:
                worker = self.worker_factory()
                await worker.run()

            except Exception as e:
                self.restart_count += 1
                logger.error(
                    f"Worker crashed (attempt {self.restart_count}): {e}"
                )

                if self.restart_count >= self.max_restarts:
                    raise

                # Exponential backoff before restart
                await asyncio.sleep(2 ** self.restart_count)
```

### Cross-Region Replication

```python
# Primary region
primary_client = await Client.connect(
    "temporal.us-east.example.com:7233",
    namespace="production"
)

# Secondary region (standby)
secondary_client = await Client.connect(
    "temporal.us-west.example.com:7233",
    namespace="production"
)

# Replicate critical workflows
@workflow.defn
class ReplicatedWorkflow:
    @workflow.run
    async def run(self, input_data: str) -> str:
        # Execute in primary
        result = await workflow.execute_activity(
            primary_activity,
            input_data
        )

        # Replicate to secondary
        await workflow.execute_activity(
            replicate_to_secondary,
            result,
            task_queue="replication-tasks"
        )

        return result
```

---

## Additional Resources

- [Temporal Production Deployment Guide](https://docs.temporal.io/operate/deployment)
- [Monitoring and Observability](https://docs.temporal.io/operate/monitoring)
- [Performance Tuning](https://temporal.io/blog/performance-tuning-temporal)
- [Security Best Practices](https://docs.temporal.io/operate/security)
