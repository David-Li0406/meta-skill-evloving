#!/usr/bin/env python3
"""
Search for regex patterns in files
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from fnmatch import fnmatch


CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.r',
    '.m', '.sql', '.sh', '.bash', '.pl', '.lua', '.vim', '.el'
}


def should_search_file(file_path: str, code_only: bool, include_glob: str | None, exclude_glob: str | None) -> bool:
    """Determine if file should be searched"""
    filename = os.path.basename(file_path)
    
    # Check exclude first
    if exclude_glob and fnmatch(file_path, exclude_glob):
        return False
    
    # Check include
    if include_glob and not fnmatch(file_path, include_glob):
        return False
    
    # Check code-only
    if code_only:
        ext = Path(file_path).suffix.lower()
        return ext in CODE_EXTENSIONS
    
    return True


def search_pattern(
    project_root: str,
    pattern: str,
    search_path: str = "",
    context: int = 0,
    code_only: bool = False,
    include_glob: str | None = None,
    exclude_glob: str | None = None
):
    """Search for regex pattern in files"""
    
    if search_path:
        full_search_path = os.path.join(project_root, search_path)
    else:
        full_search_path = project_root
    
    if not os.path.exists(full_search_path):
        raise FileNotFoundError(f"Path not found: {search_path}")
    
    # Compile regex with DOTALL flag
    regex = re.compile(pattern, re.DOTALL | re.IGNORECASE)
    
    results = {}
    
    # Determine if searching file or directory
    if os.path.isfile(full_search_path):
        search_files = [full_search_path]
    else:
        search_files = []
        for root, dirs, files in os.walk(full_search_path):
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.serena'}]
            
            for filename in files:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, project_root)
                
                if should_search_file(rel_path, code_only, include_glob, exclude_glob):
                    search_files.append(file_path)
    
    # Search each file
    for file_path in search_files:
        rel_path = os.path.relpath(file_path, project_root)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            matches = []
            for i, line in enumerate(lines):
                if regex.search(line):
                    # Get context
                    start_idx = max(0, i - context)
                    end_idx = min(len(lines), i + context + 1)
                    
                    context_lines = []
                    for j in range(start_idx, end_idx):
                        prefix = ">>> " if j == i else "    "
                        context_lines.append(f"{prefix}{j+1}: {lines[j].rstrip()}")
                    
                    matches.append({
                        "line": i + 1,
                        "content": "\n".join(context_lines)
                    })
            
            if matches:
                results[rel_path] = matches
        
        except Exception as e:
            # Skip files that can't be read
            pass
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Search for regex patterns in files")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--pattern", required=True, help="Regex pattern to search")
    parser.add_argument("--path", default="", help="Restrict to directory/file")
    parser.add_argument("--context", type=int, default=0, help="Lines of context")
    parser.add_argument("--code-only", action="store_true", help="Search only code files")
    parser.add_argument("--include-glob", help="Include pattern (e.g., '*.py')")
    parser.add_argument("--exclude-glob", help="Exclude pattern (e.g., '*test*')")
    
    args = parser.parse_args()
    
    try:
        results = search_pattern(
            args.project_root,
            args.pattern,
            args.path,
            args.context,
            args.code_only,
            args.include_glob,
            args.exclude_glob
        )
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
