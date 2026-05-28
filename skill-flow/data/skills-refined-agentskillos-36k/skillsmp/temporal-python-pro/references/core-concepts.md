# Temporal Python SDK - Core Concepts

## Table of Contents
1. [Workflows](#workflows)
2. [Activities](#activities)
3. [Workers](#workers)
4. [Task Queues](#task-queues)
5. [Determinism](#determinism)
6. [Workflow Execution](#workflow-execution)
7. [Signals](#signals)
8. [Queries](#queries)
9. [Child Workflows](#child-workflows)

---

## Workflows

Workflows are the core orchestration logic in Temporal. They define the sequence of activities and control flow.

### Defining a Workflow

```python
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            self.greet,
            name,
            start_to_close_timeout=timedelta(seconds=5)
        )

    @workflow.activity
    async def greet(self, name: str) -> str:
        return f"Hello, {name}!"
```

### Key Workflow Features

- **Deterministic execution**: Workflow code must produce the same result on replay
- **Long-running**: Can execute for days, months, or years
- **State management**: Automatically persists state between events
- **Failure handling**: Built-in retry and recovery mechanisms

### Workflow Methods

- `@workflow.run`: Main entry point for workflow execution
- `@workflow.signal`: Handler for asynchronous signals
- `@workflow.query`: Handler for synchronous state queries

### Sandbox Environment

Python workflows run in a sandbox that restricts non-deterministic operations:

```python
# Allowed in workflows
workflow.now()  # Temporal's deterministic time
workflow.logger()  # Deterministic logging
workflow.memo()  # Store workflow metadata

# NOT allowed in workflows (cause sandbox violations)
import time; time.time()  # Non-deterministic
import random; random.random()  # Non-deterministic
import datetime; datetime.now()  # Non-deterministic
```

---

## Activities

Activities perform non-deterministic operations like I/O, API calls, or database operations.

### Defining an Activity

```python
from datetime import timedelta
from temporalio import activity

@activity.defn
async def call_external_api(input_data: dict) -> dict:
    # Perform I/O operation
    response = await some_api_client.call(input_data)
    return response.data
```

### Activity Options

```python
await workflow.execute_activity(
    call_external_api,
    {"param": "value"},
    start_to_close_timeout=timedelta(seconds=30),  # Max execution time
    schedule_to_close_timeout=timedelta(seconds=60),  # Total time including queue
    retry_policy=RetryPolicy(
        maximum_attempts=3,
        initial_interval=timedelta(seconds=1),
        backoff_coefficient=2.0
    ),
    heartbeat_timeout=timedelta(seconds=10)  # For long-running activities
)
```

### Activity Types

1. **Async Activities**: Use `async def` for I/O-bound operations
2. **Sync Activities**: Use `def` for CPU-bound operations
3. **Local Activities**: Run in worker process, faster but no retries

---

## Workers

Workers host workflows and activities, executing them from task queues.

### Starting a Worker

```python
from temporalio.worker import Worker
from temporalio.client import Client

async def run_worker():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[MyWorkflow],
        activities=[call_external_api]
    )

    await worker.run()
```

### Worker Configuration

```python
worker = Worker(
    client,
    task_queue="my-task-queue",
    workflows=[MyWorkflow],
    activities=[call_external_api],
    max_concurrent_activities=10,  # Limit concurrent activity executions
    max_concurrent_workflow_tasks=5,  # Limit concurrent workflow tasks
    sticky_queue_schedule_to_close_timeout=timedelta(seconds=10)
)
```

---

## Task Queues

Task queues route work to workers and provide load balancing.

### Task Queue Features

- **Work stealing**: Idle workers can steal tasks from busy workers
- **Worker-specific queues**: Sticky queues for workflow locality
- **Rate limiting**: Control task execution rates

### Task Queue Best Practices

```python
# Good: Separate task queues for different concerns
HIGH_PRIORITY_QUEUE = "high-priority-tasks"
BACKGROUND_QUEUE = "background-processing"
ACTIVITIES_QUEUE = "activity-workers"
```

---

## Determinism

Workflow code MUST be deterministic. The same inputs must produce the same outputs.

### Deterministic Rules

1. **No external state**: Don't read/write files, network, or databases
2. **No system time**: Use `workflow.now()` instead of `datetime.now()`
3. **No random numbers**: Use workflow input for any randomness
4. **No threading**: Use async/await, not threads or processes
5. **No global mutable state**: Workflow state must be in workflow variables

### Non-Deterministic Code Examples

```python
# BAD: Non-deterministic time
current_time = datetime.datetime.now()

# GOOD: Deterministic time
current_time = workflow.now()

# BAD: Non-deterministic random
result = random.choice(options)

# GOOD: Pass random choice as input
result = options[random_seed % len(options)]
```

---

## Workflow Execution

Workflow executions represent a single run of a workflow with specific inputs.

### Starting a Workflow

```python
from temporalio.client import Client

async def start_workflow():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        MyWorkflow.run,
        "World",
        id="workflow-id-123",
        task_queue="my-task-queue"
    )
```

### Workflow Options

```python
handle = await client.start_workflow(
    MyWorkflow.run,
    "World",
    id="workflow-id-123",
    task_queue="my-task-queue",
    execution_timeout=timedelta(hours=1),
    workflow_id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE,
    memo={"key": "value"},  # Workflow metadata
    search_attributes={"CustomField": ["value"]}  # Searchable attributes
)

# Get result later
result = await handle.result()
```

---

## Signals

Signals allow asynchronous communication with running workflows.

### Defining Signal Handlers

```python
from temporalio import workflow

@workflow.defn
class OrderWorkflow:
    def __init__(self) -> None:
        self.status = "pending"

    @workflow.run
    async def run(self, order_id: str) -> None:
        # Wait for signal
        await workflow.wait_condition(lambda: self.status != "pending")

    @workflow.signal
    async def cancel(self, reason: str) -> None:
        self.status = "cancelled"
        workflow.logger.info(f"Order cancelled: {reason}")

    @workflow.signal(name="ship")  # Custom signal name
    async def ship_order(self, tracking: str) -> None:
        self.status = "shipped"
        self.tracking = tracking
```

### Sending Signals

```python
# Get workflow handle
handle = client.get_workflow_handle("workflow-id-123")

# Send signal
await handle.signal(OrderWorkflow.cancel, "Customer request")
```

---

## Queries

Queries allow synchronous inspection of workflow state.

### Defining Query Handlers

```python
@workflow.defn
class OrderWorkflow:
    def __init__(self) -> None:
        self.order_status = "pending"
        self.items = []

    @workflow.query
    def get_status(self) -> str:
        return self.order_status

    @workflow.query
    def get_items(self) -> list[str]:
        return self.items.copy()
```

### Querying Workflows

```python
handle = client.get_workflow_handle("workflow-id-123")

# Simple query
status = await handle.query(OrderWorkflow.get_status)

# Named query
items = await handle.query("get_items")
```

### Query Limitations

- Cannot modify workflow state
- Cannot perform activities
- Must be fast and deterministic
- Cannot block or wait

---

## Child Workflows

Child workflows allow composing complex workflows from simpler ones.

### Starting Child Workflows

```python
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, items: list[str]) -> None:
        # Start multiple child workflows
        tasks = [
            workflow.execute_child_workflow(
                ProcessItemWorkflow,
                item,
                id=f"child-{i}"
            )
            for i, item in enumerate(items)
        ]

        # Wait for all children
        results = await asyncio.gather(*tasks)
```

### Child Workflow Options

```python
result = await workflow.execute_child_workflow(
    ChildWorkflow.run,
    "input",
    id="child-workflow-id",
    task_queue="child-queue",
    execution_timeout=timedelta(minutes=10),
    # Parent workflow close policy
    parent_close_policy=ParentClosePolicy.TERMINATE
)
```

### Child Workflow Patterns

1. **Parallel execution**: Start multiple children for concurrent processing
2. **Sequential execution**: Start children one after another
3. **Fan-out/fan-in**: Start many children, aggregate results

---

## Additional Resources

- [Temporal Python SDK Docs](https://docs.temporal.io/develop/python)
- [API Reference](https://python.temporal.io/)
- [Temporal Blog](https://temporal.io/blog)
