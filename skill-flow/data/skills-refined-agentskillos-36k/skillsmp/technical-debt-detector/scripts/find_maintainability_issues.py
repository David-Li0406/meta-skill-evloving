#!/usr/bin/env python3
"""Find maintainability issues: missing docstrings, type hints, poor naming."""

import argparse
import ast
import json
import re
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
    symbol: str = ""

# Naming conventions
NAMING_PATTERNS = {
    "class": re.compile(r'^[A-Z][a-zA-Z0-9]*$'),  # PascalCase
    "function": re.compile(r'^[a-z_][a-z0-9_]*$'),  # snake_case
    "constant": re.compile(r'^[A-Z][A-Z0-9_]*$'),  # UPPER_SNAKE_CASE
    "variable": re.compile(r'^[a-z_][a-z0-9_]*$'),  # snake_case
}

# Common abbreviations that are too cryptic
CRYPTIC_NAMES = {'x', 'y', 'z', 'a', 'b', 'c', 'i', 'j', 'k', 'n', 'm', 'tmp', 'temp', 'foo', 'bar', 'baz', 'qux'}
# ...but allow in specific contexts (loop vars, coordinates, math)
ALLOWED_SHORT_NAMES = {'i', 'j', 'k', 'n', 'x', 'y', 'z', '_'}

def check_docstrings(filepath: Path) -> list[Finding]:
    """Check for missing docstrings."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
    except Exception:
        return findings

    # Check module docstring
    if not ast.get_docstring(tree):
        findings.append(Finding(
            file=str(filepath),
            line=1,
            issue="missing_module_docstring",
            severity="low",
            description="Module missing docstring"
        ))

    for node in ast.walk(tree):
        # Check class docstrings
        if isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="missing_class_docstring",
                    severity="medium",
                    description=f"Class '{node.name}' missing docstring",
                    symbol=node.name
                ))

        # Check function docstrings (only public functions)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith('_') and not node.name.startswith('__'):
                continue  # Skip private functions
            if node.name.startswith('test_'):
                continue  # Skip test functions

            if not ast.get_docstring(node):
                # Only flag if function has arguments or is complex
                has_args = len(node.args.args) > 1 or (len(node.args.args) == 1 and node.args.args[0].arg != 'self')
                is_complex = len(node.body) > 3

                if has_args or is_complex:
                    findings.append(Finding(
                        file=str(filepath),
                        line=node.lineno,
                        issue="missing_function_docstring",
                        severity="medium",
                        description=f"Function '{node.name}' missing docstring",
                        symbol=node.name
                    ))

    return findings

def check_type_hints(filepath: Path) -> list[Finding]:
    """Check for missing type hints."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
    except Exception:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith('_') and not node.name.startswith('__'):
                continue
            if node.name.startswith('test_'):
                continue

            missing_hints = []

            # Check return type
            if node.returns is None and node.name != '__init__':
                missing_hints.append("return type")

            # Check argument types
            for arg in node.args.args:
                if arg.arg in ('self', 'cls'):
                    continue
                if arg.annotation is None:
                    missing_hints.append(f"'{arg.arg}'")

            if missing_hints:
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="missing_type_hints",
                    severity="low",
                    description=f"Function '{node.name}' missing type hints for: {', '.join(missing_hints)}",
                    symbol=node.name
                ))

    return findings

