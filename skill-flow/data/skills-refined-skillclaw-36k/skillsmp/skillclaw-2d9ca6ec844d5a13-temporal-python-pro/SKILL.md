---
name: temporal-python-pro
description: Use this skill when you need to master Temporal workflow orchestration with the Python SDK for designing durable workflows, implementing saga patterns, and managing distributed transactions.
---

# Skill body

## Purpose

This skill is designed for developers who want to build reliable, scalable workflow orchestration systems using the Temporal Python SDK. It covers workflow design patterns, activity implementation, testing strategies, and production deployment for long-running processes and distributed transactions.

## When to Use This Skill

Use this skill proactively when:
- Designing or implementing Temporal workflows in Python
- Debugging workflow determinism issues or replay failures
- Implementing saga patterns for distributed transactions
- Setting up testing strategies for Temporal applications
- Deploying Temporal workers to production
- Optimizing workflow performance and resource utilization
- Troubleshooting common Temporal Python pitfalls
- Onboarding to Temporal Python SDK

## Core Concepts

### Workflows

Workflows define the orchestration logic and must be deterministic—same inputs must produce the same outputs.

```python
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Orchestrates activities
        await workflow.execute_activity(
            reserve_inventory,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        await workflow.execute_activity(
            process_payment,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        return f"Order {order_id} completed"
```

### Activities

Activities perform non-deterministic operations (I/O, API calls, database operations).

```python
from temporalio import activity

@activity.defn
async def reserve_inventory(order_id: str) -> None:
    # Business logic and I/O operations
    inventory_system.reserve(order_id)
```

### Determinism Rules

**CRITICAL**: Workflow code must be deterministic.

**Forbidden in workflows:**
- `datetime.now()`, `time.time()` → Use `workflow.now()`
- `random.choice()`, `random.random()` → Move to activity
- `uuid.uuid4()` → Use `workflow.uuid()` or activity
- `asyncio.wait()` with activities → Use `asyncio.gather()`
- File I/O, network calls, and other non-deterministic operations should be handled in activities.

## Worker Configuration and Startup

- Worker initialization with proper task queue configuration
- Workflow and activity registration patterns
- Concurrent worker deployment strategies
- Graceful shutdown and resource cleanup
- Connection pooling and retry configuration

## Async/Await and Execution Models

**Three Execution Patterns** (Source: docs.temporal.io):

1. **Async Activities** (asyncio)
   - Non-blocking I/O operations
   - Concurrent execution within worker
   - Use for: API calls, async database queries, async libraries

2. **Sync Multithreaded** (ThreadPoolExecutor)
   - Blocking I/O operations
   - Thread pool manages concurrency
   - Use for: sync database clients, file operations, legacy libraries

3. **Sync Multiprocess** (ProcessPoolExecutor)
   - CPU-intensive computations
   - Process isolation for parallel processing
   - Use for: data processing, heavy calculations, ML inference