#!/usr/bin/env python3
"""
Comprehensive subagent validation script.

Validates subagent structure, counts subagent-specific metrics (word count,
tool count, skill references), and provides quality analysis.

Usage:
    python3 scripts/validate_subagent.py /path/to/subagent.md
    python3 scripts/validate_subagent.py /path/to/subagent.md --minimal
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

def parse_yaml_frontmatter(content: str) -> Tuple[Optional[dict], Optional[str], str]:
    """Extract and parse YAML frontmatter. Returns (parsed_dict, error_message, body_content)."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, "No YAML frontmatter found (should start with --- and end with ---)", ""

    try:
        return yaml.safe_load(match.group(1)), None, match.group(2)
    except yaml.YAMLError as e:
        return None, f"Invalid YAML syntax: {str(e)}", ""

def count_words(text: str) -> int:
    """Count words in text, excluding code blocks."""
    # Remove code blocks
    text_without_code = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text_without_code = re.sub(r'`[^`]+`', '', text_without_code)
    # Count words
    words = text_without_code.split()
    return len(words)

def count_skill_invocations(content: str) -> int:
    """Count Skill() invocations."""
    # Match Skill(command='skill-name') or Skill(command="skill-name")
    skill_calls = len(re.findall(r'Skill\s*\(\s*command\s*=\s*["\'][^"\']+["\']\s*\)', content))
    return skill_calls

def check_gerund_form(name: str) -> bool:
    """Check if name uses gerund form (-ing pattern)."""
    return bool(re.search(r'(ing-|-ing$)', name))

def find_person_usage(content: str) -> List[Tuple[int, str]]:
    """Find first/second person usage with line numbers."""
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

        # Skip markdown headers
        if line.strip().startswith('#'):
            continue

        # Skip inline code (backtick content)
        if in_code_block or '`' in line:
            # For inline code, remove backtick content before checking
            if not in_code_block:
                line_without_code = re.sub(r'`[^`]+`', '', line)
            else:
                continue
        else:
            line_without_code = line

        for pattern in patterns:
            match = re.search(pattern, line_without_code)
            if match:
                found.append((i, match.group().strip()))
    return found

def find_time_sensitive(content: str) -> List[Tuple[int, str]]:
    """Find time-sensitive phrases with line numbers."""
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
    for i, line in enumerate(lines, 1):
        for pattern, label in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                found.append((i, label))
    return found

def has_windows_paths(content: str) -> bool:
    """Check for Windows-style backslash paths."""
    return bool(re.search(r'[a-zA-Z]:\\', content))

