#!/usr/bin/env python3
"""
Branch analysis script for clean-branches skill.
Analyzes git branches and generates a cleanup report.
"""

import subprocess
import sys
from dataclasses import dataclass


@dataclass
class BranchInfo:
    name: str
    is_local: bool
    is_remote: bool
    last_commit_hash: str
    last_commit_msg: str
    last_commit_age: str
    contained_in: list[str]
    is_archived: bool
    namespace: str  # 'archive/completed', 'archive/stopped', 'wip', 'feature', or ''


def run_git(args: list[str], check: bool = True) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout.strip()


def get_default_branch() -> str:
    """Get the default branch name."""
    try:
        # Try gh first
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to git remote show
        output = run_git(["remote", "show", "origin"])
        for line in output.splitlines():
            if "HEAD branch:" in line:
                return line.split(":")[-1].strip()
    return "main"


def get_local_branches() -> list[str]:
    """Get list of local branch names."""
    output = run_git(["branch", "--list", "--format=%(refname:short)"])
    return [b for b in output.splitlines() if b]


def get_remote_branches() -> list[str]:
    """Get list of remote branch names (without origin/ prefix)."""
    output = run_git(["branch", "-r", "--format=%(refname:short)"])
    branches = []
    for b in output.splitlines():
        if b and not b.endswith("/HEAD"):
            # Remove 'origin/' prefix
            if b.startswith("origin/"):
                branches.append(b[7:])
    return branches


def get_current_branch() -> str:
    """Get the current branch name."""
    return run_git(["branch", "--show-current"])


def get_commit_info(ref: str) -> tuple[str, str, str]:
    """Get (hash, message, age) for a ref."""
    try:
        output = run_git(["log", "-1", "--format=%h|%s|%cr", ref])
        parts = output.split("|", 2)
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
    except subprocess.CalledProcessError:
        pass
    return "", "", ""


def is_ancestor(branch: str, target: str) -> bool:
    """Check if branch is an ancestor of (contained in) target."""
    try:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", branch, target],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_namespace(branch: str) -> str:
    """Extract namespace from branch name."""
    if branch.startswith("archive/completed/"):
        return "archive/completed"
    if branch.startswith("archive/stopped/"):
        return "archive/stopped"
    if branch.startswith("archive/"):
        return "archive"
    if branch.startswith("wip/"):
        return "wip"
    if branch.startswith("feature/"):
        return "feature"
    return ""


def find_contained_in(branch: str, ref: str, all_branches: list[str], default_branch: str) -> list[str]:
    """Find which branches contain this branch."""
    contained = []

    # Check default branch first
    if is_ancestor(ref, default_branch):
        contained.append(default_branch)

    # Check other important branches
    for target in all_branches:
        if target == branch:
            continue
        if target == default_branch:
            continue
        # Check archived branches
        if target.startswith("archive/"):
            target_ref = f"origin/{target}"
            if is_ancestor(ref, target_ref):
                contained.append(target)

    return contained


def analyze_branches() -> dict:
    """Analyze all branches and return report data."""
    print("Fetching branches...", file=sys.stderr)
    run_git(["fetch", "--all", "--prune"])

    default_branch = get_default_branch()
    current_branch = get_current_branch()
    local_branches = get_local_branches()
    remote_branches = get_remote_branches()

    all_branch_names = set(local_branches) | set(remote_branches)

    branches: list[BranchInfo] = []

    print(f"Analyzing {len(all_branch_names)} branches...", file=sys.stderr)

    for name in sorted(all_branch_names):
        is_local = name in local_branches
        is_remote = name in remote_branches
        namespace = get_namespace(name)
        is_archived = namespace.startswith("archive")

        # Get ref to use for analysis
        if is_local:
            ref = name
        else:
            ref = f"origin/{name}"

        commit_hash, commit_msg, commit_age = get_commit_info(ref)

        # Only check containment for non-archived branches
        if is_archived:
            contained_in = []
        else:
            contained_in = find_contained_in(name, ref, remote_branches, default_branch)

        branches.append(BranchInfo(
            name=name,
            is_local=is_local,
            is_remote=is_remote,
            last_commit_hash=commit_hash,
            last_commit_msg=commit_msg[:50] + "..." if len(commit_msg) > 50 else commit_msg,
            last_commit_age=commit_age,
            contained_in=contained_in,
            is_archived=is_archived,
            namespace=namespace,
        ))

    return {
        "default_branch": default_branch,
        "current_branch": current_branch,
        "branches": branches,
    }


