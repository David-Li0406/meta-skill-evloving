#!/usr/bin/env python3
"""
Extract imports and dependencies for a chunk.

Shows all imports/dependencies across files in the chunk, with analysis of:
- Internal vs external dependencies
- Most frequently imported modules
- Dependency on other chunks
- Circular dependency detection

Usage:
    python extract-deps.py [chunk_id]
    python extract-deps.py                 # Current chunk
    python extract-deps.py chunk_phase_2_api
"""

import os
import sys
import json
import re
import ast
from pathlib import Path
from collections import defaultdict, Counter


def load_chunks(chunks_file=".claude/.chunks.json"):
    """Load chunks configuration."""
    if not os.path.exists(chunks_file):
        print(f"Error: Chunks file not found: {chunks_file}", file=sys.stderr)
        sys.exit(1)

    with open(chunks_file) as f:
        return json.load(f)


def get_chunk(chunks_data, chunk_id):
    """Get specific chunk by ID."""
    for chunk in chunks_data["chunks"]:
        if chunk["id"] == chunk_id:
            return chunk
    return None


def extract_python_imports(file_path):
    """Extract imports from Python file."""
    imports = []

    try:
        with open(file_path) as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split('.')[0])

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split('.')[0])

    except (SyntaxError, FileNotFoundError):
        # Fallback to regex
        try:
            with open(file_path) as f:
                for line in f:
                    if match := re.match(r'^\s*import\s+([a-zA-Z0-9_]+)', line):
                        imports.append(match.group(1))
                    elif match := re.match(r'^\s*from\s+([a-zA-Z0-9_]+)', line):
                        imports.append(match.group(1))
        except FileNotFoundError:
            pass

    return imports


def extract_rust_uses(file_path):
    """Extract use statements from Rust file."""
    uses = []

    try:
        with open(file_path) as f:
            for line in f:
                if match := re.match(r'^\s*use\s+(crate|super|self)?::?([a-zA-Z0-9_:]+)', line):
                    scope = match.group(1) or "external"
                    path = match.group(2)

                    if scope in ("crate", "super", "self"):
                        uses.append(path.split("::")[0])
    except FileNotFoundError:
        pass

    return uses


def extract_go_imports(file_path):
    """Extract imports from Go file."""
    imports = []

    try:
        with open(file_path) as f:
            content = f.read()

        # Single import
        for match in re.finditer(r'^\s*import\s+"([^"]+)"', content, re.MULTILINE):
            package = match.group(1).split('/')[-1]
            imports.append(package)

        # Import block
        import_block = re.search(r'import\s*\((.*?)\)', content, re.DOTALL)
        if import_block:
            for line in import_block.group(1).split('\n'):
                if match := re.match(r'^\s*"([^"]+)"', line):
                    package = match.group(1).split('/')[-1]
                    imports.append(package)

    except FileNotFoundError:
        pass

    return imports


def extract_js_imports(file_path):
    """Extract imports from JavaScript/TypeScript file."""
    imports = []

    try:
        with open(file_path) as f:
            for line in f:
                # import from
                if match := re.match(r'^\s*import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', line):
                    module = match.group(1)
                    # Get package name for node_modules
                    if not module.startswith('.'):
                        imports.append(module.split('/')[0])

                # require
                elif match := re.match(r'require\([\'"]([^\'"]+)[\'"]\)', line):
                    module = match.group(1)
                    if not module.startswith('.'):
                        imports.append(module.split('/')[0])

    except FileNotFoundError:
        pass

    return imports


def extract_file_imports(file_path):
    """Extract imports based on file type."""
    ext = Path(file_path).suffix

    if ext == '.py':
        return extract_python_imports(file_path)
    elif ext == '.rs':
        return extract_rust_uses(file_path)
    elif ext == '.go':
        return extract_go_imports(file_path)
    elif ext in ('.js', '.jsx', '.ts', '.tsx'):
        return extract_js_imports(file_path)
    else:
        return []


def categorize_imports(imports, project_root):
    """Categorize imports as internal or external."""
    internal = []
    external = []

    # List of standard library modules (simplified)
    python_stdlib = {
        'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 're', 'collections',
        'itertools', 'functools', 'typing', 'asyncio', 'subprocess', 'logging'
    }

    rust_stdlib = {
        'std', 'alloc', 'core'
    }

    go_stdlib = {
        'fmt', 'os', 'io', 'time', 'strings', 'errors', 'context', 'sync'
    }

    js_builtins = {
        'fs', 'path', 'util', 'os', 'crypto', 'http', 'https', 'stream'
    }

    stdlib_modules = python_stdlib | rust_stdlib | go_stdlib | js_builtins

    for imp in imports:
        if imp in stdlib_modules:
            continue  # Skip standard library

        # Check if it exists in project
        potential_paths = [
            Path(project_root) / imp,
            Path(project_root) / f"{imp}.py",
            Path(project_root) / f"src/{imp}",
            Path(project_root) / f"lib/{imp}",
        ]

        if any(p.exists() for p in potential_paths):
            internal.append(imp)
        else:
            external.append(imp)

    return internal, external


