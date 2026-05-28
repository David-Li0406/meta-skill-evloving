#!/usr/bin/env python3
"""
Validate symbol files against Schema v2.0.

This script validates symbol JSON files to ensure they conform to Schema v2.0
standards and reports any issues.

Usage:
    python validate_schema.py [file ...]

Example:
    # Validate all symbol files
    python validate_schema.py ai/symbols-*.json

    # Validate specific file
    python validate_schema.py ai/symbols-api-services.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse


# Schema v2.0 required fields
REQUIRED_FIELDS = {'name', 'kind', 'path', 'line', 'signature', 'summary', 'layer'}

# Schema v2.0 optional fields
OPTIONAL_FIELDS = {'parent', 'docstring', 'category'}

# Deprecated fields (should not be present)
DEPRECATED_FIELDS = {'expected_response', 'decorators', 'file_category'}

# Valid layer values
VALID_LAYERS = {
    # Python backend layers
    'router', 'service', 'repository', 'schema', 'model', 'core',
    'middleware', 'auth', 'observability', 'test',
    # TypeScript/JavaScript frontend layers
    'component', 'hook', 'page', 'util',
    # Fallback
    'unknown', 'other'
}


def validate_symbol(symbol: Dict[str, Any], context: str) -> Tuple[List[str], List[str]]:
    """
    Validate a single symbol against Schema v2.0.

    Args:
        symbol: Symbol dictionary
        context: Context string for error messages (e.g., "file:module:symbol")

    Returns:
        Tuple of (errors, warnings) lists
    """
    errors = []
    warnings = []

    symbol_name = symbol.get('name', 'unknown')

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in symbol:
            errors.append(f"{context}:{symbol_name} missing required field '{field}'")

    # Check for deprecated fields
    for field in DEPRECATED_FIELDS:
        if field in symbol:
            errors.append(f"{context}:{symbol_name} has deprecated field '{field}' (should be removed)")

    # Validate layer value
    if 'layer' in symbol:
        layer = symbol['layer']
        if layer not in VALID_LAYERS:
            warnings.append(f"{context}:{symbol_name} has invalid layer '{layer}'")
        if layer in ('unknown', 'other'):
            warnings.append(f"{context}:{symbol_name} has unmapped layer '{layer}'")

    # Check summary is not empty
    if 'summary' in symbol and not symbol['summary'].strip():
        warnings.append(f"{context}:{symbol_name} has empty summary")

    # Check for unknown fields
    all_known_fields = REQUIRED_FIELDS | OPTIONAL_FIELDS | DEPRECATED_FIELDS
    for field in symbol.keys():
        if field not in all_known_fields:
            warnings.append(f"{context}:{symbol_name} has unknown field '{field}'")

    return (errors, warnings)


def validate_file(file_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """
    Validate a symbol file against Schema v2.0.

    Args:
        file_path: Path to symbol JSON file
        verbose: If True, print all errors/warnings

    Returns:
        Validation results dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return {
            'file': file_path.name,
            'valid': False,
            'errors': [f"Invalid JSON: {e}"],
            'warnings': []
        }
    except Exception as e:
        return {
            'file': file_path.name,
            'valid': False,
            'errors': [f"Error reading file: {e}"],
            'warnings': []
        }

    all_errors = []
    all_warnings = []

    # Check version
    if 'version' in data:
        if data['version'] != '2.0':
            all_warnings.append(f"File version is '{data['version']}', expected '2.0'")
    else:
        all_warnings.append("File missing 'version' field")

    # Validate modules
    if 'modules' not in data:
        all_errors.append("File missing 'modules' field")
        return {
            'file': file_path.name,
            'valid': False,
            'errors': all_errors,
            'warnings': all_warnings
        }

    total_symbols = 0
    for i, module in enumerate(data['modules']):
        module_path = module.get('path', f'module_{i}')

        if 'symbols' not in module:
            all_warnings.append(f"Module '{module_path}' has no symbols")
            continue

        for symbol in module['symbols']:
            total_symbols += 1
            errors, warnings = validate_symbol(symbol, f"{file_path.name}:{module_path}")
            all_errors.extend(errors)
            all_warnings.extend(warnings)

    # Check totalSymbols matches
    if 'totalSymbols' in data and data['totalSymbols'] != total_symbols:
        all_warnings.append(f"totalSymbols mismatch: metadata says {data['totalSymbols']}, counted {total_symbols}")

    # Print results
    print(f"\n{file_path.name}:")
    print(f"   Symbols: {total_symbols}")

    if all_errors:
        print(f"   ❌ Errors: {len(all_errors)}")
        if verbose:
            for error in all_errors:
                print(f"      - {error}")
        else:
            for error in all_errors[:3]:
                print(f"      - {error}")
            if len(all_errors) > 3:
                print(f"      ... and {len(all_errors) - 3} more (use --verbose)")

    if all_warnings:
        print(f"   ⚠️  Warnings: {len(all_warnings)}")
        if verbose:
            for warning in all_warnings:
                print(f"      - {warning}")
        else:
            for warning in all_warnings[:3]:
                print(f"      - {warning}")
            if len(all_warnings) > 3:
                print(f"      ... and {len(all_warnings) - 3} more (use --verbose)")

    if not all_errors and not all_warnings:
        print(f"   ✅ Valid Schema v2.0")
    elif not all_errors:
        print(f"   ✅ Valid (with warnings)")

    return {
        'file': file_path.name,
        'valid': len(all_errors) == 0,
        'symbols': total_symbols,
        'errors': all_errors,
        'warnings': all_warnings
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Validate symbol files against Schema v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'files',
        nargs='*',
        type=Path,
        help='Symbol files to validate (default: ai/symbols-*.json)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show all errors and warnings'
    )

    args = parser.parse_args()

    # If no files specified, find all in ai/
    if not args.files:
        args.files = list(Path('ai').glob('symbols-*.json'))

    if not args.files:
        print("❌ No symbol files found", file=sys.stderr)
        sys.exit(1)

    print(f"Validating {len(args.files)} file(s)...")

    results = []
    for file_path in args.files:
        if not file_path.exists():
            print(f"\n{file_path}: ❌ File not found")
            results.append({
                'file': str(file_path),
                'valid': False,
                'errors': ['File not found'],
                'warnings': []
            })
            continue

        result = validate_file(file_path, verbose=args.verbose)
        results.append(result)

    # Summary
    valid_count = sum(1 for r in results if r['valid'])
    total_errors = sum(len(r['errors']) for r in results)
    total_warnings = sum(len(r['warnings']) for r in results)

    print(f"\n{'='*50}")
    print(f"Validation Summary:")
    print(f"   Files: {valid_count}/{len(results)} valid")
    print(f"   Total errors: {total_errors}")
    print(f"   Total warnings: {total_warnings}")

    if valid_count == len(results) and total_warnings == 0:
        print(f"\n✅ All files pass Schema v2.0 validation!")
        sys.exit(0)
    elif valid_count == len(results):
        print(f"\n✅ All files valid (with {total_warnings} warnings)")
        sys.exit(0)
    else:
        print(f"\n❌ {len(results) - valid_count} file(s) failed validation")
        sys.exit(1)


if __name__ == '__main__':
    main()
