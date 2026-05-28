# Retry with Exponential Backoff Pattern

## Metadata

- **Timestamp**: 2026-01-15 14:23:45
- **Project**: payment-service
- **Category**: Pattern
- **Tags**: resilience, http-client, retry, error-handling, go
- **Related Commit**: a3f7d92

## Context

When integrating with external payment APIs, network failures and temporary service unavailability are common. The service was experiencing frequent failures due to transient errors, impacting payment processing reliability.

## Pattern Description

Exponential backoff retry pattern for HTTP requests that automatically retries failed requests with increasing delays between attempts.

- **Solves**: Transient network failures and temporary service unavailability
- **When to use**: External API calls, network operations, distributed systems communication
- **When NOT to use**: User-initiated actions requiring immediate feedback, operations with strict time constraints

## Implementation

### Code Example

```go
type RetryConfig struct {
    MaxAttempts   int
    InitialDelay  time.Duration
    MaxDelay      time.Duration
    Multiplier    float64
}

func (c *HTTPClient) doWithRetry(req *http.Request, config RetryConfig) (*http.Response, error) {
    var resp *http.Response
    var err error

    delay := config.InitialDelay

    for attempt := 1; attempt <= config.MaxAttempts; attempt++ {
        resp, err = c.client.Do(req)

        if err == nil && resp.StatusCode < 500 {
            return resp, nil
        }

        if attempt == config.MaxAttempts {
            break
        }

        time.Sleep(delay)
        delay = time.Duration(float64(delay) * config.Multiplier)
        if delay > config.MaxDelay {
            delay = config.MaxDelay
        }
    }

    return resp, fmt.Errorf("max retry attempts reached: %w", err)
}
```

### Files Involved

- `internal/http/client.go` - HTTP client with retry logic implementation
- `internal/http/config.go` - Retry configuration structures
- `internal/payment/service.go` - Payment service using the retry client

### Key Components

1. **RetryConfig**: Configuration for retry behavior (max attempts, delays, multiplier)
2. **doWithRetry**: Core retry logic with exponential backoff calculation
3. **Error Classification**: Distinguishes between retryable and non-retryable errors

## Benefits

- Improved reliability against transient failures
- Reduced manual intervention for temporary issues
- Configurable retry behavior per use case
- Minimal code changes to existing HTTP clients

## Trade-offs

- Increased latency: Operations may take longer due to retries
- Resource consumption: Failed requests consume network and compute resources
- Potential cascading failures: If not carefully configured, retries can overwhelm downstream services
- Testing complexity: Need to test various failure scenarios and timing

## Related Patterns

- Circuit Breaker: Prevent cascading failures by stopping requests to failing services
- Bulkhead: Isolate resources to prevent one failing component from affecting others
- Timeout: Set maximum wait time for operations

## References

- [AWS Architecture Blog: Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Google Cloud: Retry Pattern](https://cloud.google.com/architecture/scalable-and-resilient-apps#retry_pattern)
