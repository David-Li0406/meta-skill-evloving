#!/usr/bin/env python3
"""HPE Copyright Header Checker and Fixer.

Scans files in a directory, checking for proper HPE copyright headers.
Adds missing headers or updates outdated year references.
"""

import argparse
import fnmatch
import re
import sys
from datetime import datetime
from pathlib import Path

COPYRIGHT_TEMPLATE = (
    "Copyright {start_year}-{end_year} Hewlett Packard Enterprise Development LP"
)
COPYRIGHT_PATTERN = re.compile(
    r"Copyright\s+(\d{4})-(\d{4})\s+Hewlett\s+Packard\s+Enterprise\s+Development\s+LP"
)

COMMENT_SYNTAX = {
    # Hash comments
    ".py": "#",
    ".sh": "#",
    ".bash": "#",
    ".zsh": "#",
    ".rb": "#",
    ".pl": "#",
    ".pm": "#",
    ".r": "#",
    ".R": "#",
    ".jl": "#",
    ".coffee": "#",
    # Double-slash comments
    ".js": "//",
    ".ts": "//",
    ".jsx": "//",
    ".tsx": "//",
    ".go": "//",
    ".c": "//",
    ".cpp": "//",
    ".cc": "//",
    ".cxx": "//",
    ".h": "//",
    ".hpp": "//",
    ".hxx": "//",
    ".cs": "//",
    ".java": "//",
    ".kt": "//",
    ".kts": "//",
    ".scala": "//",
    ".swift": "//",
    ".rs": "//",
    ".dart": "//",
    ".groovy": "//",
    ".gradle": "//",
    ".m": "//",
    ".mm": "//",
    ".php": "//",
    ".v": "//",
    ".sv": "//",
    # Dash-dash comments
    ".sql": "--",
    ".lua": "--",
    ".hs": "--",
    ".elm": "--",
    ".ada": "--",
    # Semicolon comments
    ".lisp": ";",
    ".cl": ";",
    ".clj": ";",
    ".cljs": ";",
    ".edn": ";",
    ".scm": ";",
    ".rkt": ";",
    ".el": ";",
    ".asm": ";",
    ".s": ";",
    # Percent comments
    ".tex": "%",
    ".latex": "%",
    ".m": "%",  # MATLAB (overrides Objective-C for .m files if needed)
    ".erl": "%",
    ".hrl": "%",
    # HTML/XML style (block comments)
    ".html": "<!--",
    ".htm": "<!--",
    ".xml": "<!--",
    ".xhtml": "<!--",
    ".svg": "<!--",
    ".vue": "<!--",
    # CSS style
    ".css": "/*",
    ".scss": "//",
    ".sass": "//",
    ".less": "//",
}

BLOCK_COMMENT_END = {
    "<!--": " -->",
    "/*": " */",
}


def load_ignore_patterns(repo_root: Path) -> list[str]:
    """Load patterns from .gitignore and .copyrightignore files."""
    patterns = []

    for ignore_filename in [".gitignore", ".copyrightignore"]:
        ignore_file = repo_root / ignore_filename
        if not ignore_file.exists():
            continue

        with open(ignore_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)

    return patterns


def should_ignore(file_path: Path, repo_root: Path, patterns: list[str]) -> bool:
    """Check if a file should be ignored based on patterns."""
    rel_path = file_path.relative_to(repo_root)
    rel_str = str(rel_path)
    rel_parts = rel_path.parts

    for pattern in patterns:
        # Strip trailing slashes (directory markers in gitignore)
        pattern_clean = pattern.rstrip("/")

        # Handle directory patterns (ending with /** or had trailing /)
        if pattern.endswith("/**") or pattern.endswith("/"):
            dir_pattern = pattern_clean.rstrip("*").rstrip("/")
            # Check if any part of the path matches the directory name
            if dir_pattern in rel_parts:
                return True
            if rel_str.startswith(dir_pattern + "/"):
                return True

        # Handle extension patterns (*.ext)
        elif pattern_clean.startswith("*."):
            if fnmatch.fnmatch(file_path.name, pattern_clean):
                return True

        # Handle patterns like __pycache__/ or build/
        elif "/" not in pattern_clean and "*" not in pattern_clean:
            # Match as directory name anywhere in path
            if pattern_clean in rel_parts:
                return True
            # Match as exact filename
            if file_path.name == pattern_clean:
                return True

        # Handle glob patterns with paths
        elif fnmatch.fnmatch(rel_str, pattern_clean):
            return True

        # Handle patterns like *.py[cod]
        elif "[" in pattern_clean:
            if fnmatch.fnmatch(file_path.name, pattern_clean):
                return True

    return False


