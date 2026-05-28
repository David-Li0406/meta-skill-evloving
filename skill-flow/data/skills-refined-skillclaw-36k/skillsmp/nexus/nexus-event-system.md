---
skill: nexus-event-system
description: Event system for workflow lifecycle, cross-channel broadcasting, and custom events
priority: LOW
tags: [nexus, events, broadcasting, lifecycle, hooks]
---

# Nexus Event System

Event-driven architecture for workflow lifecycle and cross-channel communication.

## ⚠️ IMPORTANT: v1.0 vs v1.1 Capabilities

**v1.0 (Current - v1.1.0):**
- ✅ Events are **logged** to `_event_log` (not broadcast in real-time)
- ✅ Retrieve events with `app.get_events()` helper method
- ✅ Event decorators work but only trigger logging
- ⏳ Real-time broadcasting **planned for v1.1**

**v1.1 (Planned):**
- 🔜 Real-time WebSocket broadcasting
- 🔜 SSE (Server-Sent Events) streaming
- 🔜 MCP notifications for AI agents
- 🔜 Cross-channel event synchronization

**Current Behavior:**
```python
# v1.0: Events are logged, not broadcast
app.broadcast_event("CUSTOM_EVENT", {"data": "value"})
# Logs: "Event logged (broadcast in v1.1): CUSTOM_EVENT"

# Retrieve events manually
events = app.get_events(event_type="CUSTOM_EVENT")
```

## Built-in Events

### Workflow Lifecycle Events

```python
from nexus import Nexus

app = Nexus()

@app.on_workflow_started
def on_workflow_start(event):
    print(f"Workflow started: {event.workflow_name}")
    print(f"Channel: {event.channel}")
    print(f"Session: {event.session_id}")
    print(f"Inputs: {event.inputs}")

@app.on_workflow_completed
def on_workflow_complete(event):
    print(f"Workflow completed: {event.workflow_name}")
    print(f"Duration: {event.duration}s")
    print(f"Result: {event.result}")

@app.on_workflow_failed
def on_workflow_fail(event):
    print(f"Workflow failed: {event.workflow_name}")
    print(f"Error: {event.error}")
    print(f"Stack trace: {event.traceback}")
```

### Session Events

```python
@app.on_session_created
def on_session_created(event):
    print(f"Session created: {event.session_id}")
    print(f"Channel: {event.channel}")
    print(f"User: {event.user_id}")

@app.on_session_updated
def on_session_updated(event):
    print(f"Session updated: {event.session_id}")
    print(f"Changes: {event.changes}")

@app.on_session_ended
def on_session_ended(event):
    print(f"Session ended: {event.session_id}")
    print(f"Duration: {event.duration}s")
    print(f"Workflows executed: {event.workflow_count}")
```

### Registration Events

```python
@app.on_workflow_registered
def on_registered(event):
    print(f"Workflow registered: {event.workflow_name}")
    print(f"Metadata: {event.metadata}")

@app.on_workflow_unregistered
def on_unregistered(event):
    print(f"Workflow unregistered: {event.workflow_name}")
```

## Cross-Channel Broadcasting

### Broadcast to All Channels (v1.0 - Logged Only)

```python
# v1.0: Event is logged (NOT broadcast in real-time)
app.broadcast_event("CUSTOM_EVENT", {
    "type": "notification",
    "message": "Important update",
    "timestamp": time.time()
})

# v1.0 Reality: Event logged to app._event_log
# Retrieve later with: app.get_events(event_type="CUSTOM_EVENT")

# v1.1 (Planned): Real-time broadcasting to:
# - API: WebSocket push
# - CLI: Terminal notification
# - MCP: Event notification
```

**How to Retrieve Events in v1.0:**
```python
# Get all events
all_events = app.get_events()

# Filter by type
custom_events = app.get_events(event_type="CUSTOM_EVENT")

# Filter by session
session_events = app.get_events(session_id="session-123")
```

