# Log Patterns

Common error patterns and how to identify them.

## Error Pattern Categories

### 1. Null/Undefined Errors

```javascript
// JavaScript/TypeScript
TypeError: Cannot read property 'x' of undefined
TypeError: Cannot read property 'x' of null
TypeError: x is not a function

// Python
AttributeError: 'NoneType' object has no attribute 'x'
TypeError: 'NoneType' object is not subscriptable
```

**Common Causes:**
- Missing null checks
- API response changes
- Race conditions
- Uninitialized variables

**Investigation:**
```bash
# Find where variable is used
grep -rn "variable\." src/

# Check API response handling
grep -rn "response\." src/ | grep -v "\.status"
```

### 2. Connection Errors

```
Error: ECONNREFUSED 127.0.0.1:5432
Error: ETIMEDOUT
Error: ENOTFOUND hostname
Error: Connection reset by peer
```

**Common Causes:**
- Service not running
- Wrong host/port
- Firewall blocking
- DNS issues
- Connection pool exhausted

**Investigation:**
```bash
# Check if service is running
netstat -tlnp | grep 5432

# Test connectivity
nc -zv hostname port

# Check DNS
nslookup hostname
```

### 3. Authentication Errors

```
Error: 401 Unauthorized
Error: JWT expired
Error: Invalid signature
Error: Token not found
```

**Common Causes:**
- Expired credentials
- Wrong credentials
- Missing token
- Clock skew
- Key rotation issues

**Investigation:**
```bash
# Check token expiration
echo $TOKEN | cut -d. -f2 | base64 -d | jq .exp

# Verify system time
date -u

# Check credential config
grep -rn "API_KEY\|SECRET" .env
```

### 4. Rate Limiting

```
Error: 429 Too Many Requests
Error: Rate limit exceeded
Error: Quota exceeded
```

**Common Causes:**
- No rate limiting on client
- Burst traffic
- Missing backoff logic
- Shared API key across services

**Investigation:**
```bash
# Check request rate
grep "api.example.com" access.log | wc -l

# Find rate limit headers
grep "X-RateLimit\|Retry-After" response.log
```

### 5. Memory Errors

```
Error: JavaScript heap out of memory
FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed
Error: Cannot allocate memory
OOM killed
```

**Common Causes:**
- Memory leaks
- Large data in memory
- No pagination
- Missing stream processing

**Investigation:**
```bash
# Monitor memory
node --max-old-space-size=4096 app.js

# Find memory usage
ps aux | grep node

# Profile memory
node --inspect app.js
```

### 6. Timeout Errors

```
Error: ETIMEDOUT
Error: Operation timed out after 30000ms
Error: Request timeout
Error: Gateway Timeout (504)
```

**Common Causes:**
- Slow queries
- Network latency
- Large payloads
- Downstream service issues

**Investigation:**
```bash
# Check query times
grep "slow query" database.log

# Monitor response times
grep "duration" access.log | sort -t= -k2 -rn | head
```

## Log Level Patterns

### INFO Level
```
2024-01-15 14:30:00 INFO  User login successful user_id=123
2024-01-15 14:30:01 INFO  Order created order_id=456
```
Normal operations, audit trail.

### WARN Level
```
2024-01-15 14:30:00 WARN  Retry attempt 2/3 for API call
2024-01-15 14:30:01 WARN  Deprecated method called: oldMethod
2024-01-15 14:30:02 WARN  Response time exceeded threshold: 2.5s
```
Potential issues, degraded performance.

### ERROR Level
```
2024-01-15 14:30:00 ERROR Failed to process payment error="Card declined"
2024-01-15 14:30:01 ERROR Database query failed error="Connection refused"
```
Failures requiring attention.

### FATAL Level
```
2024-01-15 14:30:00 FATAL Cannot start server: Port 3000 in use
2024-01-15 14:30:01 FATAL Database migration failed
```
System cannot continue.

## Pattern Recognition

### Spike Detection

```bash
# Errors per minute
grep "ERROR" app.log | cut -d' ' -f1-2 | cut -d: -f1-2 | uniq -c

# Visualize (if graphing available)
grep "ERROR" app.log | cut -d' ' -f1-2 | cut -d: -f1-2 | uniq -c | \
  awk '{print $2, $1}' | gnuplot -e "plot '-' with lines"
```

### Correlation Patterns

```bash
# Errors followed by specific events
grep -A5 "ERROR" app.log | grep "retry\|fallback\|recovery"

# Errors preceded by warnings
grep -B5 "ERROR" app.log | grep "WARN"
```

### Repeating Errors

```bash
# Most common errors
grep "ERROR" app.log | sed 's/[0-9]//g' | sort | uniq -c | sort -rn | head -20

# Errors from same source
grep "ERROR" app.log | grep -oP 'at \K[^(]+' | sort | uniq -c | sort -rn
```

## Structured Log Analysis

### JSON Logs

```bash
# Parse JSON logs
cat app.log | jq 'select(.level == "error")'

# Group by error type
cat app.log | jq -r 'select(.level == "error") | .error_type' | sort | uniq -c

# Find errors for specific user
cat app.log | jq 'select(.user_id == "123" and .level == "error")'
```

### Key-Value Logs

```bash
# Extract specific fields
grep "ERROR" app.log | grep -oP 'user_id=\K[^ ]+'

# Aggregate by field
grep "ERROR" app.log | grep -oP 'error_code=\K[^ ]+' | sort | uniq -c
```

## Alert Patterns

### Threshold Alerts

```yaml
# Example alert config
alerts:
  - name: high_error_rate
    condition: error_rate > 1%
    window: 5m
    severity: critical

  - name: slow_responses
    condition: p99_latency > 2s
    window: 10m
    severity: warning
```

### Pattern-Based Alerts

```yaml
alerts:
  - name: auth_failures
    pattern: "401.*login"
    threshold: 10
    window: 1m
    severity: high

  - name: database_errors
    pattern: "ECONNREFUSED.*5432"
    threshold: 1
    window: 1m
    severity: critical
```
