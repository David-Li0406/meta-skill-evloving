---
name: workflow-pattern-project-mgmt
description: "Project management workflow patterns (tasks, approvals, notifications). Use when asking 'project workflow', 'task automation', or 'approval workflow'."
---

# Project Management Workflow Patterns

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Pattern: Task Approval Workflow

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Create task
workflow.add_node("DatabaseExecuteNode", "create_task", {
    "query": "INSERT INTO tasks (title, description, status) VALUES (?, ?, 'pending')",
    "parameters": ["{{input.title}}", "{{input.description}}"]
})

# 2. Notify approver
workflow.add_node("APICallNode", "notify_approver", {
    "url": "https://api.slack.com/messages",
    "method": "POST",
    "body": {"text": "New task needs approval: {{input.title}}"}
})

# 3. Wait for approval
workflow.add_node("WaitForEventNode", "wait_approval", {
    "event_type": "task_approved",
    "timeout": 86400  # 24 hours
})

# 4. Update status
workflow.add_node("DatabaseExecuteNode", "update_status", {
    "query": "UPDATE tasks SET status = 'approved' WHERE id = ?",
    "parameters": ["{{create_task.task_id}}"]
})

workflow.add_connection("create_task", "notify_approver")
workflow.add_connection("notify_approver", "wait_approval")
workflow.add_connection("wait_approval", "update_status")
```

<!-- Trigger Keywords: project workflow, task automation, approval workflow, project management -->
