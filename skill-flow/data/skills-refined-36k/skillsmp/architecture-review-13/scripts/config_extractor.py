#!/usr/bin/env python3
"""
Config Extractor for Architecture Review

Extracts configuration information including:
- Environment variables from code
- .env and .env.example files
- Client-exposed variables (NEXT_PUBLIC_, VITE_, etc.)
- Configuration files (next.config.js, tsconfig.json, etc.)
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

# Directories to skip
SKIP_DIRS: Set[str] = {
    'node_modules', '.git', 'build', 'dist', '.next', 'venv',
    '__pycache__', 'coverage', '.turbo', '.vercel', '.expo',
    'android', 'ios', '.architecture-review'
}

MAX_FILE_SIZE_BYTES = 512 * 1024
MAX_FILES_TO_PROCESS = 300

# Client-exposed env var prefixes (exposed to browser)
CLIENT_EXPOSED_PREFIXES = [
    'NEXT_PUBLIC_',
    'VITE_',
    'REACT_APP_',
    'EXPO_PUBLIC_',
    'NUXT_PUBLIC_',
]

# Config file patterns
CONFIG_FILES = {
    # Framework configs
    'next.config.js': 'next.js',
    'next.config.mjs': 'next.js',
    'next.config.ts': 'next.js',
    'vite.config.js': 'vite',
    'vite.config.ts': 'vite',
    'astro.config.mjs': 'astro',
    'remix.config.js': 'remix',
    'nuxt.config.js': 'nuxt',
    'nuxt.config.ts': 'nuxt',

    # Build tools
    'webpack.config.js': 'webpack',
    'rollup.config.js': 'rollup',
    'esbuild.config.js': 'esbuild',
    'turbo.json': 'turborepo',

    # TypeScript
    'tsconfig.json': 'typescript',
    'jsconfig.json': 'javascript',

    # Linting/Formatting
    '.eslintrc': 'eslint',
    '.eslintrc.js': 'eslint',
    '.eslintrc.json': 'eslint',
    'eslint.config.js': 'eslint',
    '.prettierrc': 'prettier',
    '.prettierrc.js': 'prettier',
    'prettier.config.js': 'prettier',

    # Testing
    'jest.config.js': 'jest',
    'jest.config.ts': 'jest',
    'vitest.config.ts': 'vitest',
    'playwright.config.ts': 'playwright',
    'cypress.config.js': 'cypress',

    # Package managers
    'package.json': 'npm',
    'pnpm-workspace.yaml': 'pnpm',
    '.npmrc': 'npm',
    '.nvmrc': 'nvm',

    # Docker/Deployment
    'Dockerfile': 'docker',
    'docker-compose.yml': 'docker',
    'docker-compose.yaml': 'docker',
    'vercel.json': 'vercel',
    'netlify.toml': 'netlify',
    'fly.toml': 'fly.io',

    # Database
    'prisma/schema.prisma': 'prisma',
    'drizzle.config.ts': 'drizzle',

    # Misc
    'tailwind.config.js': 'tailwind',
    'tailwind.config.ts': 'tailwind',
    'postcss.config.js': 'postcss',
    '.env': 'environment',
    '.env.local': 'environment',
    '.env.example': 'environment',
    '.env.development': 'environment',
    '.env.production': 'environment',
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


def extract_env_vars_from_code(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract environment variable references from code."""
    env_vars = []
    seen = set()

    # Patterns for env var access
    patterns = [
        # process.env.VAR_NAME
        r'process\.env\.([A-Z][A-Z0-9_]*)',
        # process.env['VAR_NAME'] or process.env["VAR_NAME"]
        r'process\.env\[[\'"]([A-Z][A-Z0-9_]*)[\'\"]\]',
        # import.meta.env.VAR_NAME (Vite)
        r'import\.meta\.env\.([A-Z][A-Z0-9_]*)',
        # Deno.env.get('VAR_NAME')
        r'Deno\.env\.get\s*\(\s*[\'"]([A-Z][A-Z0-9_]*)[\'\"]\s*\)',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content):
            var_name = match.group(1)
            if var_name not in seen:
                seen.add(var_name)
                env_vars.append({
                    'name': var_name,
                    'file': file_path,
                    'client_exposed': any(var_name.startswith(p) for p in CLIENT_EXPOSED_PREFIXES)
                })

    return env_vars


def parse_env_file(file_path: Path) -> List[Dict[str, Any]]:
    """Parse .env file and extract variable definitions."""
    variables = []

    content = read_file_safe(file_path)
    if not content:
        return variables

    for line in content.split('\n'):
        line = line.strip()

        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue

        # Parse KEY=value
        if '=' in line:
            key = line.split('=')[0].strip()
            # Skip if it looks like a comment or invalid
            if key and re.match(r'^[A-Z][A-Z0-9_]*$', key):
                has_value = len(line.split('=', 1)) > 1 and line.split('=', 1)[1].strip()
                variables.append({
                    'name': key,
                    'has_value': bool(has_value),
                    'client_exposed': any(key.startswith(p) for p in CLIENT_EXPOSED_PREFIXES)
                })

    return variables


