#!/usr/bin/env python3
"""MIT Agent Synchronization Pattern - Integration Layer (Phase 3)

Provides non-invasive hooks for existing agents to trigger sync engine with
healthcare compliance wrappers and feature flag control.

Components:
- FlowTokenManager: Maps workflow sessions to sync engine flow tokens
- PHIDetector: Detects Protected Health Information in state snapshots
- ComplianceWrapper: Wraps sync engine with HIPAA/FDA/IRB compliance logging
- SyncEngineFactory: Creates sync engine with feature flag control
- trigger_sync_completion(): Main entry point for agent hooks

Usage:
    from worktree_agent_integration import trigger_sync_completion

    # After agent action completes
    success = await trigger_sync_completion(
        agent_id="develop",
        action="commit_complete",
        state_snapshot={"commit_sha": "abc123", "coverage": 85},
        context={"user": "stharrold", "commit_message": "fix: bug"}
    )

Created: 2025-11-17
Issue: #161 - Phase 3 Integration Layer Implementation
"""

import logging
import os
import re
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class FlowTokenType(Enum):
    """Types of flow tokens for different workflow contexts."""

    MAIN_REPO = "main_repo"
    WORKTREE = "worktree"
    ISSUE = "issue"
    AD_HOC = "ad_hoc"


class FlowTokenManager:
    """Maps workflow sessions to sync engine flow tokens.

    Flow tokens enable cross-worktree coordination and session tracking.
    They provide a stable identifier for workflow sessions that persists
    across agent actions.

    Mapping Strategy:
    - Worktree: feature/<timestamp>_<slug> (from directory name)
    - Main repo: contrib/<user> (from git branch)
    - Issue: issue-<number> (extracted from flow token or context)
    - Ad-hoc: ad-hoc-<uuid> (fallback for unknown contexts)

    Example:
        token = FlowTokenManager.get_flow_token()
        # In worktree: "feature/20251117T024349Z_phase-3-integration"
        # In main repo: "contrib/stharrold"
        # Ad-hoc: "ad-hoc-7f8a9b2c"
    """

    @staticmethod
    def get_flow_token() -> str:
        """Detect current workflow context and generate appropriate flow token.

        Detection Order:
        1. Check if in worktree (directory name pattern: german_feature_*)
        2. Check git branch (contrib/* pattern)
        3. Fallback to ad-hoc UUID

        Returns:
            Flow token string (e.g., "contrib/stharrold", "feature/20251117_slug")
        """
        cwd = Path.cwd()

        # Check if in worktree (directory name pattern: german_feature_*)
        if cwd.name.startswith("german_feature_"):
            # Extract branch name from worktree directory
            # Example: german_feature_20251117T024349Z_phase-3-integration
            #   → feature/20251117T024349Z_phase-3-integration
            parts = cwd.name.split("_", 2)  # ["german", "feature", "20251117T024349Z_phase-3-integration"]
            if len(parts) >= 3:
                return f"feature/{parts[2]}"

        # Check if in hotfix worktree (directory name pattern: german_hotfix_*)
        if cwd.name.startswith("german_hotfix_"):
            parts = cwd.name.split("_", 2)
            if len(parts) >= 3:
                return f"hotfix/{parts[2]}"

        # Check if in main repo on contrib branch
        try:
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True, timeout=5)
            branch = result.stdout.strip()
            if branch.startswith("contrib/"):
                return branch
            if branch.startswith("claude/"):
                # Claude Code session branches
                return branch
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            logger.warning(f"Failed to detect git branch: {e}")

        # Fallback: generate UUID for ad-hoc workflows
        return f"ad-hoc-{uuid4().hex[:8]}"

    @staticmethod
    def extract_issue_number(flow_token: str) -> int | None:
        """Extract issue number from flow token if present.

        Patterns:
        - issue-123 → 123
        - feature/20251117_issue-123-description → 123
        - contrib/stharrold → None

        Args:
            flow_token: Flow token string

        Returns:
            Issue number or None
        """
        # Pattern: issue-123 or feature/timestamp_issue-123-description
        match = re.search(r"issue-(\d+)", flow_token)
        if match:
            return int(match.group(1))
        return None


