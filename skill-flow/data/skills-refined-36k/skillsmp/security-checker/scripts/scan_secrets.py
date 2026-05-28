#!/usr/bin/env python3
"""Security scanner - detects secrets in git diff."""

import subprocess
import sys
import re


# Secret patterns (name, regex, severity)
SECRET_PATTERNS = [
    ("AWS Access Key", r"AKIA[0-9A-Z]{16}", "CRITICAL"),
    ("GitHub PAT", r"ghp_[a-zA-Z0-9]{36}", "CRITICAL"),
    ("Anthropic API Key", r"sk-ant-api", "CRITICAL"),
    ("OpenAI API Key", r"sk-proj-[a-zA-Z0-9_-]{20,}", "CRITICAL"),
    ("Generic API Key", r"api[_-]?key\s*[=:]\s*['\"][a-zA-Z0-9]{20,}", "HIGH"),
    ("JWT Token", r"eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*", "HIGH"),
    ("Private Key", r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "CRITICAL"),
    ("DB URL with Password", r"(postgres|mysql|mongodb)://[^:]+:[^@]+@", "CRITICAL"),
    ("Password Assignment", r"password\s*[=:]\s*['\"][^'\"]{8,}", "HIGH"),
    ("Bearer Token", r"bearer\s+[a-zA-Z0-9]{20,}", "HIGH"),
]

# File patterns that should never be committed
FORBIDDEN_FILES = [
    r"\.env",
    r"credentials.*\.json",
    r".*-key\.json",
    r".*_key\.json",
    r"\.pem$",
    r"\.p12$",
    r"gcp-key\.json",
    r"service-account.*\.json",
]

# False positive indicators
FALSE_POSITIVE_INDICATORS = [
    "example", "placeholder", "your-key-here", "xxx", "test",
    "fake", "dummy", "sample", "mock", "FAKE_", "TEST_",
]


def get_staged_files():
    """Get list of staged files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=30
        )
        return [f for f in result.stdout.strip().split("\n") if f]
    except Exception:
        return []


def get_staged_diff():
    """Get staged diff content."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout
    except Exception:
        return ""


def check_forbidden_files(files):
    """Check for forbidden file patterns."""
    findings = []
    for f in files:
        for pattern in FORBIDDEN_FILES:
            if re.search(pattern, f, re.IGNORECASE):
                findings.append({
                    "file": f,
                    "type": "Forbidden File",
                    "severity": "CRITICAL",
                    "message": f"File matches forbidden pattern: {pattern}"
                })
                break
    return findings


def is_false_positive(line, context=""):
    """Check if a match is likely a false positive."""
    combined = (line + " " + context).lower()
    for indicator in FALSE_POSITIVE_INDICATORS:
        if indicator.lower() in combined:
            return True
    # Check if it's in tests/ or docs/
    if "tests/" in combined or "docs/" in combined:
        return True
    return False


def scan_for_secrets(diff):
    """Scan diff content for secret patterns."""
    findings = []
    lines = diff.split("\n")
    current_file = ""

    for i, line in enumerate(lines):
        # Track current file
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue

        # Only check added lines
        if not line.startswith("+") or line.startswith("+++"):
            continue

        # Get context (surrounding lines)
        context = " ".join(lines[max(0, i-3):i+3])

        # Check each pattern
        for name, pattern, severity in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                if not is_false_positive(line, context):
                    findings.append({
                        "file": current_file,
                        "type": name,
                        "severity": severity,
                        "line": line[:80] + "..." if len(line) > 80 else line
                    })

    return findings


def main():
    """Run security scan and report results."""
    files = get_staged_files()
    diff = get_staged_diff()

    if not files and not diff:
        print("No staged changes to scan.")
        return 0

    findings = []

    # Check forbidden files
    findings.extend(check_forbidden_files(files))

    # Scan content for secrets
    findings.extend(scan_for_secrets(diff))

    # Report results
    if findings:
        print("SECURITY SCAN: SECRETS DETECTED")
        print("=" * 50)
        for f in findings:
            print(f"\n{f['severity']}: {f['type']}")
            print(f"  File: {f['file']}")
            if 'line' in f:
                print(f"  Match: {f['line'][:50]}...")
            if 'message' in f:
                print(f"  {f['message']}")
        print("\n" + "=" * 50)
        print("COMMIT BLOCKED - Fix issues above")
        return 1
    else:
        print("SECURITY SCAN: PASSED")
        print(f"  Files scanned: {len(files)}")
        print(f"  Patterns checked: {len(SECRET_PATTERNS)}")
        print("  Secrets found: 0")
        print("\nSafe to commit")
        return 0


if __name__ == "__main__":
    sys.exit(main())