### Real-Time Updates (v1.0 - Polling Required)

```python
workflow = WorkflowBuilder()

workflow.add_node("PythonCodeNode", "long_process", {
    "code": """
import time

for i in range(10):
    # v1.0: Logs progress event (not real-time broadcast)
    app.broadcast_event('PROGRESS_UPDATE', {
        'percentage': (i + 1) * 10,
        'step': f'Processing step {i+1}/10',
        'timestamp': time.time()
    })
    time.sleep(1)

result = {'completed': True, 'steps': 10}
"""
})

app.register("monitored-process", workflow.build())

# v1.0: Poll for progress updates
while True:
    events = app.get_events(event_type='PROGRESS_UPDATE')
    latest = events[-1] if events else None
    if latest and latest['data']['percentage'] == 100:
        break
    time.sleep(1)

# v1.1 (Planned): Real-time WebSocket streaming
# Client subscribes and receives events as they happen
```

## Custom Events

### Define Custom Events

```python
# Define custom event types
app.register_event_type("DATA_PROCESSED", {
    "description": "Data processing completed",
    "schema": {
        "records_processed": "integer",
        "duration": "float",
        "errors": "array"
    }
})

# Emit custom event
app.emit_event("DATA_PROCESSED", {
    "records_processed": 1000,
    "duration": 5.2,
    "errors": []
})

# Listen for custom event
@app.on_event("DATA_PROCESSED")
def handle_data_processed(event):
    print(f"Processed {event.data['records_processed']} records")
```

## Event Handlers

### Multiple Handlers

```python
# Multiple handlers for same event
@app.on_workflow_completed
def log_completion(event):
    logger.info(f"Workflow completed: {event.workflow_name}")

@app.on_workflow_completed
def notify_completion(event):
    send_notification(f"Workflow {event.workflow_name} completed")

@app.on_workflow_completed
def update_metrics(event):
    metrics.record("workflow_completion", event.duration)
```

### Async Handlers

```python
@app.on_workflow_started
async def async_handler(event):
    # Async operations
    await send_webhook(event)
    await update_database(event)
```

### Conditional Handlers

```python
@app.on_workflow_completed
def handle_if_long_running(event):
    if event.duration > 60:  # Only if > 1 minute
        print(f"Long-running workflow: {event.workflow_name} took {event.duration}s")
```

## Event Filtering

```python
# Filter events by channel
@app.on_workflow_started(channel="api")
def handle_api_workflows(event):
    print(f"API workflow started: {event.workflow_name}")

@app.on_workflow_started(channel="mcp")
def handle_mcp_workflows(event):
    print(f"MCP workflow started: {event.workflow_name}")

# Filter by workflow name
@app.on_workflow_completed(workflow="critical-workflow")
def handle_critical_completion(event):
    print(f"Critical workflow completed")
```

## Event Context

### Event Object Structure

```python
class WorkflowEvent:
    workflow_name: str
    workflow_id: str
    session_id: str
    channel: str
    timestamp: float
    user_id: Optional[str]
    inputs: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    duration: Optional[float]
    metadata: Dict[str, Any]
```

### Access Event Context

```python
@app.on_workflow_started
def handle_start(event):
    # Access event properties
    print(f"Workflow: {event.workflow_name}")
    print(f"User: {event.user_id}")
    print(f"Channel: {event.channel}")
    print(f"Time: {event.timestamp}")

    # Access custom metadata
    if "request_id" in event.metadata:
        print(f"Request ID: {event.metadata['request_id']}")
```

## Error Handling in Events

```python
@app.on_workflow_failed
def handle_workflow_error(event):
    error_data = {
        "workflow": event.workflow_name,
        "error": event.error,
        "user": event.user_id,
        "timestamp": event.timestamp
    }

    # Log error
    logger.error(f"Workflow error: {error_data}")

    # Send alert
    send_alert("workflow_failure", error_data)

    # Update metrics
    metrics.increment("workflow_errors", labels={
        "workflow": event.workflow_name
    })
```