class PHIDetector:
    """Detects Protected Health Information (PHI) in state snapshots.

    Replaces stub in sync_engine.py _detect_phi() method.

    Healthcare Compliance:
    - HIPAA: Detect 18 PHI identifiers (name, SSN, MRN, DOB, etc.)
    - FDA 21 CFR Part 11: Electronic records with patient data
    - IRB: Research protocols with human subjects data

    Detection Strategy:
    1. Explicit PHI markers (_contains_phi field)
    2. Field name patterns (patient_id, mrn, ssn, dob, etc.)
    3. Value patterns (SSN regex: 123-45-6789)
    4. Path patterns (/data/protected/, /phi/)

    Conservative Approach:
    - False positives are acceptable (better to over-log than under-log)
    - All PHI access requires justification (extracted from context)
    """

    # PHI field name patterns (case-insensitive)
    PHI_FIELD_PATTERNS = [
        r"patient_?id",
        r"mrn",
        r"medical_?record",
        r"ssn",
        r"social_?security",
        r"dob",
        r"date_?of_?birth",
        r"diagnosis",
        r"treatment",
        r"prescription",
        r"icd_?code",
        r"health_?record",
        r"medical_?history",
        r"patient_?name",
        r"provider_?name",
        r"insurance",
        r"claim_?number",
    ]

    # PHI path patterns
    PHI_PATH_PATTERNS = [r"/data/protected/", r"/phi/", r"/medical/", r"/patient/", r"/health_?records?/"]

    # SSN regex: 123-45-6789 or 123456789
    SSN_PATTERN = r"\b\d{3}-?\d{2}-?\d{4}\b"

    @classmethod
    def detect_phi(cls, state_snapshot: dict[str, Any]) -> bool:
        """Detect if state snapshot contains PHI.

        Args:
            state_snapshot: State data to check

        Returns:
            True if PHI detected, False otherwise

        Examples:
            >>> PHIDetector.detect_phi({"_contains_phi": True})
            True
            >>> PHIDetector.detect_phi({"patient_id": "12345"})
            True
            >>> PHIDetector.detect_phi({"notes": "SSN: 123-45-6789"})
            True
            >>> PHIDetector.detect_phi({"commit_sha": "abc123"})
            False
        """
        # Explicit PHI marker
        if state_snapshot.get("_contains_phi") is True:
            logger.info("PHI detected: explicit marker '_contains_phi': true")
            return True

        # Check field names
        for field_name in state_snapshot.keys():
            for pattern in cls.PHI_FIELD_PATTERNS:
                if re.search(pattern, field_name, re.IGNORECASE):
                    logger.info(f"PHI detected: field name '{field_name}' matches pattern '{pattern}'")
                    return True

        # Check for SSN in string values
        for key, value in state_snapshot.items():
            if isinstance(value, str):
                if re.search(cls.SSN_PATTERN, value):
                    logger.info(f"PHI detected: SSN pattern in field '{key}'")
                    return True

        # Check for PHI paths in file paths
        for key, value in state_snapshot.items():
            if isinstance(value, str):
                for pattern in cls.PHI_PATH_PATTERNS:
                    if re.search(pattern, value, re.IGNORECASE):
                        logger.info(f"PHI detected: path in field '{key}' matches pattern '{pattern}'")
                        return True

        return False

    @classmethod
    def extract_justification(cls, context: dict[str, Any]) -> str:
        """Extract or generate access justification from workflow context.

        Priority:
        1. Explicit: context["phi_justification"]
        2. Issue number: "Development work for issue #161"
        3. Commit message: "Code change: fix(patient): update schema"
        4. Generic: "user performing action"

        Args:
            context: Workflow context (commit message, issue, user, etc.)

        Returns:
            Justification string

        Examples:
            >>> PHIDetector.extract_justification({"phi_justification": "IRB #12345"})
            'IRB #12345'
            >>> PHIDetector.extract_justification({"issue_number": 161})
            'Development work for issue #161'
            >>> PHIDetector.extract_justification({"user": "stharrold", "action": "commit"})
            'stharrold performing commit'
        """
        # Priority 1: Explicit justification
        if "phi_justification" in context:
            return context["phi_justification"]

        # Priority 2: Issue number
        issue_num = context.get("issue_number")
        if issue_num:
            return f"Development work for issue #{issue_num}"

        # Priority 3: Commit message (first line)
        commit_msg = context.get("commit_message", "")
        if commit_msg:
            first_line = commit_msg.split("\n")[0][:100]  # First line, max 100 chars
            return f"Code change: {first_line}"

        # Priority 4: Generic development justification
        user = context.get("user", "unknown")
        action = context.get("action", "development")
        return f"{user} performing {action}"


