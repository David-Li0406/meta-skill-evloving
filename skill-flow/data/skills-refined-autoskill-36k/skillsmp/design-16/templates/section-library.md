# PRP Section Library

> Reusable PRP sections for common scenarios. Copy and customize as needed.

---

## How to Use This Library

1. **Find the relevant section** for your project type
2. **Copy the section** into your PRP
3. **Customize the variables** and specifics
4. **Remove irrelevant parts** - not every project needs every section

Each section includes:
- **When to use it**: Scenarios where this section applies
- **The section itself**: Ready to copy
- **Customization guide**: What to change
- **Common gotchas**: Mistakes to avoid

---

## Database Migration Sections

### When to Use
- Moving between database systems (PostgreSQL → Aurora, MySQL → PostgreSQL)
- Major version upgrades with schema changes
- Database consolidation or splitting
- Moving from on-prem to cloud

---

### Section: Data Validation Gates

```markdown
## Data Validation Gates

### Pre-Migration Baseline

| Table | Row Count | Checksum | Last Updated |
|-------|-----------|----------|--------------|
| {{TABLE_1}} | {{COUNT_1}} | {{CHECKSUM_1}} | {{DATE_1}} |
| {{TABLE_2}} | {{COUNT_2}} | {{CHECKSUM_2}} | {{DATE_2}} |

### Validation Queries

```sql
-- Row count validation (run on both source and target)
SELECT 'source' as db, count(*) FROM {{TABLE_NAME}};

-- Checksum validation for critical tables
SELECT md5(array_agg(md5(row::text))::text) as checksum
FROM (SELECT * FROM {{TABLE_NAME}} ORDER BY {{PRIMARY_KEY}}) row;

-- Foreign key integrity
SELECT count(*) FROM {{CHILD_TABLE}} c
LEFT JOIN {{PARENT_TABLE}} p ON c.{{FK_COLUMN}} = p.id
WHERE p.id IS NULL;
```

### Validation Gates

| Gate | Criterion | Pass Condition |
|------|-----------|----------------|
| Row Count | source_count = target_count | Exact match |
| Checksums | All critical tables match | 100% |
| FK Integrity | Orphan count = 0 | Zero orphans |
| Index Count | Indexes match | All recreated |

### Continuous Validation (CDC Phase)

```
VALIDATION_FREQUENCY: every 1_hour
VALIDATION_TABLES: {{CRITICAL_TABLES}}
ALERT_IF: checksum_mismatch OR row_count_delta > {{THRESHOLD}}
```
```

#### Customization Guide
- Replace `{{TABLE_*}}` with your actual tables
- Adjust checksum query for your database (PostgreSQL shown)
- For large tables, sample-based validation may be needed
- Add application-specific integrity checks

#### Common Gotchas
- Floating point columns may have precision differences
- Timestamp columns may have timezone issues
- BLOB/binary columns need special checksum handling
- Sequences/auto-increment values may differ

---

### Section: Replication Lag Monitoring

```markdown
## Replication Lag Monitoring

### Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Replication lag | >5s | >30s | Pause cutover |
| CDC throughput | <1000 rows/s | <100 rows/s | Scale DMS |
| Target disk | >70% | >85% | Expand storage |

### Monitoring Queries

```sql
-- Aurora replication lag
SELECT server_id, replica_lag_in_msec
FROM aurora_replica_status();

-- DMS task status
aws dms describe-replication-tasks \
  --filters Name=replication-task-arn,Values={{TASK_ARN}}
```

### Alerting Configuration

```yaml
alerts:
  - name: replication_lag_warning
    condition: replication_lag_seconds > 5
    for: 2m
    severity: warning
    notify: slack-data-platform

  - name: replication_lag_critical
    condition: replication_lag_seconds > 30
    for: 1m
    severity: critical
    notify: pagerduty-dba
```

### Recovery Procedures

```
IF lag > 30s for 5_minutes:
  1. Check DMS task status
  2. Check source database load
  3. Check network throughput
  4. Scale DMS instance if needed
  5. If unrecoverable: restart from checkpoint
```
```

#### Customization Guide
- Adjust thresholds based on your RPO requirements
- Add database-specific lag queries
- Configure alerts for your monitoring system

#### Common Gotchas
- Lag can spike during bulk operations on source
- Network bandwidth can be a bottleneck
- DMS instance size affects throughput
- Some operations (DDL) may require task restart

---

## API Integration Sections

### When to Use
- Third-party API integrations
- Internal service-to-service calls
- Payment gateway integrations
- Data provider connections

---

### Section: API Circuit Breakers

