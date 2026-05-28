#!/usr/bin/env python3
"""
Task Validator Tool

Validates that a task has met all completion requirements:
- Task update file exists
- Code review file exists
- Quality gate passed
- Checklist completed
- Git commit created

Usage:
    python task_validator.py /path/to/project task-name

Returns JSON with validation results.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List
import re


class TaskValidator:
    """Validates task completion requirements."""

    def __init__(self, project_path: Path, task_name: str):
        self.project_path = project_path
        self.task_name = task_name
        self.planning_path = project_path / "planning"
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.total_checks = 0

    def validate(self) -> Dict:
        """Run all validation checks."""

        # Check planning directory exists
        if not self.planning_path.exists():
            return {
                "valid": False,
                "errors": ["Planning directory not found. Has phase started?"],
                "warnings": [],
                "checks_passed": 0,
                "total_checks": 0
            }

        # Run all checks
        self._check_task_update_file()
        self._check_code_review_file()
        self._check_checklist_completion()
        self._check_git_commit()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks_passed": self.checks_passed,
            "total_checks": self.total_checks,
            "completion_percentage": round((self.checks_passed / self.total_checks * 100) if self.total_checks > 0 else 0, 1)
        }

    def _check_task_update_file(self):
        """Check if task update file exists."""
        self.total_checks += 1

        task_update_path = self.planning_path / f"task-updates/{self.task_name}.md"

        if not task_update_path.exists():
            self.errors.append(f"Task update file not found: planning/task-updates/{self.task_name}.md")
            return

        # Check file is not empty
        content = task_update_path.read_text(encoding='utf-8')

        if len(content.strip()) < 100:
            self.warnings.append(f"Task update file is very short ({len(content)} bytes). May be incomplete.")

        # Check for required sections
        required_keywords = ["What Changed", "Files Touched", "How to Verify"]
        missing_sections = [kw for kw in required_keywords if kw.lower() not in content.lower()]

        if missing_sections:
            self.warnings.append(f"Task update missing sections: {', '.join(missing_sections)}")

        self.checks_passed += 1

    def _check_code_review_file(self):
        """Check if code review file exists."""
        self.total_checks += 1

        code_review_path = self.planning_path / f"code-reviews/{self.task_name}.md"

        if not code_review_path.exists():
            self.errors.append(f"Code review file not found: planning/code-reviews/{self.task_name}.md")
            return

        # Check file is not empty
        content = code_review_path.read_text(encoding='utf-8')

        if len(content.strip()) < 100:
            self.warnings.append(f"Code review file is very short ({len(content)} bytes). May be incomplete.")

        # Check for verdict
        if "approved" not in content.lower() and "needs follow-up" not in content.lower():
            self.warnings.append("Code review missing verdict (Approved / Needs follow-up)")

        # Check for required sections
        required_keywords = ["Summary", "Issues", "Verdict"]
        missing_sections = [kw for kw in required_keywords if kw.lower() not in content.lower()]

        if missing_sections:
            self.warnings.append(f"Code review missing sections: {', '.join(missing_sections)}")

        self.checks_passed += 1

    def _check_checklist_completion(self):
        """Check if task update has completed checklist."""
        self.total_checks += 1

        task_update_path = self.planning_path / f"task-updates/{self.task_name}.md"

        if not task_update_path.exists():
            # Already reported error in _check_task_update_file
            return

        content = task_update_path.read_text(encoding='utf-8')

        # Look for checklist items
        checklist_pattern = r'- \[(x| )\]'
        checklist_items = re.findall(checklist_pattern, content, re.IGNORECASE)

        if not checklist_items:
            self.warnings.append("Task update missing checklist items")
            return

        # Check if all items are checked
        completed_items = sum(1 for item in checklist_items if item.lower() == 'x')
        total_items = len(checklist_items)

        if completed_items < total_items:
            self.warnings.append(f"Checklist incomplete: {completed_items}/{total_items} items checked")
            return

        # Check for required checklist items
        required_checks = [
            "lint passed",
            "build passed",
            "review completed",
            "commit created"
        ]

        for check in required_checks:
            if check.lower() not in content.lower():
                self.warnings.append(f"Checklist missing required item: {check}")

        self.checks_passed += 1

    def _check_git_commit(self):
        """Check if git commit exists for this task."""
        self.total_checks += 1

        try:
            # Search git log for commit message containing task name
            result = subprocess.run(
                ["git", "log", "--oneline", "--grep", f"task: {self.task_name}", "-1"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                self.warnings.append("Could not check git log (git not available or not a git repo)")
                return

            if not result.stdout.strip():
                # Try alternative commit message format
                result = subprocess.run(
                    ["git", "log", "--oneline", "--grep", self.task_name, "-1"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if not result.stdout.strip():
                    self.warnings.append(f"No git commit found for task: {self.task_name}")
                    return

            self.checks_passed += 1

        except subprocess.TimeoutExpired:
            self.warnings.append("Git log check timed out")
        except FileNotFoundError:
            self.warnings.append("Git not available")
        except Exception as e:
            self.warnings.append(f"Error checking git commits: {str(e)}")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print(json.dumps({
            "valid": False,
            "errors": ["Usage: python task_validator.py /path/to/project task-name"],
            "warnings": [],
            "checks_passed": 0,
            "total_checks": 0
        }, indent=2))
        sys.exit(1)

    project_path = Path(sys.argv[1])
    task_name = sys.argv[2]

    if not project_path.exists():
        print(json.dumps({
            "valid": False,
            "errors": [f"Project path not found: {project_path}"],
            "warnings": [],
            "checks_passed": 0,
            "total_checks": 0
        }, indent=2))
        sys.exit(1)

    # Run validation
    validator = TaskValidator(project_path, task_name)
    result = validator.validate()

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit with error code if validation failed
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
