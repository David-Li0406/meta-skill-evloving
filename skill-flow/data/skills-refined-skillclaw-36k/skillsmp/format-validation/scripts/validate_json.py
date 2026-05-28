#!/usr/bin/env python3
"""
JSON Format Validation Script
Scans directories and validates JSON file formats
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_json_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate a single JSON file

    Args:
        file_path: Path to the JSON file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON decode error at line {e.lineno}, column {e.colno}: {e.msg}"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def scan_directory(directory: str, recursive: bool = True) -> List[str]:
    """
    Scan directory for JSON files

    Args:
        directory: Directory to scan
        recursive: Whether to scan subdirectories

    Returns:
        List of JSON file paths
    """
    json_files = []
    path = Path(directory)

    if not path.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return []

    if not path.is_dir():
        print(f"Error: '{directory}' is not a directory")
        return []

    if recursive:
        pattern = '**/*.json'
    else:
        pattern = '*.json'

    for file_path in path.glob(pattern):
        # Skip files/directories in hidden folders (starting with .)
        if any(part.startswith('.') for part in file_path.parts):
            continue
        # Skip files/directories in venv, __pycache__, node_modules, etc.
        ignored_dirs = ['venv', '__pycache__', 'node_modules', '.venv', 'env', 'virtualenv']
        if any(part in ignored_dirs for part in file_path.parts):
            continue
        if file_path.is_file():
            json_files.append(str(file_path))

    return sorted(json_files)


def validate_json_files(directory: str, recursive: bool = True) -> Dict:
    """
    Validate all JSON files in directory

    Args:
        directory: Directory to scan
        recursive: Whether to scan subdirectories

    Returns:
        Dictionary with validation results
    """
    json_files = scan_directory(directory, recursive)
    results = {
        'directory': directory,
        'total_files': len(json_files),
        'valid_files': 0,
        'invalid_files': 0,
        'valid': [],
        'invalid': []
    }

    for file_path in json_files:
        is_valid, error_msg = validate_json_file(file_path)

        if is_valid:
            results['valid_files'] += 1
            results['valid'].append(file_path)
            print(f"✓ {file_path}")
        else:
            results['invalid_files'] += 1
            results['invalid'].append({
                'file': file_path,
                'error': error_msg
            })
            print(f"✗ {file_path}")
            print(f"  Error: {error_msg}")

    return results


def print_summary(results: Dict):
    """Print validation summary"""
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Directory: {results['directory']}")
    print(f"Total JSON files: {results['total_files']}")
    print(f"Valid files: {results['valid_files']}")
    print(f"Invalid files: {results['invalid_files']}")

    if results['invalid_files'] > 0:
        print("\nInvalid files:")
        for item in results['invalid']:
            print(f"  - {item['file']}")
            print(f"    {item['error']}")

    print("="*60)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py <directory> [--no-recursive]")
        print("\nArguments:")
        print("  directory    Path to directory to scan for JSON files")
        print("  --no-recursive  Scan only the top-level directory (default: recursive)")
        sys.exit(1)

    directory = sys.argv[1]
    recursive = '--no-recursive' not in sys.argv[2:]

    print(f"Validating JSON files in: {directory}")
    if recursive:
        print("(recursive scan)")
    else:
        print("(top-level only)")
    print()

    results = validate_json_files(directory, recursive)
    print_summary(results)

    # Exit with error code if any files are invalid
    sys.exit(1 if results['invalid_files'] > 0 else 0)


if __name__ == '__main__':
    main()
