---
name: saga-pattern
description: "Saga pattern for distributed workflows. Use when asking 'saga pattern', 'distributed saga', 'compensating transactions', 'saga workflows', or 'distributed coordination'."
---

# Saga Pattern

Saga Pattern for database operations and query management.

> **Skill Metadata**
> Category: `database`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Saga Pattern
- **Category**: database
- **Priority**: HIGH
- **Trigger Keywords**: saga pattern, distributed saga, compensating transactions, saga workflows

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Create saga coordinator for distributed transactions
workflow = WorkflowBuilder()
workflow.add_node("SagaCoordinatorNode", "saga", {
    "operation": "create_saga",
    "saga_name": "order_processing",
    "timeout": 600.0,
    "context": {"user_id": "user123", "order_id": "order456"}
})

# Configure saga steps with compensations
workflow.add_node("PythonCodeNode", "add_steps", {
    "code": """
steps_config = [
    {
        "name": "validate_order",
        "node_id": "ValidationNode",
        "parameters": {"check_inventory": True},
        "compensation_node_id": "CancelValidationNode"
    },
    {
        "name": "charge_payment",
        "node_id": "PaymentNode",
        "parameters": {"amount": 100.0},
        "compensation_node_id": "RefundPaymentNode"
    }
]
result = {"steps": steps_config}
"""
})

workflow.add_connection("saga", "saga_id", "add_steps", "saga_id")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Use Cases

- **Order Processing Workflows**: Multi-step order processing with inventory checks, payment processing, and shipment creation - each with automatic compensations on failure
- **Microservices Coordination**: Distributed transactions across multiple services where each service operation can be independently compensated
- **Multi-Database Operations**: Coordinating writes across multiple databases with automatic rollback through compensation actions
- **Long-Running Business Processes**: Managing complex workflows with state persistence, resumability, and automatic error recovery
- **API Integration Workflows**: Chaining external API calls where failures require undoing previous operations (e.g., cancel reservation, refund payment)

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For patterns**: See [`workflow-patterns-library`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex patterns, multi-node workflows
- **sdk-navigator**: Error resolution, parameter issues
- **testing-specialist**: Comprehensive testing strategies

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/`](../../../sdk-users/2-core-concepts/cheatsheet/)

## Quick Tips

- 💡 **Always Define Compensations**: Every saga step must have a compensation action to handle failures and maintain consistency
- 💡 **Make Steps Idempotent**: Steps should be safely retryable - use idempotency keys or check-before-execute patterns
- 💡 **Keep Steps Atomic**: Each step should be a single, coherent operation that can be independently compensated
- 💡 **Test Compensation Paths**: Explicitly test failure scenarios to ensure compensations work correctly before production
- 💡 **Use State Persistence**: Configure Redis or database storage for saga state to enable resumability after system failures
- 💡 **Handle Partial Failures**: Plan for compensation failures with manual intervention workflows and alerting
- 💡 **Set Realistic Timeouts**: Configure appropriate timeouts for both steps and compensations based on expected operation duration

## Keywords for Auto-Trigger

<!-- Trigger Keywords: saga pattern, distributed saga, compensating transactions, saga workflows -->
