#!/usr/bin/env python3
"""
Insert content at a specific line
"""
import argparse
import os
import sys


def insert_at_line(project_root: str, file: str, line: int, content: str):
    """Insert content at line"""
    
    file_path = os.path.join(project_root, file)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Convert to 0-based indexing
    line_idx = line - 1
    
    if line_idx < 0 or line_idx > len(lines):
        raise ValueError(f"Invalid line number: {line} (file has {len(lines)} lines)")
    
    # Prepare content
    if not content.endswith('\n'):
        content += '\n'
    
    # Insert at line
    new_lines = lines[:line_idx] + [content] + lines[line_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return f"Inserted content at line {line} in {file}"


def main():
    parser = argparse.ArgumentParser(description="Insert content at line")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="Relative file path")
    parser.add_argument("--line", type=int, required=True, help="Line number (1-based)")
    parser.add_argument("--content", required=True, help="Content to insert")
    
    args = parser.parse_args()
    
    try:
        result = insert_at_line(args.project_root, args.file, args.line, args.content)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
