# Temporal Python Best Practices

## Table of Contents
1. [Workflow Design](#workflow-design)
2. [Activity Design](#activity-design)
3. [Error Handling](#error-handling)
4. [Testing](#testing)
5. [Performance](#performance)
6. [Code Organization](#code-organization)
7. [Versioning](#versioning)
8. [Observability](#observability)

---

## Workflow Design

### Keep Workflows Focused on Orchestration

**BAD:**
```python
@workflow.defn
class ProcessDataWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # Business logic in workflow
        result = []
        for char in data:
            if char.isupper():
                result.append(char.lower())
            else:
                result.append(char.upper())
        return await workflow.execute_activity(
            save_result,
            ''.join(result)
        )
```

**GOOD:**
```python
@workflow.defn
class ProcessDataWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # Workflow only orchestrates
        return await workflow.execute_activity(
            transform_and_save,
            data,
            start_to_close_timeout=timedelta(seconds=30)
        )
```

### Use Data Classes for Inputs

**BAD:**
```python
@workflow.run
async def run(
    self,
    user_id: str,
    email: str,
    address: str,
    city: str,
    state: str,
    zip: str
) -> None:
    ...
```

**GOOD:**
```python
from dataclasses import dataclass

@dataclass
class CreateAccountInput:
    user_id: str
    email: str
    address: str
    city: str
    state: str
    zip: str

@workflow.run
async def run(self, input: CreateAccountInput) -> None:
    ...
```

Benefits:
- Easy to add fields without breaking existing workflows
- Self-documenting
- Can add default values

### Use Workflows for Long-Running Processes

**Use Temporal when:**
- Process takes minutes to months
- Requires durable execution across failures
- Has human-in-the-loop steps
- Needs reliable retries and compensation

**Use regular async when:**
- Process completes in seconds
- Simple orchestration
- No durability needed

### Implement Proper Time Handling

**BAD:**
```python
@workflow.run
async def run(self) -> None:
    # Non-deterministic
    now = datetime.datetime.now()
    deadline = now + datetime.timedelta(hours=24)
```

**GOOD:**
```python
@workflow.run
async def run(self) -> None:
    # Deterministic
    now = workflow.now()
    deadline = now + datetime.timedelta(hours=24)
```

---

## Activity Design

### Design Activities for Idempotency

**BAD:**
```python
@activity.defn
async def charge_credit_card(amount: float) -> bool:
    # Not idempotent - running twice charges twice
    return payment_gateway.charge(amount)
```

**GOOD:**
```python
@activity.defn
async def charge_credit_card(charge_id: str, amount: float) -> bool:
    # Idempotent - same charge_id only charges once
    return payment_gateway.charge_with_id(charge_id, amount)
```

### Use Heartbeats for Long Activities

```python
@activity.defn
async def process_large_file(file_path: str) -> None:
    activity_heartbeat = activity.heartbeat_details

    total_lines = count_lines(file_path)
    for i, line in enumerate(process_lines(file_path)):
        process_line(line)

        # Send heartbeat every 100 lines
        if i % 100 == 0:
            activity_heartbeat(f"Processed {i}/{total_lines}")
```

### Set Appropriate Timeouts

```python
await workflow.execute_activity(
    my_activity,
    input_data,
    # Max time for single activity attempt
    start_to_close_timeout=timedelta(seconds=30),
    # Max time including retries
    schedule_to_close_timeout=timedelta(seconds=120),
    # Heartbeat for long-running activities
    heartbeat_timeout=timedelta(seconds=10)
)
```

**Timeout Guidelines:**
- Start-to-close: Expected execution time + safety margin
- Schedule-to-close: Start-to-close × max_attempts
- Heartbeat: 1/3 to 1/2 of start-to-close timeout

### Use Typed Return Values

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ActivityResult:
    status: Literal["success", "partial", "failed"]
    data: dict
    error_message: str | None = None

@activity.defn
async def complex_operation(input: str) -> ActivityResult:
    try:
        result = do_operation(input)
        return ActivityResult(status="success", data=result)
    except PartialFailureException as e:
        return ActivityResult(
            status="partial",
            data=e.partial_result,
            error_message=str(e)
        )
```

---

## Error Handling

### Distinguish Expected vs. Unexpected Errors

**Expected Errors (Application Errors):**
```python
class InsufficientFundsError(Exception):
    pass

@activity.defn
async def transfer_funds(from_account: str, to_account: str, amount: float) -> None:
    if balance < amount:
        # Expected business error - don't retry
        raise ApplicationError(
            "Insufficient funds",
            type="InsufficientFunds",
            non_retryable=True
        )
```

**Unexpected Errors (Transient Errors):**
```python
@activity.defn
async def call_api(endpoint: str) -> dict:
    try:
        return await http_client.get(endpoint)
    except HTTPError as e:
        if e.status >= 500:
            # Server error - retry
            raise
        elif e.status == 429:
            # Rate limited - backoff
            raise
        else:
            # Client error - don't retry
            raise ApplicationError(f"Client error: {e}", non_retryable=True)
```

### Use Retry Policies Effectively

```python
from temporalio.common import RetryPolicy

# Standard retry policy
retry_policy = RetryPolicy(
    maximum_attempts=5,
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,  # Exponential backoff
    maximum_interval=timedelta(seconds=60)
)

# For idempotent activities
retry_policy = RetryPolicy(
    maximum_attempts=10,
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0
)

# For non-idempotent activities (no retries)
retry_policy = RetryPolicy(
    maximum_attempts=1
)
```

### Compensating Transactions Pattern

```python
@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order: Order) -> None:
        try:
            # Step 1: Reserve inventory
            await workflow.execute_activity(
                reserve_inventory,
                order.items,
                retry_policy=RetryPolicy(maximum_attempts=3)
            )

            # Step 2: Process payment
            await workflow.execute_activity(
                process_payment,
                order.payment_info,
                retry_policy=RetryPolicy(maximum_attempts=3)
            )

            # Step 3: Confirm order
            await workflow.execute_activity(
                confirm_order,
                order.id
            )

        except Exception as e:
            # Compensate on failure
            await workflow.execute_activity(
                release_inventory,
                order.items
            )
            raise
```

---

## Testing

### Write Workflow Unit Tests

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

async def test_order_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=[mock_activities]
        ):
            result = await env.client.execute_workflow(
                OrderWorkflow.run,
                test_order,
                id="test-order",
                task_queue="test-queue"
            )

            assert result.status == "completed"
```

### Test Non-Determinism

```python
# Test that workflow handles replay correctly
async def test_workflow_replay():
    # Get history from production
    handle = client.get_workflow_handle("prod-workflow-id")
    history = await handle.fetch_history()

    # Replay in test
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=[mock_activities]
        ):
            # Replay will fail if non-deterministic
            await env.client.execute_workflow(
                OrderWorkflow.run,
                args,
                id="test-replay",
                task_queue="test-queue",
                replay_history=history
            )
```

### Mock Activities in Tests

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_workflow_with_mock():
    # Create mock activities
    mock_activities = {
        "reserve_inventory": AsyncMock(return_value="reserved"),
        "process_payment": AsyncMock(return_value="paid")
    }

    # Use in workflow test
    result = await execute_workflow_with_mocks(
        OrderWorkflow.run,
        order_data,
        mock_activities
    )
```

---

## Performance

### Use Local Activities for Fast Operations

```python
@workflow.defn
class DataProcessingWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # Use local activity for fast, local operations
        validated = await workflow.execute_local_activity(
            validate_data,
            data,
            start_to_close_timeout=timedelta(seconds=1)
        )

        # Use regular activity for slower operations
        result = await workflow.execute_activity(
            process_in_external_service,
            validated,
            start_to_close_timeout=timedelta(seconds=30)
        )

        return result
```

**Local Activity Guidelines:**
- Fast operations (< 1 second)
- No external dependencies
- No retry needed
- Lower overhead than regular activities

### Configure Worker Concurrency

```python
worker = Worker(
    client,
    task_queue="my-queue",
    workflows=[MyWorkflow],
    activities=[my_activities],
    # Limit concurrent activity executions
    max_concurrent_activities=50,
    # Limit concurrent workflow tasks
    max_concurrent_workflow_tasks=20,
    # Activity worker pool size
    max_concurrent_local_activities=100
)
```

### Use Activity Worker Separation

```python
# Workflow-only worker
workflow_worker = Worker(
    client,
    task_queue="workflow-queue",
    workflows=[MyWorkflows],
    activities=[]
)

# Activity-only worker
activity_worker = Worker(
    client,
    task_queue="activity-queue",
    workflows=[],
    activities=[MyActivities]
)
```

Benefits:
- Scale workflow and activity workers independently
- Different resource requirements
- Better isolation

---

## Code Organization

### Separate Workflow and Activity Files

```
project/
├── workflows/
│   ├── __init__.py
│   ├── order_workflow.py
│   └── payment_workflow.py
├── activities/
│   ├── __init__.py
│   ├── payment_activities.py
│   └── inventory_activities.py
├── worker/
│   ├── workflow_worker.py
│   └── activity_worker.py
└── client/
    └── workflow_starter.py
```

### Use Module Structure

```python
# workflows/order_workflow.py
from temporalio import workflow
from dataclasses import dataclass

@dataclass
class OrderInput:
    items: list[str]
    customer_id: str

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order: OrderInput) -> str:
        # Implementation
        pass
```

### Document Workflows and Activities

```python
@workflow.defn
class ProcessPaymentWorkflow:
    """
    Processes payment for an order.

    Workflow steps:
    1. Validate payment method
    2. Charge payment gateway
    3. Handle 3D Secure if required
    4. Update order status

    Signals:
    - cancel(order_id): Cancel payment processing

    Queries:
    - get_status(): Current payment status
    - get_retry_count(): Number of payment retries
    """
    pass
```

---

## Versioning

### Use Workflow Versioning

```python
from datetime import timedelta

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, input: str) -> str:
        # Version 2 of workflow logic
        version = await workflow.get_version(
            "my-feature",
            1,  # min supported version
            2   # max supported version
        )

        if version == 1:
            # Old behavior
            return await self._process_v1(input)
        else:
            # New behavior
            return await self._process_v2(input)

    async def _process_v1(self, input: str) -> str:
        # Old implementation
        pass

    async def _process_v2(self, input: str) -> str:
        # New implementation
        pass
```

### Maintain Backward Compatibility

**When changing workflow logic:**
1. Add new code path with version check
2. Keep old code path for existing workflows
3. Deploy and observe
4. Only remove old code after all workflows complete

---

## Observability

### Use Search Attributes

```python
# Start workflow with search attributes
handle = await client.start_workflow(
    MyWorkflow.run,
    input_data,
    id="workflow-123",
    task_queue="my-queue",
    search_attributes={
        "CustomerId": ["customer-456"],
        "OrderValue": [999.99],
        "Priority": ["high"]
    }
)

# Query workflows by search attributes
result = await client.list_workflows(
    query="CustomerId = 'customer-456' and OrderValue > 500"
)
```

### Add Structured Logging

```python
@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order: Order) -> None:
        workflow.logger.info(
            "Processing order",
            extra={
                "order_id": order.id,
                "customer_id": order.customer_id,
                "item_count": len(order.items),
                "total_value": order.total
            }
        )
```

### Use Metrics

```python
# Worker metrics configuration
worker = Worker(
    client,
    task_queue="my-queue",
    workflows=[MyWorkflow],
    activities=[MyActivity],
    # Prometheus metrics endpoint
    metrics_headers=lambda: {
        "X-Metrics-Auth": "secret"
    }
)
```

Key metrics to track:
- Workflow throughput (started/completed per second)
- Activity latency
- Workflow execution time
- Error rates by type
- Worker resource utilization

---

## Additional Resources

- [Temporal Python Best Practices](https://docs.temporal.io/best-practices/python)
- [Workflow Design Patterns](https://temporal.io/blog/workflow-design-patterns)
- [Common Anti-Patterns](https://temporal.io/blog/spooky-stories-chilling-temporal-anti-patterns-part-1)
