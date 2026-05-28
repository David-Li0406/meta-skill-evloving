#!/usr/bin/env python3
"""
reindent.py - Convert Python file indentation to target spaces.

Auto-detects source indentation and skips files already at target.
Excludes itself from processing.

Usage:
  python reindent.py file.py --to 2
  python reindent.py folder/ --to 2 --recursive
  python reindent.py folder/ --to 2 --recursive --dry-run
"""

import argparse, sys, os
from pathlib import Path


def detect_indentation(content: str) -> int:
  """Detect indentation size (2 or 4 spaces) from file content."""
  for line in content.split('\n'):
    stripped = line.lstrip(' ')
    if stripped and not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
      leading = len(line) - len(stripped)
      if leading > 0:
        # First indented line determines the indent size
        if leading <= 2: return 2
        return 4
  return 4  # Default


def reindent_content(content: str, from_spaces: int, to_spaces: int) -> str:
  """Convert indentation in Python source code."""
  if from_spaces == to_spaces: return content
  
  lines = content.split('\n')
  result = []
  
  for line in lines:
    if not line or line.isspace():
      result.append(line)
      continue
    
    # Count leading spaces
    stripped = line.lstrip(' ')
    leading_spaces = len(line) - len(stripped)
    
    if leading_spaces == 0:
      result.append(line)
      continue
    
    # Calculate new indentation
    indent_levels = leading_spaces // from_spaces
    remainder = leading_spaces % from_spaces
    new_indent = ' ' * (indent_levels * to_spaces + remainder)
    result.append(new_indent + stripped)
  
  return '\n'.join(result)


def process_file(file_path: Path, to_spaces: int, dry_run: bool = False) -> tuple:
  """Process a single file. Returns (changed, message)."""
  try:
    content = file_path.read_text(encoding='utf-8')
  except Exception as e:
    return False, f"ERROR reading -> {e}"
  
  # Auto-detect source indentation
  actual_from = detect_indentation(content)
  if actual_from == to_spaces: return False, f"already {to_spaces}-space"
  
  new_content = reindent_content(content, actual_from, to_spaces)
  
  if content == new_content: return False, "unchanged"
  if dry_run: return True, "would change"
  
  try:
    file_path.write_text(new_content, encoding='utf-8')
    return True, "changed"
  except Exception as e:
    return False, f"ERROR writing -> {e}"


def main():
  parser = argparse.ArgumentParser(description='Convert Python indentation to target spaces. Auto-detects source indentation and skips files already at target.')
  parser.add_argument('path', type=Path, help='File or folder to process')
  parser.add_argument('--to', dest='to_spaces', type=int, default=2, help='Target indent spaces (default: 2)')
  parser.add_argument('--recursive', '-r', action='store_true', help='Process folders recursively')
  parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would change without modifying')
  args = parser.parse_args()
  
  if not args.path.exists():
    print(f"ERROR: Path not found: {args.path}", file=sys.stderr)
    sys.exit(1)
  
  files = []
  if args.path.is_file(): files = [args.path]
  elif args.path.is_dir():
    pattern = '**/*.py' if args.recursive else '*.py'
    files = list(args.path.glob(pattern))
  
  # Exclude this script from processing to avoid self-modification
  this_script = Path(__file__).resolve()
  files = [f for f in files if f.resolve() != this_script]
  
  if not files:
    print("No Python files found.", file=sys.stderr)
    sys.exit(0)
  
  file_word = "file" if len(files) == 1 else "files"
  print(f"Processing {len(files)} {file_word} -> {args.to_spaces}-space indentation", file=sys.stderr)
  if args.dry_run: print("(dry-run mode)", file=sys.stderr)
  
  changed_count = 0
  for f in files:
    changed, msg = process_file(f, args.to_spaces, args.dry_run)
    if changed: changed_count += 1
    print(f"  {msg}: {f}")
  
  file_word = "file" if changed_count == 1 else "files"
  action = "would be changed" if args.dry_run else "changed"
  print(f"\nTotal: {changed_count}/{len(files)} {file_word} {action}", file=sys.stderr)


if __name__ == '__main__':
  main()
