---
skill: nexus-sessions
description: Unified session management across API, CLI, and MCP channels with state persistence
priority: HIGH
tags: [nexus, sessions, state, multi-channel, persistence]
---

# Nexus Session Management

Unified session management across all channels with state persistence.

## Core Concept

Sessions work seamlessly across API, CLI, and MCP channels, maintaining state throughout the workflow lifecycle.

## Basic Session Creation

```python
from nexus import Nexus

app = Nexus()

# Create session for specific channel
session_id = app.create_session(channel="api")
print(f"Session ID: {session_id}")
```

## Cross-Channel Sessions

### Start in API, Continue in CLI
```python
import requests

# Start workflow via API
response = requests.post(
    "http://localhost:8000/workflows/multi-step-process/execute",
    json={
        "inputs": {"step": 1, "data": "initial"}
    },
    headers={"X-Session-ID": "session-123"}
)

# Continue via CLI (same session)
# nexus run multi-step-process --session session-123 --step 2

# Complete via MCP (state preserved)
client.call_tool("multi-step-process", {
    "step": 3,
    "session_id": "session-123"
})
```

## Session State Persistence

```python
# Sessions persist workflow state automatically
def demonstrate_session_persistence():
    # Step 1: API request with session
    api_response = requests.post(
        "http://localhost:8000/workflows/process/execute",
        json={
            "inputs": {"user_id": "123", "action": "start"},
            "session_id": "demo-session"
        }
    )

    # Step 2: Continue with same session (state available)
    cli_result = subprocess.run([
        "nexus", "run", "process",
        "--session", "demo-session",
        "--action", "continue"
    ])

    # Step 3: Complete with full state
    final = execute_mcp_tool("process", {
        "action": "complete",
        "session_id": "demo-session"
    })

    return final
```

## Session Data Synchronization

```python
# Sync session data across channels
session_data = app.sync_session(session_id, target_channel="mcp")

print(f"Session data: {session_data}")
```

## Session Configuration

```python
app = Nexus(
    session_timeout=3600,        # 1 hour timeout
    session_backend="redis",     # Redis for distributed sessions
    session_persistence=True     # Persist to database
)
```

## Session Lifecycle

### Create Session
```python
session_id = app.create_session(
    channel="api",
    metadata={
        "user_id": "user123",
        "request_id": "req-abc",
        "created_at": time.time()
    }
)
```

### Get Session Info
```python
session_info = app.get_session(session_id)
print(f"Session: {session_info}")
```

### Update Session
```python
app.update_session(session_id, {
    "last_activity": time.time(),
    "step": 2,
    "data": {"processed": True}
})
```

### End Session
```python
app.end_session(session_id)
```

## Session Metadata

```python
# Store additional metadata with session
session_id = app.create_session(
    channel="api",
    metadata={
        "user_id": "12345",
        "organization": "acme-corp",
        "permissions": ["read", "write"],
        "context": {
            "source": "web-app",
            "version": "2.0.0"
        }
    }
)
```

## Session Security

```python
# Enable session authentication
app = Nexus(
    enable_auth=True,
    session_auth_required=True
)

# Sessions require valid authentication
session_id = app.create_session(
    channel="api",
    auth_token="bearer_token_here"
)
```

## Session Recovery

```python
# Recover sessions after restart
def recover_active_sessions():
    """Recover sessions from persistent storage"""
    active_sessions = app.session_manager.get_active_sessions()

    for session_id, session_data in active_sessions.items():
        if session_data['status'] == 'in_progress':
            # Resume workflow
            app.resume_workflow(
                workflow_name=session_data['workflow'],
                session_id=session_id,
                checkpoint=session_data['last_checkpoint']
            )
            print(f"Resumed session: {session_id}")
```

## Distributed Sessions

```python
# Use Redis for distributed sessions
from nexus import Nexus

app = Nexus(
    session_backend="redis",
    redis_url="redis://localhost:6379",
    session_prefix="nexus:sessions:"
)

# Sessions accessible across multiple Nexus instances
```

## Session Monitoring

