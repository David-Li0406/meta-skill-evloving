#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
from pathlib import Path

def load_skill(source_path, dest_root):
    """
    Copies a skill from source_path to dest_root/<skill_name>.
    """
    source = Path(source_path).resolve()
    if not source.exists():
        print(f"Error: Source path '{source}' does not exist.")
        sys.exit(1)
    
    if not source.is_dir():
        print(f"Error: Source path '{source}' is not a directory.")
        sys.exit(1)

    skill_name = source.name
    dest_dir = Path(dest_root) / skill_name

    # Create destination root if it doesn't exist
    if not Path(dest_root).exists():
        try:
            os.makedirs(dest_root)
            print(f"Created destination root: {dest_root}")
        except OSError as e:
            print(f"Error creating destination root '{dest_root}': {e}")
            sys.exit(1)

    # Check if destination skill already exists
    if dest_dir.exists():
        print(f"Warning: Destination '{dest_dir}' already exists. Overwriting...")
        shutil.rmtree(dest_dir)

    try:
        shutil.copytree(source, dest_dir)
        print(f"Successfully loaded skill '{skill_name}' to '{dest_dir}'")
    except Exception as e:
        print(f"Error copying skill: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Load a local skill into the project.")
    parser.add_argument("source", help="Path to the source skill directory")
    parser.add_argument("--dest-root", default=".claude/skills", help="Root directory for project skills (default: .claude/skills)")
    
    args = parser.parse_args()
    
    load_skill(args.source, args.dest_root)

if __name__ == "__main__":
    main()
