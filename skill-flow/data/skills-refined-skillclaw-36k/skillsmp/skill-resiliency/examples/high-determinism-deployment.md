# High Determinism Example: Production Deployment Skill

This example demonstrates maximum resiliency for a production deployment skill with high determinism requirements.

## Determinism Assessment

**Scores:**
- Output Precision: 9 (exact deployment configuration)
- Process Rigidity: 8 (specific deployment sequence)
- Failure Consequence: 10 (production downtime, revenue loss)
- Recovery Difficulty: 7 (complex rollback procedures)

**Total: 34/40 - High Determinism → Maximum Resiliency**

## Skill Structure

```
deployment-skill/
├── SKILL.md
├── scripts/
│   ├── pre-flight-check.sh
│   ├── deploy.sh
│   ├── verify-deployment.sh
│   ├── rollback.sh
│   └── health-check.sh
├── references/
│   ├── runbook.md
│   └── troubleshooting.md
└── examples/
    └── deployment-checklist.md
```

## SKILL.md (Excerpt)

```markdown
---
name: production-deployment
description: This skill should be used when the user asks to "deploy to production", "release to prod", "production rollout", or discusses production deployments. Implements comprehensive resiliency for zero-downtime deployments.
version: 2.1.0
---

# Production Deployment

## Overview

This skill orchestrates production deployments with maximum resiliency: comprehensive validation, health monitoring, automatic rollback, and detailed audit trails.

## Pre-Deployment Validation

**CRITICAL:** All pre-flight checks must pass before deployment begins.

Run: `scripts/pre-flight-check.sh`

### Pre-Flight Checklist

- [ ] All tests passing in CI/CD
- [ ] Security scan completed (no critical vulnerabilities)
- [ ] Database migrations tested in staging
- [ ] Rollback procedure validated
- [ ] On-call engineer available
- [ ] Change management ticket approved
- [ ] Deployment window confirmed
- [ ] Monitoring dashboards accessible
- [ ] Communication channels ready

**If any check fails, abort deployment.**

## Deployment Procedure

### Phase 1: Snapshot Current State

Create recovery point:

```bash
scripts/create-snapshot.sh production-$(date +%Y%m%d-%H%M%S)
```

**Validation:**
- [ ] Database snapshot created
- [ ] Configuration backup complete
- [ ] Container images tagged
- [ ] Snapshot integrity verified

Proceed only after all validations pass.

### Phase 2: Pre-Deployment Health Check

Verify system is healthy before changes:

```bash
scripts/health-check.sh --phase pre-deployment
```

**Expected Results:**
- All services: status=healthy, response_time < 200ms
- Database: connections < 80% capacity
- Cache: hit_rate > 90%
- Error rate: < 0.1%

**If health check fails:**
Abort deployment. System is not in healthy state for changes.

### Phase 3: Deploy to Canary

Deploy to 5% of production traffic:

```bash
scripts/deploy.sh --target canary --traffic 0.05
```

**Monitor for 10 minutes:**
- Error rate (should remain < 0.1%)
- Response time (should remain within 10% of baseline)
- CPU/Memory (should remain within normal range)

**Automated Monitoring:**
```bash
scripts/monitor-deployment.sh --duration 600 --threshold-error-rate 0.001
```

**If monitoring detects issues:**
- Automatic rollback triggers
- Alerts sent to on-call
- Deployment halted

**Validation:**
- [ ] Canary error rate < baseline + 0.05%
- [ ] Canary response time < baseline × 1.1
- [ ] No critical errors in logs
- [ ] Smoke tests pass

Proceed only after validation passes.

### Phase 4: Gradual Rollout

Roll out to production in stages:

```bash
# 25% traffic
scripts/deploy.sh --target production --traffic 0.25
scripts/monitor-deployment.sh --duration 300 --auto-rollback

# Validation checkpoint
if ! scripts/verify-deployment.sh --traffic-level 0.25; then
    echo "❌ Validation failed at 25% traffic"
    scripts/rollback.sh
    exit 1
fi

# 50% traffic
scripts/deploy.sh --target production --traffic 0.50
scripts/monitor-deployment.sh --duration 300 --auto-rollback

# Validation checkpoint
if ! scripts/verify-deployment.sh --traffic-level 0.50; then
    echo "❌ Validation failed at 50% traffic"
    scripts/rollback.sh
    exit 1
fi

