# API Resilience & Error Handling (2026)

Strategies for building robust API integrations that handle failure gracefully in distributed systems.

## 1. Standardized Error Handling: RFC 7807 (Problem Details)

Modern APIs in 2026 return "Problem Details" objects instead of just a status code or a custom error string.

### RFC 7807 Structure
```json
{
  "type": "https://api.example.com/probs/out-of-stock",
  "title": "Out of Stock",
  "status": 403,
  "detail": "The requested item (ID: 123) is currently out of stock in your region.",
  "instance": "/orders/987/items/123",
  "balance": 0 
}
```

### TypeScript Client Implementation
```typescript
interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  [key: string]: any; // Extension members
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const contentType = response.headers.get("content-type");
    if (contentType?.includes("application/problem+json")) {
      const problem = await response.json() as ProblemDetails;
      throw new APIError(problem.title, problem);
    }
    throw new Error(`Standard HTTP Error: ${response.status}`);
  }
  return response.json();
}
```

## 2. Advanced Retry Patterns

### Exponential Backoff with Jitter
Plain exponential backoff can lead to "thundering herd" problems. Adding **Jitter** spreads the load.

```typescript
async function retryWithJitter<T>(
  fn: () => Promise<T>,
  retries = 3,
  baseDelay = 1000
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries === 0 || !isRetryable(error)) throw error;
    
    // delay = baseDelay * 2^attempt + random_jitter
    const delay = (baseDelay * Math.pow(2, 3 - retries)) + (Math.random() * 1000);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    return retryWithJitter(fn, retries - 1, baseDelay);
  }
}
```

## 3. Circuit Breaker Pattern

Prevent a failing service from overwhelming your system or itself by "tripping" the circuit after a threshold of failures.

### Simplified State Machine
- **CLOSED**: Requests flow normally. Failures increment a counter.
- **OPEN**: Requests fail immediately. After a `resetTimeout`, move to HALF_OPEN.
- **HALF_OPEN**: Allow a limited number of test requests. If they succeed, move to CLOSED. If they fail, back to OPEN.

## 4. Rate Limit Awareness (2026)

Modern APIs use `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers (standardized).

```typescript
function getRateLimitInfo(headers: Headers) {
  return {
    limit: parseInt(headers.get('RateLimit-Limit') || '0'),
    remaining: parseInt(headers.get('RateLimit-Remaining') || '0'),
    reset: parseInt(headers.get('RateLimit-Reset') || '0'), // Unix timestamp
  };
}
```

## 5. AI-Friendly Error Messages
When designing APIs for AI agents, include **Remediation Steps** in your error responses.

```json
{
  "status": 400,
  "error": "invalid_input",
  "remediation": "The 'start_date' must be in ISO 8601 format. Example: '2026-01-22T15:18:00Z'."
}
```

*Updated: January 22, 2026 - 15:18
