#!/usr/bin/env python3
"""
Create a new file with content
"""
import argparse
import os
import sys
from pathlib import Path


def create_file(project_root: str, file: str, content: str):
    """Create file with content"""
    
    file_path = Path(project_root) / file
    
    # Create parent directories
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if overwriting
    exists = file_path.exists()
    
    # Write content
    file_path.write_text(content, encoding='utf-8')
    
    result = f"File created: {file}"
    if exists:
        result += " (overwrote existing file)"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Create file with content")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="Relative file path")
    parser.add_argument("--content", required=True, help="File content")
    
    args = parser.parse_args()
    
    try:
        result = create_file(args.project_root, args.file, args.content)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
