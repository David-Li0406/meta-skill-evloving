---
name: workflow-patterns
description: Common workflow patterns and coordination strategies for multi-agent orchestration
---

# Workflow Patterns

A technology-agnostic skill for managing multi-agent workflows and coordination.

## Core Patterns

### Sequential Chain Pattern

```yaml
pattern: sequential_chain
description: "Agents execute in strict order, each depends on previous"
use_when:
  - "Output of one agent is input to next"
  - "Strict dependency exists"
  - "Order matters for correctness"

example:
  - goal-clarifier → design-architect → code-developer → test-executor

implementation:
  wait_for_completion: true
  pass_output_to_next: true
  stop_on_failure: true
```

### Parallel Execution Pattern

```yaml
pattern: parallel_execution
description: "Independent agents execute simultaneously"
use_when:
  - "Tasks are independent"
  - "No data dependencies"
  - "Time optimization needed"

example:
  parallel_group:
    - code-developer (module A)
    - code-developer (module B)
    - code-developer (module C)

implementation:
  launch_simultaneously: true
  aggregate_results: true
  fail_fast: optional
```

### Fork-Join Pattern

```yaml
pattern: fork_join
description: "Parallel execution with synchronization point"
use_when:
  - "Multiple independent tasks"
  - "Need to combine results"
  - "Subsequent step needs all outputs"

example:
  fork:
    - quality-reviewer (security check)
    - quality-reviewer (performance check)
    - quality-reviewer (style check)
  join:
    - deliverable-evaluator (combines all results)

implementation:
  fork_point: "After code-developer completes"
  join_point: "Before deliverable-evaluator"
  aggregation: "Combine all review results"
```

### Iteration Pattern

```yaml
pattern: iteration
description: "Repeat until success or max iterations"
use_when:
  - "Quality gates must pass"
  - "Debugging cycles needed"
  - "Refinement required"

example:
  loop:
    - code-developer (implement/fix)
    - test-executor (verify)
    - test-debugger (if failure, analyze)
  exit_condition: "All tests pass OR max_iterations reached"

implementation:
  max_iterations: 3
  track_iteration_count: true
  escalation_on_max: "Notify user"
```

### Conditional Routing Pattern

```yaml
pattern: conditional_routing
description: "Route based on evaluation results"
use_when:
  - "Different paths for different outcomes"
  - "Branch based on criteria"

example:
  evaluate: deliverable-evaluator
  routes:
    PASS: workflow-orchestrator (commit)
    FAIL: code-developer (rework)

implementation:
  decision_point: "Agent output"
  routing_logic: "Based on verdict/status"
```

## Workflow Templates

### Standard Implementation Workflow

```yaml
template: standard_implementation
scale: small|medium

steps:
  1:
    agent: workflow-orchestrator
    task: "Initialize workflow, track progress"

  2:
    agent: code-developer
    task: "Implement feature"
    chain_to: test-executor

  3:
    agent: test-executor
    task: "Run tests"
    on_failure: test-debugger
    on_success: quality-reviewer

  4:
    agent: quality-reviewer
    task: "Review code quality"
    on_issues: code-developer
    on_pass: deliverable-evaluator

  5:
    agent: deliverable-evaluator
    task: "Final evaluation"
    on_pass: workflow-orchestrator (commit)
    on_fail: (route to appropriate agent)
```

### Full Feature Workflow

```yaml
template: full_feature
scale: large

steps:
  1:
    agent: workflow-orchestrator
    task: "Initialize"

  2:
    agent: design-architect
    task: "Create architecture"

  3:
    agent: code-developer
    task: "Implement"
    iterations: "As needed"

  4:
    agent: test-executor
    task: "Test"
    debug_loop: test-debugger

  5:
    agent: quality-reviewer
    task: "Review"

  6:
    agent: deliverable-evaluator
    task: "Evaluate against acceptance criteria"
    iterations: "Max 3"

  7:
    agent: workflow-orchestrator
    task: "Commit and complete"
```

### Debug Loop Workflow

```yaml
template: debug_loop
trigger: "Test failures"

steps:
  loop_start:
    agent: test-executor
    task: "Run failing tests"

  analyze:
    agent: test-debugger
    task: "Identify root cause"

  fix:
    agent: code-developer
    task: "Apply fix"

  verify:
    agent: test-executor
    task: "Verify fix"
    exit_if: "All tests pass"
    continue_if: "Failures remain"

exit_conditions:
  - "All tests pass"
  - "Max iterations (3)"
  - "User intervention requested"
```

## Coordination Strategies

### Progress Tracking

```yaml
tracking:
  per_task:
    - id: "<task_id>"
    - status: pending|in_progress|completed|blocked
    - agent: "<assigned_agent>"
    - started_at: "<timestamp>"
    - completed_at: "<timestamp>"
    - result: "<summary>"

  overall:
    - total_tasks: <number>
    - completed: <number>
    - in_progress: <number>
    - blocked: <number>
    - progress_percentage: <percent>
```

### Handoff Protocol

```yaml
handoff:
  from_agent:
    - Summarize work done
    - List files modified
    - Note any issues
    - Specify next action needed

  to_agent:
    - Receive context
    - Verify prerequisites
    - Begin work
    - Report completion
```

### Error Handling

```yaml
error_handling:
  agent_failure:
    action: "Log error, attempt recovery"
    recovery: "Retry once, then escalate"

  timeout:
    threshold: "Configurable per agent"
    action: "Cancel and notify"

  blocked_task:
    detection: "No progress after N minutes"
    action: "Escalate to user"
```

## Anti-Patterns

### Over-Orchestration

```yaml
anti_pattern: over_orchestration
description: "Too many agents for simple tasks"
symptom: "5+ agents for trivial changes"
solution: "Match workflow to task scale"
```

### Circular Dependencies

```yaml
anti_pattern: circular_dependencies
description: "Agents waiting for each other"
symptom: "Deadlock in workflow"
solution: "Clear dependency ordering"
```

### Missing Exit Conditions

```yaml
anti_pattern: infinite_loop
description: "Iteration without exit condition"
symptom: "Workflow never completes"
solution: "Always define max_iterations and exit criteria"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - main-orchestrator: "Workflow selection"
  - workflow-orchestrator: "Coordination"

secondary_users:
  - task-scale-evaluator: "Workflow recommendations"
```
