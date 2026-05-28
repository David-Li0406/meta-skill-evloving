#!/usr/bin/env python3
"""
Symbol Merger

Merges programmatically extracted symbols into existing symbol graphs. Handles
incremental updates, validates consistency, and preserves existing relationships.

Configuration:
    Uses symbols.config.json for domain file paths. Falls back to default
    'ai/' directory if configuration is not available.

Usage:
    python merge_symbols.py --domain=<domain> --input=<file.json> [--validate] [--backup]

Examples:
    # Merge API symbols with validation and backup
    python merge_symbols.py --domain=api --input=extracted_api.json --validate --backup

    # Merge UI symbols without backup
    python merge_symbols.py --domain=ui --input=extracted_ui.json

    # Merge shared symbols with validation only
    python merge_symbols.py --domain=shared --input=extracted_shared.json --validate

Supported Domains:
    - ui: Frontend components, hooks, pages (symbols-ui.json)
    - api: Backend services, routers, repositories (symbols-api.json)
    - shared: Utilities, types, configs (symbols-shared.json)

Input Format:
    {
        "symbols": [
            {
                "name": "SymbolName",
                "kind": "class|function|component|etc",
                "path": "relative/path/to/file.py",
                "line": 42,
                "signature": "function signature",
                "summary": "Description"
            }
        ]
    }

The script will:
    1. Load the existing domain symbol file
    2. Merge new symbols (update existing, add new)
    3. Validate for duplicates and consistency
    4. Create backup if requested
    5. Write updated symbol file
"""

import json
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional
from datetime import datetime, timezone
from collections import defaultdict
import argparse


