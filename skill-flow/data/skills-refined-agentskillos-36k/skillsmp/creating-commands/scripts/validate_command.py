#!/usr/bin/env python3
"""
Comprehensive command validation script.

Validates command structure, counts command-specific metrics (bash commands,
@ references, Skill() invocations), and provides quality analysis.

Usage:
    python3 scripts/validate_command.py /path/to/command.md
    python3 scripts/validate_command.py /path/to/command.md --minimal
"""

import sys
import re
import yaml
from pathlib import Path
from typing import List, Tuple, Optional, Dict

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Global flag for minimal mode
_MINIMAL_MODE = False

def set_minimal_mode(enabled: bool):
    """Set global minimal mode flag."""
    global _MINIMAL_MODE
    _MINIMAL_MODE = enabled

class ValidationIssue:
    """Represents a validation failure with specific remediation."""
    def __init__(self, check: str, location: str, found: str, expected: str, fix: str, severity: str = "error"):
        self.check = check
        self.location = location
        self.found = found
        self.expected = expected
        self.fix = fix
        self.severity = severity  # "error" or "warning"

    def __str__(self):
        if self.severity == "warning":
            icon = f"{Colors.YELLOW}⚠{Colors.END}"
            title = f"{Colors.YELLOW}⚠ {self.check}{Colors.END}"
        else:
            icon = f"{Colors.RED}✗{Colors.END}"
            title = f"{Colors.RED}✗ {self.check}{Colors.END}"

        return (f"{title}\n"
                f"  Location: {self.location}\n"
                f"  Found: {self.found}\n"
                f"  Expected: {self.expected}\n"
                f"  Fix: {self.fix}")

def print_header(text: str):
    """Print formatted header."""
    if not _MINIMAL_MODE:
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

def print_section(text: str):
    """Print section header."""
    if not _MINIMAL_MODE:
        print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
        print(f"{Colors.CYAN}{'-' * len(text)}{Colors.END}\n")

def check_pass(msg: str):
    """Print passing check."""
    if not _MINIMAL_MODE:
        print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def check_fail(msg: str):
    """Print failing check."""
    if not _MINIMAL_MODE:
        print(f"{Colors.RED}✗{Colors.END} {msg}")

def check_warn(msg: str):
    """Print warning check."""
    if not _MINIMAL_MODE:
        print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def check_info(msg: str):
    """Print informational message."""
    if not _MINIMAL_MODE:
        print(f"{Colors.CYAN}ℹ{Colors.END} {msg}")

