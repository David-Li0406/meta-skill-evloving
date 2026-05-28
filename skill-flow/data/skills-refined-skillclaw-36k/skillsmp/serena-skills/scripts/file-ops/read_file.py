#!/usr/bin/env python3
"""
Read file contents or specific line ranges
"""
import argparse
import json
import os
import sys


def read_file(project_root: str, file: str, start_line: int = 0, end_line: int | None = None):
    """Read file contents"""
    file_path = os.path.join(project_root, file)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"Not a file: {file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if end_line is None:
        result_lines = lines[start_line:]
    else:
        result_lines = lines[start_line:end_line + 1]
    
    return "".join(result_lines)


def main():
    parser = argparse.ArgumentParser(description="Read file contents")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="Relative path to file")
    parser.add_argument("--start-line", type=int, default=0, help="Starting line (0-based)")
    parser.add_argument("--end-line", type=int, help="Ending line (0-based, inclusive)")
    
    args = parser.parse_args()
    
    try:
        content = read_file(args.project_root, args.file, args.start_line, args.end_line)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
