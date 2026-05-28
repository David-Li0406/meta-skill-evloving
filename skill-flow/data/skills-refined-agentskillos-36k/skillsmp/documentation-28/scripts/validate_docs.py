#!/usr/bin/env python3
"""
Documentation Structure Validator

Validates that documentation follows the required structure and conventions.
Checks for required files, proper formatting, and consistency.

Usage:
    python validate_docs.py <documentation_path> [--format text|json]
    python validate_docs.py ./Documentation --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Issue(NamedTuple):
    file: str
    issue: str
    severity: str  # "error", "warning", "info"
    fix: str


# Required top-level files
REQUIRED_FILES = [
    "project-roadmap.md",
    "architecture.md",
    "changelog.md",
]

# Feature file required sections
FEATURE_SECTIONS = [
    "## User Story",
    "## Overview",
    "## Acceptance Criteria",
    "## Technical Notes",
]

# Module explainer required sections
MODULE_SECTIONS = [
    "## Overview",
    "## Features",
]

# Status values
VALID_FEATURE_STATUS = {"Planned", "In Progress", "Complete"}
VALID_ROADMAP_STATUS = {"⏳", "🔄", "✅", "🚫"}


def find_documentation_root(path: Path) -> Path | None:
    """Find the Documentation folder."""
    if path.name.lower() == "documentation":
        return path
    doc_path = path / "Documentation"
    if doc_path.exists():
        return doc_path
    return path if path.is_dir() else None


def validate_required_files(doc_root: Path) -> list[Issue]:
    """Check that required top-level files exist."""
    issues = []

    for filename in REQUIRED_FILES:
        file_path = doc_root / filename
        if not file_path.exists():
            issues.append(Issue(
                file=str(doc_root),
                issue=f"Missing required file: {filename}",
                severity="error",
                fix=f"Create {filename} in the Documentation folder",
            ))

    return issues


def validate_changelog(doc_root: Path) -> list[Issue]:
    """Validate changelog format."""
    issues = []
    changelog_path = doc_root / "changelog.md"

    if not changelog_path.exists():
        return issues

    content = changelog_path.read_text(encoding="utf-8")

    # Check for Unreleased section
    if "## [Unreleased]" not in content:
        issues.append(Issue(
            file=str(changelog_path),
            issue="Missing [Unreleased] section",
            severity="warning",
            fix="Add ## [Unreleased] section at the top for pending changes",
        ))

    # Check for proper version format
    version_pattern = r"## \[\d+\.\d+\.\d+\]"
    if not re.search(version_pattern, content) and "[Unreleased]" in content:
        issues.append(Issue(
            file=str(changelog_path),
            issue="No released versions found (only Unreleased)",
            severity="info",
            fix="Add version entries as releases are made",
        ))

    # Check for dates on version entries
    version_no_date = r"## \[\d+\.\d+\.\d+\]\s*$"
    if re.search(version_no_date, content, re.MULTILINE):
        issues.append(Issue(
            file=str(changelog_path),
            issue="Version entry missing date",
            severity="warning",
            fix="Add date in format: ## [X.Y.Z] — YYYY-MM-DD",
        ))

    # Check for change type sections
    has_changes = any(
        section in content
        for section in ["### Added", "### Changed", "### Fixed"]
    )
    if not has_changes:
        issues.append(Issue(
            file=str(changelog_path),
            issue="No change type sections found",
            severity="warning",
            fix="Add sections like ### Added, ### Changed, ### Fixed",
        ))

    return issues


def validate_feature_file(file_path: Path) -> list[Issue]:
    """Validate a feature specification file."""
    issues = []
    content = file_path.read_text(encoding="utf-8")

    # Check for required sections
    for section in FEATURE_SECTIONS:
        if section not in content:
            issues.append(Issue(
                file=str(file_path),
                issue=f"Missing section: {section}",
                severity="error",
                fix=f"Add {section} section to the feature file",
            ))

    # Check for status field
    status_match = re.search(r"\*\*Status:\*\*\s*(\w+(?:\s+\w+)?)", content)
    if status_match:
        status = status_match.group(1)
        if status not in VALID_FEATURE_STATUS:
            issues.append(Issue(
                file=str(file_path),
                issue=f"Invalid status: {status}",
                severity="warning",
                fix=f"Use one of: {', '.join(VALID_FEATURE_STATUS)}",
            ))
    else:
        issues.append(Issue(
            file=str(file_path),
            issue="Missing status field",
            severity="error",
            fix="Add **Status:** Planned|In Progress|Complete",
        ))

    # Check for user story format
    if "## User Story" in content:
        user_story_section = content.split("## User Story")[1].split("##")[0]
        if "**As a**" not in user_story_section:
            issues.append(Issue(
                file=str(file_path),
                issue="User story doesn't follow As/Want/So format",
                severity="warning",
                fix="Use format: **As a** X, **I want** Y, **So that** Z",
            ))

    # Check for acceptance criteria checkboxes
    if "## Acceptance Criteria" in content:
        criteria_section = content.split("## Acceptance Criteria")[1].split("##")[0]
        checkboxes = re.findall(r"- \[[ x]\]", criteria_section)
        if len(checkboxes) == 0:
            issues.append(Issue(
                file=str(file_path),
                issue="No acceptance criteria checkboxes found",
                severity="warning",
                fix="Add checkboxes: - [ ] Criterion",
            ))

    # Check for Standards Checklist
    if "Standards Checklist" not in content:
        issues.append(Issue(
            file=str(file_path),
            issue="Missing Standards Checklist in Technical Notes",
            severity="warning",
            fix="Add Standards Checklist section",
        ))

    return issues


def validate_module_explainer(file_path: Path) -> list[Issue]:
    """Validate a module explainer file."""
    issues = []
    content = file_path.read_text(encoding="utf-8")

    # Check for required sections
    for section in MODULE_SECTIONS:
        if section not in content:
            issues.append(Issue(
                file=str(file_path),
                issue=f"Missing section: {section}",
                severity="error",
                fix=f"Add {section} section to the module explainer",
            ))

    # Check for feature table
    if "## Features" in content:
        feature_section = content.split("## Features")[1].split("##")[0]
        if "|" not in feature_section:
            issues.append(Issue(
                file=str(file_path),
                issue="Features section missing table format",
                severity="warning",
                fix="Add feature table with columns: Feature, Status, Description",
            ))

    # Check for status count
    status_match = re.search(r"\*\*Status:\*\*\s*(\d+)/(\d+)", content)
    if not status_match:
        issues.append(Issue(
            file=str(file_path),
            issue="Missing status count",
            severity="info",
            fix="Add **Status:** X/Y features complete",
        ))

    return issues


def validate_features_folder(doc_root: Path) -> list[Issue]:
    """Validate the features folder structure."""
    issues = []
    features_path = doc_root / "features"

    if not features_path.exists():
        issues.append(Issue(
            file=str(doc_root),
            issue="Missing features/ folder",
            severity="info",
            fix="Create features/ folder when adding features",
        ))
        return issues

    # Traverse program/module structure
    for program_dir in features_path.iterdir():
        if not program_dir.is_dir():
            continue

        for module_dir in program_dir.iterdir():
            if not module_dir.is_dir():
                continue

            # Check for module explainer
            explainer_name = f"_{module_dir.name}.md"
            explainer_path = module_dir / explainer_name
            if not explainer_path.exists():
                issues.append(Issue(
                    file=str(module_dir),
                    issue=f"Missing module explainer: {explainer_name}",
                    severity="warning",
                    fix=f"Create {explainer_name} as module overview",
                ))
            else:
                issues.extend(validate_module_explainer(explainer_path))

            # Validate feature files
            for feature_file in module_dir.glob("*.md"):
                if feature_file.name.startswith("_"):
                    continue  # Skip module explainer
                issues.extend(validate_feature_file(feature_file))

    return issues


def validate_documentation(doc_root: Path) -> list[Issue]:
    """Run all validation checks."""
    issues = []

    issues.extend(validate_required_files(doc_root))
    issues.extend(validate_changelog(doc_root))
    issues.extend(validate_features_folder(doc_root))

    return issues


def format_text_output(issues: list[Issue], doc_root: Path) -> str:
    """Format issues as human-readable text."""
    if not issues:
        return f"✅ Documentation structure is valid: {doc_root}"

    output = []
    output.append(f"Found {len(issues)} documentation issue(s):\n")

    # Group by severity
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    info = [i for i in issues if i.severity == "info"]

    def format_issues(items, label, icon):
        if items:
            output.append(f"{icon} {label}:")
            for item in items:
                rel_path = item.file.replace(str(doc_root), ".")
                output.append(f"  {rel_path}")
                output.append(f"    Issue: {item.issue}")
                output.append(f"    Fix: {item.fix}")
            output.append("")

    format_issues(errors, "ERRORS", "❌")
    format_issues(warnings, "WARNINGS", "⚠️")
    format_issues(info, "INFO", "ℹ️")

    output.append("─" * 50)
    output.append(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s), {len(info)} info")

    if errors:
        output.append("\n❌ Documentation validation FAILED")
    else:
        output.append("\n⚠️ Documentation validation passed with findings")

    return "\n".join(output)


def format_json_output(issues: list[Issue]) -> str:
    """Format issues as JSON."""
    return json.dumps({
        "total": len(issues),
        "errors": sum(1 for i in issues if i.severity == "error"),
        "warnings": sum(1 for i in issues if i.severity == "warning"),
        "info": sum(1 for i in issues if i.severity == "info"),
        "issues": [i._asdict() for i in issues],
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Validate documentation structure and formatting"
    )
    parser.add_argument("path", help="Path to Documentation folder or project root")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    doc_root = find_documentation_root(path)
    if not doc_root or not doc_root.exists():
        print(f"Error: Could not find Documentation folder in {path}", file=sys.stderr)
        sys.exit(1)

    issues = validate_documentation(doc_root)

    if args.format == "json":
        print(format_json_output(issues))
    else:
        print(format_text_output(issues, doc_root))

    # Exit code based on errors
    errors = sum(1 for i in issues if i.severity == "error")
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
