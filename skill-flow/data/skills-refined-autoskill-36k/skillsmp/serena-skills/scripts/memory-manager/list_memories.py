#!/usr/bin/env python3
"""
List all project memories
"""
import argparse
import json
import os
import sys
from pathlib import Path


def list_memories(project_root: str):
    """List all memories in project"""
    memory_dir = Path(project_root) / ".tmp" / ".serena-skills" / "memories"
    
    if not memory_dir.exists():
        return []
    
    memories = []
    for file in sorted(memory_dir.glob("*.md")):
        memories.append(file.stem)  # Name without .md extension
    
    return memories


def main():
    parser = argparse.ArgumentParser(description="List project memories")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    
    args = parser.parse_args()
    
    try:
        memories = list_memories(args.project_root)
        print(json.dumps(memories, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
