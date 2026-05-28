---
name: sqlmesh-expert
description: Use when working with SQLMesh projects - creating models, reviewing plans, validating changes, debugging failures, or deploying to production environments.
---

# SQLMesh Expert Skill

This skill enables an agent to **understand SQLMesh architecture**, **implement models correctly**, **validate projects**, **review changes safely**, and **deploy with minimal risk**.

## When to use this skill

Use this skill when the task involves:

- **Implementation**: Creating or modifying SQLMesh models, audits, tests, macros, or configuration
- **Review**: Reviewing a PR/diff in a SQLMesh repo
- **Validation**: Checking that a SQLMesh project is correctly configured and runnable
- **Planning**: Producing or interpreting a `sqlmesh plan` (backfills, restatements, forward-only)
- **Comparison**: Comparing dev results to prod via `sqlmesh table_diff`
- **Debugging**: Investigating missing intervals, data gaps, audit failures, or test failures
- **Optimization**: Improving model performance, incremental strategy selection, or backfill efficiency

---

## Non-negotiable safety rules

1. **Explain-first**: Always run `sqlmesh plan --explain` before applying anything.
2. **Never run destructive commands without explicit user approval**:
   - `sqlmesh destroy` (removes warehouse objects + state)
   - `sqlmesh migrate` (impacts shared state; affects all users)
   - `sqlmesh rollback` (global-impact)
   - `sqlmesh invalidate` (removes environments)
3. **Do not leak secrets**: Never print connection strings, tokens, passwords, or credentials from configs or env vars.
4. **Prefer dev environments for iteration**: Treat prod like a museum—look, measure, update safely, don't smash.
5. **Assess blast radius**: Before applying, understand how many models will backfill and for what time range.

---

## Part 1: Architectural Foundations

Understanding SQLMesh's architecture is essential for effective debugging, optimization, and implementation decisions.

### 1.1 Declarative vs Imperative

SQLMesh operates on a **semantic understanding** of data transformation logic. Unlike traditional orchestrators (Airflow, scripts) that execute tasks in order, SQLMesh:

- Parses the **Abstract Syntax Tree (AST)** of SQL to build dependency graphs automatically
- Treats the warehouse as a **function of the code repository**
- Uses **SQLGlot** for cross-dialect transpilation and semantic analysis

Key insight: A textual change (adding a comment) does not alter the model fingerprint; a semantic change (modifying a WHERE clause) does.

### 1.2 Virtual Data Environments (VDEs)

VDEs enable **zero-downtime deployments** and **isolated development sandboxes**.

**How it works:**

1. **Fingerprinting**: Each model version gets a cryptographic hash derived from:
   - Query logic (AST)
   - Configuration
   - Fingerprints of all upstream dependencies (Merkle tree structure)

2. **Physical vs Virtual layers**:

| Layer | Naming Convention | Lifecycle |
|-------|-------------------|-----------|
| Virtual View | `target_schema.table_name` | Mutable, updated on apply |
| Physical Table | `sqlmesh__schema.table_<fingerprint>` | Immutable, persistent |
| Dev View | `target_schema__dev.table_name` | Ephemeral, per-user |
| State Tables | `sqlmesh._snapshots` | Persistent metadata |

3. **Pointer Swap Protocol**:
   - SQLMesh creates/reuses physical table matching the fingerprint
   - On apply, executes atomic `CREATE OR REPLACE VIEW` to point to correct physical table
   - Dev environments are just different views pointing to physical tables

**Agent validation rules:**
- Virtual views must always resolve to valid physical tables
- Never manually drop physical tables
- State tables are essential for lineage—do not corrupt

### 1.3 State Management and Snapshots

SQLMesh maintains internal state in a relational database, recording every model version as **Snapshots**.

**State Store considerations:**
- Modern implementations use normalized schemas (not monolithic JSON)
- For teams: Prefer Postgres/MySQL over SQLite/DuckDB (concurrency)
- The **Janitor** process handles garbage collection of expired snapshots and orphaned tables

**Diagnosing state bloat:**
- Symptom: Slow plan generation
- Solution: Run `sqlmesh janitor` or adjust `snapshot_ttl`
- Ensure janitor runs periodically (often in CI/CD)

---

## Part 2: Project Configuration

### 2.1 Project Anatomy

A typical SQLMesh project includes:

