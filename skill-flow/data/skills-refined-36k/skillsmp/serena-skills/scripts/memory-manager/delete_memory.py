#!/usr/bin/env python3
"""
Delete a project memory
"""
import argparse
import os
import sys
from pathlib import Path


def delete_memory(project_root: str, name: str):
    """Delete memory from project"""
    memory_dir = Path(project_root) / ".tmp" / ".serena-skills" / "memories"
    
    # Ensure .md extension
    if not name.endswith('.md'):
        name = f"{name}.md"
    
    memory_file = memory_dir / name
    
    if not memory_file.exists():
        raise FileNotFoundError(f"Memory not found: {name}")
    
    memory_file.unlink()
    
    return f"Memory deleted: {name}"


def main():
    parser = argparse.ArgumentParser(description="Delete project memory")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--name", required=True, help="Memory name")
    
    args = parser.parse_args()
    
    try:
        result = delete_memory(args.project_root, args.name)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
