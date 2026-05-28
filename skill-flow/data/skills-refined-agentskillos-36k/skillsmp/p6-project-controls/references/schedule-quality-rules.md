# Schedule Quality Rules

Industry-standard validation rules for schedule quality assessment. These rules follow DCMA 14-Point Assessment and AACE Best Practices.

## 1. Logic Rules

### 1.1 Missing Predecessors
**Rule**: All activities except project start should have at least one predecessor.

**Severity**: High

**Check**:
```sql
SELECT task_code, task_name
FROM TASK t
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND task_type NOT IN ('TT_Mile', 'TT_FinMile')
  AND NOT EXISTS (
    SELECT 1 FROM TASKPRED tp WHERE tp.task_id = t.task_id
  );
```

**Exception**: Project start milestone or activities constrained to project start.

### 1.2 Missing Successors
**Rule**: All activities except project finish should have at least one successor.

**Severity**: High

**Check**:
```sql
SELECT task_code, task_name
FROM TASK t
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND task_type NOT IN ('TT_Mile', 'TT_FinMile')
  AND NOT EXISTS (
    SELECT 1 FROM TASKPRED tp WHERE tp.pred_task_id = t.task_id
  );
```

**Exception**: Project finish milestone or contractual milestones.

### 1.3 Invalid Relationships
**Rule**: Relationships should be logically valid (no circular dependencies, no SF unless justified).

**Severity**: Critical

**Checks**:
- No Start-to-Finish relationships (rare and often incorrect)
- No relationships between activities in different projects without proper handling
- No self-referencing relationships

### 1.4 Hard Constraints
**Rule**: Less than 5% of activities should have date constraints (excluding milestones).

**Severity**: Medium

**Check**:
```sql
SELECT
    COUNT(*) AS constrained_count,
    (SELECT COUNT(*) FROM TASK WHERE proj_id = :project_id AND status_code != 'TK_Complete') AS total_count,
    ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM TASK WHERE proj_id = :project_id AND status_code != 'TK_Complete'), 0), 2) AS constraint_pct
FROM TASK
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND task_type NOT IN ('TT_Mile', 'TT_FinMile')
  AND cstr_type IS NOT NULL
  AND cstr_type NOT IN ('CS_ALAP');
```

**Target**: <5% of non-milestone activities constrained

**Exceptions**:
- Regulatory or contractual milestones
- Interface dates with external parties
- Resource availability constraints

### 1.5 Relationship Logic Density
**Rule**: Average relationship count per activity should be 1.5 or higher.

**Severity**: Medium

**Check**:
```sql
SELECT
    ROUND(COUNT(tp.task_pred_id) * 1.0 / COUNT(DISTINCT t.task_id), 2) AS avg_relationships
FROM TASK t
LEFT JOIN TASKPRED tp ON (tp.task_id = t.task_id OR tp.pred_task_id = t.task_id)
WHERE t.proj_id = :project_id
  AND t.status_code != 'TK_Complete';
```

**Target**: ≥1.5 relationships per activity (predecessor + successor)

### 1.6 Out-of-Sequence Progress
**Rule**: Activities should not have actual dates that violate logic (e.g., successor starts before predecessor finishes).

**Severity**: Critical

**Check**: Identify activities with actual start dates earlier than predecessor actual finish dates (for FS relationships).

## 2. Duration Rules

### 2.1 Long Duration Activities
**Rule**: Detail activities should not exceed 20 working days (4 weeks).

**Severity**: Medium

**Check**:
```sql
SELECT task_code, task_name, target_drtn_hr_cnt / 8 AS duration_days
FROM TASK
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND task_type = 'TT_Task'
  AND target_drtn_hr_cnt > 160  -- 20 days * 8 hours
ORDER BY target_drtn_hr_cnt DESC;
```

**Target**: <5% of detail activities exceed 20 days

**Exceptions**:
- Level of Effort (LOE) activities
- Long-lead procurement activities
- Summary-level activities

### 2.2 Short Duration Activities
**Rule**: Activities should have reasonable durations (typically ≥1 day for tasks).

**Severity**: Low

**Check**:
```sql
SELECT task_code, task_name, target_drtn_hr_cnt
FROM TASK
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND task_type = 'TT_Task'
  AND target_drtn_hr_cnt < 8  -- Less than 1 day
  AND target_drtn_hr_cnt > 0;
```

**Exception**: Very small discrete activities may be valid but should be reviewed.

### 2.3 Zero Duration Non-Milestones
**Rule**: Only milestone activities should have zero duration.

**Severity**: High

**Check**:
```sql
SELECT task_code, task_name, task_type
FROM TASK
WHERE proj_id = :project_id
  AND (target_drtn_hr_cnt = 0 OR target_drtn_hr_cnt IS NULL)
  AND task_type NOT IN ('TT_Mile', 'TT_FinMile');
```

### 2.4 Invalid Remaining Duration
**Rule**: In-progress activities should have reasonable remaining duration.

**Severity**: Medium

**Check**:
- Remaining duration should not be greater than original duration for in-progress activities
- Remaining duration should not be zero for not-started activities
- Remaining duration should be zero for completed activities

## 3. Critical Path Rules

### 3.1 Critical Path Exists
**Rule**: Schedule must have a continuous critical path from start to finish.

**Severity**: Critical

