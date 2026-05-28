---
name: limit-request-rate
description: Security pattern for implementing rate limiting and throttling. Use when protecting against brute-force attacks, DoS/DDoS mitigation, preventing resource exhaustion, or limiting API abuse. Addresses "Entity absorbs excessive resources" problem.
---

# Limit Request Rate Security Pattern

Limits the number of requests an entity can make within a given timeframe, preventing resource exhaustion and brute-force attacks.

## Problem Addressed

**Entity absorbs excessive resources**: An attacker floods the system with requests, either to:
- Exhaust system resources (DoS)
- Brute-force authentication credentials
- Enumerate valid identifiers
- Abuse expensive operations

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Entity** | Entity | Makes requests to system |
| **Enforcer** | Enforcement Point | Intercepts and rate-checks requests |
| **Limiter** | Decision Point | Decides if request within limits |
| **Policy Provider** | Information Point | Manages rate limit rules |
| **History Store** | Storage | Tracks request history per entity |

### Data Elements

- **id**: Identifier for the entity (IP, user, API key)
- **history**: Record of entity's previous requests
- **policy**: Rules defining allowed request rates
- **action**: The requested operation

## Rate Limiting Flow

```
Entity → [action] → Enforcer
Enforcer → [check(id)] → Limiter
Limiter → [get_policy(id)] → Policy Provider
Policy Provider → [policy] → Limiter
Limiter → [get_history(id)] → History Store
History Store → [history] → Limiter
Limiter → [allowed/denied] → Enforcer
Enforcer → [action] → System (if allowed)
        → [429 Too Many Requests] → Entity (if denied)
```

## Entity Identification

How to identify entities for rate limiting:

| Identifier | Pros | Cons |
|------------|------|------|
| IP Address | Simple, no auth needed | NAT/proxy issues, IPv6 abundant |
| User/API Key | Accurate per-user | Requires authentication |
| Session ID | Works for logged-in users | Session rotation may reset |
| Combination | More precise | Complex implementation |

**Recommendation**: Use multiple identifiers where possible.

## Rate Limiting Algorithms

### Fixed Window
- Count requests in fixed time periods
- Simple but allows bursts at window boundaries
- Example: 100 requests per minute

### Sliding Window
- Rolling time window
- Smoother rate enforcement
- More memory intensive

### Token Bucket
- Tokens added at fixed rate
- Request consumes token
- Allows controlled bursts
- Good for APIs

### Leaky Bucket
- Requests queued and processed at fixed rate
- Smooths traffic
- May add latency

## Policy Configuration

Define policies based on:
- **Endpoint sensitivity**: Stricter limits on auth endpoints
- **User type**: Different limits for free vs. paid users
- **Operation cost**: Stricter limits on expensive operations
- **Time of day**: Adjusted limits for peak periods

Example policies:
```
/login:        5 requests per minute per IP
/api/search:   100 requests per minute per API key
/api/export:   10 requests per hour per user
```

## Security Considerations

### Authentication Endpoints
- Aggressive rate limiting on login
- Limit by IP AND username
- Exponential backoff after failures
- Consider CAPTCHA after threshold

### Distributed Attacks
- Single IP limits insufficient
- Monitor aggregate patterns
- Consider global rate limits
- Use reputation services

### Response Headers
Inform clients of limits:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
Retry-After: 60
```

### Failure Handling
- Rate limiting infrastructure must be resilient
- Fail-open vs. fail-closed decision
- Don't let rate limiter become DoS vector

### Bypass Prevention
- Ensure rate limiter cannot be circumvented
- Apply at edge/gateway level
- Rate limit before expensive operations

## Implementation Approaches

### Application Level
- Fine-grained control
- Access to user context
- Higher overhead

### API Gateway Level
- Central enforcement
- Consistent across services
- May lack context

### Infrastructure Level (CDN/WAF)
- Handles volumetric attacks
- Limited application context
- Good first line of defense

**Recommendation**: Defense in depth—use multiple levels.

## Implementation Checklist

- [ ] Authentication endpoints rate limited
- [ ] Limits per IP AND per user where applicable
- [ ] Appropriate algorithm selected
- [ ] Rate limit headers returned
- [ ] 429 responses with Retry-After
- [ ] Limits at multiple levels (app, gateway, CDN)
- [ ] Monitoring and alerting on limits hit
- [ ] Distributed attack patterns detected
- [ ] Expensive operations protected
- [ ] Fail behavior defined

## Related Patterns

- Authentication (protect login endpoints)
- Authorisation (rate limit authorization checks)
- Data validation (rate limit before validation)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/02_03_001__limit_request_rate/
- OWASP Rate Limiting
- RFC 6585 (429 Too Many Requests)
