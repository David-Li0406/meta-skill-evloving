#!/usr/bin/env python3
"""
hive-dispatch - SSH dispatch to Claude Code on remote VMs.

Usage:
    python dispatch.py <issue_id>         # Dispatch specific task
    python dispatch.py --all              # Dispatch all hive-ready tasks
    python dispatch.py <issue_id> --dry-run  # Preview without executing

Environment:
    HIVE_VMS: Comma-separated VM hostnames (default: runner1)
    HIVE_MAX_CONCURRENT: Max concurrent tasks (default: 2)
    HIVE_REPO_PATH: Repo path on VM (default: ~/affordabot)
"""

import subprocess
import json
import sys
import os
import argparse
import shlex
from pathlib import Path
from typing import List, Dict, Optional

# Configuration
VMS = os.environ.get("HIVE_VMS", "runner1").split(",")
MAX_CONCURRENT = int(os.environ.get("HIVE_MAX_CONCURRENT", "2"))
REPO_PATH = os.environ.get("HIVE_REPO_PATH", "~/affordabot")
HIVE_LABEL = "hive-ready"


def find_beads_file() -> Optional[Path]:
    """Find .beads/issues.jsonl in current or parent directories."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        beads = parent / ".beads" / "issues.jsonl"
        if beads.exists():
            return beads
    return None


def load_beads() -> List[Dict]:
    """Load all issues from Beads."""
    beads_file = find_beads_file()
    if not beads_file:
        print("❌ No .beads/issues.jsonl found")
        return []

    issues = []
    with open(beads_file) as f:
        for line in f:
            if line.strip():
                try:
                    issues.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return issues


def count_running() -> int:
    """Count tasks currently in_progress with hive-ready label."""
    return sum(
        1
        for i in load_beads()
        if i.get("status") == "in_progress" and HIVE_LABEL in i.get("labels", [])
    )


def vm_is_busy(vm: str) -> bool:
    """Check if Claude is already running on VM via SSH."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", vm, "pgrep -c claude || echo 0"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        count = int(result.stdout.strip())
        return count > 0
    except (subprocess.TimeoutExpired, ValueError, subprocess.CalledProcessError) as e:
        print(f"⚠️ Could not check {vm}: {e.__class__.__name__}")
        # If we can't check, assume NOT busy to avoid false negatives
        return False


def get_available_vm() -> Optional[str]:
    """Find first available VM."""
    for vm in VMS:
        if not vm_is_busy(vm):
            return vm
    return None


def get_issue(issue_id: str) -> Optional[Dict]:
    """Get issue details from Beads."""
    try:
        result = subprocess.run(
            ["bd", "show", issue_id, "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        # bd show --json returns a list, get first item
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return data
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"❌ Failed to get issue {issue_id}: {e}")
        return None


def build_prompt(issue: Dict) -> str:
    """Build the prompt for Claude Code."""
    issue_id = issue.get("id", "unknown")
    title = issue.get("title", "Untitled")
    description = issue.get("description", "")
    design = issue.get("design", "")

    return f"""TASK: {title} ({issue_id})

DESCRIPTION:
{description}

{f"DESIGN SPEC:{chr(10)}{design}" if design else ""}

INSTRUCTIONS:
1. Checkout feature branch: git checkout -b feature-{issue_id}
2. Implement the task per description above
3. Run tests: make ci-lite (if available)
4. Commit with trailer: Feature-Key: {issue_id}
5. Push and create PR: git push -u origin feature-{issue_id} && gh pr create

When complete, the PR is your deliverable.
"""


def dispatch(issue_id: str, dry_run: bool = False) -> bool:
    """Dispatch a single task to an available VM."""

    # Layer 1: Queue check
    running = count_running()
    if running >= MAX_CONCURRENT:
        print(f"⏳ Queue full ({running}/{MAX_CONCURRENT} running)")
        return False

    # Get issue details
    issue = get_issue(issue_id)
    if not issue:
        return False

    # Find available VM
    vm = get_available_vm()
    if not vm:
        print("⏳ No VMs available")
        return False

    # Layer 2: SSH pre-check (defense in depth)
    if vm_is_busy(vm):
        print(f"⚠️ {vm} busy (race condition avoided)")
        return False

    # Build prompt
    prompt = build_prompt(issue)
    safe_prompt = shlex.quote(prompt)

    # Remote command - source zshrc for mise PATH
    remote_cmd = f"source ~/.zshrc && cd {REPO_PATH} && claude --dangerously-skip-permissions -p {safe_prompt}"

    if dry_run:
        print(f"[DRY RUN] Would execute:")
        print(f'  ssh {vm} "{remote_cmd[:80]}..."')
        print(f"  Prompt length: {len(prompt)} chars")
        return True

    # Mark in_progress BEFORE dispatch
    try:
        subprocess.run(
            ["bd", "update", issue_id, "--status", "in_progress"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update status: {e}")
        return False

    # Dispatch via SSH (background)
    try:
        subprocess.Popen(
            ["ssh", vm, remote_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"🚀 Dispatched {issue_id} → {vm}")
        return True
    except Exception as e:
        print(f"❌ Failed to dispatch: {e}")
        # Rollback status
        subprocess.run(
            ["bd", "update", issue_id, "--status", "open"], capture_output=True
        )
        return False


def dispatch_all(dry_run: bool = False) -> int:
    """Dispatch all hive-ready tasks up to MAX_CONCURRENT."""
    dispatched = 0
    for issue in load_beads():
        if HIVE_LABEL in issue.get("labels", []) and issue.get("status") == "open":
            if dispatch(issue["id"], dry_run):
                dispatched += 1
            if count_running() >= MAX_CONCURRENT:
                break
    return dispatched


def main():
    parser = argparse.ArgumentParser(description="Dispatch Beads tasks to VMs")
    parser.add_argument("issue", nargs="?", help="Beads issue ID (e.g., bd-xyz)")
    parser.add_argument(
        "--all", action="store_true", help="Dispatch all hive-ready tasks"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without executing"
    )
    parser.add_argument(
        "--status", action="store_true", help="Show current queue status"
    )

    args = parser.parse_args()

    if args.status:
        running = count_running()
        print(f"Queue: {running}/{MAX_CONCURRENT} running")
        print(f"VMs: {', '.join(VMS)}")
        for vm in VMS:
            busy = "🔴 busy" if vm_is_busy(vm) else "🟢 available"
            print(f"  {vm}: {busy}")
        return

    if args.all:
        dispatched = dispatch_all(args.dry_run)
        print(f"Dispatched {dispatched} tasks")
    elif args.issue:
        dispatch(args.issue, args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
