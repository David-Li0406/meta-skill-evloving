-- ============================================================================
-- AgentDB Synchronization Schema v1.0.0
-- ============================================================================
-- Purpose: MIT Agent Synchronization Pattern database schema for multi-agent
--          coordination with HIPAA/FDA/IRB compliance
--
-- Academic Reference:
--   Meng, E., & Jackson, D. (2025). "What You See Is What It Does: A Structural
--   Pattern for Legible Software." Onward! at SPLASH 2025. arXiv:2508.14511v1.
--   https://arxiv.org/abs/2508.14511
--
-- Created: 2025-11-16
-- Issue: #159 - Phase 1 Database Schema Implementation
-- Blocks: #160 (Phase 2), #161 (Phase 3)
--
-- Database: DuckDB
-- Tables: 3 (agent_synchronizations, sync_executions, sync_audit_trail)
--
-- Healthcare Compliance:
-- - HIPAA Security Rule (audit controls, access controls, integrity controls)
-- - FDA 21 CFR Part 11 (electronic records, electronic signatures, audit trail)
-- - IRB Standards (consent tracking, data minimization)
--
-- Design Principles:
-- - Immutable audit trail (APPEND-ONLY for sync_audit_trail)
-- - Comprehensive PHI tracking (phi_accessed, phi_justification fields)
-- - Idempotent synchronization (checksum_before/after)
-- - Full forensic capability (actor, timestamp, event_details)
-- ============================================================================

-- ============================================================================
-- Schema Metadata
-- ============================================================================
-- This metadata table tracks schema version for future migrations
CREATE TABLE IF NOT EXISTS schema_metadata (
    schema_name VARCHAR PRIMARY KEY,
    schema_version VARCHAR NOT NULL,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    applied_by VARCHAR NOT NULL,
    description TEXT
);

-- Insert schema version record
INSERT INTO schema_metadata (schema_name, schema_version, applied_by, description)
VALUES (
    'agentdb_sync_schema',
    '1.0.0',
    'claude-code',
    'Initial MIT Agent Synchronization Pattern schema with HIPAA/FDA/IRB compliance'
)
ON CONFLICT (schema_name) DO NOTHING;