```python
# Monitor active sessions
def monitor_sessions():
    active = app.session_manager.count_active()
    total = app.session_manager.count_total()

    print(f"Active sessions: {active}")
    print(f"Total sessions: {total}")

    # Get session statistics
    stats = app.session_manager.get_statistics()
    print(f"Avg duration: {stats['avg_duration']}s")
    print(f"Success rate: {stats['success_rate']}%")
```

## Session Cleanup

```python
# Automatic cleanup of expired sessions
app = Nexus(
    session_cleanup_interval=300,  # 5 minutes
    session_max_age=3600           # 1 hour
)

# Manual cleanup
app.session_manager.cleanup_expired()
```

## Advanced Session Patterns

### Nested Sessions
```python
# Create child sessions
parent_session = app.create_session(channel="api")

child_session = app.create_session(
    channel="api",
    parent_session=parent_session
)

# Child inherits parent context
```

### Session Groups
```python
# Group related sessions
group_id = app.session_manager.create_group("batch-processing")

session1 = app.create_session(channel="api", group=group_id)
session2 = app.create_session(channel="api", group=group_id)

# Manage group collectively
app.session_manager.end_group(group_id)
```

### Session Checkpoints
```python
# Create checkpoints for recovery
workflow_result = app.execute_workflow(
    "long-running-process",
    session_id=session_id,
    checkpoint_interval=10  # Checkpoint every 10 steps
)

# Resume from checkpoint
app.resume_from_checkpoint(
    session_id=session_id,
    checkpoint_id="checkpoint-5"
)
```

## Session Events

```python
# Listen to session events
@app.on_session_created
def on_session_created(event):
    print(f"Session created: {event.session_id}")
    print(f"Channel: {event.channel}")

@app.on_session_updated
def on_session_updated(event):
    print(f"Session updated: {event.session_id}")

@app.on_session_ended
def on_session_ended(event):
    print(f"Session ended: {event.session_id}")
    print(f"Duration: {event.duration}s")
```

## Best Practices

1. **Use Unique Session IDs** for each user/request
2. **Set Appropriate Timeouts** based on workflow duration
3. **Clean Up Expired Sessions** regularly
4. **Use Redis for Distributed Systems** with multiple Nexus instances
5. **Monitor Session Metrics** for performance insights
6. **Implement Session Recovery** for long-running workflows
7. **Secure Sessions with Authentication** in production

## Common Patterns

### Request-Scoped Sessions
```python
# Create session per request
@app.route("/process")
def process_request():
    session_id = app.create_session(
        channel="api",
        metadata={"request_id": request.id}
    )

    result = app.execute_workflow(
        "process",
        session_id=session_id,
        inputs=request.json
    )

    return result
```

### User-Scoped Sessions
```python
# Maintain session per user
user_session = app.session_manager.get_or_create(
    user_id="user123",
    ttl=3600
)
```

### Batch Processing Sessions
```python
# Process batch with grouped sessions
group_id = app.session_manager.create_group("batch-2024-01")

for item in batch_items:
    session = app.create_session(
        channel="api",
        group=group_id
    )
    process_item(item, session)

# Wait for all to complete
app.session_manager.wait_for_group(group_id)
```

## Troubleshooting

### Session Not Found
```python
# Verify session exists
if not app.session_manager.exists(session_id):
    print("Session not found or expired")
```

### Session Timeout
```python
# Extend session timeout
app.session_manager.extend_timeout(session_id, additional_seconds=600)
```

### Session Recovery Failed
```python
# Check session status
status = app.session_manager.get_status(session_id)
if status == "failed":
    # Create new session
    new_session = app.create_session(channel="api")
```

## Key Takeaways

- Sessions work across all channels (API/CLI/MCP)
- State persists throughout workflow lifecycle
- Use Redis for distributed deployments
- Set appropriate timeouts for your use case
- Monitor sessions for performance insights
- Implement recovery for long-running workflows
- Clean up expired sessions regularly

## Related Skills

- [nexus-multi-channel](#) - Multi-channel architecture
- [nexus-enterprise-features](#) - Authentication and security
- [nexus-production-deployment](#) - Production session config
- [nexus-troubleshooting](#) - Fix session issues
