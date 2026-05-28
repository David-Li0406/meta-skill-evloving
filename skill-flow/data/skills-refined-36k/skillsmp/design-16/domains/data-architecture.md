# Data Architecture Domain Invariants

Extends: [[system-invariants]]
Domain: Data pipelines, warehouses, analytics, ML systems

---

## When to Use

Load this domain for:
- Data pipelines
- Data warehouses
- Analytics systems
- ML/AI data products
- ETL processes
- Databricks projects
- Work data products

---

## Domain Invariants (22-26)

### 22. Schema Evolution Must Be Explicit

**Principle**: Every schema change must specify migration path

**Violation**: Implicit schema changes without migration strategy

**Examples**:
- ❌ "Add user_preferences column"
- ❌ "Change data type to JSON"
- ❌ "Remove deprecated field"
- ✅ "Add user_preferences JSONB: default={} + backfill_strategy(lazy_on_read) + index_after_50%_backfill"
- ✅ "Change to JSON: migrate_script.sql + validation_query + rollback_plan + zero_downtime(blue_green)"
- ✅ "Remove deprecated_field: null_for_6mo → drop_after_verification + downstream_impact(none)"

**Enforcement**: Schema changes must specify: migration_approach + validation + rollback → Otherwise REJECT

---

### 23. Data Lineage Must Be Traceable

**Principle**: Every derived value must reference its source

**Violation**: Calculated fields without source documentation

**Examples**:
- ❌ "Display calculated_score"
- ❌ "Show aggregated metrics"
- ❌ "Report total_revenue"
- ✅ "calculated_score = sum(item_scores) FROM items WHERE user_id=X AND created_at > now()-30d"
- ✅ "monthly_active_users = COUNT(DISTINCT user_id) FROM events WHERE event_date BETWEEN start_of_month AND end_of_month"
- ✅ "total_revenue = SUM(order.amount) FROM orders WHERE status='completed' AND region=X, refreshed_daily"

**Enforcement**: Derived fields must specify: source_tables + transformation_logic + time_window → Otherwise REJECT

---

### 24. Aggregation Scope Must Be Bounded

**Principle**: All aggregations must specify max cardinality

**Violation**: Unbounded group-by or joins

**Examples**:
- ❌ "Show all user events"
- ❌ "Aggregate by user"
- ❌ "Join all tables"
- ✅ "User events: last_1000 + paginated(50_per_page) + index_on(user_id, timestamp)"
- ✅ "Aggregate by user: WHERE created_at > now()-90d + max_10M_rows + timeout_5min"
- ✅ "Join: max_cardinality(1M_rows) + partition_by(date) + fallback(sample_10%)"

**Enforcement**: Aggregations must specify: time_bound + row_limit + timeout → Otherwise REJECT

---

### 25. Temporal Semantics Must Be Explicit

**Principle**: Time-based queries must specify timezone and granularity

**Violation**: Implicit time handling

**Examples**:
- ❌ "Show daily active users"
- ❌ "Calculate retention"
- ❌ "Get recent orders"
- ✅ "Daily active users: UTC_day_boundaries + dedupe_by(user_id) + created_at_index"
- ✅ "7-day retention: cohort_day_0(UTC) → active_on_day_7(UTC) → percentage_calculation"
- ✅ "Recent orders: last_24h(user_local_timezone) + display_in(user_timezone) + store_in(UTC)"

**Enforcement**: Time queries must specify: timezone + boundary_definition + deduplication → Otherwise REJECT

---

### 26. PII Must Be Declared and Protected

**Principle**: Every field with personal data must be tagged

**Violation**: PII without encryption/anonymization/access_control

**Examples**:
- ❌ "Store user email"
- ❌ "Log user activity"
- ❌ "Track user location"
- ✅ "user_email: PII + encrypted_at_rest(AES256) + access_control(admin_only) + audit_log"
- ✅ "user_activity: PII_anonymized + user_id_hashed + ip_truncated + no_full_payload"
- ✅ "user_location: PII + precision_reduced(city_level) + retention(30d) + consent_required"

**Enforcement**: PII fields must specify: encryption + access_control + retention_policy → Otherwise REJECT

---

## Data-Specific Sub-Invariants

### 26a. Data Quality Checks

- Every pipeline must have data quality assertions
- Null rate thresholds must be specified
- Schema validation at ingestion
- Freshness checks with alerting

### 26b. Partitioning Strategy

- Large tables must declare partition strategy
- Partition key must align with query patterns
- Partition pruning must be validated
- Retention policy per partition

### 26c. Idempotency for Pipelines

- All pipelines must be rerunnable
- Duplicate handling must be specified
- Checkpoint/recovery mechanism required
- Exactly-once vs at-least-once declared

### 26d. Cost Attribution

- Query costs must be attributable to teams/projects
- Resource consumption must have budgets
- Alert on budget threshold (80%)
- Optimization recommendations tracked

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 22 | Schema Evolution Must Be Explicit | Changes have migration + rollback |
| 23 | Data Lineage Must Be Traceable | Derived values show source + logic |
| 24 | Aggregation Scope Must Be Bounded | Aggregations have limits + timeouts |
| 25 | Temporal Semantics Must Be Explicit | Time queries specify timezone |
| 26 | PII Must Be Declared and Protected | Personal data tagged + protected |

---

*Domain: Data Architecture*
*Invariants: 22-26 (plus sub-invariants)*
*Use with: Core invariants 1-10*
*Often combined with: integration.md*
