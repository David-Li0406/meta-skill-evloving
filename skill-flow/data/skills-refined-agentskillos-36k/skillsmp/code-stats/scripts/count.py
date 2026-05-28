#!/usr/bin/env python3
"""Count lines of code in a codebase."""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.language import (
    detect_language,
    get_comment_patterns,
    is_line_comment,
    find_block_comment_start,
    find_block_comment_end,
)
from utils.markdown import format_language_table, format_directory_table, format_summary, combine_tables


# Directories to skip by default
SKIP_DIRECTORIES = {
    ".git",
    ".github",
    "target",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    "out",
    "bin",
    "obj",
    ".vscode",
    ".idea",
    "cache",
    ".cache",
}


def is_binary_file(filepath: Path) -> bool:
    """
    Check if a file is likely binary.

    Args:
        filepath: Path to file

    Returns:
        True if file appears to be binary
    """
    # Check extension first
    binary_extensions = {
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
        '.exe', '.bin', '.a', '.lib', '.o', '.obj',
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',
        '.pdf', '.zip', '.tar', '.gz', '.rar', '.7z',
        '.mp3', '.mp4', '.avi', '.mov', '.wav',
        '.class', '.jar', '.war', '.ear',
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
    }

    if filepath.suffix.lower() in binary_extensions:
        return True

    # Try to read first 1024 bytes
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            # Check for null bytes (common in binary files)
            if b'\x00' in chunk:
                return True
            # Try to decode as UTF-8
            try:
                chunk.decode('utf-8')
            except UnicodeDecodeError:
                return True
    except (PermissionError, OSError):
        return True

    return False


def count_lines(filepath: Path) -> Dict[str, int]:
    """
    Count lines in a file (code, blank, comment).

    Args:
        filepath: Path to file

    Returns:
        Dictionary with counts: {'code': n, 'blank': m, 'comment': p}
    """
    lang = detect_language(filepath.suffix)
    patterns = get_comment_patterns(lang)

    code_lines = 0
    blank_lines = 0
    comment_lines = 0

    in_block_comment = False
    current_block_marker = None

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped = line.strip()

                # Check blank first
                if not stripped:
                    blank_lines += 1
                    continue

                # Handle block comment end first (in case we're inside one)
                if in_block_comment:
                    # Check if this line ends the block comment
                    found_end, _ = find_block_comment_end(stripped, patterns['block_end'])
                    if found_end:
                        in_block_comment = False
                        current_block_marker = None
                    comment_lines += 1
                    continue

                # Check for block comment start
                found_start, start_idx = find_block_comment_start(stripped, patterns['block_start'])
                if found_start and start_idx == 0:
                    # Line starts with block comment
                    in_block_comment = True
                    comment_lines += 1

                    # Check if block ends on same line
                    found_end, end_idx = find_block_comment_end(stripped[start_idx + len(patterns['block_start'][0]):], patterns['block_end'])
                    if found_end:
                        in_block_comment = False
                    continue

                # Check for line comment
                if is_line_comment(stripped, patterns['line']):
                    comment_lines += 1
                    continue

                # Everything else is code
                code_lines += 1

    except (PermissionError, OSError) as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return {'code': 0, 'blank': 0, 'comment': 0}

    return {
        'code': code_lines,
        'blank': blank_lines,
        'comment': comment_lines,
        'total': code_lines + blank_lines + comment_lines
    }


def scan_directory(
    root: Path,
    extensions: Optional[Set[str]] = None
) -> List[Path]:
    """
    Scan directory for code files.

    Args:
        root: Root directory to scan
        extensions: Set of file extensions to include (with dots, e.g., {'.rs', '.py'})
                   If None, include all files

    Returns:
        List of file paths
    """
    files = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip certain directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRECTORIES]

        for filename in filenames:
            filepath = Path(dirpath) / filename

            # Skip if it's a binary file
            if is_binary_file(filepath):
                continue

            # Filter by extension if specified
            if extensions is not None:
                if filepath.suffix.lower() not in extensions:
                    continue

            files.append(filepath)

    return files


