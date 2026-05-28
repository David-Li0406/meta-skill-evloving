#!/usr/bin/env python3
"""
Split symbols-api.json into layer-based chunks for token efficiency.

This script splits the large symbols-api.json file into smaller layer-based
files for targeted loading and improved token efficiency.

Configuration:
    Uses symbols.config.json for input/output paths. Falls back to 'ai/'
    directory if configuration is not available.

Input Format Support:
    Automatically detects and handles two formats:
    - Flat format: {"symbols": [...]} (produced by Python extractor)
    - Module format: {"modules": [...]} (legacy/TypeScript extractor)

Layer Mapping:
- router: HTTP endpoints (app/api/, app/api/endpoints/)
- service: Business logic (app/services/)
- repository: Data access (app/repositories/)
- schema: DTOs and types (app/schemas/)
- core: Models, core, DB, auth, utilities

Usage:
    python split_api_by_layer.py [--dry-run] [--validate-only]

Example:
    # Execute the split
    python split_api_by_layer.py

    # Validate without splitting
    python split_api_by_layer.py --validate-only

    # See what would happen without writing files
    python split_api_by_layer.py --dry-run
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime, timezone
import argparse


# Layer path mappings - symbols are assigned based on path prefixes
LAYER_PATH_MAPPING = {
    'router': ['app/api/', 'app/api/endpoints/'],
    'service': ['app/services/'],
    'repository': ['app/repositories/'],
    'schema': ['app/schemas/'],
    'core': [
        'app/core/', 'app/db/', 'app/models/', 'auth/',
        'app/middleware/', 'app/cache/', 'app/observability/'
    ]
}


def map_symbol_to_layer(module_path: str) -> str:
    """
    Map a module path to its architectural layer.

    Args:
        module_path: Relative path to the module (e.g., "app/api/endpoints/prompts.py")

    Returns:
        Layer name: router, service, repository, schema, or core
    """
    # Normalize path
    path_lower = module_path.lower()

    # Check each layer's path prefixes
    for layer, path_prefixes in LAYER_PATH_MAPPING.items():
        for prefix in path_prefixes:
            if path_lower.startswith(prefix):
                return layer

    # Default to core for unmapped paths
    return 'core'


def validate_split(
    original_modules: List[Dict],
    layers: Dict[str, List[Dict]]
) -> Dict[str, Any]:
    """
    Validate that no symbols were lost during split.

    Args:
        original_modules: Original modules list (normalized to module format)
        layers: Dictionary of layer -> modules mapping

    Returns:
        Validation results dictionary with status and details
    """
    # Count original symbols
    # Works with both flat and module format since we normalize in split_api_by_layer
    original_symbol_count = sum(
        len(module.get('symbols', []))
        for module in original_modules
    )

    # Count split symbols
    split_symbol_count = 0
    layer_counts = {}
    for layer, modules in layers.items():
        count = sum(len(module.get('symbols', [])) for module in modules)
        layer_counts[layer] = count
        split_symbol_count += count

    # Check for duplicates across layers
    seen_symbols = set()
    duplicates = []
    for layer, modules in layers.items():
        for module in modules:
            for symbol in module.get('symbols', []):
                key = (symbol['name'], module['path'], symbol['line'])
                if key in seen_symbols:
                    duplicates.append({
                        'name': symbol['name'],
                        'path': module['path'],
                        'line': symbol['line']
                    })
                seen_symbols.add(key)

    # Validation results
    is_valid = (
        original_symbol_count == split_symbol_count and
        len(duplicates) == 0
    )

    return {
        'valid': is_valid,
        'original_count': original_symbol_count,
        'split_count': split_symbol_count,
        'layer_counts': layer_counts,
        'duplicates': duplicates,
        'symbol_loss': original_symbol_count - split_symbol_count
    }


def create_layer_file_metadata(layer: str, modules: List[Dict]) -> Dict[str, Any]:
    """
    Create metadata for a layer file.

    Args:
        layer: Layer name
        modules: List of modules in this layer

    Returns:
        Metadata dictionary with version, domain, language, etc.
    """
    total_symbols = sum(len(module.get('symbols', [])) for module in modules)

    return {
        'version': '2.0',
        'domain': 'api',
        'layer': layer,
        'language': 'python',
        'generated': datetime.now(timezone.utc).isoformat(),
        'totalModules': len(modules),
        'totalSymbols': total_symbols,
        'modules': modules
    }


def split_api_by_layer(
    input_path: Path,
    output_dir: Path,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Split symbols-api.json into layer-based files.

    Args:
        input_path: Path to symbols-api.json
        output_dir: Directory to write layer files (usually ai/)
        dry_run: If True, don't write files, just report what would happen

    Returns:
        Dictionary with split results and statistics
    """
    print(f"Loading {input_path}...")

    # Load original file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Detect format and normalize to module-based structure
    if 'symbols' in data:
        # Flat format from Python extractor - group by path to create modules
        print("Detected flat symbol format, converting to module structure...")
        symbols_by_path = defaultdict(list)
        for symbol in data['symbols']:
            path = symbol.get('path', 'unknown.py')
            symbols_by_path[path].append(symbol)

        modules = [
            {'path': path, 'symbols': syms}
            for path, syms in symbols_by_path.items()
        ]
        total_symbols = len(data['symbols'])
    elif 'modules' in data:
        # Already in module format (legacy or TypeScript extractor)
        modules = data['modules']
        total_symbols = data.get('totalSymbols', sum(len(m.get('symbols', [])) for m in modules))
    else:
        print("❌ Error: Unknown symbol file format (missing 'symbols' or 'modules' key)")
        return {'success': False, 'error': 'Unknown format'}

    print(f"Loaded {len(modules)} modules with {total_symbols} symbols")

    # Group modules by layer
    layers: Dict[str, List[Dict]] = defaultdict(list)
    unmapped_paths = []

    for module in modules:
        module_path = module.get('path', '')
        layer = map_symbol_to_layer(module_path)

        # Track unmapped paths (those that went to 'core' by default)
        if layer == 'core':
            # Check if it matches any core patterns explicitly
            is_explicitly_core = any(
                module_path.startswith(prefix)
                for prefix in LAYER_PATH_MAPPING['core']
            )
            if not is_explicitly_core:
                unmapped_paths.append(module_path)

        layers[layer].append(module)

    # Validate split
    print("\nValidating split...")
    validation = validate_split(modules, layers)

    if not validation['valid']:
        print(f"❌ VALIDATION FAILED!")
        print(f"   Original symbols: {validation['original_count']}")
        print(f"   Split symbols: {validation['split_count']}")
        print(f"   Symbol loss: {validation['symbol_loss']}")
        if validation['duplicates']:
            print(f"   Duplicates found: {len(validation['duplicates'])}")
        return validation

    print(f"✅ Validation passed - no symbols lost")

    # Print layer statistics
    print("\nLayer Distribution:")
    print(f"{'Layer':<15} {'Modules':<10} {'Symbols':<10} {'Est. Size':<12}")
    print("-" * 50)

    layer_files = {}
    for layer in ['router', 'service', 'repository', 'schema', 'core']:
        module_count = len(layers[layer])
        symbol_count = validation['layer_counts'].get(layer, 0)

        # Estimate file size (rough: 550 bytes per symbol)
        est_size_kb = (symbol_count * 550) // 1024

        print(f"{layer:<15} {module_count:<10} {symbol_count:<10} ~{est_size_kb} KB")

        layer_files[layer] = {
            'filename': f'symbols-api-{layer}s.json',
            'modules': module_count,
            'symbols': symbol_count,
            'size_kb': est_size_kb
        }

    # Show unmapped paths
    if unmapped_paths:
        print(f"\n⚠️  {len(unmapped_paths)} paths assigned to 'core' by default:")
        for path in unmapped_paths[:10]:  # Show first 10
            print(f"   - {path}")
        if len(unmapped_paths) > 10:
            print(f"   ... and {len(unmapped_paths) - 10} more")

    # Write layer files
    if not dry_run:
        print("\nWriting layer files...")

        # Backup original file
        backup_path = output_dir / 'symbols-api.backup.json'
        if not backup_path.exists():
            print(f"Creating backup: {backup_path}")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        # Write each layer file
        for layer, modules in layers.items():
            output_file = output_dir / f'symbols-api-{layer}s.json'
            file_data = create_layer_file_metadata(layer, modules)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(file_data, f, indent=2)

            file_size = output_file.stat().st_size / 1024
            print(f"   ✅ {output_file.name} ({file_size:.1f} KB)")

        print(f"\n✅ Split complete! Created {len(layers)} layer files")
        print(f"   Original file: {input_path.stat().st_size / 1024:.1f} KB")
        total_size = sum(
            (output_dir / f'symbols-api-{layer}s.json').stat().st_size
            for layer in layers.keys()
        )
        print(f"   Total split size: {total_size / 1024:.1f} KB")
        print(f"   Backup saved to: {backup_path}")
    else:
        print("\n🔍 DRY RUN - No files written")

    return {
        'success': True,
        'validation': validation,
        'layer_files': layer_files,
        'unmapped_paths': unmapped_paths,
        'dry_run': dry_run
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Split symbols-api.json into layer-based files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would happen without writing files'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate the split logic, don\'t create files'
    )
    parser.add_argument(
        '--input',
        type=Path,
        help='Input file path (default: from config or ai/symbols-api.json)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory (default: from config or ai/)'
    )

    args = parser.parse_args()

    # Try to load configuration for defaults
    try:
        from config import get_config
        config = get_config()

        # Get paths from config if not provided as arguments
        if args.input is None:
            args.input = config.get_domain_file("api")
        if args.output_dir is None:
            args.output_dir = config.get_symbols_dir()

        print(f"Using configuration: {config.project_name}", file=sys.stderr)

    except Exception as e:
        print(f"Warning: Could not load configuration ({e}), using defaults", file=sys.stderr)

        # Fallback to default paths
        if args.input is None:
            args.input = Path('ai/symbols-api.json')
        if args.output_dir is None:
            args.output_dir = Path('ai')

    # Validate input file exists
    if not args.input.exists():
        print(f"❌ Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Execute split
    dry_run = args.dry_run or args.validate_only
    result = split_api_by_layer(args.input, args.output_dir, dry_run=dry_run)

    if not result.get('success'):
        print("\n❌ Split failed - see errors above", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
