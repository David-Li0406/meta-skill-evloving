---
name: cost-guardian
description: Prevent cost overruns from API abuse, infinite loops, and inefficient resource usage
---

# Cost Control and Budget Management Instructions

## Purpose
Monitor, control, and optimize costs across OutreachGlobal's multi-tenant platform, preventing budget overruns from API calls, infrastructure, and inefficient processing patterns.

## When to Use This Skill
- Reviewing code that makes external API calls
- Planning campaign executions
- Investigating cost spikes
- Setting up new integrations
- Monthly budget reviews

## Cost Landscape Analysis

### Primary Cost Drivers (From Audit)
1. **Apollo.io Enrichment**: $0.10 per record
2. **SignalHouse SMS**: $0.015 per message
3. **Twilio Voice**: $0.025 per minute
4. **Anthropic AI**: $0.003 per token
5. **Digital Ocean Infrastructure**: $350-450/month

### Risk Areas
- **Infinite loops** in enrichment processing
- **Duplicate API calls** without deduplication
- **Unbounded retries** on failed requests
- **Large batch processing** without limits
- **Missing rate limiting** on external APIs

## Cost Control Mechanisms

### 1. Budget Enforcement
**Per-tenant budgets:**
```typescript
const tenantBudgets = {
  apollo: { daily: 100, monthly: 3000 },
  signalhouse: { daily: 500, monthly: 15000 },
  twilio: { daily: 200, monthly: 6000 }
};

const checkBudget = async (tenantId, service, cost) => {
  const usage = await getTenantUsage(tenantId, service, 'month');
  if (usage + cost > tenantBudgets[service].monthly) {
    throw new Error(`Monthly budget exceeded for ${service}`);
  }
};
```

### 2. Rate Limiting Implementation
**API call throttling:**
```typescript
import { RateLimiterMemory } from 'rate-limiter-flexible';

const apolloLimiter = new RateLimiterMemory({
  keyPrefix: 'apollo',
  points: 1000, // calls
  duration: 3600, // per hour
});

const signalhouseLimiter = new RateLimiterMemory({
  keyPrefix: 'signalhouse',
  points: 5000, // calls
  duration: 3600, // per hour
});
```

### 3. Deduplication Systems
**Prevent duplicate enrichment:**
```typescript
const enrichmentCache = new Map();

const deduplicateEnrichment = async (personData) => {
  const cacheKey = `${personData.firstName}-${personData.lastName}-${personData.company}`;

  if (enrichmentCache.has(cacheKey)) {
    return enrichmentCache.get(cacheKey);
  }

  const result = await apollo.enrichPerson(personData);
  enrichmentCache.set(cacheKey, result);

  // Expire cache after 24 hours
  setTimeout(() => enrichmentCache.delete(cacheKey), 24 * 60 * 60 * 1000);

  return result;
};
```

### 4. Circuit Breakers
**Fail fast on cost issues:**
```typescript
const costCircuitBreaker = (service, operation) => {
  return async (...args) => {
    const estimatedCost = estimateCost(service, args);

    if (estimatedCost > BUDGET_THRESHOLD) {
      throw new Error(`Estimated cost too high: $${estimatedCost}`);
    }

    return await operation(...args);
  };
};
```

## Monitoring and Alerting

### Real-time Cost Tracking
**Per-request cost logging:**
```typescript
const trackCost = async (service, operation, result) => {
  const cost = calculateCost(service, operation, result);

  await db.insert(costLogTable).values({
    tenantId,
    service,
    operation,
    cost,
    timestamp: new Date()
  });

  // Check against budgets
  const monthlyUsage = await getMonthlyUsage(tenantId, service);
  if (monthlyUsage > BUDGET_WARNING_THRESHOLD) {
    await sendBudgetAlert(tenantId, service, monthlyUsage);
  }
};
```

### Cost Anomaly Detection
**Unusual spending patterns:**
- Sudden spikes in API usage
- Costs exceeding historical averages
- Single tenant consuming disproportionate resources
- Failed requests generating retry storms

## Optimization Strategies

### 1. Batch Processing Efficiency
**Group operations to reduce overhead:**
```typescript
// ❌ Inefficient: Individual calls
for (const lead of leads) {
  await apollo.enrichPerson(lead); // $0.10 each
}

// ✅ Efficient: Batch processing
const batches = chunk(leads, 50);
for (const batch of batches) {
  await apollo.enrichBatch(batch); // $0.05 each
  await sleep(1000); // Rate limiting
}
```

### 2. Caching Strategies
**Reduce redundant API calls:**
- Cache enrichment results for 24-48 hours
- Cache geolocation data
- Cache API rate limit status
- Use Redis for distributed caching

### 3. Progressive Loading
**Load data on demand:**
```typescript
// Lazy load expensive operations
const leadCard = {
  basic: () => getBasicInfo(lead),
  enriched: () => apollo.enrichPerson(lead), // Only when needed
  scored: () => ai.scoreLead(lead) // Only when requested
};
```

## Budget Planning Framework

### Cost Estimation
**Per campaign calculation:**
```
500-record campaign:
- Apollo enrichment: 500 × $0.10 = $50
- SignalHouse SMS: 500 × $0.015 = $7.50
- AI processing: 500 × $0.10 = $50
- Infrastructure: $10
Total: ~$117.50
```

### Budget Allocation
- **70%**: External API costs
- **20%**: Infrastructure
- **10%**: Monitoring and tools

## Response Format
When analyzing costs, provide:
1. **Cost breakdown** by service and operation
2. **Budget status** with warnings for approaching limits
3. **Optimization recommendations** with potential savings
4. **Risk assessment** for cost overruns
5. **Monitoring setup** for ongoing cost control

## Emergency Cost Controls

### Kill Switches
**Immediate shutdown capabilities:**
- Per-tenant API disabling
- Campaign execution pausing
- Rate limit reduction
- Service degradation modes

### Cost Quarantine
**Isolate problematic tenants:**
```typescript
const quarantineTenant = async (tenantId) => {
  await disableTenantAPIs(tenantId);
  await notifyTenant(tenantId, 'Budget exceeded - services paused');
  await scheduleReview(tenantId);
};
```

## Related Skills
- Use with `campaign-optimizer` for efficient processing
- Combine with `api-integration-test` for cost validation
- Reference `infra-capacity` for infrastructure cost optimization