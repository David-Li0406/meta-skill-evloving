---
name: dataflow-transactions
description: "DataFlow distributed transactions. Use when DataFlow transactions, saga, distributed transactions, 2PC, or transaction coordination."
---

# DataFlow Distributed Transactions

Distributed transaction patterns with saga and two-phase commit support.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+ / DataFlow 0.6.0`
> Related Skills: [`dataflow-crud-operations`](#), [`cycle-workflows-basics`](#)
> Related Subagents: `dataflow-specialist` (complex transactions)

## Quick Reference

- **Saga**: Compensating transactions for rollback
- **2PC**: Two-phase commit for ACID guarantees
- **Pattern**: Use TransactionManagerNode or context managers

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# Distributed transaction with saga pattern
workflow.add_node("TransactionManagerNode", "payment_flow", {
    "transaction_type": "saga",
    "steps": [
        {
            "node": "PaymentCreateNode",
            "compensation": "PaymentRollbackNode"
        },
        {
            "node": "OrderUpdateNode",
            "compensation": "OrderRevertNode"
        },
        {
            "node": "InventoryUpdateNode",
            "compensation": "InventoryRestoreNode"
        }
    ],
    "timeout": 30,
    "retry_attempts": 3
})
```

## Transaction Patterns

### Saga Pattern

```python
workflow.add_node("TransactionManagerNode", "saga", {
    "transaction_type": "saga",
    "steps": [
        {"node": "Step1Node", "compensation": "Undo1Node"},
        {"node": "Step2Node", "compensation": "Undo2Node"}
    ]
})
```

### Two-Phase Commit

```python
workflow.add_node("TransactionManagerNode", "2pc", {
    "transaction_type": "two_phase_commit",
    "steps": [...]
})
```

## Documentation References

### Primary Sources
- **Transactions Guide**: [`sdk-users/apps/dataflow/docs/workflows/transactions.md`](../../../../sdk-users/apps/dataflow/docs/workflows/transactions.md)
- **Transaction Context**: [`sdk-users/apps/dataflow/docs/workflows/transaction-context.md`](../../../../sdk-users/apps/dataflow/docs/workflows/transaction-context.md)
- **Distributed Transactions**: [`sdk-users/2-core-concepts/cheatsheet/049-distributed-transactions.md`](../../../../sdk-users/2-core-concepts/cheatsheet/049-distributed-transactions.md)

### Related Documentation
- **README**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L863-L874)

## Quick Tips

- Use saga for long-running transactions
- Use 2PC for strong consistency
- Define compensation actions
- Set appropriate timeouts

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow transactions, saga, distributed transactions, 2PC, transaction coordination, compensating transactions -->
