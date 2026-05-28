#!/usr/bin/env python3
"""
Create multiple Azure DevOps work items in batches.

This script formats multiple work items for batch creation using Azure DevOps MCP tools.
Batches are limited to 10 items for optimal MCP server performance.

Usage:
    python create_work_items_batch.py --project "ProjectName" --data '[{...}, {...}]' --batch-size 10

Output (JSON):
    {
        "batches": [
            {
                "batch_number": 1,
                "mcp_tool": "mcp__azure-devops__wit_create_work_item",
                "items": [...]
            }
        ],
        "summary": {
            "total_items": 15,
            "total_batches": 2,
            "batch_size": 10
        }
    }
"""

import argparse
import json
import sys
from typing import List, Dict, Any


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


def format_work_item(project: str, data: dict, objective_ucp: float = None) -> dict:
    """Format a single work item for MCP tool."""

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
        "project": project,
        "workItemType": data.get('work_item_type', 'User Story'),
        "fields": fields,
        "metadata": {
            "work_id": data.get('id'),
            "name": data.get('name'),
            "parent_id": data.get('parent_id')
        }
    }


def create_batches(items: List[dict], batch_size: int = 10) -> List[List[dict]]:
    """Split items into batches of specified size."""
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches


def format_for_batch_creation(project: str, data_list: List[dict], batch_size: int = 10) -> dict:
    """
    Format multiple work items for batch creation.

    Each work item in data_list can have an optional 'objective_ucp' field.
    """
    # Format all work items
    formatted_items = []
    for data in data_list:
        objective_ucp = data.get('objective_ucp')
        formatted = format_work_item(project, data, objective_ucp)
        formatted_items.append(formatted)

    # Split into batches
    batches = create_batches(formatted_items, batch_size)

    # Format output
    result = {
        "batches": [
            {
                "batch_number": idx + 1,
                "mcp_tool": "mcp__azure-devops__wit_create_work_item",
                "items": batch,
                "instructions": f"Call mcp__azure-devops__wit_create_work_item for each item in this batch"
            }
            for idx, batch in enumerate(batches)
        ],
        "summary": {
            "total_items": len(formatted_items),
            "total_batches": len(batches),
            "batch_size": batch_size,
            "items_per_batch": [len(b) for b in batches]
        }
    }

    return result


def format_for_batch_update(updates: List[dict], batch_size: int = 10) -> dict:
    """
    Format multiple work item updates for batch operations.

    Each update should have: id, path, value, op (default: 'Add')
    Example: [
        {"id": 923, "path": "/fields/System.AssignedTo", "value": "user@example.com"},
        {"id": 924, "path": "/fields/System.State", "value": "Active"}
    ]
    """
    # Ensure proper format for updates
    formatted_updates = []
    for update in updates:
        formatted = {
            "id": update["id"],
            "path": update["path"],
            "value": update["value"],
            "op": update.get("op", "Add")
        }
        formatted_updates.append(formatted)

    # Split into batches
    batches = create_batches(formatted_updates, batch_size)

    # Format output
    result = {
        "batches": [
            {
                "batch_number": idx + 1,
                "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
                "updates": batch,
                "instructions": "Call mcp__azure-devops__wit_update_work_items_batch with these updates"
            }
            for idx, batch in enumerate(batches)
        ],
        "summary": {
            "total_updates": len(formatted_updates),
            "total_batches": len(batches),
            "batch_size": batch_size,
            "items_per_batch": [len(b) for b in batches]
        }
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Format work items for batch creation/update in Azure DevOps'
    )
    parser.add_argument('--project', help='Azure DevOps project name (required for creation)')
    parser.add_argument('--data', required=True, help='JSON array of work items or updates')
    parser.add_argument('--operation', choices=['create', 'update'], default='create',
                       help='Operation type: create or update (default: create)')
    parser.add_argument('--batch-size', type=int, default=10,
                       help='Number of items per batch (default: 10)')
    parser.add_argument('--pretty', action='store_true', help='Pretty print output')

    args = parser.parse_args()

    # Validate operation-specific requirements
    if args.operation == 'create' and not args.project:
        print(json.dumps({'error': '--project is required for create operation'}), file=sys.stderr)
        return 1

    try:
        data_list = json.loads(args.data)

        if not isinstance(data_list, list):
            raise ValueError("Data must be a JSON array")

        if args.operation == 'create':
            result = format_for_batch_creation(args.project, data_list, args.batch_size)
        else:  # update
            result = format_for_batch_update(data_list, args.batch_size)

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
