# Google Cloud Logging Reference

## Cloud Logging Filter Syntax

Cloud Logging uses a specialized filter syntax for querying logs. This reference covers the most common patterns.

### Basic Syntax

Filters consist of expressions connected by `AND`, `OR`, and `NOT`:

```
expression [AND|OR] expression ...
```

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `severity=ERROR` |
| `!=` | Not equals | `severity!=DEBUG` |
| `>` | Greater than | `severity>WARNING` |
| `>=` | Greater or equal | `severity>=ERROR` |
| `<` | Less than | `httpRequest.status<500` |
| `<=` | Less or equal | `httpRequest.latency<=1s` |
| `=~` | Regex match | `textPayload=~"error.*timeout"` |
| `!~` | Regex not match | `textPayload!~"expected"` |
| `:` | Contains (substring) | `textPayload:"connection failed"` |

### Resource Types

Cloud Functions logs use specific resource types:

```bash
# Gen 1 Cloud Functions
resource.type="cloud_function"

# Gen 2 Cloud Functions (Cloud Run based)
resource.type="cloud_run_revision"

# All Cloud Functions
resource.type="cloud_function" OR resource.type="cloud_run_revision"
```

### Severity Levels

Severity levels from lowest to highest:

| Level | Description |
|-------|-------------|
| `DEFAULT` | Default/unspecified |
| `DEBUG` | Debug information |
| `INFO` | Informational messages |
| `NOTICE` | Normal but significant events |
| `WARNING` | Warning events |
| `ERROR` | Error events |
| `CRITICAL` | Critical events |
| `ALERT` | Action must be taken immediately |
| `EMERGENCY` | System is unusable |

```bash
# Single severity
severity=ERROR

# Severity and above
severity>=ERROR

# Multiple severities
severity=ERROR OR severity=CRITICAL
```

### Time Filters

```bash
# Logs from last hour
timestamp>="2024-01-15T10:00:00Z"

# Logs between times
timestamp>="2024-01-15T00:00:00Z" AND timestamp<"2024-01-16T00:00:00Z"

# Using duration (requires gcloud CLI)
# --freshness=1h (last hour)
# --freshness=24h (last 24 hours)
```

### Resource Labels

Filter by Cloud Function properties:

```bash
# Specific function name
resource.labels.function_name="myFunction"

# Specific region
resource.labels.region="us-central1"

# Specific project (usually implicit)
resource.labels.project_id="my-project"
```

### Text Matching

```bash
# Exact substring match
textPayload:"error"

# Case-insensitive substring
textPayload=~"(?i)error"

# Regex pattern
textPayload=~"timeout after [0-9]+ seconds"

# Multiple terms (AND)
textPayload:"connection" AND textPayload:"refused"

# Exclude pattern
NOT textPayload:"expected error"
```

### JSON Payload Fields

For structured logs (jsonPayload):

```bash
# Field exists
jsonPayload.error:*

# Field value
jsonPayload.level="error"

# Nested field
jsonPayload.request.method="POST"

# Numeric comparison
jsonPayload.statusCode>=500
```

### HTTP Request Fields

For HTTP-triggered functions:

```bash
# Status code
httpRequest.status>=500

# Request method
httpRequest.requestMethod="POST"

# URL path
httpRequest.requestUrl:"/api/users"

# Latency
httpRequest.latency>"5s"

# User agent
httpRequest.userAgent:"Mozilla"
```

### Complex Filter Examples

```bash
# All errors for a specific function in the last hour
resource.type="cloud_function"
AND resource.labels.function_name="processPayment"
AND severity>=ERROR
AND timestamp>="2024-01-15T10:00:00Z"

# Timeout errors
resource.type="cloud_function"
AND (textPayload:"timeout" OR textPayload:"deadline exceeded")
AND severity>=ERROR

# HTTP 5xx errors
resource.type="cloud_function"
AND httpRequest.status>=500

# Memory issues
resource.type="cloud_function"
AND (textPayload:"memory" OR textPayload:"OOM" OR textPayload:"killed")

# Exclude noisy logs
resource.type="cloud_function"
AND severity>=ERROR
NOT textPayload:"health check"
NOT textPayload:"scheduled task completed"
```

---

## gcloud CLI Commands

### Basic Log Reading

```bash
# Read logs (default: last 24h, 1000 entries)
gcloud logging read "FILTER"

# With project
gcloud logging read "FILTER" --project=PROJECT_ID

# Limit results
gcloud logging read "FILTER" --limit=100

# Freshness (time range)
gcloud logging read "FILTER" --freshness=1h

# Output format
gcloud logging read "FILTER" --format=json
gcloud logging read "FILTER" --format="table(timestamp,severity,textPayload)"
```

### Useful Commands

