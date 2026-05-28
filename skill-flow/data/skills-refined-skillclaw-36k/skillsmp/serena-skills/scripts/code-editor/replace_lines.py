#!/usr/bin/env python3
"""
Replace specific lines in a file
"""
import argparse
import os
import sys


def replace_lines(project_root: str, file: str, start_line: int, end_line: int, new_content: str):
    """Replace lines in file"""
    
    file_path = os.path.join(project_root, file)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Convert to 0-based indexing
    start_idx = start_line - 1
    end_idx = end_line
    
    if start_idx < 0 or end_idx > len(lines):
        raise ValueError(f"Invalid line range: {start_line}-{end_line} (file has {len(lines)} lines)")
    
    # Prepare new content
    if not new_content.endswith('\n'):
        new_content += '\n'
    
    # Replace lines
    new_lines = lines[:start_idx] + [new_content] + lines[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    replaced_count = end_idx - start_idx
    return f"Replaced {replaced_count} line(s) in {file} (lines {start_line}-{end_line})"


def main():
    parser = argparse.ArgumentParser(description="Replace lines in file")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="Relative file path")
    parser.add_argument("--start-line", type=int, required=True, help="Start line (1-based)")
    parser.add_argument("--end-line", type=int, required=True, help="End line (1-based, inclusive)")
    parser.add_argument("--new-content", required=True, help="New content")
    
    args = parser.parse_args()
    
    try:
        result = replace_lines(args.project_root, args.file, args.start_line, args.end_line, args.new_content)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
