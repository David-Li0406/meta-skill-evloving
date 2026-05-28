#!/usr/bin/env python3
"""
Edit memory using find/replace
"""
import argparse
import sys
from pathlib import Path

# Add serena-skills to path
skills_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(skills_root))

from lib.common.utils import replace_content_advanced, format_error


def edit_memory(project_root: str, name: str, needle: str, replace: str, mode: str = "literal"):
    """Edit memory file"""
    memory_dir = Path(project_root) / ".tmp" / ".serena-skills" / "memories"
    
    if not name.endswith('.md'):
        name = f"{name}.md"
    
    memory_file = memory_dir / name
    
    if not memory_file.exists():
        raise FileNotFoundError(f"Memory not found: {name}")
    
    content = memory_file.read_text(encoding='utf-8')
    
    # Use advanced replacement
    new_content, count, first_match_line = replace_content_advanced(
        content, needle, replace, mode, allow_multiple=False
    )
    
    memory_file.write_text(new_content, encoding='utf-8')
    
    result = f"Memory updated: {name} ({count} replacement(s))"
    if first_match_line:
        result += f" at line {first_match_line}"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Edit project memory")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--name", required=True, help="Memory name")
    parser.add_argument("--needle", required=True, help="Text to find")
    parser.add_argument("--replace", required=True, help="Replacement text")
    parser.add_argument("--mode", choices=["literal", "regex"], default="literal", help="Match mode")
    
    args = parser.parse_args()
    
    try:
        result = edit_memory(args.project_root, args.name, args.needle, args.replace, args.mode)
        print(result)
    except Exception as e:
        context = {
            "project_root": args.project_root,
            "memory": args.name,
            "operation": "edit_memory"
        }
        print(format_error(e, context), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
