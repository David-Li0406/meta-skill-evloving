# Common Temporal Python Pitfalls

## Table of Contents
1. [Determinism Violations](#determinism-violations)
2. [Activity Mistakes](#activity-mistakes)
3. [Workflow Anti-Patterns](#workflow-anti-patterns)
4. [Testing Pitfalls](#testing-pitfalls)
5. [Production Issues](#production-issues)
6. [AI/LLM-Generated Code Issues](#aillm-generated-code-issues)

---

## Determinism Violations

### 1. Using `asyncio.wait()` with Activities

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self, items: list[str]) -> None:
        # ❌ BAD: asyncio.wait is non-deterministic
        tasks = [
            workflow.execute_activity(process_item, item)
            for item in items
        ]
        done, pending = await asyncio.wait(tasks)  # Non-deterministic order!
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self, items: list[str]) -> None:
        # ✅ GOOD: Use asyncio.gather or execute in order
        results = await asyncio.gather(*[
            workflow.execute_activity(
                process_item,
                item,
                start_to_close_timeout=timedelta(seconds=30)
            )
            for item in items
        ])
```

**Why:** `asyncio.wait()` can return tasks in different orders across executions, breaking replay determinism. Use `asyncio.gather()` which preserves order.

---

### 2. Using System Time in Workflows

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        # ❌ BAD: Non-deterministic time
        now = datetime.datetime.now()
        timestamp = time.time()
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> str:
        # ✅ GOOD: Deterministic time from Temporal
        now = workflow.now()
        timestamp = workflow.now().timestamp()
```

**Why:** System time changes between workflow executions and replays, causing history mismatches.

---

### 3. Using Random Numbers in Workflows

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self, options: list[str]) -> str:
        # ❌ BAD: Non-deterministic random choice
        selected = random.choice(options)
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self, options: list[str], seed: int) -> str:
        # ✅ GOOD: Deterministic "random" choice
        selected = options[seed % len(options)]
```

**Better Solution:**
```python
@workflow.defn
class BetterWorkflow:
    @workflow.run
    async def run(self, options: list[str]) -> str:
        # ✅ BEST: Use activity for random choice
        selected = await workflow.execute_activity(
            random_choice,
            options,
            start_to_close_timeout=timedelta(seconds=1)
        )
```

---

### 4. Using UUID Generation in Workflows

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        # ❌ BAD: Non-deterministic UUID
        new_id = uuid.uuid4()
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> str:
        # ✅ GOOD: Deterministic ID from input
        new_id = f"{workflow.uuid()}-{workflow.now().timestamp()}"

        # OR use activity
        new_id = await workflow.execute_activity(
            generate_uuid,
            start_to_close_timeout=timedelta(seconds=1)
        )
```

---

### 5. Modifying Global Mutable State

**Problem:**
```python
# ❌ BAD: Global state
counter = 0

@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> int:
        global counter
        counter += 1  # Breaks determinism!
        return counter
```

**Solution:**
```python
# ✅ GOOD: Workflow-local state
@workflow.defn
class GoodWorkflow:
    def __init__(self) -> None:
        self.counter = 0  # Instance variable

    @workflow.run
    async def run(self) -> int:
        self.counter += 1  # Deterministic
        return self.counter
```

---

## Activity Mistakes

### 6. Non-Idempotent Activities

**Problem:**
```python
@activity.defn
async def charge_credit_card(amount: float) -> bool:
    # ❌ BAD: Not idempotent - running twice charges twice!
    return payment_gateway.charge(amount)
```

**Solution:**
```python
@activity.defn
async def charge_credit_card(charge_id: str, amount: float) -> bool:
    # ✅ GOOD: Idempotent - same charge_id only charges once
    return payment_gateway.charge_with_idempotency_key(charge_id, amount)
```

**Common Non-Idempotent Operations:**
- Sending emails
- Charging payments
- Incrementing counters
- Publishing messages

**Always Make Activities Idempotent by:**
- Using idempotency keys
- Checking state before acting
- Designing for safe retries

---

### 7. Missing Activity Heartbeats

**Problem:**
```python
@activity.defn
async def process_large_dataset(dataset_id: str) -> None:
    # ❌ BAD: No heartbeat for long-running activity
    for item in large_dataset:
        expensive_operation(item)  # Takes hours
```

**Solution:**
```python
@activity.defn
async def process_large_dataset(dataset_id: str) -> None:
    # ✅ GOOD: Regular heartbeats
    total_items = len(large_dataset)
    for i, item in enumerate(large_dataset):
        expensive_operation(item)

        # Send heartbeat every 100 items
        if i % 100 == 0:
            activity.logger.info(f"Progress: {i}/{total_items}")
            activity.heartbeat(f"Processed {i}/{total_items}")
```

---

### 8. Incorrect Activity Timeouts

**Problem:**
```python
# ❌ BAD: Timeout too short
await workflow.execute_activity(
    slow_operation,
    start_to_close_timeout=timedelta(seconds=5)  # But takes 30 seconds!
)
```

**Solution:**
```python
# ✅ GOOD: Appropriate timeout with buffer
await workflow.execute_activity(
    slow_operation,
    start_to_close_timeout=timedelta(seconds=60),  # Expected 30s + buffer
    schedule_to_close_timeout=timedelta(seconds=180),  # Including retries
    heartbeat_timeout=timedelta(seconds=20)  # Detect hangs
)
```

---

## Workflow Anti-Patterns

### 9. Business Logic in Workflows

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # ❌ BAD: Complex business logic in workflow
        result = []
        for char in data:
            if char.isupper():
                result.append(char.lower())
            elif char.islower():
                result.append(char.upper())
            else:
                result.append(char)
        return await workflow.execute_activity(
            save_result,
            ''.join(result)
        )
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # ✅ GOOD: Workflow only orchestrates
        return await workflow.execute_activity(
            transform_and_save,
            data,
            start_to_close_timeout=timedelta(seconds=30)
        )
```

**Why:** Workflow code should only orchestrate activities. Business logic belongs in activities where it can be modified without breaking workflow determinism.

---

### 10. Infinite Loops Without Conditions

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> None:
        # ❌ BAD: Infinite loop - will never complete
        while True:
            await workflow.execute_activity(
                poll_external_system,
                start_to_close_timeout=timedelta(seconds=10)
            )
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self, max_duration: timedelta) -> None:
        # ✅ GOOD: Loop with exit condition
        deadline = workflow.now() + max_duration

        while workflow.now() < deadline:
            result = await workflow.execute_activity(
                poll_external_system,
                start_to_close_timeout=timedelta(seconds=10)
            )

            if result.is_complete:
                break

            await asyncio.sleep(60)  # Use sleep, not time.sleep()
```

---

### 11. Not Handling Signals Properly

**Problem:**
```python
@workflow.defn
class BadWorkflow:
    def __init__(self) -> None:
        self.should_cancel = False

    @workflow.run
    async def run(self) -> None:
        # ❌ BAD: Never checks for cancellation signal
        await workflow.execute_activity(
            long_running_task,
            start_to_close_timeout=timedelta(hours=1)
        )

    @workflow.signal
    async def cancel(self) -> None:
        self.should_cancel = True
```

**Solution:**
```python
@workflow.defn
class GoodWorkflow:
    def __init__(self) -> None:
        self.should_cancel = False

    @workflow.run
    async def run(self) -> None:
        # ✅ GOOD: Responds to cancellation
        await workflow.execute_activity(
            long_running_task,
            start_to_close_timeout=timedelta(hours=1)
        )

        # Check signal after activity
        if self.should_cancel:
            raise ApplicationError("Cancelled by user")

    @workflow.signal
    async def cancel(self) -> None:
        self.should_cancel = True
        # Cancel any pending activities
        workflow.raise_cancelled()
```

---

## Testing Pitfalls

### 12. Not Testing Workflow Replay

**Problem:**
Deploying workflow code without testing replay against production history.

**Solution:**
```python
async def test_workflow_replay():
    # Fetch history from production
    handle = client.get_workflow_handle("prod-workflow-id")
    history = await handle.fetch_history()

    # Replay in test environment
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[MyWorkflow],
            activities=[mock_activities]
        ):
            # This will fail if workflow is non-deterministic
            await env.client.execute_workflow(
                MyWorkflow.run,
                args,
                id="test-replay",
                task_queue="test-queue",
                replay_history=history
            )
```

---

### 13. Not Using Time Skipping in Tests

**Problem:**
```python
@workflow.defn
class WorkflowWithTimer:
    @workflow.run
    async def run(self) -> None:
        await asyncio.sleep(3600)  # Wait 1 hour

# ❌ BAD: Test takes 1 hour to run!
async def test_workflow():
    await client.execute_workflow(
        WorkflowWithTimer.run,
        task_queue="test-queue"
    )
```

**Solution:**
```python
# ✅ GOOD: Test completes instantly with time skipping
async def test_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[WorkflowWithTimer]
        ):
            await env.client.execute_workflow(
                WorkflowWithTimer.run,
                id="test-workflow",
                task_queue="test-queue"
            )
```

---

## Production Issues

### 14. Not Setting Search Attributes

**Problem:**
Cannot efficiently query workflows in production.

**Solution:**
```python
await client.start_workflow(
    MyWorkflow.run,
    input_data,
    id="workflow-123",
    task_queue="my-queue",
    search_attributes={
        "CustomerId": ["customer-456"],
        "OrderValue": [999.99],
        "Priority": ["high"],
        "Department": ["sales"]
    }
)

# Now you can query:
# List all high-value orders for a customer
workflows = await client.list_workflows(
    query='CustomerId = "customer-456" and OrderValue > 500'
)
```

---

### 15. Not Configuring Worker Shutdown Gracefully

**Problem:**
Worker shuts down immediately, killing in-progress workflows.

**Solution:**
```python
import signal

worker = Worker(client, task_queue="my-queue", workflows=[MyWorkflow])

# Graceful shutdown on SIGTERM
shutdown_event = asyncio.Event()

def signal_handler():
    shutdown_event.set()

signal.signal(signal.SIGTERM, signal_handler)

# Run worker until shutdown signal
await worker.run_until(shutdown_event.is_set)

# Graceful shutdown
await worker.shutdown()
```

---

### 16. Not Monitoring Workflow Execution

**Problem:**
No visibility into workflow failures or stuck workflows.

**Solution:**
```python
# Enable structured logging
import structlog

workflow.logger = structlog.get_logger()

# Set up alerts for:
# - Workflow timeout
# - High activity failure rate
# - Workflow stuck in running state
# - Worker crash

# Use Temporal UI or metrics for monitoring
```

---

## AI/LLM-Generated Code Issues

### 17. AI Generates Non-Deterministic Code

**Common AI Mistakes:**

1. **Using `datetime.now()` in workflows**
   ```python
   # AI-generated code (WRONG)
   @workflow.defn
   class AIWorkflow:
       @workflow.run
       async def run(self) -> str:
           timestamp = datetime.datetime.now()  # ❌
   ```

2. **Using `random` module in workflows**
   ```python
   # AI-generated code (WRONG)
   @workflow.defn
   class AIWorkflow:
       @workflow.run
       async def run(self) -> str:
           result = random.choice(options)  # ❌
   ```

3. **Putting business logic in workflows**
   ```python
   # AI-generated code (WRONG)
   @workflow.defn
   class AIWorkflow:
       @workflow.run
       async def run(self, data: str) -> str:
           # Complex business logic (❌ should be in activity)
           processed = complex_transformation(data)
           return await workflow.execute_activity(save, processed)
   ```

**How to Fix AI-Generated Code:**
1. Review all workflow code for determinism violations
2. Move non-deterministic operations to activities
3. Use `workflow.now()` instead of `datetime.now()`
4. Use `workflow.uuid()` instead of `uuid.uuid4()`
5. Test replay with production history

---

### 18. AI Creates Non-Idempotent Activities

**Problem:**
```python
# AI-generated code (WRONG)
@activity.defn
async def send_notification(email: str, message: str) -> None:
    # ❌ Not idempotent - running twice sends twice!
    email_service.send(email, message)
```

**Solution:**
```python
# ✅ GOOD: Idempotent activity
@activity.defn
async def send_notification(notification_id: str, email: str, message: str) -> None:
    # Check if already sent
    if await database.notification_sent(notification_id):
        return

    await email_service.send_with_tracking_id(email, message, notification_id)
    await database.mark_notification_sent(notification_id)
```

---

### 19. AI Misses Activity Timeouts

**Problem:**
```python
# AI-generated code (WRONG)
await workflow.execute_activity(
    slow_operation,
    data  # ❌ No timeout! Will hang forever if activity fails
)
```

**Solution:**
```python
# ✅ GOOD: Always set timeouts
await workflow.execute_activity(
    slow_operation,
    data,
    start_to_close_timeout=timedelta(seconds=60),  # Required
    schedule_to_close_timeout=timedelta(seconds=180)  # Recommended
)
```

---

### 20. AI Uses Wrong Async Patterns

**Problem:**
```python
# AI-generated code (WRONG)
@workflow.defn
class AIWorkflow:
    @workflow.run
    async def run(self) -> None:
        # ❌ Using time.sleep instead of asyncio.sleep
        time.sleep(60)  # Blocks the event loop!

        # ❌ Using asyncio.wait with activities
        done, pending = await asyncio.wait(tasks)  # Non-deterministic!
```

**Solution:**
```python
# ✅ GOOD: Correct async patterns
@workflow.defn
class CorrectWorkflow:
    @workflow.run
    async def run(self) -> None:
        # Use asyncio.sleep for delays
        await asyncio.sleep(60)

        # Use asyncio.gather for parallel activities
        results = await asyncio.gather(*tasks)
```

---

## Checklist for Avoiding Pitfalls

### Before Deploying Workflow Code:
- [ ] All time references use `workflow.now()`
- [ ] No use of `random`, `uuid`, or `datetime` modules
- [ ] No use of `asyncio.wait()` with activities
- [ ] All activities are idempotent
- [ ] All activities have appropriate timeouts
- [ ] Business logic moved to activities
- [ ] Workflow replay tested
- [ ] Signals properly handled
- [ ] Search attributes configured
- [ ] Graceful shutdown implemented

### For AI-Generated Code:
- [ ] Review all code for determinism
- [ ] Add missing activity timeouts
- [ ] Make activities idempotent
- [ ] Fix async patterns
- [ ] Test with production history
- [ ] Add comprehensive error handling

---

## Additional Resources

- [Understanding Non-Determinism in Temporal](https://medium.com/@sanhdoan/understanding-non-determinism-in-temporal-io-why-it-matters-how-to-avoid-it-3d397d8a5793)
- [Spooky Stories: Chilling Temporal Anti-patterns](https://temporal.io/blog/spooky-stories-chilling-temporal-anti-patterns-part-1)
- [Temporal Python SDK Sandbox](https://docs.temporal.io/develop/python/python-sdk-sandbox)
- [asyncio.wait Non-Determinism Bug](https://github.com/temporalio/sdk-python/issues/429)
