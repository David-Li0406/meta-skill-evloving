# PRP: PostgreSQL to Aurora Migration

> Data infrastructure project demonstrating explicit state management and recovery planning.

---

## Meta

```yaml
prp_id: PRP-2026-01-20-003
source_spec: specs/infrastructure/postgres-aurora-migration-spec.md
validation_status: PASSED
validated_date: 2026-01-20
domain: data-architecture
author: Platform Team
version: 1.0
```

---

## 1. Project Overview

### 1.1 Problem Statement

Current self-managed PostgreSQL cluster on EC2 experiences 4 hours/month unplanned downtime. Vertical scaling ceiling reached at db.r5.4xlarge. DBA time spent on maintenance: 20 hours/week. Read replica lag during peak: 15 seconds.

### 1.2 Solution Summary

Migrate primary transactional database from self-managed PostgreSQL 14 to Aurora PostgreSQL 15. Implement read replicas in 2 regions. Zero-downtime migration using AWS DMS with validation checkpoints.

### 1.3 Scope Boundaries

| In Scope | Out of Scope |
|----------|--------------|
| Primary OLTP database (2.3TB) | Analytics data warehouse |
| 3 read replicas | Cross-account replication |
| Application connection string update | Application code changes |
| 90-day parallel run | Archive data migration |

### 1.4 Key Stakeholders

| Role | Name | Responsibility |
|------|------|----------------|
| DBA Lead | Chen Wei | Migration execution, validation |
| Platform Lead | Alex Kim | Infrastructure, networking |
| App Team Lead | Jordan Smith | Connection testing, cutover coordination |
| SRE Lead | Sam Patel | Monitoring, incident response |

---

## 2. Success Criteria

### 2.1 Primary Metrics

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Unplanned downtime | 4 hrs/month | <15 min/month | CloudWatch + PagerDuty |
| Read replica lag | 15s peak | <1s p99 | Aurora metrics |
| DBA maintenance time | 20 hrs/week | <5 hrs/week | Time tracking |
| Query latency (p99) | 45ms | <30ms | APM traces |

### 2.2 Success Conditions

```
SUCCESS := ALL(
  data_integrity_verified,
  zero_data_loss,
  latency_p99 < 30ms for 14_consecutive_days,
  old_cluster_decommissioned,
  cost_within_budget
)
```

### 2.3 Failure Conditions

```
FAILURE := ANY(
  data_loss_detected,
  replication_lag > 60s for 5_minutes,
  application_errors > baseline + 5%
)
```

---

## 3. Timeline with Validation Gates

### Phase 1: Infrastructure Setup

**Duration**: 1 week
**Owner**: Alex Kim

#### Deliverables
- [ ] Aurora cluster provisioned (db.r6g.2xlarge)
- [ ] VPC peering configured
- [ ] Security groups updated
- [ ] Parameter groups configured (matching current)
- [ ] Read replicas in us-east-1 and us-west-2

#### Validation Gate 1: Infrastructure Ready

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| Connectivity | App servers can reach Aurora | telnet test from all app hosts |
| Parameters | Match production PG config | pg_settings comparison |
| Networking | <1ms latency app→db | ping test |
| Security | Only authorized access | Security group audit |

```
GATE_1_PASS := connectivity AND params_match AND latency < 1ms AND security_verified
```

**If gate fails**: Fix networking/security issues. Do not proceed until app connectivity confirmed.

---

### Phase 2: DMS Replication

**Duration**: 2 weeks
**Owner**: Chen Wei

**Depends on**: Gate 1 passed

#### Deliverables
- [ ] DMS replication instance provisioned
- [ ] Source endpoint configured
- [ ] Target endpoint configured
- [ ] Full load completed
- [ ] CDC (change data capture) active
- [ ] Replication lag <10 seconds sustained

#### State Transitions (Phase 2)

<!-- Invariant #2: State Must Be Explicit -->

