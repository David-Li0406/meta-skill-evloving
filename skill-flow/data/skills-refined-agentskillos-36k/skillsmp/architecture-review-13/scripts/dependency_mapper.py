#!/usr/bin/env python3
"""
Dependency Mapper for Architecture Review

Maps internal import/export relationships including:
- ES6 imports/exports and CommonJS require()
- TypeScript path aliases (@/, ~/)
- Import graph construction
- Circular dependency detection
- Export usage tracking
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple

# Directories to skip
SKIP_DIRS: Set[str] = {
    'node_modules', '.git', 'build', 'dist', '.next', 'venv',
    '__pycache__', 'coverage', '.turbo', '.vercel', '.expo',
    'android', 'ios', '.architecture-review'
}

MAX_FILE_SIZE_BYTES = 512 * 1024
MAX_FILES_TO_PROCESS = 500

# Import patterns
IMPORT_PATTERNS = [
    # ES6 named imports: import { foo, bar } from 'module'
    r'import\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]',
    # ES6 default import: import foo from 'module'
    r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
    # ES6 namespace import: import * as foo from 'module'
    r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
    # ES6 side-effect import: import 'module'
    r'import\s+[\'"]([^\'"]+)[\'"]',
    # Dynamic import: import('module')
    r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
    # CommonJS require: require('module')
    r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
]

# Export patterns
EXPORT_PATTERNS = [
    # Named export: export { foo, bar }
    r'export\s+\{([^}]+)\}',
    # Named export declaration: export const/let/var/function/class foo
    r'export\s+(?:const|let|var|function|class|async\s+function)\s+(\w+)',
    # Default export: export default
    r'export\s+default\s+(?:function\s+)?(\w+)?',
    # Re-export: export { foo } from 'module'
    r'export\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]',
    # Re-export all: export * from 'module'
    r'export\s+\*\s+from\s+[\'"]([^\'"]+)[\'"]',
]


def read_file_safe(file_path: Path) -> Optional[str]:
    """Read file with size limit."""
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return None
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def load_path_aliases(root_path: Path) -> Dict[str, str]:
    """Load TypeScript/JavaScript path aliases from config files."""
    aliases = {}

    # Check tsconfig.json
    tsconfig_path = root_path / 'tsconfig.json'
    if tsconfig_path.exists():
        try:
            content = read_file_safe(tsconfig_path)
            if content:
                # Remove comments (simple approach)
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                config = json.loads(content)
                paths = config.get('compilerOptions', {}).get('paths', {})
                base_url = config.get('compilerOptions', {}).get('baseUrl', '.')

                for alias, targets in paths.items():
                    if targets and isinstance(targets, list):
                        # Remove trailing /* from alias
                        clean_alias = alias.rstrip('*').rstrip('/')
                        target = targets[0].rstrip('*').rstrip('/')
                        aliases[clean_alias] = os.path.join(base_url, target)
        except Exception:
            pass

    # Common default aliases
    if '@' not in aliases and '@/' not in aliases:
        if (root_path / 'src').is_dir():
            aliases['@'] = 'src'
            aliases['@/'] = 'src/'
        else:
            aliases['@'] = '.'
            aliases['@/'] = './'

    if '~' not in aliases and '~/' not in aliases:
        aliases['~'] = 'src' if (root_path / 'src').is_dir() else '.'
        aliases['~/'] = aliases['~'] + '/'

    return aliases


def resolve_import_path(
    import_path: str,
    current_file: Path,
    root_path: Path,
    aliases: Dict[str, str]
) -> Optional[str]:
    """Resolve an import path to an actual file path."""
    # Skip external packages
    if not import_path.startswith('.') and not any(import_path.startswith(a) for a in aliases):
        return None

    # Resolve aliases
    resolved = import_path
    for alias, target in sorted(aliases.items(), key=lambda x: -len(x[0])):
        if import_path.startswith(alias):
            resolved = import_path.replace(alias, target, 1)
            break

    # Handle relative imports
    if resolved.startswith('.'):
        base_dir = current_file.parent
        resolved_path = (base_dir / resolved).resolve()
    else:
        resolved_path = (root_path / resolved).resolve()

    # Try different extensions
    extensions = ['', '.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js', '/index.jsx']
    for ext in extensions:
        test_path = Path(str(resolved_path) + ext)
        if test_path.is_file():
            try:
                return str(test_path.relative_to(root_path))
            except ValueError:
                return None

    return None


def extract_imports(content: str) -> List[Tuple[str, List[str]]]:
    """Extract all imports from file content."""
    imports = []

    # Named imports: import { foo, bar } from 'module'
    for match in re.finditer(r'import\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]', content):
        names = [n.strip().split(' as ')[0].strip() for n in match.group(1).split(',')]
        imports.append((match.group(2), [n for n in names if n]))

    # Default import: import foo from 'module'
    for match in re.finditer(r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', content):
        if match.group(1) not in ['type', 'typeof']:
            imports.append((match.group(2), ['default']))

    # Namespace import: import * as foo from 'module'
    for match in re.finditer(r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', content):
        imports.append((match.group(2), ['*']))

    # Side-effect import: import 'module'
    for match in re.finditer(r"^import\s+['\"]([^'\"]+)['\"];?\s*$", content, re.MULTILINE):
        imports.append((match.group(1), []))

    # Dynamic import
    for match in re.finditer(r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', content):
        imports.append((match.group(1), ['dynamic']))

    # CommonJS require
    for match in re.finditer(r'(?:const|let|var)\s+(?:\{([^}]+)\}|(\w+))\s*=\s*require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', content):
        if match.group(1):  # Destructured
            names = [n.strip().split(':')[0].strip() for n in match.group(1).split(',')]
            imports.append((match.group(3), [n for n in names if n]))
        elif match.group(2):  # Single
            imports.append((match.group(3), [match.group(2)]))

    return imports


def extract_exports(content: str) -> List[str]:
    """Extract all exports from file content."""
    exports = []

    # Named export declarations
    for match in re.finditer(r'export\s+(?:const|let|var|function|class|async\s+function)\s+(\w+)', content):
        exports.append(match.group(1))

    # Named export list
    for match in re.finditer(r'export\s+\{([^}]+)\}(?!\s+from)', content):
        names = [n.strip().split(' as ')[-1].strip() for n in match.group(1).split(',')]
        exports.extend([n for n in names if n])

    # Default export with name
    for match in re.finditer(r'export\s+default\s+(?:function|class)\s+(\w+)', content):
        exports.append('default')
        exports.append(match.group(1))

    # Default export anonymous
    if re.search(r'export\s+default\s+(?!function|class|\w+\s*;)', content):
        exports.append('default')

    # Simple default export
    if re.search(r'export\s+default\s+\w+\s*;', content):
        exports.append('default')

    return list(set(exports))


def find_circular_dependencies(import_graph: Dict[str, List[str]]) -> List[List[str]]:
    """Detect circular dependencies using DFS."""
    cycles = []
    visited = set()
    rec_stack = set()

    def dfs(node: str, path: List[str]):
        if node in rec_stack:
            # Found cycle
            cycle_start = path.index(node)
            cycle = path[cycle_start:] + [node]
            cycles.append(cycle)
            return

        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in import_graph.get(node, []):
            dfs(neighbor, path)

        path.pop()
        rec_stack.remove(node)

    for node in import_graph:
        if node not in visited:
            dfs(node, [])

    # Deduplicate cycles (same cycle can be found starting from different nodes)
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        normalized = tuple(sorted(cycle[:-1]))
        if normalized not in seen:
            seen.add(normalized)
            unique_cycles.append(cycle)

    return unique_cycles[:20]  # Limit to 20 cycles


def analyze_dependencies(root_dir: str) -> Dict[str, Any]:
    """Main analysis function."""
    root_path = Path(root_dir).resolve()

    if not root_path.is_dir():
        return {'error': f'Directory not found: {root_dir}'}

    # Load path aliases
    aliases = load_path_aliases(root_path)

    modules: Dict[str, Dict[str, Any]] = {}
    import_graph: Dict[str, List[str]] = defaultdict(list)
    export_usage: Dict[str, List[str]] = defaultdict(list)
    external_packages: Dict[str, int] = defaultdict(int)

    files_processed = 0

    # Walk directory
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        for filename in filenames:
            if not filename.endswith(('.ts', '.tsx', '.js', '.jsx')):
                continue

            if files_processed >= MAX_FILES_TO_PROCESS:
                break

            file_path = Path(dirpath) / filename
            rel_path = str(file_path.relative_to(root_path))

            content = read_file_safe(file_path)
            if not content:
                continue

            files_processed += 1

            # Extract imports and exports
            file_imports = extract_imports(content)
            file_exports = extract_exports(content)

            module_info = {
                'imports': [],
                'exports': file_exports,
                'import_count': 0,
                'export_count': len(file_exports)
            }

            for import_path, imported_names in file_imports:
                # Check if internal or external
                resolved = resolve_import_path(import_path, file_path, root_path, aliases)

                if resolved:
                    # Internal import
                    module_info['imports'].append({
                        'from': resolved,
                        'names': imported_names
                    })
                    import_graph[rel_path].append(resolved)

                    # Track export usage
                    for name in imported_names:
                        if name and name not in ['*', 'dynamic']:
                            key = f"{resolved}::{name}"
                            export_usage[key].append(rel_path)
                else:
                    # External package
                    pkg_name = import_path.split('/')[0]
                    if pkg_name.startswith('@'):
                        pkg_name = '/'.join(import_path.split('/')[:2])
                    external_packages[pkg_name] += 1

            module_info['import_count'] = len(module_info['imports'])
            modules[rel_path] = module_info

        if files_processed >= MAX_FILES_TO_PROCESS:
            break

    # Find circular dependencies
    circular_deps = find_circular_dependencies(dict(import_graph))

    # Find unused exports
    unused_exports = []
    for module_path, info in modules.items():
        for export_name in info['exports']:
            key = f"{module_path}::{export_name}"
            if not export_usage[key]:
                # Check if it's likely an entry point
                if export_name != 'default' or 'page' not in module_path.lower():
                    unused_exports.append({
                        'file': module_path,
                        'export': export_name
                    })

    # Sort external packages by usage
    sorted_external = sorted(
        [{'name': k, 'import_count': v} for k, v in external_packages.items()],
        key=lambda x: -x['import_count']
    )

    return {
        'root': root_path.name,
        'files_analyzed': files_processed,
        'modules': modules,
        'import_graph': dict(import_graph),
        'export_usage': {k: v for k, v in export_usage.items() if v},
        'circular_dependencies': circular_deps,
        'external_packages': sorted_external[:50],
        'unused_exports': unused_exports[:100],
        'path_aliases': aliases,
        'summary': {
            'total_modules': len(modules),
            'total_internal_imports': sum(m['import_count'] for m in modules.values()),
            'total_exports': sum(m['export_count'] for m in modules.values()),
            'circular_dependency_count': len(circular_deps),
            'unused_export_count': len(unused_exports),
            'external_package_count': len(external_packages)
        }
    }


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = analyze_dependencies(root_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
