#!/usr/bin/env python3
"""
Check documentation quality metrics for AI-readiness.

This script analyzes documentation structure, heading hierarchy,
code blocks, and other quality indicators.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter


def extract_headings(content: str) -> List[Tuple[int, str, int]]:
    """
    Extract all headings from markdown content.

    Returns:
        List of (level, text, line_number) tuples
    """
    headings = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Match ATX-style headings (# Heading)
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((level, text, i))

    return headings


def check_heading_hierarchy(headings: List[Tuple[int, str, int]]) -> List[str]:
    """
    Check for skipped heading levels.

    Returns:
        List of error messages
    """
    errors = []

    if not headings:
        errors.append("No headings found in document")
        return errors

    # Check if document starts with H1
    if headings[0][0] != 1:
        errors.append(f"Document should start with H1, found H{headings[0][0]} at line {headings[0][2]}")

    # Count H1s
    h1_count = sum(1 for level, _, _ in headings if level == 1)
    if h1_count > 1:
        errors.append(f"Multiple H1 headings found ({h1_count}). Use only one H1 per document")

    # Check for skipped levels
    for i in range(1, len(headings)):
        prev_level = headings[i-1][0]
        curr_level = headings[i][0]

        # If jumping down more than one level, that's a skip
        if curr_level > prev_level + 1:
            errors.append(
                f"Skipped heading level at line {headings[i][2]}: "
                f"H{prev_level} → H{curr_level} (should not skip levels). "
                f"Heading: '{headings[i][1]}'"
            )

    return errors


def extract_code_blocks(content: str) -> List[Tuple[Optional[str], str, int]]:
    """
    Extract code blocks from markdown content.

    Returns:
        List of (language, code, line_number) tuples
    """
    code_blocks = []
    lines = content.split('\n')

    in_code_block = False
    block_start = 0
    block_lang = None
    block_content = []

    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if not in_code_block:
                # Starting a code block
                in_code_block = True
                block_start = i
                # Extract language if present
                lang_match = line.strip()[3:].strip()
                block_lang = lang_match if lang_match else None
                block_content = []
            else:
                # Ending a code block
                in_code_block = False
                code_blocks.append((block_lang, '\n'.join(block_content), block_start))
                block_lang = None
                block_content = []
        elif in_code_block:
            block_content.append(line)

    return code_blocks


def check_code_blocks(code_blocks: List[Tuple[Optional[str], str, int]]) -> Tuple[List[str], List[str]]:
    """
    Check code block formatting.

    Returns:
        Tuple of (errors, warnings)
    """
    errors = []
    warnings = []

    blocks_without_lang = [(code, line) for lang, code, line in code_blocks if lang is None]

    if blocks_without_lang:
        for code, line in blocks_without_lang:
            # Check if it's a short block that might be intentional
            if len(code.strip().split('\n')) <= 2:
                warnings.append(f"Code block at line {line} has no language tag (short block, may be intentional)")
            else:
                errors.append(f"Code block at line {line} has no language tag. Add language for proper AI parsing")

    # Check for inline code that should be in code blocks
    # (This is harder to detect accurately, so we'll add a general warning)

    return errors, warnings


def check_inline_code_mixing(content: str) -> List[str]:
    """
    Check for commands or code mixed with prose (anti-pattern).

    Returns:
        List of warnings
    """
    warnings = []

    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Skip if line is in a code block (simple heuristic)
        if line.strip().startswith('```') or line.strip().startswith('    '):
            continue

        # Look for common command patterns embedded in prose
        # Pattern: text followed by command-like text without code block
        if re.search(r'(npm install|pip install|git |curl |docker |kubectl )\S+', line):
            if '`' not in line or line.count('`') < 2:
                warnings.append(
                    f"Line {i} may contain a command in prose without proper formatting. "
                    f"Use code blocks for commands"
                )

    return warnings


def check_document_length(content: str, filename: str) -> List[str]:
    """
    Check document length for AI chunking considerations.

    Returns:
        List of warnings
    """
    warnings = []

    lines = content.split('\n')
    line_count = len(lines)
    word_count = len(content.split())
    char_count = len(content)

    # Rough token estimate (1 token ≈ 4 characters)
    estimated_tokens = char_count // 4

    if line_count > 1000:
        warnings.append(f"Very long document ({line_count} lines, ~{estimated_tokens} tokens). "
                       f"Consider splitting into multiple files for better AI chunking")

    if estimated_tokens > 4000:
        warnings.append(f"Document is ~{estimated_tokens} tokens. "
                       f"Large documents may be split during AI processing. "
                       f"Ensure sections are self-contained")

    return warnings


def check_section_structure(content: str, headings: List[Tuple[int, str, int]]) -> List[str]:
    """
    Check if sections appear self-contained with proper structure.

    Returns:
        List of warnings
    """
    warnings = []

    # Check for very short sections (might lack context)
    lines = content.split('\n')

    for i in range(len(headings)):
        start_line = headings[i][2]
        end_line = headings[i+1][2] if i+1 < len(headings) else len(lines)

        section_lines = lines[start_line:end_line]
        section_content = '\n'.join(section_lines).strip()

        # Count non-empty lines
        non_empty = [l for l in section_lines if l.strip()]

        if len(non_empty) < 3 and headings[i][0] <= 2:  # Only check H1 and H2
            warnings.append(
                f"Very short section at line {headings[i][2]} ('{headings[i][1]}'). "
                f"Consider adding more context for self-containment"
            )

    return warnings


def check_vague_language(content: str) -> List[str]:
    """
    Check for vague pronouns and references that confuse AI.

    Returns:
        List of warnings
    """
    warnings = []

    # Patterns that indicate vague references
    vague_patterns = [
        (r'\bit\b.*\bit\b', "Multiple uses of 'it' in sentence may be ambiguous"),
        (r'\bthis\b.*\bthis\b', "Multiple uses of 'this' in sentence may be ambiguous"),
        (r'\bthey\b.*\bthey\b', "Multiple uses of 'they' in sentence may be ambiguous"),
        (r'\bthem\b.*\bthem\b', "Multiple uses of 'them' in sentence may be ambiguous"),
    ]

    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern, message in vague_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                warnings.append(f"Line {i}: {message}")
                break  # Only report one per line

    return warnings[:5]  # Limit to 5 warnings to avoid spam


def analyze_quality(file_path: Path) -> Dict:
    """
    Perform comprehensive quality analysis.

    Returns:
        Dict with errors, warnings, and metrics
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "errors": [f"Failed to read file: {e}"],
            "warnings": [],
            "metrics": {}
        }

    errors = []
    warnings = []
    metrics = {}

    # Extract document components
    headings = extract_headings(content)
    code_blocks = extract_code_blocks(content)

    # Metrics
    lines = content.split('\n')
    metrics['line_count'] = len(lines)
    metrics['word_count'] = len(content.split())
    metrics['char_count'] = len(content)
    metrics['estimated_tokens'] = len(content) // 4
    metrics['heading_count'] = len(headings)
    metrics['code_block_count'] = len(code_blocks)

    # Run checks
    errors.extend(check_heading_hierarchy(headings))

    code_errors, code_warnings = check_code_blocks(code_blocks)
    errors.extend(code_errors)
    warnings.extend(code_warnings)

    warnings.extend(check_inline_code_mixing(content))
    warnings.extend(check_document_length(content, file_path.name))
    warnings.extend(check_section_structure(content, headings))
    warnings.extend(check_vague_language(content))

    return {
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: check_doc_quality.py <file_path>")
        print("Example: check_doc_quality.py docs/api/authentication.md")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    if not file_path.is_file():
        print(f"❌ Error: Not a file: {file_path}")
        sys.exit(1)

    print(f"🔍 Checking document quality: {file_path}")
    print()

    result = analyze_quality(file_path)

    # Display metrics
    print("📊 METRICS:")
    metrics = result['metrics']
    print(f"  • Lines: {metrics.get('line_count', 0)}")
    print(f"  • Words: {metrics.get('word_count', 0)}")
    print(f"  • Estimated tokens: ~{metrics.get('estimated_tokens', 0)}")
    print(f"  • Headings: {metrics.get('heading_count', 0)}")
    print(f"  • Code blocks: {metrics.get('code_block_count', 0)}")
    print()

    # Display errors
    if result['errors']:
        print("❌ ERRORS:")
        for error in result['errors']:
            print(f"  • {error}")
        print()

    # Display warnings
    if result['warnings']:
        print("⚠️  WARNINGS:")
        for warning in result['warnings']:
            print(f"  • {warning}")
        print()

    # Final status
    if not result['errors'] and not result['warnings']:
        print("✅ Document quality is excellent with no issues")
        sys.exit(0)
    elif not result['errors']:
        print("✅ Document quality is good (with warnings)")
        sys.exit(0)
    else:
        print("❌ Document has quality issues that should be fixed")
        sys.exit(1)


if __name__ == "__main__":
    main()
