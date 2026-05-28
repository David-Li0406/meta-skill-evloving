#!/usr/bin/env python3
"""Find security issues in Python code using bandit and custom checks."""

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
    confidence: str
    description: str
    cwe: str = ""

CUSTOM_CHECKS = {
    "hardcoded_password": {
        "patterns": ["password", "passwd", "pwd", "secret", "api_key", "apikey", "token", "auth"],
        "severity": "high",
        "description": "Possible hardcoded credential"
    },
    "debug_enabled": {
        "patterns": ["DEBUG = True", "debug=True", "DEBUG=True"],
        "severity": "medium",
        "description": "Debug mode may be enabled in production"
    },
}

def run_bandit(path: Path, exclude_dirs: list[str]) -> list[Finding]:
    """Run bandit security scanner."""
    findings = []

    cmd = [
        sys.executable, "-m", "bandit",
        "-r", str(path),
        "-f", "json",
        "-q",
        "--exclude", ",".join(exclude_dirs + [".venv", "venv", "test", "tests", "__pycache__"])
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            data = json.loads(result.stdout)
            for issue in data.get("results", []):
                findings.append(Finding(
                    file=issue["filename"],
                    line=issue["line_number"],
                    issue=issue["test_id"],
                    severity=issue["issue_severity"].lower(),
                    confidence=issue["issue_confidence"].lower(),
                    description=issue["issue_text"],
                    cwe=issue.get("issue_cwe", {}).get("id", "")
                ))
    except FileNotFoundError:
        print("⚠️  bandit not installed. Install with: pip install bandit", file=sys.stderr)
    except json.JSONDecodeError:
        pass  # No issues found or error

    return findings

def check_hardcoded_secrets(filepath: Path) -> list[Finding]:
    """Check for hardcoded secrets and credentials."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
    except Exception:
        return findings

    for node in ast.walk(tree):
        # Check assignments like PASSWORD = "something"
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name_lower = target.id.lower()
                    for pattern in CUSTOM_CHECKS["hardcoded_password"]["patterns"]:
                        if pattern in name_lower:
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                if len(node.value.value) > 0:  # Non-empty string
                                    findings.append(Finding(
                                        file=str(filepath),
                                        line=node.lineno,
                                        issue="hardcoded_secret",
                                        severity="high",
                                        confidence="medium",
                                        description=f"Possible hardcoded secret in '{target.id}'"
                                    ))
                            break

        # Check function calls with password-like kwargs
        if isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg:
                    arg_lower = keyword.arg.lower()
                    for pattern in CUSTOM_CHECKS["hardcoded_password"]["patterns"]:
                        if pattern in arg_lower:
                            if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                                if len(keyword.value.value) > 0:
                                    findings.append(Finding(
                                        file=str(filepath),
                                        line=node.lineno,
                                        issue="hardcoded_secret_arg",
                                        severity="high",
                                        confidence="medium",
                                        description=f"Possible hardcoded secret in argument '{keyword.arg}'"
                                    ))
                            break

    return findings

def check_unsafe_patterns(filepath: Path) -> list[Finding]:
    """Check for unsafe code patterns."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
    except Exception:
        return findings

    for node in ast.walk(tree):
        # Check for eval/exec usage
        if isinstance(node, ast.Call):
            func_name = None
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr

            if func_name in ('eval', 'exec'):
                findings.append(Finding(
                    file=str(filepath),
                    line=node.lineno,
                    issue="dangerous_function",
                    severity="high",
                    confidence="high",
                    description=f"Use of {func_name}() can execute arbitrary code"
                ))

            # Check for shell=True in subprocess
            if func_name in ('run', 'call', 'Popen', 'check_output', 'check_call'):
                for keyword in node.keywords:
                    if keyword.arg == 'shell':
                        if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            findings.append(Finding(
                                file=str(filepath),
                                line=node.lineno,
                                issue="shell_injection",
                                severity="high",
                                confidence="medium",
                                description="subprocess with shell=True may be vulnerable to injection"
                            ))

            # Check for pickle.loads
            if func_name == 'loads':
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'pickle':
                        findings.append(Finding(
                            file=str(filepath),
                            line=node.lineno,
                            issue="unsafe_deserialization",
                            severity="high",
                            confidence="high",
                            description="pickle.loads() can execute arbitrary code on untrusted data"
                        ))

        # Check for assert statements (removed in optimized code)
        if isinstance(node, ast.Assert):
            findings.append(Finding(
                file=str(filepath),
                line=node.lineno,
                issue="assert_used",
                severity="low",
                confidence="high",
                description="Assert statements are removed with -O flag; don't use for security checks"
            ))

    return findings

def scan_directory(path: Path, exclude_dirs: set[str]) -> list[Finding]:
    """Scan directory with all security checks."""
    findings = []
    exclude_dirs = exclude_dirs | {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.tox', 'build', 'dist'}

    # Run bandit on entire directory
    findings.extend(run_bandit(path, list(exclude_dirs)))

    # Run custom checks on each file
    for filepath in path.rglob('*.py'):
        if any(excluded in filepath.parts for excluded in exclude_dirs):
            continue
        findings.extend(check_hardcoded_secrets(filepath))
        findings.extend(check_unsafe_patterns(filepath))

    # Deduplicate (bandit may catch same issues as custom checks)
    seen = set()
    unique = []
    for f in findings:
        key = (f.file, f.line, f.issue)
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique

def format_text(findings: list[Finding]) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return "✅ No security issues found."

    output = []
    by_severity = defaultdict(list)
    for f in findings:
        by_severity[f.severity].append(f)

    severity_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}

    for severity in ["high", "medium", "low"]:
        items = by_severity[severity]
        if not items:
            continue

        output.append(f"\n{severity_icons[severity]} {severity.upper()} SEVERITY ({len(items)} issues)")
        output.append("-" * 50)

        for f in sorted(items, key=lambda x: (x.file, x.line)):
            cwe_str = f" [CWE-{f.cwe}]" if f.cwe else ""
            output.append(f"  {f.file}:{f.line}{cwe_str}")
            output.append(f"    {f.issue}: {f.description}")
            if f.confidence != "high":
                output.append(f"    (confidence: {f.confidence})")

    output.append(f"\n📊 Summary: {len(findings)} security issues found")
    high_count = len(by_severity["high"])
    if high_count:
        output.append(f"   ⚠️  {high_count} HIGH severity issues require immediate attention")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Find security issues in Python code")
    parser.add_argument("path", type=Path, help="File or directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--severity", choices=["high", "medium", "low"], help="Filter by minimum severity")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to exclude")
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        findings = check_hardcoded_secrets(path) + check_unsafe_patterns(path)
        # Also run bandit on single file
        findings.extend(run_bandit(path, []))
    else:
        findings = scan_directory(path, set(args.exclude))

    if args.severity:
        severity_order = {"high": 0, "medium": 1, "low": 2}
        max_level = severity_order[args.severity]
        findings = [f for f in findings if severity_order[f.severity] <= max_level]

    if args.format == "json":
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        print(format_text(findings))

    if any(f.severity == "high" for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main()