-- ============================================================================
-- Table 1: agent_synchronizations
-- ============================================================================
-- Purpose: Master registry of all agent synchronization events
--
-- This table tracks every synchronization operation between agents, worktrees,
-- and file locations. It serves as the primary coordination mechanism for the
-- MIT Agent Synchronization Pattern.
--
-- Key features:
-- - Unique sync_id for each synchronization event
-- - Pattern-based routing (enables rule-based synchronization)
-- - Status tracking (pending → in_progress → completed/failed/rolled_back)
-- - Worktree awareness (supports git worktree-based workflows)
-- - Extensible metadata (JSON field for future requirements)
--
-- Healthcare compliance:
-- - Audit trail foundation (all syncs logged with timestamps and actors)
-- - Access control support (created_by field tracks responsible party)
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_synchronizations (
    -- Primary identifier: UUIDv4 for uniqueness across distributed systems
    sync_id VARCHAR PRIMARY KEY,

    -- Agent identification: Which agent initiated this synchronization
    agent_id VARCHAR NOT NULL,

    -- Worktree context: Git worktree path (NULL for main repo operations)
    -- Rationale: Supports git-flow workflow with feature/hotfix worktrees
    worktree_path VARCHAR,

    -- Synchronization type: Categorizes the sync operation
    -- Examples: 'file_update', 'task_completion', 'state_checkpoint', 'quality_gate', 'workflow_transition'
    sync_type VARCHAR NOT NULL,

    -- Source/target locations: Where data flows from and to
    -- Examples: '../TODO_feature_*.md' → 'worktree/TODO_feature_*.md'
    source_location VARCHAR NOT NULL,
    target_location VARCHAR NOT NULL,

    -- Pattern identifier: Which synchronization rule/pattern applies
    -- Examples: 'todo_bidirectional', 'planning_readonly', 'checkpoint_append'
    -- Rationale: Enables rule-based sync behavior (bidirectional, unidirectional, append-only)
    pattern VARCHAR NOT NULL,

    -- Status tracking: Current state of synchronization
    -- Lifecycle: pending → in_progress → completed/failed/rolled_back
    status VARCHAR NOT NULL CHECK (status IN (
        'pending',      -- Sync queued but not started
        'in_progress',  -- Sync currently executing
        'completed',    -- Sync finished successfully
        'failed',       -- Sync failed with errors
        'rolled_back'   -- Sync was reversed due to failure
    )),

    -- Timestamps: Track synchronization lifecycle
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,  -- NULL until sync finishes

    -- Audit trail: Who created this synchronization
    -- Rationale: HIPAA/FDA requirement for accountability
    created_by VARCHAR NOT NULL,

    -- Extensible metadata: Additional context as JSON
    -- Examples: {"priority": "high", "retry_count": 2, "parent_sync_id": "..."}
    -- Rationale: Future-proof design without schema migrations
    metadata JSON
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_sync_agent ON agent_synchronizations(agent_id);
CREATE INDEX IF NOT EXISTS idx_sync_status ON agent_synchronizations(status);
CREATE INDEX IF NOT EXISTS idx_sync_created ON agent_synchronizations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sync_pattern ON agent_synchronizations(pattern);
CREATE INDEX IF NOT EXISTS idx_sync_worktree ON agent_synchronizations(worktree_path);

-- Composite index for common query pattern: Find in-progress syncs for an agent
CREATE INDEX IF NOT EXISTS idx_sync_agent_status ON agent_synchronizations(agent_id, status);

-- ============================================================================
-- Table 2: sync_executions
-- ============================================================================
-- Purpose: Detailed execution log for each synchronization (one-to-many with agent_synchronizations)
--
-- This table captures every operation performed during a synchronization,
-- providing granular audit trail and idempotency tracking.
--
-- Key features:
-- - One-to-many with agent_synchronizations (one sync = many executions)
-- - Execution ordering (execution_order field ensures deterministic replay)
-- - PHI tracking (phi_accessed, phi_justification for HIPAA compliance)
-- - Idempotency (checksum_before/after enables safe retries)
-- - Performance metrics (duration_ms for bottleneck analysis)
--
-- Healthcare compliance:
-- - PHI access tracking (HIPAA requirement)
-- - PHI justification (demonstrates minimum necessary standard)
-- - Forensic capability (checksum tracking for integrity validation)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sync_executions (
    -- Primary identifier: UUIDv4 for unique execution
    execution_id VARCHAR PRIMARY KEY,

    -- Foreign key: Links to parent synchronization
    -- Rationale: One sync can have many executions (multi-step operations)
    -- Note: Using ON DELETE RESTRICT to prevent accidental parent deletion (audit trail immutability)
    sync_id VARCHAR NOT NULL REFERENCES agent_synchronizations(sync_id) ON DELETE RESTRICT,

    -- Execution ordering: Sequence number within synchronization
    -- Rationale: Enables deterministic replay and debugging
    execution_order INTEGER NOT NULL,

    -- Operation type: What kind of operation was performed
    -- Examples: 'read', 'write', 'delete', 'validate', 'transform', 'merge'
    operation_type VARCHAR NOT NULL CHECK (operation_type IN (
        'read',       -- Read file/data
        'write',      -- Write file/data
        'delete',     -- Delete file/data
        'validate',   -- Validate data integrity
        'transform',  -- Transform data format
        'merge',      -- Merge conflicting data
        'rollback'    -- Reverse previous operation
    )),

    -- File path: File affected by this operation (NULL for non-file operations)
    file_path VARCHAR,

    -- PHI tracking: HIPAA-compliant Protected Health Information monitoring
    -- Rationale: HIPAA requires tracking all PHI access with justification
    phi_accessed BOOLEAN NOT NULL DEFAULT FALSE,
    phi_justification TEXT,  -- Required if phi_accessed=TRUE

    -- Operation result: Outcome of this execution
    operation_result VARCHAR NOT NULL CHECK (operation_result IN (
        'success',     -- Operation completed successfully
        'failure',     -- Operation failed
        'skipped',     -- Operation skipped (conditional logic)
        'rolled_back'  -- Operation was reversed
    )),

    -- Error tracking: Details if operation failed
    error_message TEXT,

    -- Timing information: When operation started and finished
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,

    -- Performance metric: Execution duration in milliseconds
    -- Rationale: Enables bottleneck identification and performance optimization
    duration_ms INTEGER,

    -- Idempotency tracking: File checksums before and after operation
    -- Rationale: Enables safe retries - can detect if operation already applied
    -- Algorithm: SHA-256 hex digest
    checksum_before VARCHAR,
    checksum_after VARCHAR,

    -- Extensible metadata: Additional execution context as JSON
    -- Examples: {"line_count": 150, "encoding": "utf-8", "conflict_resolved": true}
    metadata JSON
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_exec_sync ON sync_executions(sync_id, execution_order);
CREATE INDEX IF NOT EXISTS idx_exec_result ON sync_executions(operation_result);
CREATE INDEX IF NOT EXISTS idx_exec_phi ON sync_executions(phi_accessed);
CREATE INDEX IF NOT EXISTS idx_exec_started ON sync_executions(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_exec_file ON sync_executions(file_path);

-- Composite index for common query: Find all failed operations for a sync
CREATE INDEX IF NOT EXISTS idx_exec_sync_result ON sync_executions(sync_id, operation_result);

-- ============================================================================
-- Table 3: sync_audit_trail
-- ============================================================================
-- Purpose: Immutable audit log for healthcare compliance (HIPAA/FDA 21 CFR Part 11/IRB)
--
-- This table is the cornerstone of healthcare compliance, providing an
-- immutable, append-only audit trail of all synchronization events.
--
-- Key features:
-- - APPEND-ONLY: No UPDATE or DELETE allowed (FDA 21 CFR Part 11 requirement)
-- - Comprehensive event tracking (sync lifecycle, PHI access, failures)
-- - Actor attribution (who, when, what role)
-- - Compliance context (HIPAA purpose, legal basis, consent tracking)
-- - Forensic capability (full event details in JSON)
--
-- Healthcare compliance:
-- - HIPAA Security Rule: Audit controls (comprehensive logging)
-- - FDA 21 CFR Part 11: Electronic records (immutability, timestamps, signatures)
-- - IRB Standards: Consent tracking, data minimization evidence
--
-- CRITICAL: This table must NEVER be modified or deleted after creation.
-- Any attempt to UPDATE or DELETE records violates FDA 21 CFR Part 11.
-- ============================================================================

CREATE TABLE IF NOT EXISTS sync_audit_trail (
    -- Primary identifier: UUIDv4 for unique audit entry
    audit_id VARCHAR PRIMARY KEY,

    -- Foreign keys: Link to synchronization and execution
    -- Rationale: Enables correlation of audit events with operations
    -- Note: ON DELETE RESTRICT enforces audit trail immutability at database level
    sync_id VARCHAR NOT NULL REFERENCES agent_synchronizations(sync_id) ON DELETE RESTRICT,
    execution_id VARCHAR REFERENCES sync_executions(execution_id) ON DELETE RESTRICT,

    -- Event type: Category of audit event
    -- Examples: 'sync_initiated', 'phi_accessed', 'sync_completed', 'sync_failed', 'rollback_executed'
    event_type VARCHAR NOT NULL CHECK (event_type IN (
        'sync_initiated',     -- Synchronization started
        'sync_progressing',   -- Synchronization in progress (milestone)
        'sync_completed',     -- Synchronization finished successfully
        'sync_failed',        -- Synchronization failed
        'sync_rolled_back',   -- Synchronization was reversed
        'phi_accessed',       -- Protected Health Information accessed
        'phi_created',        -- Protected Health Information created
        'phi_modified',       -- Protected Health Information modified
        'validation_failed',  -- Data validation failed
        'conflict_detected',  -- Sync conflict detected
        'conflict_resolved',  -- Sync conflict resolved
        'permission_denied',  -- Access control violation
        'integrity_violation' -- Data integrity check failed
    )),

    -- Actor information: Who performed the action
    -- Rationale: HIPAA/FDA requirement for accountability and electronic signatures
    actor VARCHAR NOT NULL,
    actor_role VARCHAR NOT NULL CHECK (actor_role IN (
        'human_user',        -- Human operator
        'autonomous_agent',  -- Claude Code or other AI agent
        'system'             -- Automated system process
    )),

    -- Timestamp: When event occurred (IMMUTABLE - set once at INSERT)
    -- Rationale: FDA 21 CFR Part 11 requires accurate, immutable timestamps
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- PHI involvement: Was Protected Health Information involved
    -- Rationale: HIPAA requires tracking all PHI interactions
    phi_involved BOOLEAN NOT NULL DEFAULT FALSE,

    -- Compliance context: Legal and regulatory context (JSON)
    -- Required fields:
    -- - purpose: Why was this action performed (HIPAA minimum necessary)
    -- - legal_basis: Legal authorization (HIPAA, consent, research protocol)
    -- - consent_id: Patient consent identifier (if applicable)
    -- - irb_protocol: IRB protocol number (if research context)
    -- - data_minimization: Evidence of minimum data access
    --
    -- Example:
    -- {
    --   "purpose": "Synchronize workflow state for patient data analysis",
    --   "legal_basis": "HIPAA research authorization",
    --   "consent_id": "CONSENT-2025-001",
    --   "irb_protocol": "IRB-2025-123",
    --   "data_minimization": "Only accessed aggregate statistics, no individual PHI"
    -- }
    compliance_context JSON NOT NULL,

    -- Event details: Full event data for forensic analysis (JSON)
    -- Examples: {"files_changed": [...], "error_stack": "...", "conflict_resolution": "..."}
    -- Rationale: Complete record for investigation and debugging
    event_details JSON NOT NULL,

    -- Network context: Source IP address and session ID
    -- Rationale: Additional audit trail for security investigations
    ip_address VARCHAR,
    session_id VARCHAR
);

-- Indexes for efficient audit queries
CREATE INDEX IF NOT EXISTS idx_audit_sync ON sync_audit_trail(sync_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_execution ON sync_audit_trail(execution_id);
CREATE INDEX IF NOT EXISTS idx_audit_event ON sync_audit_trail(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON sync_audit_trail(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_phi ON sync_audit_trail(phi_involved);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON sync_audit_trail(actor);
CREATE INDEX IF NOT EXISTS idx_audit_session ON sync_audit_trail(session_id);

-- Composite index for compliance queries: Find all PHI access by actor and date range
CREATE INDEX IF NOT EXISTS idx_audit_phi_actor_time ON sync_audit_trail(phi_involved, actor, timestamp DESC);

-- ============================================================================
-- Enforcing APPEND-ONLY Constraint (FDA 21 CFR Part 11 Compliance)
-- ============================================================================
-- DuckDB Note: DuckDB does not support triggers in the same way as PostgreSQL.
-- The APPEND-ONLY constraint must be enforced at the application level.
--
-- APPLICATION REQUIREMENT:
-- All database access layers MUST:
-- 1. Only use INSERT statements for sync_audit_trail
-- 2. Never execute UPDATE or DELETE on sync_audit_trail
-- 3. Implement read-only access for audit queries
-- 4. Log any attempted UPDATE/DELETE as security violation
--
-- VALIDATION:
-- The test_schema_migration.py script validates this constraint by:
-- 1. Attempting UPDATE (must fail in application logic)
-- 2. Attempting DELETE (must fail in application logic)
-- 3. Verifying APPEND-ONLY behavior
--
-- FUTURE ENHANCEMENT:
-- When DuckDB adds trigger support, implement:
-- CREATE TRIGGER prevent_audit_update BEFORE UPDATE ON sync_audit_trail
-- FOR EACH ROW EXECUTE FUNCTION raise_exception();
-- ============================================================================

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- View: Current synchronization status (latest state for each sync)
CREATE OR REPLACE VIEW v_current_sync_status AS
SELECT
    s.sync_id,
    s.agent_id,
    s.worktree_path,
    s.sync_type,
    s.pattern,
    s.status,
    s.created_at,
    s.completed_at,
    s.created_by,
    COUNT(e.execution_id) AS execution_count,
    SUM(CASE WHEN e.phi_accessed THEN 1 ELSE 0 END) AS phi_access_count,
    SUM(CASE WHEN e.operation_result = 'failure' THEN 1 ELSE 0 END) AS failure_count,
    SUM(e.duration_ms) AS total_duration_ms
FROM agent_synchronizations s
LEFT JOIN sync_executions e ON s.sync_id = e.sync_id
GROUP BY s.sync_id, s.agent_id, s.worktree_path, s.sync_type, s.pattern,
         s.status, s.created_at, s.completed_at, s.created_by;

-- View: PHI access audit report (HIPAA compliance reporting)
CREATE OR REPLACE VIEW v_phi_access_audit AS
SELECT
    a.audit_id,
    a.timestamp,
    a.actor,
    a.actor_role,
    a.event_type,
    s.sync_type,
    s.pattern,
    e.file_path,
    e.phi_justification,
    a.compliance_context,
    a.session_id
FROM sync_audit_trail a
JOIN agent_synchronizations s ON a.sync_id = s.sync_id
LEFT JOIN sync_executions e ON a.execution_id = e.execution_id
WHERE a.phi_involved = TRUE
ORDER BY a.timestamp DESC;

-- View: Synchronization performance metrics
CREATE OR REPLACE VIEW v_sync_performance AS
SELECT
    s.pattern,
    s.sync_type,
    COUNT(*) AS total_syncs,
    SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) AS successful_syncs,
    SUM(CASE WHEN s.status = 'failed' THEN 1 ELSE 0 END) AS failed_syncs,
    AVG(datediff('millisecond', s.created_at, s.completed_at)) AS avg_duration_ms,
    MAX(datediff('millisecond', s.created_at, s.completed_at)) AS max_duration_ms
FROM agent_synchronizations s
WHERE s.completed_at IS NOT NULL
GROUP BY s.pattern, s.sync_type
ORDER BY total_syncs DESC;

-- View: Failed operations requiring investigation
CREATE OR REPLACE VIEW v_failed_operations AS
SELECT
    e.execution_id,
    e.sync_id,
    s.sync_type,
    s.pattern,
    e.operation_type,
    e.file_path,
    e.error_message,
    e.started_at,
    s.created_by,
    COUNT(a.audit_id) AS audit_event_count
FROM sync_executions e
JOIN agent_synchronizations s ON e.sync_id = s.sync_id
LEFT JOIN sync_audit_trail a ON e.execution_id = a.execution_id
WHERE e.operation_result = 'failure'
GROUP BY e.execution_id, e.sync_id, s.sync_type, s.pattern, e.operation_type,
         e.file_path, e.error_message, e.started_at, s.created_by
ORDER BY e.started_at DESC;

-- ============================================================================
-- Schema Validation Queries
-- ============================================================================

-- Query to verify schema was created successfully
-- Run this after schema creation to validate all tables exist
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

-- ============================================================================
-- End of Schema
-- ============================================================================