def parse_yaml_frontmatter(content: str) -> Tuple[Optional[dict], Optional[str]]:
    """Extract and parse YAML frontmatter. Returns (parsed_dict, error_message)."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, "No YAML frontmatter found (should start with --- and end with ---)"

    try:
        return yaml.safe_load(match.group(1)), None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML syntax: {str(e)}"

def count_bash_commands(content: str) -> int:
    """Count bash commands (! prefix patterns)."""
    # Match !`command` or !`command with spaces`
    pattern = r'!\s*`[^`]+`'
    return len(re.findall(pattern, content))

def count_file_references(content: str) -> int:
    """Count @ file references."""
    # Match @path/to/file.ext
    pattern = r'@[a-zA-Z0-9_/\-\.]+\.[a-zA-Z0-9]+'
    return len(re.findall(pattern, content))

def count_skill_references(content: str) -> int:
    """Count @ skill references."""
    # Match @skill-name (no file extension)
    pattern = r'@[a-zA-Z0-9_\-]+(?![a-zA-Z0-9_/\-\.])'
    return len(re.findall(pattern, content))

def count_skill_invocations(content: str) -> int:
    """Count Skill(command="xyz") invocations."""
    pattern = r'Skill\s*\(\s*command\s*=\s*["\'][^"\']+["\']\s*\)'
    return len(re.findall(pattern, content))

def count_task_invocations(content: str) -> int:
    """Count Task(...) invocations."""
    pattern = r'Task\s*\('
    return len(re.findall(pattern, content))

def find_person_usage(content: str) -> List[Tuple[int, str]]:
    """Find first/second person usage with line numbers.

    Note: Pattern-based check. May flag content in example blocks or
    technical documentation. Context matters - review flagged items.
    """
    patterns = [
        r'\b[Yy]ou\s+(?:should|must|can|will|need|may|might)',
        r'\b[Yy]our\s+',
        r'\bI\s+(?:will|can|recommend|suggest)',
        r'\b[Ww]e\s+(?:will|should|can|need)',
    ]

    found = []
    lines = content.split('\n')
    in_code_block = False

    for i, line in enumerate(lines, 1):
        # Track code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip markdown headers and code blocks
        if line.strip().startswith('#') or in_code_block:
            continue

        # Remove inline code before checking
        if '`' in line:
            line_without_code = re.sub(r'`[^`]+`', '', line)
        else:
            line_without_code = line

        for pattern in patterns:
            match = re.search(pattern, line_without_code)
            if match:
                found.append((i, match.group().strip()))
    return found

def find_time_sensitive(content: str) -> List[Tuple[int, str]]:
    """Find time-sensitive phrases with line numbers.

    Note: Pattern-based check. Often flags technical terms like 'current branch'
    or 'latest commit'. Context matters - review flagged items.
    """
    patterns = [
        (r'\b20\d{2}\b', 'year'),
        (r'\bcurrent(?:ly)?\b', 'current/currently'),
        (r'\bas of\b', 'as of'),
        (r'\brecent(?:ly)?\b', 'recent/recently'),
        (r'\blatest\b', 'latest'),
        (r'\btoday\b', 'today'),
        (r'\bnow\b', 'now'),
    ]

    found = []
    lines = content.split('\n')
    in_code_block = False

    for i, line in enumerate(lines, 1):
        # Track code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip code blocks
        if in_code_block:
            continue

        for pattern, label in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                found.append((i, label))
    return found

def has_windows_paths(content: str) -> bool:
    """Check for Windows-style backslash paths."""
    return bool(re.search(r'[a-zA-Z]:\\', content))

def find_absolute_paths(content: str) -> List[Tuple[int, str, str]]:
    """Find user-specific absolute paths that break portability."""
    patterns = [
        (r'/home/[a-zA-Z0-9_\-]+/', 'Linux home directory'),
        (r'/Users/[a-zA-Z0-9_\-]+/', 'macOS home directory'),
        (r'C:\\Users\\[a-zA-Z0-9_\-]+\\', 'Windows home directory'),
        (r'/root/', 'Root home directory'),
    ]

    found = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Skip lines that are already using ~/ (portable)
        if '~/' in line or '${HOME}' in line or '$HOME' in line:
            continue

        for pattern, description in patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                path = match.group()
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()
                found.append((i, path, context, description))

    return found

def validate_command(command_path: Path) -> Tuple[List[ValidationIssue], int, int, Dict]:
    """Validate command file. Returns (issues, passed, total, metrics)."""
    issues = []
    passed = 0
    total = 17  # Total number of actual validation checks

    # Initialize metrics with defaults (updated later if validation proceeds)
    metrics = {
        'line_count': 0,
        'bash_commands': 0,
        'file_references': 0,
        'skill_references': 0,
        'skill_invocations': 0,
        'task_invocations': 0,
    }

    print_section("Category 1: File Structure (2 checks)")

    # Check 1: File exists
    if not command_path.exists():
        check_fail("Command file exists")
        issues.append(ValidationIssue(
            "Command file exists",
            str(command_path.parent),
            "File not found",
            "Command .md file",
            f"Create command file at {command_path}"
        ))
        return issues, 0, total, metrics

    check_pass("Command file exists")
    passed += 1

    # Check 2: Read file content
    try:
        with open(command_path, 'r', encoding='utf-8') as f:
            content = f.read()
        check_pass("Command file readable")
        passed += 1
    except Exception as e:
        check_fail("Command file readable")
        issues.append(ValidationIssue(
            "Command file readable",
            str(command_path),
            f"Cannot read file: {e}",
            "Readable UTF-8 encoded file",
            "Ensure file has proper encoding and permissions"
        ))
        return issues, passed, total, metrics

    # Update metrics immediately after reading file
    line_count = len(content.splitlines())
    metrics['line_count'] = line_count

    # ==================== CATEGORY 2: FRONTMATTER STRUCTURE ====================
    print_section("Category 2: Frontmatter Structure (2 checks)")

    frontmatter, fm_error = parse_yaml_frontmatter(content)

    # Check 3: Valid YAML
    if fm_error:
        check_fail("Valid YAML frontmatter")
        issues.append(ValidationIssue(
            "Valid YAML frontmatter",
            "Command file lines 1-N",
            fm_error,
            "Valid YAML between --- delimiters",
            "Fix YAML syntax. Format:\n---\nallowed-tools: ...\n---"
        ))
        return issues, passed, total, metrics

    check_pass("Valid YAML frontmatter")
    passed += 1

    # Check 4: Required fields
    required_fields = ['allowed-tools', 'argument-hint', 'description', 'model']
    missing_fields = [f for f in required_fields if f not in frontmatter]

    if missing_fields:
        check_fail(f"Required fields present: {', '.join(required_fields)}")
        issues.append(ValidationIssue(
            "Required frontmatter fields",
            "Command frontmatter",
            f"Missing: {', '.join(missing_fields)}",
            "All required fields present",
            f"Add missing fields to frontmatter:\n{chr(10).join(f'{f}: ...' for f in missing_fields)}"
        ))
        return issues, passed, total, metrics

    check_pass(f"Required fields present: {', '.join(required_fields)}")
    passed += 1

    # ==================== CATEGORY 3: FRONTMATTER CONTENT ====================
    print_section("Category 3: Frontmatter Content (4 checks)")

    description = frontmatter.get('description', '')
    model = frontmatter.get('model', '')
    allowed_tools = frontmatter.get('allowed-tools', '')

    # Check 5: Description length
    # Target is ~10 words (≤100 chars is generous)
    if len(description) <= 100:
        check_pass(f"description length ≤100 chars (actual: {len(description)})")
        passed += 1
    else:
        check_fail(f"description length ≤100 chars (actual: {len(description)})")
        issues.append(ValidationIssue(
            "description length",
            "frontmatter.description",
            f"{len(description)} characters",
            "≤100 characters (~10 words)",
            f"Shorten description: '{description}'"
        ))

    # Check 6: Model value valid
    valid_models = ['sonnet', 'haiku', 'opus']
    if model in valid_models:
        check_pass(f"model value valid: '{model}'")
        passed += 1
    else:
        check_fail(f"model value valid (found: '{model}')")
        issues.append(ValidationIssue(
            "model value",
            "frontmatter.model",
            f"'{model}'",
            f"One of: {', '.join(valid_models)}",
            f"Set model to one of: {', '.join(valid_models)}"
        ))

    # Check 7: allowed-tools is restrictive
    # Check for bare "Bash" without restrictions
    tools_str = str(allowed_tools)
    if re.search(r'\bBash(?!\()', tools_str):
        check_fail("allowed-tools is restrictive (found bare 'Bash')")
        issues.append(ValidationIssue(
            "allowed-tools restrictive",
            "frontmatter.allowed-tools",
            "Contains bare 'Bash' without restrictions",
            "Specific bash commands: Bash(git:*), Bash(npm:*)",
            "Replace 'Bash' with specific commands: Bash(git add:*), Bash(git commit:*)"
        ))
    else:
        check_pass("allowed-tools is restrictive")
        passed += 1

    # Check 8: Description uses third person
    desc_person = find_person_usage(description)
    if not desc_person:
        check_pass("description uses third person")
        passed += 1
    else:
        check_fail(f"description uses third person (found {len(desc_person)} violations)")
        examples = ', '.join(f"'{p}'" for _, p in desc_person[:3])
        issues.append(ValidationIssue(
            "description perspective",
            "frontmatter.description",
            f"First/second person: {examples}",
            "Third person only",
            "Rewrite in third person: 'Creates atomic commit' not 'Create atomic commit'"
        ))

    # ==================== CATEGORY 4: REQUIRED SECTIONS ====================
    print_section("Category 4: Required Sections (4 checks)")

    required_sections = [
        'Preflight Checks',
        'Context',
        ('Task Instructions', 'Your Task'),  # Accept either variant
        'Success Criteria'
    ]

    for section_spec in required_sections:
        if isinstance(section_spec, tuple):
            # Multiple acceptable names
            section_names = section_spec
            found = any(
                bool(re.search(rf'^#+\s+{re.escape(name)}', content, re.MULTILINE))
                for name in section_names
            )
            display_name = ' or '.join(f"'{name}'" for name in section_names)
        else:
            section_names = [section_spec]
            found = bool(re.search(rf'^#+\s+{re.escape(section_spec)}', content, re.MULTILINE))
            display_name = f"'{section_spec}'"

        if found:
            check_pass(f"Section present: {display_name}")
            passed += 1
        else:
            check_fail(f"Section present: {display_name}")
            issues.append(ValidationIssue(
                f"Required section: {display_name}",
                "Command body",
                "Section not found",
                f"Section header with {display_name}",
                f"Add section: ## {section_names[0]}"
            ))

    # ==================== CATEGORY 5: COMMAND METRICS ====================
    print_section("Category 5: Command Metrics (6 checks)")

    # Collect metrics
    metrics = {
        'line_count': line_count,
        'bash_commands': count_bash_commands(content),
        'file_references': count_file_references(content),
        'skill_references': count_skill_references(content),
        'skill_invocations': count_skill_invocations(content),
        'task_invocations': count_task_invocations(content),
    }

    # Check 9: Line count
    if line_count <= 200:
        check_pass(f"line count ≤200 (actual: {line_count})")
        passed += 1
    else:
        check_warn(f"line count ≤200 (actual: {line_count}) - consider converting to skill")
        issues.append(ValidationIssue(
            "line count (warning)",
            "Command file",
            f"{line_count} lines",
            "≤200 lines (commands should be concise)",
            f"Consider converting to skill if complexity warrants it. Commands >200 lines should be skills.",
            severity="warning"
        ))
        passed += 1  # Warning, not a failure

    # Check 10: Has bash commands (preflight checks)
    if metrics['bash_commands'] > 0:
        check_pass(f"has bash commands (! prefix): {metrics['bash_commands']}")
        passed += 1
    else:
        check_warn("has bash commands (! prefix) - no preflight checks found")
        issues.append(ValidationIssue(
            "bash commands (warning)",
            "Command body",
            "0 bash commands found",
            "At least some preflight checks with !`command`",
            "Add preflight checks: - Check: !`git rev-parse --git-dir`",
            severity="warning"
        ))
        passed += 1  # Warning, not a failure

    # Metrics reporting (informational, not counted as checks)
    check_info(f"File references (@path): {metrics['file_references']}")
    check_info(f"Skill references (@skill-name): {metrics['skill_references']}")
    check_info(f"Skill() invocations: {metrics['skill_invocations']}")
    check_info(f"Task() invocations: {metrics['task_invocations']}")

    # ==================== CATEGORY 6: WRITING STYLE ====================
    print_section("Category 6: Writing Style (3 checks)")

    # Check 16: Imperative form (no you/I/we in body)
    body_person = find_person_usage(content)
    if not body_person:
        check_pass("uses imperative form (no 'you'/'I'/'we')")
        passed += 1
    else:
        check_fail(f"uses imperative form (found {len(body_person)} violations)")
        examples = '\n    '.join(f"Line {line}: '{text}'" for line, text in body_person[:5])
        issues.append(ValidationIssue(
            "imperative form",
            "Command body",
            f"{len(body_person)} first/second person instances",
            "Imperative/directive form throughout",
            f"Rewrite these lines:\n    {examples}\n    Use 'Run X' not 'You should run X'"
        ))

    # Check 17: No time-sensitive content (WARNING ONLY)
    time_refs = find_time_sensitive(content)
    if not time_refs:
        check_pass("no time-sensitive content")
        passed += 1
    else:
        check_warn(f"time-sensitive content detected ({len(time_refs)} instances) - review manually")
        examples = '\n    '.join(f"Line {line}: '{text}'" for line, text in time_refs[:5])
        issues.append(ValidationIssue(
            "time-sensitive content (warning)",
            "Command body",
            f"{len(time_refs)} potential time references",
            "Avoid dates, 'current', 'latest' when referring to command creation time",
            f"Review these manually - may be false positives:\n    {examples}",
            severity="warning"
        ))
        passed += 1  # Warning only

    # Check 18: No Windows paths
    if not has_windows_paths(content):
        check_pass("no Windows-style paths")
        passed += 1
    else:
        check_fail("no Windows-style paths")
        issues.append(ValidationIssue(
            "path style",
            "Command body",
            "Found backslash paths (C:\\...)",
            "Forward slashes only",
            "Replace all \\ with / in file paths"
        ))

    return issues, passed, total, metrics

def print_summary_minimal(issues: List[ValidationIssue], passed: int, total: int, metrics: Dict, command_name: str):
    """Print minimal command validation summary - one line + failures only."""
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    percentage = (passed / total * 100) if total > 0 else 0

    # One-line summary
    status = "✓ PASS" if passed == total else "✗ FAIL"
    print(f"{command_name}: {passed}/{total} ({percentage:.0f}%) | {len(errors)} errors, {len(warnings)} warnings | {status}")

    # Metrics summary
    print(f"Metrics: {metrics['line_count']} lines | {metrics['bash_commands']} bash cmds | " +
          f"{metrics['file_references']} @files | {metrics['skill_references']} @skills | " +
          f"{metrics['skill_invocations']} Skill() | {metrics['task_invocations']} Task()")

    # Only list errors with concise fixes
    if errors:
        print(f"\nErrors:")
        for issue in errors:
            print(f"  ✗ {issue.check}: {issue.fix}")

    # List warnings if any
    if warnings:
        print(f"\nWarnings:")
        for issue in warnings:
            print(f"  ⚠ {issue.check}")

    # Recommendations based on metrics
    print(f"\nRecommendations:")
    if metrics['line_count'] > 200:
        print(f"  • Consider converting to skill (>{200} lines)")
    if metrics['bash_commands'] == 0:
        print(f"  • Add preflight checks with !`command` syntax")
    if metrics['skill_invocations'] == 0 and metrics['skill_references'] > 0:
        print(f"  • Consider using Skill() invocations for explicit execution")

def print_summary(issues: List[ValidationIssue], passed: int, total: int, metrics: Dict):
    """Print command validation summary."""
    print_header("COMMAND VALIDATION SUMMARY")

    percentage = (passed / total * 100) if total > 0 else 0
    print(f"{Colors.BOLD}Result: {passed}/{total} checks passed ({percentage:.1f}%){Colors.END}")

    # Print metrics
    print(f"\n{Colors.BOLD}Command Metrics:{Colors.END}")
    print(f"  Lines: {metrics['line_count']}")
    print(f"  Bash commands (! prefix): {metrics['bash_commands']}")
    print(f"  File references (@path): {metrics['file_references']}")
    print(f"  Skill references (@skill-name): {metrics['skill_references']}")
    print(f"  Skill() invocations: {metrics['skill_invocations']}")
    print(f"  Task() invocations: {metrics['task_invocations']}")

    # Separate errors from warnings
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ PASS{Colors.END}")
        print("Command meets all validation requirements.")

        if warnings:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ {len(warnings)} WARNING(S){Colors.END}")
            print("Review warnings below (not blocking):\n")
            for i, warning in enumerate(warnings, 1):
                print(f"{Colors.BOLD}Warning {i}/{len(warnings)}:{Colors.END}\n")
                print(warning)
                print()
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ FAIL{Colors.END}")
        print(f"Fix {len(errors)} error(s) and re-run validation.\n")

        for i, issue in enumerate(errors, 1):
            print(f"{Colors.BOLD}Error {i}/{len(errors)}:{Colors.END}\n")
            print(issue)
            print()

        if warnings:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ {len(warnings)} WARNING(S){Colors.END}")
            print("Review warnings below (not blocking):\n")
            for i, warning in enumerate(warnings, 1):
                print(f"{Colors.BOLD}Warning {i}/{len(warnings)}:{Colors.END}\n")
                print(warning)
                print()

    # Recommendations
    print(f"\n{Colors.BOLD}Recommendations:{Colors.END}")
    if metrics['line_count'] > 200:
        print(f"  {Colors.YELLOW}•{Colors.END} Command is {metrics['line_count']} lines. Consider converting to skill for better organization.")
    if metrics['bash_commands'] == 0:
        print(f"  {Colors.YELLOW}•{Colors.END} No preflight checks found. Add validation with !`command` syntax.")
    if metrics['skill_invocations'] == 0 and metrics['skill_references'] > 0:
        print(f"  {Colors.CYAN}•{Colors.END} Consider using Skill() invocations for explicit skill execution.")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Comprehensive command validation and analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_command.py /path/to/command.md
  python3 scripts/validate_command.py /path/to/command.md --minimal

Minimal Mode:
  Use --minimal for quick iteration. Shows only:
  - One-line score summary with metrics
  - Failures with concise fix recommendations
  - Recommendations based on metrics
  - Suppresses all passing checks and verbose output
        """
    )

    parser.add_argument('command_path', type=Path, help='Path to command .md file')
    parser.add_argument('--minimal', action='store_true',
                        help='Minimal output mode: one-line score + failures only')

    args = parser.parse_args()

    # Set minimal mode flag
    if args.minimal:
        set_minimal_mode(True)

    command_path = args.command_path

    if not command_path.exists():
        print(f"{Colors.RED}Error: Path does not exist: {command_path}{Colors.END}")
        sys.exit(1)

    if not command_path.is_file():
        print(f"{Colors.RED}Error: Not a file: {command_path}{Colors.END}")
        sys.exit(1)

    command_name = command_path.stem
    minimal = args.minimal

    # Print header (suppressed in minimal mode)
    print_header(f"COMMAND VALIDATION: {command_name}")
    if not minimal:
        print(f"Path: {command_path}")
        print(f"Goal: 100% pass rate (20/20 checks)")

    # Run validation
    issues, passed, total, metrics = validate_command(command_path)

    if minimal:
        print_summary_minimal(issues, passed, total, metrics, command_name)
    else:
        print_summary(issues, passed, total, metrics)

    # Exit code
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
