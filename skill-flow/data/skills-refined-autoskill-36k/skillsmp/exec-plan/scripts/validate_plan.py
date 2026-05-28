#!/usr/bin/env python3
"""
Validate an ExecPlan file for structural completeness and common failure modes.

Usage:
    python validate_plan.py <plan.md>
    python validate_plan.py <plan.md> --strict

Returns exit code 0 if valid, 1 if errors found.
Prints specific issues with line numbers when possible.
"""

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Purpose",
    "Progress",
    "Surprises & Discoveries",
    "Decision Log",
    "Outcomes & Retrospective",
    "Context",
    "Plan of Work",
    "Validation",
]

FAILURE_PATTERNS = [
    (r'\bas\s+we\s+discussed\b', "References prior discussion (not self-contained)"),
    (r'\bas\s+mentioned\s+(earlier|before|previously)\b', "References prior context (not self-contained)"),
    (r'\bsee\s+the\s+(architecture|design)\s+doc\b', "External reference (embed knowledge instead)"),
    (r'\bper\s+the\s+RFC\b', "External reference to RFC (embed relevant content)"),
    (r'\bTBD\b', "Unresolved placeholder (decide now or add prototyping milestone)"),
    (r'\bto\s+be\s+determined\b', "Unresolved placeholder"),
    (r'\bas\s+needed\b', "Vague instruction (be specific)"),
    (r'\bas\s+appropriate\b', "Vague instruction (be specific)"),
    (r'\bconfigure\s+appropriately\b', "Outsources decision to reader"),
    (r'\buse\s+best\s+judgment\b', "Outsources decision to reader"),
    (r'\btests\s+should\s+pass\b(?!\s*\(\d)', "Vague acceptance (specify which tests, expected count)"),
    (r'\bshould\s+work\s+correctly\b', "Vague acceptance (define observable behavior)"),
]

JARGON_PATTERNS = [
    (r'\bmiddleware\b', "middleware"),
    (r'\bdaemon\b', "daemon"),
    (r'\bRPC\b', "RPC"),
    (r'\bgateway\b', "gateway"),
    (r'\borchestrat', "orchestration/orchestrator"),
    (r'\bpipeline\b', "pipeline"),
    (r'\bhandler\b', "handler"),
    (r'\bservice\s+mesh\b', "service mesh"),
]


def find_sections(content: str) -> dict[str, int]:
    """Find all markdown sections and their line numbers."""
    sections = {}
    for i, line in enumerate(content.split('\n'), 1):
        if line.startswith('#'):
            heading = re.sub(r'^#+\s*', '', line).strip()
            sections[heading.lower()] = i
    return sections


def check_required_sections(content: str) -> list[str]:
    """Check that all required sections exist."""
    sections = find_sections(content)
    errors = []
    for required in REQUIRED_SECTIONS:
        found = any(required.lower() in s for s in sections.keys())
        if not found:
            errors.append(f"Missing required section: '{required}'")
    return errors


def check_failure_patterns(content: str) -> list[str]:
    """Detect common failure mode patterns."""
    errors = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern, message in FAILURE_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                snippet = line.strip()[:60]
                errors.append(f"Line {i}: {message}\n    '{snippet}...'")
    return errors


def check_jargon_definitions(content: str) -> list[str]:
    """Check that jargon terms are defined near first use."""
    warnings = []
    lines = content.split('\n')
    defined_terms = set()
    
    # Find definitions (look for patterns like "X means" or "X is" or "(X)")
    for line in lines:
        for pattern, term in JARGON_PATTERNS:
            if re.search(rf'{pattern}\s+(means|is|refers to|\()', line, re.IGNORECASE):
                defined_terms.add(term)
            # Also check for parenthetical definitions
            if re.search(rf'\([^)]*{pattern}[^)]*\)', line, re.IGNORECASE):
                defined_terms.add(term)
    
    # Find uses without definitions
    for i, line in enumerate(lines, 1):
        for pattern, term in JARGON_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE) and term not in defined_terms:
                if "Context" in ''.join(lines[:i]) or "Terms" in ''.join(lines[:i]):
                    # Likely in a definitions section
                    defined_terms.add(term)
                else:
                    warnings.append(f"Line {i}: Term '{term}' used without definition")
                    defined_terms.add(term)  # Only warn once per term
    return warnings


def check_progress_format(content: str) -> list[str]:
    """Validate Progress section format."""
    errors = []
    in_progress = False
    has_checkbox = False
    
    for i, line in enumerate(content.split('\n'), 1):
        if re.match(r'^#+\s*Progress', line, re.IGNORECASE):
            in_progress = True
        elif in_progress and line.startswith('#'):
            in_progress = False
        elif in_progress:
            if re.match(r'^-\s*\[[ x]\]', line):
                has_checkbox = True
                # Check for timestamp on completed items
                if '[x]' in line.lower() and not re.search(r'\(\d{4}-\d{2}-\d{2}', line):
                    errors.append(f"Line {i}: Completed item missing timestamp")
    
    if not has_checkbox:
        errors.append("Progress section has no checkbox items")
    return errors


def check_acceptance_criteria(content: str) -> list[str]:
    """Check that acceptance criteria include specific commands and outputs."""
    warnings = []
    in_validation = False
    has_command = False
    has_expected_output = False
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.match(r'^#+\s*(Validation|Acceptance)', line, re.IGNORECASE):
            in_validation = True
        elif in_validation and line.startswith('#'):
            in_validation = False
        elif in_validation:
            # Look for command patterns
            if re.search(r'(npm|python|cargo|go|curl|make|sh|bash|\./)', line):
                has_command = True
            # Look for expected output patterns
            if re.search(r'(expect|output|returns|response|result)', line, re.IGNORECASE):
                has_expected_output = True
    
    if not has_command:
        warnings.append("Validation section may lack specific commands to run")
    if not has_expected_output:
        warnings.append("Validation section may lack expected output/behavior")
    return warnings


def validate_plan(filepath: str, strict: bool = False) -> tuple[bool, list[str], list[str]]:
    """
    Validate an ExecPlan file.
    
    Returns: (is_valid, errors, warnings)
    """
    path = Path(filepath)
    if not path.exists():
        return False, [f"File not found: {filepath}"], []
    
    content = path.read_text()
    errors = []
    warnings = []
    
    # Required section checks (errors)
    errors.extend(check_required_sections(content))
    
    # Failure pattern checks (errors)
    errors.extend(check_failure_patterns(content))
    
    # Progress format checks (errors)
    errors.extend(check_progress_format(content))
    
    # Jargon checks (warnings, or errors in strict mode)
    jargon_issues = check_jargon_definitions(content)
    if strict:
        errors.extend(jargon_issues)
    else:
        warnings.extend(jargon_issues)
    
    # Acceptance criteria checks (warnings, or errors in strict mode)
    acceptance_issues = check_acceptance_criteria(content)
    if strict:
        errors.extend(acceptance_issues)
    else:
        warnings.extend(acceptance_issues)
    
    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_plan.py <plan.md> [--strict]")
        print("\nValidates an ExecPlan for structural completeness and common failure modes.")
        sys.exit(1)
    
    filepath = sys.argv[1]
    strict = '--strict' in sys.argv
    
    is_valid, errors, warnings = validate_plan(filepath, strict)
    
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  ✗ {error}")
        print()
    
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()
    
    if is_valid:
        print("✓ Plan structure is valid")
        if warnings:
            print(f"  ({len(warnings)} warnings to review)")
        sys.exit(0)
    else:
        print(f"✗ Plan has {len(errors)} error(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
