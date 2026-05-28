#!/usr/bin/env python3
"""
Create Azure DevOps work item from structured data.

This is a wrapper that formats data for Claude to use with Azure DevOps MCP tools.
Claude should call the appropriate MCP tool with this formatted output.

Usage:
    python create_work_item.py --project "ProjectName" --data '{"work_item_type": "Epic", ...}'

Output (JSON):
    {
        "mcp_tool": "mcp__azure-devops__wit_create_work_item",
        "parameters": {
            "project": "ProjectName",
            "workItemType": "Epic",
            "fields": [...]
        }
    }
"""

import argparse
import json
import sys


PRIORITY_MAPPING = {
    'CRITICAL': 1,
    'HIGH': 1,
    'MEDIUM': 2,
    'LOW': 3,
    'NORMAL': 2
}

STATE_MAPPING = {
    'PLANNING': 'New',
    'IN PLANNING': 'New',
    'READY FOR IMPLEMENTATION': 'New',
    'IN PROGRESS': 'Active',
    'ACTIVE': 'Active',
    'COMPLETED': 'Resolved',
    'DONE': 'Resolved',
    'CLOSED': 'Closed'
}


def map_priority(priority_str: str) -> int:
    """Map priority string to DevOps priority number."""
    return PRIORITY_MAPPING.get(priority_str.upper(), 2)


def map_state(status_str: str) -> str:
    """Map status string to DevOps state."""
    return STATE_MAPPING.get(status_str.upper(), 'New')


def build_title(data: dict) -> str:
    """Build work item title in consistent format."""
    work_type = data.get('work_item_type', 'User Story')
    work_id = data.get('id', '')
    name = data.get('name', '')

    if work_type == 'Epic':
        return f"Epic {work_id}: {name}"
    elif work_type == 'Feature':
        return f"Feature {work_id}: {name}"
    else:
        return f"Sprint {work_id}: {name}"


def build_description(data: dict) -> str:
    """Build comprehensive description with acceptance criteria."""
    parts = [data.get('description', '')]

    # Add acceptance criteria if present
    ac = data.get('acceptance_criteria', [])
    if ac:
        parts.append('\n\n## Acceptance Criteria\n')
        for criterion in ac[:5]:  # Limit to 5
            parts.append(f"- {criterion}")

    # Add task summary if present
    tasks = data.get('tasks', [])
    if tasks:
        total_hours = sum(t.get('estimate_hours', 0) for t in tasks)
        parts.append(f"\n\n## Task Summary\n")
        parts.append(f"- Total Tasks: {len(tasks)}")
        parts.append(f"- Total Estimated Hours: {total_hours}")

    return ''.join(parts)


def format_for_mcp(project: str, data: dict, objective_ucp: float = None) -> dict:
    """Format data for Azure DevOps MCP tool call."""

    fields = [
        {
            "name": "System.Title",
            "value": build_title(data)
        },
        {
            "name": "System.Description",
            "value": build_description(data),
            "format": "Html"
        },
        {
            "name": "Microsoft.VSTS.Common.Priority",
            "value": str(map_priority(data.get('priority', 'Medium')))
        },
        {
            "name": "System.State",
            "value": map_state(data.get('status', 'New'))
        }
    ]

    # Add Objective UCP if provided
    if objective_ucp is not None:
        fields.append({
            "name": "Custom.ObjectiveUCP",
            "value": str(objective_ucp)
        })

    # Add effort for User Stories
    if data.get('work_item_type') == 'User Story':
        total_hours = sum(t.get('estimate_hours', 0) for t in data.get('tasks', []))
        if total_hours > 0:
            fields.append({
                "name": "Microsoft.VSTS.Scheduling.Effort",
                "value": str(total_hours)
            })

    # Add tags if present
    if data.get('tags'):
        fields.append({
            "name": "System.Tags",
            "value": '; '.join(data.get('tags', []))
        })

    return {
        "mcp_tool": "mcp__azure-devops__wit_create_work_item",
        "parameters": {
            "project": project,
            "workItemType": data.get('work_item_type', 'User Story'),
            "fields": fields
        },
        "metadata": {
            "work_id": data.get('id'),
            "name": data.get('name'),
            "parent_id": data.get('parent_id'),
            "tasks_count": len(data.get('tasks', [])),
            "total_hours": sum(t.get('estimate_hours', 0) for t in data.get('tasks', []))
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Format work item data for Azure DevOps MCP tool')
    parser.add_argument('--project', required=True, help='Azure DevOps project name')
    parser.add_argument('--data', required=True, help='JSON data from parse_markdown.py')
    parser.add_argument('--objective-ucp', type=float, help='Objective UCP value')
    parser.add_argument('--pretty', action='store_true', help='Pretty print output')

    args = parser.parse_args()

    try:
        data = json.loads(args.data)
        result = format_for_mcp(args.project, data, args.objective_ucp)

        if args.pretty:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result))

        return 0

    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'Invalid JSON: {e}'}), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