```markdown
## API Circuit Breakers

### Circuit Breaker Configuration

| Endpoint | Failure Threshold | Recovery Timeout | Fallback |
|----------|-------------------|------------------|----------|
| {{ENDPOINT_1}} | 5 failures in 30s | 60s | {{FALLBACK_1}} |
| {{ENDPOINT_2}} | 3 failures in 60s | 120s | {{FALLBACK_2}} |

### States

```
CIRCUIT_STATE:
  CLOSED → OPEN       [on: failure_count >= threshold]
  OPEN → HALF_OPEN    [on: recovery_timeout_elapsed]
  HALF_OPEN → CLOSED  [on: probe_request_succeeded]
  HALF_OPEN → OPEN    [on: probe_request_failed]
```

### Implementation

```javascript
const circuitBreaker = {
  state: 'CLOSED',
  failures: 0,
  lastFailure: null,

  call: async (fn) => {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > RECOVERY_TIMEOUT) {
        this.state = 'HALF_OPEN';
      } else {
        return this.fallback();
      }
    }

    try {
      const result = await fn();
      if (this.state === 'HALF_OPEN') this.state = 'CLOSED';
      this.failures = 0;
      return result;
    } catch (error) {
      this.failures++;
      this.lastFailure = Date.now();
      if (this.failures >= FAILURE_THRESHOLD) {
        this.state = 'OPEN';
      }
      return this.fallback();
    }
  }
};
```

### Monitoring

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| Circuit open events | >3 in 1 hour | Investigate API health |
| Fallback usage | >10% of calls | Review integration |
| Recovery failures | >2 consecutive | Manual intervention |
```

#### Customization Guide
- Set thresholds based on API SLA and your tolerance
- Implement fallbacks appropriate to your use case
- Add specific error types that should trigger the breaker

#### Common Gotchas
- Timeouts should count as failures
- Don't circuit-break on 4xx client errors
- Test fallback behavior regularly
- Log all circuit state changes

---

### Section: API Rate Limiting

```markdown
## API Rate Limiting

### Provider Limits

| API | Rate Limit | Burst | Reset Window |
|-----|------------|-------|--------------|
| {{PROVIDER_1}} | {{LIMIT_1}}/min | {{BURST_1}} | 60s |
| {{PROVIDER_2}} | {{LIMIT_2}}/day | N/A | 24h |

### Internal Throttling

```
RATE_LIMITER:
  algorithm: token_bucket
  capacity: {{BURST_LIMIT}}
  refill_rate: {{SUSTAINED_RATE}}/second

  on_limit_exceeded:
    action: queue_with_backoff
    max_queue_size: 1000
    max_wait: 30s
```

### Backoff Strategy

```
BACKOFF:
  initial_delay: 1s
  max_delay: 60s
  multiplier: 2
  jitter: 0.1  # 10% random jitter

  retry_on: [429, 503, 504]
  max_retries: 5
```

### Budget Tracking

| Period | Budget | Alert At | Hard Stop |
|--------|--------|----------|-----------|
| Hourly | {{HOURLY_BUDGET}} | 80% | 95% |
| Daily | {{DAILY_BUDGET}} | 70% | 90% |
| Monthly | {{MONTHLY_BUDGET}} | 60% | 85% |

### Monitoring

```yaml
alerts:
  - name: rate_limit_approaching
    condition: api_calls_remaining < 20%
    notify: slack-integrations

  - name: rate_limit_exceeded
    condition: 429_responses > 0
    notify: pagerduty-oncall
```
```

#### Customization Guide
- Get actual limits from provider documentation
- Set internal limits below provider limits (safety margin)
- Implement request prioritization if needed

#### Common Gotchas
- Rate limits may be per-endpoint, not global
- Some APIs count failed requests against limits
- Concurrent requests can exceed burst limits
- Clock skew can cause reset window issues

---

## User Testing Sections

### When to Use
- Consumer-facing features
- UX changes
- Accessibility updates
- Onboarding flows

---

### Section: User Testing Protocol

```markdown
## User Testing Protocol

### Recruitment Criteria

| Segment | Count | Criteria | Incentive |
|---------|-------|----------|-----------|
| {{SEGMENT_1}} | {{COUNT_1}} | {{CRITERIA_1}} | {{INCENTIVE_1}} |
| {{SEGMENT_2}} | {{COUNT_2}} | {{CRITERIA_2}} | {{INCENTIVE_2}} |

### Test Script

**Introduction** (2 min)
- Thank participant
- Explain think-aloud protocol
- Confirm recording consent

**Tasks** (20 min)

| Task | Success Criteria | Time Limit |
|------|------------------|------------|
| {{TASK_1}} | {{SUCCESS_1}} | {{TIME_1}} |
| {{TASK_2}} | {{SUCCESS_2}} | {{TIME_2}} |
| {{TASK_3}} | {{SUCCESS_3}} | {{TIME_3}} |

**Debrief** (5 min)
- Overall impressions
- Comparison to current experience
- Suggestions for improvement

### Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task completion rate | >85% | Tasks completed / Tasks attempted |
| Time on task | <{{TARGET_TIME}} | Stopwatch |
| Error rate | <10% | Errors / Attempts |
| SUS score | >70 | System Usability Scale |
| NPS | >40 | Post-test survey |

### Go/No-Go Criteria

```
PROCEED_TO_DEVELOPMENT := ALL(
  task_completion_rate > 0.85,
  critical_issues = 0,
  sus_score > 70
)
```
```

