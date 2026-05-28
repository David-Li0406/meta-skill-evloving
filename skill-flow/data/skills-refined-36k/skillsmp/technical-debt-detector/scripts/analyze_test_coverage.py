#!/usr/bin/env python3
"""Analyze test coverage gaps and missing tests."""

import argparse
import ast
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple


class Finding(NamedTuple):
    file: str
    line: int
    issue: str
    severity: str
    description: str
    symbol: str = ""  # Function/class name

def find_test_directory(project_path: Path) -> Path | None:
    """Find the test directory in a project."""
    candidates = ["tests", "test", "spec", "specs"]
    for name in candidates:
        test_dir = project_path / name
        if test_dir.is_dir():
            return test_dir
    return None

def get_source_modules(project_path: Path, exclude_dirs: set[str]) -> dict[str, Path]:
    """Get mapping of module names to their paths."""
    modules = {}
    exclude_dirs = exclude_dirs | {'.git', '__pycache__', '.venv', 'venv', 'node_modules',
                                    '.tox', 'build', 'dist', 'tests', 'test'}

    for filepath in project_path.rglob('*.py'):
        if any(excluded in filepath.parts for excluded in exclude_dirs):
            continue
        if filepath.name.startswith('test_') or filepath.name.endswith('_test.py'):
            continue

        # Get module name from path
        rel_path = filepath.relative_to(project_path)
        module_name = str(rel_path.with_suffix('')).replace('/', '.').replace('\\', '.')
        modules[module_name] = filepath

    return modules

def get_tested_modules(test_dir: Path) -> set[str]:
    """Extract module names that appear to be tested."""
    tested = set()

    for test_file in test_dir.rglob('*.py'):
        if test_file.name.startswith('test_'):
            # test_foo.py likely tests foo
            module_name = test_file.stem[5:]  # Remove 'test_' prefix
            tested.add(module_name)
        elif test_file.name.endswith('_test.py'):
            module_name = test_file.stem[:-5]  # Remove '_test' suffix
            tested.add(module_name)

        # Also check imports in test files
        try:
            content = test_file.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        tested.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        tested.add(node.module.split('.')[0])
        except Exception:
            continue

    return tested

def find_untested_modules(project_path: Path, exclude_dirs: set[str]) -> list[Finding]:
    """Find modules without corresponding test files."""
    findings = []
    test_dir = find_test_directory(project_path)

    if not test_dir:
        findings.append(Finding(
            file=str(project_path),
            line=0,
            issue="no_test_directory",
            severity="high",
            description="No test directory found (expected: tests/ or test/)"
        ))
        return findings

    source_modules = get_source_modules(project_path, exclude_dirs)
    tested_modules = get_tested_modules(test_dir)

    for module_name, filepath in source_modules.items():
        # Check if any part of module path appears in tested modules
        parts = module_name.split('.')
        is_tested = any(part in tested_modules for part in parts)

        if not is_tested and filepath.name not in ('__init__.py', 'setup.py', 'conftest.py'):
            findings.append(Finding(
                file=str(filepath),
                line=1,
                issue="untested_module",
                severity="medium",
                description=f"No test file found for module '{module_name}'"
            ))

    return findings

