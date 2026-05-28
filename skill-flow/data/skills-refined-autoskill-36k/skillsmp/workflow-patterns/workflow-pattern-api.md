---
name: workflow-pattern-api
description: "API integration workflow patterns (REST, GraphQL, webhooks). Use when asking 'API workflow', 'REST integration', 'API orchestration', 'webhook', or 'API automation'."
---

# API Integration Workflow Patterns

Patterns for integrating and orchestrating APIs in workflows.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-api-reference`](../nodes/nodes-api-reference.md), [`nexus-specialist`](../../03-nexus/nexus-specialist.md)
> Related Subagents: `nexus-specialist` (API platform), `pattern-expert` (API workflows)

## Quick Reference

API patterns enable:
- **REST APIs** - GET, POST, PUT, DELETE operations
- **GraphQL** - Query and mutation execution
- **Webhooks** - Event-driven integrations
- **Authentication** - OAuth, API keys, JWT
- **Rate limiting** - Backoff and throttling
- **Error handling** - Retries and fallbacks

## Pattern 1: REST API Orchestration

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# 1. Authenticate
workflow.add_node("APICallNode", "auth", {
    "url": "https://api.example.com/auth/token",
    "method": "POST",
    "body": {
        "client_id": "{{secrets.client_id}}",
        "client_secret": "{{secrets.client_secret}}"
    }
})

# 2. Get user data
workflow.add_node("APICallNode", "get_user", {
    "url": "https://api.example.com/users/{{input.user_id}}",
    "method": "GET",
    "headers": {
        "Authorization": "Bearer {{auth.access_token}}"
    }
})

# 3. Update user profile
workflow.add_node("APICallNode", "update_profile", {
    "url": "https://api.example.com/users/{{input.user_id}}/profile",
    "method": "PUT",
    "headers": {
        "Authorization": "Bearer {{auth.access_token}}"
    },
    "body": "{{input.profile_data}}"
})

# 4. Trigger webhook
workflow.add_node("APICallNode", "notify_webhook", {
    "url": "{{input.webhook_url}}",
    "method": "POST",
    "body": {
        "event": "profile_updated",
        "user_id": "{{input.user_id}}",
        "timestamp": "{{now}}"
    }
})

workflow.add_connection("auth", "get_user")
workflow.add_connection("get_user", "update_profile")
workflow.add_connection("update_profile", "notify_webhook")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build(), inputs={
    "user_id": "12345",
    "profile_data": {"name": "John Doe"},
    "webhook_url": "https://webhook.site/..."
})
```

## Pattern 2: Parallel API Calls

```python
workflow = WorkflowBuilder()

# Fetch data from multiple APIs in parallel
workflow.add_node("APICallNode", "api_weather", {
    "url": "https://api.weather.com/current/{{input.city}}",
    "method": "GET"
})

workflow.add_node("APICallNode", "api_news", {
    "url": "https://api.news.com/headlines/{{input.city}}",
    "method": "GET"
})

workflow.add_node("APICallNode", "api_events", {
    "url": "https://api.events.com/search?location={{input.city}}",
    "method": "GET"
})

# Merge results
workflow.add_node("MergeNode", "merge_results", {
    "inputs": [
        "{{api_weather.data}}",
        "{{api_news.data}}",
        "{{api_events.data}}"
    ],
    "strategy": "combine"
})

# No connections between parallel nodes - they run simultaneously
workflow.add_connection("api_weather", "merge_results")
workflow.add_connection("api_news", "merge_results")
workflow.add_connection("api_events", "merge_results")
```

## Pattern 3: API with Retry and Backoff

```python
workflow = WorkflowBuilder()

# 1. Initialize retry state
workflow.add_node("SetVariableNode", "init_retry", {
    "retry_count": 0,
    "max_retries": 3
})

# 2. Make API call
workflow.add_node("APICallNode", "api_call", {
    "url": "https://api.example.com/operation",
    "method": "POST",
    "body": "{{input.data}}",
    "timeout": 30
})

# 3. Check response status
workflow.add_node("ConditionalNode", "check_status", {
    "condition": "{{api_call.status_code}} >= 200 AND {{api_call.status_code}} < 300",
    "true_branch": "success",
    "false_branch": "check_retry"
})

# 4. Check if should retry
workflow.add_node("ConditionalNode", "check_retry", {
    "condition": "{{init_retry.retry_count}} < {{init_retry.max_retries}}",
    "true_branch": "backoff",
    "false_branch": "failed"
})

# 5. Exponential backoff
workflow.add_node("TransformNode", "calculate_delay", {
    "input": "{{init_retry.retry_count}}",
    "transformation": "2 ** value"  # 1, 2, 4 seconds
})

workflow.add_node("DelayNode", "backoff", {
    "duration_seconds": "{{calculate_delay.result}}"
})

# 6. Increment retry counter
workflow.add_node("TransformNode", "increment", {
    "input": "{{init_retry.retry_count}}",
    "transformation": "value + 1"
})

# Loop back
workflow.add_connection("init_retry", "api_call")
workflow.add_connection("api_call", "check_status")
workflow.add_connection("check_status", "check_retry", "false")
workflow.add_connection("check_retry", "calculate_delay", "true")
workflow.add_connection("calculate_delay", "backoff")
workflow.add_connection("backoff", "increment")
workflow.add_connection("increment", "api_call")  # Retry
```

