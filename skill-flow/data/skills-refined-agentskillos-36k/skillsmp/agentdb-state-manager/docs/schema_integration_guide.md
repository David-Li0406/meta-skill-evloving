---
type: technical-documentation
title: "AgentDB Sync Schema Integration Guide"
schema_version: "1.0.0"
created: "2025-11-16"
issue: "#159"
phase: "Phase 1 - Database Schema Implementation"
---

# AgentDB Sync Schema Integration Guide

## Table of Contents

1. [Overview](#1-overview)
2. [Schema Initialization](#2-schema-initialization)
3. [Schema Architecture](#3-schema-architecture)
4. [Common Use Cases](#4-common-use-cases)
5. [Query Examples](#5-query-examples)
6. [Performance Considerations](#6-performance-considerations)
7. [Migration from Existing AgentDB](#7-migration-from-existing-agentdb)
8. [Rollback Procedures](#8-rollback-procedures)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Overview

The AgentDB Sync Schema implements the **MIT Agent Synchronization Pattern** with full healthcare compliance (HIPAA/FDA/IRB). It provides three core tables for tracking agent synchronization operations, detailed execution logs, and immutable audit trails.

**Academic Reference:**
> Meng, E., & Jackson, D. (2025). "What You See Is What It Does: A Structural Pattern for Legible Software."
> *Onward! at SPLASH 2025*. arXiv:2508.14511v1. https://arxiv.org/abs/2508.14511

### 1.1 Key Features

- **Multi-agent coordination:** Track synchronization across agents and worktrees
- **Healthcare compliance:** HIPAA/FDA/IRB compliant audit trails
- **Idempotent operations:** Checksum-based conflict detection
- **Performance optimized:** Comprehensive indexes for common queries
- **Forensic capability:** Complete event logging with JSON metadata

### 1.2 Design Principles

- **Immutable audit trail:** APPEND-ONLY for `sync_audit_trail` (FDA 21 CFR Part 11)
- **PHI tracking:** Comprehensive Protected Health Information access logging
- **Foreign key integrity:** Referential consistency between tables
- **Extensible metadata:** JSON fields for future requirements

---

## 2. Schema Initialization

### 2.1 Prerequisites

**Required:**
- DuckDB installed (`uv add duckdb` or `pip install duckdb`)
- Schema file: `.claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql`

**Optional:**
- Existing AgentDB database (for migration - see §7)

### 2.2 Initialize New Database

**Method 1: Python Script (Recommended)**

```python
#!/usr/bin/env python3
"""Initialize AgentDB Sync Schema"""

import duckdb
from pathlib import Path

# Paths
SCHEMA_FILE = Path(".claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql")
DB_PATH = Path(".claude/agentdb/sync_database.db")

# Create database directory
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Connect and initialize
conn = duckdb.connect(str(DB_PATH))
schema_sql = SCHEMA_FILE.read_text()
conn.execute(schema_sql)

# Verify initialization
result = conn.execute("""
    SELECT * FROM schema_metadata WHERE schema_name = 'agentdb_sync_schema'
""").fetchone()

if result:
    print(f"✓ Schema initialized: {result[1]} (version {result[2]})")
else:
    print("✗ Schema initialization failed")

conn.close()
```

**Method 2: DuckDB CLI**

```bash
# Create database and load schema
duckdb .claude/agentdb/sync_database.db < .claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql

# Verify initialization
duckdb .claude/agentdb/sync_database.db -c "SELECT * FROM schema_metadata;"
```

### 2.3 Verify Initialization

Run the validation query included in the schema:

```sql
SELECT
    'Schema validation complete' AS status,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'agent_synchronizations') AS table_agent_sync,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'sync_executions') AS table_sync_exec,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'sync_audit_trail') AS table_audit,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'schema_metadata') AS table_metadata
WHERE
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'agent_synchronizations') = 1
    AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'sync_executions') = 1
    AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'sync_audit_trail') = 1
    AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'schema_metadata') = 1;
```

**Expected output:** Single row with all counts = 1

---

## 3. Schema Architecture

### 3.1 Entity Relationship Diagram (ASCII)

```
┌─────────────────────────────────┐
│   agent_synchronizations        │
│─────────────────────────────────│
│ PK: sync_id (VARCHAR)           │
│     agent_id                    │
│     worktree_path               │
│     sync_type                   │
│     source_location             │
│     target_location             │
│     pattern                     │
│     status                      │
│     created_at                  │
│     completed_at                │
│     created_by                  │
│     metadata (JSON)             │
└─────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────┐
│      sync_executions            │
│─────────────────────────────────│
│ PK: execution_id (VARCHAR)      │
│ FK: sync_id ─────────┘          │
│     execution_order             │
│     operation_type              │
│     file_path                   │
│     phi_accessed                │
│     phi_justification           │
│     operation_result            │
│     error_message               │
│     started_at                  │
│     completed_at                │
│     duration_ms                 │
│     checksum_before             │
│     checksum_after              │
│     metadata (JSON)             │
└─────────────────────────────────┘
         │
         │ 1:N (optional)
         ▼
┌─────────────────────────────────┐
│     sync_audit_trail            │
│─────────────────────────────────│
│ PK: audit_id (VARCHAR)          │
│ FK: sync_id ─────────┘          │
│ FK: execution_id (optional)     │
│     event_type                  │
│     actor                       │
│     actor_role                  │
│     timestamp                   │
│     phi_involved                │
│     compliance_context (JSON)   │
│     event_details (JSON)        │
│     ip_address                  │
│     session_id                  │
└─────────────────────────────────┘
    (APPEND-ONLY - FDA 21 CFR Part 11)
```

### 3.2 Table Descriptions

#### Table 1: `agent_synchronizations`

**Purpose:** Master registry of all synchronization events

**Key Fields:**
- `sync_id` (PK): Unique identifier (UUIDv4)
- `pattern`: Synchronization pattern (e.g., 'todo_bidirectional', 'planning_readonly')
- `status`: Lifecycle state (pending → in_progress → completed/failed/rolled_back)
- `worktree_path`: Git worktree path (NULL for main repo)

**Status Lifecycle:**
```
pending → in_progress → completed
                     ├→ failed
                     └→ rolled_back
```

#### Table 2: `sync_executions`

**Purpose:** Detailed execution log (one-to-many with `agent_synchronizations`)

**Key Fields:**
- `execution_order`: Sequence number for deterministic replay
- `phi_accessed`: Boolean flag for HIPAA compliance
- `checksum_before/after`: SHA-256 for idempotency
- `duration_ms`: Performance metric

**Operation Types:**
- `read`: Read file/data
- `write`: Write file/data
- `delete`: Delete file/data
- `validate`: Validate data integrity
- `transform`: Transform data format
- `merge`: Merge conflicting data
- `rollback`: Reverse previous operation

#### Table 3: `sync_audit_trail`

**Purpose:** Immutable audit log (HIPAA/FDA/IRB compliance)

**Key Fields:**
- `event_type`: 13 audit event types (sync_initiated, phi_accessed, etc.)
- `compliance_context`: JSON with consent, IRB protocol, legal basis
- `timestamp`: Immutable UTC timestamp
- `phi_involved`: Boolean flag for PHI events

**CRITICAL:** This table is APPEND-ONLY. Never UPDATE or DELETE.

### 3.3 Indexes

**Performance-critical indexes:**

| Index Name | Table | Columns | Purpose |
|------------|-------|---------|---------|
| `idx_sync_agent_status` | agent_synchronizations | (agent_id, status) | Find in-progress syncs |
| `idx_exec_sync` | sync_executions | (sync_id, execution_order) | Ordered execution retrieval |
| `idx_audit_sync` | sync_audit_trail | (sync_id, timestamp DESC) | Chronological audit trail |
| `idx_audit_phi_actor_time` | sync_audit_trail | (phi_involved, actor, timestamp) | HIPAA compliance queries |

**See schema file for complete index list (20+ indexes).**

### 3.4 Views

Four pre-built views for common queries:

1. **`v_current_sync_status`**: Current status of all syncs with execution counts
2. **`v_phi_access_audit`**: HIPAA-compliant PHI access report
3. **`v_sync_performance`**: Performance metrics by pattern and type
4. **`v_failed_operations`**: Failed operations requiring investigation

---

## 4. Common Use Cases

### 4.1 Use Case 1: Bidirectional TODO File Synchronization

**Scenario:** Synchronize TODO_feature_*.md between main repo and worktree

**Steps:**

1. **Create synchronization record:**
```python
import uuid
from datetime import datetime, timezone

sync_id = str(uuid.uuid4())
conn.execute("""
    INSERT INTO agent_synchronizations (
        sync_id, agent_id, worktree_path, sync_type,
        source_location, target_location, pattern, status, created_by
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    sync_id,
    'agent-001',
    '../german_feature_auth',
    'file_update',
    '../TODO_feature_20251116_auth.md',
    'worktree/TODO_feature_20251116_auth.md',
    'todo_bidirectional',
    'pending',
    'claude-code'
])
```

2. **Log audit event:**
```python
import json

audit_id = str(uuid.uuid4())
conn.execute("""
    INSERT INTO sync_audit_trail (
        audit_id, sync_id, event_type, actor, actor_role,
        timestamp, phi_involved, compliance_context, event_details
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    audit_id,
    sync_id,
    'sync_initiated',
    'claude-code',
    'autonomous_agent',
    datetime.now(timezone.utc),
    False,
    json.dumps({
        "purpose": "Synchronize workflow state for feature development",
        "legal_basis": "Normal development operations",
        "data_minimization": "No PHI involved"
    }),
    json.dumps({
        "sync_pattern": "todo_bidirectional",
        "worktree": "../german_feature_auth"
    })
])
```

3. **Execute synchronization operations:**
```python
# Read operation
exec_id_read = str(uuid.uuid4())
conn.execute("""
    INSERT INTO sync_executions (
        execution_id, sync_id, execution_order, operation_type,
        file_path, phi_accessed, operation_result, started_at,
        completed_at, duration_ms, checksum_before
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    exec_id_read, sync_id, 1, 'read',
    '../TODO_feature_20251116_auth.md',
    False, 'success',
    datetime.now(timezone.utc), datetime.now(timezone.utc),
    45, 'sha256:abc123...'
])

# Write operation
exec_id_write = str(uuid.uuid4())
conn.execute("""
    INSERT INTO sync_executions (
        execution_id, sync_id, execution_order, operation_type,
        file_path, phi_accessed, operation_result, started_at,
        completed_at, duration_ms, checksum_before, checksum_after
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    exec_id_write, sync_id, 2, 'write',
    'worktree/TODO_feature_20251116_auth.md',
    False, 'success',
    datetime.now(timezone.utc), datetime.now(timezone.utc),
    65, 'sha256:abc123...', 'sha256:abc123...'
])
```

4. **Mark synchronization complete:**
```python
conn.execute("""
    UPDATE agent_synchronizations
    SET status = 'completed', completed_at = ?
    WHERE sync_id = ?
""", [datetime.now(timezone.utc), sync_id])

# Log completion audit event
audit_id_complete = str(uuid.uuid4())
conn.execute("""
    INSERT INTO sync_audit_trail (
        audit_id, sync_id, event_type, actor, actor_role,
        timestamp, phi_involved, compliance_context, event_details
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    audit_id_complete, sync_id, 'sync_completed',
    'claude-code', 'autonomous_agent',
    datetime.now(timezone.utc), False,
    json.dumps({"purpose": "Completion of TODO sync"}),
    json.dumps({"execution_count": 2, "total_duration_ms": 110})
])
```

### 4.2 Use Case 2: PHI-Involving Synchronization with HIPAA Compliance

**Scenario:** Synchronize patient data with full audit trail

**Key differences from Use Case 1:**
- Set `phi_accessed = TRUE` in sync_executions
- Provide `phi_justification` (required when phi_accessed = TRUE)
- Set `phi_involved = TRUE` in sync_audit_trail
- Include detailed compliance_context (consent_id, irb_protocol, etc.)

**Example execution:**
```python
exec_id = str(uuid.uuid4())
conn.execute("""
    INSERT INTO sync_executions (
        execution_id, sync_id, execution_order, operation_type,
        file_path, phi_accessed, phi_justification,
        operation_result, started_at, completed_at, duration_ms
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    exec_id, sync_id, 1, 'read',
    'data/patient_records.csv',
    True,  # PHI accessed
    'Required to analyze patient outcomes for IRB-2025-123 research protocol',
    'success',
    datetime.now(timezone.utc), datetime.now(timezone.utc), 120
])

# Audit trail with PHI compliance
audit_id = str(uuid.uuid4())
conn.execute("""
    INSERT INTO sync_audit_trail (
        audit_id, sync_id, execution_id, event_type,
        actor, actor_role, timestamp, phi_involved,
        compliance_context, event_details
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    audit_id, sync_id, exec_id, 'phi_accessed',
    'researcher-001', 'human_user',
    datetime.now(timezone.utc), True,
    json.dumps({
        "purpose": "Analyze patient outcomes for cardiovascular study",
        "legal_basis": "HIPAA research authorization",
        "consent_id": "CONSENT-2025-001",
        "irb_protocol": "IRB-2025-123",
        "data_minimization": "Only accessed aggregate statistics, no individual identifiers"
    }),
    json.dumps({
        "file": "patient_records.csv",
        "record_count": 150,
        "phi_fields": ["patient_id", "diagnosis_code"]
    })
])
```

### 4.3 Use Case 3: Idempotent Synchronization with Conflict Detection

**Scenario:** Detect if file already synchronized using checksums

**Pattern:**
1. Calculate checksum_before (source file)
2. Query for existing sync with same checksum
3. If checksum matches, skip operation (already synchronized)
4. If checksum differs, perform sync and log new checksum_after

**Example:**
```python
import hashlib

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return f"sha256:{sha256.hexdigest()}"

# Check for existing sync
source_file = '../TODO_feature_auth.md'
checksum_before = calculate_checksum(source_file)

existing_sync = conn.execute("""
    SELECT e.checksum_after
    FROM sync_executions e
    JOIN agent_synchronizations s ON e.sync_id = s.sync_id
    WHERE s.source_location = ?
      AND s.status = 'completed'
      AND e.operation_type = 'write'
    ORDER BY e.completed_at DESC
    LIMIT 1
""", [source_file]).fetchone()

if existing_sync and existing_sync[0] == checksum_before:
    print("✓ File already synchronized (checksum match)")
    # Skip operation, log as 'skipped'
    exec_id = str(uuid.uuid4())
    conn.execute("""
        INSERT INTO sync_executions (
            execution_id, sync_id, execution_order, operation_type,
            file_path, phi_accessed, operation_result,
            started_at, completed_at, duration_ms,
            checksum_before, checksum_after
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        exec_id, sync_id, 1, 'validate',
        source_file, False, 'skipped',
        datetime.now(timezone.utc), datetime.now(timezone.utc), 5,
        checksum_before, checksum_before
    ])
else:
    print("⚠ File changed, performing synchronization")
    # Perform sync operation
```

---

## 5. Query Examples

### 5.1 Find All In-Progress Synchronizations for an Agent

```sql
SELECT
    sync_id,
    sync_type,
    pattern,
    source_location,
    target_location,
    created_at
FROM agent_synchronizations
WHERE agent_id = 'agent-001'
  AND status = 'in_progress'
ORDER BY created_at ASC;
```

### 5.2 Get Complete Execution History for a Sync

```sql
SELECT
    e.execution_order,
    e.operation_type,
    e.file_path,
    e.operation_result,
    e.duration_ms,
    e.started_at
FROM sync_executions e
WHERE e.sync_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY e.execution_order ASC;
```

### 5.3 HIPAA-Compliant PHI Access Report

```sql
-- Use pre-built view
SELECT * FROM v_phi_access_audit
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
ORDER BY timestamp DESC;

-- Or custom query
SELECT
    a.timestamp,
    a.actor,
    a.actor_role,
    a.event_type,
    e.file_path,
    e.phi_justification,
    a.compliance_context->>'consent_id' AS consent_id,
    a.compliance_context->>'irb_protocol' AS irb_protocol
FROM sync_audit_trail a
LEFT JOIN sync_executions e ON a.execution_id = e.execution_id
WHERE a.phi_involved = TRUE
  AND a.timestamp >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
ORDER BY a.timestamp DESC;
```

### 5.4 Performance Analysis: Slowest Synchronizations

```sql
SELECT
    s.sync_id,
    s.pattern,
    s.sync_type,
    COUNT(e.execution_id) AS execution_count,
    SUM(e.duration_ms) AS total_duration_ms,
    AVG(e.duration_ms) AS avg_execution_ms
FROM agent_synchronizations s
JOIN sync_executions e ON s.sync_id = e.sync_id
WHERE s.status = 'completed'
GROUP BY s.sync_id, s.pattern, s.sync_type
ORDER BY total_duration_ms DESC
LIMIT 10;
```

### 5.5 Find Failed Operations Requiring Investigation

```sql
-- Use pre-built view
SELECT * FROM v_failed_operations
ORDER BY started_at DESC
LIMIT 20;

-- Or custom query
SELECT
    e.execution_id,
    e.sync_id,
    s.pattern,
    e.operation_type,
    e.file_path,
    e.error_message,
    e.started_at
FROM sync_executions e
JOIN agent_synchronizations s ON e.sync_id = s.sync_id
WHERE e.operation_result = 'failure'
ORDER BY e.started_at DESC;
```

### 5.6 Audit Trail for Specific File

```sql
SELECT
    a.timestamp,
    a.event_type,
    a.actor,
    e.operation_type,
    e.operation_result,
    e.checksum_after
FROM sync_audit_trail a
JOIN sync_executions e ON a.execution_id = e.execution_id
WHERE e.file_path = '../TODO_feature_20251116_auth.md'
ORDER BY a.timestamp DESC;
```

### 5.7 Synchronization Success Rate by Pattern

```sql
-- Use pre-built view
SELECT * FROM v_sync_performance
ORDER BY total_syncs DESC;

-- Or custom query
SELECT
    pattern,
    sync_type,
    COUNT(*) AS total_syncs,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS successful,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed,
    ROUND(100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate
FROM agent_synchronizations
GROUP BY pattern, sync_type
ORDER BY total_syncs DESC;
```

---

## 6. Performance Considerations

### 6.1 Index Usage Recommendations

**Always use indexed columns in WHERE clauses:**

✅ **Good (uses index):**
```sql
SELECT * FROM agent_synchronizations WHERE agent_id = 'agent-001';
SELECT * FROM sync_executions WHERE sync_id = '...';
SELECT * FROM sync_audit_trail WHERE phi_involved = TRUE;
```

❌ **Bad (table scan):**
```sql
SELECT * FROM agent_synchronizations WHERE metadata->>'priority' = 'high';
SELECT * FROM sync_executions WHERE error_message LIKE '%timeout%';
```

### 6.2 Query Optimization Tips

1. **Use composite indexes:**
   - `idx_sync_agent_status` for `WHERE agent_id = ? AND status = ?`
   - `idx_audit_phi_actor_time` for PHI compliance queries

2. **Limit result sets:**
   - Always use `LIMIT` for large tables
   - Use pagination for user-facing queries

3. **Avoid SELECT *:**
   - Specify only needed columns
   - Reduces memory usage and network transfer

4. **Use views for complex queries:**
   - Pre-built views are optimized
   - Reduces query complexity in application code

### 6.3 Performance Benchmarks (Estimated)

| Operation | Row Count | Query Time | Notes |
|-----------|-----------|------------|-------|
| Single sync lookup (by sync_id) | N/A | < 1ms | Primary key lookup |
| Agent sync list (by agent_id) | 1,000 syncs | ~5ms | Uses idx_sync_agent |
| PHI access report (30 days) | 10,000 audits | ~50ms | Uses idx_audit_phi_actor_time |
| Performance analysis (all syncs) | 100,000 syncs | ~200ms | Aggregate query with JOINs |

**Optimization target:** Keep all queries < 100ms for responsive application performance.

### 6.4 Maintenance Recommendations

1. **Periodic vacuum (DuckDB):**
   ```sql
   VACUUM;
   ANALYZE;
   ```

2. **Monitor audit trail growth:**
   - Audit trail can grow large over time
   - Consider archiving old audit records (>1 year) to separate database

3. **Index health checks:**
   - DuckDB handles indexes automatically
   - No manual index rebuilding required

---

## 7. Migration from Existing AgentDB

### 7.1 Migration Strategy

**Scenario:** You have existing `workflow_records` table from agentdb-state-manager v1.0.0

**Strategy:** Parallel operation (both schemas coexist)

**Steps:**

1. **Install new schema in same database:**
   ```python
   # Existing database already has workflow_records table
   conn = duckdb.connect('.claude/agentdb/database.db')

   # Load sync schema (adds 3 new tables)
   schema_sql = Path('schemas/agentdb_sync_schema.sql').read_text()
   conn.execute(schema_sql)

   # Verify both schemas exist
   tables = conn.execute("""
       SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'main'
   """).fetchall()

   print("Tables:", [t[0] for t in tables])
   # Expected: ['workflow_records', 'agent_synchronizations', 'sync_executions', 'sync_audit_trail', 'schema_metadata']
   ```

2. **No data migration required:**
   - `workflow_records` continues to track workflow state
   - New sync schema tracks agent synchronization operations
   - Different purposes, coexist peacefully

3. **Update application code:**
   - Add sync tracking to synchronization operations
   - Continue using `workflow_records` for workflow state
   - Use sync schema for agent coordination

### 7.2 Migration Testing

```python
# Test migration script
import duckdb

conn = duckdb.connect('.claude/agentdb/database.db')

# Verify old table still works
old_count = conn.execute("SELECT COUNT(*) FROM workflow_records").fetchone()[0]
print(f"workflow_records: {old_count} records")

# Verify new tables exist
new_tables = ['agent_synchronizations', 'sync_executions', 'sync_audit_trail']
for table in new_tables:
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} records")

conn.close()
```

### 7.3 Rollback Strategy (If Migration Fails)

**Safe rollback:** Drop only new tables

```sql
-- Rollback: Remove sync schema tables
DROP TABLE IF EXISTS sync_audit_trail;
DROP TABLE IF EXISTS sync_executions;
DROP TABLE IF EXISTS agent_synchronizations;
DROP TABLE IF EXISTS schema_metadata;

-- Verify workflow_records still exists
SELECT COUNT(*) FROM workflow_records;
```

**No data loss:** Old workflow_records table is never modified during migration.

---

## 8. Rollback Procedures

### 8.1 Complete Schema Removal

**Scenario:** Need to remove sync schema entirely

```sql
-- Drop all sync schema tables (in dependency order)
DROP VIEW IF EXISTS v_failed_operations;
DROP VIEW IF EXISTS v_sync_performance;
DROP VIEW IF EXISTS v_phi_access_audit;
DROP VIEW IF EXISTS v_current_sync_status;

DROP TABLE IF EXISTS sync_audit_trail;
DROP TABLE IF EXISTS sync_executions;
DROP TABLE IF EXISTS agent_synchronizations;
DROP TABLE IF EXISTS schema_metadata;
```

**Verification:**
```sql
SELECT table_name FROM information_schema.tables
WHERE table_name LIKE '%sync%' OR table_name = 'schema_metadata';
-- Should return 0 rows
```

### 8.2 Partial Rollback (Data Cleanup)

**Scenario:** Keep schema, remove all data

```sql
-- DANGEROUS: Removes all synchronization data
-- Use only for testing or complete reset

DELETE FROM sync_audit_trail;
DELETE FROM sync_executions;
DELETE FROM agent_synchronizations;
DELETE FROM schema_metadata WHERE schema_name = 'agentdb_sync_schema';

-- Reset schema metadata
INSERT INTO schema_metadata (schema_name, schema_version, applied_by, description)
VALUES (
    'agentdb_sync_schema',
    '1.0.0',
    'claude-code',
    'Reset after data cleanup'
);
```

### 8.3 Rollback Testing

Always test rollback in non-production environment:

```python
# Test rollback script
import duckdb
from pathlib import Path

# Create test database
test_db = Path('test_rollback.db')
conn = duckdb.connect(str(test_db))

# Initialize schema
schema_sql = Path('schemas/agentdb_sync_schema.sql').read_text()
conn.execute(schema_sql)

# Insert test data
conn.execute("""
    INSERT INTO agent_synchronizations (
        sync_id, agent_id, sync_type, source_location,
        target_location, pattern, status, created_by
    ) VALUES ('test-sync', 'agent-test', 'file_update',
              '/src', '/tgt', 'test', 'completed', 'test')
""")

# Verify data exists
count_before = conn.execute("SELECT COUNT(*) FROM agent_synchronizations").fetchone()[0]
print(f"Before rollback: {count_before} syncs")

# Execute rollback
conn.execute("DROP TABLE IF EXISTS sync_audit_trail")
conn.execute("DROP TABLE IF EXISTS sync_executions")
conn.execute("DROP TABLE IF EXISTS agent_synchronizations")

# Verify rollback
try:
    conn.execute("SELECT COUNT(*) FROM agent_synchronizations")
    print("✗ Rollback failed: table still exists")
except:
    print("✓ Rollback successful: tables removed")

conn.close()
test_db.unlink()
```

---

## 9. Troubleshooting

### 9.1 Common Issues

#### Issue 1: Foreign Key Constraint Violation

**Error:**
```
duckdb.ConstraintException: Constraint Error: Violates foreign key constraint
```

**Cause:** Attempting to insert into `sync_executions` or `sync_audit_trail` with non-existent `sync_id`

**Solution:**
1. Verify parent sync exists:
   ```sql
   SELECT sync_id FROM agent_synchronizations WHERE sync_id = '...';
   ```
2. Create parent sync first, then child records

#### Issue 2: CHECK Constraint Violation

**Error:**
```
duckdb.ConstraintException: CHECK constraint failed
```

**Cause:** Invalid value for constrained field (e.g., `status = 'invalid_status'`)

**Solution:**
- Review allowed values in schema comments
- Common constraints:
  - `status`: pending, in_progress, completed, failed, rolled_back
  - `operation_type`: read, write, delete, validate, transform, merge, rollback
  - `event_type`: sync_initiated, phi_accessed, sync_completed, etc.

#### Issue 3: APPEND-ONLY Violation (Application Error)

**Error:**
```
ApplicationError: UPDATE/DELETE not allowed on sync_audit_trail
```

**Cause:** Application code attempted prohibited operation on audit trail

**Solution:**
- Review application code
- Remove UPDATE/DELETE statements for `sync_audit_trail`
- Use APPEND-ONLY pattern

#### Issue 4: JSON Field Parsing Error

**Error:**
```
duckdb.ParserException: JSON syntax error
```

**Cause:** Invalid JSON in `metadata`, `compliance_context`, or `event_details` field

**Solution:**
```python
import json

# Always validate JSON before insertion
metadata = {"key": "value"}
metadata_json = json.dumps(metadata)  # Validates JSON syntax

conn.execute("""
    INSERT INTO agent_synchronizations (..., metadata) VALUES (..., ?)
""", [metadata_json])
```

### 9.2 Debugging Queries

**Find sync with most executions:**
```sql
SELECT
    s.sync_id,
    s.pattern,
    COUNT(e.execution_id) AS exec_count
FROM agent_synchronizations s
LEFT JOIN sync_executions e ON s.sync_id = e.sync_id
GROUP BY s.sync_id, s.pattern
ORDER BY exec_count DESC
LIMIT 10;
```

**Find audit events without matching execution:**
```sql
SELECT
    a.audit_id,
    a.event_type,
    a.execution_id
FROM sync_audit_trail a
WHERE a.execution_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1 FROM sync_executions e WHERE e.execution_id = a.execution_id
  );
```

**Verify referential integrity:**
```sql
-- Should return 0 rows (no orphaned executions)
SELECT e.execution_id
FROM sync_executions e
WHERE NOT EXISTS (
    SELECT 1 FROM agent_synchronizations s WHERE s.sync_id = e.sync_id
);
```

### 9.3 Performance Issues

**Slow query diagnosis:**
```sql
-- Use EXPLAIN to analyze query plan
EXPLAIN SELECT * FROM agent_synchronizations WHERE agent_id = 'agent-001';

-- Check if indexes are being used
EXPLAIN ANALYZE SELECT * FROM sync_audit_trail WHERE phi_involved = TRUE;
```

**Optimization checklist:**
- ✅ Are you using indexed columns in WHERE clauses?
- ✅ Are you limiting result sets with LIMIT?
- ✅ Are you avoiding SELECT * for large tables?
- ✅ Are you using pre-built views for complex queries?

### 9.4 Data Validation

**Validate all syncs have audit trails:**
```sql
SELECT
    s.sync_id,
    s.status,
    COUNT(a.audit_id) AS audit_count
FROM agent_synchronizations s
LEFT JOIN sync_audit_trail a ON s.sync_id = a.sync_id
GROUP BY s.sync_id, s.status
HAVING COUNT(a.audit_id) = 0
ORDER BY s.created_at DESC;
-- Should return 0 rows (every sync has at least one audit event)
```

**Validate PHI access has justification:**
```sql
SELECT
    execution_id,
    file_path,
    phi_accessed,
    phi_justification
FROM sync_executions
WHERE phi_accessed = TRUE
  AND (phi_justification IS NULL OR phi_justification = '')
ORDER BY started_at DESC;
-- Should return 0 rows (all PHI access is justified)
```

---

## 10. Additional Resources

### 10.1 Related Documentation

- **Schema File:** `.claude/skills/agentdb-state-manager/schemas/agentdb_sync_schema.sql`
- **Migration Test:** `.claude/skills/agentdb-state-manager/scripts/test_schema_migration.py`
- **Compliance Report:** `.claude/skills/agentdb-state-manager/docs/phase1_hipaa_compliance.md`
- **Issue #159:** Phase 1 - Database Schema Implementation

### 10.2 External References

- **DuckDB Documentation:** https://duckdb.org/docs/
- **HIPAA Security Rule:** https://www.hhs.gov/hipaa/for-professionals/security/index.html
- **FDA 21 CFR Part 11:** https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application

### 10.3 Support

For questions or issues:
1. Review this guide and troubleshooting section
2. Check HIPAA compliance report for regulatory guidance
3. Run `test_schema_migration.py` to validate schema integrity
4. Consult DuckDB documentation for database-specific questions

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-16
**Maintained By:** Claude Code (Autonomous Agent)
**Issue:** #159 - Phase 1 Database Schema Implementation