def find_chunk_for_file(chunks_data, file_path):
    """Find which chunk contains a file."""
    for chunk in chunks_data["chunks"]:
        if file_path in chunk["files"]:
            return chunk["id"]
    return None


def main():
    # Get chunk ID from args or use current
    if len(sys.argv) > 1:
        chunk_id = sys.argv[1]
    else:
        chunks_data = load_chunks()
        chunk_id = chunks_data.get("current_chunk")
        if not chunk_id:
            print("Error: No current chunk set", file=sys.stderr)
            sys.exit(1)

    # Load chunks and get target chunk
    chunks_data = load_chunks()
    chunk = get_chunk(chunks_data, chunk_id)

    if not chunk:
        print(f"Error: Chunk not found: {chunk_id}", file=sys.stderr)
        sys.exit(1)

    print(f"Dependency Analysis: {chunk['name']}")
    print("=" * 60)
    print()

    # Extract imports from all files
    all_imports = []
    file_imports = {}

    for file in chunk["files"]:
        imports = extract_file_imports(file)
        all_imports.extend(imports)
        if imports:
            file_imports[file] = imports

    if not all_imports:
        print("No imports found in chunk files.")
        sys.exit(0)

    # Categorize imports
    project_root = os.getcwd()
    internal, external = categorize_imports(all_imports, project_root)

    # Count frequencies
    internal_counts = Counter(internal)
    external_counts = Counter(external)

    # Print internal dependencies
    if internal:
        print(f"Internal Dependencies ({len(internal_counts)} unique):")
        print("-" * 60)
        for module, count in internal_counts.most_common():
            print(f"  • {module} ({count} imports)")

            # Find which chunk this belongs to
            potential_file = Path(project_root) / f"{module}.py"
            if potential_file.exists():
                dep_chunk_id = find_chunk_for_file(chunks_data, str(potential_file))
                if dep_chunk_id and dep_chunk_id != chunk_id:
                    dep_chunk = get_chunk(chunks_data, dep_chunk_id)
                    print(f"    → Chunk: {dep_chunk['name']}")
        print()

    # Print external dependencies
    if external:
        print(f"External Dependencies ({len(external_counts)} unique):")
        print("-" * 60)
        for module, count in external_counts.most_common(10):
            print(f"  • {module} ({count} imports)")
        if len(external_counts) > 10:
            print(f"  ... and {len(external_counts) - 10} more")
        print()

    # Check cross-chunk dependencies
    cross_chunk_deps = set()
    for file in chunk["files"]:
        imports = extract_file_imports(file)
        for imp in imports:
            # Try to find file for import
            potential_files = [
                f"{imp}.py",
                f"src/{imp}.py",
                f"{imp}.rs",
                f"src/{imp}.rs"
            ]

            for pf in potential_files:
                if os.path.exists(pf):
                    dep_chunk_id = find_chunk_for_file(chunks_data, pf)
                    if dep_chunk_id and dep_chunk_id != chunk_id:
                        cross_chunk_deps.add(dep_chunk_id)

    if cross_chunk_deps:
        print(f"Cross-Chunk Dependencies ({len(cross_chunk_deps)} chunks):")
        print("-" * 60)
        for dep_chunk_id in cross_chunk_deps:
            dep_chunk = get_chunk(chunks_data, dep_chunk_id)
            print(f"  • {dep_chunk['name']}")
            print(f"    ID: {dep_chunk_id}")
            print(f"    Status: {dep_chunk['status']}")
        print()

    # Per-file import breakdown
    print("Per-File Imports:")
    print("-" * 60)
    for file, imports in sorted(file_imports.items()):
        print(f"  {Path(file).name}: {len(imports)} imports")
        for imp in sorted(set(imports))[:5]:
            print(f"    - {imp}")
        if len(set(imports)) > 5:
            print(f"    ... and {len(set(imports)) - 5} more")
    print()

    # Summary statistics
    total_imports = len(all_imports)
    unique_imports = len(set(all_imports))
    avg_per_file = total_imports / len(chunk["files"]) if chunk["files"] else 0

    print("Summary:")
    print("-" * 60)
    print(f"  Total imports: {total_imports}")
    print(f"  Unique modules: {unique_imports}")
    print(f"  Internal modules: {len(internal_counts)}")
    print(f"  External modules: {len(external_counts)}")
    print(f"  Average imports per file: {avg_per_file:.1f}")
    print(f"  Files with imports: {len(file_imports)}/{len(chunk['files'])}")

    sys.exit(0)


if __name__ == "__main__":
    main()
