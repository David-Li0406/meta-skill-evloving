# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Orchestrator for code hardcode audit combining Ruff, Semgrep, jscpd, and gitleaks.

Usage:
    uv run --script audit_hardcodes.py -- <path> [options]

Options:
    --output {json,text,both}  Output format (default: both)
    --tools {all,ruff,semgrep,jscpd,gitleaks}  Tools to run (default: all)
    --severity {all,high,medium,low}  Filter by severity (default: all)
    --exclude PATTERN  Glob pattern to exclude (repeatable)
    --no-parallel  Disable parallel execution
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ADR: 2025-12-08-mise-env-centralized-config
# Configuration via environment variables with defaults for backward compatibility
AUDIT_PARALLEL_WORKERS = int(os.environ.get("AUDIT_PARALLEL_WORKERS", "4"))
AUDIT_JSCPD_TIMEOUT = int(os.environ.get("AUDIT_JSCPD_TIMEOUT", "300"))
AUDIT_GITLEAKS_TIMEOUT = int(os.environ.get("AUDIT_GITLEAKS_TIMEOUT", "120"))


@dataclass
class Finding:
    """A single finding from any tool."""

    id: str
    tool: str
    rule: str
    file: str
    line: int
    column: int = 0
    end_line: int | None = None
    message: str = ""
    severity: str = "medium"
    suggested_fix: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "tool": self.tool,
            "rule": self.rule,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "end_line": self.end_line,
            "message": self.message,
            "severity": self.severity,
            "suggested_fix": self.suggested_fix,
        }

    def to_text(self) -> str:
        loc = f"{self.file}:{self.line}"
        if self.column:
            loc += f":{self.column}"
        return f"{loc}: {self.rule} {self.message} [{self.tool}]"


@dataclass
class AuditResult:
    """Aggregated results from all tools."""

    findings: list[Finding] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)

    def add_error(self, error: str) -> None:
        self.errors.append(error)

    def summary(self) -> dict[str, Any]:
        by_tool: dict[str, int] = {}
        by_severity: dict[str, int] = {}

        for f in self.findings:
            by_tool[f.tool] = by_tool.get(f.tool, 0) + 1
            by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

        return {
            "total_findings": len(self.findings),
            "by_tool": by_tool,
            "by_severity": by_severity,
        }

    def to_json(self) -> str:
        return json.dumps(
            {
                "summary": self.summary(),
                "findings": [f.to_dict() for f in self.findings],
                "errors": self.errors,
            },
            indent=2,
        )

    def to_text(self) -> str:
        lines = [f.to_text() for f in self.findings]
        summary = self.summary()
        tool_counts = ", ".join(f"{k}: {v}" for k, v in summary["by_tool"].items())
        lines.append("")
        lines.append(f"Summary: {summary['total_findings']} findings ({tool_counts})")
        if self.errors:
            lines.append(f"Errors: {len(self.errors)}")
            for e in self.errors:
                lines.append(f"  - {e}")
        return "\n".join(lines)


def run_ruff(target: Path, excludes: list[str]) -> list[Finding]:
    """Run Ruff PLR2004 check and return findings."""
    cmd = ["ruff", "check", "--select", "PLR2004", "--output-format", "json", str(target)]
    for pattern in excludes:
        cmd.extend(["--exclude", pattern])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Ruff returns exit code 1 when findings exist
        if result.stdout:
            data = json.loads(result.stdout)
            findings = []
            for i, item in enumerate(data):
                findings.append(
                    Finding(
                        id=f"RUFF-{i + 1:03d}",
                        tool="ruff",
                        rule=item.get("code", "PLR2004"),
                        file=item.get("filename", ""),
                        line=item.get("location", {}).get("row", 0),
                        column=item.get("location", {}).get("column", 0),
                        message=item.get("message", ""),
                        severity="medium",
                        suggested_fix="Extract to named constant",
                    )
                )
            return findings
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ruff error: {e}", file=sys.stderr)
    return []


