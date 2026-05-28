#!/usr/bin/env python3
"""
Backfill Schema v2.0 fields to existing symbol files.

This script updates existing symbol JSON files to conform to Schema v2.0:
- Renames 'file_category' → 'category'
- Removes deprecated fields: 'expected_response', 'decorators'
- Ensures all required fields are present (name, kind, path, line, signature, summary, layer)
- Preserves optional fields (parent, docstring, category)

Usage:
    python backfill_schema.py [--dry-run] [--validate]

Example:
    # Backfill all symbol files
    python backfill_schema.py

    # Validate without modifying
    python backfill_schema.py --validate
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import argparse


# Schema v2.0 required fields
REQUIRED_FIELDS = {'name', 'kind', 'path', 'line', 'signature', 'summary', 'layer'}

# Schema v2.0 optional fields
OPTIONAL_FIELDS = {'parent', 'docstring', 'category'}

# Deprecated fields to remove
DEPRECATED_FIELDS = {'expected_response', 'decorators', 'file_category'}


def backfill_symbol(symbol: Dict[str, Any], module_path: str = None) -> Dict[str, Any]:
    """
    Backfill a single symbol to Schema v2.0.

    Args:
        symbol: Symbol dictionary from old schema
        module_path: Path from module level (for module-based structure)

    Returns:
        Updated symbol dictionary conforming to Schema v2.0
    """
    # Start with required fields
    updated = {}

    # Copy required fields
    for field in REQUIRED_FIELDS:
        if field in symbol:
            updated[field] = symbol[field]
        elif field == 'path' and module_path:
            # In module-based structure, path comes from module level
            updated['path'] = module_path
        elif field == 'layer':
            # If layer is missing, default to 'unknown' (should not happen after Phase 1)
            updated['layer'] = symbol.get('layer', 'unknown')
        elif field == 'path':
            # Missing path and no module_path provided
            print(f"WARNING: Symbol '{symbol.get('name', 'unknown')}' missing 'path' - setting to empty", file=sys.stderr)
            updated['path'] = ''
        elif field == 'signature':
            # Missing signature - use name as fallback
            print(f"WARNING: Symbol '{symbol.get('name', 'unknown')}' missing 'signature' - using name", file=sys.stderr)
            updated['signature'] = symbol.get('name', '')
        elif field == 'summary':
            # Missing summary - use empty string
            updated['summary'] = ''
        else:
            # Missing required field - this is an error
            raise ValueError(f"Symbol missing required field '{field}': {symbol.get('name', 'unknown')}")

    # Rename file_category → category
    if 'file_category' in symbol:
        updated['category'] = symbol['file_category']
    elif 'category' in symbol:
        updated['category'] = symbol['category']

    # Copy other optional fields (but not deprecated ones)
    for field in OPTIONAL_FIELDS:
        if field in symbol and field != 'category':  # category already handled above
            updated[field] = symbol[field]

    return updated


def backfill_module(module: Dict[str, Any]) -> Dict[str, Any]:
    """
    Backfill all symbols in a module.

    Args:
        module: Module dictionary with 'path' and 'symbols'

    Returns:
        Updated module dictionary
    """
    module_path = module.get('path', '')
    updated_module = {'path': module_path}

    if 'symbols' in module:
        updated_module['symbols'] = [
            backfill_symbol(symbol, module_path=module_path)
            for symbol in module['symbols']
        ]

    return updated_module


def backfill_file(file_path: Path, dry_run: bool = False) -> Dict[str, Any]:
    """
    Backfill a symbol file to Schema v2.0.

    Args:
        file_path: Path to symbol JSON file
        dry_run: If True, don't write changes

    Returns:
        Dictionary with results and statistics
    """
    print(f"\nProcessing {file_path.name}...")

    # Load file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_symbols = data.get('totalSymbols', 0)

    # Backfill modules
    if 'modules' in data:
        updated_modules = []
        total_updated = 0
        total_deprecated_removed = 0

        for module in data['modules']:
            original_module_symbols = module.get('symbols', [])

            # Count deprecated fields before backfill
            for symbol in original_module_symbols:
                deprecated_count = sum(1 for field in DEPRECATED_FIELDS if field in symbol)
                total_deprecated_removed += deprecated_count

            # Backfill module
            updated_module = backfill_module(module)
            updated_modules.append(updated_module)
            total_updated += len(updated_module.get('symbols', []))

        # Update data
        data['modules'] = updated_modules

        # Update metadata if present
        if 'version' in data:
            data['version'] = '2.0'

        # Write back
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            new_size = file_path.stat().st_size / 1024
            print(f"   ✅ Updated {total_updated} symbols ({new_size:.1f} KB)")
            if total_deprecated_removed > 0:
                print(f"   🗑️  Removed {total_deprecated_removed} deprecated fields")
        else:
            print(f"   🔍 Would update {total_updated} symbols")
            if total_deprecated_removed > 0:
                print(f"   🔍 Would remove {total_deprecated_removed} deprecated fields")

        return {
            'file': file_path.name,
            'original_symbols': original_symbols,
            'updated_symbols': total_updated,
            'deprecated_removed': total_deprecated_removed,
            'success': True
        }

    return {
        'file': file_path.name,
        'error': 'No modules found',
        'success': False
    }


def validate_file(file_path: Path) -> Dict[str, Any]:
    """
    Validate a symbol file against Schema v2.0.

    Args:
        file_path: Path to symbol JSON file

    Returns:
        Validation results dictionary
    """
    print(f"\nValidating {file_path.name}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    errors = []
    warnings = []

    if 'modules' in data:
        for i, module in enumerate(data['modules']):
            module_path = module.get('path', f'module_{i}')

            for j, symbol in enumerate(module.get('symbols', [])):
                symbol_name = symbol.get('name', f'symbol_{j}')

                # Check required fields
                for field in REQUIRED_FIELDS:
                    if field not in symbol:
                        errors.append(f"{module_path}:{symbol_name} missing required field '{field}'")

                # Check for deprecated fields
                for field in DEPRECATED_FIELDS:
                    if field in symbol:
                        warnings.append(f"{module_path}:{symbol_name} has deprecated field '{field}'")

                # Check layer field value
                if 'layer' in symbol and symbol['layer'] == 'unknown':
                    warnings.append(f"{module_path}:{symbol_name} has layer='unknown'")

    # Check version
    if 'version' in data and data['version'] != '2.0':
        warnings.append(f"File version is '{data['version']}', expected '2.0'")

    if errors:
        print(f"   ❌ {len(errors)} errors found")
        for error in errors[:5]:  # Show first 5
            print(f"      - {error}")
        if len(errors) > 5:
            print(f"      ... and {len(errors) - 5} more")

    if warnings:
        print(f"   ⚠️  {len(warnings)} warnings")
        for warning in warnings[:5]:  # Show first 5
            print(f"      - {warning}")
        if len(warnings) > 5:
            print(f"      ... and {len(warnings) - 5} more")

    if not errors and not warnings:
        print(f"   ✅ Valid Schema v2.0")

    return {
        'file': file_path.name,
        'errors': errors,
        'warnings': warnings,
        'valid': len(errors) == 0
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Backfill Schema v2.0 to symbol files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without modifying files'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Only validate files, don\'t backfill'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        default=Path('ai'),
        help='Directory containing symbol files (default: ai/)'
    )

    args = parser.parse_args()

    # Find all symbol JSON files
    symbol_files = list(args.dir.glob('symbols-*.json'))

    if not symbol_files:
        print(f"❌ No symbol files found in {args.dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(symbol_files)} symbol files")

    results = []

    if args.validate:
        # Validation mode
        for file_path in symbol_files:
            result = validate_file(file_path)
            results.append(result)

        # Summary
        valid_count = sum(1 for r in results if r.get('valid', False))
        print(f"\n{'='*50}")
        print(f"Validation Summary: {valid_count}/{len(results)} files valid")

        if valid_count < len(results):
            sys.exit(1)
    else:
        # Backfill mode
        for file_path in symbol_files:
            result = backfill_file(file_path, dry_run=args.dry_run)
            results.append(result)

        # Summary
        total_updated = sum(r.get('updated_symbols', 0) for r in results if r.get('success'))
        total_deprecated = sum(r.get('deprecated_removed', 0) for r in results if r.get('success'))

        print(f"\n{'='*50}")
        print(f"Backfill Summary:")
        print(f"   Files processed: {len(results)}")
        print(f"   Symbols updated: {total_updated}")
        print(f"   Deprecated fields removed: {total_deprecated}")

        if args.dry_run:
            print("\n🔍 DRY RUN - No files were modified")
        else:
            print("\n✅ Backfill complete!")

    sys.exit(0)


if __name__ == '__main__':
    main()
