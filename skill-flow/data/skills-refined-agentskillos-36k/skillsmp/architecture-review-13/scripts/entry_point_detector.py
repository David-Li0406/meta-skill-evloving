#!/usr/bin/env python3
"""
Entry Point Detector for Architecture Review

Detects application entry points including:
- Main files and app entry points
- Framework-specific patterns (Next.js, Express, etc.)
- npm scripts from package.json
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

# Directories to skip
SKIP_DIRS: Set[str] = {
    'node_modules', '.git', 'build', 'dist', '.next', 'venv',
    '__pycache__', 'coverage', '.turbo', '.vercel', '.expo',
    'android', 'ios', '.architecture-review'
}

MAX_FILE_SIZE_BYTES = 512 * 1024

# Framework detection patterns
FRAMEWORK_PATTERNS = {
    'next.js': {
        'files': ['next.config.js', 'next.config.mjs', 'next.config.ts'],
        'dirs': ['pages', 'app'],
        'dependencies': ['next']
    },
    'express': {
        'patterns': [r'express\(\)', r'require\([\'"]express[\'"]\)', r'from\s+[\'"]express[\'"]'],
        'dependencies': ['express']
    },
    'fastify': {
        'patterns': [r'fastify\(\)', r'require\([\'"]fastify[\'"]\)', r'from\s+[\'"]fastify[\'"]'],
        'dependencies': ['fastify']
    },
    'hono': {
        'patterns': [r'new\s+Hono\(\)', r'from\s+[\'"]hono[\'"]'],
        'dependencies': ['hono']
    },
    'nest.js': {
        'files': ['nest-cli.json'],
        'patterns': [r'@nestjs/core', r'NestFactory'],
        'dependencies': ['@nestjs/core']
    },
    'react-native': {
        'files': ['app.json', 'metro.config.js'],
        'dependencies': ['react-native', 'expo']
    },
    'expo': {
        'files': ['app.json', 'expo.json'],
        'dirs': ['app'],
        'dependencies': ['expo']
    },
    'vite': {
        'files': ['vite.config.js', 'vite.config.ts'],
        'dependencies': ['vite']
    },
    'remix': {
        'files': ['remix.config.js'],
        'dependencies': ['@remix-run/react']
    },
    'astro': {
        'files': ['astro.config.mjs', 'astro.config.ts'],
        'dependencies': ['astro']
    }
}

# Entry point patterns by type
ENTRY_POINT_PATTERNS = {
    'main': {
        'files': ['index.ts', 'index.js', 'main.ts', 'main.js', 'app.ts', 'app.js', 'server.ts', 'server.js'],
        'patterns': [r'app\.listen\(', r'server\.listen\(', r'createServer\(']
    },
    'next_page': {
        'paths': ['/pages/', '/app/'],
        'files': ['page.tsx', 'page.ts', 'page.jsx', 'page.js']
    },
    'api_route': {
        'paths': ['/api/', '/routes/'],
        'patterns': [r'export\s+(default\s+)?(async\s+)?function\s+(GET|POST|PUT|DELETE|PATCH)']
    },
    'handler': {
        'patterns': [
            r'export\s+(const|function)\s+handler',
            r'exports\.handler\s*=',
            r'module\.exports\s*=\s*async'
        ]
    }
}


def read_file_safe(file_path: Path) -> Optional[str]:
    """Read file with size limit."""
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return None
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def parse_package_json(root_path: Path) -> Dict[str, Any]:
    """Parse package.json for scripts and dependencies."""
    pkg_path = root_path / 'package.json'
    result = {'scripts': [], 'dependencies': [], 'dev_dependencies': []}

    if not pkg_path.exists():
        return result

    try:
        content = read_file_safe(pkg_path)
        if not content:
            return result

        pkg = json.loads(content)

        # Extract scripts
        scripts = pkg.get('scripts', {})
        for name, command in scripts.items():
            result['scripts'].append({
                'name': name,
                'command': command
            })

        # Extract dependencies
        result['dependencies'] = list(pkg.get('dependencies', {}).keys())
        result['dev_dependencies'] = list(pkg.get('devDependencies', {}).keys())

    except Exception:
        pass

    return result


def detect_framework(root_path: Path, pkg_info: Dict[str, Any]) -> Optional[str]:
    """Detect the primary framework used in the project."""
    all_deps = set(pkg_info['dependencies'] + pkg_info['dev_dependencies'])

    for framework, patterns in FRAMEWORK_PATTERNS.items():
        # Check dependencies first (most reliable)
        if 'dependencies' in patterns:
            for dep in patterns['dependencies']:
                if dep in all_deps:
                    return framework

        # Check for specific files
        if 'files' in patterns:
            for filename in patterns['files']:
                if (root_path / filename).exists():
                    return framework

        # Check for specific directories
        if 'dirs' in patterns:
            for dirname in patterns['dirs']:
                if (root_path / dirname).is_dir():
                    return framework

    return None


def find_entry_points(root_path: Path, framework: Optional[str]) -> List[Dict[str, Any]]:
    """Find all entry points in the project."""
    entry_points = []
    seen_paths = set()

    # Check root level entry points
    for entry_type, config in ENTRY_POINT_PATTERNS.items():
        if 'files' in config:
            for filename in config['files']:
                # Check root directory
                file_path = root_path / filename
                if file_path.exists():
                    rel_path = filename
                    if rel_path not in seen_paths:
                        seen_paths.add(rel_path)
                        entry_points.append({
                            'file': rel_path,
                            'type': entry_type,
                            'confidence': 'high',
                            'evidence': f'Standard entry point file: {filename}'
                        })

                # Check src directory
                src_file = root_path / 'src' / filename
                if src_file.exists():
                    rel_path = f'src/{filename}'
                    if rel_path not in seen_paths:
                        seen_paths.add(rel_path)
                        entry_points.append({
                            'file': rel_path,
                            'type': entry_type,
                            'confidence': 'high',
                            'evidence': f'Standard entry point file: src/{filename}'
                        })

    # Walk directory for pattern-based detection
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        for filename in filenames:
            if not filename.endswith(('.ts', '.tsx', '.js', '.jsx')):
                continue

            file_path = Path(dirpath) / filename
            rel_path = os.path.relpath(file_path, root_path)

            if rel_path in seen_paths:
                continue

            content = read_file_safe(file_path)
            if not content:
                continue

            # Check Next.js pages/app directory
            if framework == 'next.js':
                if '/pages/' in rel_path or rel_path.startswith('pages/'):
                    if not rel_path.startswith('pages/api/') and '/api/' not in rel_path:
                        if filename not in ['_app.tsx', '_app.js', '_document.tsx', '_document.js']:
                            seen_paths.add(rel_path)
                            entry_points.append({
                                'file': rel_path,
                                'type': 'next_page',
                                'confidence': 'high',
                                'evidence': 'Next.js pages directory'
                            })
                            continue

                if '/app/' in rel_path or rel_path.startswith('app/'):
                    if filename in ['page.tsx', 'page.ts', 'page.jsx', 'page.js']:
                        seen_paths.add(rel_path)
                        entry_points.append({
                            'file': rel_path,
                            'type': 'next_page',
                            'confidence': 'high',
                            'evidence': 'Next.js App Router page'
                        })
                        continue

            # Check API routes
            if '/api/' in rel_path or '/routes/' in rel_path:
                for pattern in ENTRY_POINT_PATTERNS['api_route'].get('patterns', []):
                    if re.search(pattern, content):
                        seen_paths.add(rel_path)
                        entry_points.append({
                            'file': rel_path,
                            'type': 'api_route',
                            'confidence': 'high',
                            'evidence': f'API route handler detected'
                        })
                        break

            # Check for server/handler patterns
            for entry_type in ['main', 'handler']:
                patterns = ENTRY_POINT_PATTERNS[entry_type].get('patterns', [])
                for pattern in patterns:
                    if re.search(pattern, content):
                        if rel_path not in seen_paths:
                            seen_paths.add(rel_path)
                            entry_points.append({
                                'file': rel_path,
                                'type': entry_type,
                                'confidence': 'medium',
                                'evidence': f'Pattern match: {pattern[:30]}...'
                            })
                        break

    return entry_points


def analyze_entry_points(root_dir: str) -> Dict[str, Any]:
    """Main analysis function."""
    root_path = Path(root_dir).resolve()

    if not root_path.is_dir():
        return {'error': f'Directory not found: {root_dir}'}

    # Parse package.json
    pkg_info = parse_package_json(root_path)

    # Detect framework
    framework = detect_framework(root_path, pkg_info)

    # Find entry points
    entry_points = find_entry_points(root_path, framework)

    # Sort by confidence and type
    entry_points.sort(key=lambda x: (
        0 if x['confidence'] == 'high' else 1,
        x['type'],
        x['file']
    ))

    return {
        'root': root_path.name,
        'framework': framework,
        'entry_points': entry_points,
        'scripts': pkg_info['scripts'],
        'summary': {
            'framework_detected': framework,
            'total_entry_points': len(entry_points),
            'by_type': {},
            'by_confidence': {'high': 0, 'medium': 0, 'low': 0}
        }
    }


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = analyze_entry_points(root_dir)

    # Calculate summary stats
    if 'entry_points' in result:
        for ep in result['entry_points']:
            ep_type = ep['type']
            conf = ep['confidence']
            result['summary']['by_type'][ep_type] = result['summary']['by_type'].get(ep_type, 0) + 1
            result['summary']['by_confidence'][conf] = result['summary']['by_confidence'].get(conf, 0) + 1

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
