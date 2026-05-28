# Troubleshooting Guide

Common issues and solutions for OpenObserve API integration.

## Configuration Issues

### Missing Required Fields

**Symptom:** `frappe.ValidationError: URL, User, and Password are required`

**Cause:** OpenObserve API DocType not properly configured

**Solution:**
```python
doc = frappe.get_doc("Open Observe API", "Open Observe API")
doc.url = "https://api.openobserve.ai"
doc.user = "admin@example.com"
doc.password = "secure_password"
doc.default_org = "default"
doc.save()
```

### Test Connection Fails

**Symptom:** Test Connection button returns error

**Possible Causes:**
1. Incorrect URL format
2. Invalid credentials
3. Network connectivity issues
4. Firewall blocking outbound requests

**Solutions:**
- Verify URL includes protocol (https://)
- Check credentials in OpenObserve dashboard
- Test network connectivity from server
- Check firewall rules for outbound HTTPS

## Permission Issues

### Permission Denied

**Symptom:** `frappe.PermissionError: Only System Managers can access this function`

**Cause:** User doesn't have System Manager role

**Solution:** Assign System Manager role to the user or use a System Manager account

## API Call Failures

### Timeout Errors

**Symptom:** Request times out after 30 seconds

**Causes:**
- Network latency
- OpenObserve server overloaded
- Large batch of logs

**Solutions:**
- Reduce batch size (send logs in smaller chunks)
- Check network connectivity
- Verify OpenObserve service status

### Authentication Failed

**Symptom:** `401 Unauthorized` response

**Causes:**
- Incorrect credentials
- Password changed in OpenObserve
- User account disabled

**Solutions:**
```python
# Update credentials
doc = frappe.get_doc("Open Observe API", "Open Observe API")
doc.user = "correct_username"
doc.password = "correct_password"
doc.save()

# Test connection
result = doc.test_connection()
```

### Stream Not Found

**Symptom:** `404 Not Found` response

**Cause:** Stream doesn't exist in OpenObserve

**Solution:** Stream is automatically created on first log send. Verify organization name is correct.

## Log Format Issues

### Logs Not Appearing

**Symptoms:**
- API returns success but logs don't appear
- Empty search results

**Possible Causes:**
1. Wrong stream name
2. Wrong organization
3. Time range doesn't match log timestamps

**Solutions:**
```python
# Verify stream and organization
result = send_logs(
    stream="correct-stream-name",
    logs=[{
        "message": "Test log",
        "timestamp": frappe.utils.now()  # Use current time
    }],
    org="correct-org-name"
)

# Check for errors in response
if not result["success"]:
    print(result.get("error"))
```

### Timestamp Issues

**Symptom:** Logs appear at wrong time in OpenObserve

**Cause:** Incorrect timestamp format or missing timestamp

**Solution:**
```python
# Always include timestamp in ISO format
from datetime import datetime

logs = [{
    "message": "My log",
    "timestamp": datetime.utcnow().isoformat() + "Z"
}]

# Or use Frappe utility
logs = [{
    "message": "My log",
    "timestamp": frappe.utils.now()
}]
```

## Search Issues

### No Results Found

**Symptoms:**
- Search returns empty results
- Expected logs not appearing

**Possible Causes:**
1. Time range too narrow
2. Stream name incorrect
3. Organization mismatch
4. Query syntax error

**Solutions:**
```python
# Widen time range
from datetime import datetime, timedelta

end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=24)  # Last 24 hours

result = search_logs(
    stream="application-logs",
    start_time=start_time.isoformat() + "Z",
    end_time=end_time.isoformat() + "Z",
    size=100
)

# Verify results
if result["success"]:
    hits = result["response"].get("hits", [])
    print(f"Found {len(hits)} logs")
```

### Query Syntax Errors

**Symptom:** Search fails with query parsing error

**Cause:** Invalid SQL or JSON query syntax

**Solutions:**
```python
# Simple search without query
result = search_logs(
    stream="application-logs",
    start_time="2025-12-26T00:00:00Z",
    end_time="2025-12-26T23:59:59Z"
)

# Valid SQL query
result = search_logs(
    stream="application-logs",
    query={"sql": "SELECT * FROM logs WHERE level = 'error'"}
)

# Valid JSON query
result = search_logs(
    stream="application-logs",
    query={
        "query": {
            "term": {"level": "error"}
        }
    }
)
```

## Performance Issues

### Slow Log Sending

**Symptoms:**
- Takes long time to send logs
- Application feels sluggish

**Causes:**
- Sending too many individual requests
- Large log payloads

**Solutions:**
```python
# Batch logs together
logs_to_send = []

for item in items:
    logs_to_send.append({
        "message": f"Processing {item}",
        "item": item,
        "timestamp": frappe.utils.now()
    })

# Send in batch
result = send_logs(
    stream="batch-logs",
    logs=logs_to_send
)

# For very large batches, chunk them
def send_logs_in_chunks(stream, logs, chunk_size=100):
    for i in range(0, len(logs), chunk_size):
        chunk = logs[i:i+chunk_size]
        send_logs(stream, chunk)
```

### Memory Issues with Search

**Symptom:** Out of memory errors with large search results

**Cause:** Retrieving too many logs at once

**Solution:**
```python
# Limit result size
result = search_logs(
    stream="application-logs",
    start_time="2025-12-26T00:00:00Z",
    end_time="2025-12-26T23:59:59Z",
    size=50  # Smaller batch
)

# Paginate if needed (not built-in, manual implementation)
def search_logs_paginated(stream, start_time, end_time, page_size=50):
    all_results = []
    offset = 0
    
    while True:
        result = search_logs(
            stream=stream,
            start_time=start_time,
            end_time=end_time,
            size=page_size
        )
        
        if not result["success"]:
            break
            
        hits = result["response"].get("hits", [])
        if not hits:
            break
            
        all_results.extend(hits)
        offset += page_size
        
        if len(hits) < page_size:
            break
    
    return all_results
```

## Debugging Tips

### Enable Verbose Logging

```python
# Check Frappe Error Log for detailed errors
frappe.get_all("Error Log", 
    filters={"error": ["like", "%OpenObserve%"]},
    fields=["name", "error", "creation"],
    order_by="creation desc"
)
```

### Test with Simple Example

```python
# Minimal test case
result = send_logs(
    stream="test-stream",
    logs=[{"message": "test", "timestamp": frappe.utils.now()}]
)

print(f"Success: {result.get('success')}")
print(f"Status: {result.get('status_code')}")
print(f"Response: {result.get('response')}")
```

### Verify Configuration

```python
# Check current configuration
config = frappe.get_doc("Open Observe API", "Open Observe API")
print(f"URL: {config.url}")
print(f"User: {config.user}")
print(f"Default Org: {config.default_org}")

# Password won't be displayed (encrypted)
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `URL, User, and Password are required` | Missing configuration | Complete OpenObserve API setup |
| `Only System Managers can access` | Permission denied | Assign System Manager role |
| `401 Unauthorized` | Invalid credentials | Update username/password |
| `404 Not Found` | Stream/org doesn't exist | Verify stream and org names |
| `Timeout` | Network/performance issue | Reduce batch size, check network |
| `Connection refused` | Can't reach OpenObserve | Check URL, firewall, network |

## Getting Help

If issues persist:

1. Check OpenObserve API documentation: https://openobserve.ai/docs/api/
2. Review Frappe Error Log for detailed error messages
3. Test connection with `test_connection()` method
4. Verify OpenObserve service is operational
5. Check OpenObserve server logs for request details
