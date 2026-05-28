# Rollback Plan Template

**Document ID:** P7-ROLLBACK-{XXX}  
  
**Release:** {X.Y.Z}  
**Author:** {DevOps Lead}  

---

## 1. Rollback Overview

### 1.1 Purpose
This document provides step-by-step instructions to rollback release {X.Y.Z} to the previous stable version {X.Y.Z-1} in case of critical issues.

### 1.2 Rollback Scope

| Component | Current Version | Rollback Version |
|-----------|-----------------|------------------|
| Application | {X.Y.Z} | {X.Y.Z-1} |
| Database | Migration {N} | Migration {N-1} |
| Configuration | Config v{X} | Config v{X-1} |

---

## 2. Rollback Decision Criteria

### 2.1 Automatic Rollback Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Error Rate | > 10% for 5 min | Auto-rollback |
| P99 Latency | > 5s for 5 min | Auto-rollback |
| Health Check Failures | > 3 consecutive | Auto-rollback |

### 2.2 Manual Rollback Triggers

| Condition | Decision Maker |
|-----------|----------------|
| Critical bug affecting > 10% users | Deployment Lead |
| Security vulnerability | Security Lead |
| Data corruption | DBA + Dev Lead |
| Customer escalation | Product Owner |

---

## 3. Pre-Rollback Checklist

- [ ] Document the issue triggering rollback
- [ ] Notify stakeholders of rollback decision
- [ ] Verify rollback artifacts exist (images, backups)
- [ ] Ensure rollback team is available
- [ ] Enable maintenance mode (if needed)

---

## 4. Rollback Steps

### 4.1 Application Rollback

```bash
# Step 1: Scale down new deployment
kubectl scale deployment api-server --replicas=0 -n production

# Step 2: Verify pods terminated
kubectl get pods -n production -l app=api-server

# Step 3: Rollback to previous version
kubectl rollout undo deployment/api-server -n production

# Step 4: Verify rollback
kubectl rollout status deployment/api-server -n production

# Step 5: Verify correct version running
kubectl get deployment api-server -n production -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### 4.2 Database Rollback

```bash
# Step 1: Create point-in-time backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > pre_rollback_backup.sql

# Step 2: Run rollback migrations
./migrate.sh down --env production --to-version {target_version}

# Step 3: Verify schema
./migrate.sh status --env production

# Step 4: Validate data integrity
./scripts/validate-data.sh
```

### 4.3 Configuration Rollback

```bash
# Step 1: Restore previous configuration
vault kv rollback -version={X-1} secret/production/app-config

# Step 2: Restart services to pick up new config
kubectl rollout restart deployment/api-server -n production

# Step 3: Verify configuration
kubectl exec -it {pod-name} -n production -- env | grep APP_
```

---

## 5. Post-Rollback Verification

### 5.1 Smoke Tests

| Test | Command | Expected |
|------|---------|----------|
| Health Check | curl /health | 200 OK |
| Version Check | curl /version | {X.Y.Z-1} |
| Login | POST /auth/login | 200 + token |
| Core Function | GET /api/products | 200 + data |

### 5.2 Monitoring Checks

| Metric | Expected After Rollback |
|--------|-------------------------|
| Error Rate | < 1% |
| Latency (p95) | < 500ms |
| CPU Usage | < 70% |
| Memory | < 80% |

---

## 6. Communication

### 6.1 Notification Template

**Subject:** [ROLLBACK] {Service} rolled back from {X.Y.Z} to {X.Y.Z-1}

**Body:**
```
Team,

We have initiated a rollback of {Service} from version {X.Y.Z} to {X.Y.Z-1}.

Reason: {Brief description of issue}

Timeline:
- Issue detected: {Time}
- Rollback started: {Time}
- Rollback completed: {Time}

Impact:
- {Description of user impact}

Next Steps:
- {Action item 1}
- {Action item 2}

Post-mortem scheduled for: {Date/Time}

Please contact {name} for questions.
```

---

## 7. Post-Rollback Actions

- [ ] Complete incident report
- [ ] Schedule post-mortem meeting
- [ ] Document root cause
- [ ] Create tickets for fixes
- [ ] Update deployment procedures if needed

---

## 8. Emergency Contacts

| Role | Name | Phone | Availability |
|------|------|-------|--------------|
| DevOps Lead | {Name} | {Phone} | 24/7 |
| DBA | {Name} | {Phone} | 24/7 |
| Dev Lead | {Name} | {Phone} | Business hours |
| Escalation | {Name} | {Phone} | Critical only |

---

## 9. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| DevOps Lead | | | |
| Dev Lead | | | |

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
