#!/usr/bin/env python3
"""
Technical Debt Analyzer - Master script that runs all checks.

Produces a prioritized report of technical debt across:
- Deferred work (TODO/FIXME/HACK)
- Security issues
- Testing gaps
- Maintainability (docstrings, type hints, naming)
- Dependency health

Usage:
    python analyze_all.py /path/to/project
    python analyze_all.py /path/to/project --format json
    python analyze_all.py /path/to/project --skip security  # Skip specific checks
"""

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

@dataclass
class DebtItem:
    """Unified debt item across all analyzers."""
    file: str
    line: int
    category: str
    issue: str
    severity: str
    description: str
    fix_sketch: str = ""

def load_analyzer(name: str):
    """Dynamically load an analyzer module."""
    script_path = SCRIPT_DIR / f"{name}.py"
    if not script_path.exists():
        return None

    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_deferred_work_check(project_path: Path, exclude_dirs: set) -> list[DebtItem]:
    """Run deferred work analysis."""
    items = []
    module = load_analyzer("find_deferred_work")
    if not module:
        return items

    findings = module.scan_directory(project_path, exclude_dirs)

    fix_sketches = {
        "FIXME": "Address the bug or issue described. If complex, create a ticket and add reference.",
        "BUG": "Investigate and fix the bug. Add regression test.",
        "HACK": "Replace workaround with proper solution. Document if workaround must remain.",
        "XXX": "Review dangerous code. Refactor or add safety guards.",
        "TODO": "Implement the planned feature or create a tracked ticket.",
        "OPTIMIZE": "Profile to confirm bottleneck, then optimize.",
        "NOTE": "Review if note is still relevant. Convert to docstring if valuable.",
        "REVIEW": "Conduct code review. Remove marker after review.",
    }

    for f in findings:
        items.append(DebtItem(
            file=f.file,
            line=f.line,
            category="deferred_work",
            issue=f.marker,
            severity=f.severity,
            description=f.message,
            fix_sketch=fix_sketches.get(f.marker, "Address the deferred work item.")
        ))

    return items

def run_security_check(project_path: Path, exclude_dirs: set) -> list[DebtItem]:
    """Run security analysis."""
    items = []
    module = load_analyzer("find_security_issues")
    if not module:
        return items

    findings = module.scan_directory(project_path, exclude_dirs)

    fix_sketches = {
        "hardcoded_secret": "Move to environment variables or secrets manager. Use: os.environ.get('KEY')",
        "hardcoded_secret_arg": "Pass credentials via config/env, not hardcoded strings.",
        "dangerous_function": "Replace eval/exec with safer alternatives (ast.literal_eval, explicit logic).",
        "shell_injection": "Use shell=False with list args: subprocess.run(['cmd', 'arg'], shell=False)",
        "unsafe_deserialization": "Use json.loads() for untrusted data. If pickle needed, validate source.",
        "assert_used": "Replace security-critical asserts with explicit if/raise statements.",
    }

    for f in findings:
        items.append(DebtItem(
            file=f.file,
            line=f.line,
            category="security",
            issue=f.issue,
            severity=f.severity,
            description=f.description,
            fix_sketch=fix_sketches.get(f.issue, "Review and remediate security issue.")
        ))

    return items

def run_testing_check(project_path: Path, exclude_dirs: set) -> list[DebtItem]:
    """Run test coverage analysis."""
    items = []
    module = load_analyzer("analyze_test_coverage")
    if not module:
        return items

    findings = module.scan_directory(project_path, exclude_dirs, run_coverage=False)

    fix_sketches = {
        "no_test_directory": "Create tests/ directory with __init__.py. Add pytest to dev dependencies.",
        "untested_module": "Create test_<module>.py with tests for public functions.",
        "low_coverage": "Add tests for uncovered code paths. Focus on error handling and edge cases.",
        "empty_test": "Implement test logic with assertions. Remove if placeholder no longer needed.",
        "no_tests_in_file": "Add test functions or remove file if not needed.",
        "complex_untested_function": "Ensure function has corresponding test with edge case coverage.",
    }

    for f in findings:
        items.append(DebtItem(
            file=f.file,
            line=f.line,
            category="testing",
            issue=f.issue,
            severity=f.severity,
            description=f.description,
            fix_sketch=fix_sketches.get(f.issue, "Add appropriate test coverage.")
        ))

    return items