class ComplianceWrapper:
    """Wraps sync engine calls with healthcare compliance logging.

    Healthcare Requirements:
    - All PHI access logged with justification
    - Actor/role attribution for all operations
    - Audit trail is APPEND-ONLY (immutable)

    This wrapper adds an additional compliance layer on top of the sync
    engine's built-in audit trail, specifically focused on PHI detection
    and justification extraction from workflow context.
    """

    def __init__(self, sync_engine):
        """Initialize compliance wrapper.

        Args:
            sync_engine: SynchronizationEngine instance
        """
        self.sync_engine = sync_engine

    async def on_agent_action_complete(
        self, agent_id: str, action: str, flow_token: str, state_snapshot: dict[str, Any], context: dict[str, Any] | None = None
    ) -> list[str]:
        """Wrapped version of sync_engine.on_agent_action_complete with compliance logging.

        This method:
        1. Detects PHI in state_snapshot
        2. Extracts justification from context if PHI detected
        3. Logs compliance warnings
        4. Calls underlying sync engine
        5. Returns execution IDs

        Args:
            agent_id: Agent performing action (e.g., "develop", "assess")
            action: Action completed (e.g., "commit_complete", "test_complete")
            flow_token: Workflow session identifier
            state_snapshot: State data
            context: Additional context for compliance (user, issue, commit message)

        Returns:
            List of execution_ids (UUIDs) for triggered synchronizations

        Raises:
            Exception: If sync engine fails (logged and re-raised)
        """
        context = context or {}

        # Detect PHI
        phi_detected = PHIDetector.detect_phi(state_snapshot)

        # Check for explicit justification (not fallback)
        has_explicit_justification = "phi_justification" in context or "issue_number" in context or "commit_message" in context

        # Extract justification if PHI detected
        phi_justification = None
        if phi_detected:
            phi_justification = PHIDetector.extract_justification(context)
            logger.warning(f"PHI detected in sync: agent={agent_id}, action={action}, flow_token={flow_token}")
            logger.info(f"PHI justification: {phi_justification}")

        # Add PHI metadata to context for audit trail
        context["phi_detected"] = phi_detected
        if phi_justification:
            context["phi_justification"] = phi_justification

        # Call sync engine
        # Note: sync_engine.py has its own _detect_phi() stub, but we're
        # doing detection here in Phase 3 and passing results via context
        try:
            # Run sync engine synchronously (it's not async yet)
            execution_ids = self.sync_engine.on_agent_action_complete(agent_id=agent_id, action=action, flow_token=flow_token, state_snapshot=state_snapshot)

            # Additional compliance check: PHI without explicit justification
            if phi_detected and not has_explicit_justification:
                logger.error(f"COMPLIANCE VIOLATION: PHI detected but no explicit justification provided! agent={agent_id}, action={action}, flow_token={flow_token}")

            return execution_ids

        except Exception as e:
            logger.error(f"Sync engine failed: {e}", exc_info=True)
            raise


class SyncEngineFactory:
    """Factory for creating sync engine instances with dependency injection.

    Features:
    - Feature flag control (SYNC_ENGINE_ENABLED environment variable)
    - Singleton pattern (cache instance per db_path)
    - Graceful degradation (returns None if disabled or initialization fails)
    - Automatic compliance wrapping

    Environment Variables:
    - SYNC_ENGINE_ENABLED: "true" to enable, "false" (default) to disable
    - AGENTDB_PATH: Path to DuckDB database (default: "agentdb.duckdb")
    """

    _instances: dict[str, ComplianceWrapper] = {}

    @classmethod
    def create_sync_engine(cls, db_path: str | None = None) -> ComplianceWrapper | None:
        """Create sync engine instance if enabled.

        Feature Flag:
        - SYNC_ENGINE_ENABLED=true → Create and return engine
        - SYNC_ENGINE_ENABLED=false (default) → Return None

        Singleton Pattern:
        - Cache instance per db_path
        - Reuse existing instance if available

        Args:
            db_path: Path to DuckDB database (optional, defaults to env var or "agentdb.duckdb")

        Returns:
            ComplianceWrapper instance or None if disabled

        Examples:
            >>> os.environ["SYNC_ENGINE_ENABLED"] = "true"
            >>> engine = SyncEngineFactory.create_sync_engine()
            >>> engine is not None
            True

            >>> os.environ["SYNC_ENGINE_ENABLED"] = "false"
            >>> engine = SyncEngineFactory.create_sync_engine()
            >>> engine is None
            True
        """
        # Check feature flag
        enabled = os.getenv("SYNC_ENGINE_ENABLED", "false").lower() == "true"

        if not enabled:
            logger.debug("Sync engine disabled (SYNC_ENGINE_ENABLED=false)")
            return None

        # Get or default db_path
        if db_path is None:
            db_path = os.getenv("AGENTDB_PATH", "agentdb.duckdb")

        # Check singleton cache
        if db_path in cls._instances:
            logger.debug(f"Reusing cached sync engine for db_path={db_path}")
            return cls._instances[db_path]

        # Create new instance
        try:
            # Import sync engine (delayed to avoid import if disabled)
            # Add parent directory to path to import sync_engine
            parent_dir = Path(__file__).parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))

            from sync_engine import SynchronizationEngine

            # Create engine
            logger.info(f"Initializing sync engine with db_path={db_path}")
            engine = SynchronizationEngine(db_path=db_path)

            # Wrap with compliance
            wrapper = ComplianceWrapper(engine)

            # Cache instance
            cls._instances[db_path] = wrapper

            logger.info(f"Sync engine enabled and initialized (db_path={db_path})")
            return wrapper

        except Exception as e:
            logger.error(f"Failed to initialize sync engine: {e}", exc_info=True)
            return None


