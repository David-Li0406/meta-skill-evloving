# Runbook Template

**Document ID:** P8-RUN-{XXX}  
  
**Service:** {Service Name}  
**Author:** {SRE Lead}  

---

## 1. Service Overview

### 1.1 Service Information

| Field | Value |
|-------|-------|
| Service Name | {Service Name} |
| Description | {Brief description} |
| Team | {Owning team} |
| Criticality | {Critical/High/Medium/Low} |
| SLA | {99.9%/99.99%/etc.} |

### 1.2 Architecture Diagram

```
[Load Balancer] → [App Servers (x3)] → [Database (Primary)]
                                            ↓
                                    [Database (Replica)]
```

### 1.3 Dependencies

| Dependency | Type | Impact if Down |
|------------|------|----------------|
| {Service A} | Upstream | Complete outage |
| {Service B} | Downstream | Partial degradation |
| {Database} | Data store | Complete outage |

---

## 2. Key Contacts

| Role | Name | Contact | Escalation Order |
|------|------|---------|------------------|
| Primary On-Call | Rotation | PagerDuty | 1 |
| Team Lead | {Name} | {Contact} | 2 |
| Manager | {Name} | {Contact} | 3 |

---

## 3. Access Information

### 3.1 System Access

| System | Access Method | Credentials |
|--------|---------------|-------------|
| Production Servers | SSH via Bastion | SSO + SSH Key |
| Database | psql via Bastion | Vault secret |
| Dashboards | Web | SSO |
| Logs | Kibana | SSO |

### 3.2 Important URLs

| Resource | URL |
|----------|-----|
| Production | https://app.example.com |
| Staging | https://staging.example.com |
| Metrics Dashboard | {Grafana URL} |
| Logs | {Kibana URL} |
| Alerts | {PagerDuty URL} |

---

## 4. Monitoring & Alerting

### 4.1 Key Metrics

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Request Rate | 100-500/s | > 800/s | > 1000/s |
| Error Rate | < 0.1% | > 1% | > 5% |
| Latency (p95) | < 200ms | > 500ms | > 1s |
| CPU Usage | < 60% | > 70% | > 85% |
| Memory | < 70% | > 80% | > 90% |

### 4.2 Alerts

| Alert | Severity | Response |
|-------|----------|----------|
| High Error Rate | P1 | Immediate investigation |
| Service Down | P1 | Immediate response |
| High Latency | P2 | Investigate within 15 min |
| High CPU | P3 | Investigate within 1 hour |

---

## 5. Common Procedures

### 5.1 Service Restart

**When to use:** Service unresponsive or memory leak

```bash
# Check current status
kubectl get pods -n production -l app=api-server

# Restart service (rolling)
kubectl rollout restart deployment/api-server -n production

# Watch rollout
kubectl rollout status deployment/api-server -n production

# Verify health
curl -s https://app.example.com/health | jq .
```

### 5.2 Scale Service

**When to use:** High load or traffic spike

```bash
# Current scale
kubectl get deployment api-server -n production

# Scale up
kubectl scale deployment api-server --replicas=10 -n production

# Verify scaling
kubectl get pods -n production -l app=api-server
```

### 5.3 Check Logs

```bash
# Recent logs
kubectl logs -f deployment/api-server -n production --tail=100

# Logs from all pods
kubectl logs -f -l app=api-server -n production

# Search for errors
kubectl logs deployment/api-server -n production | grep -i error

# Kibana query
service:api-server AND level:error AND @timestamp:[now-1h TO now]
```

### 5.4 Database Connection Issues

```bash
# Check connection count
psql -h $DB_HOST -U $DB_USER -c "SELECT count(*) FROM pg_stat_activity;"

# Kill idle connections
psql -h $DB_HOST -U $DB_USER -c "
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' 
AND state_change < now() - interval '10 minutes';
"

# Check for locks
psql -h $DB_HOST -U $DB_USER -c "SELECT * FROM pg_locks WHERE NOT granted;"
```

