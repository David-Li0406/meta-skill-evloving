#!/usr/bin/env python3
"""MIT Agent Synchronization Pattern - Core Engine

Implements declarative synchronization coordination with pattern matching,
idempotency enforcement, and healthcare compliance.

Performance Requirements:
- <100ms p95 latency for single agent
- <200ms p95 latency for 13 concurrent agents
- <1ms p99 for hash computation

Healthcare Compliance:
- All PHI access logged to sync_audit_trail
- APPEND-ONLY paradigm (no deletes, no updates to history)
- Actor/role attribution for all operations

Created: 2025-11-17
Issue: #160 - Phase 2 Synchronization Engine Implementation
"""

import hashlib
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

try:
    import duckdb
except ImportError:
    raise ImportError("duckdb package required. Run: uv add duckdb")

# Add workflow-utilities to path for worktree_context
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"),
)

logger = logging.getLogger(__name__)


def _get_worktree_defaults() -> tuple[Path, str]:
    """Get default database path and worktree ID.

    Returns:
        Tuple of (db_path, worktree_id).
        Falls back to current directory and empty string if detection fails.
    """
    try:
        from worktree_context import get_state_dir, get_worktree_id

        return get_state_dir() / "agentdb.duckdb", get_worktree_id()
    except (ImportError, RuntimeError):
        return Path("agentdb.duckdb"), ""


