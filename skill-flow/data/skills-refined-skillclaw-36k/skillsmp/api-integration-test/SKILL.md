---
name: api-integration-test
description: Validate external API integrations (SignalHouse, Apollo, Twilio) for reliability and security
---

# API Integration Testing Instructions

## Purpose
Ensure reliable, secure, and cost-effective integration with external APIs in OutreachGlobal's multi-tenant platform, with focus on SignalHouse, Apollo.io, Twilio, and other third-party services.

## When to Use This Skill
- Adding new API integrations
- Troubleshooting integration failures
- Before production deployments
- Monitoring API health and performance
- Security reviews of external connections

## Integration Architecture

### Core Integrations
- **SignalHouse**: SMS delivery and multi-channel campaigns
- **Apollo.io**: Lead enrichment and data sourcing
- **Twilio**: Voice calls and telephony
- **Stripe**: Payment processing
- **SendGrid**: Email delivery
- **Google/Apple**: Maps and geolocation

### Integration Patterns
- **Webhook endpoints**: Receive events from providers
- **REST APIs**: Outbound calls to external services
- **OAuth flows**: Secure authentication
- **Batch processing**: Bulk operations with rate limiting

## Testing Framework

### 1. Connection Testing
**Basic connectivity checks:**
```typescript
// Test SignalHouse API connection
const testConnection = async () => {
  try {
    const response = await signalhouse.getAccount();
    return response.status === 'active';
  } catch (error) {
    console.error('SignalHouse connection failed:', error);
    return false;
  }
};
```

### 2. Authentication Validation
**Verify API credentials:**
- Check API keys are valid and not expired
- Test OAuth token refresh flows
- Validate webhook signatures
- Confirm rate limit headers

### 3. Rate Limiting Tests
**Test throttling behavior:**
```typescript
const testRateLimits = async () => {
  const requests = Array(100).fill().map(() =>
    apollo.enrichPerson(personData)
  );

  const results = await Promise.allSettled(requests);
  const successRate = results.filter(r => r.status === 'fulfilled').length / results.length;

  return successRate > 0.8; // 80% success rate acceptable
};
```

### 4. Error Handling Validation
**Test failure scenarios:**
- Invalid API keys
- Network timeouts
- Rate limit exceeded
- Service unavailable
- Malformed responses

## Security Testing

### API Key Management
- [ ] Keys stored in environment variables
- [ ] No hardcoded credentials in code
- [ ] Key rotation procedures documented
- [ ] Access logging enabled

### Data Transmission
- [ ] HTTPS/TLS 1.3 required
- [ ] Sensitive data encrypted
- [ ] Webhook signatures validated
- [ ] No sensitive data in URLs

### Input Validation
- [ ] All inputs validated with Zod schemas
- [ ] SQL injection prevention
- [ ] XSS protection in webhook data
- [ ] File upload scanning

## Performance Testing

### Latency Benchmarks
```
SignalHouse SMS: < 500ms
Apollo enrichment: < 2000ms
Twilio voice: < 1000ms
Stripe payment: < 1500ms
```

### Throughput Testing
- Test concurrent API calls
- Monitor memory usage during bulk operations
- Check database connection pooling
- Validate queue processing rates

## Reliability Testing

### Circuit Breaker Implementation
```typescript
const apolloBreaker = new CircuitBreaker(apollo.enrichPerson, {
  timeout: 5000,
  errorThresholdPercentage: 50,
  resetTimeout: 60000
});
```

### Retry Logic
**Exponential backoff:**
```typescript
const retryWithBackoff = async (operation, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
};
```

### Monitoring & Alerting
**Key metrics to monitor:**
- API response times
- Error rates by endpoint
- Rate limit usage
- Cost per API call

## Cost Control Testing

### Budget Enforcement
```typescript
const costTracker = {
  apollo: { used: 0, limit: 1000 },
  signalhouse: { used: 0, limit: 5000 },
  twilio: { used: 0, limit: 1000 }
};

const checkBudget = (provider, cost) => {
  if (costTracker[provider].used + cost > costTracker[provider].limit) {
    throw new Error(`Budget exceeded for ${provider}`);
  }
  costTracker[provider].used += cost;
};
```

### Usage Optimization
- Implement caching for repeated requests
- Batch API calls where possible
- Use webhooks instead of polling
- Monitor and alert on unusual usage patterns

## Integration Test Suite

### Unit Tests
- Mock external API responses
- Test error handling paths
- Validate data transformation
- Check authentication flows

### Integration Tests
- End-to-end API call flows
- Webhook processing validation
- Database state consistency
- Multi-tenant isolation

### Load Tests
- Concurrent user scenarios
- Peak usage simulation
- Failure recovery testing
- Performance under load

## Response Format
When testing integrations, provide:
1. **Connectivity status** for each API
2. **Security assessment** with vulnerability findings
3. **Performance metrics** with benchmarks
4. **Reliability score** based on error rates
5. **Cost analysis** with optimization recommendations

## Related Skills
- Use with `security-scan` for API security validation
- Combine with `cost-guardian` for budget monitoring
- Reference `campaign-optimizer` for bulk operation testing