def validate_subagent(subagent_path: Path) -> Tuple[List[ValidationIssue], int, int, Dict]:
    """Validate subagent file. Returns (issues, passed, total, metrics)."""
    issues = []
    passed = 0
    total = 15  # Total number of actual validation checks

    # Initialize metrics with defaults
    metrics = {
        'line_count': 0,
        'word_count': 0,
        'tool_count': 0,
        'skill_references': 0,
    }

    print_section("Category 1: File Structure (2 checks)")

    # Check 1: File exists
    if not subagent_path.exists():
        check_fail("Subagent file exists")
        issues.append(ValidationIssue(
            "Subagent file exists",
            str(subagent_path.parent),
            "File not found",
            "Subagent .md file",
            f"Create subagent file at {subagent_path}"
        ))
        return issues, 0, total, metrics

    check_pass("Subagent file exists")
    passed += 1

    # Check 2: Read file content
    try:
        with open(subagent_path, 'r', encoding='utf-8') as f:
            content = f.read()
        check_pass("Subagent file readable")
        passed += 1
    except Exception as e:
        check_fail("Subagent file readable")
        issues.append(ValidationIssue(
            "Subagent file readable",
            str(subagent_path),
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

    frontmatter, fm_error, body_content = parse_yaml_frontmatter(content)

    # Check 3: Valid YAML
    if fm_error:
        check_fail("Valid YAML frontmatter")
        issues.append(ValidationIssue(
            "Valid YAML frontmatter",
            "Subagent file lines 1-N",
            fm_error,
            "Valid YAML between --- delimiters",
            "Fix YAML syntax. Format:\n---\nname: ...\ndescription: ...\n---"
        ))
        return issues, passed, total, metrics

    check_pass("Valid YAML frontmatter")
    passed += 1

    # Check 4: Required fields
    required_fields = ['name', 'description', 'tools', 'model', 'color']
    missing_fields = [f for f in required_fields if f not in frontmatter]

    if missing_fields:
        check_fail(f"Required fields present: {', '.join(required_fields)}")
        issues.append(ValidationIssue(
            "Required frontmatter fields",
            "Subagent frontmatter",
            f"Missing: {', '.join(missing_fields)}",
            "All required fields present",
            f"Add missing fields to frontmatter:\n{chr(10).join(f'{f}: ...' for f in missing_fields)}"
        ))
        return issues, passed, total, metrics

    check_pass(f"Required fields present: {', '.join(required_fields)}")
    passed += 1

    # ==================== CATEGORY 3: FRONTMATTER CONTENT ====================
    print_section("Category 3: Frontmatter Content (5 checks)")

    name = frontmatter.get('name', '')
    description = frontmatter.get('description', '')
    model = frontmatter.get('model', '')
    color = frontmatter.get('color', '')
    tools = frontmatter.get('tools', '')

    # Check 5: Name length
    if len(name) <= 64:
        check_pass(f"name length ≤64 chars (actual: {len(name)})")
        passed += 1
    else:
        check_fail(f"name length ≤64 chars (actual: {len(name)})")
        issues.append(ValidationIssue(
            "name field length",
            "frontmatter.name",
            f"{len(name)} characters",
            "≤64 characters",
            f"Shorten name: '{name}'"
        ))

    # Check 6: Model value valid
    valid_models = ['inherit', 'sonnet', 'haiku', 'opus']
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

    # Check 7: Color value valid
    valid_colors = ['purple', 'blue', 'green', 'yellow', 'orange', 'red', 'cyan', 'magenta', 'white']
    if color in valid_colors:
        check_pass(f"color value valid: '{color}'")
        passed += 1
    else:
        check_fail(f"color value valid (found: '{color}')")
        issues.append(ValidationIssue(
            "color value",
            "frontmatter.color",
            f"'{color}'",
            f"One of: {', '.join(valid_colors)}",
            f"Set color to one of: {', '.join(valid_colors)}\nSee references/color-codes.md"
        ))

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
            "Rewrite in third person: 'Creates...' not 'Create...'"
        ))

    # Check 9: Description includes proactive triggers
    trigger_indicators = [
        r'\buse proactively\b',
        r'\bproactive\b',
        r'\bwhen\b',
        r'\bafter\b',
    ]
    has_triggers = any(re.search(p, description, re.IGNORECASE) for p in trigger_indicators)

    if has_triggers:
        check_pass("description includes invocation patterns")
        passed += 1
    else:
        check_fail("description includes invocation patterns")
        issues.append(ValidationIssue(
            "description invocation patterns",
            "frontmatter.description",
            "No invocation pattern keywords found",
            "Explains WHEN to invoke the subagent",
            "Add invocation context: 'Use proactively when...' or 'Use after...'"
        ))

    # ==================== CATEGORY 4: PROMPT QUALITY ====================
    print_section("Category 4: Prompt Quality (3 checks)")

    # Update metrics
    word_count = count_words(body_content)
    metrics['word_count'] = word_count
    metrics['skill_references'] = count_skill_invocations(body_content)

    # Count tools
    if isinstance(tools, list):
        metrics['tool_count'] = len(tools)
    elif isinstance(tools, str):
        # Parse comma-separated or space-separated
        tool_list = [t.strip() for t in re.split(r'[,\s]+', tools) if t.strip()]
        metrics['tool_count'] = len(tool_list)
    else:
        metrics['tool_count'] = 0

    # Check 10: Word count (50-200 words target, warning if outside)
    if 50 <= word_count <= 200:
        check_pass(f"word count in target range (actual: {word_count})")
        passed += 1
    elif word_count < 50:
        check_warn(f"word count below target (actual: {word_count}, target: 50-200)")
        issues.append(ValidationIssue(
            "word count (warning)",
            "Subagent body",
            f"{word_count} words",
            "50-200 words for concise prompts",
            f"Consider adding more guidance if subagent needs it. Very brief prompts may lack clarity.",
            severity="warning"
        ))
        passed += 1  # Warning only
    else:  # > 200
        check_warn(f"word count above target (actual: {word_count}, target: 50-200)")
        issues.append(ValidationIssue(
            "word count (warning)",
            "Subagent body",
            f"{word_count} words",
            "50-200 words for concise prompts",
            f"Consider moving detailed instructions to a skill. Subagent prompts should be directive, not educational.",
            severity="warning"
        ))
        passed += 1  # Warning only

    # Check 11: Body content is directive (starts with imperative verbs)
    # Check first few non-empty lines after frontmatter
    body_lines = [line.strip() for line in body_content.split('\n') if line.strip()]
    if body_lines:
        first_line = body_lines[0]
        # Check if it starts with imperative/directive words or patterns
        directive_patterns = [
            r'^(Create|Build|Test|Validate|Verify|Check|Run|Execute|Analyze|Review|Implement|Generate|Use)',
            r'^(Invoke|Call|Apply|Follow|Consult)',
        ]
        is_directive = any(re.search(p, first_line, re.IGNORECASE) for p in directive_patterns)

        if is_directive:
            check_pass("prompt uses directive language")
            passed += 1
        else:
            check_warn("prompt may not be directive enough")
            issues.append(ValidationIssue(
                "directive language (warning)",
                "Subagent body",
                f"First line: '{first_line[:50]}...'",
                "Directive language (imperative verbs)",
                "Start with imperative verbs: 'Create...', 'Test...', 'Validate...'",
                severity="warning"
            ))
            passed += 1  # Warning only
    else:
        check_fail("prompt has content")
        issues.append(ValidationIssue(
            "prompt content",
            "Subagent body",
            "Empty body after frontmatter",
            "Non-empty prompt content",
            "Add subagent instructions after frontmatter"
        ))

    # Check 12: Has skill invocations (if word count > 100, expect skill invocations)
    if word_count > 100 and metrics['skill_references'] == 0:
        check_warn("consider using skill invocations for complex prompts")
        issues.append(ValidationIssue(
            "skill integration (warning)",
            "Subagent body",
            f"{word_count} words but no skill invocations",
            "Skill invocations for complex knowledge",
            "Consider moving detailed instructions to a skill and invoking it with Skill(command='...')",
            severity="warning"
        ))
        passed += 1  # Warning only, not counted as failure
    else:
        # This is informational, always pass
        passed += 1

    # ==================== CATEGORY 5: WRITING STYLE ====================
    print_section("Category 5: Writing Style (3 checks)")

    # Check 13: Imperative form (no you/I/we in body)
    body_person = find_person_usage(body_content)
    if not body_person:
        check_pass("uses imperative form (no 'you'/'I'/'we')")
        passed += 1
    else:
        check_fail(f"uses imperative form (found {len(body_person)} violations)")
        examples = '\n    '.join(f"Line {line}: '{text}'" for line, text in body_person[:5])
        issues.append(ValidationIssue(
            "imperative form",
            "Subagent body",
            f"{len(body_person)} first/second person instances",
            "Imperative/directive form throughout",
            f"Rewrite these lines:\n    {examples}\n    Use 'Create X' not 'You should create X'"
        ))

    # Check 14: No time-sensitive content (WARNING ONLY)
    time_refs = find_time_sensitive(content)
    if not time_refs:
        check_pass("no time-sensitive content")
        passed += 1
    else:
        check_warn(f"time-sensitive content detected ({len(time_refs)} instances) - review manually")
        examples = '\n    '.join(f"Line {line}: '{text}'" for line, text in time_refs[:5])
        issues.append(ValidationIssue(
            "time-sensitive content (warning)",
            "Subagent file",
            f"{len(time_refs)} potential time references",
            "Avoid dates, 'current', 'latest' when referring to subagent creation time",
            f"Review these manually - may be false positives:\n    {examples}",
            severity="warning"
        ))
        passed += 1  # Warning only

    # Check 15: No Windows paths
    if not has_windows_paths(content):
        check_pass("no Windows-style paths")
        passed += 1
    else:
        check_fail("no Windows-style paths")
        issues.append(ValidationIssue(
            "path style",
            "Subagent file",
            "Found backslash paths (C:\\...)",
            "Forward slashes only",
            "Replace all \\ with / in file paths"
        ))

    # ==================== METRICS REPORTING ====================
    print_section("Subagent Metrics")

    check_info(f"Word count: {metrics['word_count']} (target: 50-200)")
    check_info(f"Tool count: {metrics['tool_count']}")
    check_info(f"Skill invocations: {metrics['skill_references']}")

    return issues, passed, total, metrics

