#!/usr/bin/env python3
"""Create release branch from base branch with TODO file generation.

This script implements Step 5.1 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It creates a release branch following git-flow conventions,
validates the version, and generates a TODO file for tracking release tasks.

Usage:
    python create_release.py <version> <base_branch> [--yes]

Example:
    python create_release.py v1.1.0 develop
    python create_release.py v1.1.0 develop --yes  # Skip confirmation prompts

Requirements:
    - Clean working directory (no uncommitted changes)
    - Base branch must exist
    - Version must follow semantic versioning (vX.Y.Z)
    - Version tag must not already exist
"""

import argparse
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))
from vcs import get_vcs_adapter

# Constants with documented rationale
RELEASE_BRANCH_PREFIX = "release/"
# Rationale: git-flow release branch naming convention for clarity and tooling compatibility

VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"
# Rationale: Enforce semantic versioning (vMAJOR.MINOR.PATCH) for consistency

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"
# Rationale: Compact ISO8601 format that remains intact when parsed by underscores/hyphens


def validate_version_format(version):
    """
    Validate version follows semantic versioning pattern.

    Args:
        version: Version string to validate (e.g., 'v1.1.0')

    Raises:
        ValueError: If version doesn't match vX.Y.Z pattern
    """
    if not re.match(VERSION_PATTERN, version):
        raise ValueError(f"Invalid version format '{version}'. Must match pattern vX.Y.Z (e.g., v1.1.0, v2.0.0)")


def check_working_directory_clean():
    """
    Verify working directory has no uncommitted changes.

    Raises:
        RuntimeError: If working directory has uncommitted changes
    """
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            raise RuntimeError("Working directory has uncommitted changes. Please commit or stash changes before creating release branch.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git status: {e.stderr.strip()}") from e