def run_maintainability_check(project_path: Path, exclude_dirs: set) -> list[DebtItem]:
    """Run maintainability analysis."""
    items = []
    module = load_analyzer("find_maintainability_issues")
    if not module:
        return items

    findings = module.scan_directory(project_path, exclude_dirs)

    fix_sketches = {
        "missing_module_docstring": 'Add module docstring: """Module description."""',
        "missing_class_docstring": 'Add class docstring describing purpose and usage.',
        "missing_function_docstring": 'Add docstring with Args, Returns, Raises sections.',
        "missing_type_hints": "Add type hints: def func(arg: Type) -> ReturnType:",
        "bad_class_name": "Rename to PascalCase (e.g., MyClassName).",
        "bad_function_name": "Rename to snake_case (e.g., my_function_name).",
        "cryptic_function_name": "Use descriptive name that explains what function does.",
        "cryptic_variable_name": "Use descriptive name that explains what variable holds.",
        "bad_constant_name": "Rename to UPPER_SNAKE_CASE (e.g., MAX_RETRIES).",
        "long_function": "Extract logical sections into smaller helper functions.",
        "too_many_arguments": "Group related args into dataclass/TypedDict config object.",
        "long_file": "Split into focused modules by responsibility.",
    }

    for f in findings:
        items.append(DebtItem(
            file=f.file,
            line=f.line,
            category="maintainability",
            issue=f.issue,
            severity=f.severity,
            description=f.description,
            fix_sketch=fix_sketches.get(f.issue, "Improve code maintainability.")
        ))

    return items

def run_dependency_check(project_path: Path) -> list[DebtItem]:
    """Run dependency health analysis."""
    items = []
    module = load_analyzer("check_dependencies")
    if not module:
        return items

    findings = module.scan_project(project_path, check_env=True)

    fix_sketches = {
        "security_vulnerability": "Update package: pip install --upgrade <package>. Check changelog for breaking changes.",
        "outdated_package": "Update package after reviewing changelog. Run tests after update.",
        "unpinned_dependency": "Pin to specific version: package==1.2.3 for reproducible builds.",
        "loose_version_constraint": "Add upper bound: package>=1.0,<2.0 to prevent breaking updates.",
    }

    for f in findings:
        items.append(DebtItem(
            file=f.file,
            line=f.line,
            category="dependencies",
            issue=f.issue,
            severity=f.severity,
            description=f"{f.package}: {f.description}",
            fix_sketch=fix_sketches.get(f.issue, "Address dependency issue.")
        ))

    return items

