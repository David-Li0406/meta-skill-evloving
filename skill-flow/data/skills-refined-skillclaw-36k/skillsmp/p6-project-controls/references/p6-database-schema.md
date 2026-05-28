# P6 Database Schema Reference

This document provides key table structures and relationships in the Primavera P6 database schema.

## Core Tables

### PROJECT
Main project table containing project-level information.

**Key Fields:**
- `proj_id` (NUMBER): Primary key, unique project identifier
- `proj_short_name` (VARCHAR2): Project short code/name
- `proj_name` (VARCHAR2): Full project name
- `plan_start_date` (DATE): Planned project start
- `plan_end_date` (DATE): Planned project finish
- `scd_end_date` (DATE): Scheduled finish date
- `est_wt_comp_pct` (NUMBER): Overall project % complete
- `sum_base_qty_labor_units` (NUMBER): Total budgeted labor hours
- `sum_remain_qty` (NUMBER): Remaining work quantity
- `clndr_id` (NUMBER): FK to CLNDR (project calendar)
- `status_code` (VARCHAR2): Project status (Active, What-If, etc.)

### TASK (Activities)
Individual schedule activities/tasks.

**Key Fields:**
- `task_id` (NUMBER): Primary key
- `proj_id` (NUMBER): FK to PROJECT
- `wbs_id` (NUMBER): FK to PROJWBS
- `task_code` (VARCHAR2): Activity ID/code
- `task_name` (VARCHAR2): Activity name
- `task_type` (VARCHAR2): TT_Task, TT_Mile, TT_Rsrc, TT_LOE, TT_FinMile
- `duration_type` (VARCHAR2): DT_FixedDrtn, DT_FixedQty, etc.
- `status_code` (VARCHAR2): TK_NotStart, TK_Active, TK_Complete
- `target_start_date` (DATE): Planned/scheduled start
- `target_end_date` (DATE): Planned/scheduled finish
- `act_start_date` (DATE): Actual start date
- `act_end_date` (DATE): Actual finish date
- `remain_drtn_hr_cnt` (NUMBER): Remaining duration in hours
- `target_drtn_hr_cnt` (NUMBER): Planned duration in hours
- `total_float_hr_cnt` (NUMBER): Total float in hours
- `free_float_hr_cnt` (NUMBER): Free float in hours
- `phys_complete_pct` (NUMBER): Physical percent complete
- `cstr_type` (VARCHAR2): Constraint type (CS_MSO, CS_ALAP, etc.)
- `cstr_date` (DATE): Constraint date
- `clndr_id` (NUMBER): FK to CLNDR (activity calendar)
- `driving_path_flag` (VARCHAR2): Y/N - on critical path

### TASKPRED (Relationships)
Predecessor/successor relationships between activities.

**Key Fields:**
- `task_pred_id` (NUMBER): Primary key
- `task_id` (NUMBER): FK to TASK (successor activity)
- `pred_task_id` (NUMBER): FK to TASK (predecessor activity)
- `pred_type` (VARCHAR2): PR_FS, PR_SS, PR_FF, PR_SF
- `lag_hr_cnt` (NUMBER): Lag in hours (negative for lead)
- `float_path_hr_cnt` (NUMBER): Float on this path
- `driving_path_flag` (VARCHAR2): Y/N - driving relationship

### PROJWBS (Work Breakdown Structure)
Hierarchical WBS elements.

**Key Fields:**
- `wbs_id` (NUMBER): Primary key
- `proj_id` (NUMBER): FK to PROJECT
- `parent_wbs_id` (NUMBER): FK to PROJWBS (parent element)
- `wbs_short_name` (VARCHAR2): WBS code
- `wbs_name` (VARCHAR2): WBS element name
- `seq_num` (NUMBER): Sort order
- `est_wt_comp_pct` (NUMBER): WBS % complete

### TASKRSRC (Resource Assignments)
Resource assignments to activities.

**Key Fields:**
- `taskrsrc_id` (NUMBER): Primary key
- `task_id` (NUMBER): FK to TASK
- `rsrc_id` (NUMBER): FK to RSRC
- `proj_id` (NUMBER): FK to PROJECT
- `target_qty` (NUMBER): Budgeted quantity
- `remain_qty` (NUMBER): Remaining quantity
- `act_reg_qty` (NUMBER): Actual quantity (regular)
- `target_cost` (NUMBER): Budgeted cost
- `remain_cost` (NUMBER): Remaining cost
- `act_reg_cost` (NUMBER): Actual cost

### RSRC (Resources)
Resource master data.

**Key Fields:**
- `rsrc_id` (NUMBER): Primary key
- `rsrc_short_name` (VARCHAR2): Resource code
- `rsrc_name` (VARCHAR2): Resource name
- `rsrc_type` (VARCHAR2): RT_Labor, RT_Mat, RT_Equip
- `max_qty_per_hr` (NUMBER): Max units per hour
- `clndr_id` (NUMBER): FK to CLNDR (resource calendar)