# 100% traffic
scripts/deploy.sh --target production --traffic 1.0
scripts/monitor-deployment.sh --duration 600 --auto-rollback
```

**At each stage, verify:**
- [ ] Error rate remains normal
- [ ] Response time acceptable
- [ ] No database errors
- [ ] Key user journeys functioning

**Automatic Rollback Triggers:**
- Error rate increases > 0.5%
- Response time increases > 50%
- Critical service unavailable
- Database connection failures
- Memory leaks detected (>20% increase)

### Phase 5: Post-Deployment Verification

After 100% rollout, comprehensive verification:

```bash
scripts/verify-deployment.sh --comprehensive
```

**Verification Suite:**

1. **Functional Tests**
   - Critical user journeys
   - API endpoint validation
   - Database query correctness
   - Third-party integrations

2. **Performance Tests**
   - Response times within SLA
   - Throughput meets requirements
   - Resource usage normal
   - Cache behavior correct

3. **Data Integrity Tests**
   - No data corruption
   - Migrations applied correctly
   - Referential integrity maintained
   - Audit logs consistent

4. **Security Tests**
   - Authentication working
   - Authorization rules enforced
   - TLS certificates valid
   - Security headers present

**If any test fails:**
```bash
scripts/rollback.sh --verify
```

### Phase 6: Extended Monitoring

Monitor for 4 hours post-deployment:

```bash
scripts/monitor-deployment.sh --duration 14400 --extended
```

**Extended checks:**
- Background job completion rates
- Scheduled task execution
- Data pipeline health
- External integration status
- Log anomaly detection

## Rollback Procedure

If deployment must be reverted:

### Step 1: Initiate Rollback

```bash
scripts/rollback.sh --confirm
```

**This will:**
1. Route all traffic to previous version
2. Restore database from snapshot (if needed)
3. Revert configuration changes
4. Clear application caches
5. Restart affected services

### Step 2: Verify Rollback

```bash
scripts/verify-rollback.sh
```

**Verification checks:**
- [ ] All services running previous version
- [ ] Traffic routed correctly (0% to new version)
- [ ] Database state correct
- [ ] Configuration matches previous
- [ ] Health checks passing

### Step 3: Post-Rollback Health

```bash
scripts/health-check.sh --phase post-rollback
```

**System must be fully healthy after rollback.**

If rollback verification fails, escalate to incident response team immediately.

## Monitoring and Alerting

**Continuous monitoring during deployment:**

```bash
# Automated alerts configured:
# - Error rate > 0.5% → PagerDuty alert
# - Response time > 500ms → Slack alert
# - Service unavailable → PagerDuty alert + auto-rollback
# - Database errors → PagerDuty alert + deployment pause

# Dashboard:
# https://monitoring.example.com/deployment-live

# Logs:
# https://logs.example.com/deployment-20260107
```

## Post-Deployment

### Document Deployment

Create deployment report:

```bash
scripts/generate-deployment-report.sh > reports/deployment-20260107.md
```

**Report includes:**
- Deployment duration
- Traffic shift timeline
- Health metrics throughout
- Any issues encountered
- Rollback events (if any)
- Final verification results

### Cleanup

Remove canary environment after 24 hours:

```bash
scripts/cleanup-canary.sh --confirm
```

### Retrospective

If issues occurred, conduct retrospective:
- What went wrong?
- What were the warning signs?
- How can we improve detection?
- What validation was missing?

## Emergency Procedures

### Emergency Rollback (System Down)

If system is completely unavailable:

```bash
scripts/emergency-rollback.sh --no-checks
```

This bypasses verification and immediately reverts to last known good state.

**After emergency rollback:**
1. Verify system is operational
2. Notify stakeholders
3. Begin incident investigation
4. Document timeline and impact

### Partial Rollback (Single Service)

If only one service has issues:

```bash
scripts/rollback-service.sh service-name --verify
```

## Audit Trail

All deployment actions are logged:

```bash
# View deployment audit log
cat logs/deployment-audit-20260107.json | jq .

# Example entry:
{
  "timestamp": "2026-01-07T15:30:45Z",
  "action": "deploy",
  "phase": "canary",
  "traffic_level": 0.05,
  "user": "deployer@example.com",
  "commit": "abc123",
  "health_checks": "passed",
  "verification": "passed"
}
```

## Success Criteria

Deployment is complete when:

- [ ] 100% traffic on new version
- [ ] All health checks passing
- [ ] All verification tests passing
- [ ] No elevated error rates
- [ ] Response times within SLA
- [ ] 4-hour monitoring complete with no issues
- [ ] Deployment report generated
- [ ] Canary cleanup scheduled
- [ ] Stakeholders notified

## Additional Resources

- **`references/runbook.md`** - Detailed operational procedures
- **`references/troubleshooting.md`** - Common issues and resolutions
- **`scripts/`** - All automation scripts with inline documentation
```

## Key Resiliency Features

### 1. Comprehensive Pre-Flight Checks

**Script: scripts/pre-flight-check.sh**

