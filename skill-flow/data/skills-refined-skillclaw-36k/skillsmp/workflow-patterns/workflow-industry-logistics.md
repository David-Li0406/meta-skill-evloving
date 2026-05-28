---
name: workflow-industry-logistics
description: "Logistics/supply chain workflows (tracking, routing, delivery). Use when asking 'logistics workflow', 'supply chain', 'shipment tracking', or 'route optimization'."
---

# Logistics/Supply Chain Workflows

> **Skill Metadata**
> Category: `industry-workflows`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Pattern: Shipment Tracking and Delivery

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Create shipment
workflow.add_node("DatabaseExecuteNode", "create_shipment", {
    "query": "INSERT INTO shipments (origin, destination, status) VALUES (?, ?, 'pending')",
    "parameters": ["{{input.origin}}", "{{input.destination}}"]
})

# 2. Calculate optimal route
workflow.add_node("APICallNode", "route_optimization", {
    "url": "https://api.routingengine.com/optimize",
    "method": "POST",
    "body": {"origin": "{{input.origin}}", "destination": "{{input.destination}}"}
})

# 3. Assign to driver
workflow.add_node("DatabaseQueryNode", "find_driver", {
    "query": "SELECT id FROM drivers WHERE status = 'available' AND location_near(?, 50) LIMIT 1",
    "parameters": ["{{input.origin}}"]
})

# 4. Update shipment with route
workflow.add_node("DatabaseExecuteNode", "update_shipment", {
    "query": "UPDATE shipments SET driver_id = ?, route = ?, status = 'in_transit' WHERE id = ?",
    "parameters": ["{{find_driver.id}}", "{{route_optimization.route}}", "{{create_shipment.id}}"]
})

# 5. Real-time tracking
workflow.add_node("LoopNode", "track_location", {
    "condition": "{{current_status}} != 'delivered'",
    "interval": 300  # Check every 5 minutes
})

# 6. Update delivery status
workflow.add_node("DatabaseExecuteNode", "mark_delivered", {
    "query": "UPDATE shipments SET status = 'delivered', delivered_at = NOW() WHERE id = ?",
    "parameters": ["{{create_shipment.id}}"]
})

workflow.add_connection("create_shipment", "route_optimization")
workflow.add_connection("route_optimization", "find_driver")
workflow.add_connection("find_driver", "update_shipment")
workflow.add_connection("update_shipment", "track_location")
workflow.add_connection("track_location", "mark_delivered")
```

<!-- Trigger Keywords: logistics workflow, supply chain, shipment tracking, route optimization, delivery -->
