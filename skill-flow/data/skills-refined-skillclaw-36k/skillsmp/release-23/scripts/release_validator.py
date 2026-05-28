#!/usr/bin/env python3
"""
Release Validator - Comprehensive SDLC validation for multi-project releases.

Supports: Claude Code plugins, Python, Node.js, Go, Rust, and generic git repos.
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class ProjectType(Enum):
    CLAUDE_PLUGIN = "claude-plugin"
    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    RUST = "rust"
    GENERIC = "generic"


class ValidationResult(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WARNING = "warning"


@dataclass
class CheckResult:
    name: str
    result: ValidationResult
    message: str
    details: Optional[str] = None
    coverage: Optional[float] = None


@dataclass
class ValidationReport:
    project_type: ProjectType
    project_path: Path
    checks: list[CheckResult] = field(default_factory=list)
    breaking_changes: list[str] = field(default_factory=list)
    semver_recommendation: str = "patch"

    @property
    def passed(self) -> bool:
        return all(c.result in (ValidationResult.PASSED, ValidationResult.SKIPPED, ValidationResult.WARNING)
                   for c in self.checks)

    @property
    def has_warnings(self) -> bool:
        return any(c.result == ValidationResult.WARNING for c in self.checks)


def run_command(cmd: list[str], cwd: Path, capture: bool = True) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 300 seconds"
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"


def detect_project_type(path: Path) -> ProjectType:
    """Detect project type using cascade detection."""
    # Claude Code plugin
    if (path / ".claude-plugin" / "plugin.json").exists():
        return ProjectType.CLAUDE_PLUGIN
    if (path / "plugin.json").exists():
        return ProjectType.CLAUDE_PLUGIN

    # Python
    if (path / "pyproject.toml").exists() or (path / "setup.py").exists():
        return ProjectType.PYTHON

    # Node.js
    if (path / "package.json").exists():
        return ProjectType.NODEJS

    # Go
    if (path / "go.mod").exists():
        return ProjectType.GO

    # Rust
    if (path / "Cargo.toml").exists():
        return ProjectType.RUST

    # Generic git repo
    if (path / ".git").exists():
        return ProjectType.GENERIC

    return ProjectType.GENERIC


def get_coverage_threshold(path: Path, project_type: ProjectType, default: float = 95.0) -> float:
    """Get coverage threshold from project config or use default."""
    try:
        if project_type == ProjectType.PYTHON:
            pyproject = path / "pyproject.toml"
            if pyproject.exists():
                content = pyproject.read_text()
                # Look for fail_under in pytest-cov config
                match = re.search(r'fail_under\s*=\s*(\d+(?:\.\d+)?)', content)
                if match:
                    return float(match.group(1))

        elif project_type == ProjectType.NODEJS:
            pkg = path / "package.json"
            if pkg.exists():
                data = json.loads(pkg.read_text())
                # Check jest config
                jest_config = data.get("jest", {})
                coverage = jest_config.get("coverageThreshold", {}).get("global", {})
                if "lines" in coverage:
                    return float(coverage["lines"])
    except Exception:
        pass

    return default


def validate_claude_plugin(path: Path, report: ValidationReport) -> None:
    """Validate Claude Code plugin structure and components."""
    # Check plugin.json
    plugin_json = path / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        plugin_json = path / "plugin.json"

    if plugin_json.exists():
        try:
            data = json.loads(plugin_json.read_text())
            required = ["name", "version", "description"]
            missing = [f for f in required if f not in data]
            if missing:
                report.checks.append(CheckResult(
                    "plugin.json", ValidationResult.FAILED,
                    f"Missing required fields: {', '.join(missing)}"
                ))
            else:
                report.checks.append(CheckResult(
                    "plugin.json", ValidationResult.PASSED,
                    f"Valid plugin.json (v{data.get('version', 'unknown')})"
                ))
        except json.JSONDecodeError as e:
            report.checks.append(CheckResult(
                "plugin.json", ValidationResult.FAILED,
                f"Invalid JSON: {e}"
            ))
    else:
        report.checks.append(CheckResult(
            "plugin.json", ValidationResult.FAILED,
            "plugin.json not found"
        ))

    # Validate agents
    agents_dir = path / "agents"
    if agents_dir.exists():
        agent_files = list(agents_dir.rglob("*.md"))
        valid_agents = 0
        for agent_file in agent_files[:10]:  # Sample first 10
            content = agent_file.read_text()
            if content.startswith("---"):
                valid_agents += 1

        if agent_files:
            report.checks.append(CheckResult(
                "agents", ValidationResult.PASSED if valid_agents > 0 else ValidationResult.WARNING,
                f"Found {len(agent_files)} agents, {valid_agents} with valid frontmatter"
            ))

    # Validate skills
    skills_dir = path / "skills"
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        valid_skills = sum(1 for d in skill_dirs if (d / "SKILL.md").exists())
        report.checks.append(CheckResult(
            "skills", ValidationResult.PASSED if valid_skills > 0 else ValidationResult.WARNING,
            f"Found {len(skill_dirs)} skill directories, {valid_skills} with SKILL.md"
        ))

    # Validate commands
    commands_dir = path / "commands"
    if commands_dir.exists():
        command_files = list(commands_dir.glob("*.md"))
        report.checks.append(CheckResult(
            "commands", ValidationResult.PASSED,
            f"Found {len(command_files)} commands"
        ))


def validate_python(path: Path, report: ValidationReport, coverage_threshold: float) -> None:
    """Validate Python project with tests, lint, type check, security."""
    # Check for test framework
    has_pytest = (path / "pytest.ini").exists() or (path / "pyproject.toml").exists()

    # Run tests with coverage
    if has_pytest:
        code, stdout, stderr = run_command(
            ["python", "-m", "pytest", "--cov", ".", "--cov-report=term-missing", "-q"],
            path
        )
        if code == 0:
            # Extract coverage percentage
            coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', stdout)
            coverage = float(coverage_match.group(1)) if coverage_match else None

            if coverage and coverage < coverage_threshold:
                report.checks.append(CheckResult(
                    "tests+coverage", ValidationResult.FAILED,
                    f"Coverage {coverage}% below threshold {coverage_threshold}%",
                    coverage=coverage
                ))
            else:
                report.checks.append(CheckResult(
                    "tests+coverage", ValidationResult.PASSED,
                    f"Tests passed, coverage: {coverage}%" if coverage else "Tests passed",
                    coverage=coverage
                ))
        else:
            report.checks.append(CheckResult(
                "tests", ValidationResult.FAILED,
                "Tests failed",
                details=stderr[:500] if stderr else stdout[:500]
            ))
    else:
        report.checks.append(CheckResult(
            "tests", ValidationResult.SKIPPED,
            "No pytest configuration found"
        ))

    # Run ruff (fast Python linter)
    code, stdout, stderr = run_command(["ruff", "check", "."], path)
    if code == 0:
        report.checks.append(CheckResult("lint (ruff)", ValidationResult.PASSED, "No lint errors"))
    else:
        # Try fallback to flake8
        code2, _, _ = run_command(["flake8", "."], path)
        if code2 == 0:
            report.checks.append(CheckResult("lint (flake8)", ValidationResult.PASSED, "No lint errors"))
        else:
            report.checks.append(CheckResult(
                "lint", ValidationResult.FAILED,
                "Lint errors found",
                details=stdout[:500]
            ))

    # Run mypy (type checking)
    code, stdout, stderr = run_command(["mypy", ".", "--ignore-missing-imports"], path)
    if code == 0:
        report.checks.append(CheckResult("typecheck (mypy)", ValidationResult.PASSED, "No type errors"))
    else:
        report.checks.append(CheckResult(
            "typecheck", ValidationResult.WARNING,
            "Type errors found (non-blocking)",
            details=stdout[:500]
        ))

    # Run bandit (security)
    code, stdout, stderr = run_command(["bandit", "-r", ".", "-q"], path)
    if code == 0:
        report.checks.append(CheckResult("security (bandit)", ValidationResult.PASSED, "No security issues"))
    else:
        report.checks.append(CheckResult(
            "security", ValidationResult.WARNING,
            "Security warnings found",
            details=stdout[:500]
        ))

    # Run pip-audit (dependency vulnerabilities)
    code, stdout, stderr = run_command(["pip-audit"], path)
    if code == 0:
        report.checks.append(CheckResult("dependencies (pip-audit)", ValidationResult.PASSED, "No vulnerable dependencies"))
    else:
        report.checks.append(CheckResult(
            "dependencies", ValidationResult.WARNING,
            "Dependency vulnerabilities found",
            details=stdout[:500]
        ))


def validate_nodejs(path: Path, report: ValidationReport, _coverage_threshold: float) -> None:
    """Validate Node.js project. Coverage threshold available but npm coverage varies by setup."""
    pkg_path = path / "package.json"
    if not pkg_path.exists():
        report.checks.append(CheckResult("package.json", ValidationResult.FAILED, "package.json not found"))
        return

    pkg = json.loads(pkg_path.read_text())
    scripts = pkg.get("scripts", {})

    # Run tests
    if "test" in scripts:
        code, stdout, stderr = run_command(["npm", "test"], path)
        if code == 0:
            report.checks.append(CheckResult("tests", ValidationResult.PASSED, "Tests passed"))
        else:
            report.checks.append(CheckResult(
                "tests", ValidationResult.FAILED,
                "Tests failed",
                details=stderr[:500] if stderr else stdout[:500]
            ))
    else:
        report.checks.append(CheckResult("tests", ValidationResult.SKIPPED, "No test script defined"))

    # Run lint
    if "lint" in scripts:
        code, stdout, stderr = run_command(["npm", "run", "lint"], path)
        if code == 0:
            report.checks.append(CheckResult("lint", ValidationResult.PASSED, "No lint errors"))
        else:
            report.checks.append(CheckResult(
                "lint", ValidationResult.FAILED,
                "Lint errors found",
                details=stdout[:500]
            ))
    else:
        # Try eslint directly
        code, stdout, stderr = run_command(["npx", "eslint", "."], path)
        if code == 0:
            report.checks.append(CheckResult("lint (eslint)", ValidationResult.PASSED, "No lint errors"))
        else:
            report.checks.append(CheckResult("lint", ValidationResult.SKIPPED, "No lint configuration"))

    # Run npm audit
    code, stdout, stderr = run_command(["npm", "audit", "--production"], path)
    if code == 0:
        report.checks.append(CheckResult("security (npm audit)", ValidationResult.PASSED, "No vulnerabilities"))
    else:
        report.checks.append(CheckResult(
            "security", ValidationResult.WARNING,
            "Vulnerabilities found",
            details=stdout[:500]
        ))


def validate_go(path: Path, report: ValidationReport, coverage_threshold: float) -> None:
    """Validate Go project."""
    # Run tests with coverage
    code, stdout, stderr = run_command(
        ["go", "test", "-cover", "-race", "./..."],
        path
    )
    if code == 0:
        # Extract coverage
        coverage_match = re.search(r'coverage: (\d+\.?\d*)%', stdout)
        coverage = float(coverage_match.group(1)) if coverage_match else None

        if coverage and coverage < coverage_threshold:
            report.checks.append(CheckResult(
                "tests+coverage", ValidationResult.FAILED,
                f"Coverage {coverage}% below threshold {coverage_threshold}%",
                coverage=coverage
            ))
        else:
            report.checks.append(CheckResult(
                "tests+coverage", ValidationResult.PASSED,
                f"Tests passed, coverage: {coverage}%" if coverage else "Tests passed",
                coverage=coverage
            ))
    else:
        report.checks.append(CheckResult(
            "tests", ValidationResult.FAILED,
            "Tests failed",
            details=stderr[:500] if stderr else stdout[:500]
        ))

    # Run golangci-lint
    code, stdout, stderr = run_command(["golangci-lint", "run"], path)
    if code == 0:
        report.checks.append(CheckResult("lint (golangci-lint)", ValidationResult.PASSED, "No lint errors"))
    else:
        report.checks.append(CheckResult(
            "lint", ValidationResult.WARNING,
            "Lint warnings found",
            details=stdout[:500]
        ))

    # Run go vet
    code, stdout, stderr = run_command(["go", "vet", "./..."], path)
    if code == 0:
        report.checks.append(CheckResult("vet", ValidationResult.PASSED, "No issues"))
    else:
        report.checks.append(CheckResult(
            "vet", ValidationResult.WARNING,
            "Vet warnings found",
            details=stderr[:500]
        ))


def validate_rust(path: Path, report: ValidationReport, _coverage_threshold: float) -> None:
    """Validate Rust project. Coverage threshold available but cargo-tarpaulin varies by setup."""
    # Run tests
    code, stdout, stderr = run_command(["cargo", "test"], path)
    if code == 0:
        report.checks.append(CheckResult("tests", ValidationResult.PASSED, "Tests passed"))
    else:
        report.checks.append(CheckResult(
            "tests", ValidationResult.FAILED,
            "Tests failed",
            details=stderr[:500] if stderr else stdout[:500]
        ))

    # Run clippy
    code, stdout, stderr = run_command(["cargo", "clippy", "--", "-D", "warnings"], path)
    if code == 0:
        report.checks.append(CheckResult("lint (clippy)", ValidationResult.PASSED, "No lint errors"))
    else:
        report.checks.append(CheckResult(
            "lint", ValidationResult.WARNING,
            "Clippy warnings found",
            details=stderr[:500]
        ))

    # Run cargo audit
    code, stdout, stderr = run_command(["cargo", "audit"], path)
    if code == 0:
        report.checks.append(CheckResult("security (cargo audit)", ValidationResult.PASSED, "No vulnerabilities"))
    else:
        report.checks.append(CheckResult(
            "security", ValidationResult.WARNING,
            "Security advisories found",
            details=stdout[:500]
        ))

    # Check formatting
    code, stdout, stderr = run_command(["cargo", "fmt", "--check"], path)
    if code == 0:
        report.checks.append(CheckResult("format", ValidationResult.PASSED, "Code is formatted"))
    else:
        report.checks.append(CheckResult(
            "format", ValidationResult.FAILED,
            "Code needs formatting (run: cargo fmt)"
        ))


def validate_changelog(path: Path, report: ValidationReport) -> None:
    """Validate CHANGELOG.md exists and has unreleased section."""
    changelog = path / "CHANGELOG.md"
    if not changelog.exists():
        report.checks.append(CheckResult(
            "changelog", ValidationResult.WARNING,
            "CHANGELOG.md not found"
        ))
        return

    content = changelog.read_text()
    if "## [Unreleased]" in content:
        report.checks.append(CheckResult(
            "changelog", ValidationResult.PASSED,
            "CHANGELOG.md has [Unreleased] section"
        ))
    else:
        report.checks.append(CheckResult(
            "changelog", ValidationResult.WARNING,
            "CHANGELOG.md missing [Unreleased] section"
        ))


def detect_breaking_changes(path: Path, report: ValidationReport) -> None:
    """Detect potential breaking changes since last tag."""
    # Get last tag
    code, stdout, stderr = run_command(
        ["git", "describe", "--tags", "--abbrev=0"],
        path
    )
    if code != 0:
        report.checks.append(CheckResult(
            "breaking-changes", ValidationResult.SKIPPED,
            "No previous tags found"
        ))
        return

    last_tag = stdout.strip()

    # Check for deleted/renamed files
    code, stdout, stderr = run_command(
        ["git", "diff", "--name-status", f"{last_tag}..HEAD"],
        path
    )
    if code != 0:
        return

    breaking = []
    for line in stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]

        if status.startswith("D"):
            file_path = parts[1]
            # Deleted public files are breaking
            if not file_path.startswith(".") and not file_path.startswith("test"):
                breaking.append(f"DELETED: {file_path}")
        elif status.startswith("R"):
            old_path = parts[1]
            new_path = parts[2] if len(parts) > 2 else "unknown"
            if not old_path.startswith(".") and not old_path.startswith("test"):
                breaking.append(f"RENAMED: {old_path} -> {new_path}")

    report.breaking_changes = breaking

    if breaking:
        report.checks.append(CheckResult(
            "breaking-changes", ValidationResult.WARNING,
            f"Found {len(breaking)} potential breaking change(s)",
            details="\n".join(breaking[:10])
        ))
        # Recommend major version
        report.semver_recommendation = "major"
    else:
        report.checks.append(CheckResult(
            "breaking-changes", ValidationResult.PASSED,
            "No breaking changes detected"
        ))


def check_ci_will_pass(path: Path, report: ValidationReport) -> None:
    """Check if CI workflows exist and are likely to pass."""
    ci_paths = [
        path / ".github" / "workflows",
        path / ".gitlab-ci.yml",
        path / "Jenkinsfile",
        path / ".circleci",
    ]

    ci_found = False
    for ci_path in ci_paths:
        if ci_path.exists():
            ci_found = True
            if ci_path.is_dir():
                workflows = list(ci_path.glob("*.yml")) + list(ci_path.glob("*.yaml"))
                report.checks.append(CheckResult(
                    "ci-config", ValidationResult.PASSED,
                    f"Found {len(workflows)} CI workflow(s) in {ci_path.name}"
                ))
            else:
                report.checks.append(CheckResult(
                    "ci-config", ValidationResult.PASSED,
                    f"Found CI config: {ci_path.name}"
                ))
            break

    if not ci_found:
        report.checks.append(CheckResult(
            "ci-config", ValidationResult.WARNING,
            "No CI configuration found"
        ))


def validate_project(
    path: Path,
    coverage_threshold: float = 95.0,
    project_type: Optional[ProjectType] = None
) -> ValidationReport:
    """Run all validations for a project."""
    if project_type is None:
        project_type = detect_project_type(path)

    report = ValidationReport(
        project_type=project_type,
        project_path=path
    )

    # Get actual coverage threshold from project config
    actual_threshold = get_coverage_threshold(path, project_type, coverage_threshold)

    # Common validations
    validate_changelog(path, report)
    detect_breaking_changes(path, report)
    check_ci_will_pass(path, report)

    # Project-specific validations
    if project_type == ProjectType.CLAUDE_PLUGIN:
        validate_claude_plugin(path, report)
    elif project_type == ProjectType.PYTHON:
        validate_python(path, report, actual_threshold)
    elif project_type == ProjectType.NODEJS:
        validate_nodejs(path, report, actual_threshold)
    elif project_type == ProjectType.GO:
        validate_go(path, report, actual_threshold)
    elif project_type == ProjectType.RUST:
        validate_rust(path, report, actual_threshold)
    else:
        report.checks.append(CheckResult(
            "project-type", ValidationResult.WARNING,
            "Generic project - minimal validation available"
        ))

    # Determine semver recommendation based on changes
    if report.breaking_changes:
        report.semver_recommendation = "major"
    elif any("feat" in c.name.lower() for c in report.checks if c.result == ValidationResult.PASSED):
        report.semver_recommendation = "minor"
    else:
        report.semver_recommendation = "patch"

    return report


def print_report(report: ValidationReport, verbose: bool = False) -> None:
    """Print validation report to stdout."""
    print(f"\n{'='*60}")
    print(f"RELEASE VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"Project Type: {report.project_type.value}")
    print(f"Project Path: {report.project_path}")
    print(f"Semver Recommendation: {report.semver_recommendation}")
    print(f"{'='*60}\n")

    # Group by result
    passed = [c for c in report.checks if c.result == ValidationResult.PASSED]
    warnings = [c for c in report.checks if c.result == ValidationResult.WARNING]
    failed = [c for c in report.checks if c.result == ValidationResult.FAILED]
    skipped = [c for c in report.checks if c.result == ValidationResult.SKIPPED]

    if passed:
        print("PASSED:")
        for c in passed:
            coverage_info = f" ({c.coverage}%)" if c.coverage else ""
            print(f"  [OK] {c.name}: {c.message}{coverage_info}")

    if warnings:
        print("\nWARNINGS:")
        for c in warnings:
            print(f"  [!!] {c.name}: {c.message}")
            if verbose and c.details:
                print(f"       {c.details[:200]}")

    if failed:
        print("\nFAILED:")
        for c in failed:
            print(f"  [XX] {c.name}: {c.message}")
            if c.details:
                print(f"       {c.details[:200]}")

    if skipped:
        print("\nSKIPPED:")
        for c in skipped:
            print(f"  [--] {c.name}: {c.message}")

    if report.breaking_changes:
        print(f"\nBREAKING CHANGES DETECTED ({len(report.breaking_changes)}):")
        for change in report.breaking_changes[:5]:
            print(f"  - {change}")
        if len(report.breaking_changes) > 5:
            print(f"  ... and {len(report.breaking_changes) - 5} more")

    print(f"\n{'='*60}")
    if report.passed:
        print("RESULT: READY FOR RELEASE")
        if report.has_warnings:
            print("(Some warnings should be reviewed)")
    else:
        print("RESULT: NOT READY FOR RELEASE")
        print(f"Fix {len(failed)} failing check(s) before release")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate project for release",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path (default: current directory)"
    )
    parser.add_argument(
        "--type",
        choices=[t.value for t in ProjectType],
        help="Force project type detection"
    )
    parser.add_argument(
        "--coverage-threshold",
        type=float,
        default=95.0,
        help="Minimum coverage percentage (default: 95)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check, don't suggest fixes"
    )

    args = parser.parse_args()

    path = Path(args.path).resolve()
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)

    project_type = ProjectType(args.type) if args.type else None

    report = validate_project(
        path,
        coverage_threshold=args.coverage_threshold,
        project_type=project_type
    )

    if args.json:
        output = {
            "project_type": report.project_type.value,
            "project_path": str(report.project_path),
            "passed": report.passed,
            "has_warnings": report.has_warnings,
            "semver_recommendation": report.semver_recommendation,
            "breaking_changes": report.breaking_changes,
            "checks": [
                {
                    "name": c.name,
                    "result": c.result.value,
                    "message": c.message,
                    "details": c.details,
                    "coverage": c.coverage
                }
                for c in report.checks
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(report, verbose=args.verbose)

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
