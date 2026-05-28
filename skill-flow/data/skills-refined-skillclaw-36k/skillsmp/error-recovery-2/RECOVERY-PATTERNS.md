# Recovery Patterns

Strategies, retry patterns, and fallback techniques for handling Claude Code errors gracefully.

---

## Retry Strategies

### Simple Retry

Best for transient errors (rate limits, temporary failures).

```
Attempt 1 --> Fail --> Wait 1s --> Attempt 2 --> Fail --> Wait 1s --> Attempt 3
```

**When to Use:**
- Network glitches
- Rate limit errors
- Overload errors
- Temporary service issues

**Implementation:**
```javascript
function simpleRetry(operation, maxAttempts = 3, delayMs = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return operation();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      sleep(delayMs);
    }
  }
}
```

---

### Exponential Backoff

Increases delay between retries to reduce load during outages.

```
Attempt 1 --> Fail --> Wait 1s
Attempt 2 --> Fail --> Wait 2s
Attempt 3 --> Fail --> Wait 4s
Attempt 4 --> Fail --> Wait 8s
Attempt 5 --> Success
```

**When to Use:**
- API overload errors
- Resource contention
- High-traffic scenarios
- Service degradation

**Implementation:**
```javascript
function exponentialBackoff(operation, maxAttempts = 5, baseDelayMs = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return operation();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      const delay = baseDelayMs * Math.pow(2, attempt - 1);
      sleep(Math.min(delay, 60000)); // Cap at 60s
    }
  }
}
```

---

### Exponential Backoff with Jitter

Adds randomness to prevent thundering herd.

```
Attempt 1 --> Fail --> Wait 1.2s (1s + 200ms jitter)
Attempt 2 --> Fail --> Wait 2.8s (2s + 800ms jitter)
Attempt 3 --> Fail --> Wait 4.1s (4s + 100ms jitter)
```

**When to Use:**
- Multiple clients retrying simultaneously
- Distributed systems
- High-contention resources

**Implementation:**
```javascript
function backoffWithJitter(operation, maxAttempts = 5, baseDelayMs = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return operation();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      const base = baseDelayMs * Math.pow(2, attempt - 1);
      const jitter = Math.random() * 1000;
      sleep(Math.min(base + jitter, 60000));
    }
  }
}
```

---

### Circuit Breaker

Stops retrying when failure rate is too high.

```
Normal --> [Failures > Threshold] --> Open
Open --> [Timeout Elapsed] --> Half-Open
Half-Open --> [Success] --> Normal
Half-Open --> [Failure] --> Open
```

**States:**
- **Closed (Normal)**: Requests pass through, failures counted
- **Open**: Requests immediately fail, no attempt made
- **Half-Open**: Single test request allowed

**When to Use:**
- Persistent API failures
- Service outages
- Protecting downstream services
- Preventing cascade failures

**Implementation:**
```javascript
class CircuitBreaker {
  constructor(threshold = 3, resetTimeout = 60000) {
    this.failures = 0;
    this.threshold = threshold;
    this.resetTimeout = resetTimeout;
    this.state = 'closed';
    this.lastFailure = null;
  }

  async execute(operation) {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}
```

---

## Fallback Strategies

### Graceful Degradation

Provide reduced functionality when full functionality unavailable.

**Pattern:**
```
Primary Operation --> Fail --> Fallback Operation --> Partial Result
```

**Examples:**

| Primary | Fallback | Trade-off |
|---------|----------|-----------|
| Full file read | First 1000 lines | Less data, still useful |
| API call | Cached result | Stale data, still works |
| Complex query | Simple query | Less info, still answers |
| Real-time data | Last known value | Not current, still functional |

**Implementation:**
```javascript
async function withFallback(primary, fallback) {
  try {
    return await primary();
  } catch (error) {
    console.warn(`Primary failed: ${error.message}, using fallback`);
    return await fallback();
  }
}

// Usage
const result = await withFallback(
  () => readFullFile(path),
  () => readFileHead(path, 1000)
);
```

---

### Default Values

Return safe defaults when operation fails.

**Pattern:**
```
Operation --> Fail --> Return Default
```

**Examples:**

| Operation | Default | Rationale |
|-----------|---------|-----------|
| Get config value | Sensible default | Continue with standard behavior |
| List files | Empty array | No files to process is valid |
| Get count | Zero | Treat as "none found" |
| Get object | Empty object | Avoid null pointer errors |

**Implementation:**
```javascript
function withDefault(operation, defaultValue) {
  try {
    const result = operation();
    return result ?? defaultValue;
  } catch (error) {
    return defaultValue;
  }
}

// Usage
const config = withDefault(
  () => readConfig(),
  { timeout: 30000, retries: 3 }
);
```

---

### Alternative Paths

Try different approaches when primary fails.

**Pattern:**
```
Path A --> Fail --> Path B --> Fail --> Path C --> Success
```

**Examples:**

| Path A | Path B | Path C |
|--------|--------|--------|
| Specific file | Parent directory | Search recursively |
| Exact match | Fuzzy match | Ask user |
| Fast method | Slow method | Manual intervention |
| Primary API | Backup API | Local cache |