def group_by_language(files: List[Path], root: Path) -> Dict[str, Dict[str, int]]:
    """
    Group files by language and count statistics.

    Args:
        files: List of file paths
        root: Root directory (for relative paths)

    Returns:
        Dictionary mapping language to statistics
    """
    lang_stats: Dict[str, Dict[str, int]] = {}

    for filepath in files:
        # Count lines
        counts = count_lines(filepath)

        # Detect language
        lang = detect_language(filepath.suffix)

        # Initialize language stats if needed
        if lang not in lang_stats:
            lang_stats[lang] = {
                'files': 0,
                'code': 0,
                'blank': 0,
                'comment': 0,
                'total': 0
            }

        # Accumulate counts
        lang_stats[lang]['files'] += 1
        lang_stats[lang]['code'] += counts['code']
        lang_stats[lang]['blank'] += counts['blank']
        lang_stats[lang]['comment'] += counts['comment']
        lang_stats[lang]['total'] += counts['total']

    return lang_stats


def group_by_directory(files: List[Path], root: Path, max_depth: int = 2) -> Dict[str, Dict[str, any]]:
    """
    Group files by directory and count statistics.

    Args:
        files: List of file paths
        root: Root directory
        max_depth: Maximum directory depth to group by

    Returns:
        Dictionary mapping directory to statistics
    """
    dir_stats: Dict[str, Dict[str, any]] = {}

    for filepath in files:
        # Get relative path
        try:
            rel_path = filepath.relative_to(root)
        except ValueError:
            # File is not under root, skip
            continue

        # Get directory at specified depth
        parts = list(rel_path.parts[:-1])  # Exclude filename
        if len(parts) > max_depth:
            parts = parts[:max_depth]
        dir_name = str(Path(*parts)) + "/" if parts else "./"

        # Count lines
        counts = count_lines(filepath)

        # Detect language
        lang = detect_language(filepath.suffix)

        # Initialize directory stats if needed
        if dir_name not in dir_stats:
            dir_stats[dir_name] = {
                'files': 0,
                'code': 0,
                'comment': 0,
                'languages': set()
            }

        # Accumulate counts
        dir_stats[dir_name]['files'] += 1
        dir_stats[dir_name]['code'] += counts['code']
        dir_stats[dir_name]['comment'] += counts['comment']
        dir_stats[dir_name]['languages'].add(lang)

    # Convert sets to sorted lists for consistent output
    for dir_name in dir_stats:
        dir_stats[dir_name]['languages'] = sorted(dir_stats[dir_name]['languages'])

    return dir_stats


def calculate_total(stats: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Calculate total statistics across all entries.

    Args:
        stats: Statistics dictionary (language or directory)

    Returns:
        Total statistics
    """
    total = {
        'files': 0,
        'code': 0,
        'blank': 0,
        'comment': 0,
        'total': 0
    }

    for entry_stats in stats.values():
        total['files'] += entry_stats.get('files', 0)
        total['code'] += entry_stats.get('code', 0)
        total['blank'] += entry_stats.get('blank', 0)
        total['comment'] += entry_stats.get('comment', 0)
        total['total'] += entry_stats.get('total', 0)

    return total


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Count lines of code in a codebase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count all code in current directory
  python scripts/count.py --path .

  # Count only Rust files
  python scripts/count.py --path . --extensions rs

  # Group by directory structure
  python scripts/count.py --path . --group-by directory
        """
    )

    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Root directory to scan (default: current directory)'
    )

    parser.add_argument(
        '--extensions',
        type=str,
        help='Comma-separated file extensions to include (e.g., "rs,py,js")'
    )

    parser.add_argument(
        '--group-by',
        type=str,
        choices=['language', 'directory'],
        default='language',
        help='How to group results (default: language)'
    )

    parser.add_argument(
        '--depth',
        type=int,
        default=2,
        help='Directory depth for grouping (default: 2)'
    )

    args = parser.parse_args()

    # Parse root path
    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Error: Path '{root}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not root.is_dir():
        print(f"Error: Path '{root}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Parse extensions
    extensions = None
    if args.extensions:
        extensions = set(f".{ext.strip()}" if not ext.startswith('.') else ext.strip()
                        for ext in args.extensions.split(','))

    # Scan for files
    print(f"Scanning {root}...", file=sys.stderr)
    files = scan_directory(root, extensions)
    print(f"Found {len(files)} files", file=sys.stderr)

    if not files:
        print("No files found to analyze")
        sys.exit(0)

    # Group and count
    if args.group_by == 'language':
        stats = group_by_language(files, root)
        table = format_language_table(stats)
    else:  # directory
        stats = group_by_directory(files, root, args.depth)
        table = format_directory_table(stats)

    # Calculate totals
    total_stats = calculate_total(stats)
    summary = format_summary(total_stats)

    # Print results
    output = combine_tables(summary, "", table)
    print(output)


if __name__ == '__main__':
    main()
