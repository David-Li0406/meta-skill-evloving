---
name: workflow-pattern-cyclic
description: "Cyclic workflow patterns with loops and iterations. Use when asking 'loop workflow', 'cyclic', 'iterate', 'repeat until', or 'workflow cycles'."
---

# Cyclic Workflow Patterns

Patterns for implementing loops, iterations, and cyclic workflows.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`workflow-pattern-etl`](workflow-pattern-etl.md), [`pattern-expert`](../../01-core-sdk/pattern-expert.md)
> Related Subagents: `pattern-expert` (cyclic workflows)

## Quick Reference

Cyclic workflows enable:
- **Loop until condition** - Repeat until success/threshold
- **Batch processing** - Process items in chunks
- **Retry logic** - Automatic retry with backoff
- **Iterative refinement** - Multi-pass processing

## Pattern 1: Loop Until Condition

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# 1. Initialize counter
workflow.add_node("SetVariableNode", "init_counter", {
    "variable_name": "counter",
    "value": 0
})

# 2. Process iteration
workflow.add_node("APICallNode", "check_status", {
    "url": "https://api.example.com/status",
    "method": "GET"
})

# 3. Evaluate condition
workflow.add_node("ConditionalNode", "check_complete", {
    "condition": "{{check_status.status}} == 'completed'",
    "true_branch": "complete",
    "false_branch": "increment"
})

# 4. Increment counter
workflow.add_node("TransformNode", "increment", {
    "input": "{{init_counter.counter}}",
    "transformation": "value + 1"
})

# 5. Check max iterations
workflow.add_node("ConditionalNode", "check_max", {
    "condition": "{{increment.result}} < 10",
    "true_branch": "wait",
    "false_branch": "timeout"
})

# 6. Wait before retry
workflow.add_node("DelayNode", "wait", {
    "duration_seconds": 5
})

# 7. Loop back (connect to check_status)
workflow.add_connection("init_counter", "check_status")
workflow.add_connection("check_status", "check_complete")
workflow.add_connection("check_complete", "increment", "false")
workflow.add_connection("increment", "check_max")
workflow.add_connection("check_max", "wait", "true")
workflow.add_connection("wait", "check_status")  # Loop!

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Pattern 2: Batch Processing

```python
workflow = WorkflowBuilder()

# 1. Load all items
workflow.add_node("DatabaseQueryNode", "load_items", {
    "query": "SELECT id, data FROM items WHERE processed = FALSE",
    "batch_size": 100
})

# 2. Split into batches
workflow.add_node("BatchSplitNode", "split_batches", {
    "input": "{{load_items.results}}",
    "batch_size": 10
})

# 3. Process each batch
workflow.add_node("MapNode", "process_batch", {
    "input": "{{split_batches.batches}}",
    "operation": "process_item"
})

# 4. Update database
workflow.add_node("DatabaseExecuteNode", "mark_processed", {
    "query": "UPDATE items SET processed = TRUE WHERE id IN ({{process_batch.ids}})"
})

# 5. Check for more items
workflow.add_node("ConditionalNode", "check_more", {
    "condition": "{{load_items.has_more}} == true",
    "true_branch": "load_items",  # Loop back!
    "false_branch": "complete"
})

workflow.add_connection("load_items", "split_batches")
workflow.add_connection("split_batches", "process_batch")
workflow.add_connection("process_batch", "mark_processed")
workflow.add_connection("mark_processed", "check_more")
workflow.add_connection("check_more", "load_items", "true")
```

## Pattern 3: Exponential Backoff Retry