```
REPLICATION_STATE:
  NOT_STARTED → FULL_LOAD_RUNNING  [on: dms_task_started]
  FULL_LOAD_RUNNING → FULL_LOAD_COMPLETE  [on: initial_load_done]
  FULL_LOAD_COMPLETE → CDC_ACTIVE  [on: cdc_streaming]
  CDC_ACTIVE → CDC_CAUGHT_UP  [on: lag < 10s for 1_hour]

  * → REPLICATION_FAILED  [on: dms_error OR lag > 60s]
  REPLICATION_FAILED → CDC_ACTIVE  [on: error_resolved AND task_resumed]
```

#### Validation Gate 2: Replication Stable

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| Full load complete | 100% tables loaded | DMS console |
| Row counts match | Source = Target ±0 | Count comparison script |
| CDC lag | <10s for 24 hours | CloudWatch metrics |
| No DMS errors | Zero errors in 24h | DMS logs |

```
GATE_2_PASS := tables_loaded AND rows_match AND cdc_lag < 10s AND no_errors_24h
```

**If gate fails**: Investigate DMS issues, check network bandwidth, verify no schema conflicts.

#### Data Validation Queries

```sql
-- Run on both source and target, compare results
-- Gate 2 requires: source_count = target_count for all tables

SELECT schemaname, tablename, n_live_tup
FROM pg_stat_user_tables
ORDER BY schemaname, tablename;

-- Checksum validation for critical tables
SELECT md5(array_agg(md5(row::text))::text)
FROM (SELECT * FROM orders ORDER BY id) row;
```

---

### Phase 3: Application Cutover (Staged)

**Duration**: 2 weeks
**Owner**: Jordan Smith

**Depends on**: Gate 2 passed

#### Deliverables
- [ ] Connection string abstraction (if not exists)
- [ ] Read traffic to Aurora: 10% → 50% → 100%
- [ ] Write traffic to Aurora: shadow writes → primary
- [ ] Old cluster demoted to read-only backup

#### Cutover State Machine

```
CUTOVER_STATE:
  SOURCE_PRIMARY → READS_10PCT_AURORA  [on: feature_flag_enabled]
  READS_10PCT_AURORA → READS_50PCT_AURORA  [on: 24h_stable]
  READS_50PCT_AURORA → READS_100PCT_AURORA  [on: 48h_stable]

  READS_100PCT_AURORA → SHADOW_WRITES  [on: 72h_stable]
  SHADOW_WRITES → WRITES_TO_AURORA  [on: shadow_validation_passed]
  WRITES_TO_AURORA → SOURCE_READ_ONLY  [on: 24h_stable]
  SOURCE_READ_ONLY → CUTOVER_COMPLETE  [on: 7_days_stable]

  * → ROLLBACK  [on: error_threshold_exceeded]
  ROLLBACK → SOURCE_PRIMARY  [immediately]
```

#### Validation Gate 3: Cutover Stable

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| Read latency | p99 <30ms | APM dashboard |
| Write latency | p99 <20ms | APM dashboard |
| Error rate | <0.1% | Application logs |
| Data consistency | Checksums match (shadow period) | Validation script |
| App health | All services green | Health checks |

```
GATE_3_PASS := latency_targets_met AND error_rate < 0.001 AND data_consistent
```

**If gate fails**: Rollback to source. Analyze latency/error spikes. Do not decommission source.

#### Rollback Procedure

<!-- Invariant #4: No Irreversible Without Recovery -->

```
ROLLBACK_PROCEDURE:
  1. Disable Aurora writes (feature flag) [immediate]
  2. Wait for in-flight transactions [max 30s]
  3. Enable source writes [immediate]
  4. Redirect read traffic to source [gradual, 1h]
  5. Pause DMS replication [after traffic stable]
  6. Investigate root cause [within 24h]
  7. Decide: retry or abort migration [stakeholder decision]

ROLLBACK_WINDOW: 90 days (until source decommissioned)
```

---

### Phase 4: Decommission

**Duration**: 1 week (after 90-day parallel run)
**Owner**: Chen Wei

