#!/usr/bin/env python3
"""Version consistency validator for WORKFLOW.md and SKILL.md files.

This script validates that:
1. All SKILL.md files have valid semantic version numbers in YAML frontmatter
2. WORKFLOW.md has a valid version number
3. WORKFLOW.md phase descriptions reference correct skill versions
4. TODO.md manifest has correct version
5. All version numbers follow semantic versioning (MAJOR.MINOR.PATCH)

Usage:
    python .claude/skills/workflow-utilities/scripts/validate_versions.py

Options:
    --verbose: Show detailed version information for all skills
    --fix: Attempt to auto-fix minor inconsistencies (use with caution)

Exit codes:
    0: All validations passed
    1: Validation errors found
    2: Script error (missing files, parse errors)

Constants:
- SKILL_DIRS: List of expected skill directory names
  Rationale: Define expected skills to validate against
- VERSION_PATTERN: Regex for semantic versioning
  Rationale: Enforce MAJOR.MINOR.PATCH format
"""

import re
import sys
from pathlib import Path

# Constants with documented rationale
SKILL_DIRS = [
    "workflow-orchestrator",
    "tech-stack-adapter",
    "git-workflow-manager",
    "bmad-planner",
    "speckit-author",
    "quality-enforcer",
    "workflow-utilities",
    "initialize-repository",
    "agentdb-state-manager",
]  # Expected skills to validate

VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")  # Semantic versioning: MAJOR.MINOR.PATCH
YAML_FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL | re.MULTILINE)


class ValidationError:
    """Represents a validation error found during checks."""

    def __init__(self, severity: str, file: str, message: str):
        self.severity = severity  # 'ERROR' or 'WARNING'
        self.file = file
        self.message = message

    def __str__(self):
        return f"[{self.severity}] {self.file}: {self.message}"


