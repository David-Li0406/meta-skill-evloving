#!/usr/bin/env python3
"""
Secret Scanner

Scans source code for accidentally committed secrets like API keys,
passwords, tokens, and credentials.

Usage:
    python scan_secrets.py <path> [--format text|json]
    python scan_secrets.py . --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Finding(NamedTuple):
    file: str
    line: int
    type: str
    match: str
    severity: str


# Patterns for detecting secrets
SECRET_PATTERNS = {
    # API Keys
    "aws_access_key": {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "critical",
        "description": "AWS Access Key ID",
    },
    "aws_secret_key": {
        "pattern": r"(?i)aws[_\-]?secret[_\-]?access[_\-]?key['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{40})",
        "severity": "critical",
        "description": "AWS Secret Access Key",
    },
    "github_token": {
        "pattern": r"gh[pousr]_[A-Za-z0-9_]{36,}",
        "severity": "critical",
        "description": "GitHub Token",
    },
    "github_oauth": {
        "pattern": r"gho_[A-Za-z0-9]{36}",
        "severity": "critical",
        "description": "GitHub OAuth Token",
    },
    "slack_token": {
        "pattern": r"xox[baprs]-[0-9A-Za-z\-]{10,}",
        "severity": "high",
        "description": "Slack Token",
    },
    "stripe_key": {
        "pattern": r"sk_live_[0-9a-zA-Z]{24,}",
        "severity": "critical",
        "description": "Stripe Secret Key",
    },
    "stripe_test_key": {
        "pattern": r"sk_test_[0-9a-zA-Z]{24,}",
        "severity": "medium",
        "description": "Stripe Test Key",
    },
    "google_api_key": {
        "pattern": r"AIza[0-9A-Za-z\-_]{35}",
        "severity": "high",
        "description": "Google API Key",
    },
    "heroku_api_key": {
        "pattern": r"(?i)heroku[_\-]?api[_\-]?key['\"]?\s*[:=]\s*['\"]?([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        "severity": "high",
        "description": "Heroku API Key",
    },
    "twilio_api_key": {
        "pattern": r"SK[0-9a-fA-F]{32}",
        "severity": "high",
        "description": "Twilio API Key",
    },
    "sendgrid_api_key": {
        "pattern": r"SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}",
        "severity": "high",
        "description": "SendGrid API Key",
    },

    # Generic secrets
    "generic_api_key": {
        "pattern": r"(?i)(api[_\-]?key|apikey)['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{20,})['\"]?",
        "severity": "medium",
        "description": "Generic API Key",
    },
    "generic_secret": {
        "pattern": r"(?i)(secret|secret[_\-]?key)['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})['\"]?",
        "severity": "medium",
        "description": "Generic Secret",
    },
    "generic_password": {
        "pattern": r"(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?([^\s'\"]{8,})['\"]?",
        "severity": "medium",
        "description": "Hardcoded Password",
    },
    "generic_token": {
        "pattern": r"(?i)(access[_\-]?token|auth[_\-]?token|bearer)['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{20,})['\"]?",
        "severity": "medium",
        "description": "Generic Token",
    },

    # Database URLs
    "database_url": {
        "pattern": r"(?i)(postgres|mysql|mongodb|redis)://[^\s'\"]+:[^\s'\"]+@",
        "severity": "critical",
        "description": "Database URL with credentials",
    },

    # Private keys
    "private_key_rsa": {
        "pattern": r"-----BEGIN RSA PRIVATE KEY-----",
        "severity": "critical",
        "description": "RSA Private Key",
    },
    "private_key_openssh": {
        "pattern": r"-----BEGIN OPENSSH PRIVATE KEY-----",
        "severity": "critical",
        "description": "OpenSSH Private Key",
    },
    "private_key_dsa": {
        "pattern": r"-----BEGIN DSA PRIVATE KEY-----",
        "severity": "critical",
        "description": "DSA Private Key",
    },
    "private_key_ec": {
        "pattern": r"-----BEGIN EC PRIVATE KEY-----",
        "severity": "critical",
        "description": "EC Private Key",
    },
    "private_key_pgp": {
        "pattern": r"-----BEGIN PGP PRIVATE KEY BLOCK-----",
        "severity": "critical",
        "description": "PGP Private Key",
    },

    # JWT tokens (only if they look like production tokens)
    "jwt_token": {
        "pattern": r"eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]{20,}",
        "severity": "medium",
        "description": "JWT Token",
    },
}

# Files and directories to skip
SKIP_PATTERNS = [
    r"node_modules",
    r"\.git",
    r"\.venv",
    r"venv",
    r"__pycache__",
    r"\.pyc$",
    r"\.min\.js$",
    r"\.min\.css$",
    r"package-lock\.json$",
    r"yarn\.lock$",
    r"Pipfile\.lock$",
    r"poetry\.lock$",
    r"\.svg$",
    r"\.png$",
    r"\.jpg$",
    r"\.jpeg$",
    r"\.gif$",
    r"\.ico$",
    r"\.woff",
    r"\.ttf$",
    r"\.eot$",
]

# Known false positives to ignore
FALSE_POSITIVE_PATTERNS = [
    r"example",
    r"sample",
    r"placeholder",
    r"your[_\-]?api[_\-]?key",
    r"xxx+",
    r"123+",
    r"test[_\-]?key",
    r"\*\*\*",
    r"REPLACE_ME",
    r"<[^>]+>",  # HTML-like placeholders
    r"\$\{[^}]+\}",  # Template variables
    r"process\.env\.",  # Environment variable references
    r"os\.environ",  # Python env references
    r"ENV\[",  # Ruby env references
]


def should_skip_file(file_path: str) -> bool:
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def is_false_positive(match_text: str, line: str) -> bool:
    """Check if match is likely a false positive."""
    lower_line = line.lower()
    lower_match = match_text.lower()

    for pattern in FALSE_POSITIVE_PATTERNS:
        if re.search(pattern, lower_line) or re.search(pattern, lower_match):
            return True

    # Skip if in a comment (basic check)
    stripped = line.strip()
    if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('*'):
        # Unless it looks like an actual secret was commented out
        if 'TODO' not in line and 'FIXME' not in line:
            return True

    return False


def scan_file(file_path: Path) -> list[Finding]:
    """Scan a single file for secrets."""
    findings = []

    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return findings

    lines = content.split('\n')

    for line_num, line in enumerate(lines, start=1):
        for secret_type, config in SECRET_PATTERNS.items():
            for match in re.finditer(config["pattern"], line):
                match_text = match.group(0)

                # Skip false positives
                if is_false_positive(match_text, line):
                    continue

                # Mask the middle of the secret for display
                if len(match_text) > 10:
                    masked = match_text[:4] + '*' * (len(match_text) - 8) + match_text[-4:]
                else:
                    masked = match_text[:2] + '*' * (len(match_text) - 2)

                findings.append(Finding(
                    file=str(file_path),
                    line=line_num,
                    type=config["description"],
                    match=masked,
                    severity=config["severity"],
                ))

    return findings


def find_files(path: Path) -> list[Path]:
    """Find all files to scan."""
    if path.is_file():
        return [path] if not should_skip_file(str(path)) else []

    files = []
    for file_path in path.rglob('*'):
        if file_path.is_file() and not should_skip_file(str(file_path)):
            files.append(file_path)

    return sorted(files)


def format_text_output(findings: list[Finding]) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return "✅ No secrets found."

    output = []
    output.append(f"🔴 Found {len(findings)} potential secret(s):\n")

    # Group by severity
    critical = [f for f in findings if f.severity == "critical"]
    high = [f for f in findings if f.severity == "high"]
    medium = [f for f in findings if f.severity == "medium"]

    if critical:
        output.append("🚨 CRITICAL:")
        for f in critical:
            output.append(f"  {f.file}:{f.line}")
            output.append(f"    Type: {f.type}")
            output.append(f"    Found: {f.match}")
        output.append("")

    if high:
        output.append("⚠️  HIGH:")
        for f in high:
            output.append(f"  {f.file}:{f.line}")
            output.append(f"    Type: {f.type}")
            output.append(f"    Found: {f.match}")
        output.append("")

    if medium:
        output.append("📋 MEDIUM:")
        for f in medium:
            output.append(f"  {f.file}:{f.line}")
            output.append(f"    Type: {f.type}")
            output.append(f"    Found: {f.match}")
        output.append("")

    output.append("─" * 50)
    output.append(f"Summary: {len(critical)} critical, {len(high)} high, {len(medium)} medium")
    output.append("\n⚠️  IMPORTANT:")
    output.append("  1. Rotate any exposed secrets immediately")
    output.append("  2. Remove secrets from code and history")
    output.append("  3. Use environment variables or a secrets manager")
    output.append("  4. Consider the repo compromised if secrets were pushed")

    return "\n".join(output)


def format_json_output(findings: list[Finding]) -> str:
    """Format findings as JSON."""
    return json.dumps({
        "total": len(findings),
        "critical": sum(1 for f in findings if f.severity == "critical"),
        "high": sum(1 for f in findings if f.severity == "high"),
        "medium": sum(1 for f in findings if f.severity == "medium"),
        "findings": [f._asdict() for f in findings],
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Scan source code for accidentally committed secrets"
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

    # Find and scan files
    files = find_files(path)

    if not files:
        print(f"No files to scan in {path}", file=sys.stderr)
        sys.exit(0)

    all_findings = []
    for file_path in files:
        findings = scan_file(file_path)
        all_findings.extend(findings)

    # Output
    if args.format == "json":
        print(format_json_output(all_findings))
    else:
        print(format_text_output(all_findings))

    # Exit code: 1 if critical/high findings, 0 otherwise
    critical_or_high = sum(
        1 for f in all_findings
        if f.severity in ("critical", "high")
    )
    sys.exit(1 if critical_or_high > 0 else 0)


if __name__ == "__main__":
    main()
