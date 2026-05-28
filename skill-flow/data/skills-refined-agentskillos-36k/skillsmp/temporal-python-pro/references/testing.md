# Temporal Python Testing Guide

## Table of Contents
1. [Testing Overview](#testing-overview)
2. [Unit Testing Workflows](#unit-testing-workflows)
3. [Integration Testing](#integration-testing)
4. [Replay Testing](#replay-testing)
5. [Activity Testing](#activity-testing)
6. [Time Skipping](#time-skipping)
7. [Mocking Activities](#mocking-activities)
8. [Test Best Practices](#test-best-practices)

---

## Testing Overview

Temporal Python SDK provides comprehensive testing support through the `temporalio.testing` module.

### Testing Pyramid

```
           /\   E2E Tests (few)
          /  \
         /    \
        /      \  Integration Tests (some)
       /        \
      /          \
     /            \  Unit Tests (many)
    /______________\
```

- **Unit Tests**: Test workflow logic with mocked activities
- **Integration Tests**: Test workflows with real activities in in-memory Temporal
- **E2E Tests**: Test complete workflows against real Temporal server
- **Replay Tests**: Verify workflow determinism with production history

---

## Unit Testing Workflows

### Basic Workflow Test

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from temporalio.client import Client

from my_workflows import MyWorkflow

@pytest.mark.asyncio
async def test_my_workflow():
    # Start in-memory Temporal server
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # Create worker with workflow and mocked activities
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[MyWorkflow],
            activities=[mock_activities]
        ):
            # Execute workflow
            result = await env.client.execute_workflow(
                MyWorkflow.run,
                "test-input",
                id="test-workflow-id",
                task_queue="test-queue"
            )

            # Assert result
            assert result == "expected-output"
```

### Testing Workflow State

```python
@pytest.mark.asyncio
async def test_workflow_state():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[StateMachineWorkflow],
            activities=[mock_activities]
        ):
            # Start workflow (don't wait for completion)
            handle = await env.client.start_workflow(
                StateMachineWorkflow.run,
                id="state-test",
                task_queue="test-queue"
            )

            # Query workflow state
            state = await handle.query(StateMachineWorkflow.get_state)
            assert state == "processing"

            # Send signal to advance state
            await handle.signal(StateMachineWorkflow.advance)

            # Query new state
            state = await handle.query(StateMachineWorkflow.get_state)
            assert state == "completed"
```

### Testing Signals

```python
@pytest.mark.asyncio
async def test_workflow_signals():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[SignallableWorkflow],
            activities=[]
        ):
            handle = await env.client.start_workflow(
                SignallableWorkflow.run,
                id="signal-test",
                task_queue="test-queue"
            )

            # Send multiple signals
            await handle.signal(SignallableWorkflow.add_item, "item1")
            await handle.signal(SignallableWorkflow.add_item, "item2")

            # Signal completion
            await handle.signal(SignallableWorkflow.complete)

            # Wait for workflow completion
            result = await handle.result()
            assert result == ["item1", "item2"]
```

---

## Integration Testing

### Testing with Real Activities

```python
from my_activities import (
    process_payment,
    reserve_inventory,
    confirm_order
)

@pytest.mark.asyncio
async def test_order_workflow_integration():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # Use real activities (with test database/services)
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=[
                process_payment,
                reserve_inventory,
                confirm_order
            ]
        ):
            result = await env.client.execute_workflow(
                OrderWorkflow.run,
                test_order,
                id="integration-test",
                task_queue="test-queue"
            )

            assert result.status == "completed"
```

### Testing with External Dependencies

```python
@pytest.mark.asyncio
async def test_workflow_with_database():
    # Set up test database
    test_db = await setup_test_database()

    async with await WorkflowEnvironment.start_time_skipping() as env:
        # Configure activities to use test database
        activities = create_test_activities(test_db)

        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[DatabaseWorkflow],
            activities=activities.values()
        ):
            result = await env.client.execute_workflow(
                DatabaseWorkflow.run,
                user_id="test-user",
                id="db-test",
                task_queue="test-queue"
            )

            assert result.success

            # Verify database state
            user = await test_db.get_user("test-user")
            assert user.processed
```

---

## Replay Testing

Replay testing is critical for catching non-determinism bugs before deployment.

### Fetching Production History

```python
from temporalio.client import Client

async def get_production_history(workflow_id: str, run_id: str):
    client = await Client.connect("localhost:7233")

    handle = client.get_workflow_handle(
        workflow_id,
        run_id=run_id
    )

    history = await handle.fetch_history()
    return history
```

### Replay Test

```python
@pytest.mark.asyncio
async def test_workflow_replay():
    # Fetch history from production
    prod_history = await get_production_history(
        "prod-workflow-id",
        "prod-run-id"
    )

    # Replay in test environment
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[MyWorkflow],  # Your NEW workflow code
            activities=[mock_activities]
        ):
            # This will raise exception if non-deterministic
            await env.client.execute_workflow(
                MyWorkflow.run,
                args,
                id="replay-test",
                task_queue="test-queue",
                replay_history=prod_history  # Replay with production history
            )
```

### Automated Replay Testing

```python
import os
from temporalio.client import Client

# Fetch multiple production histories for testing
async def fetch_production_workflows(count: int = 10):
    client = await Client.connect("localhost:7233")

    workflows = await client.list_workflows(
        query="WorkflowType = 'MyWorkflow' and ExecutionStatus = 'Completed'"
    )

    histories = []
    for i, workflow in enumerate(workflows):
        if i >= count:
            break

        handle = client.get_workflow_handle(workflow.id, workflow.run_id)
        history = await handle.fetch_history()
        histories.append(history)

    return histories

@pytest.mark.asyncio
async def test_replay_production_workflows():
    histories = await fetch_production_workflows(count=10)

    for history in histories:
        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with Worker(
                env.client,
                task_queue="test-queue",
                workflows=[MyWorkflow],
                activities=[mock_activities]
            ):
                # Replay each production workflow
                await env.client.execute_workflow(
                    MyWorkflow.run,
                    history.inputs,
                    id=f"replay-{history.workflow_id}",
                    task_queue="test-queue",
                    replay_history=history
                )
```

---

## Activity Testing

### Testing Activity Logic

```python
from my_activities import calculate_discount

@pytest.mark.asyncio
async def test_calculate_discount():
    # Test activity directly
    result = await calculate_discount(
        customer_id="cust123",
        order_total=100.0
    )

    assert result.discounted_total == 90.0
    assert result.discount_percent == 10
```

### Testing Activity with Temporal ActivityEnvironment

```python
from temporalio.activity import ActivityEnvironment

@pytest.mark.asyncio
async def test_activity_with_environment():
    env = ActivityEnvironment()

    # Test activity with heartbeat
    result = await env.run(
        long_running_activity,
        "input-data"
    )

    assert result == "success"

    # Verify heartbeats were sent
    heartbeats = env.heartbeats
    assert len(heartbeats) > 0
```

### Testing Activity Error Handling

```python
from temporalio.common import ApplicationError

@pytest.mark.asyncio
async def test_activity_error_handling():
    # Test activity raises expected error
    with pytest.raises(ApplicationError) as exc_info:
        await charge_payment(
            card_id="invalid-card",
            amount=100.0
        )

    assert "insufficient funds" in str(exc_info.value).lower()
```

---

## Time Skipping

Time skipping allows tests that would take hours/years to complete instantly.

### Enabling Time Skipping

```python
async with await WorkflowEnvironment.start_time_skipping() as env:
    # Time automatically skips over delays
    result = await env.client.execute_workflow(
        LongRunningWorkflow.run,
        id="time-skip-test",
        task_queue="test-queue"
    )
    # Test completes instantly, even if workflow has long timers!
```

### Testing Time-Based Workflows

```python
@workflow.defn
class SubscriptionWorkflow:
    @workflow.run
    async def run(self, trial_days: int) -> None:
        # Wait for trial period
        await asyncio.sleep(trial_days * 24 * 3600)

        # Charge subscription
        await workflow.execute_activity(
            charge_subscription,
            start_to_close_timeout=timedelta(seconds=30)
        )

# Test would take 30 days without time skipping!
@pytest.mark.asyncio
async def test_subscription_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[SubscriptionWorkflow],
            activities=[mock_charge_subscription]
        ):
            # Test completes instantly
            result = await env.client.execute_workflow(
                SubscriptionWorkflow.run,
                30,  # 30-day trial
                id="subscription-test",
                task_queue="test-queue"
            )

            assert result == "charged"
```

### Testing Workflow Deadlines

```python
@workflow.defn
class DeadlineWorkflow:
    @workflow.run
    async def run(self) -> str:
        deadline = workflow.now() + timedelta(hours=24)

        while workflow.now() < deadline:
            result = await workflow.execute_activity(
                check_status,
                start_to_close_timeout=timedelta(seconds=10)
            )

            if result.is_complete:
                return "completed"

            await asyncio.sleep(3600)  # Check every hour

        return "timeout"

# Test 24-hour workflow instantly
@pytest.mark.asyncio
async def test_deadline_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[DeadlineWorkflow],
            activities=[lambda: ActivityResult(is_complete=False)]
        ):
            result = await env.client.execute_workflow(
                DeadlineWorkflow.run,
                id="deadline-test",
                task_queue="test-queue"
            )

            assert result == "timeout"
