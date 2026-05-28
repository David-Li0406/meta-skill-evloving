---
name: distributed-transactions
description: "Distributed transaction patterns for workflows. Use when asking 'distributed transactions', 'transaction patterns', 'distributed SQL', 'transaction coordination', or 'ACID workflows'."
---

# Distributed Transactions

Distributed Transactions for database operations and query management.

> **Skill Metadata**
> Category: `database`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Distributed Transactions
- **Category**: database
- **Priority**: HIGH
- **Trigger Keywords**: distributed transactions, transaction patterns, distributed SQL

## Core Pattern

```python
from kailash.nodes.transaction import DistributedTransactionManagerNode

# Automatic pattern selection (Saga vs 2PC)
manager = DistributedTransactionManagerNode(
    transaction_name="business_process",
    state_storage="redis",
    storage_config={
        "redis_client": redis_client,
        "key_prefix": "transactions:"
    }
)

# Create transaction with requirements
result = manager.execute(
    operation="create_transaction",
    requirements={
        "consistency": "eventual",  # eventual, strong, immediate
        "availability": "high",     # high, medium, low
        "timeout": 300
    },
    context={"order_id": "123", "customer_id": "456"}
)

# Add participants with capabilities
participants = [
    {
        "participant_id": "payment_service",
        "endpoint": "http://payment:8080/api",
        "supports_2pc": True,
        "supports_saga": True,
        "compensation_action": "refund_payment"
    }
]

for participant in participants:
    manager.execute(operation="add_participant", **participant)

# Execute - DTM selects optimal pattern (Saga or 2PC)
result = manager.execute(operation="execute_transaction")
```

## Common Use Cases

- **Automatic Pattern Selection**: DTM intelligently chooses between Saga (high availability) or Two-Phase Commit (strong consistency) based on requirements and participant capabilities
- **Microservices Order Processing**: Coordinate multi-step order workflows across payment, inventory, shipping services with automatic compensation on failures
- **Financial Transfers**: Strong ACID guarantees with 2PC for money transfers between accounts/banks requiring immediate consistency
- **Cross-System Integration**: Handle mixed systems - legacy systems without 2PC support automatically trigger Saga pattern
- **Enterprise Workflows**: Production-ready patterns with Redis/database state persistence, monitoring, audit logging, and recovery

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

- 💡 **Let DTM Choose Pattern**: Specify requirements (consistency, availability) and let DistributedTransactionManagerNode select optimal pattern - "immediate" consistency forces 2PC, "eventual" prefers Saga
- 💡 **Mixed Capabilities Default to Saga**: If ANY participant doesn't support 2PC, DTM automatically uses Saga pattern for maximum compatibility
- 💡 **Use Redis for Production**: Configure state_storage="redis" with Redis cluster for high-performance, durable transaction state management
- 💡 **Implement Compensation Actions**: Every Saga step needs a compensation - refund payment, release inventory, cancel shipment, etc.
- 💡 **Monitor Transaction State**: Use get_status() to track execution, check for failures, and trigger manual recovery if needed
- 💡 **Pattern Selection Rules**: immediate consistency → 2PC (if supported), high availability → Saga, mixed systems → Saga, default → Saga

## Keywords for Auto-Trigger

<!-- Trigger Keywords: distributed transactions, transaction patterns, distributed SQL -->