def _extract_rule_id(check_id: str) -> str:
    """Extract clean rule ID from Semgrep's path-based check_id.

    Semgrep generates check_ids like:
    'Users.terryli..claude.skills.code-hardcode-audit.assets.hardcoded-timeframe'

    This extracts just 'hardcoded-timeframe'.
    """
    # Split by dots and find the actual rule name (after 'assets' or last segment)
    parts = check_id.split(".")
    # Look for 'assets' marker, take everything after it
    if "assets" in parts:
        idx = parts.index("assets")
        return ".".join(parts[idx + 1 :]) if idx + 1 < len(parts) else check_id
    # Fallback: return last segment
    return parts[-1] if parts else check_id


def run_semgrep(target: Path, excludes: list[str]) -> list[Finding]:
    """Run Semgrep with custom rules and return findings."""
    rules_path = Path(__file__).parent.parent / "assets" / "semgrep-hardcode-rules.yaml"

    if not rules_path.exists():
        print(f"semgrep rules not found: {rules_path}", file=sys.stderr)
        return []

    cmd = ["semgrep", "--config", str(rules_path), "--json", str(target)]
    for pattern in excludes:
        cmd.extend(["--exclude", pattern])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            data = json.loads(result.stdout)
            findings = []
            for i, item in enumerate(data.get("results", [])):
                severity_map = {"ERROR": "high", "WARNING": "medium", "INFO": "low"}
                raw_check_id = item.get("check_id", "")
                findings.append(
                    Finding(
                        id=f"SGRP-{i + 1:03d}",
                        tool="semgrep",
                        rule=_extract_rule_id(raw_check_id),
                        file=item.get("path", ""),
                        line=item.get("start", {}).get("line", 0),
                        column=item.get("start", {}).get("col", 0),
                        end_line=item.get("end", {}).get("line"),
                        message=item.get("extra", {}).get("message", ""),
                        severity=severity_map.get(
                            item.get("extra", {}).get("severity", "WARNING"), "medium"
                        ),
                        suggested_fix=item.get("extra", {})
                        .get("metadata", {})
                        .get("suggested_fix", ""),
                    )
                )
            return findings
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"semgrep error: {e}", file=sys.stderr)
    return []