**Depends on**: Gate 3 passed, 90 days stable

#### Deliverables
- [ ] Final data validation
- [ ] Source database snapshot (archive)
- [ ] DMS task stopped
- [ ] Source cluster terminated
- [ ] DNS records updated
- [ ] Documentation updated

#### Final Validation Gate

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| 90-day stability | No rollbacks needed | Incident history |
| Final validation | Checksums match | Validation script |
| Snapshot created | Archived to S3 | S3 console |
| No source connections | 0 active connections | pg_stat_activity |

```
PROJECT_COMPLETE := stable_90_days AND final_validation AND snapshot_archived
```

---

## 4. Risk Assessment and Mitigation

### 4.1 Risk Matrix

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Data loss during cutover | Low | Critical | Shadow writes + validation | Chen |
| Replication lag spike | Medium | High | Dedicated DMS instance, monitoring | Chen |
| Application compatibility | Low | High | Extensive testing, staged rollout | Jordan |
| Cost overrun (parallel run) | Medium | Medium | 90-day cap, monitoring | Alex |
| Schema drift during migration | Low | Medium | Schema change freeze | Chen |

### 4.2 Fallback Strategies

```
IF replication_lag > 60s:
  THEN pause_cutover AND scale_dms_instance

IF application_errors > baseline + 5%:
  THEN rollback_to_source immediately

IF aurora_performance_degraded:
  THEN scale_aurora_instance (auto-scaling enabled)

IF dms_task_failed:
  THEN restart_from_checkpoint (full reload if necessary)
```

### 4.3 Circuit Breakers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Replication lag | >60s for 5 min | Alert + pause cutover |
| Aurora CPU | >80% for 10 min | Scale up instance |
| Application errors | >1% for 5 min | Rollback to source |
| DMS errors | Any error | Alert + investigate |

---

## 5. Resource Requirements

### 5.1 Human Resources

| Role | Allocation | Skills Required |
|------|------------|-----------------|
| DBA | 1 FTE, 6 weeks | PostgreSQL, Aurora, DMS |
| Platform Engineer | 0.5 FTE, 4 weeks | AWS, Terraform, networking |
| App Engineer | 0.25 FTE, 2 weeks | Connection management, testing |
| SRE | 0.25 FTE, ongoing | Monitoring, incident response |

### 5.2 Technical Resources

| Resource | Specification | Purpose |
|----------|--------------|---------|
| Aurora cluster | db.r6g.2xlarge (primary) | Target database |
| Aurora replicas | db.r6g.xlarge x 3 | Read scaling |
| DMS instance | dms.r5.2xlarge | Replication |
| S3 bucket | Standard, versioned | Snapshots, logs |

### 5.3 External Dependencies

| Dependency | Owner | SLA | Fallback |
|------------|-------|-----|----------|
| AWS Aurora | AWS | 99.99% | Multi-AZ automatic |
| AWS DMS | AWS | 99.9% | Restart from checkpoint |
| VPC peering | Internal | N/A | Direct connect backup |

### 5.4 Budget

| Category | Estimated | Cap | Approval Required |
|----------|-----------|-----|-------------------|
| Aurora (monthly) | $3,200 | $4,500 | Platform Lead |
| DMS (migration period) | $800 | $1,200 | Platform Lead |
| Parallel run (90 days) | $9,600 | $12,000 | VP Engineering |
| Data transfer | $200 | $500 | N/A |

---

## 6. Communication Plan

### 6.1 Regular Updates

| Audience | Frequency | Format | Owner |
|----------|-----------|--------|-------|
| Platform team | Daily | Standup | Chen |
| Stakeholders | Weekly | Status report | Alex |
| Application teams | Pre-cutover | Training session | Jordan |
| On-call | Pre-cutover | Runbook review | Sam |

### 6.2 Escalation Matrix

