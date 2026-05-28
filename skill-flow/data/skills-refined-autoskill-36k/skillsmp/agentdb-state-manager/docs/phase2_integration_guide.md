# Phase 2 → Phase 3 Integration Guide

**Created**: 2025-11-17
**Issue**: #160 - Phase 2 Synchronization Engine Implementation
**For**: Phase 3 - Integration Layer (Issue #161)

## Overview

This guide explains how Phase 3 (Integration Layer) integrates with the completed Phase 2 (Synchronization Engine).

**Phase 2 provides**:
- `SynchronizationEngine` class with declarative pattern matching
- Idempotency enforcement via content-addressed hashing
- Healthcare compliance logging (HIPAA/FDA/IRB)
- Performance: <100ms p95 latency for single agent

**Phase 3 will add**:
- Agent instrumentation (hooks into worktree operations)
- PHI detection heuristics
- Feature flags for gradual rollout
- Production monitoring

## Quick Start

### 1. Import and Initialize

```python
from claude.skills.agentdb_state_manager.scripts.sync_engine import SynchronizationEngine

# Initialize engine (singleton pattern recommended)
sync_engine = SynchronizationEngine(db_path="agentdb.duckdb", cache_ttl=300)
```

### 2. Call on Agent Action Complete

Phase 3 will call `on_agent_action_complete()` whenever an agent finishes an action:

```python
# Example: Agent "develop" completed a commit
execution_ids = sync_engine.on_agent_action_complete(
    agent_id="develop",
    action="commit_complete",
    flow_token="worktree-auth-system-20251117",
    state_snapshot={
        "commit_sha": "abc123def456",
        "coverage": {"percentage": 85, "lines_covered": 1234},
        "lint_status": "pass",
        "tests_passing": True
    }
)

# Returns: List of execution_ids (UUIDs) for triggered synchronizations
print(f"Triggered {len(execution_ids)} synchronizations")
```

### 3. Handle Execution IDs

Phase 3 is responsible for **actually triggering** the target agents based on the returned execution IDs:

```python
for exec_id in execution_ids:
    # Query execution details
    result = sync_engine.conn.execute("""
        SELECT e.sync_id, e.trigger_state_snapshot, s.target_agent_id, s.target_action
        FROM sync_executions e
        JOIN agent_synchronizations s ON e.sync_id = s.sync_id
        WHERE e.execution_id = ?
    """, [exec_id]).fetchone()

    sync_id, trigger_state, target_agent_id, target_action = result

    # Phase 3: Actually trigger the target agent
    trigger_target_agent(target_agent_id, target_action, json.loads(trigger_state))
```

## Integration Points

### Integration Point 1: Agent Hooks

Phase 3 will instrument agents to call `on_agent_action_complete()` at specific lifecycle events.

**Example agent lifecycle**:
```
develop:
  - commit_start → (no trigger)
  - commit_complete → call sync_engine.on_agent_action_complete()

assess:
  - test_start → (no trigger)
  - test_passed → call sync_engine.on_agent_action_complete()
  - test_failed → call sync_engine.on_agent_action_complete()

integrate:
  - pr_created → call sync_engine.on_agent_action_complete()
  - pr_merged → call sync_engine.on_agent_action_complete()
```

**Implementation location**: `.claude/skills/agentdb-state-manager/scripts/worktree_agent_integration.py`

### Integration Point 2: PHI Detection

Phase 2 provides a stub `_detect_phi()` method that always returns `False`. Phase 3 will implement sophisticated PHI detection:

```python
# Phase 3: Replace stub with real implementation
def _detect_phi(self, state: Dict[str, Any]) -> bool:
    """Detect Protected Health Information in state.

    Heuristics:
    - Field names: patient_id, mrn, ssn, dob, diagnosis
    - Patterns: SSN (XXX-XX-XXXX), MRN (alphanumeric)
    - NER: Named Entity Recognition for PII
    """
    # Check field names
    phi_fields = {'patient_id', 'mrn', 'ssn', 'dob', 'diagnosis', 'medical_record'}
    if any(field in state for field in phi_fields):
        return True

    # Check for SSN pattern
    import re
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    state_str = json.dumps(state)
    if re.search(ssn_pattern, state_str):
        return True

    # Check for MRN pattern (hospital-specific)
    # ...

    return False
```

**File to modify**: `.claude/skills/agentdb-state-manager/scripts/sync_engine.py` (replace `_detect_phi()` method)

### Integration Point 3: Target Agent Triggering

Phase 2 records sync executions but doesn't actually trigger target agents. Phase 3 must implement this:

```python
# Phase 3: Implement actual agent triggering
def trigger_target_agent(agent_id: str, action: str, state: Dict[str, Any]):
    """Trigger target agent with resolved parameters.

    Args:
        agent_id: Target agent (e.g., "assess", "integrate")
        action: Action to trigger (e.g., "run_tests", "create_pr")
        state: Workflow state to pass to agent
    """
    if agent_id == "assess" and action == "run_tests":
        # Trigger test runner
        run_tests_agent(state)
    elif agent_id == "integrate" and action == "create_pr":
        # Trigger PR creation
        create_pr_agent(state)
    else:
        logger.warning(f"Unknown target: {agent_id}.{action}")
```

**Implementation location**: `.claude/skills/agentdb-state-manager/scripts/worktree_agent_integration.py`

## Database Schema

Phase 2 migration added these fields to the Phase 1 schema:

**agent_synchronizations** (new fields):
- `trigger_agent_id` VARCHAR - Which agent triggers this sync
- `trigger_action` VARCHAR - What action triggers (e.g., "commit_complete")
- `trigger_pattern` JSON - Conditional pattern (e.g., `{"lint_status": "pass"}`)
- `target_agent_id` VARCHAR - Which agent to trigger
- `target_action` VARCHAR - What action to trigger
- `priority` INTEGER - Execution priority (higher = first)
- `enabled` BOOLEAN - Whether this sync rule is active

**sync_executions** (new fields):
- `provenance_hash` VARCHAR(64) UNIQUE - SHA-256 hash for idempotency
- `trigger_state_snapshot` JSON - Full state at trigger time
- `exec_status` VARCHAR - Phase 2 status ('pending', 'completed', 'failed')

## Example Workflow

### Scenario: Commit → Tests → PR

**Setup**: Define synchronization rules in database

```sql
-- Rule 1: develop.commit_complete → assess.run_tests (when lint passes)
INSERT INTO agent_synchronizations (
    sync_id, agent_id, trigger_agent_id, trigger_action, trigger_pattern,
    target_agent_id, target_action, priority, enabled,
    worktree_path, sync_type, source_location, target_location,
    pattern, status, created_by
) VALUES (
    'sync-commit-to-tests',
    'develop',
    'develop',
    'commit_complete',
    '{"lint_status": "pass"}',
    'assess',
    'run_tests',
    100,
    TRUE,
    NULL, 'agent_sync', 'worktree', 'main',
    'commit_complete', 'pending', 'workflow_setup'
);

-- Rule 2: assess.test_passed → integrate.create_pr (when coverage >= 85)
INSERT INTO agent_synchronizations (
    sync_id, agent_id, trigger_agent_id, trigger_action, trigger_pattern,
    target_agent_id, target_action, priority, enabled,
    worktree_path, sync_type, source_location, target_location,
    pattern, status, created_by
) VALUES (
    'sync-tests-to-pr',
    'assess',
    'assess',
    'test_passed',
    '{"coverage": {"percentage": 85}}',
    'integrate',
    'create_pr',
    100,
    TRUE,
    NULL, 'agent_sync', 'worktree', 'main',
    'test_passed', 'pending', 'workflow_setup'
);
```

**Execution**:

```python
# Step 1: Developer commits code
# Phase 3 agent hook calls:
exec_ids = sync_engine.on_agent_action_complete(
    agent_id="develop",
    action="commit_complete",
    flow_token="worktree-auth-20251117",
    state_snapshot={
        "commit_sha": "abc123",
        "lint_status": "pass"  # Matches sync-commit-to-tests pattern
    }
)
# Returns: ['exec-uuid-1'] - sync-commit-to-tests triggered

# Phase 3: Trigger assess.run_tests
trigger_target_agent("assess", "run_tests", state_snapshot)

# Step 2: Tests pass with good coverage
# Phase 3 agent hook calls:
exec_ids = sync_engine.on_agent_action_complete(
    agent_id="assess",
    action="test_passed",
    flow_token="worktree-auth-20251117",
    state_snapshot={
        "coverage": {"percentage": 85},  # Matches sync-tests-to-pr pattern
        "tests": {"passed": 150, "failed": 0}
    }
)
# Returns: ['exec-uuid-2'] - sync-tests-to-pr triggered

# Phase 3: Trigger integrate.create_pr
trigger_target_agent("integrate", "create_pr", state_snapshot)
```

## Performance Considerations

Phase 2 meets the following performance targets:

- **p95 latency**: <100ms for single agent
- **p99 hash computation**: <1ms
- **Idempotency**: Zero duplicates in 10k iteration test

Phase 3 should:
1. **Cache sync engine instance** (singleton pattern)
2. **Batch execution ID queries** if triggering multiple agents
3. **Monitor latency** in production (add metrics)

## Testing Integration

Phase 3 should test integration by:

1. **Unit tests**: Mock `SynchronizationEngine` methods
2. **Integration tests**: Use real engine with test database
3. **E2E tests**: Full workflow from commit → tests → PR

**Example integration test**:

```python
def test_commit_to_tests_workflow(sync_engine):
    """Test full workflow: commit → tests."""

    # Trigger commit_complete
    exec_ids = sync_engine.on_agent_action_complete(
        agent_id="develop",
        action="commit_complete",
        flow_token="test-workflow",
        state_snapshot={"lint_status": "pass"}
    )

    # Verify sync triggered
    assert len(exec_ids) == 1

    # Verify target agent details
    result = sync_engine.conn.execute("""
        SELECT s.target_agent_id, s.target_action
        FROM sync_executions e
        JOIN agent_synchronizations s ON e.sync_id = s.sync_id
        WHERE e.execution_id = ?
    """, [exec_ids[0]]).fetchone()

    assert result[0] == "assess"
    assert result[1] == "run_tests"
```

## Error Handling

Phase 2 follows **append-only paradigm** - errors are logged but don't crash:

```python
try:
    execution_id = self._execute_sync(...)
    execution_ids.append(execution_id)
except Exception as e:
    # Log error but don't raise (append-only paradigm)
    logger.error(f"Failed to execute sync {sync['sync_id']}: {e}", exc_info=True)
```

Phase 3 should:
1. **Monitor error logs** for failed syncs
2. **Implement retry logic** if needed (with exponential backoff)
3. **Alert on repeated failures** (same sync fails >3 times)

## Feature Flags

Phase 3 should implement feature flags for gradual rollout:

```python
class SynchronizationEngine:
    def __init__(self, db_path: str, cache_ttl: int = 300, feature_flags: Dict[str, bool] = None):
        self.db_path = db_path
        self.cache_ttl = cache_ttl
        self.feature_flags = feature_flags or {}

    def on_agent_action_complete(self, ...):
        # Check if synchronization is enabled
        if not self.feature_flags.get('sync_enabled', True):
            logger.info("Synchronization disabled by feature flag")
            return []

        # Check if specific agent is enabled
        if not self.feature_flags.get(f'sync_{agent_id}_enabled', True):
            logger.info(f"Synchronization disabled for agent {agent_id}")
            return []

        # Continue with normal execution...
```

## Healthcare Compliance

Phase 2 logs all operations to `sync_audit_trail` with:
- **Actor attribution** (`actor`, `actor_role`)
- **PHI tracking** (`phi_involved`)
- **Compliance context** (purpose, legal basis, consent ID)

Phase 3 must:
1. **Implement real PHI detection** (replace stub)
2. **Add consent validation** before accessing PHI
3. **Ensure APPEND-ONLY** audit trail (no deletes/updates)

## Next Steps for Phase 3

1. **Create worktree_agent_integration.py**
   - Implement agent hooks
   - Call `on_agent_action_complete()` at lifecycle events

2. **Implement PHI detection**
   - Replace `_detect_phi()` stub
   - Add NER for PII detection

3. **Implement target agent triggering**
   - `trigger_target_agent()` function
   - Route to correct agent based on target_agent_id

4. **Add feature flags**
   - Gradual rollout control
   - Per-agent enable/disable

5. **Production monitoring**
   - Latency metrics
   - Error rate tracking
   - Sync execution analytics

## Contact

For questions about Phase 2 integration:
- Issue #160: https://github.com/stharrold/german/issues/160
- Issue #161: https://github.com/stharrold/german/issues/161 (Phase 3)
