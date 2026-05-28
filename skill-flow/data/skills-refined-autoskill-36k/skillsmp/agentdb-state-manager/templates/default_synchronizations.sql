-- ============================================================================
-- Default Synchronization Rules for 4-Tier Workflow
-- ============================================================================
-- Purpose: Define default agent coordination rules for MIT Agent Synchronization
--          Pattern across 4-tier workflow (Orchestrate → Develop → Assess → Research)
--
-- Created: 2025-11-18
-- Issue: #162 - Phase 4 Default Synchronization Rules Implementation
-- Depends: Phase 2 (#160), Phase 3 (#161)
--
-- Database: DuckDB
-- Tables: agent_synchronizations
--
-- Rule Design Principles:
-- 1. Single Responsibility: Each rule has ONE purpose
-- 2. Explicit Error Handling: Dedicated rules for each error type
-- 3. Priority Ordering: Errors (200) > Normal (100) > Background (1-99)
-- 4. Minimize Cascading: Each rule is terminal (no Rule A → Rule B → Rule C)
-- 5. Idempotency: Same trigger state → same provenance hash → executes once
--
-- Priority Levels:
-- - 200-299: Error recovery (highest priority - execute first)
-- - 100-199: Normal workflow flow
-- - 1-99: Background tasks (lowest priority)
--
-- Pattern Matching (Phase 2 Schema):
-- - Uses trigger_pattern (JSON field) for conditional triggering
-- - Pattern matching implemented in application code (sync_engine.py)
-- - target_action contains JSON template with parameter substitution
--
-- Note: Future enhancements (not in current schema):
-- - condition_jsonpath: JSONPath queries for complex conditions (Phase 5+)
-- - version: Rule versioning for A/B testing (Phase 6+)
-- ============================================================================

-- ============================================================================
-- 4-Tier Workflow Overview
-- ============================================================================
--
--   ┌──────────────┐
--   │ Orchestrate  │  Planning phase (BMAD)
--   │   Agent      │  Creates planning/ documents
--   └──────┬───────┘  Outputs: requirements.md, architecture.md
--          │
--          │ trigger_action: planning_complete
--          │ trigger_pattern: {"bmad_approved": true, "spec_validated": true}
--          ▼
--   ┌──────────────┐
--   │   Develop    │  Implementation phase
--   │   Agent      │  Creates code + tests
--   └──────┬───────┘  Outputs: source files, test files
--          │
--          │ trigger_action: commit_complete
--          │ trigger_pattern: {"lint_passed": true, "coverage_pct": 80}
--          ▼
--   ┌──────────────┐
--   │   Assess     │  Quality validation phase
--   │   Agent      │  Runs tests, checks coverage
--   └──────┬───────┘  Outputs: test results, coverage report
--          │
--          │ trigger_action: assessment_complete
--          │ trigger_pattern: {"tests_passed": true}
--          ▼
--   ┌──────────────┐
--   │  Research    │  Documentation generation
--   │   Agent      │  Creates docs, changelog
--   └──────────────┘  Outputs: README.md, CHANGELOG.md
--
-- ============================================================================

-- ============================================================================
-- Idempotency: Delete existing default rules before inserting
-- ============================================================================
-- This allows the file to be executed multiple times safely without creating
-- duplicate rules. Pattern names are unique identifiers for default rules.
DELETE FROM agent_synchronizations WHERE pattern IN (
    'orchestrate_to_develop',
    'develop_to_assess',
    'assess_to_research',
    'research_to_orchestrate',
    'test_failure_recovery',
    'lint_failure_recovery',
    'coverage_gap_recovery',
    'documentation_incomplete_recovery'
);

-- ============================================================================
-- Normal Flow Rules (Priority: 100-199)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Rule 1: Orchestrate → Develop Handoff
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'orchestrate',
    NULL,
    'workflow_transition',
    'planning/',
    '../feature_${trigger_state.slug}/',
    'orchestrate_to_develop',
    'pending',
    'claude-code',
    '{"description": "Transition from planning to implementation phase", "phase": "1_to_2"}',
    'orchestrate',
    'planning_complete',
    '{"bmad_approved": true, "spec_validated": true}',
    'develop',
    '{"action": "initialize_worktree", "params": {"planning_ref": "${trigger_state.planning_path}", "slug": "${trigger_state.slug}"}}',
    100,
    true
);

-- ----------------------------------------------------------------------------
-- Rule 2: Develop → Assess Handoff
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'develop',
    '../feature_${trigger_state.slug}/',
    'workflow_transition',
    'src/',
    'tests/',
    'develop_to_assess',
    'pending',
    'claude-code',
    '{"description": "Transition from implementation to quality validation", "phase": "2_to_3"}',
    'develop',
    'commit_complete',
    '{"lint_passed": true, "coverage_pct": 80}',
    'assess',
    '{"action": "run_test_suite", "params": {"test_path": "${trigger_state.test_files}", "coverage_threshold": 80}}',
    100,
    true
);

-- ----------------------------------------------------------------------------
-- Rule 3: Assess → Research Handoff
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'assess',
    '../feature_${trigger_state.slug}/',
    'workflow_transition',
    'tests/',
    'docs/',
    'assess_to_research',
    'pending',
    'claude-code',
    '{"description": "Transition from quality validation to documentation", "phase": "3_to_4"}',
    'assess',
    'assessment_complete',
    '{"tests_passed": true}',
    'research',
    '{"action": "generate_documentation", "params": {"test_report": "${trigger_state.test_report_path}", "coverage_data": "${trigger_state.coverage_data}"}}',
    100,
    true
);