#### Customization Guide
- Tailor tasks to your specific feature
- Adjust sample size based on confidence needed
- Include accessibility testing if relevant

#### Common Gotchas
- Avoid leading questions
- Recruit outside your company/friends
- Test on realistic devices
- Record sessions for team review

---

### Section: A/B Test Configuration

```markdown
## A/B Test Configuration

### Experiment Setup

```yaml
experiment:
  name: {{EXPERIMENT_NAME}}
  hypothesis: {{HYPOTHESIS}}

  variants:
    control:
      allocation: 50%
      description: Current experience
    treatment:
      allocation: 50%
      description: {{TREATMENT_DESCRIPTION}}

  targeting:
    include: {{INCLUDE_CRITERIA}}
    exclude: {{EXCLUDE_CRITERIA}}

  duration:
    minimum: 14 days
    maximum: 30 days
```

### Primary Metric

| Metric | Baseline | MDE | Sample Size |
|--------|----------|-----|-------------|
| {{PRIMARY_METRIC}} | {{BASELINE}} | {{MDE}}% | {{SAMPLE_SIZE}} |

### Guardrail Metrics

| Metric | Must Not Decrease By |
|--------|---------------------|
| {{GUARDRAIL_1}} | {{THRESHOLD_1}}% |
| {{GUARDRAIL_2}} | {{THRESHOLD_2}}% |

### Decision Framework

```
IF primary_metric_lift > MDE AND guardrails_pass:
  SHIP treatment
ELSE IF primary_metric_lift < -MDE:
  KEEP control
ELSE:
  EXTEND experiment OR re-evaluate hypothesis
```

### Early Stopping Rules

```
STOP_EARLY_IF:
  - guardrail_degradation > 5% (p < 0.01)
  - error_rate_increase > 2x
  - revenue_impact < -${{THRESHOLD}}/day
```
```

#### Customization Guide
- Calculate sample size based on your baseline and MDE
- Choose guardrails that protect user experience
- Set appropriate early stopping thresholds

#### Common Gotchas
- Don't peek at results before reaching sample size
- Account for novelty effects
- Watch for interaction with other experiments
- Consider day-of-week effects

---

## Documentation Sections

### When to Use
- Any project with external handoff
- Operations runbooks needed
- API documentation required
- User-facing help content

---

### Section: Runbook Template

```markdown
## Operations Runbook

### Service Overview

| Property | Value |
|----------|-------|
| Service Name | {{SERVICE_NAME}} |
| Team | {{TEAM}} |
| On-Call | {{ONCALL_ROTATION}} |
| Dashboard | {{DASHBOARD_URL}} |
| Logs | {{LOG_URL}} |

### Alert Response

#### {{ALERT_NAME_1}}

**Severity**: {{SEVERITY}}
**Description**: {{DESCRIPTION}}

**Triage Steps**:
1. Check {{METRIC_1}} on dashboard
2. Review recent deployments
3. Check dependent service health

**Resolution Steps**:
```bash
# Step 1: {{DESCRIPTION}}
{{COMMAND_1}}

# Step 2: {{DESCRIPTION}}
{{COMMAND_2}}
```

**Escalation**:
- If not resolved in {{TIME}}: Page {{ESCALATION_TARGET}}

---

### Common Operations

#### Restart Service

```bash
# Graceful restart
kubectl rollout restart deployment/{{SERVICE_NAME}}

# Verify
kubectl get pods -l app={{SERVICE_NAME}} -w
```

#### Scale Service

```bash
# Scale up
kubectl scale deployment/{{SERVICE_NAME}} --replicas={{N}}

# Verify
kubectl get hpa {{SERVICE_NAME}}
```

#### Check Logs

```bash
# Recent errors
kubectl logs -l app={{SERVICE_NAME}} --since=1h | grep ERROR

# Follow logs
kubectl logs -f -l app={{SERVICE_NAME}}
```

### Rollback Procedure

```bash
# 1. Identify previous version
kubectl rollout history deployment/{{SERVICE_NAME}}

