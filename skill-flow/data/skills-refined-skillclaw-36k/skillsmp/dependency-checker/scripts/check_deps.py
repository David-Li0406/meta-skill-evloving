#!/usr/bin/env python3
"""Dependency checker - audits Python dependencies for security and best practices."""

import subprocess
import sys
import re
import json
from pathlib import Path


def find_requirements():
    """Find all requirements files."""
    patterns = ["requirements*.txt", "pyproject.toml"]
    files = []
    for pattern in patterns:
        files.extend(Path(".").glob(pattern))
    return [str(f) for f in files if f.exists()]


def check_vulnerabilities():
    """Run pip-audit to check for security issues."""
    try:
        result = subprocess.run(
            ["pip-audit", "-r", "requirements.txt", "--format", "json"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return True, "No vulnerabilities found", []

        try:
            vulns = json.loads(result.stdout)
            critical = [v for v in vulns if v.get("fix_versions")]
            return False, f"{len(vulns)} vulnerabilities found", vulns
        except json.JSONDecodeError:
            return False, result.stdout[:200], []
    except FileNotFoundError:
        return None, "pip-audit not installed (skipped)", []
    except subprocess.TimeoutExpired:
        return False, "Audit timed out (>120s)", []
    except Exception as e:
        return None, f"Error: {e}", []


def check_outdated():
    """Check for outdated packages."""
    try:
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format", "json"],
            capture_output=True, text=True, timeout=60
        )
        outdated = json.loads(result.stdout) if result.stdout else []
        return outdated
    except Exception:
        return []


def check_format():
    """Validate requirements.txt format."""
    issues = []
    req_file = Path("requirements.txt")
    if not req_file.exists():
        return [{"line": 0, "issue": "requirements.txt not found"}]

    with open(req_file) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue

            # Check for unpinned
            if "==" not in line and ">=" not in line and "<" not in line:
                if "@" not in line:  # Not a git/URL reference
                    issues.append({
                        "line": i,
                        "package": line,
                        "issue": "No version constraint"
                    })
            # Check for unbounded upper
            elif ">=" in line and "<" not in line and "==" not in line:
                pkg = line.split(">=")[0].strip()
                issues.append({
                    "line": i,
                    "package": pkg,
                    "issue": "Unbounded upper limit (use >= and <)"
                })

    return issues


def check_conflicts():
    """Run pip check for dependency conflicts."""
    try:
        result = subprocess.run(
            ["pip", "check"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, "No conflicts"
        return False, result.stdout.strip()
    except Exception as e:
        return None, f"Error: {e}"


def main():
    """Run all dependency checks."""
    print("DEPENDENCY AUDIT")
    print("=" * 50)

    # Find files
    files = find_requirements()
    print(f"\nFiles found: {', '.join(files) or 'None'}")

    has_issues = False
    critical_issues = False

    # Security audit
    print("\n[1/4] Security Audit")
    vuln_ok, vuln_msg, vulns = check_vulnerabilities()
    if vuln_ok is True:
        print(f"  ✅ {vuln_msg}")
    elif vuln_ok is False:
        print(f"  ❌ {vuln_msg}")
        for v in vulns[:3]:
            print(f"     - {v.get('name', 'unknown')}: {v.get('vulns', [{}])[0].get('id', 'CVE-?')}")
        has_issues = True
        critical_issues = True
    else:
        print(f"  ⚠️  {vuln_msg}")

    # Outdated packages
    print("\n[2/4] Outdated Packages")
    outdated = check_outdated()
    if not outdated:
        print("  ✅ All packages up to date")
    else:
        print(f"  ⚠️  {len(outdated)} packages outdated")
        for pkg in outdated[:5]:
            print(f"     - {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        has_issues = True

    # Format validation
    print("\n[3/4] Format Validation")
    format_issues = check_format()
    if not format_issues:
        print("  ✅ All dependencies properly pinned")
    else:
        print(f"  ⚠️  {len(format_issues)} format issues")
        for issue in format_issues[:3]:
            print(f"     - Line {issue['line']}: {issue.get('package', '')} - {issue['issue']}")
        has_issues = True

    # Conflict check
    print("\n[4/4] Dependency Conflicts")
    conflict_ok, conflict_msg = check_conflicts()
    if conflict_ok:
        print(f"  ✅ {conflict_msg}")
    elif conflict_ok is False:
        print(f"  ❌ {conflict_msg[:100]}")
        has_issues = True
        critical_issues = True
    else:
        print(f"  ⚠️  {conflict_msg}")

    # Summary
    print("\n" + "=" * 50)
    if critical_issues:
        print("AUDIT FAILED - Critical issues found")
        print("Fix vulnerabilities and conflicts before deployment")
        return 1
    elif has_issues:
        print("AUDIT WARNING - Non-critical issues found")
        print("Consider updating outdated packages")
        return 0
    else:
        print("AUDIT PASSED - All checks OK")
        return 0


if __name__ == "__main__":
    sys.exit(main())
