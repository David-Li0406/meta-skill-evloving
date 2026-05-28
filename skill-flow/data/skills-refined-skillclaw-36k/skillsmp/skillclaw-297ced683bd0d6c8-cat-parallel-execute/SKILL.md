---
name: cat:parallel-execute
description: Use this skill when you need to orchestrate multiple independent subagents concurrently to maximize throughput and efficiently manage tasks with no dependencies.
---

# Parallel Execute

## Purpose

Launch and manage multiple independent subagents simultaneously to maximize throughput. This skill coordinates spawning, monitoring, result collection, and merging for tasks that can execute in complete isolation, making it essential for efficient use of CAT's multi-agent capabilities.

## When to Use

- When multiple tasks have no dependencies between them
- When tasks can execute in complete isolation
- When the parent agent needs to coordinate multiple work streams
- When optimizing for wall-clock time rather than token efficiency
- **AUTO-TRIGGERED:** After the `decompose-task` creates independent subtasks

## Auto-Trigger from Decomposition

When `/cat:work` triggers auto-decomposition (task exceeds context threshold), this skill is automatically invoked for parallel execution:

```
work → analyze_task_size → (exceeds threshold) → decompose-task → parallel-execute
```

**Integration Workflow:**

1. `work` estimates task size > threshold (e.g., 80K tokens)
2. `work` auto-invokes `decompose-task`
3. `decompose-task` creates subtasks and generates a parallel execution plan
4. `decompose-task` identifies sub-task-based parallelization
5. `work` auto-invokes `parallel-execute` with the sub-task plan
6. `parallel-execute` spawns subagents for each sub-task

**Example Auto-Trigger Flow:**

```yaml
# work detects large task
task: 1.2-implement-parser
estimated_tokens: 120000
# See agent-architecture.md § Context Limit Constants for threshold

# Auto-decomposition triggered
decomposed_into:
  - 1.2a-parser-lexer (25K tokens)
  - 1.2b-parser-ast (30K tokens)
  - 1.2c-parser-semantic (25K tokens)

# Parallel plan generated
parallel_plan:
  sub_task_1: [1.2a, 1.2c]  # Independent, run concurrently
  sub_task_2: [1.2b]         # Depends on 1.2a

# Auto-parallel execution
action: spawn 2 subagents for sub_task_1
```

## Workflow

**Progress Output (MANDATORY):**

Display sub-task-based progress for parallel execution:
```
═══════════════════════════════════════════════════
Sub-task N/M: Spawning K subagents (P% overall | Xs elapsed)
═══════════════════════════════════════════════════
[Subagent 1/K] task-name-a... spawned
[Subagent 2/K] task-name-b... spawned

Sub-task N/M: Monitoring K subagents (P% | Xs elapsed | ~Ys remaining)
  ✓ task-name-a: complete (12s, 45K tokens)
  ⏳ task-name-b: running (8s elapsed)

Sub-task N/M: Collecting results (P% | Xs elapsed)
```