---

## 6. Troubleshooting Guides

### 6.1 High Error Rate

**Symptoms:** Error rate > 1%

**Diagnosis:**
1. Check error logs for patterns
2. Identify affected endpoints
3. Check downstream dependencies
4. Review recent deployments

**Resolution:**
```bash
# 1. Get error breakdown
kubectl logs deployment/api-server -n production | grep ERROR | cut -d' ' -f5 | sort | uniq -c | sort -rn | head

# 2. Check dependency health
curl -s https://dependency.example.com/health

# 3. If recent deploy, consider rollback
kubectl rollout undo deployment/api-server -n production
```

### 6.2 High Latency

**Symptoms:** P95 latency > 500ms

**Diagnosis:**
1. Check database query performance
2. Check cache hit rates
3. Review CPU/memory usage
4. Check network latency

**Resolution:**
```bash
# 1. Check slow queries
psql -h $DB_HOST -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# 2. Check Redis
redis-cli -h $REDIS_HOST INFO stats | grep hit

# 3. Scale if needed
kubectl scale deployment api-server --replicas=10 -n production
```

### 6.3 Out of Memory

**Symptoms:** OOMKilled pods, high memory usage

**Resolution:**
```bash
# 1. Check memory usage
kubectl top pods -n production -l app=api-server

# 2. Check for memory leaks (heap dump)
kubectl exec -it {pod} -n production -- /usr/bin/jmap -heap {pid}

# 3. Restart affected pods
kubectl delete pod {pod-name} -n production

# 4. Increase memory limits if needed
kubectl patch deployment api-server -n production -p '{"spec":{"template":{"spec":{"containers":[{"name":"api-server","resources":{"limits":{"memory":"4Gi"}}}]}}}}'
```

---

## 7. Incident Response

### 7.1 Incident Classification

| Severity | Description | Response Time | Escalation |
|----------|-------------|---------------|------------|
| SEV1 | Complete outage | 5 min | Immediate |
| SEV2 | Major degradation | 15 min | 30 min |
| SEV3 | Minor issue | 1 hour | 4 hours |

### 7.2 Incident Checklist

1. [ ] Acknowledge alert
2. [ ] Assess impact and severity
3. [ ] Start incident channel (#incident-{date})
4. [ ] Communicate status to stakeholders
5. [ ] Investigate root cause
6. [ ] Implement fix or workaround
7. [ ] Verify resolution
8. [ ] Update status page
9. [ ] Document timeline
10. [ ] Schedule post-mortem

---

## 8. Maintenance Procedures

### 8.1 Database Maintenance

**Frequency:** Weekly

```bash
# 1. Run vacuum analyze
psql -h $DB_HOST -U $DB_USER -c "VACUUM ANALYZE;"

# 2. Check bloat
psql -h $DB_HOST -U $DB_USER -c "SELECT schemaname, relname, n_dead_tup FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;"

# 3. Reindex if needed
psql -h $DB_HOST -U $DB_USER -c "REINDEX DATABASE mydb;"
```

### 8.2 Log Rotation

**Frequency:** Daily (automated)

```bash
# Verify log rotation
ls -la /var/log/app/

# Manual rotation if needed
logrotate -f /etc/logrotate.d/app
```

---

## 9. Disaster Recovery

### 9.1 Backup Information

| Data | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Database | Hourly | 30 days | S3 + cross-region |
| Config | On change | Indefinite | Git + Vault |
| Logs | Real-time | 90 days | Elasticsearch |

### 9.2 Recovery Procedure

```bash
# 1. List available backups
aws s3 ls s3://backups/database/ | tail -10

# 2. Restore database
./scripts/restore-db.sh --backup-id {backup_id} --target production

# 3. Verify data integrity
./scripts/verify-data.sh
```

---

## 10. Change Log

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| {Date} | 1.0 | {Author} | Initial version |

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
