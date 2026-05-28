---
name: dataflow-custom-nodes
description: "Extend DataFlow with custom nodes beyond the auto-generated 9. Use when asking 'custom dataflow nodes', 'extend dataflow', or 'custom operations'."
---

# Custom DataFlow Nodes

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`dataflow-specialist`](dataflow-specialist.md)

## Add Custom Workflow Nodes

DataFlow auto-generates 9 nodes per model, but you can add custom business logic:

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder

db = DataFlow("sqlite:///app.db")

@db.model
class User:
    id: str
    email: str
    status: str

# Use auto-generated nodes
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create_user", {
    "email": "{{input.email}}",
    "status": "active"
})

# Add custom business logic node
workflow.add_node("APICallNode", "send_welcome_email", {
    "url": "https://api.sendgrid.com/mail/send",
    "method": "POST",
    "body": {
        "to": "{{create_user.email}}",
        "subject": "Welcome!",
        "template": "welcome"
    }
})

# Add custom validation node
workflow.add_node("ConditionalNode", "check_domain", {
    "condition": "{{create_user.email}}.endswith('@company.com')",
    "true_branch": "internal_user",
    "false_branch": "external_user"
})

workflow.add_connection("create_user", "send_welcome_email")
workflow.add_connection("send_welcome_email", "check_domain")
```

## Custom Aggregation Nodes

```python
# Use DataFlow nodes + custom aggregation
workflow.add_node("UserListNode", "get_users", {
    "filters": {"status": "active"}
})

# Custom aggregation with TransformNode
workflow.add_node("TransformNode", "calculate_metrics", {
    "input": "{{get_users.users}}",
    "transformation": """
        total = len(input)
        domains = {}
        for user in input:
            domain = user['email'].split('@')[1]
            domains[domain] = domains.get(domain, 0) + 1
        return {'total': total, 'domains': domains}
    """
})

workflow.add_connection("get_users", "calculate_metrics")
```

## Best Practices

1. **Use auto-generated nodes first** - Don't reinvent CRUD
2. **Add business logic nodes** - API calls, validations, notifications
3. **Compose workflows** - Combine DataFlow + Core SDK nodes
4. **Keep models simple** - DataFlow handles data, custom nodes handle logic

## Documentation

- **Custom Nodes**: [`sdk-users/apps/dataflow/07-advanced-patterns.md#custom-nodes`](../../../../sdk-users/apps/dataflow/07-advanced-patterns.md)

<!-- Trigger Keywords: custom dataflow nodes, extend dataflow, custom operations, dataflow business logic -->
