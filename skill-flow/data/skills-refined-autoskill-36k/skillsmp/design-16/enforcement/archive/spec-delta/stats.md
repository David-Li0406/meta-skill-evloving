# Invariant Statistics and ROI Tracking

> Track what matters: Are our invariants preventing real incidents?

---

## Summary Dashboard

**Last Updated**: 2026-01-20

| Metric | Current Period (Q1 2026) | Previous Period (Q4 2025) | Trend |
|--------|--------------------------|---------------------------|-------|
| Total Active Invariants | 44 | 41 | +7% |
| Violations Caught | 127 | 98 | +30% |
| Estimated Incidents Prevented | 23 | 18 | +28% |
| False Positive Rate | 4.2% | 6.1% | -31% (improved) |
| Override Requests | 8 | 12 | -33% |
| New Invariants Added | 3 | 5 | -40% |
| Invariants Retired | 0 | 2 | - |

---

## Invariant Effectiveness Leaderboard

Ranked by estimated incidents prevented in the last 90 days.

| Rank | Invariant | Violations Caught | Est. Incidents Prevented | False Positives | ROI Score |
|------|-----------|-------------------|--------------------------|-----------------|-----------|
| 1 | INVARIANT-07: Database migration rollback required | 34 | 6 | 1 | 97% |
| 2 | INVARIANT-15: API versioning on breaking changes | 28 | 5 | 2 | 94% |
| 3 | INVARIANT-23: Environment isolation validation | 19 | 4 | 0 | 100% |
| 4 | INVARIANT-31: Secrets not in code or configs | 15 | 3 | 1 | 95% |
| 5 | INVARIANT-12: Backup verification before deployment | 12 | 2 | 2 | 86% |
| 6 | INVARIANT-44: OpenSearch deletion protection | 8 | 2 | 0 | 100% |
| 7 | INVARIANT-19: Circuit breaker on external calls | 6 | 1 | 1 | 86% |
| 8 | INVARIANT-38: PII logging prohibition | 5 | 0 | 0 | N/A |

**ROI Score** = (Violations Caught - False Positives) / Violations Caught * 100

---

## Invariants Needing Attention

### High False Positive Rate (>10%)

| Invariant | False Positive Rate | Last 30 Days | Action |
|-----------|---------------------|--------------|--------|
| INVARIANT-28: Max function complexity | 18% | 7 FPs | Under review - threshold too strict |
| INVARIANT-33: Dependency update frequency | 12% | 4 FPs | Refining exclusion list |

### Never Triggered (>90 days)

| Invariant | Days Since Last Trigger | Recommendation |
|-----------|------------------------|----------------|
| INVARIANT-09: Kernel version validation | 142 | Keep - catastrophic if violated |
| INVARIANT-22: Multi-region failover test | 98 | Keep - rare but critical |
| INVARIANT-36: GPU memory allocation limits | 94 | Review - may be obsolete |

### Recently Overridden (requires follow-up)

| Invariant | Override Date | Reason | Follow-up Status |
|-----------|--------------|--------|------------------|
| INVARIANT-15 | 2026-01-18 | Emergency hotfix for CVE | Closed - legitimate |
| INVARIANT-07 | 2026-01-12 | Schema-only change, no data migration | Open - considering exception rule |

---

## Monthly Tracking Template

Copy this section for each month's data collection.

### Month: January 2026

**Collection Date**: 2026-01-20

#### Violation Summary by Category

| Category | Violations | Prevented Incidents | Notes |
|----------|------------|---------------------|-------|
| Critical Data Protection | 23 | 4 | OpenSearch incident drove new invariant |
| Observability Requirements | 18 | 2 | |
| Deployment Safety | 41 | 8 | Migration checks working well |
| Security Boundaries | 15 | 3 | |
| Performance Guarantees | 12 | 2 | |
| API Contracts | 18 | 4 | Versioning catching breaking changes |

#### Top Violating Teams (for targeted training)

| Team | Violations | Primary Invariant | Action |
|------|------------|-------------------|--------|
| Data Platform | 24 | INVARIANT-07 | Schedule migration training |
| ML Engineering | 19 | INVARIANT-38 | PII handling refresher |
| API Gateway | 15 | INVARIANT-15 | Versioning workshop held |