def verify_branch_exists(branch_name):
    """
    Verify that a git branch exists.

    Args:
        branch_name: Name of branch to verify

    Raises:
        ValueError: If branch doesn't exist
    """
    try:
        subprocess.run(["git", "rev-parse", "--verify", branch_name], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        raise ValueError(f"Base branch '{branch_name}' does not exist. Use 'git branch -a' to list available branches.")


def verify_tag_not_exists(version):
    """
    Verify that a version tag doesn't already exist.

    Args:
        version: Version tag to check (e.g., 'v1.1.0')

    Raises:
        ValueError: If tag already exists
    """
    try:
        result = subprocess.run(["git", "tag", "-l", version], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            raise ValueError(f"Tag '{version}' already exists. Use 'git tag -l' to list existing tags.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git tags: {e.stderr.strip()}") from e


def get_semantic_version_recommendation(base_branch):
    """
    Get recommended version from semantic_version.py.

    Args:
        base_branch: Branch to analyze for changes

    Returns:
        Recommended version string (e.g., 'v1.1.0'), or None if script unavailable
    """
    script_path = Path(__file__).parent / "semantic_version.py"

    if not script_path.exists():
        print(f"Warning: semantic_version.py not found at {script_path}", file=sys.stderr)
        return None

    try:
        # Get latest tag to determine current version
        result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True, check=False)

        current_version = result.stdout.strip() if result.returncode == 0 else "v1.0.0"

        # Call semantic_version.py to get recommendation
        result = subprocess.run(["python3", str(script_path), base_branch, current_version], capture_output=True, text=True, check=True)

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to get semantic version recommendation: {e.stderr.strip()}", file=sys.stderr)
        return None


def confirm_version_mismatch(provided_version, recommended_version, auto_confirm=False):
    """
    Prompt user to confirm if provided version differs from recommendation.

    Args:
        provided_version: Version provided by user
        recommended_version: Version recommended by semantic_version.py
        auto_confirm: If True, skip confirmation prompt (for --yes flag)

    Returns:
        True if user confirms or auto_confirm is True, False otherwise
    """
    if provided_version == recommended_version:
        return True

    if auto_confirm:
        print(f"⚠️  Version mismatch: provided {provided_version}, recommended {recommended_version}", file=sys.stderr)
        print(f"Continuing with {provided_version} (--yes flag enabled)", file=sys.stderr)
        return True

    print("\n⚠️  Version Mismatch Warning", file=sys.stderr)
    print(f"Provided version:    {provided_version}", file=sys.stderr)
    print(f"Recommended version: {recommended_version}", file=sys.stderr)
    print(f"\nSemantic versioning suggests {recommended_version} based on changes.", file=sys.stderr)
    print(f"Do you want to continue with {provided_version}? (Y/n): ", end="", file=sys.stderr)

    response = input().strip().lower()
    return response in ["y", "yes", ""]


def create_release_branch(version, base_branch):
    """
    Create release branch from base branch.

    Args:
        version: Release version (e.g., 'v1.1.0')
        base_branch: Branch to create release from (e.g., 'develop')

    Returns:
        Tuple of (branch_name, base_commit_sha)

    Raises:
        RuntimeError: If branch creation fails
    """
    branch_name = f"{RELEASE_BRANCH_PREFIX}{version}"

    try:
        # Get base commit SHA for reporting
        result = subprocess.run(["git", "rev-parse", "--short", base_branch], capture_output=True, text=True, check=True)
        base_commit = result.stdout.strip()

        # Create branch
        subprocess.run(["git", "checkout", "-b", branch_name, base_branch], capture_output=True, check=True)

        # Push to origin
        subprocess.run(["git", "push", "-u", "origin", branch_name], capture_output=True, check=True)

        return branch_name, base_commit

    except subprocess.CalledProcessError as e:
        # Cleanup on failure
        print("ERROR: Failed to create release branch", file=sys.stderr)
        print("Cleaning up...", file=sys.stderr)

        # Try to delete local branch if it was created
        subprocess.run(["git", "branch", "-D", branch_name], capture_output=True, check=False)

        # Try to return to base branch
        subprocess.run(["git", "checkout", base_branch], capture_output=True, check=False)

        raise RuntimeError(f"Failed to create release branch: {e.stderr.decode() if e.stderr else 'Unknown error'}") from e


def create_todo_file(version, base_branch, base_commit):
    """
    Create TODO file for release workflow tracking.

    Args:
        version: Release version (e.g., 'v1.1.0')
        base_branch: Base branch name (e.g., 'develop')
        base_commit: Base commit SHA

    Returns:
        Path to created TODO file

    Raises:
        RuntimeError: If TODO file creation fails
    """
    timestamp = datetime.now(UTC).strftime(TIMESTAMP_FORMAT)
    version_slug = version.replace(".", "-")
    todo_filename = f"TODO_release_{timestamp}_{version_slug}.md"

    repo_root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

    todo_path = repo_root / todo_filename

    # Get VCS user (GitHub/Azure DevOps)
    # Gracefully handle VCS adapter failures - user info is non-critical for release creation
    try:
        vcs = get_vcs_adapter()
        github_user = vcs.get_current_user()
    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError):
        # VCS CLI not available or not authenticated - use fallback
        github_user = "unknown"

    # Create TODO content
    created_timestamp = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    todo_content = f"""---
type: workflow-manifest
workflow_type: release
slug: {version_slug}
timestamp: {timestamp}
github_user: {github_user}

metadata:
  title: "Release {version}"
  description: "Release workflow for version {version} from {base_branch}"
  created: "{created_timestamp}"
  base_branch: "{base_branch}"
  base_commit: "{base_commit}"
  stack: python
  package_manager: uv
  test_framework: pytest
  containers: []

workflow_progress:
  phase: 5
  current_step: "5.2"
  last_task: null
  last_update: "{created_timestamp}"
  status: "qa"

quality_gates:
  test_coverage: 80
  tests_passing: false
  build_successful: false
  linting_clean: false
  types_clean: false
  semantic_version: "{version}"

tasks:
  qa:
    - id: qa_001
      description: "Run full test suite with coverage"
      status: pending
      files: []
      dependencies: []
    - id: qa_002
      description: "Verify all quality gates pass"
      status: pending
      files: []
      dependencies: [qa_001]
    - id: qa_003
      description: "Update documentation (README, CHANGELOG)"
      status: pending
      files:
        - README.md
        - CHANGELOG.md
      dependencies: []
    - id: qa_004
      description: "Update version in pyproject.toml"
      status: pending
      files:
        - pyproject.toml
      dependencies: []

  integration:
    - id: int_001
      description: "Create PR: release/{version} → main"
      status: pending
      files: []
      dependencies: [qa_001, qa_002, qa_003, qa_004]
    - id: int_002
      description: "User merges PR in GitHub UI"
      status: pending
      files: []
      dependencies: [int_001]
    - id: int_003
      description: "Tag release on main"
      status: pending
      files: []
      dependencies: [int_002]
    - id: int_004
      description: "Back-merge release to develop"
      status: pending
      files: []
      dependencies: [int_003]
    - id: int_005
      description: "Cleanup release branch"
      status: pending
      files: []
      dependencies: [int_004]
---

# TODO: Release {version}

**Type:** release
**Slug:** {version_slug}
**Created:** {created_timestamp}
**Base Branch:** {base_branch}
**Base Commit:** {base_commit}
**GitHub User:** {github_user}

## Overview

Release workflow for version {version} created from {base_branch} branch.

## Current Status

**Phase:** Release Workflow (5)
**Current Step:** 5.2 - Quality Assurance
**Last Updated:** {created_timestamp}

## Release Tasks

### Phase 5.2: Quality Assurance

- [ ] **qa_001**: Run full test suite with coverage
  - Command: `uv run pytest --cov=src --cov-report=term --cov-fail-under=80`

- [ ] **qa_002**: Verify all quality gates pass
  - Test coverage ≥ 80%
  - All tests passing
  - Build successful
  - Linting clean (ruff)
  - Type checking clean (mypy)

- [ ] **qa_003**: Update documentation (README, CHANGELOG)
  - Document new features and changes
  - Update version numbers

- [ ] **qa_004**: Update version in pyproject.toml
  - Set version to {version}

### Phase 5.3-5.7: Integration and Cleanup

- [ ] **int_001**: Create PR: release/{version} → main
  - Command: `gh pr create --base main --title "Release {version}"`

- [ ] **int_002**: User merges PR in GitHub UI
  - Manual step: Review and merge in GitHub

- [ ] **int_003**: Tag release on main
  - Command: `python .claude/skills/git-workflow-manager/scripts/tag_release.py {version} main`

- [ ] **int_004**: Back-merge release to develop
  - Command: `python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop`

- [ ] **int_005**: Cleanup release branch
  - Command: `python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}`

## Quality Gates

- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Build successful
- [ ] Linting clean (ruff)
- [ ] Type checking clean (mypy)
- [ ] Containers healthy (if applicable)

## Workflow Commands

```bash
# Update task status
python .claude/skills/workflow-utilities/scripts/todo_updater.py {todo_filename} <task_id> <status>

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Create PR to main
gh pr create --base main --title "Release {version}" --body "Release {version} from {base_branch}"

# Tag release (after merge)
python .claude/skills/git-workflow-manager/scripts/tag_release.py {version} main

# Back-merge to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop

# Cleanup release branch
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}
```

## Status History

- {created_timestamp}: Release branch created from {base_branch} ({base_commit})
"""

    try:
        todo_path.write_text(todo_content)
        return todo_path

    except Exception as e:
        raise RuntimeError(f"Failed to create TODO file at {todo_path}: {e}") from e