```bash
#!/bin/bash
set -e

echo "🔍 Pre-Flight Check - Production Deployment"
echo "=========================================="
echo ""

FAILURES=0

# Check 1: CI/CD Status
echo "Checking CI/CD status..."
CI_STATUS=$(curl -s https://ci.example.com/api/status/latest)
if echo "$CI_STATUS" | jq -e '.tests == "passed"' >/dev/null; then
    echo "  ✅ All tests passing"
else
    echo "  ❌ Tests not passing"
    ((FAILURES++))
fi

# Check 2: Security Scan
echo "Checking security scan..."
SCAN_RESULT=$(curl -s https://security.example.com/api/scan/latest)
CRITICAL_VULNS=$(echo "$SCAN_RESULT" | jq '.critical_count')
if [ "$CRITICAL_VULNS" -eq 0 ]; then
    echo "  ✅ No critical vulnerabilities"
else
    echo "  ❌ $CRITICAL_VULNS critical vulnerabilities found"
    ((FAILURES++))
fi

# Check 3: Staging Validation
echo "Checking staging validation..."
if [ -f ".staging-validated" ]; then
    VALIDATED_COMMIT=$(cat .staging-validated)
    CURRENT_COMMIT=$(git rev-parse HEAD)
    if [ "$VALIDATED_COMMIT" == "$CURRENT_COMMIT" ]; then
        echo "  ✅ Current commit validated in staging"
    else
        echo "  ❌ Current commit not validated in staging"
        ((FAILURES++))
    fi
else
    echo "  ❌ No staging validation found"
    ((FAILURES++))
fi

# Check 4: Change Management
echo "Checking change management..."
if [ -n "$CHANGE_TICKET" ]; then
    TICKET_STATUS=$(curl -s "https://cm.example.com/api/ticket/$CHANGE_TICKET")
    if echo "$TICKET_STATUS" | jq -e '.status == "approved"' >/dev/null; then
        echo "  ✅ Change ticket approved"
    else
        echo "  ❌ Change ticket not approved"
        ((FAILURES++))
    fi
else
    echo "  ❌ No change ticket specified"
    ((FAILURES++))
fi

# Check 5: On-Call Engineer
echo "Checking on-call availability..."
ONCALL=$(curl -s https://pagerduty.example.com/api/oncall/current)
if echo "$ONCALL" | jq -e '.available == true' >/dev/null; then
    echo "  ✅ On-call engineer available"
else
    echo "  ❌ No on-call engineer available"
    ((FAILURES++))
fi

# Check 6: Deployment Window
echo "Checking deployment window..."
CURRENT_HOUR=$(date +%H)
CURRENT_DAY=$(date +%u)
if [ "$CURRENT_DAY" -le 4 ] && [ "$CURRENT_HOUR" -ge 10 ] && [ "$CURRENT_HOUR" -le 16 ]; then
    echo "  ✅ Within approved deployment window"
else
    echo "  ⚠️  Outside normal deployment window (requires exception)"
    if [ -z "$DEPLOYMENT_EXCEPTION" ]; then
        echo "     Set DEPLOYMENT_EXCEPTION=approved to override"
        ((FAILURES++))
    fi
fi

# Check 7: Monitoring Systems
echo "Checking monitoring systems..."
if curl -s -f https://monitoring.example.com/health >/dev/null 2>&1; then
    echo "  ✅ Monitoring systems accessible"
else
    echo "  ❌ Monitoring systems unreachable"
    ((FAILURES++))
fi

# Summary
echo ""
echo "=========================================="
if [ $FAILURES -eq 0 ]; then
    echo "✅ All pre-flight checks passed"
    echo "   Deployment may proceed"
    exit 0
else
    echo "❌ $FAILURES pre-flight check(s) failed"
    echo "   Deployment BLOCKED"
    exit 1
fi
```

### 2. Gradual Rollout with Automatic Rollback

The deployment proceeds in stages (5% → 25% → 50% → 100%), with comprehensive validation at each stage. If any metric exceeds thresholds, automatic rollback triggers immediately.

### 3. Multi-Level Validation

- **Pre-deployment:** System health, prerequisites
- **During deployment:** Real-time metrics monitoring
- **Post-deployment:** Comprehensive functional, performance, and security tests
- **Extended monitoring:** 4-hour observation period

### 4. Verified Rollback Procedures

Rollback isn't just documentation—it's tested, automated, and verified to work correctly.

### 5. Complete Audit Trail

Every action is logged with full context for compliance and debugging.

## Why This Level of Resiliency?

**Determinism Score: 34/40 (High)**

- **Output Precision (9):** Exact deployment configuration must match specification
- **Process Rigidity (8):** Specific sequence required for zero-downtime deployment
- **Failure Consequence (10):** Production downtime = revenue loss, reputation damage, SLA violations
- **Recovery Difficulty (7):** Complex rollback with database state management

**Therefore:** Maximum resiliency is justified and required. The investment in comprehensive validation, monitoring, and recovery procedures is proportional to the risk.

## Resiliency ROI

**Without Resiliency:**
- 1 in 10 deployments causes production incident
- Average incident duration: 2 hours
- Cost per incident: $50,000 (revenue + eng time)
- Annual cost: $500,000 (assuming 100 deployments/year)

**With Resiliency:**
- Failed deployments caught in canary phase (5% traffic impact)
- Average rollback time: 5 minutes
- Cost per failed deployment: $1,000
- Annual cost: $10,000 + $30,000 (resiliency investment) = $40,000

**Net benefit: $460,000/year**

---

**Key Takeaway:** High determinism + high consequences = maximum resiliency investment is clearly justified.