### CLNDR (Calendars)
Calendar definitions.

**Key Fields:**
- `clndr_id` (NUMBER): Primary key
- `clndr_name` (VARCHAR2): Calendar name
- `default_day_hr_cnt` (NUMBER): Standard hours per day
- `clndr_type` (VARCHAR2): CA_Project, CA_Resource, etc.
- `day_hr_cnt` (NUMBER): Hours per day

### SCHEDOPTIONS (Schedule Settings)
Scheduling calculation options per project.

**Key Fields:**
- `proj_id` (NUMBER): FK to PROJECT
- `leveldate_flag` (VARCHAR2): Y/N - level resources during scheduling
- `sched_outer_depend_type` (VARCHAR2): How to handle external dependencies
- `use_project_baseline_flag` (VARCHAR2): Y/N - use project baseline

## Common Table Relationships

### Get All Activities for a Project
```sql
SELECT
    t.task_code,
    t.task_name,
    t.target_start_date,
    t.target_end_date,
    t.total_float_hr_cnt,
    w.wbs_short_name
FROM TASK t
JOIN PROJWBS w ON t.wbs_id = w.wbs_id
WHERE t.proj_id = :project_id
ORDER BY t.target_start_date;
```

### Get Activity Predecessors
```sql
SELECT
    succ.task_code AS successor_code,
    pred.task_code AS predecessor_code,
    tp.pred_type,
    tp.lag_hr_cnt,
    tp.driving_path_flag
FROM TASKPRED tp
JOIN TASK succ ON tp.task_id = succ.task_id
JOIN TASK pred ON tp.pred_task_id = pred.task_id
WHERE succ.proj_id = :project_id;
```

### Get Critical Path Activities
```sql
SELECT
    t.task_code,
    t.task_name,
    t.target_start_date,
    t.target_end_date,
    t.total_float_hr_cnt
FROM TASK t
WHERE t.proj_id = :project_id
  AND t.total_float_hr_cnt <= 0
  AND t.status_code != 'TK_Complete'
ORDER BY t.target_start_date;
```

### Get Resource Assignments
```sql
SELECT
    t.task_code,
    r.rsrc_short_name,
    tr.target_qty,
    tr.remain_qty,
    tr.act_reg_qty
FROM TASKRSRC tr
JOIN TASK t ON tr.task_id = t.task_id
JOIN RSRC r ON tr.rsrc_id = r.rsrc_id
WHERE tr.proj_id = :project_id;
```

### Get Project Baseline Comparison
```sql
-- Requires baseline project to exist
SELECT
    curr.task_code,
    curr.task_name,
    curr.target_start_date AS current_start,
    base.target_start_date AS baseline_start,
    curr.target_end_date AS current_finish,
    base.target_end_date AS baseline_finish,
    (curr.target_end_date - base.target_end_date) AS finish_variance_days
FROM TASK curr
LEFT JOIN TASK base ON curr.task_code = base.task_code
    AND base.proj_id = :baseline_project_id
WHERE curr.proj_id = :current_project_id;
```

## Important Field Mappings

### Task Type Codes
- `TT_Task`: Task Dependent (normal activity)
- `TT_Rsrc`: Resource Dependent
- `TT_LOE`: Level of Effort
- `TT_Mile`: Start Milestone
- `TT_FinMile`: Finish Milestone
- `TT_WBS`: WBS Summary

### Relationship Types
- `PR_FS`: Finish-to-Start
- `PR_SS`: Start-to-Start
- `PR_FF`: Finish-to-Finish
- `PR_SF`: Start-to-Finish

### Constraint Types
- `CS_MSO`: Mandatory Start On
- `CS_MFO`: Mandatory Finish On
- `CS_SNLT`: Start No Later Than
- `CS_SNЕТ`: Start No Earlier Than
- `CS_FNLT`: Finish No Later Than
- `CS_FNET`: Finish No Earlier Than
- `CS_ALAP`: As Late As Possible

### Activity Status Codes
- `TK_NotStart`: Not Started
- `TK_Active`: In Progress
- `TK_Complete`: Completed

### Duration Types
- `DT_FixedDrtn`: Fixed Duration & Units/Time
- `DT_FixedQty`: Fixed Duration & Units
- `DT_FixedDUR2`: Fixed Units/Time
- `DT_FixedRate`: Fixed Units

## Notes

- All duration and float fields with `_hr_cnt` suffix are in hours
- Date fields are stored as Oracle DATE type (includes time component)
- P6 uses Y/N flags (VARCHAR2) for boolean values, not numeric 0/1
- Deleted records may still exist with `delete_flag = 'Y'` - always filter these out
- For SQLite implementation, NUMBER maps to REAL, VARCHAR2 to TEXT, DATE to TEXT (ISO format)
