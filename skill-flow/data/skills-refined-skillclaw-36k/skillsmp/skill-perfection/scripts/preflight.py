#!/usr/bin/env python3
"""
Skill Preflight - Python Syntax Validator

Quick syntax check for Python code blocks in skill markdown files.
This is ADVISORY ONLY - if results are confusing, ignore them.

Usage:
    uv run python preflight.py <skill.md>
    uv run python preflight.py <skill.md> --no-urls
    uv run python preflight.py <skill.md> --json

Limitations:
    - Only validates Python code blocks (```python)
    - Other languages are skipped, not validated
    - If this script produces confusing output, ignore it entirely
"""

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Optional dependencies - graceful degradation
try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class Issue:
    severity: str  # critical, medium, low
    location: str
    message: str


@dataclass
class Result:
    skill_path: str
    passed: bool
    issues: list[Issue] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "skill_path": self.skill_path,
            "passed": self.passed,
            "issues": [{"severity": i.severity, "location": i.location, "message": i.message} for i in self.issues],
            "stats": self.stats,
        }


def extract_python_blocks(content: str) -> list[tuple[str, int]]:
    """Extract Python code blocks with their starting line numbers."""
    blocks = []
    lines = content.split("\n")
    in_block = False
    is_python = False
    block_code = []
    block_start = 0

    for i, line in enumerate(lines, 1):
        if line.startswith("```") and not in_block:
            in_block = True
            lang = line[3:].strip().lower().split()[0] if line[3:].strip() else ""
            is_python = lang in ("python", "python3", "py")
            block_code = []
            block_start = i + 1
        elif line.startswith("```") and in_block:
            if is_python and block_code:
                blocks.append(("\n".join(block_code), block_start))
            in_block = False
            is_python = False
        elif in_block and is_python:
            block_code.append(line)

    return blocks


def check_python_syntax(code: str, line_start: int) -> Optional[Issue]:
    """Check Python syntax using ast.parse."""
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        actual_line = line_start + (e.lineno or 1) - 1
        snippet = e.text.strip()[:40] if e.text else ""
        return Issue(
            severity="critical",
            location=f"line {actual_line}",
            message=f"Python syntax error: {e.msg}" + (f" near `{snippet}`" if snippet else "")
        )


def check_markdown_structure(content: str) -> list[Issue]:
    """Check for unclosed code blocks."""
    issues = []
    fence_count = content.count("\n```")
    if fence_count % 2 != 0:
        issues.append(Issue(
            severity="critical",
            location="file",
            message="Unclosed code block (mismatched ``` fences)"
        ))
    return issues


def check_urls(content: str, timeout: float = 5.0) -> list[Issue]:
    """Check URL accessibility. Returns empty list if httpx not available."""
    if not HAS_HTTPX:
        return []

    import asyncio

    url_pattern = r'https?://[^\s\)\]>"\'\`]+'
    urls = []
    for i, line in enumerate(content.split("\n"), 1):
        if not line.strip().startswith("```"):
            for match in re.finditer(url_pattern, line):
                urls.append((match.group().rstrip(".,;:)"), i))

    if not urls:
        return []

    issues = []

    async def check_all():
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            for url, line in urls:
                try:
                    r = await client.head(url)
                    if r.status_code >= 400:
                        issues.append(Issue("medium", f"line {line}", f"URL returned {r.status_code}: {url[:50]}..."))
                except Exception:
                    issues.append(Issue("low", f"line {line}", f"URL unreachable: {url[:50]}..."))

    try:
        asyncio.run(check_all())
    except Exception:
        pass  # URL checking failed, not critical

    return issues


def run_preflight(skill_path: str, check_url_flag: bool = True) -> Result:
    """Run preflight checks. Returns Result with passed=True if no critical issues."""
    path = Path(skill_path)

    if not path.exists():
        return Result(skill_path, False, [Issue("critical", "file", f"File not found: {skill_path}")])

    try:
        content = path.read_text()
    except Exception as e:
        return Result(skill_path, False, [Issue("critical", "file", f"Cannot read file: {e}")])

    python_blocks = extract_python_blocks(content)
    issues = []

    # Markdown structure
    issues.extend(check_markdown_structure(content))

    # Python syntax
    for code, line_start in python_blocks:
        issue = check_python_syntax(code, line_start)
        if issue:
            issues.append(issue)

    # URLs (optional)
    if check_url_flag:
        issues.extend(check_urls(content))

    # Sort by severity
    severity_order = {"critical": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda i: severity_order.get(i.severity, 99))

    # Passed if no critical issues
    has_critical = any(i.severity == "critical" for i in issues)

    stats = {
        "python_blocks": len(python_blocks),
        "issues_found": len(issues),
        "critical": sum(1 for i in issues if i.severity == "critical"),
    }

    return Result(skill_path, not has_critical, issues, stats)


def print_result(result: Result, as_json: bool = False):
    """Print result to stdout."""
    if as_json:
        print(json.dumps(result.to_dict(), indent=2))
        return

    status = "✅ PASSED" if result.passed else "❌ FAILED"
    print(f"\nPreflight: {result.skill_path}")
    print(f"Status: {status}")
    print(f"Python blocks checked: {result.stats.get('python_blocks', 0)}")

    if result.issues:
        print(f"\nIssues ({len(result.issues)}):")
        for issue in result.issues:
            icon = {"critical": "🔴", "medium": "🟡", "low": "🔵"}.get(issue.severity, "⚪")
            print(f"  {icon} [{issue.severity}] {issue.location}: {issue.message}")
    else:
        print("\n✨ No issues found")

    if result.passed:
        print("\n→ Preflight passed. Proceed with LLM verification.")
    else:
        print("\n→ Fix critical issues, or ignore preflight if output seems wrong.")


def main():
    parser = argparse.ArgumentParser(description="Python syntax check for skill files (advisory only)")
    parser.add_argument("skill_path", help="Path to skill markdown file")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--no-urls", action="store_true", help="Skip URL checks")

    args = parser.parse_args()

    try:
        result = run_preflight(args.skill_path, check_url_flag=not args.no_urls)
        print_result(result, as_json=args.json)
        sys.exit(0 if result.passed else 1)
    except Exception as e:
        # Script itself failed - print error and exit gracefully
        if args.json:
            print(json.dumps({"error": str(e), "suggestion": "Ignore preflight, proceed with LLM verification"}))
        else:
            print(f"\n⚠️  Preflight script error: {e}")
            print("→ Ignore preflight and proceed with LLM verification.")
        sys.exit(2)  # Distinct exit code for script failure


if __name__ == "__main__":
    main()
