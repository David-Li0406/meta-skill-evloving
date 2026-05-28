#!/usr/bin/env python3
"""
Write content to project memory
"""
import argparse
import os
import sys
from pathlib import Path


def write_memory(project_root: str, name: str, content: str):
    """Write memory to project"""
    memory_dir = Path(project_root) / ".tmp" / ".serena-skills" / "memories"
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure .md extension
    if not name.endswith('.md'):
        name = f"{name}.md"
    
    memory_file = memory_dir / name
    
    memory_file.write_text(content, encoding='utf-8')
    
    return f"Memory saved: {name}"


def main():
    parser = argparse.ArgumentParser(description="Write project memory")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--name", required=True, help="Memory name")
    parser.add_argument("--content", required=True, help="Content to save")
    
    args = parser.parse_args()
    
    try:
        result = write_memory(args.project_root, args.name, args.content)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