def main():
    """Main entry point for create_release.py script."""
    parser = argparse.ArgumentParser(
        description="Create release branch from base branch with TODO file generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s v1.1.0 develop
  %(prog)s v1.1.0 develop --yes

For more information, see WORKFLOW.md Phase 5 (Release Workflow).
        """,
    )
    parser.add_argument("version", help="Release version (e.g., v1.1.0)")
    parser.add_argument("base_branch", help="Base branch to create release from (e.g., develop)")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompts (non-interactive mode)")

    args = parser.parse_args()
    version = args.version
    base_branch = args.base_branch
    auto_confirm = args.yes

    try:
        # Step 1: Input Validation
        print("Validating inputs...", file=sys.stderr)
        validate_version_format(version)
        verify_branch_exists(base_branch)
        check_working_directory_clean()
        verify_tag_not_exists(version)

        # Step 2: Version Verification
        print("Checking semantic version recommendation...", file=sys.stderr)
        recommended_version = get_semantic_version_recommendation(base_branch)

        if recommended_version and recommended_version != version:
            if not confirm_version_mismatch(version, recommended_version, auto_confirm):
                print("Release creation cancelled by user.", file=sys.stderr)
                sys.exit(1)

        # Step 3: Create Release Branch
        print("Creating release branch...", file=sys.stderr)
        branch_name, base_commit = create_release_branch(version, base_branch)

        # Step 4: Create TODO File
        print("Creating TODO file...", file=sys.stderr)
        todo_path = create_todo_file(version, base_branch, base_commit)

        # Success output
        print(f"\n✓ Created release branch: {branch_name}")
        print(f"✓ Base: {base_branch} (commit {base_commit})")
        print(f"✓ TODO file: {todo_path.name}")
        print("✓ Ready for final QA and documentation updates")
        print("\nNext steps:")
        print("  1. Run quality gates: python .claude/skills/quality-enforcer/scripts/run_quality_gates.py")
        print("  2. Update documentation and version in pyproject.toml")
        print(f"  3. Create PR to main: gh pr create --base main --title 'Release {version}'")

    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nRelease creation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