class SymbolMerger:
    """Handles merging of extracted symbols into existing symbol graphs."""

    def __init__(self, project_root: Path, config=None):
        """
        Initialize SymbolMerger.

        Args:
            project_root: Project root directory
            config: Optional SymbolConfig instance. If None, will attempt to load.
        """
        self.project_root = project_root
        self._config = config

        # Try to load config if not provided
        if self._config is None:
            try:
                from config import get_config
                self._config = get_config()
            except Exception:
                pass  # Will use fallback paths

        # Build domain files mapping from config or use minimal defaults
        if self._config:
            self.DOMAIN_FILES = {}
            for domain in self._config.get_enabled_domains():
                try:
                    domain_file = self._config.get_domain_file(domain)
                    # Make relative to project root for compatibility
                    self.DOMAIN_FILES[domain] = str(domain_file.relative_to(self.project_root))
                except Exception:
                    pass
            # Add test files
            for domain in self._config.get_enabled_domains():
                try:
                    test_file = self._config.get_test_file(domain)
                    if test_file:
                        self.DOMAIN_FILES[f"{domain}-tests"] = str(test_file.relative_to(self.project_root))
                except Exception:
                    pass
        else:
            # Minimal generic fallback - only basic domains
            print("Warning: Configuration not loaded, using minimal defaults", file=sys.stderr)
            print("  Run 'python init_symbols.py' to initialize the symbols system", file=sys.stderr)
            self.DOMAIN_FILES = {
                'api': 'ai/symbols-api.json',
                'ui': 'ai/symbols-ui.json',
            }

    def merge(
        self,
        domain: str,
        extracted_symbols: List[Dict[str, Any]],
        validate: bool = True,
        backup: bool = True
    ) -> Tuple[int, int, int]:
        """
        Merge extracted symbols into domain file.

        Args:
            domain: Target domain (ui, api, shared)
            extracted_symbols: List of extracted symbol dictionaries
            validate: Whether to validate merged symbols
            backup: Whether to create backup before writing

        Returns:
            Tuple of (added, updated, total) counts
        """
        # Get domain file path
        domain_file = self._get_domain_file(domain)

        # Load existing symbols
        existing_data = self._load_existing(domain_file)

        # Create backup if requested
        if backup and domain_file.exists():
            self._create_backup(domain_file)

        # Merge symbols
        added, updated = self._merge_symbols(existing_data, extracted_symbols)

        # Validate if requested
        if validate:
            self._validate_symbols(existing_data)

        # Update metadata
        self._update_metadata(existing_data)

        # Write updated file
        self._write_symbols(domain_file, existing_data)

        total = len(self._get_all_symbols(existing_data))

        return added, updated, total

    def _get_domain_file(self, domain: str) -> Path:
        """Get the path to the domain symbol file."""
        if domain not in self.DOMAIN_FILES:
            raise ValueError(
                f"Invalid domain: {domain}. "
                f"Valid domains: {', '.join(self.DOMAIN_FILES.keys())}"
            )

        return self.project_root / self.DOMAIN_FILES[domain]

    def _load_existing(self, domain_file: Path) -> Dict[str, Any]:
        """Load existing symbol file or create new structure."""
        if not domain_file.exists():
            print(f"Warning: Domain file does not exist, creating new: {domain_file}", file=sys.stderr)
            return {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "generatedAt": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "sourceDirectory": "",
                "totalFiles": 0,
                "totalSymbols": 0,
                "domains": {}
            }

        try:
            with open(domain_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {domain_file}: {e}", file=sys.stderr)
            sys.exit(1)

    def _create_backup(self, domain_file: Path) -> None:
        """Create a timestamped backup of the domain file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = domain_file.with_suffix(f'.backup_{timestamp}.json')

        shutil.copy2(domain_file, backup_file)
        print(f"Created backup: {backup_file}", file=sys.stderr)

    def _merge_symbols(
        self,
        existing_data: Dict[str, Any],
        extracted_symbols: List[Dict[str, Any]]
    ) -> Tuple[int, int]:
        """
        Merge extracted symbols into existing data structure.

        Returns:
            Tuple of (added_count, updated_count)
        """
        added = 0
        updated = 0

        # Build index of existing symbols by (path, name)
        existing_index = self._build_symbol_index(existing_data)

        # Group extracted symbols by file path
        symbols_by_path: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for symbol in extracted_symbols:
            symbols_by_path[symbol['path']].append(symbol)

        # Process each file
        for file_path, file_symbols in symbols_by_path.items():
            # Find or create the module entry
            module_entry = self._find_or_create_module(existing_data, file_path)

            for symbol in file_symbols:
                key = (file_path, symbol['name'])

                if key in existing_index:
                    # Update existing symbol
                    existing_symbol = existing_index[key]
                    if self._symbol_changed(existing_symbol, symbol):
                        self._update_symbol(existing_symbol, symbol)
                        updated += 1
                else:
                    # Add new symbol
                    module_entry['symbols'].append(symbol)
                    added += 1

        return added, updated

    def _build_symbol_index(
        self,
        existing_data: Dict[str, Any]
    ) -> Dict[Tuple[str, str], Dict[str, Any]]:
        """Build index of existing symbols by (path, name) for fast lookup."""
        index: Dict[Tuple[str, str], Dict[str, Any]] = {}

        domains = existing_data.get('domains', {})
        for domain_data in domains.values():
            modules = domain_data.get('modules', [])
            for module in modules:
                path = module.get('path', '')
                for symbol in module.get('symbols', []):
                    key = (path, symbol['name'])
                    index[key] = symbol

        return index

    def _find_or_create_module(
        self,
        existing_data: Dict[str, Any],
        file_path: str
    ) -> Dict[str, Any]:
        """Find existing module entry or create new one."""
        # Determine domain from path
        domain_name = self._determine_domain_from_path(file_path)

        # Ensure domain exists
        if 'domains' not in existing_data:
            existing_data['domains'] = {}

        if domain_name not in existing_data['domains']:
            existing_data['domains'][domain_name] = {
                'count': 0,
                'modules': []
            }

        domain = existing_data['domains'][domain_name]

        # Find existing module
        for module in domain['modules']:
            if module['path'] == file_path:
                return module

        # Create new module
        new_module = {
            'path': file_path,
            'symbols': []
        }
        domain['modules'].append(new_module)

        return new_module

    def _determine_domain_from_path(self, file_path: str) -> str:
        """Determine domain category from file path."""
        path_lower = file_path.lower()

        # API/Backend patterns
        if any(p in path_lower for p in ['api/', 'routes/', 'services/', 'repositories/']):
            return 'routes' if 'routes/' in path_lower or 'api/' in path_lower else 'services'

        # UI/Frontend patterns
        if any(p in path_lower for p in ['components/', 'hooks/', 'pages/', 'app/']):
            return 'components' if 'components/' in path_lower else 'ui'

        # Utilities
        if any(p in path_lower for p in ['utils/', 'helpers/', 'lib/']):
            return 'utils'

        # Types/Schemas
        if any(p in path_lower for p in ['types/', 'schemas/', 'interfaces/']):
            return 'types'

        # Default
        return 'other'

    def _symbol_changed(
        self,
        existing: Dict[str, Any],
        new: Dict[str, Any]
    ) -> bool:
        """Check if a symbol has changed."""
        # Compare key fields
        fields_to_compare = ['kind', 'line', 'signature', 'summary']

        for field in fields_to_compare:
            if existing.get(field) != new.get(field):
                return True

        return False

    def _update_symbol(
        self,
        existing: Dict[str, Any],
        new: Dict[str, Any]
    ) -> None:
        """Update existing symbol with new data."""
        # Update all fields from new symbol
        for key, value in new.items():
            existing[key] = value

    def _get_all_symbols(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all symbols from data structure."""
        symbols = []
        domains = data.get('domains', {})

        for domain_data in domains.values():
            modules = domain_data.get('modules', [])
            for module in modules:
                symbols.extend(module.get('symbols', []))

        return symbols

    def _validate_symbols(self, data: Dict[str, Any]) -> None:
        """Validate symbol data for consistency and duplicates."""
        # Check for duplicates
        seen: Set[Tuple[str, str]] = set()
        duplicates: List[Tuple[str, str]] = []

        domains = data.get('domains', {})
        for domain_data in domains.values():
            modules = domain_data.get('modules', [])
            for module in modules:
                path = module.get('path', '')
                for symbol in module.get('symbols', []):
                    key = (path, symbol['name'])
                    if key in seen:
                        duplicates.append(key)
                    seen.add(key)

        if duplicates:
            print("Warning: Found duplicate symbols:", file=sys.stderr)
            for path, name in duplicates[:10]:  # Show first 10
                print(f"  - {name} in {path}", file=sys.stderr)

        # Validate required fields
        required_fields = ['name', 'kind', 'path', 'line']
        invalid_symbols = []

        for symbol in self._get_all_symbols(data):
            missing = [f for f in required_fields if f not in symbol]
            if missing:
                invalid_symbols.append((symbol.get('name', 'unknown'), missing))

        if invalid_symbols:
            print("Warning: Found symbols with missing fields:", file=sys.stderr)
            for name, missing in invalid_symbols[:10]:
                print(f"  - {name}: missing {missing}", file=sys.stderr)

    def _update_metadata(self, data: Dict[str, Any]) -> None:
        """Update metadata fields in symbol data."""
        data['generatedAt'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        # Count total symbols
        total_symbols = len(self._get_all_symbols(data))
        data['totalSymbols'] = total_symbols

        # Count files
        total_files = 0
        domains = data.get('domains', {})
        for domain_data in domains.values():
            modules = domain_data.get('modules', [])
            total_files += len(modules)
            # Update domain count
            domain_symbols = sum(
                len(m.get('symbols', []))
                for m in modules
            )
            domain_data['count'] = domain_symbols

        data['totalFiles'] = total_files

    def _write_symbols(self, domain_file: Path, data: Dict[str, Any]) -> None:
        """Write symbols to domain file."""
        # Ensure directory exists
        domain_file.parent.mkdir(parents=True, exist_ok=True)

        with open(domain_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Updated {domain_file}", file=sys.stderr)


def load_extracted_symbols(input_file: Path) -> List[Dict[str, Any]]:
    """Load extracted symbols from JSON file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'symbols' not in data:
            print(f"Error: Input file missing 'symbols' key", file=sys.stderr)
            sys.exit(1)

        return data['symbols']

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)


def find_project_root() -> Path:
    """Find the project root directory (contains ai/ directory)."""
    current = Path.cwd()

    # Search up to 5 levels
    for _ in range(5):
        if (current / 'ai').exists():
            return current
        current = current.parent

    print("Error: Could not find project root (no ai/ directory found)", file=sys.stderr)
    sys.exit(1)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Merge extracted symbols into existing symbol graphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--domain',
        required=True,
        choices=['ui', 'api', 'shared', 'ui-tests', 'api-tests', 'shared-tests'],
        help='Target domain for symbol merge'
    )
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        help='Input JSON file with extracted symbols'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate symbols after merge'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup before writing'
    )
    parser.add_argument(
        '--project-root',
        help='Project root directory (default: auto-detect)'
    )

    args = parser.parse_args()

    # Determine project root
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = find_project_root()

    print(f"Project root: {project_root}", file=sys.stderr)

    # Load extracted symbols
    input_file = Path(args.input)
    extracted_symbols = load_extracted_symbols(input_file)

    print(f"Loaded {len(extracted_symbols)} extracted symbols from {input_file}", file=sys.stderr)

    # Merge symbols
    merger = SymbolMerger(project_root)

    try:
        added, updated, total = merger.merge(
            domain=args.domain,
            extracted_symbols=extracted_symbols,
            validate=args.validate,
            backup=args.backup
        )

        # Print summary
        print("\nMerge Summary:", file=sys.stderr)
        print(f"  Added: {added}", file=sys.stderr)
        print(f"  Updated: {updated}", file=sys.stderr)
        print(f"  Total symbols: {total}", file=sys.stderr)
        print(f"  Domain: {args.domain}", file=sys.stderr)

        # Output JSON result for programmatic use
        result = {
            "success": True,
            "domain": args.domain,
            "added": added,
            "updated": updated,
            "total": total
        }
        print(json.dumps(result))

    except Exception as e:
        print(f"Error during merge: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
