---
name: temporal
description: "Design and implement durable workflows using Temporal.io. Use this when building resilient, long-running processes, AI agent orchestration, or any workflow that needs to survive failures."
---

# Temporal Workflow Design

## Overview

Help design and implement durable workflows using Temporal.io - an open-source platform for building reliable applications that automatically recover from failures.

## When to Use Temporal

- **Long-running processes**: Multi-step workflows that span hours, days, or weeks
- **AI/Agent orchestration**: Resilient AI pipelines that need state management
- **Order fulfillment**: Maintain transaction integrity across service failures
- **Human-in-the-loop**: Workflows requiring human approval steps
- **Financial transactions**: Durable ledgers tracking transactions reliably
- **CI/CD pipelines**: Deployments with built-in retries and rollbacks

## Core Concepts

**Workflows**: Durable functions that define the overall process. They automatically capture state at each step and resume from failures.

**Activities**: Individual tasks within a workflow (API calls, database operations, file processing). These are the units that can fail and be retried.

**Workers**: Processes that execute workflows and activities. They poll task queues for work.

**Signals**: External inputs that can modify workflow behavior mid-execution.

**Queries**: Read-only operations to inspect workflow state without affecting execution.

**Task Queues**: Named queues that route work to appropriate workers.

## Design Process

**1. Identify the workflow boundary:**
- What triggers the workflow?
- What's the final outcome?
- How long might it run?

**2. Break into activities:**
- What are the discrete steps?
- Which steps can fail and need retries?
- What are the retry policies for each?

**3. Define state and signals:**
- What state needs to persist between steps?
- What external events need to modify the workflow?
- What information should be queryable?

**4. Plan failure modes:**
- What happens if an activity fails permanently?
- Are there compensation/rollback requirements?
- How should timeouts be handled?

## Supported Languages

- TypeScript/JavaScript
- Python
- Go
- Java
- C# (.NET)
- PHP
- Ruby

## Implementation Patterns

**Saga Pattern**: Long-running transactions with compensation on failure.

**State Machine**: Workflows that transition between defined states.

**Pipeline**: Sequential processing with optional parallelization.

**Fan-out/Fan-in**: Parallel activity execution with aggregated results.

**Polling**: Periodic checks until a condition is met.

**Human-in-the-Loop**: Wait for external signals (approvals, reviews).

## Best Practices

- Keep workflows deterministic - no random values, current time, or I/O in workflow code
- Put all non-deterministic operations in activities
- Use meaningful workflow and activity names
- Set appropriate retry policies per activity type
- Use timeouts at both workflow and activity levels
- Design for idempotency in activities
- Use versioning for workflow updates in production

## Resources

- [Temporal Documentation](https://docs.temporal.io)
- [Temporal Cloud](https://temporal.io/cloud)
- [TypeScript SDK](https://typescript.temporal.io)
- [Python SDK](https://python.temporal.io)