def check_naming(filepath: Path) -> list[Finding]:
    """Check for naming convention violations."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
    except Exception:
        return findings

    for node in ast.walk(tree):
        # Check class names
        if isinstance(node, ast.ClassDef):
            if not NAMING_PATTERNS["class"].match(node.name):
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="bad_class_name",
                    severity="medium",
                    description=f"Class '{node.name}' should use PascalCase",
                    symbol=node.name
                ))

        # Check function names
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith('__') and node.name.endswith('__'):
                continue  # Dunder methods
            if not NAMING_PATTERNS["function"].match(node.name):
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="bad_function_name",
                    severity="medium",
                    description=f"Function '{node.name}' should use snake_case",
                    symbol=node.name
                ))

            # Check for overly short function names
            if len(node.name) < 3 and node.name not in ALLOWED_SHORT_NAMES:
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="cryptic_function_name",
                    severity="medium",
                    description=f"Function '{node.name}' is too cryptic - use descriptive name",
                    symbol=node.name
                ))

        # Check for cryptic variable names in assignments (excluding loop vars)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    if name in CRYPTIC_NAMES and name not in ALLOWED_SHORT_NAMES:
                        findings.append(Finding(
                            file=str(filepath),
                            line=node.lineno,
                            issue="cryptic_variable_name",
                            severity="low",
                            description=f"Variable '{name}' is too cryptic - use descriptive name",
                            symbol=name
                        ))

        # Check module-level constants (UPPER_CASE)
        if isinstance(node, ast.Assign):
            # Only at module level
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    # If it looks like a constant (all caps) but isn't proper format
                    if name.isupper() and not NAMING_PATTERNS["constant"].match(name):
                        findings.append(Finding(
                            file=str(filepath),
                            line=node.lineno,
                            issue="bad_constant_name",
                            severity="low",
                            description=f"Constant '{name}' should use UPPER_SNAKE_CASE",
                            symbol=name
                        ))

    return findings

def check_complexity_indicators(filepath: Path) -> list[Finding]:
    """Check for maintainability issues that indicate complexity."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
        lines = content.splitlines()
    except Exception:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check function length
            end_line = getattr(node, 'end_lineno', node.lineno + len(node.body))
            func_length = end_line - node.lineno

            if func_length > 50:
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="long_function",
                    severity="medium",
                    description=f"Function '{node.name}' is {func_length} lines - consider splitting",
                    symbol=node.name
                ))

            # Check argument count
            total_args = (
                len(node.args.args) +
                len(node.args.kwonlyargs) +
                (1 if node.args.vararg else 0) +
                (1 if node.args.kwarg else 0)
            )
            # Exclude 'self' and 'cls'
            if node.args.args and node.args.args[0].arg in ('self', 'cls'):
                total_args -= 1

            if total_args > 5:
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="too_many_arguments",
                    severity="medium",
                    description=f"Function '{node.name}' has {total_args} arguments - consider using a config object",
                    symbol=node.name
                ))

    # Check file length
    if len(lines) > 500:
        findings.append(Finding(
            file=str(filepath),
            line=1,
            issue="long_file",
            severity="low",
            description=f"File is {len(lines)} lines - consider splitting into modules"
        ))

    return findings

def scan_file(filepath: Path) -> list[Finding]:
    """Run all maintainability checks on a file."""
    findings = []
    findings.extend(check_docstrings(filepath))
    findings.extend(check_type_hints(filepath))
    findings.extend(check_naming(filepath))
    findings.extend(check_complexity_indicators(filepath))
    return findings

def scan_directory(path: Path, exclude_dirs: set[str]) -> list[Finding]:
    """Scan directory for maintainability issues."""
    findings = []
    exclude_dirs = exclude_dirs | {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.tox', 'build', 'dist'}

    for filepath in path.rglob('*.py'):
        if any(excluded in filepath.parts for excluded in exclude_dirs):
            continue
        findings.extend(scan_file(filepath))

    return findings

def format_text(findings: list[Finding]) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return "✅ No maintainability issues found."

    output = []
    by_issue = defaultdict(list)
    for f in findings:
        by_issue[f.issue].append(f)

    severity_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}

    issue_order = [
        ("missing_class_docstring", "Missing Class Docstrings"),
        ("missing_function_docstring", "Missing Function Docstrings"),
        ("missing_module_docstring", "Missing Module Docstrings"),
        ("missing_type_hints", "Missing Type Hints"),
        ("bad_class_name", "Class Naming Issues"),
        ("bad_function_name", "Function Naming Issues"),
        ("cryptic_function_name", "Cryptic Function Names"),
        ("cryptic_variable_name", "Cryptic Variable Names"),
        ("bad_constant_name", "Constant Naming Issues"),
        ("long_function", "Long Functions"),
        ("too_many_arguments", "Too Many Arguments"),
        ("long_file", "Long Files"),
    ]

    for issue_type, desc in issue_order:
        items = by_issue.get(issue_type, [])
        if not items:
            continue

        severity = items[0].severity
        icon = severity_icons.get(severity, "⚪")

        output.append(f"\n{icon} {desc} ({len(items)} items)")
        output.append("-" * 50)

        for f in sorted(items, key=lambda x: (x.file, x.line))[:20]:  # Limit output
            output.append(f"  {f.file}:{f.line}")
            output.append(f"    {f.description}")

        if len(items) > 20:
            output.append(f"  ... and {len(items) - 20} more")

    output.append(f"\n📊 Summary: {len(findings)} maintainability issues found")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Find maintainability issues")
    parser.add_argument("path", type=Path, help="File or directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--check", choices=["docstrings", "types", "naming", "all"], default="all")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to exclude")
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        findings = scan_file(path)
    else:
        findings = scan_directory(path, set(args.exclude))

    # Filter by check type
    if args.check != "all":
        check_mapping = {
            "docstrings": ["missing_module_docstring", "missing_class_docstring", "missing_function_docstring"],
            "types": ["missing_type_hints"],
            "naming": ["bad_class_name", "bad_function_name", "cryptic_function_name", "cryptic_variable_name", "bad_constant_name"],
        }
        allowed_issues = check_mapping.get(args.check, [])
        findings = [f for f in findings if f.issue in allowed_issues]

    if args.format == "json":
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        print(format_text(findings))

if __name__ == "__main__":
    main()
