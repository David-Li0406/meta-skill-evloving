-- ============================================================================
-- Phase 2 Schema Migration v2.0.0
-- ============================================================================
-- Purpose: Extend Phase 1 schema with MIT Agent Synchronization Pattern fields
--          for declarative pattern matching, trigger/target coordination, and
--          idempotency enforcement
--
-- Created: 2025-11-17
-- Issue: #160 - Phase 2 Synchronization Engine Implementation
-- Depends: Phase 1 schema v1.0.0 (agentdb_sync_schema.sql)
--
-- Database: DuckDB
-- Changes: Add fields to agent_synchronizations and sync_executions tables
--
-- Migration Strategy: ALTER TABLE (Option A - extends Phase 1 schema)
--
-- Rationale:
-- - Preserves Phase 1 fields for backward compatibility
-- - Single unified schema (no duplicate tables)
-- - Simple migration path
-- - Phase 1 fields remain usable for file-based synchronization
-- - Phase 2 fields enable rule-based agent coordination
-- ============================================================================

-- ============================================================================
-- Update schema metadata
-- ============================================================================
-- Note: DuckDB's ON CONFLICT syntax is different from PostgreSQL
-- We use INSERT OR REPLACE instead
INSERT OR REPLACE INTO schema_metadata (schema_name, schema_version, applied_by, description, applied_at)
VALUES (
    'agentdb_sync_schema',
    '2.0.0',
    'claude-code',
    'Phase 2 migration: Add MIT Agent Synchronization Pattern fields for declarative coordination',
    CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table 1: agent_synchronizations - Add Phase 2 fields
-- ============================================================================
-- New fields for MIT Agent Synchronization Pattern:
-- - trigger_agent_id: Which agent triggers this sync (e.g., "develop", "assess")
-- - trigger_action: What action triggers this sync (e.g., "commit_complete", "test_passed")
-- - trigger_pattern: JSON pattern for conditional triggering (e.g., {"lint_status": "pass"})
-- - target_agent_id: Which agent to trigger (e.g., "assess", "integrate")
-- - target_action: What action to trigger (e.g., "run_tests", "create_pr")
-- - priority: Execution priority (higher = first, default 100)
-- - enabled: Whether this sync rule is active (default TRUE)
--
-- Design Notes:
-- - trigger_pattern uses DuckDB JSON type (not JSONB like PostgreSQL)
-- - Pattern matching implemented in application code (no @> operator in DuckDB)
-- - NULL allowed for backward compatibility with Phase 1 file-based syncs
-- ============================================================================

-- Add Phase 2 fields one at a time (DuckDB limitation)
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS trigger_agent_id VARCHAR;
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS trigger_action VARCHAR;
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS trigger_pattern JSON;
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS target_agent_id VARCHAR;
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS target_action VARCHAR;
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 100;
ALTER TABLE agent_synchronizations ADD COLUMN IF NOT EXISTS enabled BOOLEAN DEFAULT TRUE;

-- Create indexes for Phase 2 query patterns
CREATE INDEX IF NOT EXISTS idx_sync_trigger ON agent_synchronizations(trigger_agent_id, trigger_action);
CREATE INDEX IF NOT EXISTS idx_sync_target ON agent_synchronizations(target_agent_id);
-- Note: DuckDB doesn't support partial indexes (WHERE clause), so we index all rows
CREATE INDEX IF NOT EXISTS idx_sync_enabled ON agent_synchronizations(enabled);
CREATE INDEX IF NOT EXISTS idx_sync_priority ON agent_synchronizations(priority DESC);

-- Composite index for main sync matching query
-- Query: Find enabled syncs for trigger_agent + trigger_action, ordered by priority
CREATE INDEX IF NOT EXISTS idx_sync_matching ON agent_synchronizations(
    trigger_agent_id,
    trigger_action,
    enabled,
    priority DESC
);

-- ============================================================================
-- Table 2: sync_executions - Add Phase 2 fields
-- ============================================================================
-- New fields for idempotency and state tracking:
-- - provenance_hash: SHA-256 content-addressed hash for idempotency enforcement
--   Format: hex string (64 chars)
--   Uniqueness: Ensures same state doesn't trigger duplicate executions
--   Algorithm: SHA-256(sync_id + flow_token + trigger_state_snapshot)
--
-- - trigger_state_snapshot: Full workflow state at trigger time (JSON)
--   Purpose: Forensic record of what state triggered this execution
--   Used for: Parameter substitution, debugging, audit trail
--
-- - exec_status: Phase 2 execution status (simpler than operation_result)
--   Values: 'pending', 'completed', 'failed'
--   Rationale: Separate from operation_result for backward compatibility
--
-- Design Notes:
-- - provenance_hash has UNIQUE constraint (idempotency enforcement)
-- - trigger_state_snapshot stored as DuckDB JSON (not JSONB)
-- - exec_status is separate field (doesn't replace operation_result)
-- ============================================================================

-- Add Phase 2 fields one at a time (DuckDB limitation)
ALTER TABLE sync_executions ADD COLUMN IF NOT EXISTS provenance_hash VARCHAR(64);
ALTER TABLE sync_executions ADD COLUMN IF NOT EXISTS trigger_state_snapshot JSON;
-- Note: CHECK constraint cannot be added via ALTER TABLE in DuckDB
-- Must be enforced at application level
ALTER TABLE sync_executions ADD COLUMN IF NOT EXISTS exec_status VARCHAR;

-- Create unique constraint for idempotency enforcement
-- Note: DuckDB doesn't support ADD CONSTRAINT UNIQUE after table creation
-- We create a unique index instead (equivalent for DuckDB)
CREATE UNIQUE INDEX IF NOT EXISTS idx_exec_provenance_unique ON sync_executions(provenance_hash);

-- Create indexes for Phase 2 queries
CREATE INDEX IF NOT EXISTS idx_exec_status ON sync_executions(exec_status);
CREATE INDEX IF NOT EXISTS idx_exec_sync_status ON sync_executions(sync_id, exec_status);

-- ============================================================================
-- Add comment to document migration
-- ============================================================================
COMMENT ON TABLE agent_synchronizations IS
'Synchronization rules for MIT Agent Synchronization Pattern.
Phase 1: File-based synchronization (agent_id, source_location, target_location, pattern)
Phase 2: Agent-based coordination (trigger_agent_id, trigger_action, trigger_pattern, target_agent_id, target_action)
Extended in Phase 2 migration v2.0.0 (Issue #160)';

COMMENT ON TABLE sync_executions IS
'Detailed execution log for synchronizations.
Phase 1: File operations with checksums (operation_type, file_path, checksum_before/after)
Phase 2: Idempotent agent coordination (provenance_hash, trigger_state_snapshot, exec_status)
Extended in Phase 2 migration v2.0.0 (Issue #160)';

-- ============================================================================
-- Updated View: Current sync status with Phase 2 fields
-- ============================================================================
CREATE OR REPLACE VIEW v_current_sync_status_v2 AS
SELECT
    s.sync_id,
    s.agent_id,
    s.worktree_path,
    s.sync_type,
    s.pattern,
    s.status,
    -- Phase 2 fields
    s.trigger_agent_id,
    s.trigger_action,
    s.trigger_pattern,
    s.target_agent_id,
    s.target_action,
    s.priority,
    s.enabled,
    -- Metadata
    s.created_at,
    s.completed_at,
    s.created_by,
    -- Aggregates
    COUNT(e.execution_id) AS execution_count,
    SUM(CASE WHEN e.phi_accessed THEN 1 ELSE 0 END) AS phi_access_count,
    SUM(CASE WHEN e.operation_result = 'failure' THEN 1 ELSE 0 END) AS failure_count,
    SUM(CASE WHEN e.exec_status = 'failed' THEN 1 ELSE 0 END) AS phase2_failure_count,
    SUM(e.duration_ms) AS total_duration_ms
FROM agent_synchronizations s
LEFT JOIN sync_executions e ON s.sync_id = e.sync_id
GROUP BY s.sync_id, s.agent_id, s.worktree_path, s.sync_type, s.pattern,
         s.status, s.trigger_agent_id, s.trigger_action, s.trigger_pattern,
         s.target_agent_id, s.target_action, s.priority, s.enabled,
         s.created_at, s.completed_at, s.created_by;

-- ============================================================================
-- Migration Validation
-- ============================================================================
-- Verify all Phase 2 fields were added successfully
SELECT
    'Phase 2 migration validation' AS status,
    -- agent_synchronizations new columns
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'trigger_agent_id') AS has_trigger_agent,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'trigger_action') AS has_trigger_action,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'trigger_pattern') AS has_trigger_pattern,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'target_agent_id') AS has_target_agent,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'target_action') AS has_target_action,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'priority') AS has_priority,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'agent_synchronizations' AND column_name = 'enabled') AS has_enabled,
    -- sync_executions new columns
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'sync_executions' AND column_name = 'provenance_hash') AS has_provenance_hash,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'sync_executions' AND column_name = 'trigger_state_snapshot') AS has_trigger_state,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'sync_executions' AND column_name = 'exec_status') AS has_exec_status
WHERE
    -- All fields must exist (count = 1)
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'trigger_agent_id') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'trigger_action') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'trigger_pattern') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'target_agent_id') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'target_action') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'priority') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'agent_synchronizations' AND column_name = 'enabled') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'sync_executions' AND column_name = 'provenance_hash') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'sync_executions' AND column_name = 'trigger_state_snapshot') = 1
    AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'sync_executions' AND column_name = 'exec_status') = 1;

-- ============================================================================
-- End of Phase 2 Migration
-- ============================================================================
