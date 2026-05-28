---
name: api-integration
description: Use this skill when you need to build robust API integrations, handling authentication, error management, and rate limiting in your applications.
---

# API Integration Skill

This skill provides patterns and best practices for building reliable API integrations in Python applications.

## Purpose
Build reliable integrations with external APIs, handling authentication flows, retries, rate limits, and error conditions gracefully.

## When to Use
- Integrating third-party services
- Building API clients
- Consuming webhooks
- Managing API credentials

## Key Capabilities
1. **Authentication Handling** - OAuth, API keys, JWT
2. **Error Recovery** - Retries with exponential backoff
3. **Rate Limit Management** - Respect API quotas

## HTTP Client Best Practices

### Client Setup
1. **Use a session for connection pooling** - Reuse connections for better performance.
2. **Set appropriate timeouts** - Always configure connect and read timeouts.
3. **Configure base URLs** - Use a base URL to avoid repetition.
4. **Add default headers** - Include User-Agent, Accept, and Content-Type headers.

### Request Handling
1. **Validate inputs before sending** - Check required parameters.
2. **Use appropriate HTTP methods** - GET for reads, POST for creates, etc.
3. **Handle query parameters properly** - Use library features, don't concatenate strings.
4. **Stream large responses** - Don't load large files entirely into memory.

### Response Processing
1. **Check status codes first** - Handle 4xx and 5xx errors appropriately.
2. **Parse JSON safely** - Handle malformed JSON responses.
3. **Validate response schema** - Ensure responses match expected format.
4. **Log important details** - Request ID, timing, status for debugging.

## Error Handling Strategies

### Retry Logic
Implement exponential backoff for transient errors:
- **Retry on**: 429 (Too Many Requests), 500, 502, 503, 504
- **Don't retry on**: 400, 401, 403, 404 (client errors)
- **Use exponential backoff**: Start with 1s, double each retry.
- **Set max retries**: Typically 3-5 attempts.

### Circuit Breaker Pattern
Prevent cascading failures:
- Track consecutive failures.
- Open circuit after threshold (e.g., 5 failures).
- Allow limited requests during half-open state.
- Close circuit after successful requests.

### Graceful Degradation
When APIs are unavailable:
- Return cached data if available.
- Provide meaningful error messages.
- Log failures for monitoring.
- Consider fallback services.

## Example
```python
import requests
from time import sleep
import logging

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'MyApp/1.0'
        })
    
    def make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logging.warning(f"Rate limited. Waiting {retry_after}s")
                    sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                # Exponential backoff
                wait = 2 ** attempt
                logging.warning(f"Request failed, retrying in {wait}s: {e}")
                sleep(wait)
        
        raise Exception("Max retries exceeded")
```

## Best Practices
- ✅ Implement exponential backoff for retries.
- ✅ Respect rate limits (429 responses).
- ✅ Use timeouts on all requests.
- ✅ Log all API interactions for debugging.
- ✅ Validate webhook signatures.
- ❌ Avoid: Infinite retry loops.
- ❌ Avoid: Storing API keys in code.

## Available Resources
See `references/api-patterns.md` for detailed implementation patterns.
See `examples/api-client-example.py` for working code examples.
Use `scripts/test-endpoint.sh` to test API endpoints.