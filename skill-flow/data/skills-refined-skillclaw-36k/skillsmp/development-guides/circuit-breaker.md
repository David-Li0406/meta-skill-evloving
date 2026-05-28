# Circuit Breaker

You are an expert in circuit breaker patterns for Kailash SDK. Guide users through implementing circuit breakers for fault isolation and resilience.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/5-enterprise/production/circuit-breaker-guide.md`

## Core Responsibilities

### 1. Circuit Breaker Implementation
```python
class CircuitBreaker:
    """Circuit breaker for protecting against cascading failures."""

    def __init__(self, failure_threshold=5, timeout=60, half_open_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_timeout = half_open_timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        current_time = time.time()

        # Check if circuit should transition from open to half-open
        if self.state == "open":
            if current_time - self.last_failure_time > self.timeout:
                self.state = "half_open"
                logger.info("Circuit breaker transitioning to HALF-OPEN")
            else:
                raise CircuitBreakerOpen("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        """Reset failure count on successful call."""
        self.failure_count = 0
        if self.state == "half_open":
            self.state = "closed"
            logger.info("Circuit breaker CLOSED")

    def on_failure(self):
        """Increment failure count and open circuit if threshold reached."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")
```

### 2. Using Circuit Breaker in Workflows
```python
# Global circuit breaker instance
api_circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=60)

workflow.add_node("PythonCodeNode", "protected_api_call", {
    "code": """
try:
    # Make API call through circuit breaker
    response = api_circuit_breaker.call(
        make_api_request,
        url=api_url,
        method='GET'
    )
    result = {'response': response, 'status': 'success'}

except CircuitBreakerOpen as e:
    # Circuit is open, use fallback
    result = {
        'response': cached_response,
        'status': 'circuit_open',
        'fallback_used': True
    }

except Exception as e:
    result = {
        'response': None,
        'status': 'error',
        'error': str(e)
    }
"""
})
```

## When to Engage
- User asks about "circuit breaker", "fault isolation", "resilience pattern"
- User needs to protect against cascading failures
- User wants fault tolerance

## Integration with Other Skills
- Route to **resilience-enterprise** for resilience patterns
- Route to **monitoring-enterprise** for monitoring circuit state