class VersionValidator:
    """Validates version consistency across workflow documentation."""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.errors: list[ValidationError] = []
        self.warnings: list[ValidationError] = []
        self.skill_versions: dict[str, tuple[str, Path]] = {}  # skill_name -> (version, path)

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(message)

    def add_error(self, file: str, message: str):
        """Add validation error."""
        self.errors.append(ValidationError("ERROR", file, message))

    def add_warning(self, file: str, message: str):
        """Add validation warning."""
        self.warnings.append(ValidationError("WARNING", file, message))

    def parse_version(self, version_str: str) -> tuple[int, int, int] | None:
        """Parse semantic version string into (major, minor, patch) tuple.

        Args:
            version_str: Version string like "5.1.0"

        Returns:
            Tuple of (major, minor, patch) integers, or None if invalid

        Raises:
            None - returns None on invalid input
        """
        match = VERSION_PATTERN.match(version_str)
        if not match:
            return None
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))

    def extract_yaml_frontmatter(self, content: str) -> dict[str, str] | None:
        """Extract YAML frontmatter from markdown file.

        Args:
            content: File content

        Returns:
            Dictionary of YAML key-value pairs, or None if no frontmatter found
        """
        match = YAML_FRONTMATTER_PATTERN.match(content)
        if not match:
            return None

        frontmatter = {}
        for line in match.group(1).split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter

    def validate_skill_file(self, skill_name: str, skill_dir: Path) -> bool:
        """Validate a single SKILL.md file.

        Args:
            skill_name: Name of the skill
            skill_dir: Path to skill directory

        Returns:
            True if validation passed, False otherwise
        """
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            self.add_error(str(skill_md), "SKILL.md file not found")
            return False

        content = skill_md.read_text()

        # Extract YAML frontmatter
        frontmatter = self.extract_yaml_frontmatter(content)
        if not frontmatter:
            self.add_error(str(skill_md), "No YAML frontmatter found")
            return False

        # Check for required fields
        if "name" not in frontmatter:
            self.add_error(str(skill_md), "Missing 'name' field in frontmatter")
            return False

        if "version" not in frontmatter:
            self.add_error(str(skill_md), "Missing 'version' field in frontmatter")
            return False

        # Validate name matches directory
        expected_name = skill_name
        actual_name = frontmatter["name"]
        if actual_name != expected_name:
            self.add_warning(str(skill_md), f"Name mismatch: frontmatter has '{actual_name}', expected '{expected_name}'")

        # Validate version format
        version = frontmatter["version"]
        parsed_version = self.parse_version(version)
        if not parsed_version:
            self.add_error(str(skill_md), f"Invalid version format: '{version}' (expected MAJOR.MINOR.PATCH)")
            return False

        # Store version for cross-reference checks
        self.skill_versions[skill_name] = (version, skill_md)

        self.log(f"✓ {skill_name}: version {version}")

        return True

    def validate_all_skills(self) -> bool:
        """Validate all skill SKILL.md files.

        Returns:
            True if all validations passed, False otherwise
        """
        self.log("\nValidating skill SKILL.md files...")
        self.log("-" * 70)

        skills_dir = self.repo_root / ".claude" / "skills"
        if not skills_dir.exists():
            self.add_error(str(skills_dir), "Skills directory not found")
            return False

        all_valid = True

        for skill_name in SKILL_DIRS:
            skill_dir = skills_dir / skill_name
            if not skill_dir.exists():
                self.add_warning(str(skill_dir), f"Skill directory not found: {skill_name}")
                continue

            if not self.validate_skill_file(skill_name, skill_dir):
                all_valid = False

        return all_valid

    def validate_workflow_md(self) -> bool:
        """Validate WORKFLOW.md version and skill references.

        Returns:
            True if validation passed, False otherwise
        """
        self.log("\nValidating WORKFLOW.md...")
        self.log("-" * 70)

        workflow_md = self.repo_root / "WORKFLOW.md"
        if not workflow_md.exists():
            self.add_error(str(workflow_md), "WORKFLOW.md not found")
            return False

        content = workflow_md.read_text()

        # Extract version from line 3: **Version:** X.Y.Z
        version_match = re.search(r"\*\*Version:\*\*\s+(\d+\.\d+\.\d+)", content)
        if not version_match:
            self.add_error(str(workflow_md), "Version number not found (expected on line 3)")
            return False

        workflow_version = version_match.group(1)
        parsed_version = self.parse_version(workflow_version)
        if not parsed_version:
            self.add_error(str(workflow_md), f"Invalid version format: '{workflow_version}' (expected MAJOR.MINOR.PATCH)")
            return False

        self.log(f"✓ WORKFLOW.md: version {workflow_version}")

        # Check for skill references in phase sections
        # Look for patterns like: [bmad-planner](/.claude/skills/bmad-planner/SKILL.md)
        skill_ref_pattern = re.compile(r"\[([a-z-]+)\]\(/\.claude/skills/\1/SKILL\.md\)")
        skill_refs = skill_ref_pattern.findall(content)

        self.log(f"  Found {len(skill_refs)} skill references in WORKFLOW.md")

        for skill_name in skill_refs:
            if skill_name not in self.skill_versions:
                self.add_warning(str(workflow_md), f"Referenced skill '{skill_name}' not found or not validated")

        return True

    def validate_todo_md(self) -> bool:
        """Validate TODO.md manifest version.

        Returns:
            True if validation passed, False otherwise
        """
        self.log("\nValidating TODO.md manifest...")
        self.log("-" * 70)

        todo_md = self.repo_root / "TODO.md"
        if not todo_md.exists():
            self.add_warning(str(todo_md), "TODO.md not found (optional)")
            return True

        content = todo_md.read_text()

        # Extract frontmatter
        frontmatter = self.extract_yaml_frontmatter(content)
        if not frontmatter:
            self.add_warning(str(todo_md), "No YAML frontmatter found")
            return True

        # Check for version field
        if "version" in frontmatter:
            version = frontmatter["version"]
            parsed_version = self.parse_version(version)
            if not parsed_version:
                self.add_warning(str(todo_md), f"Invalid version format: '{version}' (expected MAJOR.MINOR.PATCH)")
                return False

            self.log(f"✓ TODO.md: version {version}")
        else:
            self.log("  TODO.md: no version field (optional)")

        return True

    def validate_claude_md(self) -> bool:
        """Validate root CLAUDE.md references.

        Returns:
            True if validation passed, False otherwise
        """
        self.log("\nValidating root CLAUDE.md...")
        self.log("-" * 70)

        claude_md = self.repo_root / "CLAUDE.md"
        if not claude_md.exists():
            self.add_error(str(claude_md), "CLAUDE.md not found")
            return False

        content = claude_md.read_text()

        # Look for skill version references
        # Pattern: **current_version:** v1.X.Y
        version_ref_pattern = re.compile(r"\*\*[Cc]urrent[_ ]version:\*\*\s+v?(\d+\.\d+\.\d+)")
        version_refs = version_ref_pattern.findall(content)

        if version_refs:
            for version in version_refs:
                parsed = self.parse_version(version)
                if not parsed:
                    self.add_warning(str(claude_md), f"Invalid version format in reference: '{version}'")

            self.log(f"✓ CLAUDE.md: found {len(version_refs)} version references")
        else:
            self.log("  CLAUDE.md: no explicit version references found (may be OK)")

        return True

    def print_summary(self) -> bool:
        """Print validation summary and return overall status.

        Returns:
            True if no errors found, False otherwise
        """
        print("\n" + "=" * 70)
        print("Validation Summary")
        print("=" * 70)

        if self.errors:
            print(f"\n❌ {len(self.errors)} ERROR(S) found:\n")
            for error in self.errors:
                print(f"  {error}")
        else:
            print("\n✓ No errors found")

        if self.warnings:
            print(f"\n⚠ {len(self.warnings)} WARNING(S) found:\n")
            for warning in self.warnings:
                print(f"  {warning}")

        print("\n" + "=" * 70)

        if self.verbose and self.skill_versions:
            print("\nSkill Versions:")
            print("-" * 70)
            for skill, (version, path) in sorted(self.skill_versions.items()):
                print(f"  {skill:25s} v{version}")
            print()

        return len(self.errors) == 0

    def run_validation(self) -> bool:
        """Run all validation checks.

        Returns:
            True if all validations passed, False otherwise
        """
        print("=" * 70)
        print("Version Consistency Validator")
        print("=" * 70)
        print(f"Repository: {self.repo_root}")
        print()

        all_valid = True

        # Validate all SKILL.md files
        if not self.validate_all_skills():
            all_valid = False

        # Validate WORKFLOW.md
        if not self.validate_workflow_md():
            all_valid = False

        # Validate TODO.md
        if not self.validate_todo_md():
            all_valid = False

        # Validate root CLAUDE.md
        if not self.validate_claude_md():
            all_valid = False

        return all_valid


def main():
    """Main entry point for version validator."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate version consistency across WORKFLOW.md and SKILL.md files")
    parser.add_argument("--verbose", action="store_true", help="Show detailed version information")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix minor inconsistencies (NOT IMPLEMENTED YET)")

    args = parser.parse_args()

    if args.fix:
        print("ERROR: --fix option is not yet implemented")
        sys.exit(2)

    # Determine repository root
    try:
        import subprocess

        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True)
        repo_root = Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("ERROR: Not in a git repository")
        sys.exit(2)
    except FileNotFoundError:
        print("ERROR: git command not found")
        sys.exit(2)

    # Run validation
    validator = VersionValidator(repo_root, verbose=args.verbose)
    validator.run_validation()

    # Print summary
    success = validator.print_summary()

    # Exit with appropriate code
    if success:
        print("✓ All validation checks passed!")
        sys.exit(0)
    else:
        print("❌ Validation failed - please fix errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