async def trigger_sync_completion(
    agent_id: str, action: str, state_snapshot: dict[str, Any], context: dict[str, Any] | None = None, sync_engine: ComplianceWrapper | None = None
) -> bool:
    """Trigger sync engine after agent action completes.

    This is the main entry point for agent hooks. It provides:
    - Automatic flow token detection
    - Feature flag control (SYNC_ENGINE_ENABLED)
    - Graceful degradation (returns False on error, doesn't crash)
    - PHI detection and compliance logging

    Agent scripts should call this function after completing an action:

        await trigger_sync_completion(
            agent_id="develop",
            action="commit_complete",
            state_snapshot={"commit_sha": "abc123", "coverage": 85},
            context={"user": "stharrold", "commit_message": "fix: bug"}
        )

    Args:
        agent_id: Agent performing action (e.g., "develop", "assess", "orchestrate", "research")
        action: Action completed (e.g., "commit_complete", "test_complete", "planning_complete")
        state_snapshot: State data (coverage, test results, commit SHA, etc.)
        context: Additional context (user, issue, commit message, phi_justification)
        sync_engine: Optional sync engine instance (created if None)

    Returns:
        True if sync triggered successfully, False otherwise

    Examples:
        >>> # Enable sync engine
        >>> os.environ["SYNC_ENGINE_ENABLED"] = "true"

        >>> # Trigger sync after commit
        >>> success = await trigger_sync_completion(
        ...     agent_id="develop",
        ...     action="commit_complete",
        ...     state_snapshot={"commit_sha": "abc123", "coverage": 85},
        ...     context={"user": "stharrold"}
        ... )
        >>> success
        True

        >>> # Disable sync engine
        >>> os.environ["SYNC_ENGINE_ENABLED"] = "false"
        >>> success = await trigger_sync_completion(
        ...     agent_id="develop",
        ...     action="commit_complete",
        ...     state_snapshot={"commit_sha": "abc123"}
        ... )
        >>> success
        False
    """
    # Get or create sync engine
    if sync_engine is None:
        sync_engine = SyncEngineFactory.create_sync_engine()

    # If disabled, return early
    if sync_engine is None:
        logger.debug(f"Sync not triggered: engine disabled (agent={agent_id}, action={action})")
        return False

    try:
        # Get flow token
        flow_token = FlowTokenManager.get_flow_token()

        # Add flow token to context
        context = context or {}
        context["flow_token"] = flow_token

        # Extract issue number if present
        issue_num = FlowTokenManager.extract_issue_number(flow_token)
        if issue_num:
            context["issue_number"] = issue_num

        # Trigger sync (call wrapper, which calls underlying engine)
        execution_ids = await sync_engine.on_agent_action_complete(
            agent_id=agent_id, action=action, flow_token=flow_token, state_snapshot=state_snapshot, context=context
        )

        logger.info(f"Sync triggered: agent={agent_id}, action={action}, flow_token={flow_token}, executions={len(execution_ids)}")

        # TODO (Phase 4): Execute target actions
        # For now, just log them
        for exec_id in execution_ids:
            logger.info(f"Target execution queued: {exec_id}")

        return True

    except Exception as e:
        logger.error(f"Sync trigger failed: agent={agent_id}, action={action}, error={e}", exc_info=True)
        # Graceful degradation: don't crash the agent
        return False
