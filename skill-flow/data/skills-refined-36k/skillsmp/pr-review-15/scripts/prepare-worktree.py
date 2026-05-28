#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "GitPython>=3.1.0",
# ]
# ///
"""
Prepare a git worktree for reviewing a GitHub PR.

Creates a worktree in git-worktrees/<branch-name> and checks out the PR branch.
Also creates a review-notes/<branch-name> directory for storing review notes.
This keeps the main repository clean and allows reviewing multiple PRs simultaneously.

Usage:
    ./prepare-worktree.py <REPO_PATH> <PR_NUMBER>

Example:
    ./prepare-worktree.py /path/to/repo 744

Returns:
    Prints the path to the worktree directory on success.
"""

import os
import subprocess
import sys
from pathlib import Path
from git import Repo
from git.exc import GitCommandError


def get_pr_info(repo_path: str, pr_number: int) -> dict:
    """Get PR information using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--json", "headRefName,headRefOid"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        import json
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to get PR information: {e.stderr}")


def get_repo_info(repo_path: str) -> tuple[str, str]:
    """Get the owner and name of the current repository using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        import json
        repo_info = json.loads(result.stdout)
        return repo_info["owner"]["login"], repo_info["name"]
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to get repository information: {e.stderr}")


def find_remote_for_repo(repo: Repo, owner: str, repo_name: str) -> str:
    """Find the remote that points to the specified repository."""
    for remote in repo.remotes:
        # Get remote URL
        url = remote.url
        # Check if this remote points to the target repository
        # Handle both SSH and HTTPS URLs
        if f"{owner}/{repo_name}" in url or f":{owner}/{repo_name}" in url:
            return remote.name
    raise ValueError(f"No remote found for {owner}/{repo_name}")


def prepare_worktree(repo_path: str, pr_number: int) -> str:
    """
    Prepare a git worktree for reviewing a PR.

    Args:
        repo_path: Path to the git repository
        pr_number: PR number to review

    Returns:
        Path to the worktree directory
    """
    repo_path = Path(repo_path).resolve()

    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    # Open the repository
    try:
        repo = Repo(repo_path)
    except Exception as e:
        raise ValueError(f"Not a valid git repository: {repo_path}") from e

    # Get PR information
    pr_info = get_pr_info(str(repo_path), pr_number)
    branch_name = pr_info["headRefName"]
    head_sha = pr_info["headRefOid"]

    # Get the base repository information (where the PR is targeting)
    repo_owner, repo_name = get_repo_info(str(repo_path))

    # Find the correct remote for the base repository
    remote_name = find_remote_for_repo(repo, repo_owner, repo_name)

    # Create git-worktrees directory if it doesn't exist
    worktrees_dir = repo_path / "git-worktrees"
    worktrees_dir.mkdir(exist_ok=True)

    # Create review-notes directory if it doesn't exist
    review_notes_dir = repo_path / "review-notes"
    review_notes_dir.mkdir(exist_ok=True)

    # Worktree path
    worktree_path = worktrees_dir / branch_name

    # Review notes path for this PR
    review_notes_path = review_notes_dir / branch_name
    review_notes_path.mkdir(exist_ok=True)

    # Create README.md template in review-notes if it doesn't exist
    readme_path = review_notes_path / "README.md"
    if not readme_path.exists():
        readme_template = f"""# PR #{pr_number} Review Notes

## PR Information
- **Branch**: `{branch_name}`
- **Worktree**: `{worktree_path}`
- **Review Started**: {subprocess.run(['date', '+%Y-%m-%d %H:%M:%S'], capture_output=True, text=True).stdout.strip()}

## Review Progress

### 1. PR Summary Analysis
- [ ] Reviewed PR description and metadata
- [ ] Reviewed file changes
- [ ] Reviewed discussion timeline
- [ ] Identified unresolved comments

**Notes:**


### 2. Context Gathering
- [ ] Identified related files and dependencies
- [ ] Reviewed test coverage
- [ ] Checked documentation updates
- [ ] Reviewed architecture alignment

**Notes:**


### 3. Code Review
- [ ] Reviewed all changed files
- [ ] Checked for correctness and logic issues
- [ ] Verified error handling
- [ ] Assessed performance implications
- [ ] Checked security concerns

**Notes:**


### 4. Issues Found

#### Unresolved Comments (from PR)


#### New Issues Found


### 5. Final Recommendation

**Status**: [ ] Approve [ ] Request Changes [ ] Comment

**Summary:**


**Action Items:**

"""
        readme_path.write_text(readme_template)
        print(f"Created review notes at: {review_notes_path}/README.md", file=sys.stderr)

    # Check if worktree already exists
    if worktree_path.exists():
        print(f"Worktree already exists at: {worktree_path}", file=sys.stderr)

        # Check if the worktree is dirty (has uncommitted changes)
        try:
            worktree_repo = Repo(worktree_path)
            if worktree_repo.is_dirty(untracked_files=True):
                raise ValueError(
                    f"Worktree at {worktree_path} has uncommitted changes. "
                    f"Please commit or discard changes before recreating the worktree."
                )
        except Exception as e:
            if "uncommitted changes" in str(e):
                raise
            # If we can't check dirty status, continue with warning
            print(f"Warning: Could not check if worktree is dirty: {e}", file=sys.stderr)

        print(f"Removing and recreating...", file=sys.stderr)

        # Remove the worktree
        try:
            repo.git.worktree("remove", str(worktree_path), "--force")
        except GitCommandError:
            # If git worktree remove fails, try manual cleanup
            import shutil
            shutil.rmtree(worktree_path)
            # Prune worktree references
            repo.git.worktree("prune")

    # Fetch the PR ref without checking it out in the main repo
    # This preserves the main repo's current state
    try:
        # First, ensure the local branch doesn't already exist
        try:
            repo.git.branch("-D", branch_name)
            print(f"Deleted existing local branch: {branch_name}", file=sys.stderr)
        except GitCommandError:
            # Branch doesn't exist, which is fine
            pass

        # Fetch the PR ref from GitHub
        # This works for both same-repo and cross-repo (fork) PRs
        # GitHub exposes all PRs via refs/pull/{number}/head
        repo.git.fetch(remote_name, f"pull/{pr_number}/head:{branch_name}")
        print(f"Created local branch {branch_name} at {head_sha[:8]}", file=sys.stderr)

    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to fetch PR: {e.stderr}")
    except Exception as e:
        raise ValueError(f"Failed to create branch: {e}")

    # Create the worktree
    try:
        repo.git.worktree("add", str(worktree_path), branch_name)
    except GitCommandError as e:
        raise ValueError(f"Failed to create worktree: {e}")

    return str(worktree_path)


def main():
    if len(sys.argv) != 3:
        print("Usage: prepare-worktree.py <REPO_PATH> <PR_NUMBER>", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]
    pr_number = int(sys.argv[2])

    try:
        worktree_path = prepare_worktree(repo_path, pr_number)
        print(worktree_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
