# Post-Deployment Verification Checklist

## Overview
This checklist ensures the deployment was successful and the system is operating correctly. Complete these checks immediately after deployment and continue monitoring for the specified duration.

## Immediate Verification (0-15 minutes)

### Deployment Success
- [ ] Deployment command/script completed without errors
- [ ] All instances/pods are running
- [ ] Correct version deployed (verify version endpoint or image tag)
- [ ] No instances stuck in pending or error state
- [ ] Load balancer routing to new instances
- [ ] Old instances properly terminated (for rolling deployments)

### Health Checks
- [ ] Health check endpoint returns 200 OK
- [ ] All health check components reporting healthy
- [ ] Liveness probes passing
- [ ] Readiness probes passing
- [ ] All instances passing health checks
- [ ] Load balancer health checks green

### Basic Functionality
- [ ] Application responds to requests
- [ ] Homepage/main endpoint loads correctly
- [ ] API endpoints responding
- [ ] Authentication working
- [ ] Database connectivity confirmed
- [ ] External service integrations working

## Critical Path Testing (15-30 minutes)

### Smoke Tests
- [ ] Critical user flow #1 works end-to-end
- [ ] Critical user flow #2 works end-to-end
- [ ] Critical user flow #3 works end-to-end
- [ ] Payment processing works (if applicable)
- [ ] User registration/login works
- [ ] Data retrieval working correctly
- [ ] Data updates persisting correctly

### API Testing
- [ ] GET endpoints returning correct data
- [ ] POST endpoints creating records
- [ ] PUT/PATCH endpoints updating records
- [ ] DELETE endpoints removing records
- [ ] Authentication endpoints working
- [ ] Authorization rules enforced

### Static Assets
- [ ] Images loading correctly
- [ ] CSS styles applied
- [ ] JavaScript executing without errors
- [ ] Fonts rendering correctly
- [ ] CDN serving assets (if applicable)

## Monitoring and Metrics (30-60 minutes)

### Error Monitoring
- [ ] No error spikes in application logs
- [ ] Error rate within normal range (< 1%)
- [ ] No critical errors in logs
- [ ] Exception tracking shows no new critical issues
- [ ] No database connection errors
- [ ] No external API timeout errors

### Performance Metrics
- [ ] Response time within SLA (typically < 500ms p95)
- [ ] Response time similar to pre-deployment
- [ ] No significant latency increase
- [ ] Throughput handling expected load
- [ ] No request queuing/backlog

### Resource Utilization
- [ ] CPU usage within normal range (< 70%)
- [ ] Memory usage stable (no leaks detected)
- [ ] Disk I/O normal
- [ ] Network traffic normal
- [ ] Database connections within limits
- [ ] Cache hit rate acceptable

### Application Metrics
- [ ] Request rate as expected
- [ ] Success rate > 99%
- [ ] Active users/sessions normal
- [ ] Business metrics stable (conversions, signups, etc.)
- [ ] Queue depths normal
- [ ] Background job processing normal

## Database and Data Integrity (30-60 minutes)

### Database Health
- [ ] Database connections stable
- [ ] Query performance normal
- [ ] No slow query alerts
- [ ] Database replication lag acceptable (< 5 seconds)
- [ ] Connection pool usage healthy
- [ ] No deadlocks or lock timeouts

### Data Verification
- [ ] Database migrations applied successfully
- [ ] Data integrity checks passed
- [ ] No data corruption detected
- [ ] Foreign key constraints valid
- [ ] Indexes performing well
- [ ] Sample data queries return expected results

## Infrastructure and Networking

### Infrastructure
- [ ] All required services running
- [ ] Auto-scaling functioning correctly
- [ ] Load balancer distributing traffic evenly
- [ ] DNS routing correctly
- [ ] SSL certificates valid and working
- [ ] Network policies enforced

### Service Dependencies
- [ ] All dependent microservices healthy
- [ ] Message queues processing messages
- [ ] Cache services responding
- [ ] External APIs accessible
- [ ] Third-party integrations working

## Security Verification

### Security Checks
- [ ] No security alerts triggered
- [ ] Authentication working correctly
- [ ] Authorization rules enforced
- [ ] No exposed secrets in logs
- [ ] HTTPS enforced (no HTTP fallback)
- [ ] Security headers present
- [ ] Rate limiting working

### Compliance
- [ ] Audit logs being generated
- [ ] PII handling correct
- [ ] Data encryption at rest verified
- [ ] Data encryption in transit verified

## Alerting and Monitoring Systems

### Alerts
- [ ] No critical alerts firing
- [ ] Expected alerts configured
- [ ] Alert notifications working
- [ ] Alert thresholds appropriate
- [ ] Runbooks accessible

