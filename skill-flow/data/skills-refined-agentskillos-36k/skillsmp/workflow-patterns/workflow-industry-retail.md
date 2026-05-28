---
name: workflow-industry-retail
description: "Retail/e-commerce workflows (orders, inventory, shipping). Use when asking 'retail workflow', 'e-commerce', 'order processing', or 'inventory sync'."
---

# Retail/E-Commerce Workflows

> **Skill Metadata**
> Category: `industry-workflows`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Pattern: Order Fulfillment Workflow

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Receive order
workflow.add_node("DatabaseExecuteNode", "create_order", {
    "query": "INSERT INTO orders (customer_id, items, total) VALUES (?, ?, ?)",
    "parameters": ["{{input.customer_id}}", "{{input.items}}", "{{input.total}}"]
})

# 2. Check inventory
workflow.add_node("DatabaseQueryNode", "check_inventory", {
    "query": "SELECT quantity FROM inventory WHERE product_id = ?",
    "parameters": ["{{input.product_id}}"]
})

# 3. Reserve stock
workflow.add_node("DatabaseExecuteNode", "reserve_stock", {
    "query": "UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?",
    "parameters": ["{{input.quantity}}", "{{input.product_id}}"]
})

# 4. Process payment
workflow.add_node("APICallNode", "payment", {
    "url": "https://api.stripe.com/charges",
    "method": "POST",
    "body": {"amount": "{{input.total}}", "customer": "{{input.customer_id}}"}
})

# 5. Create shipping label
workflow.add_node("APICallNode", "shipping", {
    "url": "https://api.shippo.com/shipments",
    "method": "POST",
    "body": {"address": "{{input.address}}", "weight": "{{input.weight}}"}
})

# 6. Send confirmation
workflow.add_node("APICallNode", "notify_customer", {
    "url": "https://api.sendgrid.com/mail/send",
    "method": "POST",
    "body": {"to": "{{input.email}}", "subject": "Order Confirmed", "tracking": "{{shipping.tracking_number}}"}
})

workflow.add_connection("create_order", "check_inventory")
workflow.add_connection("check_inventory", "reserve_stock")
workflow.add_connection("reserve_stock", "payment")
workflow.add_connection("payment", "shipping")
workflow.add_connection("shipping", "notify_customer")
```

<!-- Trigger Keywords: retail workflow, e-commerce, order processing, inventory sync, order fulfillment -->
