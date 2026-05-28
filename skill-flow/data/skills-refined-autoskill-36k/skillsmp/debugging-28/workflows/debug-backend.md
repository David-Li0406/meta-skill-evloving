# Backend Debugging Workflow

## When to Use

- API returning errors (4xx, 5xx)
- Server crashes or hangs
- Slow response times
- Business logic producing wrong results
- Database query issues
- Authentication/authorization failures

## Step 1: Gather Symptoms

```
□ What is the exact error message/status code?
□ Which endpoint(s) are affected?
□ Is it reproducible consistently?
□ When did it start? What changed?
□ Does it happen for all users or specific ones?
□ What's in the request payload?
```

## Step 2: Check the Logs

### Log locations (varies by setup):
```bash
# Application logs
tail -f logs/app.log
journalctl -u myapp -f

# Docker logs
docker logs -f container_name

# Cloud logs
aws logs tail /aws/lambda/my-function --follow
gcloud logging tail "resource.type=cloud_run_revision"
```

### What to look for:
- Stack traces (read bottom-up for root cause)
- Error messages just before the failure
- Request IDs for correlation
- Timing information

## Step 3: Reproduce the Request

### Using curl:
```bash
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"key": "value"}' \
  -v  # verbose output
```

### Capture the exact request:
- Check browser Network tab → Copy as cURL
- Check API client/Postman history

## Step 4: Trace the Request Path

```
Request Flow:
1. Load balancer / reverse proxy
2. Web server (nginx, etc.)
3. Application framework routing
4. Middleware (auth, validation, logging)
5. Controller/handler
6. Service layer
7. Data access layer
8. Database
```

### Add tracing if missing:
```python
# Python example
import logging
logger = logging.getLogger(__name__)

def my_function(data):
    logger.debug(f"Entering my_function with: {data}")
    # ... logic ...
    logger.debug(f"Returning: {result}")
    return result
```

## Step 5: Database Debugging

If the issue involves data:

```sql
-- Check the actual data
SELECT * FROM users WHERE id = 123;

-- Check recent changes
SELECT * FROM audit_log WHERE entity_id = 123 ORDER BY created_at DESC;

-- Check query performance
EXPLAIN ANALYZE SELECT ...;
```

### Common database issues:
- Missing records
- Stale data (caching)
- Constraint violations
- Deadlocks
- N+1 queries

## Step 6: Debugger Approach

### Python (pdb):
```python
import pdb; pdb.set_trace()  # Breakpoint

# In debugger:
# n - next line
# s - step into
# c - continue
# p variable - print variable
# l - list code around current line
```

### Node.js:
```javascript
debugger;  // Breakpoint

// Run with: node --inspect app.js
// Open: chrome://inspect
```

### Remote debugging:
```bash
# Python
python -m debugpy --listen 5678 --wait-for-client app.py

# Node
node --inspect=0.0.0.0:9229 app.js
```

## Step 7: Isolate the Problem

### Binary search in code:
1. Add log/breakpoint at midpoint
2. Is the data correct at this point?
3. If yes, bug is after; if no, bug is before
4. Repeat

### Test in isolation:
```python
# Unit test the specific function
def test_calculate_discount():
    result = calculate_discount(100, "VIP")
    assert result == 80
```

## Step 8: Common Error Patterns

### 500 Internal Server Error
```
Check:
□ Unhandled exceptions in logs
□ Null pointer / undefined access
□ Database connection issues
□ Out of memory
□ Timeout exceeded
```

### 401 Unauthorized
```
Check:
□ Token expired?
□ Token format correct?
□ Token signature valid?
□ User exists and active?
```

### 403 Forbidden
```
Check:
□ User has required role/permission?
□ Resource ownership correct?
□ CORS preflight failing?
```

### 404 Not Found
```
Check:
□ Route registered correctly?
□ Resource ID exists?
□ Typo in URL?
□ HTTP method correct?
```

### 422 Validation Error
```
Check:
□ Request body format correct?
□ Required fields present?
□ Field types correct?
□ Field values in allowed range?
```

## Step 9: Performance Debugging

If the endpoint is slow:

```
□ Add timing logs around suspect code
□ Profile database queries (EXPLAIN ANALYZE)
□ Check for N+1 queries
□ Look for blocking I/O
□ Check external service latency
□ Review memory usage
```

### Profiling:
```python
# Python
import cProfile
cProfile.run('my_function()')

# Or use py-spy for production
py-spy record -o profile.svg -- python app.py
```

## Step 10: Follow TDD to duplicate & resolve the failing test.
- When bug is identified, follow TDD debugging workflow:
- See: test-driven-development/references/debugging-workflow.md
- Verify all tests pass.

## Quick Reference: HTTP Status Codes

| Code | Meaning | Likely Cause |
|------|---------|--------------|
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Auth missing/invalid |
| 403 | Forbidden | No permission |
| 404 | Not Found | Wrong URL/ID |
| 409 | Conflict | Duplicate/conflict |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many | Rate limited |
| 500 | Server Error | Unhandled exception |
| 502 | Bad Gateway | Upstream failure |
| 503 | Unavailable | Overloaded/down |
| 504 | Timeout | Slow upstream |
