---
name: open-observe-api-expert
description: Expert guidance for OpenObserve API integration in Frappe Tweaks. Use when creating, configuring, or troubleshooting OpenObserve API DocType, implementing send_logs() or search_logs() functionality, integrating with Server Scripts/Business Logic/Client-side code, debugging connection issues, or implementing logging, monitoring, error tracking, performance metrics, or audit trail use cases.
---

# OpenObserve API Expert

Expert guidance for the OpenObserve API integration - a logging and observability integration for Frappe applications.

## Quick Start

**Configuration**: Single DocType "Open Observe API" with URL, user, password, default organization  
**Core Functions**: `send_logs()`, `search_logs()`, `test_connection()`  
**Access**: System Manager only  
**Safe Exec**: Available as `open_observe.send_logs()` and `open_observe.search_logs()`

## Core Concepts

**OpenObserve**: Open-source observability platform for logs, metrics, and traces  
**Stream**: Named channel for organizing logs (e.g., "application-logs", "error-logs")  
**Organization**: Namespace for separating environments (defaults to configured default_org)  
**Safe Exec Global**: Access API from Server Scripts/Business Logic without importing  
**Timestamps**: Use `_timestamp` or `@timestamp` fields (Unix microseconds). Frappe datetimes are timezone-naive—use `frappe.utils.convert_timezone_to_utc()` for accurate timestamps

## Common Tasks

### Configuration Setup

```python
doc = frappe.get_doc("Open Observe API", "Open Observe API")
doc.url = "https://api.openobserve.ai"
doc.user = "admin@example.com"
doc.password = "secure_password"
doc.default_org = "default"
doc.save()
```

### Send Logs

**From Python**:
```python
frappe.call(
    "tweaks.tweaks.doctype.open_observe_api.open_observe_api.send_logs",
    stream="application-logs",
    logs=[{"message": "Event occurred", "level": "info"}]
)
```

**From Server Scripts/Business Logic**:
```python
open_observe.send_logs(
    stream="server-logs",
    logs=[{"message": "Script executed", "user": frappe.session.user}]
)
```

### Search Logs

```python
results = open_observe.search_logs(
    sql="SELECT * FROM application_logs",
    start_time="2025-12-26T00:00:00Z",
    end_time="2025-12-26T23:59:59Z",
    size=100
)
```

## Key Features

**Batch Logging**: Send multiple logs in single request  
**Time-based Search**: ISO format timestamps auto-converted to Unix microseconds  
**Query Support**: SQL queries and JSON filters for advanced search  
**Dry Run**: Test without actually sending to OpenObserve  
**Secure Storage**: Password encrypted using Frappe's password field

## Detailed Documentation

**API Functions**: See [references/api-reference.md](references/api-reference.md) for complete parameter documentation  
**Examples**: See [references/examples.md](references/examples.md) for comprehensive usage examples across different contexts and use cases  
**Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md) for common issues and solutions

## Best Practices

1. Use descriptive stream names (hierarchical: `app-errors`, `user-activity`)
2. Include timestamps in all log entries
3. Add context (user, doctype, action) to logs
4. Batch multiple logs in single request for efficiency
5. Handle logging failures gracefully (don't break application)
6. Use appropriate log levels (info, warning, error, debug)
7. Leverage search for analytics and pattern analysis

## Security

- System Manager permission required
- Password stored with Frappe encryption
- HTTP Basic Auth with base64 encoding
- 30-second timeout prevents hanging
- Errors logged to Frappe Error Log