def find_untested_functions(filepath: Path) -> list[Finding]:
    """Find public functions/methods without tests (heuristic)."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
    except Exception:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private functions, test functions, and dunder methods
            if node.name.startswith('_') and not node.name.startswith('__'):
                continue
            if node.name.startswith('test_'):
                continue

            # Check if function is complex enough to warrant testing
            complexity = sum(1 for _ in ast.walk(node) if isinstance(_, (ast.If, ast.For, ast.While, ast.Try, ast.With)))

            if complexity >= 2:  # Has some control flow
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="complex_untested_function",
                    severity="low",
                    description=f"Function '{node.name}' has {complexity} control flow statements - ensure it's tested",
                    symbol=node.name
                ))

    return findings

def run_coverage_report(project_path: Path) -> list[Finding]:
    """Run pytest-cov and parse results."""
    findings = []

    # Try to run coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=" + str(project_path),
        "--cov-report=json",
        "-q", "--no-header",
        str(project_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(project_path)
        )

        cov_file = project_path / "coverage.json"
        if cov_file.exists():
            data = json.loads(cov_file.read_text())

            for filename, file_data in data.get("files", {}).items():
                coverage_pct = file_data.get("summary", {}).get("percent_covered", 100)
                missing_lines = file_data.get("missing_lines", [])

                if coverage_pct < 50:
                    findings.append(Finding(
                        file=filename,
                        line=missing_lines[0] if missing_lines else 1,
                        issue="low_coverage",
                        severity="high" if coverage_pct < 20 else "medium",
                        description=f"Only {coverage_pct:.0f}% code coverage ({len(missing_lines)} uncovered lines)"
                    ))

            cov_file.unlink()  # Clean up

    except subprocess.TimeoutExpired:
        findings.append(Finding(
            file=str(project_path),
            line=0,
            issue="coverage_timeout",
            severity="low",
            description="Coverage analysis timed out - tests may be slow or hanging"
        ))
    except FileNotFoundError:
        pass  # pytest not installed
    except Exception:
        pass  # Coverage analysis failed

    return findings

def check_test_quality(project_path: Path) -> list[Finding]:
    """Check for test quality issues."""
    findings = []
    test_dir = find_test_directory(project_path)

    if not test_dir:
        return findings

    for test_file in test_dir.rglob('*.py'):
        if not (test_file.name.startswith('test_') or test_file.name.endswith('_test.py')):
            continue

        try:
            content = test_file.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)
        except Exception:
            continue

        test_count = 0
        has_assertions = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_count += 1

                # Check for assertions in test
                for child in ast.walk(node):
                    if isinstance(child, ast.Assert):
                        has_assertions = True
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Attribute):
                            if child.func.attr.startswith('assert'):
                                has_assertions = True

                # Check for empty tests
                body_nodes = [n for n in node.body if not isinstance(n, (ast.Pass, ast.Expr))]
                if len(body_nodes) == 0:
                    findings.append(Finding(
                        file=str(test_file),
                        line=node.lineno,
                        issue="empty_test",
                        severity="medium",
                        description=f"Test '{node.name}' appears to be empty or placeholder"
                    ))

        if test_count == 0:
            findings.append(Finding(
                file=str(test_file),
                line=1,
                issue="no_tests_in_file",
                severity="medium",
                description="Test file contains no test functions"
            ))

    return findings

def scan_directory(path: Path, exclude_dirs: set[str], run_coverage: bool = False) -> list[Finding]:
    """Run all test coverage checks."""
    findings = []
    exclude_dirs = exclude_dirs | {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}

    findings.extend(find_untested_modules(path, exclude_dirs))
    findings.extend(check_test_quality(path))

    if run_coverage:
        findings.extend(run_coverage_report(path))

    # Check complex functions in source files
    source_modules = get_source_modules(path, exclude_dirs)
    for _, filepath in source_modules.items():
        findings.extend(find_untested_functions(filepath))

    return findings

def format_text(findings: list[Finding]) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return "✅ No testing gaps found."

    output = []
    by_issue = defaultdict(list)
    for f in findings:
        by_issue[f.issue].append(f)

    severity_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}

    issue_descriptions = {
        "no_test_directory": "Missing Test Directory",
        "untested_module": "Modules Without Tests",
        "low_coverage": "Low Code Coverage",
        "empty_test": "Empty/Placeholder Tests",
        "no_tests_in_file": "Test Files Without Tests",
        "complex_untested_function": "Complex Functions (verify tested)",
    }

    for issue_type, items in by_issue.items():
        if not items:
            continue

        severity = items[0].severity
        icon = severity_icons.get(severity, "⚪")
        desc = issue_descriptions.get(issue_type, issue_type)

        output.append(f"\n{icon} {desc} ({len(items)} items)")
        output.append("-" * 50)

        for f in sorted(items, key=lambda x: (x.file, x.line)):
            if f.line > 0:
                output.append(f"  {f.file}:{f.line}")
            else:
                output.append(f"  {f.file}")
            output.append(f"    {f.description}")

    output.append(f"\n📊 Summary: {len(findings)} testing gaps found")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Analyze test coverage gaps")
    parser.add_argument("path", type=Path, help="Project directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--run-coverage", action="store_true", help="Run pytest-cov (slower)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to exclude")
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if not path.is_dir():
        print("Error: Test analysis requires a directory, not a single file", file=sys.stderr)
        sys.exit(1)

    findings = scan_directory(path, set(args.exclude), args.run_coverage)

    if args.format == "json":
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        print(format_text(findings))

    if any(f.severity == "high" for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main()