def run_jscpd(target: Path, excludes: list[str]) -> list[Finding]:
    """Run jscpd via npx and return findings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        cmd = ["npx", "jscpd", "--reporters", "json", "--output", str(output_dir), str(target)]
        for pattern in excludes:
            cmd.extend(["--ignore", pattern])

        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=AUDIT_JSCPD_TIMEOUT)
            report_path = output_dir / "jscpd-report.json"
            if report_path.exists():
                data = json.loads(report_path.read_text())
                findings = []
                for i, dup in enumerate(data.get("duplicates", [])):
                    first = dup.get("firstFile", {})
                    second = dup.get("secondFile", {})
                    findings.append(
                        Finding(
                            id=f"JSCPD-{i + 1:03d}",
                            tool="jscpd",
                            rule="duplicate-code",
                            file=first.get("name", ""),
                            line=first.get("startLoc", {}).get("line", 0),
                            end_line=first.get("endLoc", {}).get("line"),
                            message=f"Clone detected with {second.get('name', '')} "
                            f"({dup.get('lines', 0)} lines, "
                            f"{dup.get('fragment', '')})",
                            severity="low",
                            suggested_fix="Extract to shared function or module",
                        )
                    )
                return findings
        except (json.JSONDecodeError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"jscpd error: {e}", file=sys.stderr)
    return []


def run_gitleaks(target: Path, excludes: list[str]) -> list[Finding]:
    """Run gitleaks for secret detection and return findings.

    Uses modern 'dir' command for directory scanning (v8.19.0+).
    Exit codes: 0 = clean, 1 = secrets found (expected), 2+ = error.
    """
    cmd = [
        "gitleaks",
        "dir",
        str(target),
        "--report-format",
        "json",
        "--report-path",
        "/dev/stdout",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=AUDIT_GITLEAKS_TIMEOUT)

        # Exit code 1 = secrets found (expected, not an error)
        if result.returncode in (0, 1) and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                findings = []
                for i, item in enumerate(data):
                    findings.append(
                        Finding(
                            id=f"GITLEAKS-{i + 1:03d}",
                            tool="gitleaks",
                            rule=item.get("RuleID", "secret"),
                            file=item.get("File", ""),
                            line=item.get("StartLine", 0),
                            end_line=item.get("EndLine"),
                            message=f"Secret detected: {item.get('Match', '')[:30]}...",
                            severity="high",  # Secrets are always high severity
                            suggested_fix="Remove secret and rotate credentials",
                        )
                    )
                return findings
            except json.JSONDecodeError:
                pass
        return []
    except FileNotFoundError:
        print("gitleaks not found. Install with: mise use --global gitleaks", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print(f"gitleaks timed out after {AUDIT_GITLEAKS_TIMEOUT} seconds", file=sys.stderr)
        return []


def run_audit(
    target: Path,
    tools: list[str],
    excludes: list[str],
    parallel: bool = True,
) -> AuditResult:
    """Run selected tools and aggregate results."""
    result = AuditResult()

    tool_funcs = {
        "ruff": run_ruff,
        "semgrep": run_semgrep,
        "jscpd": run_jscpd,
        "gitleaks": run_gitleaks,
    }

    selected = tools if tools != ["all"] else list(tool_funcs.keys())

    if parallel:
        with ThreadPoolExecutor(max_workers=AUDIT_PARALLEL_WORKERS) as executor:
            futures = {
                executor.submit(tool_funcs[name], target, excludes): name
                for name in selected
                if name in tool_funcs
            }
            for future in as_completed(futures):
                name = futures[future]
                try:
                    for finding in future.result():
                        result.add_finding(finding)
                except Exception as e:
                    result.add_error(f"{name}: {e}")
    else:
        for name in selected:
            if name in tool_funcs:
                try:
                    for finding in tool_funcs[name](target, excludes):
                        result.add_finding(finding)
                except Exception as e:
                    result.add_error(f"{name}: {e}")

    # Sort by file, then line
    result.findings.sort(key=lambda f: (f.file, f.line))
    return result


def filter_by_severity(result: AuditResult, severity: str) -> AuditResult:
    """Filter findings by severity level."""
    if severity == "all":
        return result

    severity_order = {"high": 0, "medium": 1, "low": 2}
    threshold = severity_order.get(severity, 2)

    filtered = AuditResult(errors=result.errors)
    for f in result.findings:
        if severity_order.get(f.severity, 2) <= threshold:
            filtered.add_finding(f)
    return filtered


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit code for hardcoded values using Ruff, Semgrep, jscpd, and gitleaks"
    )
    parser.add_argument("path", type=Path, help="Path to audit")
    parser.add_argument(
        "--output",
        choices=["json", "text", "both"],
        default="both",
        help="Output format",
    )
    parser.add_argument(
        "--tools",
        choices=["all", "ruff", "semgrep", "jscpd", "gitleaks"],
        nargs="+",
        default=["all"],
        help="Tools to run",
    )
    parser.add_argument(
        "--severity",
        choices=["all", "high", "medium", "low"],
        default="all",
        help="Filter by minimum severity",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob pattern to exclude",
    )
    parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Disable parallel execution",
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        return 1

    result = run_audit(
        target=args.path,
        tools=args.tools,
        excludes=args.exclude,
        parallel=not args.no_parallel,
    )

    result = filter_by_severity(result, args.severity)

    if args.output == "json":
        print(result.to_json())
    elif args.output == "text":
        print(result.to_text())
    else:  # both
        print(result.to_text())
        print("\n--- JSON Output ---")
        print(result.to_json())

    return 0 if not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
