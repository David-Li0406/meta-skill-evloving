#!/usr/bin/env python3
"""
Parse Epic, Feature, or Sprint markdown files to extract structured metadata.

Usage:
    python parse_markdown.py <markdown_file_path>

Output (JSON):
    {
        "work_item_type": "Epic|Feature|User Story",
        "id": "1" or "101.1" or "101.1.1",
        "name": "Update Existing Services",
        "status": "Planning",
        "priority": "CRITICAL",
        "duration": "1.5 weeks",
        "description": "Combined overview text",
        "tasks": [
            {"name": "Task 1.1", "estimate_hours": 3, "description": "..."},
            ...
        ],
        "parent_id": "101" (for features/sprints),
        "success_criteria": ["criterion 1", "criterion 2"],
        "acceptance_criteria": ["AC 1", "AC 2"]
    }
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_frontmatter(content: str) -> dict:
    """Extract metadata from the header section of markdown."""
    metadata = {}

    # Extract ID and Name from first heading
    # Pattern: # Epic 1: Name OR # Feature 101.1: Name OR # Sprint 101.1.1: Name
    match = re.search(r'^#\s+(Epic|Feature|Sprint)\s+([\d.]+):\s+(.+)$', content, re.MULTILINE)
    if match:
        work_type = match.group(1)
        metadata['id'] = match.group(2)
        metadata['name'] = match.group(3).strip()

        # Map to DevOps work item types
        type_mapping = {
            'Epic': 'Epic',
            'Feature': 'Feature',
            'Sprint': 'User Story'
        }
        metadata['work_item_type'] = type_mapping.get(work_type, 'User Story')

    # Extract bold metadata fields
    # Pattern: **Epic ID**: 1 **Epic Name**: Name **Status**: Planning
    for match in re.finditer(r'\*\*([^*]+)\*\*:\s*([^\n*]+)', content):
        key = match.group(1).strip().lower().replace(' ', '_')
        value = match.group(2).strip()
        metadata[key] = value

    return metadata


def extract_description(content: str) -> str:
    """Extract description from overview sections."""
    sections = []

    # Look for common overview sections
    overview_patterns = [
        r'##\s+Epic Overview\s*\n(.*?)(?=\n##|\Z)',
        r'##\s+Executive Summary\s*\n(.*?)(?=\n##|\Z)',
        r'##\s+Sprint Goals\s*\n(.*?)(?=\n##|\Z)',
        r'###\s+Purpose\s*\n(.*?)(?=\n###|\n##|\Z)',
    ]

    for pattern in overview_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sections.append(match.group(1).strip())

    # Combine sections, limit to 2000 chars for DevOps
    description = '\n\n'.join(sections)
    if len(description) > 2000:
        description = description[:1997] + '...'

    return description or 'No description available'


def extract_tasks(content: str) -> list:
    """Extract task information with estimates."""
    tasks = []

    # Pattern: **TASK-001: Create GlobalServices class structure**
    # - Estimated: 4 hours
    task_pattern = r'\*\*TASK-(\d+):\s+([^*]+)\*\*\s*\n\s*-\s*Estimated:\s*(\d+)\s*hours?'

    for match in re.finditer(task_pattern, content, re.IGNORECASE):
        tasks.append({
            'task_id': match.group(1),
            'name': match.group(2).strip(),
            'estimate_hours': int(match.group(3))
        })

    # Alternative pattern: ### Task 1.1: Update AgentInstallationService
    # **Estimated Effort**: 2 hours development
    alt_pattern = r'###\s+Task\s+([\d.]+):\s+([^\n]+)\n.*?\*\*Estimated Effort\*\*:\s*(\d+)\s*hours?'

    for match in re.finditer(alt_pattern, content, re.DOTALL | re.IGNORECASE):
        tasks.append({
            'task_id': match.group(1),
            'name': match.group(2).strip(),
            'estimate_hours': int(match.group(3))
        })

    return tasks


def extract_acceptance_criteria(content: str) -> list:
    """Extract acceptance criteria checkboxes."""
    criteria = []

    # Pattern: - [ ] Criterion text OR - [x] Criterion text
    pattern = r'-\s+\[[x ]\]\s+(.+)$'

    for match in re.finditer(pattern, content, re.MULTILINE):
        criteria.append(match.group(1).strip())

    return criteria[:10]  # Limit to top 10


def infer_parent_id(metadata: dict) -> str:
    """Infer parent ID from work item ID."""
    work_id = metadata.get('id', '')
    work_type = metadata.get('work_item_type', '')

    if work_type == 'Feature' and '.' in work_id:
        # Feature 101.1 → parent Epic 101
        return work_id.split('.')[0]
    elif work_type == 'User Story' and work_id.count('.') >= 2:
        # Sprint 101.1.1 → parent Feature 101.1
        parts = work_id.split('.')
        return f"{parts[0]}.{parts[1]}"

    # Check for explicit parent in metadata
    return metadata.get('epic', metadata.get('feature', None))


def parse_markdown_file(file_path: str) -> dict:
    """Parse markdown file and return structured data."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text(encoding='utf-8')

    # Extract all components
    metadata = extract_frontmatter(content)

    result = {
        'work_item_type': metadata.get('work_item_type', 'User Story'),
        'id': metadata.get('id', ''),
        'name': metadata.get('name', metadata.get('epic_name', metadata.get('feature_name', metadata.get('sprint_name', '')))),
        'status': metadata.get('status', 'New'),
        'priority': metadata.get('priority', 'Medium'),
        'duration': metadata.get('duration', metadata.get('estimated_duration', '')),
        'description': extract_description(content),
        'tasks': extract_tasks(content),
        'parent_id': infer_parent_id(metadata),
        'acceptance_criteria': extract_acceptance_criteria(content)
    }

    return result


def main():
    parser = argparse.ArgumentParser(description='Parse markdown file for DevOps work item creation')
    parser.add_argument('file_path', help='Path to markdown file')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON output')

    args = parser.parse_args()

    try:
        result = parse_markdown_file(args.file_path)

        if args.pretty:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result))

        return 0

    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
