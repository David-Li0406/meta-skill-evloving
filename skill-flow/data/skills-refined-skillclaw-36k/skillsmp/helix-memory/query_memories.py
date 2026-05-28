#!/usr/bin/env python3
"""
Query Memories Script

Simple CLI tool to query and display memories stored in HelixDB.

Usage:
    ./query_memories.py                        - Show all memories
    ./query_memories.py --search "wordpress"   - Search memories (BM25)
    ./query_memories.py --category preference  - Filter by category
    ./query_memories.py --contexts             - Show all contexts
"""

import sys
import argparse
from pathlib import Path
from pprint import pprint

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "hooks"))

from common import (
    check_helix_running,
    get_all_memories,
    get_all_contexts,
    search_project_locations
)

from load_memories import (
    search_memories_by_keywords,
    extract_keywords
)

def display_memories(memories: list, filter_category: str = None):
    """Display memories in a readable format."""
    if not memories:
        print("No memories found.")
        return

    # Filter by category if specified
    if filter_category:
        memories = [m for m in memories if m.get("category") == filter_category]
        if not memories:
            print(f"No memories found with category: {filter_category}")
            return

    # Sort by importance (highest first)
    memories.sort(key=lambda m: m.get("importance", 0), reverse=True)

    print(f"\n{'='*80}")
    print(f"Found {len(memories)} {'memory' if len(memories) == 1 else 'memories'}")
    print(f"{'='*80}\n")

    for i, memory in enumerate(memories, 1):
        category = memory.get("category", "unknown")
        importance = memory.get("importance", 0)
        content = memory.get("content", "")
        tags = memory.get("tags", "")
        memory_id = memory.get("id", "")

        print(f"[{i}] {category.upper()} (importance: {importance})")
        print(f"    ID: {memory_id}")
        print(f"    Tags: {tags}")
        print(f"    Content: {content[:200]}{'...' if len(content) > 200 else ''}")
        print()

def display_contexts(contexts: list):
    """Display contexts in a readable format."""
    if not contexts:
        print("No contexts found.")
        return

    print(f"\n{'='*80}")
    print(f"Found {len(contexts)} {'context' if len(contexts) == 1 else 'contexts'}")
    print(f"{'='*80}\n")

    for i, context in enumerate(contexts, 1):
        name = context.get("name", "unknown")
        description = context.get("description", "")
        context_type = context.get("context_type", "")
        context_id = context.get("id", "")

        print(f"[{i}] {name} ({context_type})")
        print(f"    ID: {context_id}")
        print(f"    Description: {description}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Query memories from HelixDB")
    parser.add_argument("--search", metavar="QUERY", help="Search memories using BM25 ranking")
    parser.add_argument("--category", help="Filter memories by category")
    parser.add_argument("--contexts", action="store_true", help="Show contexts instead of memories")
    parser.add_argument("--projects", metavar="NAME", nargs="?", const="", help="Show project locations (optional: filter by project name)")
    parser.add_argument("--raw", action="store_true", help="Show raw JSON output")

    args = parser.parse_args()

    # Check if HelixDB is running
    if not check_helix_running():
        print("ERROR: HelixDB is not running. Start it with: helix push dev", file=sys.stderr)
        sys.exit(1)

    if args.search:
        # Search memories using BM25
        keywords = extract_keywords(args.search)
        if not keywords:
            print("No valid search terms provided.")
            sys.exit(1)
        memories = search_memories_by_keywords(keywords)
        if args.raw:
            pprint(memories)
        else:
            print(f"Searching for: {', '.join(keywords)}")
            display_memories(memories, args.category)
    elif args.contexts:
        # Show contexts
        contexts = get_all_contexts()
        if args.raw:
            pprint(contexts)
        else:
            display_contexts(contexts)
    elif args.projects is not None:
        # Show project locations
        project_name = args.projects if args.projects else None
        locations = search_project_locations(project_name)
        if args.raw:
            pprint(locations)
        else:
            display_memories(locations)
    else:
        # Show memories
        memories = get_all_memories()
        if args.raw:
            pprint(memories)
        else:
            display_memories(memories, args.category)

if __name__ == "__main__":
    main()