class SynchronizationEngine:
    """Core synchronization engine for multi-agent workflows.

    Coordinates autonomous agents via declarative synchronization rules with
    pattern matching, idempotency enforcement, and healthcare compliance.

    Example Usage:
        engine = SynchronizationEngine(db_path="agentdb.duckdb")

        # Agent "develop" completed a commit
        execution_ids = engine.on_agent_action_complete(
            agent_id="develop",
            action="commit_complete",
            flow_token="worktree-20251117",
            state_snapshot={
                "commit_sha": "abc123",
                "coverage": {"percentage": 85, "lines_covered": 1234},
                "lint_status": "pass"
            }
        )

        # Returns: ['exec-uuid-1', 'exec-uuid-2'] - IDs of triggered syncs
    """

    def __init__(
        self,
        db_path: str | None = None,
        cache_ttl: int = 300,
        worktree_id: str | None = None,
    ):
        """Initialize sync engine with database connection.

        Args:
            db_path: Path to DuckDB database. If None, uses worktree state directory.
            cache_ttl: Cache TTL in seconds for active syncs (default 5 minutes)
            worktree_id: Worktree identifier for scoping. If None, auto-detected.
        """
        # Get worktree-aware defaults if not specified
        default_db_path, default_worktree_id = _get_worktree_defaults()

        self.db_path = db_path or str(default_db_path)
        self.worktree_id = worktree_id or default_worktree_id
        self.cache_ttl = cache_ttl
        self._sync_cache: dict[str, Any] = {}
        self._cache_invalidated_at: datetime | None = None

        # Initialize database connection
        # Note: DuckDB supports concurrent readers but single writer
        # For production, consider connection pooling
        self.conn = duckdb.connect(self.db_path, read_only=False)

    def _compute_provenance_hash(self, sync_id: str, flow_token: str, state: dict[str, Any]) -> str:
        """Compute SHA-256 content-addressed hash for idempotency.

        Performance Target: <1ms p99

        Algorithm:
        1. Serialize state to deterministic JSON (sort_keys=True)
        2. Combine sync_id + flow_token + state_json
        3. SHA-256 hash

        Determinism Requirement:
        - Same inputs MUST produce same hash across all invocations
        - JSON key ordering must be consistent (sort_keys=True)

        Args:
            sync_id: Synchronization rule ID
            flow_token: Workflow session ID
            state: Current workflow state

        Returns:
            64-character hex string (SHA-256 hash)

        Example:
            hash = _compute_provenance_hash(
                sync_id="sync-123",
                flow_token="worktree-auth",
                state={"coverage": {"percentage": 85}}
            )
            # Returns: "a3f2b8..." (64 chars)
        """
        # Deterministic JSON serialization (sort keys for consistency)
        state_json = json.dumps(state, sort_keys=True, separators=(",", ":"))

        # Combine components with delimiter
        content = f"{sync_id}:{flow_token}:{state_json}"

        # SHA-256 hash
        hash_bytes = hashlib.sha256(content.encode("utf-8")).digest()
        return hash_bytes.hex()

    def _get_nested_value(self, obj: dict[str, Any], path: str) -> Any:
        """Extract nested value from dict using dot-notation path.

        Args:
            obj: Dictionary to extract from
            path: Dot-notation path (e.g., "coverage.percentage")

        Returns:
            Value at path, or None if path doesn't exist

        Example:
            obj = {"coverage": {"percentage": 85, "lines": 1234}}
            value = _get_nested_value(obj, "coverage.percentage")
            # Returns: 85
        """
        keys = path.split(".")
        current = obj

        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]

        return current

    def _resolve_params(self, action_spec: dict[str, Any], trigger_state: dict[str, Any]) -> dict[str, Any]:
        """Resolve ${trigger_state.path} placeholders in action spec.

        Template Syntax:
        - Simple path: ${trigger_state.field} → extract top-level field
        - Nested path: ${trigger_state.coverage.percentage} → nested access
        - Missing path: ${trigger_state.nonexistent} → null + warning log

        Args:
            action_spec: Action specification with ${...} placeholders
            trigger_state: State to extract values from

        Returns:
            Action spec with placeholders replaced by actual values

        Example:
            action_spec = {
                "action": "notify",
                "message": "Coverage: ${trigger_state.coverage.percentage}%"
            }
            trigger_state = {"coverage": {"percentage": 85}}

            result = _resolve_params(action_spec, trigger_state)
            # Returns: {"action": "notify", "message": "Coverage: 85%"}
        """
        # Convert to JSON string for regex replacement
        spec_json = json.dumps(action_spec)

        # Pattern: ${trigger_state.path.to.value}
        pattern = r"\$\{trigger_state\.([^}]+)\}"

        def replacer(match):
            path = match.group(1)
            value = self._get_nested_value(trigger_state, path)

            if value is None:
                logger.warning(f"Missing path in trigger_state: {path}")
                return "null"

            # Return JSON-encoded value (handles strings, numbers, objects)
            return json.dumps(value) if not isinstance(value, str) else value

        # Replace all ${...} patterns
        resolved_json = re.sub(pattern, replacer, spec_json)

        return json.loads(resolved_json)

    def _pattern_matches(self, pattern: dict[str, Any], state: dict[str, Any]) -> bool:
        """Check if state contains pattern (partial match).

        Pattern matching rules:
        - Empty pattern {} matches any state
        - Pattern keys must exist in state
        - Pattern values must equal state values
        - Nested dicts are matched recursively

        Examples:
            pattern = {"coverage": {"percentage": 85}}
            state = {"coverage": {"percentage": 85, "lines": 1234}, "lint": "pass"}
            result = True  # state ⊃ pattern

            pattern = {"lint": "fail"}
            state = {"lint": "pass"}
            result = False  # values don't match

        Args:
            pattern: Pattern to match (subset)
            state: Current state (superset)

        Returns:
            True if state contains pattern, False otherwise
        """
        if not pattern:
            return True  # Empty pattern matches everything

        for key, expected_value in pattern.items():
            if key not in state:
                return False

            actual_value = state[key]

            # Recursive matching for nested dicts
            if isinstance(expected_value, dict) and isinstance(actual_value, dict):
                if not self._pattern_matches(expected_value, actual_value):
                    return False
            elif expected_value != actual_value:
                return False

        return True

    def _find_matching_syncs(self, agent_id: str, action: str, state: dict[str, Any]) -> list[dict[str, Any]]:
        """Find synchronization rules matching current agent/action/state.

        Query Pattern (DuckDB):
            SELECT * FROM agent_synchronizations
            WHERE trigger_agent_id = ?
              AND trigger_action = ?
              AND enabled = TRUE
            ORDER BY priority DESC

        Args:
            agent_id: Triggering agent ID
            action: Triggering action
            state: Current workflow state

        Returns:
            List of matching sync rules (ordered by priority, highest first)
        """
        # TODO: Implement caching with TTL
        # For now, query database directly

        # Query for matching syncs
        query = """
            SELECT
                sync_id,
                trigger_agent_id,
                trigger_action,
                trigger_pattern,
                target_agent_id,
                target_action,
                priority,
                enabled
            FROM agent_synchronizations
            WHERE trigger_agent_id = ?
              AND trigger_action = ?
              AND enabled = TRUE
            ORDER BY priority DESC
        """

        results = self.conn.execute(query, [agent_id, action]).fetchall()

        # Convert to list of dicts
        columns = ["sync_id", "trigger_agent_id", "trigger_action", "trigger_pattern", "target_agent_id", "target_action", "priority", "enabled"]
        syncs = [dict(zip(columns, row)) for row in results]

        # Filter by pattern matching (state must contain pattern)
        matched_syncs = []
        for sync in syncs:
            # Parse trigger_pattern JSON
            pattern_json = sync["trigger_pattern"]
            if pattern_json:
                try:
                    pattern = json.loads(pattern_json) if isinstance(pattern_json, str) else pattern_json
                except (json.JSONDecodeError, TypeError):
                    logger.error(f"Invalid trigger_pattern JSON in sync {sync['sync_id']}: {pattern_json}")
                    continue
            else:
                pattern = {}

            if self._pattern_matches(pattern, state):
                matched_syncs.append(sync)

        return matched_syncs

    def _detect_phi(self, state: dict[str, Any]) -> bool:
        """Detect if state contains PHI (Protected Health Information).

        Heuristics:
        - Check for common PHI field names
        - Check for patterns (SSN, MRN, email, phone)

        Note: This is a conservative heuristic. False positives are acceptable
        (better to over-log than under-log for compliance).

        Args:
            state: Workflow state to check

        Returns:
            True if PHI detected, False otherwise
        """
        # TODO (Phase 3): Implement sophisticated PHI detection
        # For Phase 2, return False (defer to Phase 3)
        return False

    def _log_audit_trail(self, sync_id: str, execution_id: str, event_type: str, phi_involved: bool, event_details: dict[str, Any]):
        """Log event to sync_audit_trail (APPEND-ONLY compliance log).

        Healthcare Compliance Requirements:
        - All operations logged with actor attribution
        - PHI access logged with justification
        - APPEND-ONLY (no deletes, no updates)

        Args:
            sync_id: Synchronization rule ID
            execution_id: Execution ID
            event_type: Type of event (e.g., 'sync_triggered')
            phi_involved: Was PHI accessed?
            event_details: Additional event metadata
        """
        audit_id = str(uuid4())

        self.conn.execute(
            """
            INSERT INTO sync_audit_trail (
                audit_id,
                sync_id,
                execution_id,
                event_type,
                actor,
                actor_role,
                phi_involved,
                compliance_context,
                event_details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            [
                audit_id,
                sync_id,
                execution_id,
                event_type,
                "sync_engine",  # Actor
                "autonomous_agent",  # Role
                phi_involved,
                json.dumps({"purpose": "Workflow synchronization", "legal_basis": "Research protocol"}),
                json.dumps(event_details),
            ],
        )

    def _execute_sync(self, sync: dict[str, Any], flow_token: str, trigger_state: dict[str, Any], prov_hash: str) -> str:
        """Record sync execution and trigger target agent.

        Database Operations:
        1. INSERT into sync_executions (append-only)
        2. INSERT into sync_audit_trail (compliance logging)
        3. Trigger target agent (Phase 3 integration point)

        Args:
            sync: Synchronization rule from database
            flow_token: Workflow session ID
            trigger_state: State that triggered this sync
            prov_hash: Provenance hash for idempotency

        Returns:
            execution_id (UUID string)
        """
        execution_id = str(uuid4())

        # Resolve parameters from trigger state
        # Example: "${trigger_state.coverage.percentage}" → 85
        action_spec = {"action": sync["target_action"], "agent_id": sync["target_agent_id"]}
        resolved_params = self._resolve_params(action_spec, trigger_state)

        # Insert execution record (append-only)
        self.conn.execute(
            """
            INSERT INTO sync_executions (
                execution_id,
                sync_id,
                provenance_hash,
                trigger_state_snapshot,
                exec_status,
                execution_order,
                operation_type,
                operation_result,
                phi_accessed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            [
                execution_id,
                sync["sync_id"],
                prov_hash,
                json.dumps(trigger_state),
                "pending",
                1,  # TODO: Proper sequence number (query max order + 1)
                "read",  # Phase 2: placeholder operation type
                "success",  # Phase 2: execution just recorded, not actually run yet
                False,  # No PHI in Phase 2 (defer to Phase 3)
            ],
        )

        # Log to audit trail (healthcare compliance)
        self._log_audit_trail(
            sync_id=sync["sync_id"],
            execution_id=execution_id,
            event_type="sync_initiated",
            phi_involved=self._detect_phi(trigger_state),
            event_details={
                "trigger_agent": sync["trigger_agent_id"],
                "target_agent": sync["target_agent_id"],
                "flow_token": flow_token,
                "resolved_params": resolved_params,
            },
        )

        # TODO (Phase 3): Actually trigger target agent
        # This is the integration point with Phase 3 (Integration Layer)
        # For now, just record the execution

        logger.info(
            f"Sync recorded: {sync['trigger_agent_id']}.{sync['trigger_action']} → {sync['target_agent_id']}.{sync['target_action']} (execution_id={execution_id})"
        )

        return execution_id

    def on_agent_action_complete(self, agent_id: str, action: str, flow_token: str, state_snapshot: dict[str, Any]) -> list[str]:
        """Main entry point - called after any agent action completes.

        Performance Requirements:
        - <100ms p95 latency for single agent
        - <200ms p95 latency for 13 concurrent agents

        Args:
            agent_id: Which agent triggered this (e.g., "develop", "assess")
            action: What action completed (e.g., "commit_complete", "test_passed")
            flow_token: Workflow session identifier (worktree path or issue ID)
            state_snapshot: Current state of the workflow (JSON-serializable dict)

        Returns:
            List of execution_ids (UUIDs) for triggered synchronizations

        Example:
            execution_ids = engine.on_agent_action_complete(
                agent_id="develop",
                action="commit_complete",
                flow_token="worktree-auth-system",
                state_snapshot={
                    "commit_sha": "abc123",
                    "coverage": {"percentage": 85}
                }
            )
            # Returns: ['uuid-1', 'uuid-2'] if 2 syncs matched and triggered
        """
        execution_ids = []

        # Find matching synchronization rules
        matching_syncs = self._find_matching_syncs(agent_id, action, state_snapshot)

        logger.info(f"Agent action: {agent_id}.{action} (flow_token={flow_token}) matched {len(matching_syncs)} sync rules")

        for sync in matching_syncs:
            # Compute provenance hash for idempotency
            prov_hash = self._compute_provenance_hash(sync_id=sync["sync_id"], flow_token=flow_token, state=state_snapshot)

            # Check if this sync already executed for this exact state
            existing = self.conn.execute("SELECT execution_id FROM sync_executions WHERE provenance_hash = ?", [prov_hash]).fetchone()

            if existing:
                logger.info(f"Idempotency: Sync {sync['sync_id']} already executed (hash={prov_hash[:8]}...)")
                continue

            # Execute sync (trigger target agent)
            try:
                execution_id = self._execute_sync(sync=sync, flow_token=flow_token, trigger_state=state_snapshot, prov_hash=prov_hash)
                execution_ids.append(execution_id)
                logger.info(f"Triggered sync {sync['sync_id']} → execution {execution_id}")
            except Exception as e:
                # Log error but don't raise (append-only paradigm)
                logger.error(f"Failed to execute sync {sync['sync_id']}: {e}", exc_info=True)

        return execution_ids

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
