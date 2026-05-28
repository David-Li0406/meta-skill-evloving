#!/usr/bin/env python3
"""
Get next sequential ID for any entity type.

Usage:
    next-id.py decision
    next-id.py question
    next-id.py functional_requirement
    next-id.py --discovery-path ../discovery question
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.id_manager import IDManager


def main():
    parser = argparse.ArgumentParser(
        description='Get next sequential ID for entity type'
    )
    parser.add_argument(
        'entity_type',
        choices=[
            'decision', 'research', 'question', 'functional_requirement',
            'edge_case', 'success_criteria', 'revision', 'iteration', 'story'
        ],
        help='Type of entity'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Get next ID
        id_manager = IDManager(discovery_dir)
        next_id = id_manager.get_next_id(args.entity_type)

        # Output just the ID (for easy scripting)
        print(next_id)
        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