```
project/
├── config.yaml (or config.py)
├── models/           # SQL and Python model definitions
├── audits/           # Shared audits (can also be inline)
├── tests/            # Unit tests
├── macros/           # Reusable SQL macros
└── seeds/            # Static CSV data
```

### 2.2 Configuration: YAML vs Python

**YAML (`config.yaml`)**:
- Static, declarative
- Simpler, less prone to code execution risks
- Suitable for small, rigid projects

**Python (`config.py`)**:
- Dynamic, enterprise standard
- Allows environment variable injection, conditional logic
- Security risks require monitoring

**Security protocol for `config.py`:**

```python
# ANTI-PATTERN: Hardcoded secret
password = "super_secret_password"

# BEST PRACTICE: Environment variable
password = os.environ.get("DB_PASSWORD")
```

**Validation checklist:**
- [ ] No hardcoded credentials in config.py
- [ ] `.env` files in `.gitignore`
- [ ] Sensitive values come from environment variables or secret managers

### 2.3 Gateway Architecture

Gateways define how SQLMesh connects to compute engines and state stores.

| Parameter | Function | Agent Check |
|-----------|----------|-------------|
| `connection` | Compute engine (Snowflake, DuckDB, etc.) | Matches target infrastructure |
| `state_connection` | Metadata storage | Distinct for isolated systems; Postgres for teams |
| `state_schema` | SQLMesh internal tables | Default `sqlmesh`; verify write permissions |
| `scheduler` | Execution backend | Compatible with orchestration layer |

**Isolated Systems (Air-Gapped)**:
- Separate `state_connection` for dev and prod gateways
- Plan in dev cannot leverage prod data for backfill forecasting
- Synchronization happens at "promote to prod" step

### 2.4 Physical Schema Configuration

```yaml
physical_schema_mapping:
  analytics: analytics_physical

physical_table_naming_convention: schema_and_table  # or hash_md5
```

**Warning**: Changing `physical_table_naming_convention` invalidates all fingerprints, forcing complete warehouse rebuild.

---

## Part 3: The Semantic Modeling Layer

### 3.1 SQL Models

Models are defined in `.sql` files with a metadata header:

```sql
MODEL (
  name schema.model_name,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column event_date
  ),
  cron '@daily',
  start '2023-01-01',
  audits (not_null(columns=[id]))
);

SELECT
  id::INT,
  event_date::DATE,
  amount::DECIMAL(10,2)
FROM upstream.events
WHERE event_date BETWEEN @start_ds AND @end_ds
```

**Transpilation**: SQLMesh can execute SQL written in one dialect on another engine (e.g., DuckDB → Databricks).

**Best practices:**
- Explicitly cast columns in final SELECT (`::INT`, `::TEXT`)
- Verify `dialect` setting in `model_defaults`
- Run `sqlmesh plan` to validate transpilation compatibility

### 3.2 Python Models

For logic exceeding SQL expressiveness:

```python
from sqlmesh import model
import pandas as pd

@model(
    "schema.python_model",
    columns={
        "id": "INT",
        "score": "FLOAT"
    },
    depends_on=["schema.upstream_model"]
)
def execute(context, start, end, **kwargs):
    df = context.table("schema.upstream_model")
    # Process data...
    return result_df
```

**Critical rules:**
- Must return DataFrame (Pandas or Spark)
- Dependencies require explicit declaration (`depends_on` or `context.table()`)
- **Idempotency**: Never use `datetime.now()` without arguments; use `context.execution_time`

### 3.3 Macros and Jinja

Macros enable reusable logic (defined in `macros/` directory):

```sql
{% macro calculate_tax(amount, rate) %}
  {{ amount }} * {{ rate }}
{% endmacro %}
```

**Agent checks:**
- Verify macros are "pure" (return SQL strings, no side effects)
- Ensure global variables (`@VAR`) are defined in config
- Undefined variables cause compile-time errors

### 3.4 Seeds and External Models

**Seeds**: Static CSV files committed to repo
- Keep small (<100MB)
- Verify UTF-8 encoding
- Large datasets should use ETL tools + External Models

**External Models**: Data not managed by SQLMesh (raw ingestion tables)
- Act as boundary layer
- Include audits (e.g., `not_null`) to validate incoming data quality
- Create "Data Contracts" at ingestion point

