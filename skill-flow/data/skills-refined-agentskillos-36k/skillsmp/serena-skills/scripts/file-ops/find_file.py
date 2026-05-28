#!/usr/bin/env python3
"""
Find files matching a pattern
"""
import argparse
import json
import os
import sys
from pathlib import Path
from fnmatch import fnmatch


def find_files(project_root: str, mask: str, search_path: str = "."):
    """Find files matching pattern"""
    full_search_path = os.path.join(project_root, search_path)
    
    if not os.path.exists(full_search_path):
        raise FileNotFoundError(f"Path not found: {search_path}")
    
    matches = []
    
    for root, dirs, files in os.walk(full_search_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.serena'}]
        
        for filename in files:
            if fnmatch(filename, mask):
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, project_root)
                matches.append(rel_path)
    
    return sorted(matches)


def main():
    parser = argparse.ArgumentParser(description="Find files matching a pattern")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--mask", required=True, help="Filename pattern (* and ? wildcards)")
    parser.add_argument("--path", default=".", help="Search within relative path")
    
    args = parser.parse_args()
    
    try:
        matches = find_files(args.project_root, args.mask, args.path)
        print(json.dumps(matches, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
