---
name: api-integration
description: API integration patterns for building robust HTTP clients, handling authentication, error handling, and rate limiting.
version: 1.0.0
author: AIECS Team
tags:
  - api
  - http
  - rest
  - integration
  - requests
dependencies: []
recommended_tools:
  - python
  - requests
  - httpx
  - curl
scripts:
  test-endpoint:
    path: scripts/test-endpoint.sh
    mode: subprocess
    description: Tests an API endpoint and reports status
    parameters:
      url:
        type: string
        required: true
        description: The URL of the endpoint to test
      method:
        type: string
        required: false
        description: HTTP method (GET, POST, etc.)
---

# API Integration Skill

This skill provides patterns and best practices for building robust API integrations in Python applications.

## When to Use This Skill

Use this skill when you need to:

- Build HTTP clients to consume REST APIs
- Implement authentication flows (API keys, OAuth, JWT)
- Handle API errors gracefully with retries
- Manage rate limiting and throttling
- Parse and validate API responses

## HTTP Client Best Practices

### Client Setup

1. **Use a session for connection pooling** - Reuse connections for better performance
2. **Set appropriate timeouts** - Always configure connect and read timeouts
3. **Configure base URLs** - Use a base URL to avoid repetition
4. **Add default headers** - Include User-Agent, Accept, and Content-Type headers

### Request Handling

1. **Validate inputs before sending** - Check required parameters
2. **Use appropriate HTTP methods** - GET for reads, POST for creates, etc.
3. **Handle query parameters properly** - Use library features, don't concatenate strings
4. **Stream large responses** - Don't load large files entirely into memory

### Response Processing

1. **Check status codes first** - Handle 4xx and 5xx errors appropriately
2. **Parse JSON safely** - Handle malformed JSON responses
3. **Validate response schema** - Ensure responses match expected format
4. **Log important details** - Request ID, timing, status for debugging

## Error Handling Strategies

### Retry Logic

Implement exponential backoff for transient errors:

- **Retry on**: 429 (Too Many Requests), 500, 502, 503, 504
- **Don't retry on**: 400, 401, 403, 404 (client errors)
- **Use exponential backoff**: Start with 1s, double each retry
- **Set max retries**: Typically 3-5 attempts

### Circuit Breaker Pattern

Prevent cascading failures:

- Track consecutive failures
- Open circuit after threshold (e.g., 5 failures)
- Allow limited requests during half-open state
- Close circuit after successful requests

### Graceful Degradation

When APIs are unavailable:

- Return cached data if available
- Provide meaningful error messages
- Log failures for monitoring
- Consider fallback services

## Available Resources

See `references/api-patterns.md` for detailed implementation patterns.
See `examples/api-client-example.py` for working code examples.
Use `scripts/test-endpoint.sh` to test API endpoints.

