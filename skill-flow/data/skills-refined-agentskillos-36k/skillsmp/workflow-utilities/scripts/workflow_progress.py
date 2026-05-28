"""Workflow progress tracking in worktree state directory.

This module manages workflow progress state stored in .claude-state/workflow.json.
It provides functions to read and update workflow progress without conflicts
across concurrent worktrees.

Usage:
    from workflow_progress import get_workflow_progress, update_workflow_progress

    # Get current progress
    progress = get_workflow_progress()
    print(f"Current step: {progress['current_step']}")

    # Update progress
    update_workflow_progress(step=3, artifact="specs/006-feature/tasks.md")
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import UTC, datetime
from typing import Any

from worktree_context import get_state_dir, get_worktree_id

logger = logging.getLogger(__name__)


def get_workflow_progress() -> dict[str, Any]:
    """Load workflow progress from state directory.

    Reads the workflow.json file from the worktree's state directory.
    Returns a default structure if the file doesn't exist.

    Returns:
        Dictionary containing workflow progress state:
        - worktree_id: str
        - current_step: int
        - steps_completed: list[int]
        - artifacts: dict[str, str]
        - last_updated: str (ISO format)
    """
    state_dir = get_state_dir()
    progress_file = state_dir / "workflow.json"

    if progress_file.exists():
        try:
            return json.loads(progress_file.read_text())
        except json.JSONDecodeError:
            logger.warning(
                "Corrupted workflow.json at %s, returning default state",
                progress_file,
            )
            pass

    # Return default structure
    return {
        "worktree_id": get_worktree_id(),
        "current_step": 0,
        "steps_completed": [],
        "artifacts": {},
        "last_updated": None,
    }


def update_workflow_progress(
    step: int | None = None,
    artifact: str | None = None,
    feature_branch: str | None = None,
    session_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update workflow progress in state directory.

    Updates the workflow.json file with new progress information.
    Creates the file if it doesn't exist.

    Args:
        step: Current step number (1-7 for workflow steps).
        artifact: Path to artifact created in this step.
        feature_branch: Name of the feature branch.
        session_id: Session identifier.
        **kwargs: Additional fields to store in progress.

    Returns:
        Updated progress dictionary.
    """
    progress = get_workflow_progress()

    # Update current step
    if step is not None:
        progress["current_step"] = step
        if step not in progress["steps_completed"]:
            progress["steps_completed"].append(step)
            progress["steps_completed"].sort()

    # Add artifact if provided
    if artifact is not None:
        progress.setdefault("artifacts", {})
        if step is not None:
            progress["artifacts"][f"step_{step}"] = artifact
        else:
            # Use timestamp if no step provided
            progress["artifacts"][f"artifact_{len(progress['artifacts'])}"] = artifact

    # Update optional fields
    if feature_branch is not None:
        progress["feature_branch"] = feature_branch

    if session_id is not None:
        progress["session_id"] = session_id

    # Add any additional kwargs
    for key, value in kwargs.items():
        progress[key] = value

    # Update timestamp
    progress["last_updated"] = datetime.now(UTC).isoformat()

    # Ensure worktree_id is set
    progress["worktree_id"] = get_worktree_id()

    # Write to file atomically (write to temp, then rename)
    state_dir = get_state_dir()
    progress_file = state_dir / "workflow.json"

    # Create temp file in same directory to ensure atomic rename
    fd, temp_path = tempfile.mkstemp(dir=state_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(progress, f, indent=2)
        # Atomic rename (works on POSIX systems)
        os.replace(temp_path, progress_file)
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise

    return progress


def clear_workflow_progress() -> None:
    """Clear workflow progress (reset to default state).

    Removes the workflow.json file from the state directory.
    """
    state_dir = get_state_dir()
    progress_file = state_dir / "workflow.json"

    if progress_file.exists():
        progress_file.unlink()


def is_step_completed(step: int) -> bool:
    """Check if a workflow step has been completed.

    Args:
        step: Step number to check.

    Returns:
        True if step is in completed steps list.
    """
    progress = get_workflow_progress()
    return step in progress.get("steps_completed", [])


if __name__ == "__main__":
    # Quick test when run directly
    print("Current progress:")
    progress = get_workflow_progress()
    print(json.dumps(progress, indent=2))

    print("\nUpdating progress to step 1...")
    progress = update_workflow_progress(step=1, artifact="specs/test/spec.md")
    print(json.dumps(progress, indent=2))
