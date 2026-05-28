#!/usr/bin/env python3
"""
Find and filter iterations from ITERATIONS.md.

Usage:
    find-iterations.py --id ITR-001
    find-iterations.py --phase "Story Crystallization"
    find-iterations.py --keyword "personas"
    find-iterations.py --id ITR-001,ITR-003 --format json
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


def parse_iteration(entry_text: str) -> dict:
    """
    Parse an iteration entry into structured data.

    Args:
        entry_text: Text of iteration entry (starting with ## ITR-###:)

    Returns:
        Dict with parsed iteration fields
    """
    lines = entry_text.strip().split('\n')

    # Parse header: ## ITR-001: 2026-01-19 — Problem Exploration
    header_match = re.match(r'^## (ITR-\d+):\s*(.+?)\s*—\s*(.+)$', lines[0])
    if not header_match:
        return None

    iteration = {
        'id': header_match.group(1),
        'date_range': header_match.group(2).strip(),
        'phase': header_match.group(3).strip(),
        'goals': '',
        'activities': '',
        'outcomes': '',
        'questions_added': '',
        'decisions_made': '',
        'research_conducted': '',
        'next_steps': ''
    }

    # Parse fields
    current_field = None
    field_content = []

    for line in lines[1:]:
        # Check for field headers
        if line.startswith('**Phase**:'):
            continue  # Skip duplicate phase field
        elif line.startswith('**Goals**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'goals'
            field_content = []
        elif line.startswith('**Activities**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'activities'
            field_content = []
        elif line.startswith('**Key Outcomes**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'outcomes'
            field_content = []
        elif line.startswith('**Questions Added**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'questions_added'
            field_content = [line.replace('**Questions Added**:', '').strip()]
        elif line.startswith('**Decisions Made**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'decisions_made'
            field_content = [line.replace('**Decisions Made**:', '').strip()]
        elif line.startswith('**Research Conducted**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'research_conducted'
            field_content = [line.replace('**Research Conducted**:', '').strip()]
        elif line.startswith('**Next Steps**:'):
            if current_field and field_content:
                iteration[current_field] = '\n'.join(field_content)
            current_field = 'next_steps'
            field_content = []
        else:
            if current_field:
                field_content.append(line)

    # Save last field
    if current_field and field_content:
        iteration[current_field] = '\n'.join(field_content)

    return iteration


def extract_iterations(content: str) -> list:
    """
    Extract all iteration entries from ITERATIONS.md content.

    Args:
        content: Full file content

    Returns:
        List of iteration dicts
    """
    iterations = []

    # Split by iteration headers
    pattern = re.compile(r'^## ITR-\d+:', re.MULTILINE)
    matches = list(pattern.finditer(content))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        entry_text = content[start:end].strip()

        iteration = parse_iteration(entry_text)
        if iteration:
            iterations.append(iteration)

    return iterations


def filter_iterations(iterations: list, filters: dict) -> list:
    """
    Filter iterations based on criteria.

    Args:
        iterations: List of iteration dicts
        filters: Dict of filter criteria

    Returns:
        Filtered list of iterations
    """
    filtered = iterations

    # Filter by IDs
    if filters.get('ids'):
        ids_set = set(filters['ids'])
        filtered = [i for i in filtered if i['id'] in ids_set]

    # Filter by phase
    if filters.get('phase'):
        phase_pattern = re.compile(filters['phase'], re.IGNORECASE)
        filtered = [i for i in filtered if phase_pattern.search(i['phase'])]

    # Filter by keyword
    if filters.get('keyword'):
        keyword_pattern = re.compile(filters['keyword'], re.IGNORECASE)
        filtered = [i for i in filtered if (
            keyword_pattern.search(i['goals']) or
            keyword_pattern.search(i['outcomes']) or
            keyword_pattern.search(i['activities']) or
            keyword_pattern.search(i['next_steps'])
        )]

    return filtered


def format_output(iterations: list, format_type: str) -> str:
    """
    Format iterations for output.

    Args:
        iterations: List of iteration dicts
        format_type: Output format (table, summary, json)

    Returns:
        Formatted string
    """
    if format_type == 'json':
        return json.dumps(iterations, indent=2)

    if format_type == 'summary':
        lines = []
        for i in iterations:
            lines.append(f"{i['id']}: {i['date_range']} — {i['phase']}")
        return '\n'.join(lines)

    # Table format (default)
    if not iterations:
        return "No iterations found."

    lines = ['| ID | Date Range | Phase | Outcomes |']
    lines.append('|----|------------|-------|----------|')

    for i in iterations:
        # Truncate long outcomes
        outcomes = i['outcomes'][:40] + '...' if len(i['outcomes']) > 40 else i['outcomes']
        outcomes = outcomes.replace('\n', ' ')  # Single line
        lines.append(f"| {i['id']} | {i['date_range']} | {i['phase']} | {outcomes} |")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Find and filter iterations from ITERATIONS.md'
    )
    parser.add_argument(
        '--id',
        help='Iteration ID(s) to find (comma-separated for multiple)'
    )
    parser.add_argument(
        '--phase',
        help='Filter by phase name (case-insensitive regex)'
    )
    parser.add_argument(
        '--keyword',
        help='Search by keyword in goals, outcomes, activities, or next steps'
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

        # Load ITERATIONS.md
        iterations_file = discovery_dir / 'archive' / 'ITERATIONS.md'
        if not iterations_file.exists():
            print("No iterations logged yet.", file=sys.stderr)
            return 0

        content = SafeFileOperations.read_file(iterations_file)

        # Extract all iterations
        iterations = extract_iterations(content)

        if not iterations:
            print("No iterations found in ITERATIONS.md")
            return 0

        # Build filters
        filters = {}
        if args.id:
            filters['ids'] = [id.strip() for id in args.id.split(',')]
        if args.phase:
            filters['phase'] = args.phase
        if args.keyword:
            filters['keyword'] = args.keyword

        # Filter iterations
        filtered = filter_iterations(iterations, filters) if filters else iterations

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