```

---

## Mocking Activities

### Simple Activity Mocks

```python
from unittest.mock import AsyncMock

# Create mock activities
mock_activities = {
    "send_email": AsyncMock(return_value="sent"),
    "process_payment": AsyncMock(return_value="paid"),
    "reserve_inventory": AsyncMock(return_value="reserved")
}

@pytest.mark.asyncio
async def test_with_mocks():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=mock_activities.values()
        ):
            await env.client.execute_workflow(
                OrderWorkflow.run,
                test_order,
                id="mock-test",
                task_queue="test-queue"
            )

            # Verify mocks were called
            mock_activities["process_payment"].assert_called_once()
            mock_activities["reserve_inventory"].assert_called_once()
```

### Conditional Activity Mocks

```python
class MockActivities:
    def __init__(self):
        self.payment_attempts = 0

    async def process_payment(self, amount: float) -> str:
        self.payment_attempts += 1

        # Fail first two attempts, succeed on third
        if self.payment_attempts < 3:
            raise ApplicationError("Payment declined")

        return "paid"

@pytest.mark.asyncio
async def test_payment_retries():
    mocks = MockActivities()

    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=[mocks.process_payment]
        ):
            await env.client.execute_workflow(
                OrderWorkflow.run,
                test_order,
                id="retry-test",
                task_queue="test-queue"
            )

            # Verify payment was retried
            assert mocks.payment_attempts == 3
