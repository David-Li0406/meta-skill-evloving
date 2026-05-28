---
name: nodes-transaction-reference
description: "Transaction nodes reference (Saga, 2PC, DTM). Use when asking 'transaction node', 'Saga', '2PC', 'distributed transaction', or 'transaction coordinator'."
---

# Transaction Nodes Reference

Complete reference for distributed transaction management nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (transaction patterns)

## Quick Reference

```python
from kailash.nodes.transaction import (
    DistributedTransactionManagerNode,  # Auto-select pattern
    SagaCoordinatorNode,  # High availability
    SagaStepNode,
    TwoPhaseCommitCoordinatorNode  # Strong consistency
)
```

## Automatic Pattern Selection

### DistributedTransactionManagerNode ⭐
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# Auto-select Saga or 2PC based on requirements
workflow.add_node("DistributedTransactionManagerNode", "dtm", {
    "transaction_id": "txn_123",
    "participants": [
        {"service": "order_service", "supports_2pc": True},
        {"service": "payment_service", "supports_2pc": True},
        {"service": "inventory_service", "supports_2pc": False}
    ],
    "pattern": "auto"  # or "saga", "2pc"
})
```

## Saga Pattern (High Availability)

### SagaCoordinatorNode
```python
workflow.add_node("SagaCoordinatorNode", "saga", {
    "saga_id": "saga_123",
    "steps": [
        {"service": "order", "action": "create_order", "compensation": "cancel_order"},
        {"service": "payment", "action": "charge", "compensation": "refund"},
        {"service": "inventory", "action": "reserve", "compensation": "release"}
    ]
})
```

### SagaStepNode
```python
workflow.add_node("SagaStepNode", "step", {
    "saga_id": "saga_123",
    "step_name": "create_order",
    "action": "execute",
    "compensation_action": "cancel_order"
})
```

## Two-Phase Commit (Strong Consistency)

### TwoPhaseCommitCoordinatorNode
```python
workflow.add_node("TwoPhaseCommitCoordinatorNode", "2pc", {
    "transaction_id": "txn_123",
    "participants": [
        {"service": "order_db", "endpoint": "/prepare"},
        {"service": "payment_db", "endpoint": "/prepare"},
        {"service": "inventory_db", "endpoint": "/prepare"}
    ],
    "timeout": 30
})
```

## When to Use Each Pattern

| Pattern | Use When | Benefits |
|---------|----------|----------|
| **DistributedTransactionManagerNode** | Mixed capabilities | Auto-selection |
| **SagaCoordinatorNode** | High availability needed | Eventual consistency |
| **TwoPhaseCommitCoordinatorNode** | Strong consistency required | ACID properties |

## Related Skills

- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Transaction Nodes**: [`sdk-users/2-core-concepts/nodes/transaction-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/transaction-nodes.md)

<!-- Trigger Keywords: transaction node, Saga, 2PC, distributed transaction, transaction coordinator, SagaCoordinatorNode, TwoPhaseCommitCoordinatorNode -->