def extract_config_keys(file_path: Path, config_type: str) -> List[str]:
    """Extract key configuration options from config files."""
    content = read_file_safe(file_path)
    if not content:
        return []

    keys = []

    if config_type == 'typescript':
        try:
            # Remove comments
            clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)
            config = json.loads(clean)

            if 'compilerOptions' in config:
                keys.extend([f"compilerOptions.{k}" for k in config['compilerOptions'].keys()])
            if 'paths' in config.get('compilerOptions', {}):
                keys.append('compilerOptions.paths (path aliases)')
            if 'include' in config:
                keys.append('include')
            if 'exclude' in config:
                keys.append('exclude')
        except Exception:
            pass

    elif config_type == 'npm':
        try:
            pkg = json.loads(content)
            if 'scripts' in pkg:
                keys.extend([f"scripts.{k}" for k in pkg['scripts'].keys()])
            if 'workspaces' in pkg:
                keys.append('workspaces (monorepo)')
            if 'type' in pkg:
                keys.append(f"type: {pkg['type']}")
        except Exception:
            pass

    elif config_type in ['next.js', 'vite', 'astro']:
        # Extract exported config keys
        export_match = re.search(r'(?:export\s+default|module\.exports\s*=)\s*\{([^}]+)\}', content)
        if export_match:
            # Simple key extraction
            key_pattern = r'(\w+)\s*:'
            keys = re.findall(key_pattern, export_match.group(1))

    return keys[:20]  # Limit keys


def find_config_files(root_path: Path) -> List[Dict[str, Any]]:
    """Find all configuration files in the project."""
    configs = []

    # Check root level first
    for filename, config_type in CONFIG_FILES.items():
        file_path = root_path / filename
        if file_path.exists():
            keys = extract_config_keys(file_path, config_type)
            configs.append({
                'file': filename,
                'type': config_type,
                'keys': keys
            })

    # Check for prisma schema
    prisma_path = root_path / 'prisma' / 'schema.prisma'
    if prisma_path.exists():
        configs.append({
            'file': 'prisma/schema.prisma',
            'type': 'prisma',
            'keys': ['database schema']
        })

    # Check src directory
    src_path = root_path / 'src'
    if src_path.is_dir():
        for filename, config_type in CONFIG_FILES.items():
            if filename.startswith('.'):
                continue
            file_path = src_path / filename
            if file_path.exists():
                configs.append({
                    'file': f'src/{filename}',
                    'type': config_type,
                    'keys': []
                })

    return configs


def analyze_config(root_dir: str) -> Dict[str, Any]:
    """Main analysis function."""
    root_path = Path(root_dir).resolve()

    if not root_path.is_dir():
        return {'error': f'Directory not found: {root_dir}'}

    result = {
        'root': root_path.name,
        'environment_variables': {
            'from_code': [],
            'from_env_files': {},
            'required': [],
            'client_exposed': [],
            'server_only': []
        },
        'config_files': [],
        'summary': {}
    }

    # Find config files
    result['config_files'] = find_config_files(root_path)

    # Parse .env files
    env_file_patterns = ['.env', '.env.local', '.env.example', '.env.development', '.env.production']
    for env_file in env_file_patterns:
        env_path = root_path / env_file
        if env_path.exists():
            vars_list = parse_env_file(env_path)
            result['environment_variables']['from_env_files'][env_file] = vars_list

    # Scan code for env var usage
    all_env_vars = defaultdict(list)
    files_processed = 0

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

            env_vars = extract_env_vars_from_code(content, rel_path)
            for var in env_vars:
                all_env_vars[var['name']].append(var['file'])

        if files_processed >= MAX_FILES_TO_PROCESS:
            break

    # Consolidate env var findings
    for var_name, used_in in all_env_vars.items():
        is_client_exposed = any(var_name.startswith(p) for p in CLIENT_EXPOSED_PREFIXES)

        var_info = {
            'name': var_name,
            'used_in': used_in[:5],  # Limit files shown
            'usage_count': len(used_in),
            'client_exposed': is_client_exposed
        }

        result['environment_variables']['from_code'].append(var_info)

        if is_client_exposed:
            result['environment_variables']['client_exposed'].append(var_name)
        else:
            result['environment_variables']['server_only'].append(var_name)

    # Determine required vars (in code but not in .env.example)
    example_vars = set()
    if '.env.example' in result['environment_variables']['from_env_files']:
        example_vars = {v['name'] for v in result['environment_variables']['from_env_files']['.env.example']}

    for var in result['environment_variables']['from_code']:
        if var['name'] not in example_vars:
            result['environment_variables']['required'].append({
                'name': var['name'],
                'reason': 'used in code but not in .env.example'
            })

    # Build summary
    result['summary'] = {
        'total_env_vars_in_code': len(all_env_vars),
        'client_exposed_count': len(result['environment_variables']['client_exposed']),
        'server_only_count': len(result['environment_variables']['server_only']),
        'config_files_count': len(result['config_files']),
        'config_types': list(set(c['type'] for c in result['config_files'])),
        'has_env_example': '.env.example' in result['environment_variables']['from_env_files'],
        'files_analyzed': files_processed
    }

    return result


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = analyze_config(root_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
