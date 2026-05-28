#!/usr/bin/env python3
"""Consolidated runs-tools CLI - fallback implementation for .runs/ operations.

This is the Python fallback for the demoswarm Rust binary.
Agents should invoke via the shim: bash .claude/scripts/demoswarm.sh <command> [options]

Command structure mirrors the Rust CLI:
    demoswarm count pattern --file X --regex Y
    demoswarm count bdd --dir X
    demoswarm ms get --file X --section Y --key Z
    demoswarm yaml get --file X --key Y
    demoswarm yaml count-items --file X --item-regex Y
    demoswarm inv get --file X --marker Y
    demoswarm line get --file X --prefix Y
    demoswarm receipts count --run-dir X
    demoswarm receipt get --file X --key Y
    demoswarm openapi count-paths --file X
    demoswarm index upsert-status --index X --run-id Y --status Z --last-flow W --updated-at T
    demoswarm time now
    demoswarm secrets scan --path X --output Y
    demoswarm secrets redact --file X --type Y
    demoswarm openq next-id --file X --prefix Y
    demoswarm openq append --file X --prefix Y --question Q --default D --impact I
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# =============================================================================
# Common utilities
# =============================================================================

def print_result(value: Any) -> None:
    """Print result to stdout. None becomes 'null'."""
    if value is None:
        print("null")
    else:
        print(value)


def file_exists(path: str) -> bool:
    """Check if file exists."""
    return Path(path).is_file()


def dir_exists(path: str) -> bool:
    """Check if directory exists."""
    return Path(path).is_dir()


def read_file(path: str) -> Optional[str]:
    """Read file contents, return None on error."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return None


def write_file(path: str, content: str) -> bool:
    """Write content to file, return success."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False


def count_pattern(content: str, pattern: str) -> Optional[int]:
    """Count lines matching pattern in content."""
    try:
        regex = re.compile(pattern)
    except re.error:
        return None

    return sum(1 for line in content.splitlines() if regex.search(line))


def iso_now() -> str:
    """Return current UTC time in ISO8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_write_json(path: str, data: dict) -> bool:
    """Write JSON atomically using temp file + rename."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = p.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        tmp_path.replace(p)
        return True
    except Exception:
        return False


def extract_machine_summary_section(content: str) -> Optional[str]:
    """Extract the ## Machine Summary section from markdown."""
    lines = content.splitlines()
    in_section = False
    section_lines = []

    for line in lines:
        if re.match(r'^##\s+Machine Summary\s*$', line):
            in_section = True
            continue
        if in_section:
            if re.match(r'^##\s+', line):
                break
            section_lines.append(line)

    if not section_lines:
        return None
    return "\n".join(section_lines)


def extract_field_from_section(section: str, key: str) -> Optional[str]:
    """Extract a field value from a section (YAML-ish format)."""
    pattern = rf'^\s*{re.escape(key)}\s*:\s*(.+?)\s*$'
    for line in section.splitlines():
        match = re.match(pattern, line)
        if match:
            value = match.group(1).strip()
            # Template leak guard: reject values with | or <
            if '|' in value or '<' in value:
                return None
            return value.split()[0] if value else None
    return None


def extract_yaml_block(content: str) -> Optional[str]:
    """Extract fenced YAML block from start of file."""
    lines = content.splitlines()
    in_yaml = False
    yaml_lines = []

    for line in lines:
        if not in_yaml:
            if line.strip() == "```yaml":
                in_yaml = True
                continue
        else:
            if line.strip() == "```":
                break
            yaml_lines.append(line)

    if not yaml_lines:
        return None
    return "\n".join(yaml_lines)


def extract_yaml_field(yaml_content: str, key: str) -> Optional[str]:
    """Extract a field from YAML content (simple parser, indent-tolerant)."""
    pattern = rf'^\s*{re.escape(key)}:\s*(.+?)\s*$'
    for line in yaml_content.splitlines():
        match = re.match(pattern, line)
        if match:
            value = match.group(1).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            return value
    return None


# =============================================================================
# Command handlers
# =============================================================================