```python
workflow = WorkflowBuilder()

# 1. Initialize retry state
workflow.add_node("SetVariableNode", "init_retry", {
    "retry_count": 0,
    "backoff_seconds": 1
})

# 2. Execute operation
workflow.add_node("APICallNode", "api_call", {
    "url": "https://api.example.com/operation",
    "method": "POST",
    "timeout": 30
})

# 3. Check success
workflow.add_node("ConditionalNode", "check_success", {
    "condition": "{{api_call.status_code}} == 200",
    "true_branch": "success",
    "false_branch": "check_retry"
})

# 4. Check retry count
workflow.add_node("ConditionalNode", "check_retry", {
    "condition": "{{init_retry.retry_count}} < 5",
    "true_branch": "calculate_backoff",
    "false_branch": "failed"
})

# 5. Calculate exponential backoff
workflow.add_node("TransformNode", "calculate_backoff", {
    "input": "{{init_retry.backoff_seconds}}",
    "transformation": "value * 2"  # Exponential: 1, 2, 4, 8, 16 seconds
})

# 6. Wait with backoff
workflow.add_node("DelayNode", "backoff_wait", {
    "duration_seconds": "{{calculate_backoff.result}}"
})

# 7. Increment retry counter
workflow.add_node("TransformNode", "increment_retry", {
    "input": "{{init_retry.retry_count}}",
    "transformation": "value + 1"
})

# 8. Loop back to retry
workflow.add_connection("init_retry", "api_call")
workflow.add_connection("api_call", "check_success")
workflow.add_connection("check_success", "check_retry", "false")
workflow.add_connection("check_retry", "calculate_backoff", "true")
workflow.add_connection("calculate_backoff", "backoff_wait")
workflow.add_connection("backoff_wait", "increment_retry")
workflow.add_connection("increment_retry", "api_call")  # Loop!
```

## Pattern 4: Iterative Refinement

```python
workflow = WorkflowBuilder()

# 1. Initial prompt
workflow.add_node("SetVariableNode", "init_prompt", {
    "prompt": "Write a product description for: {{product_name}}",
    "iteration": 0
})

# 2. Generate content (LLM)
workflow.add_node("LLMNode", "generate", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "{{init_prompt.prompt}}"
})

# 3. Evaluate quality
workflow.add_node("LLMNode", "evaluate", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "Rate this description 1-10: {{generate.response}}"
})

# 4. Check quality threshold
workflow.add_node("ConditionalNode", "check_quality", {
    "condition": "{{evaluate.score}} >= 8",
    "true_branch": "approved",
    "false_branch": "refine"
})

# 5. Refine prompt with feedback
workflow.add_node("LLMNode", "refine", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "Improve this: {{generate.response}}. Feedback: {{evaluate.feedback}}"
})

# 6. Check max iterations
workflow.add_node("ConditionalNode", "check_max", {
    "condition": "{{init_prompt.iteration}} < 3",
    "true_branch": "increment",
    "false_branch": "use_best"
})

# 7. Increment iteration
workflow.add_node("TransformNode", "increment", {
    "input": "{{init_prompt.iteration}}",
    "transformation": "value + 1"
})

# Loop back for refinement
workflow.add_connection("init_prompt", "generate")
workflow.add_connection("generate", "evaluate")
workflow.add_connection("evaluate", "check_quality")
workflow.add_connection("check_quality", "refine", "false")
workflow.add_connection("refine", "check_max")
workflow.add_connection("check_max", "increment", "true")
workflow.add_connection("increment", "generate")  # Loop!
```

## Best Practices

1. **Always set max iterations** - Prevent infinite loops
2. **Use explicit loop counters** - Track iteration count
3. **Implement backoff delays** - Avoid overwhelming systems
4. **Store intermediate results** - Enable debugging/recovery
5. **Clear exit conditions** - Define success/failure states
6. **Monitor loop metrics** - Track iterations, duration, success rate

## Common Pitfalls

- **No exit condition** - Infinite loops
- **Missing max iterations** - Runaway processes
- **No backoff delay** - API rate limiting
- **Memory leaks** - Accumulating state in loops
- **Poor error handling** - Unhandled failures in iterations

## Related Skills

- **ETL Patterns**: [`workflow-pattern-etl`](workflow-pattern-etl.md)
- **Error Handling**: [`gold-error-handling`](../../17-gold-standards/gold-error-handling.md)
- **Conditional Logic**: [`nodes-logic-reference`](../nodes/nodes-logic-reference.md)

## Documentation

- **Workflow Patterns**: [`sdk-users/2-core-concepts/workflows/05-workflow-patterns.md`](../../../../sdk-users/2-core-concepts/workflows/05-workflow-patterns.md)
- **Advanced Patterns**: [`sdk-users/7-advanced-topics/workflows/advanced-workflow-patterns.md`](../../../../sdk-users/7-advanced-topics/workflows/advanced-workflow-patterns.md)

<!-- Trigger Keywords: loop workflow, cyclic, iterate, repeat until, workflow cycles, retry logic, batch processing -->
