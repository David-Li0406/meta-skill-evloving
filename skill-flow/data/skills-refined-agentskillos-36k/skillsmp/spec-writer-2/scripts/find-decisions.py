#!/usr/bin/env python3
"""
Find and filter decisions from DECISIONS.md.

Usage:
    find-decisions.py --story 1
    find-decisions.py --question Q23
    find-decisions.py --keyword "notification"
    find-decisions.py --id D5 --format json
    find-decisions.py --id D3,D4,D5
"""

import sys
import argparse
import re
import json
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.file_operations import SafeFileOperations


def parse_decision(entry_text: str) -> dict:
    """
    Parse a decision entry into structured data.

    Args:
        entry_text: Text of decision entry (starting with ## D#:)

    Returns:
        Dict with parsed decision fields
    """
    lines = entry_text.strip().split('\n')

    # Parse header: ## D15: Title — 2026-01-18
    header_match = re.match(r'^## (D\d+):\s*(.+?)\s*—\s*(.+)$', lines[0])
    if not header_match:
        return None

    decision = {
        'id': header_match.group(1),
        'title': header_match.group(2).strip(),
        'date': header_match.group(3).strip(),
        'context': '',
        'question': '',
        'options': '',
        'decision': '',
        'rationale': '',
        'implications': '',
        'stories': '',
        'questions': ''
    }

    # Parse fields
    current_field = None
    field_content = []

    for line in lines[1:]:
        # Check for field headers
        if line.startswith('**Context**:'):
            current_field = 'context'
            field_content = [line.replace('**Context**:', '').strip()]
        elif line.startswith('**Question**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'question'
            field_content = [line.replace('**Question**:', '').strip()]
        elif line.startswith('**Options Considered**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'options'
            field_content = []
        elif line.startswith('**Decision**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'decision'
            field_content = [line.replace('**Decision**:', '').strip()]
        elif line.startswith('**Rationale**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'rationale'
            field_content = [line.replace('**Rationale**:', '').strip()]
        elif line.startswith('**Implications**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'implications'
            field_content = []
        elif line.startswith('**Stories Affected**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'stories'
            field_content = [line.replace('**Stories Affected**:', '').strip()]
        elif line.startswith('**Related Questions**:'):
            if current_field and field_content:
                decision[current_field] = '\n'.join(field_content)
            current_field = 'questions'
            field_content = [line.replace('**Related Questions**:', '').strip()]
        else:
            if current_field:
                field_content.append(line)

    # Save last field
    if current_field and field_content:
        decision[current_field] = '\n'.join(field_content)

    return decision


def extract_decisions(content: str) -> list:
    """
    Extract all decision entries from DECISIONS.md content.

    Args:
        content: Full file content

    Returns:
        List of decision dicts
    """
    decisions = []

    # Split by decision headers
    pattern = re.compile(r'^## D\d+:', re.MULTILINE)
    matches = list(pattern.finditer(content))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        entry_text = content[start:end].strip()

        decision = parse_decision(entry_text)
        if decision:
            decisions.append(decision)

    return decisions


def filter_decisions(decisions: list, filters: dict) -> list:
    """
    Filter decisions based on criteria.

    Args:
        decisions: List of decision dicts
        filters: Dict of filter criteria

    Returns:
        Filtered list of decisions
    """
    filtered = decisions

    # Filter by IDs
    if filters.get('ids'):
        ids_set = set(filters['ids'])
        filtered = [d for d in filtered if d['id'] in ids_set]

    # Filter by story
    if filters.get('story'):
        story_pattern = re.compile(rf'\bStory {filters["story"]}\b', re.IGNORECASE)
        filtered = [d for d in filtered if story_pattern.search(d['stories'])]

    # Filter by question
    if filters.get('questions'):
        question_pattern = '|'.join(re.escape(q) for q in filters['questions'])
        filtered = [d for d in filtered if re.search(question_pattern, d['questions'])]

    # Filter by keyword
    if filters.get('keyword'):
        keyword_pattern = re.compile(filters['keyword'], re.IGNORECASE)
        filtered = [d for d in filtered if (
            keyword_pattern.search(d['title']) or
            keyword_pattern.search(d['context']) or
            keyword_pattern.search(d['rationale'])
        )]

    return filtered


def format_output(decisions: list, format_type: str) -> str:
    """
    Format decisions for output.

    Args:
        decisions: List of decision dicts
        format_type: Output format (table, summary, json)

    Returns:
        Formatted string
    """
    if format_type == 'json':
        return json.dumps(decisions, indent=2)

    if format_type == 'summary':
        lines = []
        for d in decisions:
            lines.append(f"{d['id']}: {d['title']}")
        return '\n'.join(lines)

    # Table format (default)
    if not decisions:
        return "No decisions found."

    lines = ['| ID | Title | Date | Stories |']
    lines.append('|----|-------|------|---------|')

    for d in decisions:
        # Truncate long titles
        title = d['title'][:50] + '...' if len(d['title']) > 50 else d['title']
        lines.append(f"| {d['id']} | {title} | {d['date']} | {d['stories']} |")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Find and filter decisions from DECISIONS.md'
    )
    parser.add_argument(
        '--id',
        help='Decision ID(s) to find (comma-separated for multiple)'
    )
    parser.add_argument(
        '--story',
        help='Filter by story number'
    )
    parser.add_argument(
        '--question',
        help='Filter by question IDs (comma-separated)'
    )
    parser.add_argument(
        '--keyword',
        help='Search by keyword in title, context, or rationale'
    )
    parser.add_argument(
        '--format',
        choices=['table', 'summary', 'json'],
        default='table',
        help='Output format (default: table)'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Load DECISIONS.md
        decisions_file = discovery_dir / 'archive' / 'DECISIONS.md'
        if not decisions_file.exists():
            print("No decisions logged yet.", file=sys.stderr)
            return 0

        content = SafeFileOperations.read_file(decisions_file)

        # Extract all decisions
        decisions = extract_decisions(content)

        if not decisions:
            print("No decisions found in DECISIONS.md")
            return 0

        # Build filters
        filters = {}
        if args.id:
            filters['ids'] = [id.strip() for id in args.id.split(',')]
        if args.story:
            filters['story'] = args.story
        if args.question:
            filters['questions'] = [q.strip() for q in args.question.split(',')]
        if args.keyword:
            filters['keyword'] = args.keyword

        # Filter decisions
        filtered = filter_decisions(decisions, filters) if filters else decisions

        # Format and output
        output = format_output(filtered, args.format)
        print(output)

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
