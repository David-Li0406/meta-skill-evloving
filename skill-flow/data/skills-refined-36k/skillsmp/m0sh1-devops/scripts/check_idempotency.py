#!/usr/bin/env python3
"""
Check Ansible playbooks for common idempotency issues.

Detects:
- Command/shell tasks without changed_when
- Shell tasks without set -euo pipefail
- Tasks without no_log that may contain secrets
- Tasks missing name attribute
- Use of deprecated short module names

Usage:
    ./check_idempotency.py playbook.yml
    ./check_idempotency.py playbooks/*.yml
    ./check_idempotency.py --strict playbook.yml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required: python -m pip install pyyaml", file=sys.stderr)
    sys.exit(1)


class IdempotencyChecker:
    """Check Ansible playbooks for idempotency issues."""

    # Modules that should have changed_when
    COMMAND_MODULES = [
        "command",
        "shell",
        "ansible.builtin.command",
        "ansible.builtin.shell",
    ]

    # Modules that handle secrets
    SECRET_MODULES = [
        "user",
        "ansible.builtin.user",
        "mysql_user",
        "community.mysql.mysql_user",
        "postgresql_user",
        "community.postgresql.postgresql_user",
    ]

    # Keywords that suggest secrets
    SECRET_KEYWORDS = ["password", "token", "secret", "key", "credential", "api_key"]

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.issues: List[dict] = []

    def check_playbook(self, playbook_path: Path) -> List[dict]:
        """Check a playbook file for issues."""
        self.issues = []

        try:
            with playbook_path.open("r", encoding="utf-8") as handle:
                content = yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            return [{"severity": "error", "message": f"Failed to parse YAML: {exc}"}]
        except OSError as exc:
            return [{"severity": "error", "message": f"Failed to read file: {exc}"}]

        if not content:
            return []

        # Check each play
        for play_idx, play in enumerate(content):
            if not isinstance(play, dict):
                continue

            # Check tasks
            tasks = play.get("tasks", [])
            self._check_tasks(tasks, f"play[{play_idx}].tasks")

            # Check handlers
            handlers = play.get("handlers", [])
            self._check_tasks(handlers, f"play[{play_idx}].handlers")

            # Check pre_tasks
            pre_tasks = play.get("pre_tasks", [])
            self._check_tasks(pre_tasks, f"play[{play_idx}].pre_tasks")

            # Check post_tasks
            post_tasks = play.get("post_tasks", [])
            self._check_tasks(post_tasks, f"play[{play_idx}].post_tasks")

        return self.issues

    def _check_tasks(self, tasks: list, location: str) -> None:
        """Check a list of tasks."""
        for task_idx, task in enumerate(tasks):
            if not isinstance(task, dict):
                continue

            task_location = f"{location}[{task_idx}]"

            # Check for name
            self._check_task_name(task, task_location)

            # Check for command/shell issues
            self._check_command_shell(task, task_location)

            # Check for secret handling
            self._check_secrets(task, task_location)

            # Check for deprecated short names
            self._check_module_names(task, task_location)

            # Recursively check blocks
            if "block" in task:
                self._check_tasks(task["block"], f"{task_location}.block")
            if "rescue" in task:
                self._check_tasks(task["rescue"], f"{task_location}.rescue")
            if "always" in task:
                self._check_tasks(task["always"], f"{task_location}.always")

    def _check_task_name(self, task: dict, location: str) -> None:
        """Check if task has a name."""
        if "name" not in task and "include_tasks" not in task and "import_tasks" not in task:
            self.issues.append(
                {
                    "severity": "warning",
                    "location": location,
                    "message": "Task missing name attribute",
                    "suggestion": "Add name: field to describe what this task does",
                }
            )

    def _check_command_shell(self, task: dict, location: str) -> None:
        """Check command/shell tasks for idempotency."""
        # Find module name
        module_name = None
        module_args = None

        for key in task:
            if key in self.COMMAND_MODULES:
                module_name = key
                module_args = task[key]
                break

        if not module_name:
            return

        task_name = task.get("name", "unnamed task")

        # Check for changed_when
        if "changed_when" not in task:
            # Allow exception for tasks with register but no changed_when if they're checks
            if "register" in task:
                # If task name suggests it's a check, this might be intentional
                if any(word in task_name.lower() for word in ["check", "verify", "test", "get", "find"]):
                    if self.strict:
                        self.issues.append(
                            {
                                "severity": "info",
                                "location": location,
                                "message": "Command/shell task without changed_when",
                                "suggestion": "Add changed_when: false if this is a read-only check",
                            }
                        )
                else:
                    self.issues.append(
                        {
                            "severity": "warning",
                            "location": location,
                            "message": "Command/shell task without changed_when",
                            "suggestion": "Add changed_when: to control when task reports as changed",
                        }
                    )
            else:
                self.issues.append(
                    {
                        "severity": "warning",
                        "location": location,
                        "message": "Command/shell task without changed_when or register",
                        "suggestion": "Add changed_when: and register: for proper idempotency",
                    }
                )

        # Check shell tasks for set -euo pipefail
        if "shell" in module_name and isinstance(module_args, str):
            if "|" in module_args or ">" in module_args:  # Has pipes or redirects
                if "set -euo pipefail" not in module_args and "set -o pipefail" not in module_args:
                    self.issues.append(
                        {
                            "severity": "warning",
                            "location": location,
                            "message": 'Shell task with pipes missing "set -euo pipefail"',
                            "suggestion": 'Add "set -euo pipefail" at the start of shell script',
                        }
                    )

        # Check if command could be shell (uses pipes, redirects, etc.)
        if "command" in module_name and isinstance(module_args, str):
            if any(char in module_args for char in ["|", ">", "<", "&", ";", "$"]):
                self.issues.append(
                    {
                        "severity": "info",
                        "location": location,
                        "message": "Command module used with shell features",
                        "suggestion": "Consider using shell module instead (requires pipes, redirects, etc.)",
                    }
                )

    def _check_secrets(self, task: dict, location: str) -> None:
        """Check if secrets are handled properly."""
        module_name = None
        for key in task:
            if key in self.SECRET_MODULES:
                module_name = key
                break

        # Check task for secret-related keywords
        task_text = str(task).lower()
        has_secret_keyword = any(keyword in task_text for keyword in self.SECRET_KEYWORDS)

        if module_name or has_secret_keyword:
            if "no_log" not in task:
                self.issues.append(
                    {
                        "severity": "warning",
                        "location": location,
                        "message": "Task may handle secrets without no_log",
                        "suggestion": "Add no_log: true to prevent secret leakage",
                    }
                )

    def _check_module_names(self, task: dict, location: str) -> None:
        """Check for deprecated short module names."""
        for key in task:
            if key in ["command", "shell", "copy", "template", "service", "file"]:
                self.issues.append(
                    {
                        "severity": "info",
                        "location": location,
                        "message": "Short module name used",
                        "suggestion": f"Use ansible.builtin.{key} for clarity",
                    }
                )


def print_issues(playbook_path: Path, issues: List[dict]) -> None:
    """Print issues for a playbook."""
    if not issues:
        return

    print(f"\nPlaybook: {playbook_path}")
    print("=" * 70)

    errors = [i for i in issues if i.get("severity") == "error"]
    warnings = [i for i in issues if i.get("severity") == "warning"]
    info = [i for i in issues if i.get("severity") == "info"]

    for severity, items in [("ERROR", errors), ("WARNING", warnings), ("INFO", info)]:
        if not items:
            continue

        print(f"\n{severity} ({len(items)}):")
        for issue in items:
            print(f"  Location: {issue.get('location', 'unknown')}")
            print(f"  Issue: {issue.get('message')}")
            if "suggestion" in issue:
                print(f"  Suggestion: {issue.get('suggestion')}")
            print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Ansible playbooks for common idempotency issues"
    )
    parser.add_argument(
        "playbooks",
        nargs="+",
        type=Path,
        help="Playbook files to check",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Include informational issues",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show only summary, not individual issues",
    )

    args = parser.parse_args()

    checker = IdempotencyChecker(strict=args.strict)
    all_issues: dict[Path, List[dict]] = {}
    total_issues = 0

    for playbook_path in args.playbooks:
        if not playbook_path.exists():
            print(f"ERROR: File not found: {playbook_path}", file=sys.stderr)
            continue

        issues = checker.check_playbook(playbook_path)
        all_issues[playbook_path] = issues
        total_issues += len(issues)

        if not args.summary:
            print_issues(playbook_path, issues)

    print("\n" + "=" * 70)
    print(f"Summary: Checked {len(args.playbooks)} playbook(s)")
    print(f"Total issues: {total_issues}")

    if total_issues == 0:
        print("All playbooks look good.")
        return 0

    print(f"Found issues in {sum(1 for i in all_issues.values() if i)} playbook(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
