---
name: workflow-pattern-business-rules
description: "Business rule engine patterns. Use when asking 'business rules', 'rule engine', 'conditional logic', or 'decision workflow'."
---

# Business Rule Engine Patterns

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Pattern: Discount Calculation Rules

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Load customer data
workflow.add_node("DatabaseQueryNode", "load_customer", {
    "query": "SELECT * FROM customers WHERE id = ?",
    "parameters": ["{{input.customer_id}}"]
})

# 2. Check membership tier
workflow.add_node("ConditionalNode", "check_tier", {
    "condition": "{{load_customer.tier}}",
    "branches": {
        "gold": "gold_discount",
        "silver": "silver_discount",
        "bronze": "bronze_discount"
    }
})

# 3. Calculate discounts
workflow.add_node("TransformNode", "gold_discount", {
    "input": "{{input.amount}}",
    "transformation": "value * 0.80"  # 20% off
})

workflow.add_node("TransformNode", "silver_discount", {
    "input": "{{input.amount}}",
    "transformation": "value * 0.90"  # 10% off
})

workflow.add_node("TransformNode", "bronze_discount", {
    "input": "{{input.amount}}",
    "transformation": "value * 0.95"  # 5% off
})

# 4. Apply additional rules
workflow.add_node("ConditionalNode", "check_bulk", {
    "condition": "{{input.quantity}} > 10",
    "true_branch": "bulk_discount",
    "false_branch": "final_price"
})

workflow.add_connection("load_customer", "check_tier")
workflow.add_connection("check_tier", "check_bulk")
```

<!-- Trigger Keywords: business rules, rule engine, conditional logic, decision workflow -->