---

## Part 4: Incremental Strategies

### 4.1 Strategy Selection Matrix

| Data Characteristic | Recommended Kind | Agent Check |
|---------------------|------------------|-------------|
| Immutable event stream | `INCREMENTAL_BY_TIME_RANGE` | Check `time_column` & WHERE filter |
| Mutable dimensions (updates) | `INCREMENTAL_BY_UNIQUE_KEY` | Check `unique_key` |
| Small static lookup | `FULL` or `SEED` | Check row count (< 1M rows) |
| Complex history tracking | `SCD_TYPE_2` | Verify `valid_from`/`valid_to` logic |
| Massive table schema change | `INCREMENTAL` + `forward_only` | Warn about historical inconsistency |

### 4.2 INCREMENTAL_BY_TIME_RANGE

Most efficient for large-scale event processing:

```sql
MODEL (
  name schema.events,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column event_date
  ),
  cron '@daily',
  start '2023-01-01'
);

SELECT * FROM raw.events
WHERE event_date BETWEEN @start_ds AND @end_ds  -- REQUIRED
```

**Validation rule**: If kind is `INCREMENTAL_BY_TIME_RANGE`, the WHERE clause MUST filter by the time column. Without this, full table scans occur on every run.

**Data gaps**: SQLMesh tracks specific intervals. If Tuesday fails but Wednesday succeeds, Tuesday is marked missing and will be filled on next run.

### 4.3 INCREMENTAL_BY_UNIQUE_KEY

For datasets with record updates (not just appends):

```sql
MODEL (
  name schema.users,
  kind INCREMENTAL_BY_UNIQUE_KEY (
    unique_key user_id
  )
);
```

Uses MERGE (upsert) operations.

**Validation**: Verify `unique_key` is truly unique. Duplicate keys cause non-deterministic behavior. Add `unique_values` audit on key columns.

### 4.4 Forward-Only Models

For massive tables where full backfill is impractical:

```sql
MODEL (
  name schema.huge_table,
  kind INCREMENTAL_BY_TIME_RANGE (...),
  on_destructive_change allow
);
```

**Critical warnings:**
- Breaks semantic consistency (data is not a pure function of code)
- New columns are NULL for historical data
- Dropped columns cause query failures for old data
- Require explicit `on_destructive_change: allow`
- Downstream models must handle potential schema mismatches

---

## Part 5: Quality Assurance

### 5.1 Unit Tests

Tests are defined in `tests/` directory as YAML:

```yaml
test_order_total:
  model: schema.orders
  inputs:
    raw.order_items:
      - {order_id: 1, quantity: 2, price: 10.00}
      - {order_id: 1, quantity: 1, price: 5.00}
  outputs:
    query:
      - {order_id: 1, total: 25.00}
```

**Best practices:**
- Every model with complex logic should have tests
- Use static dates (e.g., `'2023-01-01'`) not `CURRENT_DATE()`
- Test individual CTEs for large models
- Run tests: `sqlmesh test` or `sqlmesh test -k <pattern>`

### 5.2 Audits

Audits validate data contracts. A query returning zero rows = pass.

```sql
MODEL (
  name schema.orders,
  audits (
    not_null(columns=[order_id, customer_id]),
    unique_values(columns=[order_id]),
    accepted_values(column=status, is_in=['pending', 'shipped', 'delivered'])
  )
);
```

**Types:**
- **Blocking** (default): Failed audit stops the pipeline
- **Non-blocking**: Warnings only (useful for statistical anomalies)

**Standard audits to enforce:**
- `not_null` on critical keys
- `unique_values` on primary keys
- `accepted_values` for enum fields
- Domain-specific assertions

Run explicitly: `sqlmesh audit` or `sqlmesh audit --model <schema.model>`

### 5.3 Table Diff

Compare candidate model against production:

```bash
sqlmesh table_diff prod:dev schema.model_name
```

**Options:**
```bash
# Specify join keys if grain not defined
sqlmesh table_diff prod:dev schema.model -o key1 -o key2

# Show sample rows (can be wide)
sqlmesh table_diff prod:dev schema.model --show-sample

# Control decimal precision for floats
sqlmesh table_diff prod:dev schema.model --decimals 3

# Skip expected-to-differ columns
sqlmesh table_diff prod:dev schema.model -s updated_at -s ingested_at
```

