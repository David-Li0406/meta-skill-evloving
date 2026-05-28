#!/usr/bin/env python3
"""Worktree-aware agent integration utilities.

Provides flow token extraction and sync completion triggers using
worktree context detection.

This module bridges git-workflow-manager with the worktree-aware
state management system.
"""

import sys
from pathlib import Path
from typing import Any

# Add workflow-utilities to path for worktree_context
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"),
)


def get_flow_token() -> str:
    """Get flow token using worktree context.

    The flow token identifies the current workflow session, derived from
    the git branch name or worktree ID.

    Returns:
        Flow token string (e.g., "feature/20251123T120000Z_auth-system"
        or "worktree-a1b2c3d4e5f6").
    """
    try:
        from worktree_context import get_worktree_context

        ctx = get_worktree_context()

        # Use branch name if it's a feature/hotfix/release branch
        if ctx.branch_name.startswith(("feature/", "hotfix/", "release/")):
            return ctx.branch_name

        # For contrib branches, use the branch name
        if ctx.branch_name.startswith("contrib/"):
            return ctx.branch_name

        # Fallback to worktree ID
        return f"worktree-{ctx.worktree_id}"

    except (ImportError, RuntimeError):
        # Fallback for non-git environments
        from uuid import uuid4

        return f"ad-hoc-{uuid4().hex[:8]}"


def get_worktree_info() -> dict[str, Any]:
    """Get comprehensive worktree information.

    Returns:
        Dictionary with worktree context information:
        - worktree_root: Path to worktree
        - is_worktree: Whether in a git worktree
        - worktree_id: Stable identifier
        - branch_name: Current branch
        - flow_token: Computed flow token
    """
    try:
        from worktree_context import get_worktree_context

        ctx = get_worktree_context()
        return {
            "worktree_root": str(ctx.worktree_root),
            "is_worktree": ctx.is_worktree,
            "worktree_id": ctx.worktree_id,
            "branch_name": ctx.branch_name,
            "flow_token": get_flow_token(),
        }
    except (ImportError, RuntimeError):
        return {
            "worktree_root": str(Path.cwd()),
            "is_worktree": False,
            "worktree_id": "",
            "branch_name": "unknown",
            "flow_token": get_flow_token(),
        }


async def trigger_sync_completion(
    agent_id: str,
    action: str,
    state_snapshot: dict[str, Any],
    context: dict[str, Any] | None = None,
) -> list[str]:
    """Trigger synchronization after agent action completes.

    Integrates with the AgentDB synchronization engine to record
    agent actions and trigger downstream syncs.

    Args:
        agent_id: Identifier for the agent (e.g., "assess", "develop").
        action: Action that completed (e.g., "test_complete", "commit_complete").
        state_snapshot: Current state to record.
        context: Additional context information.

    Returns:
        List of execution IDs for triggered syncs.
    """
    try:
        # Import sync engine
        agentdb_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(agentdb_path) not in sys.path:
            sys.path.insert(0, str(agentdb_path))

        from sync_engine import SynchronizationEngine

        # Get worktree-aware flow token
        flow_token = get_flow_token()

        # Initialize engine (uses worktree-aware defaults)
        engine = SynchronizationEngine()

        # Record the action
        execution_ids = engine.on_agent_action_complete(
            agent_id=agent_id,
            action=action,
            flow_token=flow_token,
            state_snapshot=state_snapshot,
        )

        return execution_ids

    except Exception as e:
        # Graceful degradation - don't fail the workflow
        import logging

        logging.getLogger(__name__).warning(f"Sync completion trigger failed (non-critical): {e}")
        return []


if __name__ == "__main__":
    # Quick test when run directly
    print("Worktree Agent Integration")
    print("=" * 40)

    info = get_worktree_info()
    for key, value in info.items():
        print(f"{key}: {value}")
