---
name: Execution Orchestrator
description: Parallel task execution and coordination when multiple independent tasks available
applyIntelligently: true
---

# Execution Orchestrator Skill

## Purpose

Execute multiple tasks in parallel for faster completion when tasks are independent.

## Trigger

- Multiple independent tasks identified
- Tasks can run concurrently without conflicts
- Parallel execution would save time
- Tools support parallel invocation

## Features

### Parallel Tool Execution

- **Multiple tools at once**: Read multiple files, run multiple commands simultaneously
- **Batch operations**: Group similar operations for efficiency
- **Independent tasks**: Only parallelize tasks with no dependencies

### Task Orchestration

- **Dependency management**: Ensure prerequisites complete before dependent tasks
- **Task prioritization**: Execute critical tasks first
- **Resource coordination**: Manage shared resources (files, locks)

### Result Aggregation

- **Combine results efficiently**: Merge parallel outputs intelligently
- **Handle partial failures**: Continue with successful results
- **Consolidate outputs**: Present unified results to user

## Usage Guidelines

**Parallelize when:**

- Tasks are independent (no shared state)
- Tools support concurrent execution
- Time savings justify complexity

**Sequential when:**

- Tasks have dependencies
- Shared state requires coordination
- Simplicity more important than speed

## Benefits

- 60% faster execution
- Better resource utilization
- Optimized token usage (shared context)

## Metrics

- **Parallel Tasks**: Number of parallel tasks executed
- **Execution Time**: Total vs serial time comparison
- **Token Efficiency**: Shared context usage optimization

## Usage

Agent automatically orchestrates tasks and executes tools in parallel when possible.