def generate_report(items: list[DebtItem], project_path: Path) -> str:
    """Generate prioritized human-readable report."""
    if not items:
        return "✅ No technical debt found! Codebase is clean."

    lines = []
    lines.append("=" * 70)
    lines.append("TECHNICAL DEBT REPORT")
    lines.append(f"Project: {project_path}")
    lines.append("=" * 70)

    # Summary by category and severity
    by_category = defaultdict(list)
    by_severity = defaultdict(list)
    for item in items:
        by_category[item.category].append(item)
        by_severity[item.severity].append(item)

    lines.append("\n📊 EXECUTIVE SUMMARY")
    lines.append("-" * 70)
    lines.append(f"Total debt items: {len(items)}")
    lines.append(f"  🔴 High:   {len(by_severity['high']):>4} (fix immediately)")
    lines.append(f"  🟡 Medium: {len(by_severity['medium']):>4} (fix soon)")
    lines.append(f"  🔵 Low:    {len(by_severity['low']):>4} (fix when convenient)")

    lines.append("\nBy category:")
    category_icons = {
        "security": "🔒",
        "deferred_work": "📝",
        "testing": "🧪",
        "maintainability": "🔧",
        "dependencies": "📦",
    }
    for cat in ["security", "dependencies", "deferred_work", "testing", "maintainability"]:
        if cat in by_category:
            icon = category_icons.get(cat, "•")
            high_count = sum(1 for i in by_category[cat] if i.severity == "high")
            lines.append(f"  {icon} {cat}: {len(by_category[cat])} items ({high_count} high)")

    # Prioritized items - HIGH severity first
    lines.append("\n" + "=" * 70)
    lines.append("🔴 HIGH PRIORITY (Fix Immediately)")
    lines.append("=" * 70)

    high_items = sorted(by_severity["high"], key=lambda x: (x.category, x.file, x.line))
    if high_items:
        current_category = None
        for item in high_items[:30]:  # Limit output
            if item.category != current_category:
                current_category = item.category
                lines.append(f"\n[{current_category.upper()}]")

            lines.append(f"\n  📍 {item.file}:{item.line}")
            lines.append(f"     Issue: {item.issue}")
            lines.append(f"     {item.description}")
            lines.append(f"     💡 Fix: {item.fix_sketch}")

        if len(high_items) > 30:
            lines.append(f"\n  ... and {len(high_items) - 30} more high-priority items")
    else:
        lines.append("\n  ✅ No high-priority items!")

    # Medium priority
    lines.append("\n" + "=" * 70)
    lines.append("🟡 MEDIUM PRIORITY (Fix Soon)")
    lines.append("=" * 70)

    medium_items = sorted(by_severity["medium"], key=lambda x: (x.category, x.file, x.line))
    if medium_items:
        # Group by category for readability
        for category in ["security", "dependencies", "deferred_work", "testing", "maintainability"]:
            cat_items = [i for i in medium_items if i.category == category]
            if not cat_items:
                continue

            lines.append(f"\n[{category.upper()}] - {len(cat_items)} items")
            for item in cat_items[:10]:
                lines.append(f"  • {item.file}:{item.line} - {item.issue}")
                lines.append(f"    {item.description}")
            if len(cat_items) > 10:
                lines.append(f"  ... and {len(cat_items) - 10} more")
    else:
        lines.append("\n  ✅ No medium-priority items!")

    # Low priority - just summary
    lines.append("\n" + "=" * 70)
    lines.append("🔵 LOW PRIORITY (Fix When Convenient)")
    lines.append("=" * 70)

    low_items = by_severity["low"]
    if low_items:
        by_issue = defaultdict(int)
        for item in low_items:
            by_issue[item.issue] += 1

        lines.append(f"\n  {len(low_items)} items total:")
        for issue, count in sorted(by_issue.items(), key=lambda x: -x[1])[:10]:
            lines.append(f"    • {issue}: {count}")
    else:
        lines.append("\n  ✅ No low-priority items!")

    # Recommendations
    lines.append("\n" + "=" * 70)
    lines.append("📋 RECOMMENDED ACTIONS")
    lines.append("=" * 70)

    if by_category.get("security"):
        high_sec = sum(1 for i in by_category["security"] if i.severity == "high")
        if high_sec:
            lines.append(f"\n1. 🔒 SECURITY: Address {high_sec} high-severity security issues immediately")

    if by_category.get("dependencies"):
        vuln_count = sum(1 for i in by_category["dependencies"] if i.issue == "security_vulnerability")
        if vuln_count:
            lines.append(f"\n2. 📦 DEPENDENCIES: Update {vuln_count} packages with known vulnerabilities")

    if by_category.get("deferred_work"):
        fixme_count = sum(1 for i in by_category["deferred_work"] if i.issue in ("FIXME", "BUG", "HACK"))
        if fixme_count:
            lines.append(f"\n3. 📝 DEFERRED: Address {fixme_count} FIXME/BUG/HACK items")

    if by_category.get("testing"):
        untested = sum(1 for i in by_category["testing"] if i.issue == "untested_module")
        if untested:
            lines.append(f"\n4. 🧪 TESTING: Add tests for {untested} untested modules")

    lines.append("\n" + "=" * 70)
    lines.append("For complexity and code smell analysis, use the python-simplifier skill.")
    lines.append("=" * 70)

    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze technical debt in Python projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/project                    # Full analysis
  %(prog)s . --format json                     # JSON output
  %(prog)s . --skip dependencies               # Skip dependency check
  %(prog)s . --only security testing           # Only specific checks
        """
    )
    parser.add_argument("path", type=Path, help="Project directory to analyze")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--skip", nargs="*", default=[],
                        choices=["security", "deferred", "testing", "maintainability", "dependencies"],
                        help="Skip specific checks")
    parser.add_argument("--only", nargs="*", default=[],
                        choices=["security", "deferred", "testing", "maintainability", "dependencies"],
                        help="Run only specific checks")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to exclude")
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if not path.is_dir():
        print("Error: Analysis requires a directory, not a single file", file=sys.stderr)
        sys.exit(1)

    exclude_dirs = set(args.exclude)
    all_items = []

    # Determine which checks to run
    checks = ["security", "deferred", "testing", "maintainability", "dependencies"]
    if args.only:
        checks = args.only
    checks = [c for c in checks if c not in args.skip]

    print("🔍 Analyzing technical debt...", file=sys.stderr)

    if "security" in checks:
        print("  • Security issues...", file=sys.stderr)
        all_items.extend(run_security_check(path, exclude_dirs))

    if "deferred" in checks:
        print("  • Deferred work markers...", file=sys.stderr)
        all_items.extend(run_deferred_work_check(path, exclude_dirs))

    if "testing" in checks:
        print("  • Testing gaps...", file=sys.stderr)
        all_items.extend(run_testing_check(path, exclude_dirs))

    if "maintainability" in checks:
        print("  • Maintainability...", file=sys.stderr)
        all_items.extend(run_maintainability_check(path, exclude_dirs))

    if "dependencies" in checks:
        print("  • Dependencies...", file=sys.stderr)
        all_items.extend(run_dependency_check(path))

    print("✅ Analysis complete!\n", file=sys.stderr)

    if args.format == "json":
        print(json.dumps([asdict(item) for item in all_items], indent=2))
    else:
        print(generate_report(all_items, path))

    # Exit code based on findings
    high_count = sum(1 for i in all_items if i.severity == "high")
    if high_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