-- ----------------------------------------------------------------------------
-- Rule 4: Research → Orchestrate (PR Creation)
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'research',
    '../feature_${trigger_state.slug}/',
    'workflow_transition',
    'docs/',
    './',
    'research_to_orchestrate',
    'pending',
    'claude-code',
    '{"description": "Complete workflow cycle with PR creation", "phase": "4_to_1"}',
    'research',
    'documentation_complete',
    '{"deliverables_complete": true}',
    'orchestrate',
    '{"action": "create_pr", "params": {"title": "${trigger_state.pr_title}", "body": "${trigger_state.pr_body}", "deliverables": "${trigger_state.deliverables}"}}',
    100,
    true
);

-- ============================================================================
-- Error Recovery Rules (Priority: 200-299)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Rule 5: Test Failure → Add Tests (Error Recovery)
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'assess',
    '../feature_${trigger_state.slug}/',
    'error_recovery',
    'tests/',
    'src/',
    'test_failure_recovery',
    'pending',
    'claude-code',
    '{"description": "Recover from test failures by adding tests", "error_type": "test_failure"}',
    'assess',
    'assessment_complete',
    '{"tests_passed": false}',
    'develop',
    '{"action": "add_tests", "params": {"failed_modules": "${trigger_state.failed_tests}", "priority": "high"}}',
    200,
    true
);

-- ----------------------------------------------------------------------------
-- Rule 6: Lint Failure → Fix Linting (Error Recovery)
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'develop',
    '../feature_${trigger_state.slug}/',
    'error_recovery',
    'src/',
    'src/',
    'lint_failure_recovery',
    'pending',
    'claude-code',
    '{"description": "Recover from linting failures by fixing code style", "error_type": "lint_failure"}',
    'develop',
    'commit_complete',
    '{"lint_passed": false}',
    'develop',
    '{"action": "fix_linting", "params": {"violations": "${trigger_state.lint_violations}", "auto_fix": true}}',
    200,
    true
);

-- ----------------------------------------------------------------------------
-- Rule 7: Coverage Gap → Identify Untested Modules (Error Recovery)
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'assess',
    '../feature_${trigger_state.slug}/',
    'error_recovery',
    'tests/',
    'src/',
    'coverage_gap_recovery',
    'pending',
    'claude-code',
    '{"description": "Recover from coverage gap by identifying untested modules", "error_type": "coverage_gap"}',
    'assess',
    'assessment_complete',
    '{"coverage_pct": 79}',
    'develop',
    '{"action": "add_coverage", "params": {"untested_modules": "${trigger_state.untested_modules}", "current_coverage": "${trigger_state.coverage_pct}", "target_coverage": 80}}',
    200,
    true
);

-- ----------------------------------------------------------------------------
-- Rule 8: Documentation Incomplete → Retry (Error Recovery)
-- ----------------------------------------------------------------------------
INSERT INTO agent_synchronizations (
    sync_id,
    agent_id,
    worktree_path,
    sync_type,
    source_location,
    target_location,
    pattern,
    status,
    created_by,
    metadata,
    trigger_agent_id,
    trigger_action,
    trigger_pattern,
    target_agent_id,
    target_action,
    priority,
    enabled
) VALUES (
    gen_random_uuid(),
    'research',
    '../feature_${trigger_state.slug}/',
    'error_recovery',
    'docs/',
    'docs/',
    'documentation_incomplete_recovery',
    'pending',
    'claude-code',
    '{"description": "Retry documentation generation with missing artifacts", "error_type": "documentation_incomplete"}',
    'research',
    'documentation_complete',
    '{"deliverables_complete": false}',
    'research',
    '{"action": "retry_documentation", "params": {"missing_artifacts": "${trigger_state.missing_artifacts}", "retry_count": "${trigger_state.retry_count}"}}',
    200,
    true
);

-- ============================================================================
-- Validation Query
-- ============================================================================
SELECT
    'Default synchronization rules validation' AS status,
    COUNT(*) AS total_rules,
    SUM(CASE WHEN priority BETWEEN 100 AND 199 THEN 1 ELSE 0 END) AS normal_flow_rules,
    SUM(CASE WHEN priority BETWEEN 200 AND 299 THEN 1 ELSE 0 END) AS error_recovery_rules,
    SUM(CASE WHEN enabled = true THEN 1 ELSE 0 END) AS enabled_rules,
    MIN(priority) AS min_priority,
    MAX(priority) AS max_priority
FROM agent_synchronizations
WHERE pattern IN (
    'orchestrate_to_develop',
    'develop_to_assess',
    'assess_to_research',
    'research_to_orchestrate',
    'test_failure_recovery',
    'lint_failure_recovery',
    'coverage_gap_recovery',
    'documentation_incomplete_recovery'
);

-- ============================================================================
-- Rule Summary by Priority
-- ============================================================================
SELECT
    pattern,
    trigger_agent_id,
    trigger_action,
    target_agent_id,
    priority,
    enabled,
    sync_type
FROM agent_synchronizations
WHERE pattern IN (
    'orchestrate_to_develop',
    'develop_to_assess',
    'assess_to_research',
    'research_to_orchestrate',
    'test_failure_recovery',
    'lint_failure_recovery',
    'coverage_gap_recovery',
    'documentation_incomplete_recovery'
)
ORDER BY priority DESC, pattern;

-- ============================================================================
-- End of Default Synchronization Rules
-- ============================================================================
