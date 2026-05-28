# API Reference

Complete documentation for OpenObserve API integration functions.

## send_logs(stream, logs, org=None)

Send logs to an OpenObserve stream.

**Parameters:**
- `stream` (str, required): Stream name to send logs to
- `logs` (list, required): List of log dictionaries to send. Each log can contain:
  - Standard fields: `message`, `level`, etc.
  - **Timestamp field**: Use `_timestamp` or `@timestamp` (Unix timestamp in microseconds)
  - **Important**: Frappe datetime objects are timezone-naive. Use `frappe.utils.convert_timezone_to_utc()` before converting to Unix timestamps
  - If no timestamp field is provided, OpenObserve uses ingestion time
- `org` (str, optional): Organization name (uses default_org if not provided)

**Returns:**
```python
{
    "success": bool,
    "response": dict,  # OpenObserve API response
    "status_code": int
}
```

**Permissions:** System Manager only

**Examples:**
```python
from frappe.utils import convert_timezone_to_utc, now_datetime

# With explicit timestamp (Unix microseconds) - correct way
dt = now_datetime()
dt_utc = convert_timezone_to_utc(dt)
timestamp = int(dt_utc.timestamp() * 1000000)

result = send_logs(
    stream="application-logs",
    logs=[{
        "message": "User login successful",
        "level": "info",
        "user": "john@example.com",
        "_timestamp": timestamp
    }]
)

# Without timestamp (uses ingestion time)
result = send_logs(
    stream="error-logs",
    logs=[
        {"message": "Error occurred", "level": "error", "code": 500},
        {"message": "Retry failed", "level": "error", "code": 503}
    ],
    org="production"
)
```
)
```

## search_logs(query=None, stream=None, sql=None, org=None, start_time=None, end_time=None, start=None, size=None, search_type="ui", timeout=0)

Search logs from an OpenObserve stream.

**Parameters:**
- `query` (dict, optional): Query object that can be complete or incomplete. Missing fields will be filled from individual parameters. Can contain sql, start_time, end_time, start, size
- `stream` (str, optional): Stream name to search logs from (used to replace {stream} placeholder in sql)
- `sql` (str, optional): SQL query string for filtering logs (e.g., "SELECT * FROM stream_name WHERE level='error'"). Use {stream} placeholder which will be replaced with the actual stream name
- `org` (str, optional): Organization name (uses default_org if not provided)
- `start_time` (str/datetime/int, optional): Start time in ISO format, datetime object, or Unix timestamp in microseconds. Naive datetimes are converted to UTC
- `end_time` (str/datetime/int, optional): End time in same formats as start_time
- `start` (int, optional): Starting offset for pagination (default: 0). Maps to 'from' field in OpenObserve API
- `size` (int, optional): Maximum number of logs to return (default: 100)
- `search_type` (str, optional): Type of search, typically "ui" (default: "ui")
- `timeout` (int, optional): Query timeout in seconds (default: 0 for no timeout)

**Returns:**
```python
{
    "success": bool,
    "response": dict,  # Search results with "hits" array
    "status_code": int
}
```

**Permissions:** System Manager only

**Examples:**
```python
# Search with individual parameters (ISO strings)
result = search_logs(
    stream="application-logs",
    sql="SELECT * FROM {stream} WHERE level='error'",
    start_time="2025-12-26T05:00:00Z",
    end_time="2025-12-26T06:00:00Z",
    size=50
)

# Search with complete query object (Unix timestamps)
result = search_logs(
    query={
        "sql": "SELECT * FROM application_logs",
        "start_time": 1674789786006000,
        "end_time": 1674789886006000,
        "start": 0,
        "size": 100
    }
)

# Search with datetime objects
from datetime import datetime, timedelta
result = search_logs(
    sql="SELECT * FROM error_logs",
    start_time=datetime.now() - timedelta(hours=1),
    end_time=datetime.now()
)

# Parameter override - query provides base, parameters override
result = search_logs(
    query={"sql": "SELECT * FROM logs", "start_time": "2025-01-01T00:00:00Z"},
    end_time="2025-01-01T23:59:59Z",  # Completes missing end_time
    size=200  # Overrides default size
)
```

## test_connection()

Test connection to OpenObserve API by sending a test log entry.

**Returns:**
```python
{
    "success": bool,
    "message": str,
    "details": dict,  # If successful
    "error": str      # If failed
}
```

**Example:**
```python
result = test_connection()
if result["success"]:
    print("Connection successful!")
else:
    print(f"Connection failed: {result['error']}")
```

## Configuration Methods

### validate_setup()

Validates OpenObserve API configuration.

**Raises:** `frappe.ValidationError` if configuration is invalid (missing URL, user, or password)

**Example:**
```python
config = frappe.get_doc("Open Observe API", "Open Observe API")
config.validate_setup()  # Raises error if invalid
```

## API Endpoint Formats

**Send Logs:**
```
{url}/api/{org}/{stream}/_json
```

**Search Logs:**
```
{url}/api/{org}/{stream}/_search
```

**Example:**
```
https://api.openobserve.ai/api/default/application-logs/_json
https://api.openobserve.ai/api/default/application-logs/_search
```

## Error Handling

All API calls include:
- Configuration validation (missing fields)
- HTTP error catching and logging
- Error logging to Frappe Error Log
- User-friendly error messages
- 30-second timeout

**Example:**
```python
try:
    send_logs("my-stream", [{"message": "test"}])
except Exception as e:
    # Error is logged and user-friendly message is displayed
    print(f"Failed: {e}")
```
