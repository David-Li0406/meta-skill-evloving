#!/usr/bin/env python3
"""
Replace content in a file using exact string matching or regex
"""
import argparse
import os
import sys
from pathlib import Path

# Add serena-skills to path
skills_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(skills_root))

from lib.common.utils import replace_content_advanced, format_error


def replace_content(
    project_root: str,
    file: str,
    old: str,
    new: str,
    mode: str = "literal",
    allow_multiple: bool = False
):
    """Replace content in file"""
    
    file_path = os.path.join(project_root, file)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use advanced replacement with ambiguity detection and backreferences
    new_content, count, first_match_line = replace_content_advanced(
        content, old, new, mode, allow_multiple
    )
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    result = f"Replaced {count} occurrence(s)"
    if first_match_line:
        result += f" (first match at line {first_match_line})"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Replace content in file")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="Relative file path")
    parser.add_argument("--old", required=True, help="Text to find")
    parser.add_argument("--new", required=True, help="Replacement text")
    parser.add_argument("--mode", choices=["literal", "regex"], default="literal", help="Match mode")
    parser.add_argument("--allow-multiple", action="store_true", help="Allow multiple replacements")
    
    args = parser.parse_args()
    
    try:
        result = replace_content(
            args.project_root,
            args.file,
            args.old,
            args.new,
            args.mode,
            args.allow_multiple
        )
        print(result)
    except Exception as e:
        context = {
            "project_root": args.project_root,
            "file": args.file,
            "mode": args.mode,
            "operation": "replace_content"
        }
        print(format_error(e, context), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
