#!/usr/bin/env python3
"""
List directory contents with optional recursion
"""
import argparse
import json
import os
import sys
from pathlib import Path

# Add serena-skills to path
skills_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(skills_root))

from lib.common.utils import load_ignore_patterns, is_ignored_path, format_error


def list_directory(
    project_root: str,
    relative_path: str,
    recursive: bool = False,
    skip_ignored: bool = False
):
    """List directory contents"""
    
    dir_path = os.path.join(project_root, relative_path)
    
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory not found: {relative_path}")
    
    if not os.path.isdir(dir_path):
        raise ValueError(f"Not a directory: {relative_path}")
    
    # Load ignore patterns if needed
    ignore_spec = None
    if skip_ignored:
        ignore_spec = load_ignore_patterns(project_root)
    
    dirs = []
    files = []
    
    if recursive:
        for root, dirnames, filenames in os.walk(dir_path):
            # Filter ignored directories
            if skip_ignored and ignore_spec:
                dirnames[:] = [
                    d for d in dirnames
                    if not is_ignored_path(
                        os.path.relpath(os.path.join(root, d), project_root),
                        project_root,
                        ignore_spec
                    )
                ]
            
            rel_root = os.path.relpath(root, project_root)
            
            for dirname in dirnames:
                full_dir = os.path.join(rel_root, dirname)
                if skip_ignored and ignore_spec:
                    if not is_ignored_path(full_dir, project_root, ignore_spec):
                        dirs.append(full_dir)
                else:
                    dirs.append(full_dir)
            
            for filename in filenames:
                full_file = os.path.join(rel_root, filename)
                if skip_ignored and ignore_spec:
                    if not is_ignored_path(full_file, project_root, ignore_spec):
                        files.append(full_file)
                else:
                    files.append(full_file)
    else:
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            rel_path = os.path.relpath(full_path, project_root)
            
            if skip_ignored and ignore_spec:
                if is_ignored_path(rel_path, project_root, ignore_spec):
                    continue
            
            if os.path.isdir(full_path):
                dirs.append(rel_path)
            else:
                files.append(rel_path)
    
    return {"dirs": sorted(dirs), "files": sorted(files)}


def main():
    parser = argparse.ArgumentParser(description="List directory contents")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--path", required=True, help="Relative path to directory")
    parser.add_argument("--recursive", action="store_true", help="List recursively")
    parser.add_argument("--skip-ignored", action="store_true", help="Skip ignored files/dirs")
    
    args = parser.parse_args()
    
    try:
        result = list_directory(
            args.project_root,
            args.path,
            args.recursive,
            args.skip_ignored
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        context = {
            "project_root": args.project_root,
            "path": args.path,
            "operation": "list_dir"
        }
        print(format_error(e, context), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