## Pattern 4: GraphQL API Integration

```python
workflow = WorkflowBuilder()

# 1. GraphQL query
workflow.add_node("APICallNode", "graphql_query", {
    "url": "https://api.example.com/graphql",
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer {{secrets.api_token}}"
    },
    "body": {
        "query": """
            query GetUser($id: ID!) {
                user(id: $id) {
                    id
                    name
                    email
                    posts {
                        id
                        title
                        createdAt
                    }
                }
            }
        """,
        "variables": {
            "id": "{{input.user_id}}"
        }
    }
})

# 2. Extract nested data
workflow.add_node("TransformNode", "extract_posts", {
    "input": "{{graphql_query.data.user.posts}}",
    "transformation": "map(lambda p: {'id': p.id, 'title': p.title})"
})

# 3. GraphQL mutation
workflow.add_node("APICallNode", "graphql_mutation", {
    "url": "https://api.example.com/graphql",
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer {{secrets.api_token}}"
    },
    "body": {
        "query": """
            mutation UpdateUser($id: ID!, $input: UserInput!) {
                updateUser(id: $id, input: $input) {
                    id
                    name
                    updatedAt
                }
            }
        """,
        "variables": {
            "id": "{{input.user_id}}",
            "input": "{{input.updates}}"
        }
    }
})

workflow.add_connection("graphql_query", "extract_posts")
workflow.add_connection("extract_posts", "graphql_mutation")
```

## Pattern 5: Webhook Receiver Workflow

```python
from kailash.api.workflow_api import WorkflowAPI

workflow = WorkflowBuilder()

# 1. Validate webhook signature
workflow.add_node("TransformNode", "validate_signature", {
    "input": "{{input.signature}}",
    "expected": "{{secrets.webhook_secret}}",
    "transformation": "hmac_sha256(input.body, expected)"
})

workflow.add_node("ConditionalNode", "check_signature", {
    "condition": "{{validate_signature.result}} == {{input.signature}}",
    "true_branch": "process",
    "false_branch": "reject"
})

# 2. Parse webhook payload
workflow.add_node("TransformNode", "parse_payload", {
    "input": "{{input.body}}",
    "transformation": "json.loads(value)"
})

# 3. Route by event type
workflow.add_node("ConditionalNode", "route_event", {
    "condition": "{{parse_payload.event_type}}",
    "branches": {
        "user.created": "create_user",
        "user.updated": "update_user",
        "user.deleted": "delete_user"
    }
})

# 4. Process each event type
workflow.add_node("DatabaseExecuteNode", "create_user", {
    "query": "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
    "parameters": "{{parse_payload.data}}"
})

workflow.add_node("DatabaseExecuteNode", "update_user", {
    "query": "UPDATE users SET name = ?, email = ? WHERE id = ?",
    "parameters": "{{parse_payload.data}}"
})

workflow.add_node("DatabaseExecuteNode", "delete_user", {
    "query": "DELETE FROM users WHERE id = ?",
    "parameters": ["{{parse_payload.data.id}}"]
})

workflow.add_connection("validate_signature", "check_signature")
workflow.add_connection("check_signature", "parse_payload", "true")
workflow.add_connection("parse_payload", "route_event")

# Deploy as API endpoint
api = WorkflowAPI(workflow.build())
api.run(port=8000)  # POST /execute receives webhooks
```

## Best Practices

1. **Authentication** - Store credentials in secrets
2. **Timeouts** - Set reasonable timeout values
3. **Retry logic** - Implement exponential backoff
4. **Rate limiting** - Respect API limits
5. **Error handling** - Graceful degradation
6. **Logging** - Track all API calls
7. **Validation** - Verify responses
8. **Parallel calls** - Use for independent APIs

## Common Pitfalls

- **No retry logic** - Transient failures kill workflows
- **Missing timeouts** - Hanging requests
- **Hard-coded credentials** - Security risks
- **No rate limiting** - API bans
- **Blocking parallel calls** - Slow execution
- **Poor error messages** - Hard to debug

## Related Skills

- **API Nodes**: [`nodes-api-reference`](../nodes/nodes-api-reference.md)
- **Nexus Platform**: [`nexus-specialist`](../../03-nexus/nexus-specialist.md)
- **Error Handling**: [`gold-error-handling`](../../17-gold-standards/gold-error-handling.md)

## Documentation

- **API Integration**: [`sdk-users/7-advanced-topics/workflows/api-integration.md`](../../../../sdk-users/7-advanced-topics/workflows/api-integration.md)
- **Nexus Guide**: [`sdk-users/apps/nexus/README.md`](../../../../sdk-users/apps/nexus/README.md)

<!-- Trigger Keywords: API workflow, REST integration, API orchestration, webhook, API automation, GraphQL -->
