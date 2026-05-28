---
name: campaign-optimizer
description: Improve campaign execution efficiency and reliability in OutreachGlobal's multi-channel outreach platform
---

# Campaign Workflow Optimization Instructions

## Purpose
Optimize campaign execution for OutreachGlobal's AI-powered outreach platform, ensuring efficient processing of large-scale multi-channel campaigns while maintaining reliability and cost control.

## When to Use This Skill
- Designing new campaign workflows
- Troubleshooting campaign performance issues
- Optimizing for large-scale executions (500+ records)
- Before deploying campaign changes
- Analyzing campaign metrics and bottlenecks

## Campaign Architecture Overview

### Core Components
- **Lead State Machine**: Manages contact progression through touchpoints
- **Queue System**: BullMQ + Redis for background processing
- **AI Agents**: Gianna (SDR), LUCI (Research), Cathy (Follow-up)
- **Multi-Channel**: SMS, Voice, Email integration
- **Batch Processing**: Handle 10K+ record campaigns

### Performance Bottlenecks (From Audit)
1. **In-memory storage** (globalThis) - data lost on restart
2. **Unbounded loops** - infinite processing without limits
3. **No batch processing** - loads all records into memory
4. **Missing rate limiting** - API throttling issues
5. **Queue configuration** - Upstash 250/batch limit

## Optimization Strategies

### 1. Persistent Storage Migration
**Replace globalThis with database:**
```typescript
// ❌ Current problematic approach
(globalThis as any).__campaigns.push(campaignData);

// ✅ Recommended database approach
await db.insert(campaignsTable).values({
  id: campaignData.id,
  teamId: teamId,
  status: 'active',
  config: campaignData,
  createdAt: new Date(),
  updatedAt: new Date()
});
```

### 2. Batch Processing Implementation
**Process records in chunks:**
```typescript
const BATCH_SIZE = 100;
const batches = chunk(leads, BATCH_SIZE);

for (const batch of batches) {
  await processBatch(batch);
  await sleep(1000); // Rate limiting
}
```

### 3. Queue Optimization
**BullMQ configuration best practices:**
```typescript
const campaignQueue = new Queue('campaigns', {
  redis: redisConfig,
  defaultJobOptions: {
    removeOnComplete: 50,
    removeOnFail: 100,
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 5000
    }
  }
});
```

### 4. Rate Limiting Implementation
**API rate limiting:**
```typescript
const limiter = new RateLimiter({
  keyPrefix: 'signalhouse',
  points: 100, // requests
  duration: 60, // per 60 seconds
  execEvenly: true
});
```

## Performance Monitoring

### Key Metrics to Track
- **Throughput**: Records processed per minute
- **Latency**: Time from queue to completion
- **Error Rate**: Failed vs successful executions
- **Memory Usage**: Peak memory during processing
- **API Limits**: Calls remaining per hour

### Campaign Health Checks
```typescript
const campaignHealth = {
  queueDepth: await campaignQueue.getWaiting(),
  activeJobs: await campaignQueue.getActive(),
  failedJobs: await campaignQueue.getFailed(),
  completionRate: completed / total * 100
};
```

## Workflow Optimization Patterns

### 1. Lead Qualification Pipeline
**Progressive filtering:**
```
Raw Leads (10000)
  ↓ Enrichment (Apollo.io)
Qualified Leads (3000)
  ↓ AI Scoring
High-Priority (500)
  ↓ Campaign Execution
```

### 2. Multi-Touch Sequencing
**Intelligent spacing:**
- Touch 1: SMS introduction (immediate)
- Touch 2: Voice call (24h later)
- Touch 3: Follow-up SMS (48h later)
- Touch 4: AI follow-up (1 week later)

### 3. Error Recovery
**Resilient processing:**
```typescript
try {
  await processCampaignStep(step);
} catch (error) {
  await logError(error);
  await retryWithBackoff(step, error);
  if (retriesExhausted) {
    await quarantineLead(lead);
  }
}
```

## Cost Optimization

### API Usage Control
- **Deduplication**: Check existing contacts before enrichment
- **Caching**: Store enrichment results with TTL
- **Batching**: Group API calls to reduce overhead
- **Prioritization**: Process high-value leads first

### Resource Management
- **Memory limits**: Process in batches to control memory usage
- **CPU optimization**: Avoid blocking operations
- **Storage efficiency**: Compress campaign data
- **Cleanup**: Remove old campaign data regularly

## Reliability Improvements

### Circuit Breakers
**Fail fast on external service issues:**
```typescript
const signalhouseBreaker = new CircuitBreaker(sendSMS, {
  timeout: 5000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000
});
```

### Dead Letter Queues
**Handle unprocessable messages:**
```typescript
campaignQueue.on('failed', async (job, err) => {
  await deadLetterQueue.add({
    originalJob: job,
    error: err.message,
    retryCount: job.attemptsMade
  });
});
```

## Testing Strategies

### Load Testing
- Test with 500, 2000, 10000 record campaigns
- Monitor memory, CPU, and queue performance
- Validate error handling under load

### Integration Testing
- Test full campaign workflow end-to-end
- Verify webhook processing
- Check data consistency across services

## Response Format
When optimizing campaigns, provide:
1. **Performance analysis** with bottleneck identification
2. **Specific code changes** with before/after examples
3. **Scalability assessment** for target workloads
4. **Cost impact** analysis
5. **Monitoring recommendations** with key metrics

## Related Skills
- Use with `infra-capacity` for infrastructure scaling
- Combine with `cost-guardian` for budget monitoring
- Reference `signalhouse-integration` for API optimization