| Condition | Escalate To | Within | Channel |
|-----------|-------------|--------|---------|
| Replication failure | Chen Wei | 15 min | PagerDuty |
| Data inconsistency | Chen + Alex | 30 min | Slack #data-platform |
| Cutover rollback | All stakeholders | 1 hour | Email + Slack |
| Budget threshold | VP Engineering | 24 hours | Email |

### 6.3 Decision Authority

| Decision Type | Authority | Escalation |
|--------------|-----------|------------|
| Cutover timing | Jordan + Chen | Alex Kim |
| Rollback decision | On-call (Sam) | Chen Wei |
| Budget increase | Alex Kim | VP Engineering |
| Timeline extension | Alex Kim | VP Engineering |

---

## 7. Pre-Execution Checklist

### 7.1 Validation Complete

- [x] Source spec passed validator with no blocking violations
- [x] All warnings reviewed and accepted
- [x] Domain-specific invariants checked: data-architecture

### 7.2 Resources Confirmed

- [x] DBA time allocated
- [x] AWS quota increase approved
- [x] Budget approved (including parallel run)
- [x] Change freeze communicated

### 7.3 Communication Ready

- [x] Kickoff meeting scheduled
- [x] Stakeholders notified
- [x] On-call runbook drafted

### 7.4 Risk Preparation

- [x] Rollback procedure documented
- [x] Monitoring dashboards created
- [x] Alerting configured
- [ ] Disaster recovery drill scheduled

---

## 8. Validation Commands

Run these commands to verify the Aurora migration:

### 8.1 Test Verification

```bash
# Connection test to Aurora
psql "$AURORA_URL" -c "SELECT 1 AS connection_test"

# Row count comparison (source vs target)
./scripts/compare-row-counts.sh source target

# Checksum validation for critical tables
./scripts/validate-checksums.sh orders users transactions
```

### 8.2 Code Quality

```bash
# Validate DMS task configuration
aws dms describe-replication-tasks --filters Name=replication-task-id,Values=postgres-aurora \
  | jq '.ReplicationTasks[0].Status'

# Check for schema drift
pg_dump --schema-only "$SOURCE_URL" > /tmp/source.sql
pg_dump --schema-only "$AURORA_URL" > /tmp/target.sql
diff /tmp/source.sql /tmp/target.sql
```

### 8.3 Integration Checks

```bash
# DMS replication lag
aws cloudwatch get-metric-statistics \
  --namespace "AWS/DMS" \
  --metric-name "CDCLatencySource" \
  --dimensions Name=ReplicationInstanceIdentifier,Value=dms-instance \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average

# Application health with Aurora
curl -sf http://localhost:8080/health/database && echo "APP+DB HEALTHY"

# Read replica lag check
psql "$AURORA_READER_URL" -c "SELECT NOW() - pg_last_xact_replay_timestamp() AS replication_lag"
```

### 8.4 Build Verification

```bash
# Verify connection string abstraction
grep -r "DATABASE_URL" src/ | wc -l  # Should be 0 (use abstraction)

# Test rollback procedure (dry run)
./scripts/rollback-dryrun.sh

# Verify monitoring dashboards
aws cloudwatch describe-dashboards --dashboard-names "aurora-migration" | jq '.DashboardEntries[0].DashboardName'
```

---

## 9. Recommended Thinking Level

### Assessment

| Factor | Value | Impact |
|--------|-------|--------|
| Confidence Score | 6.8/10 | Think carefully |
| Domains Involved | 1 (data-architecture) | Think |
| Invariants Applied | 15 | Think |
| Files Affected | ~5 (infra) + app connections | Think |
| Pattern Availability | Good (DMS is standard) | Normal |

### Recommendation

**Overall Level**: Think Hard

**Apply higher thinking to**:
- Cutover timing and rollback window decisions
- Data validation query design
- Replication lag threshold tuning
- 90-day parallel run cost monitoring

---

## 10. State Transitions

