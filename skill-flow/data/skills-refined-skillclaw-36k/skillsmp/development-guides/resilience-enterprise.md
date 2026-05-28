# Resilience Enterprise

You are an expert in enterprise resilience patterns for Kailash SDK. Guide users through fault tolerance, retry logic, and graceful degradation.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/5-enterprise/resilience-patterns.md`

## Core Responsibilities

### 1. Retry Pattern
```python
workflow = WorkflowBuilder()

workflow.add_node("PythonCodeNode", "retry_operation", {
    "code": """
max_retries = 3
attempt = 0

while attempt < max_retries:
    try:
        result = risky_operation()
        break
    except Exception as e:
        attempt += 1
        if attempt >= max_retries:
            raise
        time.sleep(2 ** attempt)  # Exponential backoff

result = {'success': True, 'attempts': attempt}
"""
})
```

### 2. Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        self.state = "closed"

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
```

### 3. Graceful Degradation
```python
workflow.add_node("PythonCodeNode", "with_fallback", {
    "code": """
try:
    # Try primary service
    result = primary_service_call()
except Exception:
    # Fall back to secondary service
    try:
        result = secondary_service_call()
    except Exception:
        # Use cached data as last resort
        result = cached_data
"""
})
```

## When to Engage
- User asks about "resilience", "fault tolerance", "enterprise resilience"
- User needs retry logic
- User wants circuit breakers
- User needs graceful degradation

## Integration with Other Skills
- Route to **circuit-breaker** for detailed circuit breaker patterns
- Route to **monitoring-enterprise** for monitoring resilience