def cmd_count_pattern(args: argparse.Namespace) -> None:
    """Count lines matching a regex pattern in a file."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    count = count_pattern(content, args.regex)
    if count is None:
        print_result(None)
        return

    # Try fallback if primary returns 0
    if count == 0 and args.fallback_regex:
        fallback = count_pattern(content, args.fallback_regex)
        if fallback is None:
            print_result(None)
            return
        count = fallback

    if count == 0 and getattr(args, "null_if_zero", False):
        print_result(None)
    else:
        print_result(count)


def cmd_count_bdd(args: argparse.Namespace) -> None:
    """Count BDD scenarios across feature files in a directory."""
    if not dir_exists(args.dir):
        print_result(None)
        return

    features_dir = Path(args.dir)
    total = 0
    pattern = r'^\s*(Scenario:|Scenario Outline:)'

    try:
        for feature_file in features_dir.glob("*.feature"):
            content = feature_file.read_text(encoding="utf-8")
            count = count_pattern(content, pattern)
            if count is None:
                print_result(None)
                return
            total += count
        print_result(total)
    except Exception:
        print_result(None)


def cmd_ms_get(args: argparse.Namespace) -> None:
    """Extract a field from a Machine Summary block."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    section = extract_machine_summary_section(content)
    if section is None:
        print_result(None)
        return

    value = extract_field_from_section(section, args.key)
    print_result(value)


def cmd_yaml_get(args: argparse.Namespace) -> None:
    """Extract a field from a fenced YAML block."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    yaml_content = extract_yaml_block(content)
    if yaml_content is None:
        print_result(None)
        return

    value = extract_yaml_field(yaml_content, args.key)
    print_result(value)


def cmd_yaml_count_items(args: argparse.Namespace) -> None:
    """Count items matching a pattern in a YAML block."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    yaml_content = extract_yaml_block(content)
    if yaml_content is None:
        print_result(None)
        return

    # Convert POSIX character class to Python
    pattern = args.item_regex.replace("[[:space:]]", r"\s")
    count = count_pattern(yaml_content, pattern)
    print_result(count)


def cmd_inv_get(args: argparse.Namespace) -> None:
    """Extract value from an inventory marker line."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    # Look for pattern: ^- <MARKER>: <value>
    pattern = rf'^- {re.escape(args.marker)}:\s*(.+?)\s*$'
    for line in content.splitlines():
        match = re.match(pattern, line)
        if match:
            print_result(match.group(1).strip())
            return

    print_result(None)


def cmd_line_get(args: argparse.Namespace) -> None:
    """Extract value from a line with a known prefix."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    for line in content.splitlines():
        if line.startswith(args.prefix):
            value = line[len(args.prefix):].strip()
            print_result(value)
            return

    print_result(None)


def cmd_receipts_count(args: argparse.Namespace) -> None:
    """Count prior flow receipts in a run directory."""
    if not dir_exists(args.run_dir):
        print_result(None)
        return

    run_dir = Path(args.run_dir)

    try:
        count = len(list(run_dir.glob("*/*_receipt.json")))
        print_result(count)
    except Exception:
        print_result(None)


