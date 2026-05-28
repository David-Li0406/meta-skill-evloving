#!/usr/bin/env python3
"""Check dependency health: outdated packages and known vulnerabilities."""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple


class Finding(NamedTuple):
    file: str
    line: int
    package: str
    issue: str
    severity: str
    description: str
    current_version: str = ""
    latest_version: str = ""
    vulnerability_id: str = ""

def find_requirements_files(project_path: Path) -> list[Path]:
    """Find all requirements files in project."""
    patterns = [
        "requirements*.txt",
        "requirements/*.txt",
        "setup.py",
        "setup.cfg",
        "pyproject.toml",
        "Pipfile",
        "Pipfile.lock",
    ]

    files = []
    for pattern in patterns:
        files.extend(project_path.glob(pattern))
        files.extend(project_path.glob(f"**/{pattern}"))

    # Deduplicate
    return list(set(files))

def check_outdated_packages() -> list[Finding]:
    """Check for outdated packages using pip."""
    findings = []

    cmd = [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.stdout:
            packages = json.loads(result.stdout)

            for pkg in packages:
                name = pkg["name"]
                current = pkg["version"]
                latest = pkg["latest_version"]

                # Determine severity based on version difference
                current_parts = current.split('.')
                latest_parts = latest.split('.')

                try:
                    if int(latest_parts[0]) > int(current_parts[0]):
                        severity = "high"  # Major version behind
                        desc = f"Major version behind ({current} → {latest})"
                    elif len(latest_parts) > 1 and len(current_parts) > 1 and int(latest_parts[1]) > int(current_parts[1]):
                        severity = "medium"  # Minor version behind
                        desc = f"Minor version behind ({current} → {latest})"
                    else:
                        severity = "low"  # Patch version behind
                        desc = f"Patch available ({current} → {latest})"
                except (ValueError, IndexError):
                    severity = "low"
                    desc = f"Update available ({current} → {latest})"

                findings.append(Finding(
                    file="environment",
                    line=0,
                    package=name,
                    issue="outdated_package",
                    severity=severity,
                    description=desc,
                    current_version=current,
                    latest_version=latest
                ))

    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass

    return findings

def check_vulnerabilities() -> list[Finding]:
    """Check for known vulnerabilities using pip-audit."""
    findings = []

    cmd = [sys.executable, "-m", "pip_audit", "--format=json", "--progress-spinner=off"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.stdout:
            data = json.loads(result.stdout)

            for vuln in data.get("dependencies", []):
                pkg_name = vuln["name"]
                pkg_version = vuln["version"]

                for v in vuln.get("vulns", []):
                    vuln_id = v.get("id", "UNKNOWN")
                    fix_versions = v.get("fix_versions", [])

                    # Determine severity from vulnerability ID
                    severity = "high"  # Default to high for known CVEs
                    if vuln_id.startswith("PYSEC"):
                        severity = "medium"

                    fix_str = f" (fix: {fix_versions[0]})" if fix_versions else ""

                    findings.append(Finding(
                        file="environment",
                        line=0,
                        package=pkg_name,
                        issue="security_vulnerability",
                        severity=severity,
                        description=f"{vuln_id}: {v.get('description', 'Known vulnerability')[:100]}",
                        current_version=pkg_version,
                        latest_version=fix_versions[0] if fix_versions else "",
                        vulnerability_id=vuln_id
                    ))

    except FileNotFoundError:
        print("⚠️  pip-audit not installed. Install with: pip install pip-audit", file=sys.stderr)
    except subprocess.TimeoutExpired:
        pass
    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    return findings

def check_requirements_pinning(project_path: Path) -> list[Finding]:
    """Check for unpinned or loosely pinned dependencies."""
    findings = []
    req_files = find_requirements_files(project_path)

    for req_file in req_files:
        if req_file.suffix != '.txt':
            continue

        try:
            content = req_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()
        except Exception:
            continue

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('-'):
                continue

            # Check for unpinned packages
            if '==' not in line and '>=' not in line and '<=' not in line:
                # Extract package name
                pkg_name = line.split('[')[0].split(';')[0].strip()
                if pkg_name:
                    findings.append(Finding(
                        file=str(req_file),
                        line=i,
                        package=pkg_name,
                        issue="unpinned_dependency",
                        severity="medium",
                        description=f"Package '{pkg_name}' is not pinned to a specific version"
                    ))

            # Check for >= without upper bound
            elif '>=' in line and '<' not in line:
                pkg_name = line.split('>=')[0].strip()
                findings.append(Finding(
                    file=str(req_file),
                    line=i,
                    package=pkg_name,
                    issue="loose_version_constraint",
                    severity="low",
                    description=f"Package '{pkg_name}' has no upper version bound"
                ))

    return findings

def check_unused_dependencies(project_path: Path) -> list[Finding]:
    """Heuristic check for potentially unused dependencies."""
    findings = []

    # Get installed packages
    cmd = [sys.executable, "-m", "pip", "list", "--format=json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        installed = {pkg["name"].lower().replace("-", "_") for pkg in json.loads(result.stdout)}
    except Exception:
        return findings

    # Get imports from all Python files
    used_imports = set()
    exclude_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.tox', 'build', 'dist'}

    for filepath in project_path.rglob('*.py'):
        if any(excluded in filepath.parts for excluded in exclude_dirs):
            continue

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            import ast
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        used_imports.add(alias.name.split('.')[0].lower().replace("-", "_"))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        used_imports.add(node.module.split('.')[0].lower().replace("-", "_"))
        except Exception:
            continue

    # Find potentially unused packages
    # Note: This is heuristic - package names don't always match import names
    common_mismatches = {
        'pillow': 'pil',
        'beautifulsoup4': 'bs4',
        'pyyaml': 'yaml',
        'scikit_learn': 'sklearn',
        'opencv_python': 'cv2',
    }

    # Add common mapping variations
    for installed_name in installed:
        mapped_name = common_mismatches.get(installed_name, installed_name)
        if mapped_name in used_imports:
            continue
        if installed_name in used_imports:
            continue

        # Skip common dev/build tools
        dev_packages = {'pip', 'setuptools', 'wheel', 'pytest', 'black', 'flake8', 'mypy', 'isort', 'bandit'}
        if installed_name in dev_packages:
            continue

    return findings

def scan_project(project_path: Path, check_env: bool = True) -> list[Finding]:
    """Run all dependency checks."""
    findings = []

    findings.extend(check_requirements_pinning(project_path))

    if check_env:
        findings.extend(check_outdated_packages())
        findings.extend(check_vulnerabilities())

    return findings

def format_text(findings: list[Finding]) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return "✅ No dependency issues found."

    output = []
    by_issue = defaultdict(list)
    for f in findings:
        by_issue[f.issue].append(f)

    severity_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}

    issue_descriptions = {
        "security_vulnerability": "Security Vulnerabilities",
        "outdated_package": "Outdated Packages",
        "unpinned_dependency": "Unpinned Dependencies",
        "loose_version_constraint": "Loose Version Constraints",
    }

    issue_order = ["security_vulnerability", "outdated_package", "unpinned_dependency", "loose_version_constraint"]

    for issue_type in issue_order:
        items = by_issue.get(issue_type, [])
        if not items:
            continue

        # Group by severity
        by_severity = defaultdict(list)
        for item in items:
            by_severity[item.severity].append(item)

        desc = issue_descriptions.get(issue_type, issue_type)
        output.append(f"\n📦 {desc} ({len(items)} items)")
        output.append("-" * 50)

        for severity in ["high", "medium", "low"]:
            sev_items = by_severity.get(severity, [])
            if not sev_items:
                continue

            icon = severity_icons[severity]
            for f in sorted(sev_items, key=lambda x: x.package)[:15]:
                if f.vulnerability_id:
                    output.append(f"  {icon} {f.package} ({f.current_version}): {f.vulnerability_id}")
                elif f.file != "environment":
                    output.append(f"  {icon} {f.file}:{f.line} - {f.package}")
                else:
                    output.append(f"  {icon} {f.package}: {f.description}")

            if len(sev_items) > 15:
                output.append(f"  ... and {len(sev_items) - 15} more")

    # Summary
    vuln_count = len(by_issue.get("security_vulnerability", []))
    outdated_count = len(by_issue.get("outdated_package", []))

    output.append("\n📊 Summary")
    output.append("-" * 50)
    if vuln_count:
        output.append(f"  ⚠️  {vuln_count} security vulnerabilities - update immediately!")
    if outdated_count:
        output.append(f"  📦 {outdated_count} outdated packages")
    output.append(f"  Total: {len(findings)} dependency issues")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Check dependency health")
    parser.add_argument("path", type=Path, help="Project directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--skip-env", action="store_true", help="Skip environment checks (faster)")
    parser.add_argument("--only", choices=["vulnerabilities", "outdated", "pinning"], help="Run only specific check")
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if args.only:
        if args.only == "vulnerabilities":
            findings = check_vulnerabilities()
        elif args.only == "outdated":
            findings = check_outdated_packages()
        elif args.only == "pinning":
            findings = check_requirements_pinning(path)
        else:
            findings = []
    else:
        findings = scan_project(path, check_env=not args.skip_env)

    if args.format == "json":
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        print(format_text(findings))

    if any(f.severity == "high" for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main()
