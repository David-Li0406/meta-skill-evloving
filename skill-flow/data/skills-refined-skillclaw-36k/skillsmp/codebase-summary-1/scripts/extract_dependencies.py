#!/usr/bin/env python3
"""
Extract dependencies from various package manager files.
Supports: package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod, etc.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None


def parse_package_json(path: Path) -> dict:
    """Parse Node.js package.json."""
    data = json.loads(path.read_text())
    return {
        'type': 'Node.js',
        'file': str(path),
        'name': data.get('name', 'unknown'),
        'version': data.get('version', 'unknown'),
        'dependencies': data.get('dependencies', {}),
        'dev_dependencies': data.get('devDependencies', {}),
        'peer_dependencies': data.get('peerDependencies', {}),
    }


def parse_requirements_txt(path: Path) -> dict:
    """Parse Python requirements.txt."""
    deps = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue
        # Handle various formats: pkg, pkg==1.0, pkg>=1.0, pkg[extra]
        match = re.match(r'^([a-zA-Z0-9_-]+)(?:\[.*\])?(?:[=<>!~]+(.*))?', line)
        if match:
            deps[match.group(1)] = match.group(2) or '*'
    return {
        'type': 'Python',
        'file': str(path),
        'dependencies': deps,
    }


def parse_pyproject_toml(path: Path) -> dict:
    """Parse Python pyproject.toml."""
    if tomllib is None:
        # Fallback: basic regex parsing
        content = path.read_text()
        deps = {}
        in_deps = False
        for line in content.splitlines():
            if 'dependencies' in line and '=' in line:
                in_deps = True
                continue
            if in_deps:
                if line.startswith('[') or (line.strip() and not line.startswith(' ') and not line.startswith('"')):
                    in_deps = False
                    continue
                match = re.search(r'"([^"]+)"', line)
                if match:
                    dep = match.group(1)
                    name = re.match(r'^([a-zA-Z0-9_-]+)', dep)
                    if name:
                        deps[name.group(1)] = dep
        return {
            'type': 'Python',
            'file': str(path),
            'dependencies': deps,
        }

    data = tomllib.loads(path.read_text())
    project = data.get('project', {})
    deps = {}

    for dep in project.get('dependencies', []):
        match = re.match(r'^([a-zA-Z0-9_-]+)', dep)
        if match:
            deps[match.group(1)] = dep

    optional_deps = {}
    for group, group_deps in project.get('optional-dependencies', {}).items():
        for dep in group_deps:
            match = re.match(r'^([a-zA-Z0-9_-]+)', dep)
            if match:
                optional_deps[match.group(1)] = dep

    return {
        'type': 'Python',
        'file': str(path),
        'name': project.get('name', 'unknown'),
        'version': project.get('version', 'unknown'),
        'dependencies': deps,
        'optional_dependencies': optional_deps,
    }


def parse_cargo_toml(path: Path) -> dict:
    """Parse Rust Cargo.toml."""
    content = path.read_text()
    deps = {}
    dev_deps = {}

    current_section = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('['):
            if 'dependencies' in line.lower():
                if 'dev' in line.lower():
                    current_section = 'dev'
                else:
                    current_section = 'main'
            else:
                current_section = None
            continue

        if current_section and '=' in line:
            parts = line.split('=', 1)
            name = parts[0].strip()
            version = parts[1].strip().strip('"\'')
            if current_section == 'dev':
                dev_deps[name] = version
            else:
                deps[name] = version

    # Extract package info
    name = 'unknown'
    version = 'unknown'
    for line in content.splitlines():
        if line.startswith('name'):
            match = re.search(r'"([^"]+)"', line)
            if match:
                name = match.group(1)
        elif line.startswith('version'):
            match = re.search(r'"([^"]+)"', line)
            if match:
                version = match.group(1)

    return {
        'type': 'Rust',
        'file': str(path),
        'name': name,
        'version': version,
        'dependencies': deps,
        'dev_dependencies': dev_deps,
    }


def parse_go_mod(path: Path) -> dict:
    """Parse Go go.mod."""
    content = path.read_text()
    deps = {}

    in_require = False
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('require ('):
            in_require = True
            continue
        if line == ')':
            in_require = False
            continue
        if in_require or line.startswith('require '):
            line = line.replace('require ', '')
            parts = line.split()
            if len(parts) >= 2:
                deps[parts[0]] = parts[1]

    # Get module name
    name = 'unknown'
    for line in content.splitlines():
        if line.startswith('module '):
            name = line.replace('module ', '').strip()
            break

    return {
        'type': 'Go',
        'file': str(path),
        'name': name,
        'dependencies': deps,
    }


def parse_gemfile(path: Path) -> dict:
    """Parse Ruby Gemfile."""
    deps = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith('gem '):
            match = re.search(r"gem ['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]+)['\"])?", line)
            if match:
                deps[match.group(1)] = match.group(2) or '*'
    return {
        'type': 'Ruby',
        'file': str(path),
        'dependencies': deps,
    }


PARSERS = {
    'package.json': parse_package_json,
    'requirements.txt': parse_requirements_txt,
    'pyproject.toml': parse_pyproject_toml,
    'Cargo.toml': parse_cargo_toml,
    'go.mod': parse_go_mod,
    'Gemfile': parse_gemfile,
}


def find_dependency_files(root: Path) -> list:
    """Find all dependency files in a directory."""
    found = []
    for name in PARSERS.keys():
        for path in root.rglob(name):
            # Skip common non-project directories
            skip = False
            for part in path.parts:
                if part in {'node_modules', '.git', 'vendor', 'venv', '.venv'}:
                    skip = True
                    break
            if not skip:
                found.append(path)
    return found


def main():
    parser = argparse.ArgumentParser(
        description='Extract dependencies from package files'
    )
    parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f'Error: Path does not exist: {root}', file=sys.stderr)
        sys.exit(1)

    dep_files = find_dependency_files(root)
    results = []

    for dep_file in dep_files:
        parser_func = PARSERS.get(dep_file.name)
        if parser_func:
            try:
                result = parser_func(dep_file)
                result['file'] = str(dep_file.relative_to(root))
                results.append(result)
            except Exception as e:
                results.append({
                    'file': str(dep_file.relative_to(root)),
                    'error': str(e)
                })

    if args.json:
        output = json.dumps(results, indent=2)
    else:
        lines = ['# Dependencies Report\n']
        for result in results:
            if 'error' in result:
                lines.append(f"## {result['file']} (Error: {result['error']})\n")
                continue

            lines.append(f"## {result.get('type', 'Unknown')} - {result['file']}\n")
            if 'name' in result:
                lines.append(f"**Package:** {result['name']} v{result.get('version', 'unknown')}\n")

            if result.get('dependencies'):
                lines.append('\n### Dependencies\n')
                for name, version in sorted(result['dependencies'].items()):
                    lines.append(f'- {name}: {version}')
                lines.append('')

            if result.get('dev_dependencies'):
                lines.append('\n### Dev Dependencies\n')
                for name, version in sorted(result['dev_dependencies'].items()):
                    lines.append(f'- {name}: {version}')
                lines.append('')

            if result.get('optional_dependencies'):
                lines.append('\n### Optional Dependencies\n')
                for name, version in sorted(result['optional_dependencies'].items()):
                    lines.append(f'- {name}: {version}')
                lines.append('')

            if result.get('peer_dependencies'):
                lines.append('\n### Peer Dependencies\n')
                for name, version in sorted(result['peer_dependencies'].items()):
                    lines.append(f'- {name}: {version}')
                lines.append('')

        output = '\n'.join(lines)

    if args.output:
        Path(args.output).write_text(output)
        print(f'Output written to {args.output}')
    else:
        print(output)


if __name__ == '__main__':
    main()