```

---

## Test Best Practices

### 1. Test Workflow Determinism

Always test workflow replay with production history before deploying:

```python
# Run in CI/CD pipeline
async def test_replay_all_production_workflows():
    histories = await fetch_production_workflows(count=50)

    for history in histories:
        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with Worker(
                env.client,
                task_queue="test-queue",
                workflows=[MyWorkflow],
                activities=[mock_activities]
            ):
                await env.client.execute_workflow(
                    MyWorkflow.run,
                    history.inputs,
                    id=f"replay-{history.workflow_id}",
                    task_queue="test-queue",
                    replay_history=history
                )
```

### 2. Use Fixtures for Common Setup

```python
@pytest.fixture
async def test_env():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        yield env

@pytest.fixture
def mock_activities():
    return {
        "activity1": AsyncMock(return_value="result1"),
        "activity2": AsyncMock(return_value="result2")
    }

@pytest.mark.asyncio
async def test_with_fixtures(test_env, mock_activities):
    async with Worker(
        test_env.client,
        task_queue="test-queue",
        workflows=[MyWorkflow],
        activities=mock_activities.values()
    ):
        result = await test_env.client.execute_workflow(
            MyWorkflow.run,
            "input",
            id="fixture-test",
            task_queue="test-queue"
        )

        assert result == "expected"
```

### 3. Test Error Scenarios

```python
@pytest.mark.asyncio
async def test_workflow_failure_recovery():
    # Activity that fails then succeeds
    attempts = [0]

    async def flaky_activity(input_data):
        attempts[0] += 1
        if attempts[0] < 3:
            raise ApplicationError("Temporary failure")
        return "success"

    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[ResilientWorkflow],
            activities=[flaky_activity]
        ):
            result = await env.client.execute_workflow(
                ResilientWorkflow.run,
                "input",
                id="failure-test",
                task_queue="test-queue"
            )

            assert result == "success"
            assert attempts[0] == 3  # Retried twice
```

### 4. Test Concurrent Workflows

```python
@pytest.mark.asyncio
async def test_concurrent_workflows():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[MyWorkflow],
            activities=[mock_activities]
        ):
            # Start multiple workflows concurrently
            tasks = [
                env.client.execute_workflow(
                    MyWorkflow.run,
                    f"input-{i}",
                    id=f"concurrent-{i}",
                    task_queue="test-queue"
                )
                for i in range(10)
            ]

            results = await asyncio.gather(*tasks)

            assert len(results) == 10
            assert all(r == "expected" for r in results)
```

### 5. Test Workflow Queries

```python
@pytest.mark.asyncio
async def test_workflow_queries():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[QueryableWorkflow],
            activities=[]
        ):
            handle = await env.client.start_workflow(
                QueryableWorkflow.run,
                id="query-test",
                task_queue="test-queue"
            )

            # Query various states
            status = await handle.query(QueryableWorkflow.get_status)
            progress = await handle.query(QueryableWorkflow.get_progress)
            metrics = await handle.query(QueryableWorkflow.get_metrics)

            assert status in ["pending", "processing", "completed"]
            assert progress >= 0
            assert metrics["items_processed"] >= 0
```

---

## Additional Resources

- [Temporal Python Testing Documentation](https://docs.temporal.io/develop/python/testing-suite)
- [Workflow Replay Guide](https://docs.temporal.io/develop/python/workflows#workflow-replay)
- [Testing Best Practices](https://temporal.io/blog/testing-temporal-workflows)