def get_comment_syntax(file_path: Path) -> str | None:
    """Get the comment syntax for a file based on its extension."""
    suffix = file_path.suffix.lower()
    return COMMENT_SYNTAX.get(suffix)


def format_copyright_line(comment_prefix: str, start_year: int, end_year: int) -> str:
    """Format a complete copyright line with comment syntax."""
    copyright_text = COPYRIGHT_TEMPLATE.format(start_year=start_year, end_year=end_year)
    block_end = BLOCK_COMMENT_END.get(comment_prefix, "")
    return f"{comment_prefix} {copyright_text}{block_end}"


def check_and_fix_file(
    file_path: Path, current_year: int, dry_run: bool = False
) -> dict:
    """Check and optionally fix the copyright header in a file.

    Returns a dict with:
        - status: 'ok', 'added', 'updated', 'skipped', 'error'
        - message: description of what happened
    """
    comment_prefix = get_comment_syntax(file_path)
    if comment_prefix is None:
        return {"status": "skipped", "message": "Unknown file type"}

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError) as e:
        return {"status": "error", "message": str(e)}

    lines = content.split("\n") if content else []
    first_line = lines[0] if lines else ""

    # Check if copyright exists
    match = COPYRIGHT_PATTERN.search(first_line)

    if match:
        start_year = int(match.group(1))
        end_year = int(match.group(2))

        if end_year == current_year:
            return {"status": "ok", "message": "Copyright header is current"}

        # Update the year
        new_copyright_line = format_copyright_line(
            comment_prefix, start_year, current_year
        )
        lines[0] = new_copyright_line
        new_content = "\n".join(lines)

        if not dry_run:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

        return {
            "status": "updated",
            "message": f"Updated year: {start_year}-{end_year} → {start_year}-{current_year}",
        }
    else:
        # Add new copyright header
        new_copyright_line = format_copyright_line(
            comment_prefix, current_year, current_year
        )

        if content:
            new_content = new_copyright_line + "\n" + content
        else:
            new_content = new_copyright_line + "\n"

        if not dry_run:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

        return {
            "status": "added",
            "message": f"Added copyright header ({current_year}-{current_year})",
        }


def find_files(repo_root: Path, patterns: list[str]) -> list[Path]:
    """Find all files that should be checked."""
    files = []
    for file_path in repo_root.rglob("*"):
        if file_path.is_file():
            # Skip hidden files and directories
            if any(part.startswith(".") for part in file_path.parts):
                continue
            # Skip if matches ignore patterns
            if should_ignore(file_path, repo_root, patterns):
                continue
            # Skip if no known comment syntax
            if get_comment_syntax(file_path) is None:
                continue
            files.append(file_path)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="Check and fix HPE copyright headers in source files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository root path (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--check-only",
        "-c",
        action="store_true",
        help="Check files and report issues (exit code 1 if issues found)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show all files, including those that are OK",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Current year to use (default: actual current year)",
    )

    args = parser.parse_args()
    repo_root = Path(args.path).resolve()

    if not repo_root.exists():
        print(f"Error: Path does not exist: {repo_root}", file=sys.stderr)
        sys.exit(1)

    current_year = args.year
    patterns = load_ignore_patterns(repo_root)

    print(f"Scanning: {repo_root}")
    print(f"Current year: {current_year}")
    if args.dry_run:
        print("Mode: DRY RUN (no changes will be made)")
    elif args.check_only:
        print("Mode: CHECK ONLY")
    print()

    files = find_files(repo_root, patterns)
    results = {"ok": [], "added": [], "updated": [], "skipped": [], "error": []}

    for file_path in files:
        result = check_and_fix_file(
            file_path,
            current_year,
            dry_run=args.dry_run or args.check_only,
        )
        results[result["status"]].append((file_path, result["message"]))

        if args.verbose or result["status"] not in ("ok", "skipped"):
            rel_path = file_path.relative_to(repo_root)
            status_icon = {
                "ok": "✓",
                "added": "+",
                "updated": "~",
                "skipped": "-",
                "error": "!",
            }[result["status"]]
            print(f"  {status_icon} {rel_path}: {result['message']}")

    # Summary
    print()
    print("Summary:")
    print(f"  ✓ OK:      {len(results['ok'])}")
    print(f"  + Added:   {len(results['added'])}")
    print(f"  ~ Updated: {len(results['updated'])}")
    print(f"  - Skipped: {len(results['skipped'])}")
    print(f"  ! Errors:  {len(results['error'])}")

    # Exit with error if check-only and issues found
    if args.check_only and (results["added"] or results["updated"]):
        print()
        print("ERROR: Files need copyright header fixes!")
        sys.exit(1)

    if results["error"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
