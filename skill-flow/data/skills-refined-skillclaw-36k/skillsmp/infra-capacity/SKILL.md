---
name: infra-capacity
description: Monitor and plan Digital Ocean infrastructure scaling for OutreachGlobal's multi-tenant platform
---

# Infrastructure Capacity Planning Instructions

## Purpose
Ensure Digital Ocean infrastructure can handle OutreachGlobal's campaign workloads, with focus on memory, CPU, database performance, and scaling limits.

## When to Use This Skill
- Planning infrastructure upgrades
- Before large campaign executions
- Investigating performance issues
- Cost optimization reviews
- Capacity planning for growth

## Current Infrastructure Assessment

### Digital Ocean App Platform
**Current specs (from audit):**
- Frontend: 512MB RAM (insufficient for 500+ records)
- API: 512MB RAM (will OOM on large queries)
- Database: 1vCPU / 1GB RAM (cannot handle batch operations)

**Recommended minimums:**
- Frontend: 2GB RAM
- API: 2GB RAM
- Database: 2vCPU / 4GB RAM with HA

### Performance Benchmarks

#### Memory Requirements
```
Small campaign (50 records):   512MB sufficient
Medium campaign (500 records): 2GB minimum
Large campaign (2000 records): 4GB recommended
Mass campaign (10000 records): 8GB+ required
```

#### Database Scaling
```
Current: 1vCPU/1GB
- Max concurrent queries: ~10
- Max records per query: ~1000
- Batch processing: Not supported

Recommended: 2vCPU/4GB
- Max concurrent queries: ~50
- Max records per query: ~10000
- Batch processing: Supported
```

### Monitoring Metrics

#### Key Performance Indicators
- **Memory usage** > 80% = Scale up
- **CPU usage** > 70% sustained = Add instances
- **Database connections** > 80% of limit = Scale DB
- **Response time** > 2 seconds = Performance issue
- **Error rate** > 1% = Investigate immediately

#### Cost Optimization
```
Current monthly cost: ~$92
Recommended for production: ~$400-500

Breakdown:
- App Platform (2GB instances): $144
- Database (2vCPU/4GB HA): $240
- Monitoring (Sentry): $30
- Spaces: $20
```

## Scaling Strategies

### Horizontal Scaling
**App Platform auto-scaling:**
- Scale based on CPU/memory usage
- Minimum 1 instance, maximum 5
- Scale-up time: 2-3 minutes

### Vertical Scaling
**Instance size upgrades:**
- 1GB → 2GB: Handles 500 record campaigns
- 2GB → 4GB: Handles 2000 record campaigns
- 4GB+: Handles mass campaigns

### Database Scaling
**Read replicas for reporting:**
- Primary: Write operations
- Replicas: Analytics and reporting
- Connection pooling required

## Capacity Planning Framework

### 1. Workload Analysis
**Calculate requirements:**
```
Campaign size × Processing factor × Safety margin

Example: 500 records
500 × 2MB memory per record × 1.5 safety = 1.5GB minimum
```

### 2. Peak Load Planning
**Identify peak usage:**
- Campaign execution windows
- API call patterns
- Database query spikes
- File upload periods

### 3. Failure Mode Analysis
**Plan for failures:**
- Instance failure: Auto-restart within 3 minutes
- Database failover: HA setup with < 30 second switch
- Regional outage: Multi-region deployment

## Cost-Benefit Analysis

### Scaling Triggers
```
Memory > 85%: Immediate scale-up
CPU > 75% for 5+ minutes: Add instance
Database connections > 90%: Scale database
Campaign failures > 5%: Infrastructure issue
```

### Cost Control
- Use reserved instances for predictable workloads
- Implement auto-scaling down after peak hours
- Monitor and alert on cost anomalies
- Regular capacity reviews (monthly)

## Implementation Checklist

### Immediate Actions (Week 1)
- [ ] Upgrade all instances to 2GB RAM minimum
- [ ] Scale database to 2vCPU/4GB
- [ ] Enable auto-scaling on App Platform
- [ ] Setup monitoring alerts

### Medium-term (Month 1)
- [ ] Implement connection pooling
- [ ] Add read replicas for analytics
- [ ] Setup performance monitoring
- [ ] Create scaling playbooks

### Long-term (Quarter 1)
- [ ] Multi-region deployment
- [ ] Advanced auto-scaling rules
- [ ] Cost optimization automation
- [ ] Performance benchmarking suite

## Response Format
When analyzing capacity, provide:
1. **Current utilization** percentages
2. **Bottleneck identification** with specific metrics
3. **Scaling recommendations** with cost impact
4. **Timeline and risk assessment**
5. **Monitoring setup** requirements

## Related Skills
- Use with `campaign-optimizer` for workload optimization
- Combine with `cost-guardian` for budget monitoring
- Reference `security-scan` for secure scaling practices