## Integration Examples

### Slack Notifications

```python
import requests

@app.on_workflow_completed
def notify_slack(event):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    message = {
        "text": f"Workflow {event.workflow_name} completed",
        "attachments": [{
            "fields": [
                {"title": "Duration", "value": f"{event.duration:.2f}s"},
                {"title": "Channel", "value": event.channel},
                {"title": "Status", "value": "Success"}
            ]
        }]
    }

    requests.post(webhook_url, json=message)
```

### Email Notifications

```python
import smtplib
from email.mime.text import MIMEText

@app.on_workflow_failed
def email_on_failure(event):
    msg = MIMEText(f"""
    Workflow: {event.workflow_name}
    Error: {event.error}
    Time: {event.timestamp}
    User: {event.user_id}
    """)

    msg['Subject'] = f"Workflow Failure: {event.workflow_name}"
    msg['From'] = "nexus@example.com"
    msg['To'] = "admin@example.com"

    smtp = smtplib.SMTP('localhost')
    smtp.send_message(msg)
    smtp.quit()
```

### Database Logging

```python
@app.on_workflow_started
def log_to_database(event):
    db.execute("""
        INSERT INTO workflow_logs (
            workflow_name, workflow_id, session_id,
            channel, user_id, timestamp, inputs
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event.workflow_name,
        event.workflow_id,
        event.session_id,
        event.channel,
        event.user_id,
        event.timestamp,
        json.dumps(event.inputs)
    ))

@app.on_workflow_completed
def update_database(event):
    db.execute("""
        UPDATE workflow_logs
        SET status = 'completed',
            duration = ?,
            result = ?
        WHERE workflow_id = ?
    """, (
        event.duration,
        json.dumps(event.result),
        event.workflow_id
    ))
```

## Event Routing

```python
class EventRouter:
    def __init__(self):
        self.handlers = {}

    def register(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def route(self, event_type, event):
        handlers = self.handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Handler error: {e}")

# Usage
router = EventRouter()
router.register("workflow_completed", log_completion)
router.register("workflow_completed", notify_completion)
router.route("workflow_completed", event)
```

## Best Practices (v1.1.0)

1. **Understand v1.0 Limitations** - Events are logged, not broadcast in real-time
2. **Use `get_events()` for Retrieval** - Poll for events when needed
3. **Keep Event Data Small** - Large payloads stored in `_event_log`
4. **Filter Events Efficiently** - Use `event_type` and `session_id` parameters
5. **Plan for v1.1 Migration** - Design with real-time broadcasting in mind
6. **Use Event Decorators** - They work but only trigger logging in v1.0

**v1.0 Workarounds:**
```python
# Instead of real-time broadcast, use polling
def poll_events(app, event_type, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        events = app.get_events(event_type=event_type)
        if events:
            return events[-1]
        time.sleep(0.5)
    return None
```

## Key Takeaways (v1.1.0)

**v1.0 Reality (Current):**
- ✅ Events are **logged** to `_event_log`, not broadcast in real-time
- ✅ Retrieve events with `app.get_events(event_type, session_id)`
- ✅ Event decorators work but only trigger logging
- ✅ Custom events supported via `broadcast_event()`
- ❌ Real-time broadcasting NOT available (planned for v1.1)

**v1.1 Planned:**
- 🔜 Real-time WebSocket broadcasting
- 🔜 SSE streaming for browser clients
- 🔜 MCP notifications for AI agents
- 🔜 Cross-channel event synchronization

**Current Usage Pattern:**
```python
# Log event
app.broadcast_event("EVENT_TYPE", {"data": "value"})

# Retrieve later
events = app.get_events(event_type="EVENT_TYPE")
```

## Related Skills

- [nexus-multi-channel](#) - Multi-channel architecture
- [nexus-sessions](#) - Session management
- [nexus-health-monitoring](#) - Monitoring events
