# Examples

Essential examples for OpenObserve API integration.

## Timestamp Handling

Log entries can specify timestamps using `_timestamp` or `@timestamp` fields:
- **Format**: Unix timestamp in microseconds (int)
- **Example**: `"_timestamp": 1674789786006000`
- If not specified, OpenObserve uses the ingestion time

**Important**: Frappe datetime objects are timezone-naive. Use `frappe.utils.convert_timezone_to_utc()` before converting to Unix timestamps for accuracy:

```python
from frappe.utils import convert_timezone_to_utc, now_datetime

# Correct way to generate timestamp from Frappe datetime
dt = now_datetime()  # Naive datetime
dt_utc = convert_timezone_to_utc(dt)  # Convert to UTC
timestamp = int(dt_utc.timestamp() * 1000000)  # Unix microseconds
```

## Basic Usage

### Send Logs with Timestamp

```python
import frappe
from frappe.utils import convert_timezone_to_utc, now_datetime

# Using _timestamp field (Unix microseconds)
dt = now_datetime()
dt_utc = convert_timezone_to_utc(dt)
timestamp = int(dt_utc.timestamp() * 1000000)

result = frappe.call(
    "tweaks.tweaks.doctype.open_observe_api.open_observe_api.send_logs",
    stream="application-logs",
    logs=[{
        "message": "User login successful",
        "level": "info",
        "user": "john@example.com",
        "_timestamp": timestamp
    }]
)

# Or using @timestamp field
logs = [{
    "message": "Process completed",
    "level": "info",
    "@timestamp": int(convert_timezone_to_utc(now_datetime()).timestamp() * 1000000)
}]
```

### Search Logs

```python
result = frappe.call(
    "tweaks.tweaks.doctype.open_observe_api.open_observe_api.search_logs",
    sql="SELECT * FROM application_logs WHERE level='error'",
    start_time="2025-12-26T00:00:00Z",
    end_time="2025-12-26T23:59:59Z",
    size=100
)
```

## Integration Contexts

### Server Scripts / Business Logic

```python
from frappe.utils import convert_timezone_to_utc, now_datetime

# Send logs using safe_exec global
dt = now_datetime()
dt_utc = convert_timezone_to_utc(dt)

open_observe.send_logs(
    stream="server-logs",
    logs=[{
        "message": "Script executed",
        "user": frappe.session.user,
        "_timestamp": int(dt_utc.timestamp() * 1000000)
    }]
)

# Search logs
results = open_observe.search_logs(
    sql="SELECT * FROM server_logs WHERE level='error'",
    start_time="2025-12-26T00:00:00Z",
    end_time="2025-12-26T23:59:59Z"
)
```

### JavaScript (Client-side)

```javascript
frappe.call({
    method: 'tweaks.tweaks.doctype.open_observe_api.open_observe_api.send_logs',
    args: {
        stream: 'client-events',
        logs: [{
            message: 'Form submitted',
            level: 'info',
            user: frappe.session.user,
            _timestamp: Date.now() * 1000  // Convert milliseconds to microseconds
        }]
    }
});
```

### Document Hooks

```python
from frappe.utils import convert_timezone_to_utc, now_datetime

# In hooks.py
doc_events = {
    "Sales Order": {
        "after_save": "myapp.hooks.log_changes"
    }
}

# In myapp/hooks.py
def log_changes(doc, method):
    dt_utc = convert_timezone_to_utc(now_datetime())
    open_observe.send_logs(
        stream="audit-trail",
        logs=[{
            "doctype": doc.doctype,
            "name": doc.name,
            "action": method,
            "user": frappe.session.user,
            "_timestamp": int(dt_utc.timestamp() * 1000000)
        }]
    )
```

## Common Use Cases

### Error Logging

```python
from frappe.utils import convert_timezone_to_utc, now_datetime

try:
    process_operation()
except Exception as e:
    dt_utc = convert_timezone_to_utc(now_datetime())
    open_observe.send_logs(
        stream="errors",
        logs=[{
            "message": str(e),
            "level": "error",
            "traceback": frappe.get_traceback(),
            "_timestamp": int(dt_utc.timestamp() * 1000000)
        }]
    )
    raise
```

### Performance Monitoring

```python
import time
from frappe.utils import convert_timezone_to_utc, now_datetime

start = time.time()
process_data()
duration = time.time() - start

dt_utc = convert_timezone_to_utc(now_datetime())
open_observe.send_logs(
    stream="performance",
    logs=[{
        "operation": "process_data",
        "duration_seconds": duration,
        "_timestamp": int(dt_utc.timestamp() * 1000000)
    }]
)
```

### Audit Trail

```python
from frappe.utils import convert_timezone_to_utc, now_datetime

def log_document_change(doc, method):
    if method == "on_update" and hasattr(doc, "_doc_before_save"):
        changes = {}
        for field in doc.meta.get_valid_columns():
            old_val = getattr(doc._doc_before_save, field, None)
            new_val = getattr(doc, field, None)
            if old_val != new_val:
                changes[field] = {"old": old_val, "new": new_val}
        
        if changes:
            dt_utc = convert_timezone_to_utc(now_datetime())
            open_observe.send_logs(
                stream="audit-trail",
                logs=[{
                    "doctype": doc.doctype,
                    "name": doc.name,
                    "changes": changes,
                    "user": frappe.session.user,
                    "_timestamp": int(dt_utc.timestamp() * 1000000)
                }]
            )
```
