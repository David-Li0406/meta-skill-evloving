#!/usr/bin/env python3
"""
Dependency Security Checker

Checks project dependencies for known vulnerabilities using multiple sources.
Supports Python (pip), JavaScript (npm), and provides guidance for other ecosystems.

Usage:
    python check_dependencies.py <path> [--format text|json]
    python check_dependencies.py . --format json
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple, Optional


class Vulnerability(NamedTuple):
    package: str
    version: str
    vulnerability_id: str
    severity: str
    description: str
    fix_version: Optional[str]


def find_package_files(path: Path) -> dict:
    """Find dependency manifest files."""
    manifests = {
        "python": [],
        "javascript": [],
        "ruby": [],
        "go": [],
        "rust": [],
        "php": [],
    }

    if path.is_file():
        classify_manifest(path, manifests)
    else:
        for file_path in path.rglob("*"):
            if file_path.is_file():
                classify_manifest(file_path, manifests)

    return manifests


def classify_manifest(file_path: Path, manifests: dict):
    """Classify a file as a package manifest."""
    name = file_path.name.lower()

    # Python
    if name in ("requirements.txt", "requirements-dev.txt", "requirements-prod.txt"):
        manifests["python"].append(file_path)
    elif name == "pyproject.toml":
        manifests["python"].append(file_path)
    elif name == "pipfile.lock":
        manifests["python"].append(file_path)

    # JavaScript
    elif name == "package-lock.json":
        manifests["javascript"].append(file_path)
    elif name == "yarn.lock":
        manifests["javascript"].append(file_path)
    elif name == "package.json" and "package-lock.json" not in [f.name for f in file_path.parent.iterdir()]:
        manifests["javascript"].append(file_path)

    # Ruby
    elif name == "gemfile.lock":
        manifests["ruby"].append(file_path)

    # Go
    elif name == "go.sum":
        manifests["go"].append(file_path)

    # Rust
    elif name == "cargo.lock":
        manifests["rust"].append(file_path)

    # PHP
    elif name == "composer.lock":
        manifests["php"].append(file_path)


def check_python_pip_audit(requirements_path: Path) -> list[Vulnerability]:
    """Check Python dependencies using pip-audit."""
    vulnerabilities = []

    try:
        result = subprocess.run(
            ["pip-audit", "-r", str(requirements_path), "--format", "json"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0 and not result.stdout:
            # pip-audit not installed or error
            return vulnerabilities

        data = json.loads(result.stdout) if result.stdout else []

        for vuln in data:
            fix_versions = vuln.get("fix_versions", [])
            vulnerabilities.append(Vulnerability(
                package=vuln.get("name", "unknown"),
                version=vuln.get("version", "unknown"),
                vulnerability_id=vuln.get("id", "unknown"),
                severity=vuln.get("severity", "unknown"),
                description=vuln.get("description", "")[:200],
                fix_version=fix_versions[0] if fix_versions else None,
            ))

    except FileNotFoundError:
        print("Note: pip-audit not installed. Install with: pip install pip-audit", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("Warning: pip-audit timed out", file=sys.stderr)
    except json.JSONDecodeError:
        print("Warning: Could not parse pip-audit output", file=sys.stderr)
    except Exception as e:
        print(f"Warning: pip-audit error: {e}", file=sys.stderr)

    return vulnerabilities


def check_python_safety(requirements_path: Path) -> list[Vulnerability]:
    """Check Python dependencies using safety."""
    vulnerabilities = []

    try:
        result = subprocess.run(
            ["safety", "check", "-r", str(requirements_path), "--json"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.stdout:
            data = json.loads(result.stdout)
            for vuln in data.get("vulnerabilities", []):
                vulnerabilities.append(Vulnerability(
                    package=vuln.get("package_name", "unknown"),
                    version=vuln.get("analyzed_version", "unknown"),
                    vulnerability_id=vuln.get("vulnerability_id", "unknown"),
                    severity=vuln.get("severity", "unknown"),
                    description=vuln.get("advisory", "")[:200],
                    fix_version=vuln.get("fixed_versions", [None])[0] if vuln.get("fixed_versions") else None,
                ))

    except FileNotFoundError:
        # safety not installed, skip silently (pip-audit is preferred)
        pass
    except Exception as e:
        print(f"Warning: safety error: {e}", file=sys.stderr)

    return vulnerabilities


def check_npm_audit(package_path: Path) -> list[Vulnerability]:
    """Check JavaScript dependencies using npm audit."""
    vulnerabilities = []

    try:
        result = subprocess.run(
            ["npm", "audit", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=package_path.parent,
        )

        if result.stdout:
            data = json.loads(result.stdout)

            # npm audit format varies by version
            vulns = data.get("vulnerabilities", {})
            for pkg_name, vuln_info in vulns.items():
                severity = vuln_info.get("severity", "unknown")
                via = vuln_info.get("via", [])

                # Get first advisory info
                advisory = via[0] if via and isinstance(via[0], dict) else {}

                vulnerabilities.append(Vulnerability(
                    package=pkg_name,
                    version=vuln_info.get("range", "unknown"),
                    vulnerability_id=str(advisory.get("source", "unknown")),
                    severity=severity,
                    description=advisory.get("title", "")[:200] if isinstance(advisory, dict) else str(via)[:200],
                    fix_version=vuln_info.get("fixAvailable", {}).get("version") if isinstance(vuln_info.get("fixAvailable"), dict) else None,
                ))

    except FileNotFoundError:
        print("Note: npm not found", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("Warning: npm audit timed out", file=sys.stderr)
    except json.JSONDecodeError:
        print("Warning: Could not parse npm audit output", file=sys.stderr)
    except Exception as e:
        print(f"Warning: npm audit error: {e}", file=sys.stderr)

    return vulnerabilities


def check_yarn_audit(lock_path: Path) -> list[Vulnerability]:
    """Check JavaScript dependencies using yarn audit."""
    vulnerabilities = []

    try:
        result = subprocess.run(
            ["yarn", "audit", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=lock_path.parent,
        )

        # yarn audit outputs newline-delimited JSON
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get("type") == "auditAdvisory":
                    advisory = data.get("data", {}).get("advisory", {})
                    vulnerabilities.append(Vulnerability(
                        package=advisory.get("module_name", "unknown"),
                        version=advisory.get("vulnerable_versions", "unknown"),
                        vulnerability_id=str(advisory.get("id", "unknown")),
                        severity=advisory.get("severity", "unknown"),
                        description=advisory.get("title", "")[:200],
                        fix_version=advisory.get("patched_versions"),
                    ))
            except json.JSONDecodeError:
                continue

    except FileNotFoundError:
        # yarn not installed, skip
        pass
    except Exception as e:
        print(f"Warning: yarn audit error: {e}", file=sys.stderr)

    return vulnerabilities


def check_dependencies(path: Path) -> dict:
    """Check all dependencies in the given path."""
    manifests = find_package_files(path)
    results = {
        "python": [],
        "javascript": [],
        "other": [],
    }

    # Check Python
    for manifest in manifests["python"]:
        if manifest.name.startswith("requirements"):
            vulns = check_python_pip_audit(manifest)
            if not vulns:
                vulns = check_python_safety(manifest)
            results["python"].extend(vulns)

    # Check JavaScript
    for manifest in manifests["javascript"]:
        if manifest.name == "package-lock.json" or manifest.name == "package.json":
            vulns = check_npm_audit(manifest)
            results["javascript"].extend(vulns)
        elif manifest.name == "yarn.lock":
            vulns = check_yarn_audit(manifest)
            results["javascript"].extend(vulns)

    # Note other ecosystems
    for ecosystem in ["ruby", "go", "rust", "php"]:
        if manifests[ecosystem]:
            results["other"].append({
                "ecosystem": ecosystem,
                "files": [str(f) for f in manifests[ecosystem]],
                "note": f"Manual audit recommended. Use: {get_audit_command(ecosystem)}",
            })

    return results


def get_audit_command(ecosystem: str) -> str:
    """Get the audit command for an ecosystem."""
    commands = {
        "ruby": "bundle audit check",
        "go": "govulncheck ./...",
        "rust": "cargo audit",
        "php": "composer audit",
    }
    return commands.get(ecosystem, "Check ecosystem documentation")


def severity_order(severity: str) -> int:
    """Get numeric order for severity (higher = more severe)."""
    order = {
        "critical": 4,
        "high": 3,
        "moderate": 2,
        "medium": 2,
        "low": 1,
        "info": 0,
    }
    return order.get(severity.lower(), 0)


def format_text_output(results: dict) -> str:
    """Format results as human-readable text."""
    output = []

    all_vulns = results["python"] + results["javascript"]

    if not all_vulns and not results["other"]:
        return "✅ No vulnerabilities found in scanned dependencies."

    if all_vulns:
        # Sort by severity
        sorted_vulns = sorted(all_vulns, key=lambda v: severity_order(v.severity), reverse=True)

        output.append(f"🔴 Found {len(all_vulns)} vulnerable package(s):\n")

        critical = [v for v in sorted_vulns if v.severity.lower() == "critical"]
        high = [v for v in sorted_vulns if v.severity.lower() == "high"]
        medium = [v for v in sorted_vulns if v.severity.lower() in ("medium", "moderate")]
        low = [v for v in sorted_vulns if v.severity.lower() in ("low", "info")]

        def format_vulns(vulns, label, icon):
            if vulns:
                output.append(f"{icon} {label}:")
                for v in vulns:
                    output.append(f"  📦 {v.package} @ {v.version}")
                    output.append(f"     ID: {v.vulnerability_id}")
                    if v.description:
                        output.append(f"     {v.description[:80]}...")
                    if v.fix_version:
                        output.append(f"     Fix: Upgrade to {v.fix_version}")
                output.append("")

        format_vulns(critical, "CRITICAL", "🚨")
        format_vulns(high, "HIGH", "⚠️")
        format_vulns(medium, "MEDIUM", "📋")
        format_vulns(low, "LOW", "ℹ️")

    if results["other"]:
        output.append("📝 Other ecosystems detected (manual check recommended):")
        for item in results["other"]:
            output.append(f"  • {item['ecosystem'].capitalize()}: {item['note']}")
        output.append("")

    output.append("─" * 50)

    if all_vulns:
        critical_count = len([v for v in all_vulns if v.severity.lower() == "critical"])
        high_count = len([v for v in all_vulns if v.severity.lower() == "high"])
        output.append(f"Summary: {critical_count} critical, {high_count} high, {len(all_vulns) - critical_count - high_count} other")
        output.append("\n🔧 Remediation:")
        output.append("  1. Update vulnerable packages to fixed versions")
        output.append("  2. If no fix available, consider alternatives")
        output.append("  3. Add exceptions only with documented risk acceptance")

    return "\n".join(output)


def format_json_output(results: dict) -> str:
    """Format results as JSON."""
    all_vulns = results["python"] + results["javascript"]

    return json.dumps({
        "total": len(all_vulns),
        "critical": len([v for v in all_vulns if v.severity.lower() == "critical"]),
        "high": len([v for v in all_vulns if v.severity.lower() == "high"]),
        "medium": len([v for v in all_vulns if v.severity.lower() in ("medium", "moderate")]),
        "low": len([v for v in all_vulns if v.severity.lower() in ("low", "info")]),
        "vulnerabilities": {
            "python": [v._asdict() for v in results["python"]],
            "javascript": [v._asdict() for v in results["javascript"]],
        },
        "other_ecosystems": results["other"],
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Check project dependencies for known vulnerabilities"
    )
    parser.add_argument("path", help="File or directory to scan")
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

    # Check dependencies
    results = check_dependencies(path)

    # Output
    if args.format == "json":
        print(format_json_output(results))
    else:
        print(format_text_output(results))

    # Exit code based on critical/high vulnerabilities
    all_vulns = results["python"] + results["javascript"]
    critical_or_high = len([
        v for v in all_vulns
        if v.severity.lower() in ("critical", "high")
    ])
    sys.exit(1 if critical_or_high > 0 else 0)


if __name__ == "__main__":
    main()
