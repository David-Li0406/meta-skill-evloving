# Runbook Template

Use this template to create operational runbooks for production services.

---

## Service: [SERVICE NAME]

**Owner:** [Team/Person]
**Last Updated:** [Date]
**Version:** [Version]

---

## 1. Service Overview

### Description
[Brief description of what this service does]

### Dependencies
| Dependency | Type | Required | Fallback |
|------------|------|----------|----------|
| [Database] | PostgreSQL | Yes | None |
| [Cache] | Redis | No | Bypass cache |
| [External API] | REST | Yes | Return error |

### SLOs
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Availability | 99.9% | <99.5% |
| p99 Latency | <500ms | >1000ms |
| Error Rate | <0.1% | >1% |

---

## 2. Access & Tools

### Dashboards
- Grafana: [URL]
- Datadog: [URL]
- Custom: [URL]

### Logs
```bash
# View recent logs
kubectl logs -f deployment/[service-name] -n [namespace]

# Search logs in [logging system]
[logging query]
```

### Shell Access
```bash
# Get shell in container
kubectl exec -it deployment/[service-name] -n [namespace] -- /bin/sh

# Port forward for local debugging
kubectl port-forward deployment/[service-name] 8080:8080
```

---

## 3. Common Operations

### 3.1 Restart Service

**When to use:** Service is unresponsive, memory leak suspected

```bash
# Graceful restart (rolling)
kubectl rollout restart deployment/[service-name] -n [namespace]

# Verify restart
kubectl rollout status deployment/[service-name] -n [namespace]
```

**Expected outcome:** Pods restart one by one, no downtime
**Estimated time:** 2-5 minutes

---

### 3.2 Scale Service

**When to use:** High load, need more capacity

```bash
# Scale up
kubectl scale deployment/[service-name] --replicas=5 -n [namespace]

# Verify scaling
kubectl get pods -l app=[service-name] -n [namespace]
```

**Expected outcome:** Additional pods start, load distributed
**Estimated time:** 1-2 minutes

---

### 3.3 Rollback Deployment

**When to use:** New deployment causing issues

```bash
# View rollout history
kubectl rollout history deployment/[service-name] -n [namespace]

# Rollback to previous version
kubectl rollout undo deployment/[service-name] -n [namespace]

# Rollback to specific revision
kubectl rollout undo deployment/[service-name] --to-revision=2 -n [namespace]

# Verify rollback
kubectl rollout status deployment/[service-name] -n [namespace]
```

**Expected outcome:** Previous version deployed
**Estimated time:** 2-5 minutes

---

### 3.4 Clear Cache

**When to use:** Stale data, cache corruption suspected

```bash
# Connect to Redis
redis-cli -h [redis-host] -p 6379

# Clear specific keys
DEL [key-pattern]*

# Clear all (DANGEROUS - affects all services!)
# FLUSHALL
```

**Expected outcome:** Cache miss on next requests, fresh data loaded
**Estimated time:** Immediate

---

### 3.5 Database Operations

**When to use:** Need to run migrations or queries

```bash
# Connect to database
psql -h [db-host] -U [user] -d [database]

# Run pending migrations
npm run migrate

# Check migration status
npm run migrate:status
```

**Warning:** Always take backup before schema changes

---

## 4. Incident Response

### 4.1 Service Down

**Symptoms:** Health checks failing, 5xx errors, no logs

**Immediate actions:**
1. Check pod status: `kubectl get pods -l app=[service-name]`
2. Check recent events: `kubectl describe pod [pod-name]`
3. Check logs: `kubectl logs [pod-name] --previous`
4. If OOMKilled: Increase memory limits or investigate leak
5. If CrashLoopBackOff: Check startup dependencies

**Escalation:** If not resolved in 15 minutes, escalate to [Team Lead]

---

### 4.2 High Error Rate

**Symptoms:** Error rate >1%, customer complaints

**Immediate actions:**
1. Check error logs for patterns
2. Check dependency health (DB, cache, external APIs)
3. Check recent deployments: `kubectl rollout history`
4. If caused by deploy: Rollback immediately
5. If external dependency: Enable fallback/circuit breaker

**Escalation:** If customer-impacting for >5 minutes, escalate to [On-call]

---

### 4.3 High Latency

**Symptoms:** p99 >1s, timeouts reported

**Immediate actions:**
1. Check database slow queries
2. Check external API latency
3. Check pod resource usage (CPU/memory)
4. If DB: Check for missing indexes, long transactions
5. If external: Check circuit breaker status

**Escalation:** If SLO breach >10 minutes, escalate to [Team Lead]

---

### 4.4 Data Inconsistency

**Symptoms:** Wrong data displayed, calculation errors

**Immediate actions:**
1. DO NOT make manual data changes without review
2. Identify affected records
3. Check recent deployments and migrations
4. Check for race conditions in logs
5. If critical: Consider feature flag to disable affected flow

**Escalation:** Always escalate data issues to [Data Team Lead]

---

## 5. Maintenance Procedures

### 5.1 Scheduled Maintenance

**Pre-maintenance:**
1. Notify stakeholders 24h in advance
2. Verify backup exists
3. Prepare rollback procedure
4. Schedule during low-traffic window

**During maintenance:**
1. Enable maintenance mode (if applicable)
2. Perform changes
3. Verify health checks
4. Run smoke tests

**Post-maintenance:**
1. Monitor for 30 minutes
2. Notify stakeholders of completion
3. Document any issues encountered

---

### 5.2 Database Migration

**Pre-migration:**
1. Take database backup
2. Test migration on staging with production data copy
3. Estimate migration time
4. Plan rollback

**During migration:**
```bash
# Run migration
npm run migrate

# Verify migration
npm run migrate:status
```

**Post-migration:**
1. Verify application health
2. Run data validation queries
3. Monitor for errors

---

## 6. Contacts & Escalation

### On-Call
- Primary: [Name] - [Phone/Slack]
- Secondary: [Name] - [Phone/Slack]

### Escalation Path
| Level | Contact | When |
|-------|---------|------|
| L1 | On-call engineer | First responder |
| L2 | Team Lead | >15 min unresolved |
| L3 | Engineering Manager | Customer impact >30 min |
| L4 | VP Engineering | Major incident |

### External Vendors
| Vendor | Support | SLA |
|--------|---------|-----|
| [Cloud Provider] | [support URL] | 24/7 |
| [Database] | [support URL] | Business hours |

---

## 7. Change Log

| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | [Name] | Initial version |
| YYYY-MM-DD | [Name] | Added scaling procedure |
