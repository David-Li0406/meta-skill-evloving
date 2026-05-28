---
name: workflow-pattern-security
description: "Security workflow patterns (auth, encryption, audit). Use when asking 'security workflow', 'authentication', 'encryption workflow', or 'audit trail'."
---

# Security Workflow Patterns

Patterns for authentication, authorization, encryption, and audit workflows.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`gold-security`](../../17-gold-standards/gold-security.md)

## Pattern: User Authentication Flow

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Validate credentials
workflow.add_node("DatabaseQueryNode", "check_user", {
    "query": "SELECT id, password_hash, role FROM users WHERE email = ?",
    "parameters": ["{{input.email}}"]
})

# 2. Verify password
workflow.add_node("TransformNode", "verify_password", {
    "input": "{{input.password}}",
    "stored_hash": "{{check_user.password_hash}}",
    "transformation": "bcrypt.verify(input, stored_hash)"
})

# 3. Check authorization
workflow.add_node("ConditionalNode", "check_auth", {
    "condition": "{{verify_password.match}} == true",
    "true_branch": "generate_token",
    "false_branch": "audit_failure"
})

# 4. Generate JWT
workflow.add_node("TransformNode", "generate_token", {
    "input": {"user_id": "{{check_user.id}}", "role": "{{check_user.role}}"},
    "transformation": "jwt.encode(input, secret, algorithm='HS256')"
})

# 5. Audit log
workflow.add_node("DatabaseExecuteNode", "audit_success", {
    "query": "INSERT INTO audit_log (user_id, action, timestamp) VALUES (?, 'login', NOW())",
    "parameters": ["{{check_user.id}}"]
})

workflow.add_node("DatabaseExecuteNode", "audit_failure", {
    "query": "INSERT INTO audit_log (email, action, timestamp) VALUES (?, 'failed_login', NOW())",
    "parameters": ["{{input.email}}"]
})

workflow.add_connection("check_user", "verify_password")
workflow.add_connection("verify_password", "check_auth")
workflow.add_connection("check_auth", "generate_token", "true")
workflow.add_connection("generate_token", "audit_success")
workflow.add_connection("check_auth", "audit_failure", "false")
```

## Documentation

- **Security**: [`sdk-users/7-advanced-topics/security/security-patterns.md`](../../../../sdk-users/7-advanced-topics/security/security-patterns.md)

<!-- Trigger Keywords: security workflow, authentication, encryption workflow, audit trail, user auth -->