**Interpreting results:**
- **Zero diff**: Ideal for refactoring (code change, same logic)
- **Expected diff**: Logic changed; diff should be explainable
- **Unexpected diff**: Large variance without clear reason = red flag

---

## Part 6: Core Workflow (Dev → Validate → Prod)

### Step 1: Preflight Validation

```bash
# Project info and connection check
sqlmesh info
# or without warehouse:
sqlmesh info --skip-connection

# Lint all models
sqlmesh lint

# Run unit tests
sqlmesh test

# Optional: formatting check
sqlmesh format --check

# Optional: DAG visualization
sqlmesh dag dag.html
```

### Step 2: Generate and Review Dev Plan

```bash
sqlmesh plan dev --explain
```

**Extract and summarize:**
- Which models changed (direct + downstream impact)
- Change category (breaking/non-breaking/forward-only)
- Backfill scope (models, time range, compute cost)
- Restatement presence (`--restate-model`)

**Key flags:**
- `--no-gaps`: Ensure no interval gaps
- `--skip-backfill` / `--dry-run`: Create plan without computing
- `--diff-rendered`: Diff rendered SQL
- `--no-prompts`: CI mode

### Step 3: Apply to Dev (only when explicitly requested)

```bash
sqlmesh plan dev
```

Audits run automatically. Failed audits = stop-the-line signal.

### Step 4: Validate Outputs

```bash
# Run audits explicitly
sqlmesh audit

# Run tests
sqlmesh test

# Diff dev vs prod (most important safety check)
sqlmesh table_diff prod:dev schema.model_name
```

### Step 5: Promote to Prod

```bash
# Explain first
sqlmesh plan --explain
# or:
sqlmesh plan prod --explain

# Apply after review
sqlmesh plan
# or:
sqlmesh plan prod

# Optional: run latest intervals as part of plan
sqlmesh plan --run
```

---

## Part 7: Special Scenarios

### 7.1 Restatements

Recompute historical intervals for existing models:

```bash
# Explain first
sqlmesh plan prod --restate-model schema.model --explain

# Apply
sqlmesh plan prod --restate-model schema.model
```

**Gotchas:**
- Restatement **cascades downstream** (expect bigger blast radius)
- Cannot restate a model new to the environment; it must already exist

### 7.2 Forward-Only Deployments

Trade historical backfill for deploy practicality:

```bash
# Explain first
sqlmesh plan prod --forward-only --explain

# Apply if approved
sqlmesh plan prod --forward-only
```

**Notes:**
- Avoids backfills
- History won't be recomputed—validate with targeted diffs and audits
- May use temporary tables/shallow clones depending on engine

### 7.3 Backfill Optimization

For large datasets:

```sql
MODEL (
  name schema.large_model,
  kind INCREMENTAL_BY_TIME_RANGE (...),
  batch_size 30  -- Process in monthly chunks
);
```

**Guidance:**
- Set `batch_size` to prevent OOM errors
- SQLMesh runs backfills in parallel where dependencies allow
- Check dependency chains to maximize parallelism

---

## Part 8: Operational Commands

### Generally Safe

```bash
# List environments
sqlmesh environments

# Check missing intervals
sqlmesh check_intervals prod

# Run missing intervals
sqlmesh run prod
```

### High-Risk (require explicit approval)

```bash
# Invalidate environment (removes via janitor)
sqlmesh invalidate <env>

# Janitor cleanup
sqlmesh janitor

# Global state changes
sqlmesh migrate
sqlmesh rollback

# Nuclear option
sqlmesh destroy
```

---

## Part 9: Troubleshooting and Anti-Patterns

### 9.1 The "Cron Inference" Trap

**Symptom**: Model fails or backfills from beginning of time unexpectedly.
**Cause**: Incremental model has `cron` but no explicit `start` date.
**Fix**: Every incremental model must have an explicit `start` date string.

### 9.2 DuckDB Concurrency Locks

**Symptom**: "Database lock" errors during local dev or CI.
**Cause**: Multiple processes writing to local DuckDB state file (single-writer).
**Fix**: Use server-based state store (Postgres/MySQL) for teams; close other connections locally.

### 9.3 Infinite Loops in Recursive CTEs