```
PROJECT_STATE:
  NOT_STARTED → PHASE_1_ACTIVE         [on: kickoff]
  PHASE_1_ACTIVE → GATE_1              [on: infra_ready]
  GATE_1 → PHASE_2_ACTIVE              [on: connectivity_verified]

  PHASE_2_ACTIVE → FULL_LOAD           [on: dms_started]
  FULL_LOAD → CDC_ACTIVE               [on: initial_load_complete]
  CDC_ACTIVE → GATE_2                  [on: lag_stable_24h]
  GATE_2 → PHASE_3_ACTIVE              [on: replication_validated]

  PHASE_3_ACTIVE → READS_MIGRATING     [on: read_traffic_started]
  READS_MIGRATING → SHADOW_WRITES      [on: reads_100pct_stable]
  SHADOW_WRITES → WRITES_MIGRATED      [on: shadow_validated]
  WRITES_MIGRATED → GATE_3             [on: 7_days_stable]

  GATE_3 → PARALLEL_RUN                [on: cutover_validated]
  PARALLEL_RUN → PHASE_4_ACTIVE        [on: 90_days_complete]
  PHASE_4_ACTIVE → COMPLETE            [on: source_decommissioned]

  READS_MIGRATING|SHADOW_WRITES|WRITES_MIGRATED → ROLLBACK  [on: error_threshold]
  ROLLBACK → PHASE_3_ACTIVE            [on: issue_resolved]
```

---

## 11. Execution Log

### Phase Completion

| Phase | Started | Gate Attempted | Gate Result | Notes |
|-------|---------|----------------|-------------|-------|
| Phase 1: Infrastructure | | | | |
| Phase 2: Replication | | | | |
| Phase 3: Cutover | | | | |
| Phase 4: Decommission | | | | |

### Deviations from Plan

| Date | Deviation | Impact | Resolution |
|------|-----------|--------|------------|

### Lessons Learned

| Category | Learning | Action |
|----------|----------|--------|

---

## Appendix A: Source Spec Reference

**Spec Path**: specs/infrastructure/postgres-aurora-migration-spec.md
**Spec Version**: 1.3
**Invariants Validated**: 1-10 (universal), 22-26 (data-architecture)

### Key Spec Sections Compiled

| Spec Section | PRP Section | Transformation |
|--------------|-------------|----------------|
| Data Inventory | Phase 2 full load | Table list + row counts |
| Migration Strategy | Phase 3 state machine | Cutover steps → states |
| Rollback Requirements | Section 4.3, Rollback Procedure | Added 90-day window |
| Consistency Requirements | Gate validation queries | SQL checksums |

### Data Architecture Invariants Applied

| Invariant | Application |
|-----------|-------------|
| #22: Schema Changes Require Migration Path | Change freeze during migration |
| #23: Data Validation Must Be Continuous | Checkpoint validation at each gate |
| #24: Backup Strategy Must Be Explicit | Snapshot before decommission |
| #25: Replication Lag Must Be Bounded | <10s threshold with alerting |

---

## Appendix B: Validation Queries

```sql
-- Pre-migration baseline (run on source)
\copy (
  SELECT schemaname, tablename, n_live_tup
  FROM pg_stat_user_tables
  ORDER BY 1, 2
) TO '/tmp/source_counts.csv' CSV HEADER;

-- Post-migration validation (run on target, compare)
\copy (
  SELECT schemaname, tablename, n_live_tup
  FROM pg_stat_user_tables
  ORDER BY 1, 2
) TO '/tmp/target_counts.csv' CSV HEADER;

-- Critical table checksums (run on both)
SELECT 'orders' as tbl, md5(array_agg(md5(row::text))::text) as checksum
FROM (SELECT * FROM orders ORDER BY id) row
UNION ALL
SELECT 'users', md5(array_agg(md5(row::text))::text)
FROM (SELECT * FROM users ORDER BY id) row
UNION ALL
SELECT 'transactions', md5(array_agg(md5(row::text))::text)
FROM (SELECT * FROM transactions ORDER BY id) row;
```

---

*Compiled from validated spec on 2026-01-20*