#### Incident Correlation

| Date | Incident | Related Invariant | Caught? | Notes |
|------|----------|-------------------|---------|-------|
| 2026-01-20 | OpenSearch deletion | None (now INVARIANT-44) | No | New invariant created |
| 2026-01-15 | API breaking change | INVARIANT-15 | Yes | Deployment blocked correctly |
| 2026-01-08 | Backup restoration failure | INVARIANT-12 | Partial | Caught missing backup, not restoration test |

---

## Quarterly Analysis Template

### Q1 2026 Analysis

**Period**: January 1 - March 31, 2026

#### Invariant Lifecycle

| New Invariants | Source Incident | Effectiveness |
|----------------|-----------------|---------------|
| INVARIANT-42 | Cache invalidation cascade | 4 catches, 0 FPs |
| INVARIANT-43 | Unbounded query results | 7 catches, 1 FP |
| INVARIANT-44 | OpenSearch deletion | 8 catches, 0 FPs |

| Retired Invariants | Reason | Replacement |
|--------------------|--------|-------------|
| (none this quarter) | | |

| Modified Invariants | Change | Impact |
|---------------------|--------|--------|
| INVARIANT-12 | Added restoration test requirement | +2 catches |
| INVARIANT-28 | Relaxed complexity threshold | -60% FPs |

#### Cost-Benefit Analysis

**Estimated Cost of Prevented Incidents**:
- 23 incidents prevented x average $45,000/incident = $1,035,000
- (Average incident cost based on: engineering time, SLA credits, customer impact)

**Cost of Invariant System**:
- Tooling maintenance: 0.5 FTE = ~$75,000/quarter
- False positive resolution: 15 hours x $150/hr = $2,250
- New invariant development: 40 hours x $150/hr = $6,000
- **Total**: ~$83,250/quarter

**ROI**: 12.4x return on investment

#### Trends and Observations

1. **Migration invariants most valuable**: INVARIANT-07 consistently prevents highest-impact incidents
2. **API versioning culture improving**: Violation rate down 40% YoY despite more deployments
3. **ML teams need attention**: Higher violation rate, mostly PII-related
4. **False positive rate improving**: Refinements to thresholds paying off

#### Recommendations for Q2

1. Add training requirement for teams with >20 violations/quarter
2. Review INVARIANT-36 for potential retirement
3. Consider new invariant category for ML model deployment safety
4. Improve INVARIANT-12 to verify restoration time, not just success

---

## Historical Data

### Violations by Quarter

| Quarter | Total Violations | Incidents Prevented | FP Rate | Active Invariants |
|---------|------------------|---------------------|---------|-------------------|
| Q1 2025 | 67 | 8 | 11.2% | 32 |
| Q2 2025 | 89 | 12 | 9.1% | 35 |
| Q3 2025 | 94 | 15 | 7.3% | 38 |
| Q4 2025 | 98 | 18 | 6.1% | 41 |
| Q1 2026* | 127 | 23 | 4.2% | 44 |

*Q1 2026 projected based on January data

### Invariant Age vs. Effectiveness

| Age (quarters) | Avg Catches/Quarter | Avg FP Rate | Notes |
|----------------|---------------------|-------------|-------|
| 0-2 | 8.3 | 7.2% | New invariants catching novel issues |
| 2-4 | 5.1 | 4.1% | Teams learning, FPs refined |
| 4-6 | 2.8 | 2.3% | Mature, low-maintenance |
| 6+ | 1.2 | 1.1% | Consider if still relevant |

---

## How to Update This Document

### Weekly (Friday)
1. Pull violation counts from `guardrails/metrics` dashboard
2. Update "Invariants Needing Attention" section
3. Log any overrides from the past week

### Monthly (First Monday)
1. Complete the Monthly Tracking Template
2. Update Summary Dashboard
3. Review teams with high violation counts

### Quarterly (First week of quarter)
1. Complete Quarterly Analysis Template
2. Calculate ROI
3. Present findings in Platform Review meeting
4. Archive previous quarter's data

### After Each New Invariant
1. Add to Leaderboard with initial zeros
2. Add source incident to Quarterly Analysis
3. Set reminder for 30-day effectiveness review