**Implementation:**
```javascript
async function tryAlternatives(...alternatives) {
  const errors = [];
  for (const alt of alternatives) {
    try {
      return await alt();
    } catch (error) {
      errors.push(error);
    }
  }
  throw new Error(`All alternatives failed: ${errors.map(e => e.message).join(', ')}`);
}

// Usage
const file = await tryAlternatives(
  () => readFile('./config.json'),
  () => readFile('./config.default.json'),
  () => ({ default: true })
);
```

---

## Recovery Workflows

### Context Overflow Recovery

When context exceeds token limit:

```
1. Error: context_length_exceeded
   |
2. Try /compact
   |
   +-- Success --> Continue with summarized context
   +-- Fail --> Continue to step 3
   |
3. Try /clear with checkpoint
   |
   +-- Save important state externally
   +-- Clear context
   +-- Reload essential state
   |
4. Continue with fresh context
```

**Commands:**
```bash
# Try compact first
/compact

# If still too large, save state and clear
# Save important info to file first
# Then clear
/clear

# Re-establish context from saved state
```

---

### Rate Limit Recovery

When hitting API rate limits:

```
1. Error: rate_limit_error
   |
2. Extract retry-after header (or default 60s)
   |
3. Wait for specified duration
   |
4. Retry with reduced request rate
   |
   +-- Success --> Continue with throttling
   +-- Fail --> Increase wait time, retry
```

**Best Practice:**
- Track request timing
- Implement request queue
- Spread requests over time
- Batch when possible

---

### MCP Server Recovery

When MCP server fails:

```
1. Error: mcp_connection_failed
   |
2. Check server status
   |
   +-- Not running --> Start server
   +-- Running --> Continue to step 3
   |
3. Check configuration
   |
   +-- Invalid --> Fix .mcp.json
   +-- Valid --> Continue to step 4
   |
4. Test connection
   |
   +-- Success --> Resume operations
   +-- Fail --> Restart server, retry
```

**Commands:**
```bash
# Check MCP status
/mcp

# Restart server (example for local server)
claude mcp restart <server-name>

# Verify configuration
cat .mcp.json | jq .
```

---

### Permission Denied Recovery

When tool permission denied:

```
1. Error: permission_denied for [tool]
   |
2. Check current permissions
   |
3. Determine if tool should be allowed
   |
   +-- Yes --> Allow tool
   +-- No --> Use alternative approach
   |
4. Retry operation
```

**Commands:**
```bash
# Check permissions
/permissions

# Allow specific tool
/permissions --allow [tool]

# Allow with pattern
/permissions --allow "Bash(git:*)"
```

---

## State Recovery

### Session Checkpoint Pattern

Save state before risky operations:

```
1. Serialize current state
   |
2. Save to external file
   |
3. Perform risky operation
   |
   +-- Success --> Clean up checkpoint
   +-- Fail --> Restore from checkpoint
```

**Implementation:**
```bash
# Before risky operation
# Save important context to file

# Perform operation
# ...

# On failure, reference saved state
cat /tmp/checkpoint.json
```

---

### Memory Bank Recovery

When memory needs recovery:

```
1. Error or corruption in memory
   |
2. Check memory status
   |
3. Clear affected memory bank
   |
4. Restore from external backup if available
   |
5. Continue with cleaned memory
```

**Commands:**
```bash
# Check memory
/memory

# Clear specific bank
/memory clear <bank-name>

# Clear all memory
/memory clear --all
```

---

## Error Handling Patterns

### Catch and Transform

Transform low-level errors to user-friendly messages:

```javascript
try {
  await operation();
} catch (error) {
  if (error.code === 'ENOENT') {
    throw new UserError(`File not found: ${error.path}`);
  }
  if (error.code === 'EACCES') {
    throw new UserError(`Permission denied: ${error.path}`);
  }
  throw new UserError(`Unexpected error: ${error.message}`);
}
```

---

### Catch and Log

Log errors for debugging while continuing:

```javascript
try {
  await optionalOperation();
} catch (error) {
  console.error(`Optional operation failed: ${error.message}`);
  // Continue without this result
}
```

---

### Catch and Escalate

Wrap and re-throw with context:

```javascript
try {
  await operation();
} catch (error) {
  throw new Error(`Failed during [context]: ${error.message}`, { cause: error });
}
```

---

## Recovery Checklists

### Quick Recovery Checklist

- [ ] Identify error type from message
- [ ] Check quick reference for immediate fix
- [ ] Apply appropriate retry strategy
- [ ] Use fallback if retry fails
- [ ] Verify recovery with health check

### Deep Recovery Checklist

- [ ] Enable debug mode (`claude --debug`)
- [ ] Review error logs
- [ ] Identify root cause
- [ ] Check configuration files
- [ ] Clear caches if needed
- [ ] Reset affected components
- [ ] Verify fix with test case
- [ ] Document fix for future

### Escalation Checklist

- [ ] Confirm error is reproducible
- [ ] Gather debug output
- [ ] Note Claude Code version
- [ ] Document steps to reproduce
- [ ] Submit bug report via `/bug`
- [ ] Check for existing issues
- [ ] Follow up as needed