def print_summary_minimal(issues: List[ValidationIssue], passed: int, total: int, metrics: Dict, subagent_name: str):
    """Print minimal subagent validation summary - one line + failures only."""
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    percentage = (passed / total * 100) if total > 0 else 0

    # One-line summary
    status = "✓ PASS" if len(errors) == 0 else "✗ FAIL"
    print(f"{subagent_name}: {passed}/{total} ({percentage:.0f}%) | {len(errors)} errors, {len(warnings)} warnings | {status}")

    # Metrics summary
    print(f"Metrics: {metrics['word_count']} words (target: 50-200) | " +
          f"{metrics['tool_count']} tools | {metrics['skill_references']} Skill() calls")

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
    if metrics['word_count'] < 50:
        print(f"  • Prompt may be too brief ({metrics['word_count']} words) - consider adding more guidance")
    elif metrics['word_count'] > 200:
        print(f"  • Prompt is verbose ({metrics['word_count']} words) - consider moving knowledge to a skill")
    if metrics['word_count'] > 100 and metrics['skill_references'] == 0:
        print(f"  • Complex prompt with no Skill() invocations - consider skill integration")
    if metrics['tool_count'] > 10:
        print(f"  • Many tools ({metrics['tool_count']}) - ensure all are necessary")

def print_summary(issues: List[ValidationIssue], passed: int, total: int, metrics: Dict):
    """Print subagent validation summary."""
    print_header("SUBAGENT VALIDATION SUMMARY")

    percentage = (passed / total * 100) if total > 0 else 0
    print(f"{Colors.BOLD}Result: {passed}/{total} checks passed ({percentage:.1f}%){Colors.END}")

    # Print metrics
    print(f"\n{Colors.BOLD}Subagent Metrics:{Colors.END}")
    print(f"  Lines: {metrics['line_count']}")
    print(f"  Words: {metrics['word_count']} (target: 50-200)")
    print(f"  Tools: {metrics['tool_count']}")
    print(f"  Skill() invocations: {metrics['skill_references']}")

    # Separate errors from warnings
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    if len(errors) == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ PASS{Colors.END}")
        print("Subagent meets all validation requirements.")

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
    if metrics['word_count'] < 50:
        print(f"  {Colors.YELLOW}•{Colors.END} Prompt is brief ({metrics['word_count']} words). Ensure clarity is maintained.")
    elif metrics['word_count'] > 200:
        print(f"  {Colors.YELLOW}•{Colors.END} Prompt is verbose ({metrics['word_count']} words). Consider creating a skill for detailed instructions.")
    if metrics['word_count'] > 100 and metrics['skill_references'] == 0:
        print(f"  {Colors.CYAN}•{Colors.END} Complex prompt without Skill() invocations. Consider skill integration for maintainability.")
    if metrics['tool_count'] > 10:
        print(f"  {Colors.YELLOW}•{Colors.END} Many tools granted ({metrics['tool_count']}). Verify all are necessary.")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Comprehensive subagent validation and analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_subagent.py /path/to/subagent.md
  python3 scripts/validate_subagent.py /path/to/subagent.md --minimal