### Monitoring
- [ ] Metrics being collected
- [ ] Dashboards displaying current data
- [ ] Logs being aggregated
- [ ] Traces being collected (if applicable)
- [ ] Synthetic monitoring running

## User Experience

### Frontend
- [ ] UI rendering correctly
- [ ] No console errors
- [ ] Forms submitting correctly
- [ ] Navigation working
- [ ] Mobile view functional
- [ ] Browser compatibility verified

### Customer Reports
- [ ] No customer complaints
- [ ] Support tickets normal volume
- [ ] Social media sentiment normal
- [ ] Status page shows operational

## Rollout Progress (for gradual deployments)

### Canary/Blue-Green
- [ ] Canary metrics comparable to stable
- [ ] No elevated errors in canary
- [ ] Traffic routing as planned
- [ ] Ready to increase traffic percentage
- [ ] Rollback plan still accessible

## Extended Monitoring (1-24 hours)

### First Hour
- [ ] Error rate remains stable
- [ ] Performance metrics stable
- [ ] No memory leaks detected
- [ ] Resource usage predictable
- [ ] No unexpected alerts

### First 4 Hours
- [ ] Business metrics tracking normally
- [ ] User activity patterns normal
- [ ] Background jobs completing
- [ ] Scheduled tasks executing
- [ ] Log volume normal

### First 24 Hours
- [ ] No degradation over time
- [ ] Memory usage stable (no leaks)
- [ ] CPU usage remains consistent
- [ ] No accumulating errors
- [ ] Database performance stable

## Documentation and Communication

### Internal Communication
- [ ] Team notified of successful deployment
- [ ] Deployment summary shared
- [ ] Any issues encountered documented
- [ ] Lessons learned captured
- [ ] Next steps communicated

### External Communication
- [ ] Customers notified (if applicable)
- [ ] Status page updated to operational
- [ ] Release notes published
- [ ] Documentation updated
- [ ] Social media announcement (if applicable)

### Documentation Updates
- [ ] Runbooks updated with learnings
- [ ] Deployment log completed
- [ ] Configuration changes documented
- [ ] Known issues documented
- [ ] Troubleshooting guides updated

## Issue Resolution

### If Issues Detected
- [ ] Severity assessed (critical, high, medium, low)
- [ ] Impact on users quantified
- [ ] Root cause investigation initiated
- [ ] Fix or rollback decision made
- [ ] Stakeholders notified
- [ ] Incident response activated (if severe)

### Rollback Criteria
Initiate rollback if:
- [ ] Error rate > 5% above baseline
- [ ] Response time > 50% above baseline
- [ ] Critical functionality broken
- [ ] Security vulnerability discovered
- [ ] Data corruption detected
- [ ] Service completely down

## Post-Deployment Tasks

### Cleanup
- [ ] Old versions decommissioned (after stability confirmed)
- [ ] Temporary resources removed
- [ ] Feature flags toggled (if applicable)
- [ ] Maintenance mode disabled (if used)
- [ ] Test data cleaned up (staging)

### Optimization
- [ ] Performance bottlenecks identified
- [ ] Resource allocation optimized
- [ ] Cost optimization opportunities noted
- [ ] Monitoring coverage gaps identified
- [ ] Technical debt documented

## Sign-off

### Deployment Verification
- [ ] All critical checks passed
- [ ] No critical issues identified
- [ ] System operating normally
- [ ] Deployment considered successful
- [ ] Extended monitoring plan in place

### Approval
- Verified By: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Date/Time: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Status: ✅ Success / ⚠️ Success with issues / ❌ Rollback required

---

## Deployment Summary

**Deployment Details:**
- Version deployed: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Environment: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Deployment start time: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Deployment end time: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Total duration: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Key Metrics:**
- Error rate: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Response time (p95): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Throughput: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Instance count: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Issues Encountered:**
```
[List any issues, even if resolved]
```

**Action Items:**
```
[List follow-up tasks]
```

---

## Monitoring Schedule

**Immediate (0-1 hour):**
- Check every 5-10 minutes
- Watch dashboards continuously
- Monitor chat for customer reports

**Short-term (1-4 hours):**
- Check every 30 minutes
- Review metrics for trends
- Check error logs periodically

**Medium-term (4-24 hours):**
- Check every 2-4 hours
- Monitor for gradual degradation
- Review daily summary metrics

**Long-term (1-7 days):**
- Daily health checks
- Weekly performance review
- Monitor for memory leaks or slow degradation

---

## Emergency Contacts

**On-Call Engineer:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Team Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**DevOps Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Product Owner:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Escalation Path:**
1. On-call engineer (immediate)
2. Team lead (if unresolved in 15 min)
3. DevOps lead (if rollback needed)
4. Incident commander (if customer-impacting)

---

**Remember:** Continue monitoring for at least 24 hours after deployment. Many issues appear gradually and may not be immediately visible.
