#!/usr/bin/env python3
"""
Comprehensive skill validation script.

Validates SKILL.md structure, analyzes reference materials, scripts, and templates,
and provides cross-reference analysis to identify documentation gaps.

Usage:
    python3 scripts/validate_skill.py /path/to/skill-folder
    python3 scripts/validate_skill.py /path/to/skill-folder --check skill
    python3 scripts/validate_skill.py /path/to/skill-folder --check references
    python3 scripts/validate_skill.py /path/to/skill-folder --check scripts
    python3 scripts/validate_skill.py /path/to/skill-folder --check templates
"""

import sys
import re
import yaml
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from collections import defaultdict

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
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

def check_skip(msg: str):
    """Print skipped check."""
    if not _MINIMAL_MODE:
        print(f"{Colors.YELLOW}⊘{Colors.END} {msg}")

def check_info(msg: str):
    """Print informational message."""
    if not _MINIMAL_MODE:
        print(f"{Colors.YELLOW}ℹ{Colors.END} {msg}")

def check_warn(msg: str):
    """Print warning check."""
    if not _MINIMAL_MODE:
        print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def parse_yaml_frontmatter(content: str) -> Tuple[Optional[dict], Optional[str]]:
    """Extract and parse YAML frontmatter. Returns (parsed_dict, error_message)."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, "No YAML frontmatter found (should start with --- and end with ---)"

    try:
        return yaml.safe_load(match.group(1)), None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML syntax: {str(e)}"

def check_gerund_form(name: str) -> bool:
    """Check if name uses gerund form (-ing pattern)."""
    return bool(re.search(r'(ing-|-ing$)', name))

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
    """Find user-specific absolute paths that break portability.

    Returns list of (line_number, path, context) tuples.
    """
    # Patterns for user-specific absolute paths (note: these pattern definitions
    # themselves may trigger in validation - this is expected and acceptable)
    patterns = [
        (r'/home/[a-zA-Z0-9_\-]+/', 'Linux home directory'),
        (r'/Users/[a-zA-Z0-9_\-]+/', 'macOS home directory'),
        (r'C:\\Users\\[a-zA-Z0-9_\-]+\\', 'Windows home directory'),
        (r'(?:^|[^a-zA-Z0-9])/root/', 'Root home directory'),
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
                # Get context around the match
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()
                found.append((i, path, context, description))

    return found

def check_file_depth(skill_path: Path) -> List[str]:
    """Find files nested deeper than 2 levels."""
    deep_files = []
    base_depth = len(skill_path.parts)

    for file_path in skill_path.rglob('*'):
        if file_path.is_file():
            # Skip build artifacts
            if '__pycache__' in str(file_path) or '.pyc' in str(file_path):
                continue

            depth = len(file_path.parts) - base_depth
            if depth > 2:
                deep_files.append(str(file_path.relative_to(skill_path)))

    return deep_files

def extract_headings(content: str) -> List[Tuple[int, str]]:
    """Extract all markdown headings with their levels, skipping code blocks."""
    headings = []
    in_code_block = False

    for line in content.split('\n'):
        # Track code block state (both ``` and ~~~)
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Extract heading if this is a heading line
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))

    return headings

def analyze_heading_hierarchy(headings: List[Tuple[int, str]]) -> Tuple[bool, List[str]]:
    """Check if heading hierarchy is correct (no level skipping)."""
    issues = []
    prev_level = 0

    for i, (level, title) in enumerate(headings):
        if prev_level > 0 and level > prev_level + 1:
            issues.append(f"Skips from H{prev_level} to H{level} - '{title}'")
        prev_level = level

    return len(issues) == 0, issues

def detect_bloat_patterns(content: str) -> Dict[str, List[str]]:
    """Detect basic redundancy patterns."""
    patterns = {
        'Redundancy': [
            (r'(?:for example|e\.g\.).*(?:another example|e\.g\.)', 'Multiple examples in close proximity'),
            (r'(?i)(?:as (?:mentioned|stated|discussed) (?:above|earlier|previously))', 'Repeated content references'),
        ]
    }

    findings = defaultdict(list)

    for category, pattern_list in patterns.items():
        for pattern, description in pattern_list:
            matches = list(re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE))
            if matches:
                findings[category].append(f"{description} ({len(matches)} occurrences)")

    return dict(findings)

def detect_high_density_patterns(content: str) -> Dict[str, int]:
    """Detect high-density information patterns."""
    patterns = {
        'Tables': r'\|[^\n]+\|[^\n]+\|',
        'Checklists': r'^\s*[-*]\s+\[[ xX]\]',
        'Numbered Lists': r'^\d+\.\s+',
        'Decision Trees': r'(?:if|when|where)[^\n]{5,50}(?:then|:|→)',
        'Code Blocks': r'```[\w]*\n',
        'Inline Code': r'`[^`]+`',
        'Definition Lists': r'^[\w\s]+:\s*$',
    }

    counts = {}
    for name, pattern in patterns.items():
        matches = re.findall(pattern, content, re.MULTILINE)
        counts[name] = len(matches)

    return counts

def calculate_density_score(content: str, density: Dict) -> int:
    """Calculate information density score (1-10) based on structural patterns."""
    lines = len(content.splitlines())
    words = len(content.split())

    if lines == 0 or words == 0:
        return 0

    # Structure bonuses (max 6 points)
    structure_score = 0
    if density['Tables'] > 0:
        structure_score += 2
    if density['Checklists'] > 0:
        structure_score += 2
    if density['Decision Trees'] > 0:
        structure_score += 1
    if density['Code Blocks'] > 5:
        structure_score += 1

    structure_score = min(structure_score, 6)

    # Base score from words per line (max 4 points)
    words_per_line = words / lines
    base_score = min(words_per_line / 3, 4)

    raw_score = base_score + structure_score
    final_score = max(1, min(10, int(raw_score)))

    return final_score

def find_resource_mentions(content: str, skill_path: Path) -> Dict[str, List[Tuple[int, str]]]:
    """Find all mentions of resources (scripts/, references/, templates/, assets/) in content.

    Returns dict mapping file paths to list of (line_number, context) tuples.
    """
    mentions = defaultdict(list)
    lines = content.split('\n')

    # Patterns to match resource paths
    patterns = [
        r'(?:scripts|references|templates|assets)/[\w\-./]+',
    ]

    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            for match in re.finditer(pattern, line):
                path = match.group()
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(line), match.end() + 50)
                context = line[start:end].strip()
                mentions[path].append((line_num, context))

    return dict(mentions)

def validate_skill_md(skill_path: Path) -> Tuple[List[ValidationIssue], int, int, str]:
    """Validate SKILL.md. Returns (issues, passed, total, content)."""
    issues = []
    passed = 0
    total = 23

    print_section("Category 1: File Structure (2 checks)")

    skill_md = skill_path / "SKILL.md"

    # Check 1: SKILL.md exists
    if not skill_md.exists():
        check_fail("SKILL.md exists")
        issues.append(ValidationIssue(
            "SKILL.md exists",
            str(skill_path),
            "SKILL.md not found",
            "SKILL.md file in skill root directory",
            "Create SKILL.md with proper YAML frontmatter and content"
        ))
        return issues, 0, total, ""

    check_pass("SKILL.md exists")
    passed += 1

    # Check 2: Read file content
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        check_pass("SKILL.md readable")
        passed += 1
    except Exception as e:
        check_fail("SKILL.md readable")
        issues.append(ValidationIssue(
            "SKILL.md readable",
            str(skill_md),
            f"Cannot read file: {e}",
            "Readable UTF-8 encoded file",
            "Ensure file has proper encoding and permissions"
        ))
        return issues, passed, total, ""

    line_count = len(content.splitlines())

    # ==================== CATEGORY 2: FRONTMATTER STRUCTURE ====================
    print_section("Category 2: Frontmatter Structure (3 checks)")

    frontmatter, fm_error = parse_yaml_frontmatter(content)

    # Check 3: Valid YAML
    if fm_error:
        check_fail("Valid YAML frontmatter")
        issues.append(ValidationIssue(
            "Valid YAML frontmatter",
            "SKILL.md lines 1-N",
            fm_error,
            "Valid YAML between --- delimiters",
            "Fix YAML syntax. Format:\n---\nname: skill-name\ndescription: ...\n---"
        ))
        return issues, passed, total, content

    check_pass("Valid YAML frontmatter")
    passed += 1

    # Check 4: Required fields
    required_fields = ['name', 'description']
    missing_fields = [f for f in required_fields if f not in frontmatter]

    if missing_fields:
        check_fail(f"Required fields present: {', '.join(required_fields)}")
        issues.append(ValidationIssue(
            "Required frontmatter fields",
            "SKILL.md frontmatter",
            f"Missing: {', '.join(missing_fields)}",
            "Both 'name' and 'description' fields present",
            f"Add missing fields to frontmatter:\n{chr(10).join(f'{f}: ...' for f in missing_fields)}"
        ))
        return issues, passed, total, content

    check_pass(f"Required fields present: {', '.join(required_fields)}")
    passed += 1

    # Check 4.5: Only valid keys (Claude schema)
    valid_keys = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    invalid_keys = set(frontmatter.keys()) - valid_keys

    if invalid_keys:
        check_fail(f"Only valid frontmatter keys (found invalid: {', '.join(invalid_keys)})")
        issues.append(ValidationIssue(
            "Invalid frontmatter keys",
            "SKILL.md frontmatter",
            f"Invalid keys: {', '.join(invalid_keys)}",
            f"Valid keys: {', '.join(sorted(valid_keys))}",
            f"Remove invalid keys and move content to description if needed:\n- Remove: {', '.join(invalid_keys)}\n- Valid keys: name, description, license, allowed-tools, metadata"
        ))
    else:
        check_pass(f"Only valid frontmatter keys: {', '.join(sorted(frontmatter.keys()))}")
        passed += 1

    # ==================== CATEGORY 3: FRONTMATTER CONTENT ====================
    print_section("Category 3: Frontmatter Content (4 checks)")

    name = frontmatter['name']
    description = frontmatter['description']

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

    # Check 6: Name uses gerund form
    if check_gerund_form(name):
        check_pass(f"name uses gerund form: '{name}'")
        passed += 1
    else:
        check_fail(f"name uses gerund form: '{name}'")
        issues.append(ValidationIssue(
            "name gerund form",
            "frontmatter.name",
            f"'{name}' (no -ing pattern)",
            "Gerund form (e.g., 'processing-pdfs', 'creating-skills')",
            "Rename using gerund: verb-ing-noun or noun-verb-ing"
        ))

    # Check 7: Name avoids generic terms
    generic_terms = ['helper', 'utils', 'tools', 'misc', 'common']
    found_generic = [t for t in generic_terms if t in name.lower()]

    if not found_generic:
        check_pass("name avoids generic terms")
        passed += 1
    else:
        check_fail(f"name avoids generic terms (found: {', '.join(found_generic)})")
        issues.append(ValidationIssue(
            "name specificity",
            "frontmatter.name",
            f"Contains generic: {', '.join(found_generic)}",
            "Specific, descriptive name",
            f"Replace '{found_generic[0]}' with specific domain term"
        ))

    # Check 8: Description length
    if len(description) <= 1024:
        check_pass(f"description length ≤1024 chars (actual: {len(description)})")
        passed += 1
    else:
        check_fail(f"description length ≤1024 chars (actual: {len(description)})")
        issues.append(ValidationIssue(
            "description length",
            "frontmatter.description",
            f"{len(description)} characters",
            "≤1024 characters",
            "Condense description to essential purpose and triggers only"
        ))

    # ==================== CATEGORY 4: DESCRIPTION CONTENT ====================
    print_section("Category 4: Description Content (2 checks)")

    # Check 9: Third person (no you/I/we)
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
            "Third person only (e.g., 'This skill...')",
            "Rewrite: 'This skill does X' not 'You can do X' or 'I/We do X'"
        ))

    # Check 10: Description includes triggers
    trigger_indicators = [
        r'\bwhen\b',
        r'\bfor\b',
        r'\bshould be used\b',
        r'\btriggers? on\b',
    ]
    has_triggers = any(re.search(p, description, re.IGNORECASE) for p in trigger_indicators)

    if has_triggers:
        check_pass("description includes usage triggers")
        passed += 1
    else:
        check_fail("description includes usage triggers")
        issues.append(ValidationIssue(
            "description triggers",
            "frontmatter.description",
            "No trigger keywords found",
            "Explains WHEN to use the skill",
            "Add trigger context: 'This skill should be used when...' or 'Triggers on...'"
        ))

    # ==================== CATEGORY 5: WRITING STYLE ====================
    print_section("Category 5: Writing Style (4 checks)")

    # Check 11: Imperative form (no you/I/we in body)
    body_person = find_person_usage(content)
    if not body_person:
        check_pass("uses imperative form (no 'you'/'I'/'we')")
        passed += 1
    else:
        check_fail(f"uses imperative form (found {len(body_person)} violations)")
        examples = '\n    '.join(f"Line {line}: '{text}'" for line, text in body_person[:5])
        issues.append(ValidationIssue(
            "imperative form",
            "SKILL.md body",
            f"{len(body_person)} first/second person instances",
            "Imperative/infinitive form throughout",
            f"Rewrite these lines:\n    {examples}\n    Use 'To do X, run Y' not 'You should run Y'"
        ))

    # Check 12: No time-sensitive content (WARNING ONLY - not counted as failure)
    time_refs = find_time_sensitive(content)
    if not time_refs:
        check_pass("no time-sensitive content")
        passed += 1
    else:
        check_warn(f"time-sensitive content detected ({len(time_refs)} instances) - review manually")
        examples = '\n    '.join(f"Line {line}: '{text}'" for line, text in time_refs[:5])
        issues.append(ValidationIssue(
            "time-sensitive content (warning)",
            "SKILL.md",
            f"{len(time_refs)} potential time references",
            "Avoid dates, 'current', 'latest', 'recent' when referring to document creation time",
            f"Review these manually - may be false positives (e.g., 'current branch', 'recent commits'):\n    {examples}",
            severity="warning"
        ))
        # Still count as passed since it's just a warning
        passed += 1

    # Check 13: No Windows paths
    if not has_windows_paths(content):
        check_pass("no Windows-style paths")
        passed += 1
    else:
        check_fail("no Windows-style paths")
        issues.append(ValidationIssue(
            "path style",
            "SKILL.md",
            "Found backslash paths (C:\\...)",
            "Forward slashes only",
            "Replace all \\ with / in file paths"
        ))

    # Check 14: No user-specific absolute paths
    absolute_paths = find_absolute_paths(content)
    if not absolute_paths:
        check_pass("no user-specific absolute paths")
        passed += 1
    else:
        check_fail(f"no user-specific absolute paths (found {len(absolute_paths)} instances)")
        examples = '\n    '.join(f"Line {line}: '{path}' ({desc})" for line, path, _, desc in absolute_paths[:5])
        issues.append(ValidationIssue(
            "portable paths",
            "SKILL.md",
            f"{len(absolute_paths)} user-specific absolute paths",
            "Use relative paths or ~/ for portability",
            f"Replace these absolute paths:\n    {examples}\n    Use '~/' instead of '/home/user/', or use relative paths"
        ))

    # ==================== CATEGORY 6: FILE STRUCTURE ====================
    print_section("Category 6: File Structure (2 checks)")

    # Check 15: File size
    if line_count <= 500:
        check_pass(f"file size ≤500 lines (actual: {line_count})")
        passed += 1
    else:
        check_fail(f"file size ≤500 lines (actual: {line_count})")
        issues.append(ValidationIssue(
            "file size",
            "SKILL.md",
            f"{line_count} lines",
            "≤500 lines",
            "Move detailed content to references/ files. Keep only core workflow in SKILL.md"
        ))

    # Check 16: Has section headers
    has_headers = bool(re.search(r'^#{1,3}\s+\w+', content, re.MULTILINE))
    if has_headers:
        check_pass("contains section headers")
        passed += 1
    else:
        check_fail("contains section headers")
        issues.append(ValidationIssue(
            "section headers",
            "SKILL.md",
            "No markdown headers found",
            "Structured sections with headers",
            "Add headers: # Main Section, ## Subsection, ### Detail"
        ))

    # ==================== CATEGORY 7: DIRECTORY STRUCTURE ====================
    print_section("Category 7: Directory Structure (3 checks)")

    # Check 17: No deep nesting
    deep_files = check_file_depth(skill_path)
    if not deep_files:
        check_pass("no deep file nesting (max 2 levels)")
        passed += 1
    else:
        check_fail(f"no deep file nesting (found {len(deep_files)} deep files)")
        examples = '\n    '.join(deep_files[:3])
        issues.append(ValidationIssue(
            "file nesting",
            "skill directory",
            f"{len(deep_files)} files nested >2 levels",
            "Max 2 levels (skill/dir/file.ext)",
            f"Flatten these:\n    {examples}"
        ))

    # Check 18: References mentioned if they exist
    refs_dir = skill_path / "references"
    if refs_dir.exists() and any(refs_dir.iterdir()):
        has_ref_mentions = bool(re.search(r'references?/', content, re.IGNORECASE))
        if has_ref_mentions:
            check_pass("references/ mentioned in SKILL.md")
            passed += 1
        else:
            check_fail("references/ mentioned in SKILL.md")
            issues.append(ValidationIssue(
                "reference mentions",
                "SKILL.md",
                "references/ exists but not mentioned",
                "References cited in content",
                "Add references: 'See references/filename.md for details'"
            ))
    else:
        check_skip("references/ mentioned (N/A - no references)")
        passed += 1

    # Check 19: Scripts mentioned if they exist
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists() and any(scripts_dir.iterdir()):
        has_script_mentions = bool(re.search(r'scripts?/', content, re.IGNORECASE))
        if has_script_mentions:
            check_pass("scripts/ mentioned in SKILL.md")
            passed += 1
        else:
            check_fail("scripts/ mentioned in SKILL.md")
            issues.append(ValidationIssue(
                "script mentions",
                "SKILL.md",
                "scripts/ exists but not mentioned",
                "Scripts referenced in content",
                "Add script references: 'Run scripts/script_name.py' or similar"
            ))
    else:
        check_skip("scripts/ mentioned (N/A - no scripts)")
        passed += 1

    # ==================== CATEGORY 8: CODE & EXAMPLES ====================
    print_section("Category 8: Code & Examples (3 checks)")

    # Check 20: Code blocks present
    # Match code block pairs to identify opening fences only
    lines = content.split('\n')
    code_blocks = []
    in_code_block = False

    for line in lines:
        if line.startswith('```'):
            if not in_code_block:
                # Opening fence - extract language tag
                tag = line[3:].strip()
                code_blocks.append(tag)
                in_code_block = True
            else:
                # Closing fence
                in_code_block = False

    if code_blocks:
        check_pass(f"contains code examples ({len(code_blocks)} blocks)")
        passed += 1

        # Check 21: Language tags
        untagged = [i for i, tag in enumerate(code_blocks, 1) if not tag]
        if not untagged:
            check_pass("all code blocks have language tags")
            passed += 1
        else:
            check_fail(f"all code blocks have language tags ({len(untagged)} missing)")
            issues.append(ValidationIssue(
                "code block language tags",
                "SKILL.md code blocks",
                f"{len(untagged)} blocks without language tags",
                "All blocks tagged (```python, ```bash, etc.)",
                f"Add language tags to code blocks {untagged[:5]}"
            ))

        # Check 22: No pseudocode
        has_pseudo = bool(re.search(r'```(?:pseudo|text)\n', content))
        if not has_pseudo:
            check_pass("no pseudocode (real code only)")
            passed += 1
        else:
            check_fail("no pseudocode (real code only)")
            issues.append(ValidationIssue(
                "pseudocode blocks",
                "SKILL.md",
                "Found ```pseudo or ```text blocks",
                "Real, runnable code only",
                "Replace pseudocode with actual bash/python/etc code"
            ))
    else:
        check_skip("code examples (N/A for this skill)")
        passed += 3  # Skip code-related checks

    # ==================== CATEGORY 9: SCRIPTS QUALITY ====================
    print_section("Category 9: Scripts Quality (1 check)")

    # Check 23: Scripts have error handling
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        script_files = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))
        if script_files:
            scripts_no_errors = []
            for script in script_files:
                try:
                    script_content = script.read_text()
                    if script.suffix == '.py':
                        if not re.search(r'\btry\b|\bexcept\b|\braise\b', script_content):
                            scripts_no_errors.append(script.name)
                    elif script.suffix == '.sh':
                        if not re.search(r'\bset -e\b|\|\||\bexit\b', script_content):
                            scripts_no_errors.append(script.name)
                except Exception:
                    pass

            if not scripts_no_errors:
                check_pass(f"all scripts have error handling ({len(script_files)} scripts)")
                passed += 1
            else:
                check_fail(f"scripts have error handling ({len(scripts_no_errors)} missing)")
                script_list = ', '.join(scripts_no_errors[:5])
                issues.append(ValidationIssue(
                    "script error handling",
                    "scripts/",
                    f"{len(scripts_no_errors)} scripts lack error handling: {script_list}",
                    "All scripts handle errors",
                    "Add try/except (Python) or set -e/|| (Bash) to all scripts"
                ))
        else:
            check_skip("script error handling (no scripts)")
            passed += 1
    else:
        check_skip("script error handling (no scripts/ dir)")
        passed += 1

    return issues, passed, total, content

def validate_reference_frontmatter(frontmatter: Optional[dict]) -> Dict:
    """Validate frontmatter for a reference file.

    Returns dict with validation results:
        - has_frontmatter: bool
        - has_title: bool
        - has_description: bool
        - has_skill: bool
        - title_length_ok: bool
        - description_length_ok: bool
        - issues: List[str]
    """
    result = {
        'has_frontmatter': frontmatter is not None,
        'has_title': False,
        'has_description': False,
        'has_skill': False,
        'title_length_ok': True,
        'description_length_ok': True,
        'has_keywords': False,
        'issues': []
    }

    if not frontmatter:
        result['issues'].append("Missing YAML frontmatter")
        return result

    # Check required fields
    if 'title' in frontmatter:
        result['has_title'] = True
        title = frontmatter['title']
        if len(title) > 100:
            result['title_length_ok'] = False
            result['issues'].append(f"Title too long: {len(title)} chars (max 100)")
    else:
        result['issues'].append("Missing required field: 'title'")

    if 'description' in frontmatter:
        result['has_description'] = True
        description = frontmatter['description']
        if len(description) > 500:
            result['description_length_ok'] = False
            result['issues'].append(f"Description too long: {len(description)} chars (max 500)")
    else:
        result['issues'].append("Missing required field: 'description'")

    if 'skill' in frontmatter:
        result['has_skill'] = True
    else:
        result['issues'].append("Missing required field: 'skill'")

    # Check optional but recommended fields
    if 'keywords' in frontmatter:
        result['has_keywords'] = True

    return result

def analyze_references(skill_path: Path) -> Dict:
    """Analyze reference materials."""
    refs_dir = skill_path / "references"

    if not refs_dir.exists():
        return {'files': [], 'message': 'No references/ directory found'}

    ref_files = list(refs_dir.glob("*.md"))

    if not ref_files:
        return {'files': [], 'message': 'No markdown files in references/'}

    analyses = []
    for ref_file in sorted(ref_files):
        content = ref_file.read_text(encoding='utf-8')
        frontmatter, fm_error = parse_yaml_frontmatter(content)

        analysis = {
            'path': str(ref_file.relative_to(skill_path)),
            'lines': len(content.splitlines()),
            'words': len(content.split()),
            'frontmatter': frontmatter,
            'frontmatter_error': fm_error,
            'frontmatter_validation': validate_reference_frontmatter(frontmatter),
            'headings': extract_headings(content),
            'hierarchy_ok': True,
            'hierarchy_issues': [],
            'bloat': {},
            'density_patterns': {},
            'density_score': 0,
        }

        # Analyze heading hierarchy
        analysis['hierarchy_ok'], analysis['hierarchy_issues'] = analyze_heading_hierarchy(analysis['headings'])

        # Detect patterns
        analysis['bloat'] = detect_bloat_patterns(content)
        analysis['density_patterns'] = detect_high_density_patterns(content)
        analysis['density_score'] = calculate_density_score(content, analysis['density_patterns'])

        analyses.append(analysis)

    return {'files': analyses}

def analyze_scripts(skill_path: Path) -> Dict:
    """Analyze scripts."""
    scripts_dir = skill_path / "scripts"

    if not scripts_dir.exists():
        return {'files': [], 'message': 'No scripts/ directory found'}

    script_files = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))

    if not script_files:
        return {'files': [], 'message': 'No scripts in scripts/'}

    analyses = []
    for script_file in sorted(script_files):
        try:
            content = script_file.read_text(encoding='utf-8')

            analysis = {
                'path': str(script_file.relative_to(skill_path)),
                'lines': len(content.splitlines()),
                'has_docstring': bool(re.search(r'"""[\s\S]*?"""', content)),
                'has_error_handling': False,
                'has_main': bool(re.search(r'if __name__ == ["\']__main__["\']', content)),
            }

            # Check error handling
            if script_file.suffix == '.py':
                analysis['has_error_handling'] = bool(re.search(r'\btry\b|\bexcept\b|\braise\b', content))
            elif script_file.suffix == '.sh':
                analysis['has_error_handling'] = bool(re.search(r'\bset -e\b|\|\||\bexit\b', content))

            analyses.append(analysis)
        except Exception as e:
            analyses.append({
                'path': str(script_file.relative_to(skill_path)),
                'error': str(e)
            })

    return {'files': analyses}

def analyze_templates(skill_path: Path) -> Dict:
    """Analyze templates."""
    templates_dir = skill_path / "templates"

    if not templates_dir.exists():
        return {'files': [], 'message': 'No templates/ directory found'}

    template_files = list(templates_dir.glob("*.md")) + list(templates_dir.glob("*.txt"))

    if not template_files:
        return {'files': [], 'message': 'No templates in templates/'}

    analyses = []
    for template_file in sorted(template_files):
        try:
            content = template_file.read_text(encoding='utf-8')

            # Find placeholder patterns
            placeholders = {
                'double_brace': len(re.findall(r'\{\{[\w\-]+\}\}', content)),
                'angle_bracket': len(re.findall(r'<[\w\-]+>', content)),
                'dollar_brace': len(re.findall(r'\$\{[\w\-]+\}', content)),
                'todo_markers': len(re.findall(r'TODO|FIXME|XXX', content)),
            }

            analysis = {
                'path': str(template_file.relative_to(skill_path)),
                'lines': len(content.splitlines()),
                'has_frontmatter': parse_yaml_frontmatter(content)[0] is not None,
                'placeholders': placeholders,
                'total_placeholders': sum(placeholders.values()),
            }

            analyses.append(analysis)
        except Exception as e:
            analyses.append({
                'path': str(template_file.relative_to(skill_path)),
                'error': str(e)
            })

    return {'files': analyses}

def analyze_cross_references(skill_path: Path, skill_md_content: str) -> Dict:
    """Analyze cross-references between SKILL.md and bundled resources, including inter-resource references."""

    # Get all actual files in resource directories
    actual_files = {}
    for dir_name in ['scripts', 'references', 'templates', 'assets']:
        dir_path = skill_path / dir_name
        if dir_path.exists():
            for file_path in dir_path.rglob('*'):
                if file_path.is_file():
                    # Skip binary files and cache
                    if '__pycache__' in str(file_path) or file_path.suffix in ['.pyc', '.pyo']:
                        continue
                    rel_path = str(file_path.relative_to(skill_path))
                    actual_files[rel_path] = file_path

    # Find mentions in SKILL.md
    skill_mentions = find_resource_mentions(skill_md_content, skill_path)

    # Find mentions in each resource file (cross-references between resources)
    resource_mentions = {}  # Map of file_path -> {mentioned_file: [(line, context), ...]}

    for file_path, abs_path in actual_files.items():
        try:
            # Only scan text files
            if abs_path.suffix in ['.md', '.txt', '.py', '.sh', '.yaml', '.yml', '.json']:
                content = abs_path.read_text(encoding='utf-8')
                mentions = find_resource_mentions(content, skill_path)
                if mentions:
                    resource_mentions[file_path] = mentions
        except Exception:
            # Skip files that can't be read
            pass

    # Build reference graph
    # Track which files reference each file
    referenced_by = defaultdict(list)  # file -> [(referrer, line_num, context), ...]

    # Add SKILL.md references
    for mentioned_file, mention_list in skill_mentions.items():
        for line_num, context in mention_list:
            referenced_by[mentioned_file].append(('SKILL.md', line_num, context))

    # Add inter-resource references
    for referrer_file, mentions in resource_mentions.items():
        for mentioned_file, mention_list in mentions.items():
            for line_num, context in mention_list:
                referenced_by[mentioned_file].append((referrer_file, line_num, context))

    # Classify files by reference type
    directly_referenced = set()  # Mentioned in SKILL.md
    indirectly_referenced = set()  # Mentioned in other resources but not SKILL.md
    unreferenced = set()  # Never mentioned anywhere

    for file_path in actual_files:
        refs = referenced_by.get(file_path, [])

        if any(ref[0] == 'SKILL.md' for ref in refs):
            directly_referenced.add(file_path)
        elif refs:
            indirectly_referenced.add(file_path)
        else:
            unreferenced.add(file_path)

    # Build comprehensive cross-reference map
    xref_map = {}
    for file_path in actual_files:
        refs = referenced_by.get(file_path, [])

        # Determine reference chain for indirectly referenced files
        reference_chain = []
        if file_path in indirectly_referenced:
            # Find path to SKILL.md through intermediate references
            visited = set()
            chain = _find_reference_chain(file_path, referenced_by, 'SKILL.md', visited, actual_files)
            if chain:
                reference_chain = chain

        xref_map[file_path] = {
            'exists': True,
            'reference_type': 'direct' if file_path in directly_referenced
                            else 'indirect' if file_path in indirectly_referenced
                            else 'unreferenced',
            'referenced_by': refs,
            'reference_count': len(refs),
            'reference_chain': reference_chain,
            'mentions_others': list(resource_mentions.get(file_path, {}).keys()) if file_path in resource_mentions else []
        }

    # Check for broken references (mentioned but don't exist)
    broken_refs = []
    all_mentions = {**skill_mentions}
    for rm in resource_mentions.values():
        for path, mentions in rm.items():
            if path not in all_mentions:
                all_mentions[path] = []
            all_mentions[path].extend(mentions)

    for mentioned_path, mention_list in all_mentions.items():
        if mentioned_path not in actual_files:
            # Find who referenced this broken path
            referrers = []
            if mentioned_path in skill_mentions:
                referrers.append('SKILL.md')
            for referrer, mentions in resource_mentions.items():
                if mentioned_path in mentions:
                    referrers.append(referrer)

            broken_refs.append({
                'path': mentioned_path,
                'mentioned_in': referrers,
                'mentions': mention_list[:3]  # Limit to 3 examples
            })

    # Calculate statistics
    total_files = len(actual_files)

    return {
        'xref_map': xref_map,
        'broken_refs': broken_refs,
        'resource_cross_refs': resource_mentions,
        'stats': {
            'total_files': total_files,
            'directly_referenced': len(directly_referenced),
            'indirectly_referenced': len(indirectly_referenced),
            'unreferenced': len(unreferenced),
            'broken_references': len(broken_refs),
            'direct_coverage_pct': (len(directly_referenced) / total_files * 100) if total_files > 0 else 0,
            'total_coverage_pct': ((len(directly_referenced) + len(indirectly_referenced)) / total_files * 100) if total_files > 0 else 0,
        }
    }

def _find_reference_chain(target: str, referenced_by: Dict, goal: str, visited: set, actual_files: Dict, max_depth: int = 5) -> List[str]:
    """Find reference chain from target to goal (typically SKILL.md).

    Returns a chain like: ['SKILL.md', 'references/guide-a.md', 'references/guide-b.md']
    """
    if max_depth == 0:
        return []

    if target in visited:
        return []

    visited.add(target)

    refs = referenced_by.get(target, [])

    for referrer, _, _ in refs:
        if referrer == goal:
            return [goal, target]

        # Recurse only if referrer is an actual resource file
        if referrer in actual_files:
            chain = _find_reference_chain(referrer, referenced_by, goal, visited.copy(), actual_files, max_depth - 1)
            if chain:
                return chain + [target]

    return []

def print_skill_summary_minimal(issues: List[ValidationIssue], passed: int, total: int):
    """Print minimal SKILL.md validation summary - one line + failures only."""
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    percentage = (passed / total * 100) if total > 0 else 0

    # One-line summary
    status = "✓ PASS" if passed == total else "✗ FAIL"
    print(f"SKILL.md: {passed}/{total} ({percentage:.0f}%) | {len(errors)} errors, {len(warnings)} warnings | {status}")

    # Only list errors with concise fixes
    if errors:
        print(f"\nErrors:")
        for issue in errors:
            print(f"  ✗ {issue.check}: {issue.fix}")

    # List warnings if any
    if warnings:
        print(f"\nWarnings:")
        for issue in warnings:
            print(f"  ⚠ {issue.check}: {issue.fix}")

def print_skill_summary(issues: List[ValidationIssue], passed: int, total: int):
    """Print SKILL.md validation summary."""
    print_header("SKILL.MD VALIDATION SUMMARY")

    percentage = (passed / total * 100) if total > 0 else 0
    print(f"{Colors.BOLD}Result: {passed}/{total} checks passed ({percentage:.1f}%){Colors.END}")

    # Separate errors from warnings
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ PASS{Colors.END}")
        print("SKILL.md meets all validation requirements.")

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

def print_references_summary(analysis: Dict, skill_name: str):
    """Print reference material analysis summary."""
    print_header(f"REFERENCE MATERIAL ANALYSIS: {skill_name}")

    if 'message' in analysis:
        print(f"{Colors.YELLOW}{analysis['message']}{Colors.END}")
        return

    files = analysis['files']
    print(f"Total reference files: {len(files)}\n")

    for file_analysis in files:
        print(f"{Colors.BOLD}📄 {file_analysis['path']}{Colors.END}")
        print(f"  Lines: {file_analysis['lines']} | Words: {file_analysis['words']} | "
              f"Density: {file_analysis['density_score']}/10")

        # Frontmatter validation (per document)
        fm_validation = file_analysis['frontmatter_validation']
        if fm_validation['has_frontmatter']:
            if not fm_validation['issues']:
                check_pass("Frontmatter valid (title, description, skill)")
                # Show optional fields if present
                if fm_validation['has_keywords']:
                    print(f"    {Colors.CYAN}+ keywords field present{Colors.END}")
            else:
                check_fail(f"Frontmatter issues: {len(fm_validation['issues'])}")
                for issue in fm_validation['issues']:
                    print(f"    • {issue}")
        else:
            check_fail("No frontmatter (required for discoverability)")
            print(f"    {Colors.YELLOW}Add: ---\\ntitle: ...\\ndescription: ...\\nskill: skill-name\\n---{Colors.END}")

        # Heading hierarchy
        if file_analysis['hierarchy_ok']:
            check_pass("Heading hierarchy correct")
        else:
            check_fail(f"Heading hierarchy issues: {len(file_analysis['hierarchy_issues'])}")
            for issue in file_analysis['hierarchy_issues'][:3]:
                print(f"    • {issue}")

        # Show density patterns
        patterns = file_analysis['density_patterns']
        high_density = [(k, v) for k, v in patterns.items() if v > 0]
        if high_density:
            print(f"  High-density patterns: {', '.join(f'{k}({v})' for k, v in high_density[:5])}")

        print()

    # Aggregate statistics
    if files:
        avg_density = sum(f['density_score'] for f in files) / len(files)
        hierarchy_issues = sum(1 for f in files if not f['hierarchy_ok'])
        frontmatter_issues = sum(1 for f in files if not f['frontmatter_validation']['has_frontmatter']
                                or f['frontmatter_validation']['issues'])

        print(f"{Colors.BOLD}Aggregate Statistics:{Colors.END}")
        print(f"  Average density score: {avg_density:.1f}/10")
        print(f"  Files with hierarchy issues: {hierarchy_issues}/{len(files)}")
        print(f"  Files with frontmatter issues: {frontmatter_issues}/{len(files)}")
        print(f"  {Colors.CYAN}Target: 7+/10 density, 0 hierarchy issues, 0 frontmatter issues{Colors.END}")

def print_scripts_summary(analysis: Dict):
    """Print scripts analysis summary."""
    print_header("SCRIPTS ANALYSIS")

    if 'message' in analysis:
        print(f"{Colors.YELLOW}{analysis['message']}{Colors.END}")
        return

    files = analysis['files']
    print(f"Total scripts: {len(files)}\n")

    for script in files:
        if 'error' in script:
            print(f"{Colors.RED}✗ {script['path']}: {script['error']}{Colors.END}")
            continue

        print(f"{Colors.BOLD}🔧 {script['path']}{Colors.END}")
        print(f"  Lines: {script['lines']}")

        checks = []
        if script.get('has_docstring'):
            checks.append(f"{Colors.GREEN}✓ Docstring{Colors.END}")
        else:
            checks.append(f"{Colors.YELLOW}⊘ No docstring{Colors.END}")

        if script.get('has_error_handling'):
            checks.append(f"{Colors.GREEN}✓ Error handling{Colors.END}")
        else:
            checks.append(f"{Colors.RED}✗ No error handling{Colors.END}")

        if script.get('has_main'):
            checks.append(f"{Colors.GREEN}✓ Main guard{Colors.END}")
        else:
            checks.append(f"{Colors.YELLOW}⊘ No main guard{Colors.END}")

        print(f"  {' | '.join(checks)}")
        print()

def print_templates_summary(analysis: Dict):
    """Print templates analysis summary."""
    print_header("TEMPLATES ANALYSIS")

    if 'message' in analysis:
        print(f"{Colors.YELLOW}{analysis['message']}{Colors.END}")
        return

    files = analysis['files']
    print(f"Total templates: {len(files)}\n")

    for template in files:
        if 'error' in template:
            print(f"{Colors.RED}✗ {template['path']}: {template['error']}{Colors.END}")
            continue

        print(f"{Colors.BOLD}📋 {template['path']}{Colors.END}")
        print(f"  Lines: {template['lines']}")

        if template['has_frontmatter']:
            check_pass("Has YAML frontmatter")
        else:
            check_info("No YAML frontmatter")

        if template['total_placeholders'] > 0:
            check_info(f"{template['total_placeholders']} placeholders found")
            for ptype, count in template['placeholders'].items():
                if count > 0:
                    print(f"    • {ptype}: {count}")
        else:
            check_info("No placeholders detected")

        print()

def scan_all_files_for_absolute_paths(skill_path: Path) -> Dict:
    """Scan all resource files for user-specific absolute paths."""

    findings = {}

    # Get all text files
    for dir_name in ['references', 'scripts', 'templates', 'assets']:
        dir_path = skill_path / dir_name
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                # Skip binary files and cache
                if '__pycache__' in str(file_path) or file_path.suffix in ['.pyc', '.pyo']:
                    continue

                # Only scan text files
                if file_path.suffix in ['.md', '.txt', '.py', '.sh', '.yaml', '.yml', '.json', '.html', '.css', '.js']:
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        absolute_paths = find_absolute_paths(content)

                        if absolute_paths:
                            rel_path = str(file_path.relative_to(skill_path))
                            findings[rel_path] = absolute_paths
                    except Exception:
                        # Skip files that can't be read
                        pass

    return findings

def print_absolute_paths_analysis(findings: Dict):
    """Print analysis of user-specific absolute paths found in all files."""
    print_header("PORTABILITY CHECK: ABSOLUTE PATHS")

    if not findings:
        print(f"{Colors.GREEN}✓ No user-specific absolute paths found in any files{Colors.END}")
        print("All files use portable relative paths or ~/")
        return

    total_violations = sum(len(paths) for paths in findings.values())

    print(f"{Colors.BOLD}Overview:{Colors.END}")
    print(f"  Files with absolute paths: {len(findings)}")
    print(f"  Total violations: {total_violations}")
    print(f"  {Colors.RED}Action required: Replace with ~/ or relative paths{Colors.END}\n")

    print_section("Files with User-Specific Absolute Paths")

    for file_path in sorted(findings.keys()):
        paths = findings[file_path]
        print(f"{Colors.RED}✗ {Colors.BOLD}{file_path}{Colors.END}")
        print(f"  Found {len(paths)} absolute path(s):")

        for line_num, path, context, desc in paths[:5]:
            print(f"    Line {line_num}: {Colors.YELLOW}{path}{Colors.END} ({desc})")
            print(f"      Context: ...{context}...")

        if len(paths) > 5:
            print(f"    ... and {len(paths) - 5} more violations")

        print()

    print(f"{Colors.BOLD}Recommended Fixes:{Colors.END}")
    print("  1. Replace /home/username/ with ~/")
    print("  2. Replace /Users/username/ with ~/")
    print("  3. Replace C:\\Users\\username\\ with relative paths")
    print("  4. Use skill-relative paths where possible")
    print("  5. Use ${HOME} or $HOME in scripts if needed")

def print_cross_reference_analysis(xref: Dict):
    """Print cross-reference analysis."""
    print_header("CROSS-REFERENCE ANALYSIS")

    stats = xref['stats']
    print(f"{Colors.BOLD}Overview:{Colors.END}")
    print(f"  Total bundled files: {stats['total_files']}")
    print(f"  Directly referenced (in SKILL.md): {stats['directly_referenced']}")
    print(f"  Indirectly referenced (via other resources): {stats['indirectly_referenced']}")
    print(f"  Unreferenced (orphaned): {stats['unreferenced']}")
    print(f"  Broken references: {stats['broken_references']}")
    print(f"  Direct coverage: {stats['direct_coverage_pct']:.1f}%")
    print(f"  Total coverage: {stats['total_coverage_pct']:.1f}%")

    # Show per-file cross-references grouped by type
    print_section("Directly Referenced Files (mentioned in SKILL.md)")

    xref_map = xref['xref_map']
    direct_files = {k: v for k, v in xref_map.items() if v['reference_type'] == 'direct'}

    if direct_files:
        for file_path in sorted(direct_files.keys()):
            info = direct_files[file_path]
            print(f"{Colors.GREEN}✓{Colors.END} {Colors.BOLD}{file_path}{Colors.END}")

            # Show where it's referenced
            skill_refs = [r for r in info['referenced_by'] if r[0] == 'SKILL.md']
            if skill_refs:
                print(f"  Referenced {len(skill_refs)} time(s) in SKILL.md:")
                for referrer, line_num, context in skill_refs[:2]:
                    print(f"    Line {line_num}: ...{context}...")
                if len(skill_refs) > 2:
                    print(f"    ... and {len(skill_refs) - 2} more")

            # Show if it mentions other files
            if info['mentions_others']:
                print(f"  {Colors.CYAN}→ References: {', '.join(info['mentions_others'][:3])}{Colors.END}")
                if len(info['mentions_others']) > 3:
                    print(f"    ... and {len(info['mentions_others']) - 3} more")
            print()
    else:
        print(f"  {Colors.YELLOW}No files directly referenced in SKILL.md{Colors.END}\n")

    # Show indirectly referenced files
    print_section("Indirectly Referenced Files (via other resources)")

    indirect_files = {k: v for k, v in xref_map.items() if v['reference_type'] == 'indirect'}

    if indirect_files:
        for file_path in sorted(indirect_files.keys()):
            info = indirect_files[file_path]
            print(f"{Colors.CYAN}⟿{Colors.END} {Colors.BOLD}{file_path}{Colors.END}")

            # Show reference chain
            if info['reference_chain']:
                chain_str = ' → '.join(info['reference_chain'])
                print(f"  {Colors.CYAN}Reference chain: {chain_str}{Colors.END}")

            # Show who references it
            print(f"  Referenced {len(info['referenced_by'])} time(s) by:")
            for referrer, line_num, context in info['referenced_by'][:2]:
                print(f"    {referrer} (line {line_num}): ...{context}...")
            if len(info['referenced_by']) > 2:
                print(f"    ... and {len(info['referenced_by']) - 2} more")

            # Show if it mentions other files
            if info['mentions_others']:
                print(f"  {Colors.CYAN}→ References: {', '.join(info['mentions_others'][:3])}{Colors.END}")
            print()
    else:
        print(f"  {Colors.GREEN}No indirectly referenced files{Colors.END}\n")

    # Show unreferenced (orphaned) files
    print_section("Unreferenced Files (orphaned - never mentioned)")

    unreferenced_files = {k: v for k, v in xref_map.items() if v['reference_type'] == 'unreferenced'}

    if unreferenced_files:
        for file_path in sorted(unreferenced_files.keys()):
            info = unreferenced_files[file_path]
            print(f"{Colors.YELLOW}⚠{Colors.END} {Colors.BOLD}{file_path}{Colors.END}")
            print(f"  {Colors.YELLOW}NEVER MENTIONED anywhere{Colors.END}")

            # Show if it mentions other files (it's a dead-end reference)
            if info['mentions_others']:
                print(f"  {Colors.YELLOW}But references: {', '.join(info['mentions_others'][:3])}{Colors.END}")
            print()
    else:
        print(f"  {Colors.GREEN}All files are referenced!{Colors.END}\n")

    # Show broken references
    if xref['broken_refs']:
        print_section("Broken References (mentioned but don't exist)")
        for broken in xref['broken_refs']:
            print(f"{Colors.RED}✗ {broken['path']}{Colors.END} (FILE NOT FOUND)")
            print(f"  Mentioned in: {', '.join(broken['mentioned_in'])}")
            for line_num, context in broken['mentions'][:2]:
                print(f"    Line {line_num}: ...{context}...")
            print()

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Comprehensive skill validation and analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_skill.py /path/to/skill
  python3 scripts/validate_skill.py /path/to/skill --check skill
  python3 scripts/validate_skill.py /path/to/skill --minimal
  python3 scripts/validate_skill.py /path/to/skill --check references
  python3 scripts/validate_skill.py /path/to/skill --check scripts
  python3 scripts/validate_skill.py /path/to/skill --check templates

Minimal Mode:
  Use --minimal for automated checks by agents. Shows only:
  - One-line score summary
  - Failures with concise fix recommendations
  - Suppresses all passing checks and verbose output
        """
    )

    parser.add_argument('skill_path', type=Path, help='Path to skill directory')
    parser.add_argument('--check', choices=['all', 'skill', 'references', 'scripts', 'templates'],
                        default='all', help='What to check (default: all)')
    parser.add_argument('--minimal', action='store_true',
                        help='Minimal output mode: one-line score + failures only (for automated checks)')

    args = parser.parse_args()

    # Set minimal mode flag
    if args.minimal:
        set_minimal_mode(True)

    skill_path = args.skill_path

    if not skill_path.exists():
        print(f"{Colors.RED}Error: Path does not exist: {skill_path}{Colors.END}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"{Colors.RED}Error: Not a directory: {skill_path}{Colors.END}")
        sys.exit(1)

    check_target = args.check
    skill_name = skill_path.name
    minimal = args.minimal

    # Print header (suppressed in minimal mode)
    print_header(f"SKILL VALIDATION: {skill_name}")
    if not minimal:
        print(f"Path: {skill_path}")
        print(f"Checking: {check_target}")
        print(f"Goal: 100% pass rate on SKILL.md validation (23/23 checks)")

    # Run validations based on target
    skill_issues = []
    skill_passed = 0
    skill_total = 0
    skill_content = ""

    if check_target in ['all', 'skill']:
        skill_issues, skill_passed, skill_total, skill_content = validate_skill_md(skill_path)
        if minimal:
            print_skill_summary_minimal(skill_issues, skill_passed, skill_total)
        else:
            print_skill_summary(skill_issues, skill_passed, skill_total)

    # Skip other analyses in minimal mode - only validate SKILL.md
    if not minimal:
        if check_target in ['all', 'references']:
            ref_analysis = analyze_references(skill_path)
            print_references_summary(ref_analysis, skill_name)

        if check_target in ['all', 'scripts']:
            script_analysis = analyze_scripts(skill_path)
            print_scripts_summary(script_analysis)

        if check_target in ['all', 'templates']:
            template_analysis = analyze_templates(skill_path)
            print_templates_summary(template_analysis)

        # Always run cross-reference analysis and portability check if checking all
        if check_target == 'all' and skill_content:
            xref_analysis = analyze_cross_references(skill_path, skill_content)
            print_cross_reference_analysis(xref_analysis)

            # Scan all files for absolute paths (portability check)
            absolute_path_findings = scan_all_files_for_absolute_paths(skill_path)
            print_absolute_paths_analysis(absolute_path_findings)

    # Exit code
    if check_target in ['all', 'skill']:
        sys.exit(0 if skill_passed == skill_total else 1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
