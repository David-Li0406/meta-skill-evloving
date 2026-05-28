---
name: swarm-orchestration
description:
  Use when distributing multiple tasks across agents or VMs - handles work manifests,
  dependency graphs, parallel execution, agent coordination, and failure recovery for
  batch development workflows
---

# Swarm Orchestration

## Overview

Coordinate multiple /autotask executions across distributed agents. Each task runs in
isolation, produces its own PR, and reports back to the orchestrator. Git branches are
the source of truth, agents are stateless workers.

## When to Use

- Batch of 3+ independent development tasks
- Sprint planning with parallelizable work items
- Large refactoring split across multiple areas
- When local CPU is overwhelmed by single-agent work
- CI/CD integration needing parallel task execution

When NOT to use: Single task (use /autotask directly), tasks with heavy interdependencies
that can't be parallelized, exploratory work without clear task boundaries.

## Core Pattern

Work manifests define tasks declaratively:

```yaml
name: "Sprint 47"
base_branch: main
tasks:
  - id: feature-a
    prompt: "Implement feature A following existing patterns"
    branch: feature/a
  - id: feature-b
    prompt: "Implement feature B with tests"
    branch: feature/b
  - id: feature-c
    prompt: "Implement feature C"
    branch: feature/c
    depends_on: [feature-a]  # Waits for feature-a PR
```

Orchestrator builds dependency graph, distributes ready tasks to available agents,
monitors progress, handles failures gracefully.

## Dependency Resolution

Tasks form a directed acyclic graph (DAG). Execution order:

1. Tasks with no dependencies start immediately (parallel)
2. Tasks with dependencies wait until all dependencies have PRs
3. Circular dependencies are detected and rejected at parse time

```yaml
# Parallel: a, b, c run simultaneously
# Sequential: d waits for a AND b, e waits for d
tasks:
  - id: a
  - id: b  
  - id: c
  - id: d
    depends_on: [a, b]
  - id: e
    depends_on: [d]
```

## Agent Communication

Agents expose simple HTTP endpoints:

```
GET  /status   → { status: "idle"|"busy", current_task?: string }
POST /execute  → { task_id, prompt, branch, repo } → { accepted: true }
GET  /progress → { task_id, percent, stage, logs }
```

Orchestrator polls or uses WebSocket for real-time updates. Agents are stateless - if
one crashes, task is reassigned to another.

## Failure Handling

Task failure is isolated. Independent tasks continue. Only dependent tasks block.

```
task-a: SUCCESS → PR #101
task-b: FAILED  → logged, retryable
task-c: SUCCESS → PR #102  (independent of b)
task-d: BLOCKED → waiting on task-b (depends_on: [b])
```

Recovery: `--retry task-b` to retry failed task, `--skip task-b` to unblock dependents.

## State Persistence

Minimal state in `.swarm/state.json`:

```json
{
  "manifest": "work.yaml",
  "started": "2024-01-15T10:00:00Z",
  "tasks": {
    "feature-a": { "status": "complete", "pr": 101 },
    "feature-b": { "status": "in_progress", "agent": "oracle-1" },
    "feature-c": { "status": "queued" }
  }
}
```

Git branches are the real state. State file enables resume after interruption.

## Common Pitfalls

Over-specifying dependencies: Tasks that could run parallel marked as sequential.
Analyze actual dependencies, not assumed order.

Huge task prompts: Each task should be /autotask-sized (single feature, single PR).
Split large features into multiple tasks.

Missing base_branch: Tasks branch from wrong base, causing merge conflicts. Always
specify base_branch in manifest.

Agent exhaustion: Too many tasks, not enough agents. Orchestrator queues excess tasks,
but consider agent capacity when planning sprints.