**Symptom**: Plan generation hangs indefinitely.
**Cause**: `WITH RECURSIVE` block without proper termination condition.
**Fix**: Statically analyze recursive blocks; ensure bounded recursion depth.

### 9.4 Mutable External Inputs

**Symptom**: Data quality issues despite no code changes.
**Cause**: Model queries raw table directly without defining as EXTERNAL model.
**Fix**: All external inputs must be defined as EXTERNAL models to capture schema in fingerprint.

### 9.5 SELECT * in Production

**Symptom**: Performance degradation, fragile dependencies.
**Cause**: `SELECT *` creates implicit dependencies on all columns.
**Fix**: Enforce explicit column selection—reduces I/O, makes dependency graph precise.

### 9.6 Destructive Changes

**Symptom**: Deployment fails or downstream reports break.
**Cause**: Column dropped or renamed.
**Protocol**:
- Check `on_destructive_change` setting
- If set to `error` (default), plan is blocked
- For intentional drops: explicit acknowledgment or forward-only plan
- Recommend view models to alias columns for deprecation

### 9.7 Python Model Non-Idempotency

**Symptom**: Re-running model for past date produces different results.
**Cause**: Python model uses `datetime.now()` instead of execution context.
**Fix**: Replace with `context.execution_time` or use execution-provided timestamps.

---

## Part 10: Decision Matrices

### 10.1 Plan Validation Matrix

| Change Type | Detection Logic | Action Required | Risk Level |
|-------------|-----------------|-----------------|------------|
| Logic Change | AST difference in query | Run table_diff, check backfill cost | Medium |
| Breaking Change | Affects downstream result | Alert user to cascade effect | High |
| Non-Breaking | Additive (e.g., new column) | Verify forward_only eligibility | Low |
| Destructive | Drop column / change type | Block unless `on_destructive_change: allow` | Critical |
| Config Change | `cron` or `owner` change | Update metadata (Virtual Update) | Negligible |

### 10.2 Model Optimization Heuristics

| Observation | Diagnosis | Recommendation |
|-------------|-----------|----------------|
| INCREMENTAL model lacks WHERE clause | Full table scan (inefficient) | Add `WHERE time_col BETWEEN @start_ds AND @end_ds` |
| `batch_size` missing for large table | Potential OOM risk | Set `batch_size` (e.g., 30) |
| `unique_key` uses high-cardinality columns | Slow merge performance | Check clustering/partitioning keys |
| Python model calls `datetime.now()` | Non-idempotent | Replace with `context.execution_time` |
| Raw table in FROM clause | Unmanaged dependency | Define as EXTERNAL model |

---

## Part 11: Report Templates

### A) Project Validation Report

```markdown
## Project Validation Report

### What I Checked
- [ ] Config present and valid
- [ ] Required directories exist (models/, etc.)
- [ ] `sqlmesh info` results (models count, connection status)
- [ ] Lint status
- [ ] Test status

### Findings
- Key risks:
- Missing elements:

### Recommendations (priority order)
1. ...
2. ...
```

### B) Plan Review Report

```markdown
## Plan Review Report

### Plan Target
- Environment: dev / prod

### Change Summary
- Direct model edits:
- Downstream impact:
- Change categorization: breaking / non-breaking / forward-only

### Backfill/Restatement
- Models:
- Time range:
- Expected compute cost:

### Validation Evidence
- Audits: pass / fail
- Tests: pass / fail
- table_diff highlights:

### Go/No-Go Decision
- Decision:
- Justification:
- Risks:
```

---

## Reference Links

- [SQLMesh CLI Reference](https://sqlmesh.readthedocs.io/en/stable/reference/cli/)
- [Plans](https://sqlmesh.readthedocs.io/en/latest/concepts/plans/)
- [Audits](https://sqlmesh.readthedocs.io/en/latest/concepts/audits/)
- [Tests](https://sqlmesh.readthedocs.io/en/latest/concepts/tests/)
- [Table Diff Guide](https://sqlmesh.readthedocs.io/en/stable/guides/tablediff/)
- [Configuration Guide](https://sqlmesh.readthedocs.io/en/stable/guides/configuration/)
- [Project Structure Guide](https://sqlmesh.readthedocs.io/en/latest/guides/projects/)
- [Model Kinds](https://sqlmesh.readthedocs.io/en/stable/concepts/models/model_kinds/)