Minimal Mode:
  Use --minimal for quick iteration. Shows only:
  - One-line score summary with metrics
  - Failures with concise fix recommendations
  - Recommendations based on metrics
  - Suppresses all passing checks and verbose output
        """
    )

    parser.add_argument('subagent_path', type=Path, help='Path to subagent .md file')
    parser.add_argument('--minimal', action='store_true',
                        help='Minimal output mode: one-line score + failures only')

    args = parser.parse_args()

    # Set minimal mode flag
    if args.minimal:
        set_minimal_mode(True)

    subagent_path = args.subagent_path

    if not subagent_path.exists():
        print(f"{Colors.RED}Error: Path does not exist: {subagent_path}{Colors.END}")
        sys.exit(1)

    if not subagent_path.is_file():
        print(f"{Colors.RED}Error: Not a file: {subagent_path}{Colors.END}")
        sys.exit(1)

    subagent_name = subagent_path.stem
    minimal = args.minimal

    # Print header (suppressed in minimal mode)
    print_header(f"SUBAGENT VALIDATION: {subagent_name}")
    if not minimal:
        print(f"Path: {subagent_path}")
        print(f"Goal: 100% pass rate (15/15 checks)")

    # Run validation
    issues, passed, total, metrics = validate_subagent(subagent_path)

    if minimal:
        print_summary_minimal(issues, passed, total, metrics, subagent_name)
    else:
        print_summary(issues, passed, total, metrics)

    # Exit code: 0 if no errors, 1 if errors (warnings don't cause failure)
    errors = [issue for issue in issues if issue.severity == "error"]
    sys.exit(0 if len(errors) == 0 else 1)

if __name__ == "__main__":
    main()