def print_report(data: dict) -> None:
    """Print the branch analysis report."""
    default_branch = data["default_branch"]
    current_branch = data["current_branch"]
    branches = data["branches"]

    print(f"\n## Branch Analysis Report\n")
    print(f"**Default branch:** `{default_branch}`")
    print(f"**Current branch:** `{current_branch}`")

    # Separate by category
    active = [b for b in branches if not b.is_archived and b.namespace not in ("wip",)]
    wip = [b for b in branches if b.namespace == "wip"]
    archived = [b for b in branches if b.is_archived]

    # Active branches
    print(f"\n### Active Branches ({len(active)})\n")
    if active:
        print("| Branch | Local | Remote | Last Commit | Age | Contained In | Action |")
        print("|--------|-------|--------|-------------|-----|--------------|--------|")
        for b in active:
            local = "Yes" if b.is_local else "No"
            remote = "Yes" if b.is_remote else "No"
            contained = ", ".join(b.contained_in) if b.contained_in else "-"

            # Determine recommended action
            # Standard branches that should always be kept
            standard_branches = {"main", "master", "develop", "dev"}

            if b.name == default_branch:
                action = "Keep (default)"
            elif b.name == current_branch:
                action = "Keep (current)"
            elif b.name in standard_branches:
                action = "Keep (standard)"
            elif b.contained_in:
                if b.is_local and not b.is_remote:
                    action = "Delete local (in " + b.contained_in[0] + ")"
                else:
                    action = "Archive? (in " + b.contained_in[0] + ")"
            else:
                action = "Review"

            print(f"| `{b.name}` | {local} | {remote} | {b.last_commit_hash} {b.last_commit_msg} | {b.last_commit_age} | {contained} | {action} |")
    else:
        print("*No active branches*")

    # WIP branches
    print(f"\n### Work in Progress ({len(wip)})\n")
    if wip:
        print("| Branch | Last Commit | Age | Contained In | Action |")
        print("|--------|-------------|-----|--------------|--------|")
        for b in wip:
            contained = ", ".join(b.contained_in) if b.contained_in else "-"
            if default_branch in b.contained_in:
                action = f"-> archive/completed (merged to {default_branch})"
            elif b.contained_in:
                action = f"Review (in {b.contained_in[0]})"
            else:
                action = "Keep (active)"
            print(f"| `{b.name}` | {b.last_commit_hash} {b.last_commit_msg} | {b.last_commit_age} | {contained} | {action} |")
    else:
        print("*No WIP branches*")

    # Archived summary
    print(f"\n### Archived ({len(archived)})\n")
    completed = [b for b in archived if b.namespace == "archive/completed"]
    stopped = [b for b in archived if b.namespace == "archive/stopped"]
    other = [b for b in archived if b.namespace == "archive"]

    print(f"- **Completed:** {len(completed)}")
    print(f"- **Stopped:** {len(stopped)}")
    print(f"- **Other:** {len(other)}")

    # Recommendations
    standard_branches = {"main", "master", "develop", "dev"}
    needs_action = [b for b in active if b.name not in (default_branch, current_branch) and b.name not in standard_branches]

    # WIP branches that are merged to default branch need action
    wip_needs_action = [b for b in wip if default_branch in b.contained_in]

    if needs_action or wip_needs_action:
        print(f"\n### Recommendations\n")

        # WIP branches merged to default
        for b in wip_needs_action:
            short_name = b.name.replace("wip/", "")
            print(f"- `{b.name}`: **Merged to {default_branch}** -> move to `archive/completed/{short_name}`")

        # Active branches
        for b in needs_action:
            if b.contained_in:
                if b.is_local and not b.is_remote:
                    print(f"- `{b.name}`: Local-only, already in `{b.contained_in[0]}` - **safe to delete**")
                elif not b.is_local and b.is_remote:
                    print(f"- `{b.name}`: Remote-only, in `{b.contained_in[0]}` - consider archiving")
            else:
                if b.is_local and not b.is_remote:
                    print(f"- `{b.name}`: Local-only, **not merged** - review before deleting")
                else:
                    print(f"- `{b.name}`: Not merged - keep, move to wip/, or archive")


def main() -> None:
    data = analyze_branches()
    print_report(data)


if __name__ == "__main__":
    main()
