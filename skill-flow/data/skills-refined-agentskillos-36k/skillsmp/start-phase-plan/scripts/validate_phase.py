#!/usr/bin/env python3
"""
Phase Validator Tool

Validates phase directory structure and planning files.

Usage:
    python validate_phase.py /path/to/project

Returns JSON with validation results.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


class PhaseValidator:
    """Validates phase structure and planning files."""

    REQUIRED_DIRS = [
        "planning/task-updates",
        "planning/agent-delegation",
        "planning/phase-structure",
        "planning/code-reviews"
    ]

    PLANNING_FILES = [
        "planning/agent-delegation/task-delegation.md",
        "planning/agent-delegation/sub-agent-plan.md",
        "planning/phase-structure/system-changes.md"
    ]

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.total_checks = 0

    def validate(self) -> Dict:
        """Run all validation checks."""

        self._check_directories()
        self._check_planning_files()
        self._check_task_updates()
        self._check_code_reviews()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks_passed": self.checks_passed,
            "total_checks": self.total_checks,
            "structure_complete": len(self.errors) == 0 and len(self.warnings) == 0
        }

    def _check_directories(self):
        """Check if all required directories exist."""
        for dir_path in self.REQUIRED_DIRS:
            self.total_checks += 1
            full_path = self.project_path / dir_path

            if not full_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
            elif not full_path.is_dir():
                self.errors.append(f"Path exists but is not a directory: {dir_path}")
            else:
                self.checks_passed += 1

    def _check_planning_files(self):
        """Check if planning files exist and have content."""
        for file_path in self.PLANNING_FILES:
            self.total_checks += 1
            full_path = self.project_path / file_path

            if not full_path.exists():
                self.warnings.append(f"Planning file not found: {file_path}")
                continue

            # Check file is not empty
            content = full_path.read_text(encoding='utf-8')

            if len(content.strip()) < 100:
                self.warnings.append(f"Planning file is very short: {file_path} ({len(content)} bytes)")
            else:
                self.checks_passed += 1

            # Specific checks per file type
            if "task-delegation.md" in file_path:
                self._validate_task_delegation(content, file_path)
            elif "sub-agent-plan.md" in file_path:
                self._validate_sub_agent_plan(content, file_path)
            elif "system-changes.md" in file_path:
                self._validate_system_changes(content, file_path)

    def _validate_task_delegation(self, content: str, file_path: str):
        """Validate task delegation file content."""
        # Check for Mermaid graph
        if "```mermaid" not in content:
            self.warnings.append(f"{file_path}: Missing Mermaid graph")

        # Check for agent assignments
        if "agent" not in content.lower() and "persona" not in content.lower():
            self.warnings.append(f"{file_path}: No agent assignments found")

        # Check for priorities
        if "priority" not in content.lower():
            self.warnings.append(f"{file_path}: No task priorities defined")

    def _validate_sub_agent_plan(self, content: str, file_path: str):
        """Validate sub-agent plan file content."""
        # Check for parallel execution instruction
        parallel_keywords = ["parallel", "concurrent", "spawn", "subagent"]

        if not any(keyword in content.lower() for keyword in parallel_keywords):
            self.warnings.append(f"{file_path}: No parallel execution strategy defined")

        # Check for waves or groups
        if "wave" not in content.lower() and "group" not in content.lower() and "phase" not in content.lower():
            self.warnings.append(f"{file_path}: Tasks not organized into execution waves")

    def _validate_system_changes(self, content: str, file_path: str):
        """Validate system changes file content."""
        # Check for Mermaid flowchart
        if "```mermaid" not in content or "flowchart" not in content.lower():
            self.warnings.append(f"{file_path}: Missing Mermaid flowchart of file relationships")

        # Check for SLOC table
        if "sloc" not in content.lower() or "baseline" not in content.lower():
            self.warnings.append(f"{file_path}: Missing SLOC tracking table")

    def _check_task_updates(self):
        """Check task updates directory."""
        task_updates_dir = self.project_path / "planning/task-updates"

        if not task_updates_dir.exists():
            # Already reported in _check_directories
            return

        # Count task update files
        task_files = list(task_updates_dir.glob("*.md"))

        if len(task_files) == 0:
            self.warnings.append("No task update files found (no tasks completed yet?)")
        else:
            # Check a sample of files for completeness
            sample_size = min(3, len(task_files))
            for task_file in task_files[:sample_size]:
                self._validate_task_update(task_file)

    def _validate_task_update(self, task_file: Path):
        """Validate a single task update file."""
        content = task_file.read_text(encoding='utf-8')

        # Check for required sections
        required_sections = [
            "what changed",
            "files touched",
            "how to verify"
        ]

        missing = [section for section in required_sections if section not in content.lower()]

        if missing:
            self.warnings.append(f"{task_file.name}: Missing sections - {', '.join(missing)}")

        # Check for checklist
        if "- [x]" not in content and "- [ ]" not in content:
            self.warnings.append(f"{task_file.name}: Missing quality gate checklist")

    def _check_code_reviews(self):
        """Check code reviews directory."""
        code_reviews_dir = self.project_path / "planning/code-reviews"

        if not code_reviews_dir.exists():
            # Already reported in _check_directories
            return

        # Count code review files
        review_files = list(code_reviews_dir.glob("*.md"))

        if len(review_files) == 0:
            self.warnings.append("No code review files found (no tasks reviewed yet?)")
        else:
            # Check a sample of files for completeness
            sample_size = min(3, len(review_files))
            for review_file in review_files[:sample_size]:
                self._validate_code_review(review_file)

    def _validate_code_review(self, review_file: Path):
        """Validate a single code review file."""
        content = review_file.read_text(encoding='utf-8')

        # Check for required sections
        required_keywords = ["summary", "issues", "verdict"]

        missing = [kw for kw in required_keywords if kw.lower() not in content.lower()]

        if missing:
            self.warnings.append(f"{review_file.name}: Missing sections - {', '.join(missing)}")

        # Check for verdict
        if "approved" not in content.lower() and "needs follow-up" not in content.lower():
            self.warnings.append(f"{review_file.name}: No clear verdict (Approved/Needs follow-up)")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "valid": False,
            "errors": ["Usage: python validate_phase.py /path/to/project"],
            "warnings": [],
            "checks_passed": 0,
            "total_checks": 0
        }, indent=2))
        sys.exit(1)

    project_path = Path(sys.argv[1])

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
    validator = PhaseValidator(project_path)
    result = validator.validate()

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit with error code if validation failed
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