def try_git_show(path: str) -> Optional[str]:
    """Try to read file content via git show HEAD:<path>."""
    import subprocess

    # Normalize path separators to forward slashes for git
    git_path = path.replace("\\", "/")

    try:
        result = subprocess.run(
            ["git", "show", f"HEAD:{git_path}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        # Best-effort git fallback: if git is unavailable or errors, behave as if
        # the file is missing and let the caller handle None.
        pass
    return None


def discover_receipt_content(path: str) -> tuple[Optional[str], str]:
    """Discover receipt content using file-first, git-fallback protocol.

    Returns (content, method) where method is 'direct_read', 'git_show', or 'missing'.
    """
    # Try direct file read first
    if file_exists(path):
        content = read_file(path)
        if content is not None:
            return (content, "direct_read")

    # Try git fallback
    content = try_git_show(path)
    if content is not None:
        return (content, "git_show")

    return (None, "missing")


def cmd_receipt_get(args: argparse.Namespace) -> None:
    """Read a field from a receipt JSON file with git fallback."""
    content, method = discover_receipt_content(args.file)

    # Log discovery method to stderr for structured output
    print(f"discovery_method: {method}", file=sys.stderr)

    if content is None:
        print_result(None)
        return

    try:
        data = json.loads(content)
        value = data.get(args.key)
        print_result(value)
    except Exception:
        print_result(None)


def cmd_openapi_count_paths(args: argparse.Namespace) -> None:
    """Count API paths in an OpenAPI YAML file."""
    if not file_exists(args.file):
        print_result(None)
        return

    content = read_file(args.file)
    if content is None:
        print_result(None)
        return

    lines = content.splitlines()
    in_paths = False
    count = 0

    for line in lines:
        if line.strip() == "paths:" or line.startswith("paths:"):
            in_paths = True
            continue

        if in_paths:
            if line and not line[0].isspace() and line[0] != '#':
                break
            if re.match(r'^\s+[\'"]?/', line):
                count += 1

    if count == 0 and not in_paths:
        print_result(None)
    else:
        print_result(count)


def cmd_index_upsert_status(args: argparse.Namespace) -> None:
    """Update a run's status in .runs/index.json."""
    if not file_exists(args.index):
        print("SKIPPED_MISSING_INDEX")
        return

    try:
        with open(args.index, "r", encoding="utf-8") as f:
            index = json.load(f)
    except Exception:
        print("SKIPPED_MISSING_INDEX")
        return

    runs = index.get("runs", [])
    found = False
    for run in runs:
        if run.get("run_id") == args.run_id:
            run["status"] = args.status
            run["last_flow"] = args.last_flow
            run["updated_at"] = args.updated_at
            found = True
            break

    if not found:
        print("SKIPPED_RUN_NOT_FOUND")
        return

    # Sort runs by run_id for stable diffs
    runs.sort(key=lambda r: r.get("run_id", ""))
    index["runs"] = runs

    if atomic_write_json(args.index, index):
        print("ok")
    else:
        print("SKIPPED_WRITE_ERROR")


def cmd_time_now(args: argparse.Namespace) -> None:
    """Print current UTC timestamp in ISO8601 format."""
    print(iso_now())


# Secrets patterns (high-confidence only)
SECRETS_PATTERNS = [
    (r'gh[pousr]_[A-Za-z0-9_]{36,}', 'github-token'),
    (r'AKIA[0-9A-Z]{16}', 'aws-access-key'),
    (r'sk_live_[0-9a-zA-Z]{24,}', 'stripe-key'),
    (r'-----BEGIN\s.*PRIVATE KEY-----', 'private-key'),
    (r'eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*', 'jwt-token'),
]

REDACTION_PATTERNS = {
    'github-token': (r'gh[pousr]_[A-Za-z0-9_]{36,}', '[REDACTED:github-token]'),
    'aws-access-key': (r'AKIA[0-9A-Z]{16}', '[REDACTED:aws-access-key]'),
    'stripe-key': (r'sk_live_[0-9a-zA-Z]{24,}', '[REDACTED:stripe-key]'),
    'jwt-token': (r'eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*', '[REDACTED:jwt-token]'),
}


def cmd_secrets_scan(args: argparse.Namespace) -> None:
    """Scan for secrets (locations only, never content)."""
    scan_path = Path(args.path)

    if not scan_path.exists():
        result = {"status": "SCAN_PATH_MISSING", "findings": []}
        atomic_write_json(args.output, result)
        print("SCAN_PATH_MISSING")
        return

    findings = []
    has_secrets = False

    def scan_file(file_path: Path) -> bool:
        nonlocal has_secrets
        found = False
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            for pattern, secret_type in SECRETS_PATTERNS:
                regex = re.compile(pattern)
                matching_lines = []
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        matching_lines.append(str(i))
                        found = True

                if matching_lines:
                    findings.append({
                        "file": str(file_path),
                        "type": secret_type,
                        "lines": ",".join(matching_lines)
                    })
        except Exception:
            pass
        return found

    if scan_path.is_file():
        has_secrets = scan_file(scan_path)
    elif scan_path.is_dir():
        for file_path in scan_path.rglob("*"):
            if file_path.is_file():
                if scan_file(file_path):
                    has_secrets = True

    status = "SECRETS_FOUND" if has_secrets else "CLEAN"
    result = {"status": status, "findings": findings}
    atomic_write_json(args.output, result)
    print(status)


def cmd_secrets_redact(args: argparse.Namespace) -> None:
    """Redact a specific secret type in a file."""
    if not file_exists(args.file):
        print("FILE_NOT_FOUND")
        return

    p = Path(args.file)
    content = p.read_text(encoding="utf-8")

    if args.type == 'private-key':
        pattern = r'-----BEGIN\s+.*PRIVATE KEY-----.*?-----END\s+.*PRIVATE KEY-----'
        content = re.sub(pattern, '[REDACTED:private-key]', content, flags=re.DOTALL)
    else:
        pattern, replacement = REDACTION_PATTERNS[args.type]
        content = re.sub(pattern, replacement, content)

    p.write_text(content, encoding="utf-8")
    print("ok")


def cmd_openq_next_id(args: argparse.Namespace) -> None:
    """Generate next open question ID."""
    if not file_exists(args.file):
        print(f"OQ-{args.prefix}-001")
        return

    content = read_file(args.file)
    if content is None:
        print(f"OQ-{args.prefix}-001")
        return

    pattern = rf'OQ-{re.escape(args.prefix)}-(\d{{3}})'
    matches = re.findall(pattern, content)

    if not matches:
        print(f"OQ-{args.prefix}-001")
        return

    highest = max(int(m) for m in matches)

    if highest >= 999:
        print(f"OQ-{args.prefix}-UNK")
        return

    print(f"OQ-{args.prefix}-{highest + 1:03d}")


def cmd_openq_append(args: argparse.Namespace) -> None:
    """Append an open question to a file."""
    # Get next ID by calling the function directly
    if not file_exists(args.file):
        qid = f"OQ-{args.prefix}-001"
    else:
        content = read_file(args.file)
        if content is None:
            qid = f"OQ-{args.prefix}-001"
        else:
            pattern = rf'OQ-{re.escape(args.prefix)}-(\d{{3}})'
            matches = re.findall(pattern, content)
            if not matches:
                qid = f"OQ-{args.prefix}-001"
            else:
                highest = max(int(m) for m in matches)
                if highest >= 999:
                    qid = f"OQ-{args.prefix}-UNK"
                else:
                    qid = f"OQ-{args.prefix}-{highest + 1:03d}"

    ts = iso_now()
    p = Path(args.file)

    # Create file with header if missing
    if not file_exists(args.file):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Open Questions\n\n", encoding="utf-8")

    # Append question
    entry = f"""- QID: {qid}
  - Q: {args.question} [OPEN]
  - Suggested default: {args.default}
  - Impact if different: {args.impact}
  - Added: {ts}

"""
    with open(args.file, "a", encoding="utf-8") as f:
        f.write(entry)

    print(qid)


# =============================================================================
# CLI parser setup
# =============================================================================

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="demoswarm",
        description="Deterministic helpers for .runs/ operations (Python fallback)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # count command
    count_parser = subparsers.add_parser("count", help="Count operations")
    count_sub = count_parser.add_subparsers(dest="subcommand", required=True)

    # count pattern
    count_pattern_p = count_sub.add_parser("pattern", help="Count lines matching regex")
    count_pattern_p.add_argument("--file", required=True, help="File to search")
    count_pattern_p.add_argument("--regex", required=True, help="Extended regex pattern")
    count_pattern_p.add_argument("--fallback-regex", help="Fallback regex if primary returns 0")
    count_pattern_p.add_argument("--null-if-missing", action="store_true")
    count_pattern_p.add_argument("--null-if-zero", action="store_true")
    count_pattern_p.set_defaults(func=cmd_count_pattern)

    # count bdd
    count_bdd_p = count_sub.add_parser("bdd", help="Count BDD scenarios")
    count_bdd_p.add_argument("--dir", required=True, help="Features directory")
    count_bdd_p.add_argument("--null-if-missing", action="store_true")
    count_bdd_p.set_defaults(func=cmd_count_bdd)

    # ms command
    ms_parser = subparsers.add_parser("ms", help="Machine Summary operations")
    ms_sub = ms_parser.add_subparsers(dest="subcommand", required=True)

    # ms get
    ms_get_p = ms_sub.add_parser("get", help="Extract Machine Summary field")
    ms_get_p.add_argument("--file", required=True, help="Markdown file")
    ms_get_p.add_argument("--section", required=True, help="Section header")
    ms_get_p.add_argument("--key", required=True, help="Field name to extract")
    ms_get_p.add_argument("--null-if-missing", action="store_true")
    ms_get_p.set_defaults(func=cmd_ms_get)

    # yaml command
    yaml_parser = subparsers.add_parser("yaml", help="YAML block operations")
    yaml_sub = yaml_parser.add_subparsers(dest="subcommand", required=True)

    # yaml get
    yaml_get_p = yaml_sub.add_parser("get", help="Extract YAML block field")
    yaml_get_p.add_argument("--file", required=True, help="Markdown file with YAML block")
    yaml_get_p.add_argument("--key", required=True, help="YAML key to extract")
    yaml_get_p.add_argument("--null-if-missing", action="store_true")
    yaml_get_p.set_defaults(func=cmd_yaml_get)

    # yaml count-items
    yaml_count_p = yaml_sub.add_parser("count-items", help="Count YAML block items")
    yaml_count_p.add_argument("--file", required=True, help="Markdown file with YAML block")
    yaml_count_p.add_argument("--item-regex", required=True, help="Pattern to count")
    yaml_count_p.add_argument("--null-if-missing", action="store_true")
    yaml_count_p.set_defaults(func=cmd_yaml_count_items)

    # inv command
    inv_parser = subparsers.add_parser("inv", help="Inventory marker operations")
    inv_sub = inv_parser.add_subparsers(dest="subcommand", required=True)

    # inv get
    inv_get_p = inv_sub.add_parser("get", help="Extract inventory marker value")
    inv_get_p.add_argument("--file", required=True, help="File to search")
    inv_get_p.add_argument("--marker", required=True, help="Marker prefix")
    inv_get_p.add_argument("--null-if-missing", action="store_true")
    inv_get_p.set_defaults(func=cmd_inv_get)

    # line command
    line_parser = subparsers.add_parser("line", help="Line value operations")
    line_sub = line_parser.add_subparsers(dest="subcommand", required=True)

    # line get
    line_get_p = line_sub.add_parser("get", help="Extract line value by prefix")
    line_get_p.add_argument("--file", required=True, help="File to search")
    line_get_p.add_argument("--prefix", required=True, help="Line prefix")
    line_get_p.add_argument("--null-if-missing", action="store_true")
    line_get_p.set_defaults(func=cmd_line_get)

    # receipts command
    receipts_parser = subparsers.add_parser("receipts", help="Receipt counting operations")
    receipts_sub = receipts_parser.add_subparsers(dest="subcommand", required=True)

    # receipts count
    receipts_count_p = receipts_sub.add_parser("count", help="Count existing receipts")
    receipts_count_p.add_argument("--run-dir", required=True, help="Run directory path")
    receipts_count_p.add_argument("--null-if-missing", action="store_true")
    receipts_count_p.set_defaults(func=cmd_receipts_count)

    # receipt command
    receipt_parser = subparsers.add_parser("receipt", help="Receipt field operations")
    receipt_sub = receipt_parser.add_subparsers(dest="subcommand", required=True)

    # receipt get
    receipt_get_p = receipt_sub.add_parser("get", help="Read receipt field")
    receipt_get_p.add_argument("--file", required=True, help="Receipt JSON file")
    receipt_get_p.add_argument("--key", required=True, help="Top-level key to extract")
    receipt_get_p.add_argument("--null-if-missing", action="store_true")
    receipt_get_p.set_defaults(func=cmd_receipt_get)

    # openapi command
    openapi_parser = subparsers.add_parser("openapi", help="OpenAPI operations")
    openapi_sub = openapi_parser.add_subparsers(dest="subcommand", required=True)

    # openapi count-paths
    openapi_count_p = openapi_sub.add_parser("count-paths", help="Count OpenAPI paths")
    openapi_count_p.add_argument("--file", required=True, help="OpenAPI YAML file")
    openapi_count_p.add_argument("--null-if-missing", action="store_true")
    openapi_count_p.set_defaults(func=cmd_openapi_count_paths)

    # index command
    index_parser = subparsers.add_parser("index", help="Index operations")
    index_sub = index_parser.add_subparsers(dest="subcommand", required=True)

    # index upsert-status
    index_upsert_p = index_sub.add_parser("upsert-status", help="Update run status in index")
    index_upsert_p.add_argument("--index", required=True, help="Path to index.json")
    index_upsert_p.add_argument("--run-id", required=True, help="Run ID to update")
    index_upsert_p.add_argument("--status", required=True,
                                choices=["VERIFIED", "UNVERIFIED", "CANNOT_PROCEED"])
    index_upsert_p.add_argument("--last-flow", required=True,
                                choices=["signal", "plan", "build", "gate", "deploy", "wisdom"])
    index_upsert_p.add_argument("--updated-at", required=True, help="ISO8601 timestamp")
    index_upsert_p.set_defaults(func=cmd_index_upsert_status)

    # time command
    time_parser = subparsers.add_parser("time", help="Time utilities")
    time_sub = time_parser.add_subparsers(dest="subcommand", required=True)

    # time now
    time_now_p = time_sub.add_parser("now", help="Get ISO8601 timestamp")
    time_now_p.set_defaults(func=cmd_time_now)

    # secrets command
    secrets_parser = subparsers.add_parser("secrets", help="Secrets operations")
    secrets_sub = secrets_parser.add_subparsers(dest="subcommand", required=True)

    # secrets scan
    secrets_scan_p = secrets_sub.add_parser("scan", help="Scan for secrets")
    secrets_scan_p.add_argument("--path", required=True, help="File or directory to scan")
    secrets_scan_p.add_argument("--output", required=True, help="JSON findings file")
    secrets_scan_p.set_defaults(func=cmd_secrets_scan)

    # secrets redact
    secrets_redact_p = secrets_sub.add_parser("redact", help="Redact secret type")
    secrets_redact_p.add_argument("--file", required=True, help="File to redact")
    secrets_redact_p.add_argument("--type", required=True,
                                  choices=['github-token', 'aws-access-key', 'stripe-key',
                                           'jwt-token', 'private-key'])
    secrets_redact_p.set_defaults(func=cmd_secrets_redact)

    # openq command
    openq_parser = subparsers.add_parser("openq", help="Open questions operations")
    openq_sub = openq_parser.add_subparsers(dest="subcommand", required=True)

    # openq next-id
    openq_nextid_p = openq_sub.add_parser("next-id", help="Generate next OQ ID")
    openq_nextid_p.add_argument("--file", required=True, help="Questions file")
    openq_nextid_p.add_argument("--prefix", required=True, help="Prefix (SIG, PLAN, BUILD)")
    openq_nextid_p.set_defaults(func=cmd_openq_next_id)

    # openq append
    openq_append_p = openq_sub.add_parser("append", help="Append open question")
    openq_append_p.add_argument("--file", required=True, help="Questions file")
    openq_append_p.add_argument("--prefix", required=True, help="Prefix (SIG, PLAN, BUILD)")
    openq_append_p.add_argument("--question", required=True, help="Question text")
    openq_append_p.add_argument("--default", required=True, help="Suggested default")
    openq_append_p.add_argument("--impact", required=True, help="Impact if different")
    openq_append_p.set_defaults(func=cmd_openq_append)

    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