**Check**: Verify that:
1. At least one path exists with total float ≤ 0
2. Critical path is continuous (no gaps)
3. Critical path leads to project completion milestone

### 3.2 Critical Path Validity
**Rule**: Critical activities should be logically critical (not just constraint-driven).

**Severity**: Medium

**Check**: Review critical activities to ensure criticality is due to logic, not excessive constraints.

### 3.3 High Float
**Rule**: Identify activities with excessive float (>44 working days / ~2 months).

**Severity**: Low

**Check**:
```sql
SELECT task_code, task_name, total_float_hr_cnt / 8 AS float_days
FROM TASK
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND total_float_hr_cnt > 352  -- 44 days * 8 hours
ORDER BY total_float_hr_cnt DESC;
```

**Purpose**: High float may indicate logic errors or activities not properly tied to completion.

### 3.4 Negative Float
**Rule**: Monitor activities with negative float.

**Severity**: High

**Check**:
```sql
SELECT task_code, task_name, total_float_hr_cnt / 8 AS float_days,
       target_end_date
FROM TASK
WHERE proj_id = :project_id
  AND status_code != 'TK_Complete'
  AND total_float_hr_cnt < 0
ORDER BY total_float_hr_cnt;
```

**Interpretation**: Negative float indicates schedule compression or delays beyond planned completion.

## 4. Resource Rules

### 4.1 Missing Resource Assignments
**Rule**: Activities should have resource assignments (if project uses resource loading).

**Severity**: Medium (project-dependent)

**Check**:
```sql
SELECT t.task_code, t.task_name
FROM TASK t
WHERE t.proj_id = :project_id
  AND t.status_code != 'TK_Complete'
  AND t.task_type = 'TT_Task'
  AND NOT EXISTS (
    SELECT 1 FROM TASKRSRC tr WHERE tr.task_id = t.task_id
  );
```

**Exception**: Not all projects use resource-loaded schedules.

### 4.2 Resource Over-Allocation
**Rule**: Resources should not be over-allocated beyond defined limits.

**Severity**: Medium

**Check**: Sum resource usage per time period and compare to max_qty_per_hr.

**Target**: <10% of resource-hours over-allocated

### 4.3 Resource Calendar Assignment
**Rule**: Resources should have appropriate calendars assigned.

**Severity**: Low

**Check**: Verify resources have valid calendar assignments matching work patterns.

## 5. Progress Rules

### 5.1 Actual Date Logic
**Rule**: Actual dates should align with percent complete and logic.

**Severity**: High

**Checks**:
- Activities with actual start should have phys_complete_pct > 0
- Activities with actual finish should have phys_complete_pct = 100
- Actual start should not be after data date
- Actual finish should not be after data date

### 5.2 Future Actuals
**Rule**: No actual dates in the future.

**Severity**: Critical

**Check**:
```sql
SELECT task_code, task_name, act_start_date, act_end_date
FROM TASK
WHERE proj_id = :project_id
  AND (act_start_date > CURRENT_DATE OR act_end_date > CURRENT_DATE);
```

### 5.3 Invalid Percent Complete
**Rule**: Percent complete should be between 0 and 100 and align with dates.

**Severity**: High

**Check**:
```sql
SELECT task_code, task_name, phys_complete_pct, act_start_date, act_end_date
FROM TASK
WHERE proj_id = :project_id
  AND (
    phys_complete_pct < 0 OR phys_complete_pct > 100
    OR (phys_complete_pct > 0 AND act_start_date IS NULL)
    OR (phys_complete_pct = 100 AND act_end_date IS NULL)
  );
```

### 5.4 Incomplete Predecessor
**Rule**: Activities should not start until predecessors are complete (unless approved out-of-sequence).

**Severity**: Medium

**Check**: Identify activities that have started but have incomplete predecessors (potential out-of-sequence work).

## 6. Baseline Rules

### 6.1 Baseline Assignment
**Rule**: Project should have an approved baseline for variance tracking.

**Severity**: Medium

**Check**: Verify baseline project exists and is properly assigned.

### 6.2 Baseline Variance Thresholds
**Rule**: Monitor activities with significant variance from baseline.

**Severity**: Medium

**Thresholds**:
- Critical activities: >5 days finish variance
- Near-critical (<10 days float): >10 days finish variance
- Non-critical: >15 days finish variance

### 6.3 Baseline Maintenance
**Rule**: Baseline should be maintained and updated per project procedures.

**Severity**: Low

**Check**: Verify baseline is current and approved.

## Summary Quality Metrics

A high-quality schedule should meet these overall targets:

| Metric | Target | Source |
|--------|--------|--------|
| Activities with predecessors | >95% | DCMA |
| Activities with successors | >95% | DCMA |
| Relationships per activity | ≥1.5 | DCMA |
| Activities with constraints | <5% | DCMA |
| Long duration activities (>44 days) | <5% | DCMA |
| High float activities (>44 days) | <5% | DCMA |
| Negative float | 0% (ideal) | DCMA |
| Invalid actual dates | 0% | DCMA |
| Missing critical path | 0 (must have) | DCMA |
| Resource over-allocation | <10% | Industry |

## Implementation Notes

- Run validation checks weekly during active project phases
- Generate exception reports highlighting violations with severity
- Track trends over time (improving vs degrading schedule quality)
- Integrate checks into automated schedule review workflows
- Customize thresholds based on project phase and industry standards
- Document approved exceptions (e.g., valid constraints)