# 2. Rollback
kubectl rollout undo deployment/{{SERVICE_NAME}}

# 3. Verify
kubectl rollout status deployment/{{SERVICE_NAME}}
```
```

#### Customization Guide
- Add all alerts that page on-call
- Include actual commands, not placeholders
- Test all commands before documenting

#### Common Gotchas
- Keep runbooks in version control
- Update after every incident
- Include "who to call" for edge cases
- Test rollback procedure regularly

---

## Deployment Sections

### When to Use
- Any code deployment
- Infrastructure changes
- Configuration updates
- Feature flag changes

---

### Section: Staged Rollout Plan

```markdown
## Staged Rollout Plan

### Rollout Stages

| Stage | % Traffic | Duration | Success Criteria |
|-------|-----------|----------|------------------|
| Canary | 1% | 1 hour | Error rate <0.1% |
| Early Adopters | 10% | 24 hours | Error rate <0.5%, latency stable |
| Wider | 50% | 48 hours | All metrics stable |
| Full | 100% | — | — |

### Feature Flag Configuration

```yaml
feature_flag:
  name: {{FEATURE_NAME}}
  type: percentage_rollout

  stages:
    - name: canary
      percentage: 1
      targeting:
        include: [internal_users]

    - name: early_adopters
      percentage: 10
      targeting:
        include: [beta_program]

    - name: wider
      percentage: 50

    - name: full
      percentage: 100
```

### Promotion Criteria

```
PROMOTE_TO_NEXT_STAGE := ALL(
  error_rate < threshold_for_stage,
  latency_p99 < baseline * 1.1,
  no_critical_bugs_reported,
  minimum_duration_elapsed
)
```

### Rollback Triggers

| Condition | Action | Recovery |
|-----------|--------|----------|
| Error rate >1% | Immediate rollback | Disable flag |
| P1 bug reported | Pause rollout | Investigate |
| Performance degradation >20% | Rollback to previous stage | Analyze |

### Rollback Commands

```bash
# Immediate rollback
launchdarkly toggle {{FEATURE_NAME}} off

# Partial rollback (to previous stage)
launchdarkly set-percentage {{FEATURE_NAME}} {{PREVIOUS_PERCENTAGE}}

# Verify
launchdarkly get-flag {{FEATURE_NAME}}
```
```

#### Customization Guide
- Adjust percentages based on user base size
- Set stage durations based on metric collection needs
- Add targeting rules for specific user segments

#### Common Gotchas
- Monitor for both direct and downstream effects
- Consider time zones for percentage rollout
- Have rollback tested before starting
- Communicate rollback to stakeholders

---

### Section: Deployment Checklist

```markdown
## Pre-Deployment Checklist

### Code Ready
- [ ] All tests passing in CI
- [ ] Code review approved
- [ ] Security scan passed
- [ ] Performance benchmarks acceptable

### Documentation
- [ ] CHANGELOG updated
- [ ] API docs updated (if applicable)
- [ ] Runbook updated (if applicable)
- [ ] Migration notes written (if applicable)

### Infrastructure
- [ ] Database migrations tested
- [ ] Feature flags configured
- [ ] Monitoring dashboards ready
- [ ] Alerts configured

### Communication
- [ ] Team notified of deployment window
- [ ] On-call aware
- [ ] Stakeholders informed (if user-facing)

### Rollback Ready
- [ ] Rollback procedure documented
- [ ] Previous version tagged
- [ ] Database rollback script ready (if applicable)
- [ ] Feature flag kill switch tested

## Post-Deployment Checklist

### Immediate (0-15 min)
- [ ] Deployment successful (no errors)
- [ ] Health checks passing
- [ ] Key metrics stable

### Short-term (15-60 min)
- [ ] Error rates normal
- [ ] Latency within bounds
- [ ] No user complaints

### Next Day
- [ ] Full metrics review
- [ ] Deployment log completed
- [ ] Lessons learned documented
```

#### Customization Guide
- Add project-specific checks
- Include stakeholder sign-offs if required
- Automate what can be automated

#### Common Gotchas
- Don't deploy on Fridays (or before holidays)
- Have the right people available during deploy
- Don't rush the checklist
- Keep evidence of checks for audit

---

## Quick Reference: Section Selection

| Project Type | Recommended Sections |
|--------------|---------------------|
| API Integration | Circuit Breakers, Rate Limiting, Staged Rollout |
| Database Migration | Data Validation, Replication Monitoring, Rollback |
| User Feature | User Testing, A/B Test, Staged Rollout |
| Infrastructure | Runbook, Deployment Checklist, Staged Rollout |
| Any Project | Deployment Checklist, Runbook |

---

*Section Library v1.0 - Add new sections as patterns emerge*
