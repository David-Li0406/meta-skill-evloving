---
name: temporal-workflow-orchestration
description: Use this skill when designing and implementing durable workflows and activities in Temporal, whether in TypeScript or Python.
---

# Temporal Workflow Orchestration

Temporal SDK patterns for building durable, distributed workflows in both TypeScript and Python.

## Package Location (TypeScript)

Temporal workflows and activities are located in `packages/workflows/`.

```
packages/workflows/
├── src/
│   ├── workflows/        # Workflow definitions
│   ├── activities/       # Activity implementations
│   ├── worker.ts         # Worker configuration
│   └── client.ts         # Temporal client
└── package.json
```

## Worker Setup

### TypeScript

```typescript
// packages/workflows/src/worker.ts
import { Worker } from '@temporalio/worker';
import * as activities from './activities';

async function run() {
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    activities,
    taskQueue: 'order-processing',
    connection: {
      address: process.env.TEMPORAL_ADDRESS || 'localhost:7233',
    },
  });

  await worker.run();
}

run().catch(console.error);
```

### Python

```python
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[MyWorkflow],
        activities=[my_activity],
    )

    await worker.run()
```

## Workflow Definition

### TypeScript

```typescript
// packages/workflows/src/workflows/order.workflow.ts
import {
  proxyActivities,
  defineSignal,
  setHandler,
} from '@temporalio/workflow';
import type * as activities from '../activities';

export const cancelOrderSignal = defineSignal('cancelOrder');

export async function orderWorkflow(input: OrderWorkflowInput): Promise<string> {
  // Workflow logic here
}
```

### Python

```python
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        result = await workflow.execute_activity(
            my_activity,
            name,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"Hello {result}"
```

## Activity Implementation

### TypeScript

```typescript
// packages/workflows/src/activities/payment.activities.ts
export async function processPayment(input: ProcessPaymentInput): Promise<ProcessPaymentResult> {
  // Payment processing logic here
}
```

### Python

```python
from temporalio import activity

@activity.defn
async def my_activity(name: str) -> str:
    return name.upper()
```

## Starting Workflows

### TypeScript

```typescript
// apps/order/src/order/order.service.ts
async createOrder(orderData: CreateOrderDto): Promise<string> {
  // Start workflow logic here
}
```

### Python

```python
from temporalio.client import Client

async def start_workflow():
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        MyWorkflow.run,
        "World",
        id="my-workflow-id",
        task_queue="my-task-queue",
    )
    result = await handle.result()
    print(result)  # "Hello WORLD"
```

## Error Handling

### TypeScript

```typescript
// Handle errors in workflows
```

### Python

```python
from temporalio.exceptions import ActivityError

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self) -> str:
        try:
            result = await workflow.execute_activity(
                risky_activity,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
        except ActivityError as e:
            return "Failed"
        return result
```

## Signals and Queries

### TypeScript

```typescript
// Define signals and queries in workflows
```

### Python

```python
@workflow.defn
class OrderWorkflow:
    def __init__(self):
        self.status = "pending"

    @workflow.signal
    def approve(self):
        self.status = "approved"

    @workflow.query
    def get_status(self) -> str:
        return self.status
```

## Best Practices

1. **Keep workflows deterministic** - Avoid direct I/O, random, or time-dependent operations.
2. **Use activities for side effects** - All external calls should be made in activities.
3. **Set appropriate timeouts** - Configure timeouts for activities.
4. **Handle signals gracefully** - Check for signals at appropriate points in workflows.
5. **Use queries for state** - Do not expose internal state directly.
6. **Version workflows** - Implement versioning for workflow updates.
7. **Test workflows** - Utilize Temporal's testing framework.

## Docker Setup

To run Temporal in a Docker environment, use the following command:

```bash
# Start Temporal server + UI
docker-compose up -d temporal temporal-ui

# Access Temporal UI
open http://localhost:8080
```