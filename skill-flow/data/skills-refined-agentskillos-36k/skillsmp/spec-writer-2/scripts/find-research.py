#!/usr/bin/env python3
"""
Find and filter research from RESEARCH.md.

Usage:
    find-research.py --story 1
    find-research.py --question Q23
    find-research.py --keyword "CI/CD"
    find-research.py --id R5 --format json
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


def parse_research(entry_text: str) -> dict:
    """Parse a research entry into structured data."""
    lines = entry_text.strip().split('\n')

    # Parse header: ## R5: Topic — 2026-01-18
    header_match = re.match(r'^## (R\d+):\s*(.+?)\s*—\s*(.+)$', lines[0])
    if not header_match:
        return None

    research = {
        'id': header_match.group(1),
        'topic': header_match.group(2).strip(),
        'date': header_match.group(3).strip(),
        'purpose': '',
        'approach': '',
        'findings': '',
        'patterns': '',
        'examples': '',
        'implications': '',
        'stories': '',
        'questions': ''
    }

    # Parse fields
    current_field = None
    field_content = []

    for line in lines[1:]:
        if line.startswith('**Purpose**:'):
            current_field = 'purpose'
            field_content = [line.replace('**Purpose**:', '').strip()]
        elif line.startswith('**Approach**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'approach'
            field_content = [line.replace('**Approach**:', '').strip()]
        elif line.startswith('**Findings**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'findings'
            field_content = []
        elif line.startswith('**Industry Patterns**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'patterns'
            field_content = []
        elif line.startswith('**Relevant Examples**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'examples'
            field_content = []
        elif line.startswith('**Implications**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'implications'
            field_content = []
        elif line.startswith('**Stories Informed**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'stories'
            field_content = [line.replace('**Stories Informed**:', '').strip()]
        elif line.startswith('**Related Questions**:'):
            if current_field and field_content:
                research[current_field] = '\n'.join(field_content)
            current_field = 'questions'
            field_content = [line.replace('**Related Questions**:', '').strip()]
        else:
            if current_field:
                field_content.append(line)

    # Save last field
    if current_field and field_content:
        research[current_field] = '\n'.join(field_content)

    return research


def extract_research(content: str) -> list:
    """Extract all research entries from RESEARCH.md content."""
    research_list = []

    # Split by research headers
    pattern = re.compile(r'^## R\d+:', re.MULTILINE)
    matches = list(pattern.finditer(content))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        entry_text = content[start:end].strip()

        research = parse_research(entry_text)
        if research:
            research_list.append(research)

    return research_list


def filter_research(research_list: list, filters: dict) -> list:
    """Filter research based on criteria."""
    filtered = research_list

    # Filter by IDs
    if filters.get('ids'):
        ids_set = set(filters['ids'])
        filtered = [r for r in filtered if r['id'] in ids_set]

    # Filter by story
    if filters.get('story'):
        story_pattern = re.compile(rf'\bStory {filters["story"]}\b', re.IGNORECASE)
        filtered = [r for r in filtered if story_pattern.search(r['stories'])]

    # Filter by question
    if filters.get('questions'):
        question_pattern = '|'.join(re.escape(q) for q in filters['questions'])
        filtered = [r for r in filtered if re.search(question_pattern, r['questions'])]

    # Filter by keyword
    if filters.get('keyword'):
        keyword_pattern = re.compile(filters['keyword'], re.IGNORECASE)
        filtered = [r for r in filtered if (
            keyword_pattern.search(r['topic']) or
            keyword_pattern.search(r['purpose']) or
            keyword_pattern.search(r['findings'])
        )]

    return filtered


def format_output(research_list: list, format_type: str) -> str:
    """Format research for output."""
    if format_type == 'json':
        return json.dumps(research_list, indent=2)

    if format_type == 'summary':
        lines = []
        for r in research_list:
            lines.append(f"{r['id']}: {r['topic']}")
        return '\n'.join(lines)

    # Table format (default)
    if not research_list:
        return "No research found."

    lines = ['| ID | Topic | Date | Stories |']
    lines.append('|----|-------|------|---------|')

    for r in research_list:
        # Truncate long topics
        topic = r['topic'][:50] + '...' if len(r['topic']) > 50 else r['topic']
        lines.append(f"| {r['id']} | {topic} | {r['date']} | {r['stories']} |")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Find and filter research from RESEARCH.md'
    )
    parser.add_argument(
        '--id',
        help='Research ID(s) to find (comma-separated for multiple)'
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
        help='Search by keyword in topic, purpose, or findings'
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

        # Load RESEARCH.md
        research_file = discovery_dir / 'archive' / 'RESEARCH.md'
        if not research_file.exists():
            print("No research logged yet.", file=sys.stderr)
            return 0

        content = SafeFileOperations.read_file(research_file)

        # Extract all research
        research_list = extract_research(content)

        if not research_list:
            print("No research found in RESEARCH.md")
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

        # Filter research
        filtered = filter_research(research_list, filters) if filters else research_list

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