```bash
# List available log names
gcloud logging logs list --project=PROJECT_ID

# List Cloud Functions
gcloud functions list --project=PROJECT_ID

# Describe a function
gcloud functions describe FUNCTION_NAME --project=PROJECT_ID

# View function logs directly
gcloud functions logs read FUNCTION_NAME --project=PROJECT_ID --limit=50
```

### Authentication

```bash
# Check current auth
gcloud auth list

# Login interactively
gcloud auth login

# Use service account
gcloud auth activate-service-account --key-file=KEY.json

# Application default credentials
gcloud auth application-default login
```

### Project Configuration

```bash
# List projects
gcloud projects list

# Set default project
gcloud config set project PROJECT_ID

# Get current project
gcloud config get-value project
```

---

## Log Entry Structure

### Standard Fields

| Field | Description |
|-------|-------------|
| `logName` | Full resource name of the log |
| `resource` | Monitored resource that produced the log |
| `timestamp` | Time the event occurred |
| `receiveTimestamp` | Time the log was received |
| `severity` | Log severity level |
| `insertId` | Unique identifier for the log entry |
| `labels` | User-defined labels |
| `trace` | Trace ID for distributed tracing |
| `spanId` | Span ID within the trace |

### Payload Types

Logs can have one of three payload types:

```json
// Text payload (unstructured)
{
  "textPayload": "Error: Connection refused"
}

// JSON payload (structured)
{
  "jsonPayload": {
    "message": "Request failed",
    "error": "Connection refused",
    "statusCode": 500
  }
}

// Proto payload (GCP service logs)
{
  "protoPayload": {
    "@type": "type.googleapis.com/...",
    "status": { "code": 7, "message": "..." }
  }
}
```

### Cloud Function Resource Labels

```json
{
  "resource": {
    "type": "cloud_function",
    "labels": {
      "function_name": "myFunction",
      "project_id": "my-project",
      "region": "us-central1"
    }
  }
}
```

---

## Error Categories Reference

### HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 400 | Bad Request | Invalid input, malformed JSON |
| 401 | Unauthorized | Missing/invalid auth token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 408 | Request Timeout | Client timeout |
| 429 | Too Many Requests | Rate limiting |
| 500 | Internal Server Error | Unhandled exception |
| 502 | Bad Gateway | Upstream service error |
| 503 | Service Unavailable | Service overloaded |
| 504 | Gateway Timeout | Upstream timeout |

### GCP-Specific Error Codes

| Error | Description |
|-------|-------------|
| `DEADLINE_EXCEEDED` | Operation took too long |
| `RESOURCE_EXHAUSTED` | Quota or resource limit reached |
| `PERMISSION_DENIED` | IAM permission missing |
| `UNAUTHENTICATED` | Auth credentials missing/invalid |
| `NOT_FOUND` | Resource doesn't exist |
| `ALREADY_EXISTS` | Resource already exists |
| `INVALID_ARGUMENT` | Invalid parameter |
| `FAILED_PRECONDITION` | Operation prerequisites not met |
| `INTERNAL` | Internal service error |
| `UNAVAILABLE` | Service temporarily unavailable |

---

## Best Practices

### Structured Logging

Use structured logging for better querying:

```javascript
// Node.js
console.log(JSON.stringify({
  severity: 'ERROR',
  message: 'Request failed',
  error: error.message,
  stack: error.stack,
  requestId: req.id,
  userId: user.id
}));
```

```python
# Python
import json
print(json.dumps({
    'severity': 'ERROR',
    'message': 'Request failed',
    'error': str(e),
    'request_id': request_id
}))
```

### Log Correlation

Include trace context for distributed tracing:

```javascript
const traceHeader = req.get('X-Cloud-Trace-Context');
console.log(JSON.stringify({
  message: 'Processing request',
  'logging.googleapis.com/trace': `projects/${projectId}/traces/${traceId}`
}));
```

### Efficient Queries

- Use specific time ranges to reduce data scanned
- Filter by resource type first
- Use `--limit` to avoid fetching too many logs
- Prefer equality (`=`) over substring (`:`) when possible
- Index frequently queried fields with log-based metrics

---

## Troubleshooting

### No Logs Found

1. Verify project ID is correct
2. Check time range (logs might be older)
3. Verify function name spelling
4. Check if function has been invoked
5. Verify logs are not being filtered/excluded

### Permission Denied

Required IAM roles:
- `roles/logging.viewer` - Read logs
- `roles/logging.admin` - Full logging access

```bash
# Grant viewer role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:email@example.com" \
  --role="roles/logging.viewer"
```

### Rate Limiting

Cloud Logging API has rate limits:
- 60 requests per minute per project
- Use pagination for large result sets
- Implement exponential backoff for retries

### Large Result Sets

```bash
# Use pagination
gcloud logging read "FILTER" --limit=1000 --format=json > page1.json
# Then use pageToken from response for next page
```
