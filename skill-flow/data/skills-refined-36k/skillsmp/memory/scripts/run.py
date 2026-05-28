#!/usr/bin/env python3
"""
OpenMemory CLI for AI Agent Long-term Memory Management.

Command-line interface for the memory skill.
Triggered by `/memory` command in opencode.

Usage:
    python run.py add "content" [--tags=tag1,tag2]
    python run.py query "question" [--limit=5]
    python run.py list [--limit=20] [--tags=tag1,tag2]
    python run.py delete <memory_id>
    python run.py clear --confirm
"""

import argparse
import json
import sys
from pathlib import Path


# Add project root to path
def find_project_root():
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (
            (current / ".opencode").exists()
            or (current / "shared" / "context" / "config.yaml").exists()
            or (current / ".git").exists()
        ):
            return current
        if current.parent == current:
            break
        current = current.parent
    return Path(__file__).resolve().parents[4]


PROJECT_ROOT = find_project_root()
sys.path.insert(0, str(PROJECT_ROOT))


def parse_tags(tags_str: str | None) -> list[str] | None:
    """Parse comma-separated tags string into list."""
    if not tags_str:
        return None
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def format_output(data, pretty: bool = True) -> str:
    """Format output data as JSON."""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    return json.dumps(data, ensure_ascii=False, default=str)


def cmd_add(args):
    """Handle add command."""
    from memory_client import MemoryClient

    # Use context-manager user ID to match Context Manager
    client = MemoryClient(user_id="context-manager")
    tags = parse_tags(args.tags)
    result = client.add(args.content, tags=tags)
    print(format_output(result))


def cmd_query(args):
    """Handle query command."""
    from memory_client import MemoryClient

    # Use context-manager user ID to match Context Manager
    client = MemoryClient(user_id="context-manager")
    results = client.query(args.question, limit=args.limit)
    print(format_output({"query": args.question, "results": results}))


def cmd_list(args):
    """Handle list command."""
    from memory_client import MemoryClient

    # Use context-manager user ID to match Context Manager
    client = MemoryClient(user_id="context-manager")
    tags = parse_tags(args.tags)
    memories = client.list_memories(limit=args.limit, tags=tags)
    print(format_output({"memories": memories, "count": len(memories)}))


def cmd_delete(args):
    """Handle delete command."""
    from memory_client import MemoryClient

    # Use context-manager user ID to match Context Manager
    client = MemoryClient(user_id="context-manager")
    result = client.delete(args.memory_id)
    print(format_output(result))


def cmd_status(args):
    """Handle status command."""
    from opencode_memory import ContextManager, load_config

    config = load_config(project_root=PROJECT_ROOT)
    cm = ContextManager(config)
    print(format_output(cm.status()))


def cmd_clear(args):
    """Handle clear command."""
    if not args.confirm:
        print(
            format_output(
                {
                    "status": "error",
                    "message": "Clear requires --confirm flag to prevent accidental data loss",
                }
            )
        )
        sys.exit(1)

    from memory_client import MemoryClient

    client = MemoryClient()
    result = client.clear()
    print(format_output(result))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="OpenMemory - AI Agent Long-term Memory Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "User prefers dark mode" --tags=preferences,ui
  %(prog)s query "What does the user prefer?"
  %(prog)s list --limit=10
  %(prog)s delete abc123
  %(prog)s clear --confirm
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new memory")
    add_parser.add_argument("content", help="Memory content to store")
    add_parser.add_argument(
        "--tags", "-t", help="Comma-separated tags (e.g., 'preferences,ui')"
    )
    add_parser.set_defaults(func=cmd_add)

    # Query command
    query_parser = subparsers.add_parser("query", help="Query memories")
    query_parser.add_argument("question", help="Query question")
    query_parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=5,
        help="Maximum number of results (default: 5)",
    )
    query_parser.set_defaults(func=cmd_query)

    # List command
    list_parser = subparsers.add_parser("list", help="List stored memories")
    list_parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=20,
        help="Maximum number of memories (default: 20)",
    )
    list_parser.add_argument("--tags", "-t", help="Filter by comma-separated tags")
    list_parser.set_defaults(func=cmd_list)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a memory")
    delete_parser.add_argument("memory_id", help="ID of the memory to delete")
    delete_parser.set_defaults(func=cmd_delete)

    # Status command
    status_parser = subparsers.add_parser("status", help="Show memory system status")
    status_parser.set_defaults(func=cmd_status)

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all memories")
    clear_parser.add_argument(
        "--confirm", action="store_true", help="Confirm clearing all memories"
    )
    clear_parser.set_defaults(func=cmd_clear)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except ImportError as e:
        print(
            format_output(
                {
                    "status": "error",
                    "message": str(e),
                    "hint": "Run: pip install openmemory-py",
                }
            )
        )
        sys.exit(1)
    except Exception as e:
        print(format_output({"status": "error", "message": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
