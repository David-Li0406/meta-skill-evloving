#!/usr/bin/env python3
"""
API Surface Extractor for Architecture Review

Extracts API routes and endpoints from:
- Express.js
- Fastify
- Next.js (Pages Router API routes and App Router route handlers)
- Hono
- NestJS
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
MAX_FILES_TO_PROCESS = 300

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']


def read_file_safe(file_path: Path) -> Optional[str]:
    """Read file with size limit."""
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return None
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def detect_framework(root_path: Path) -> Optional[str]:
    """Detect which API framework is being used."""
    pkg_path = root_path / 'package.json'

    if not pkg_path.exists():
        return None

    try:
        content = read_file_safe(pkg_path)
        if not content:
            return None

        pkg = json.loads(content)
        deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

        # Check in priority order
        if 'next' in deps:
            return 'next.js'
        if '@nestjs/core' in deps:
            return 'nestjs'
        if 'hono' in deps:
            return 'hono'
        if 'fastify' in deps:
            return 'fastify'
        if 'express' in deps:
            return 'express'
        if '@hapi/hapi' in deps:
            return 'hapi'
        if 'koa' in deps:
            return 'koa'

    except Exception:
        pass

    return None


def extract_express_routes(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract routes from Express.js code."""
    routes = []

    # Patterns for Express routes
    patterns = [
        # app.get('/path', handler)
        r'(?:app|router)\.(get|post|put|delete|patch|head|options)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        # router.route('/path').get(handler).post(handler)
        r'\.route\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)\.(\w+)',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            if len(match.groups()) == 2:
                if match.group(1) in HTTP_METHODS or match.group(1).upper() in HTTP_METHODS:
                    method = match.group(1).upper()
                    path = match.group(2)
                else:
                    path = match.group(1)
                    method = match.group(2).upper()

                if method.upper() in HTTP_METHODS:
                    routes.append({
                        'path': path,
                        'method': method.upper(),
                        'file': file_path,
                        'framework': 'express'
                    })

    # Extract middleware usage
    middleware_pattern = r'(?:app|router)\.use\s*\(\s*[\'"]?([^\'")\s,]+)'
    for match in re.finditer(middleware_pattern, content):
        middleware = match.group(1)
        if not middleware.startswith('/'):
            routes.append({
                'path': '*',
                'method': 'MIDDLEWARE',
                'file': file_path,
                'framework': 'express',
                'middleware': middleware
            })

    return routes


def extract_fastify_routes(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract routes from Fastify code."""
    routes = []

    # fastify.get('/path', handler)
    pattern = r'(?:fastify|server|app)\.(get|post|put|delete|patch|head|options)\s*\(\s*[\'"]([^\'"]+)[\'"]'

    for match in re.finditer(pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        path = match.group(2)

        if method in HTTP_METHODS:
            routes.append({
                'path': path,
                'method': method,
                'file': file_path,
                'framework': 'fastify'
            })

    # fastify.route({ method: 'GET', url: '/path' })
    route_obj_pattern = r'\.route\s*\(\s*\{[^}]*method\s*:\s*[\'"](\w+)[\'"][^}]*url\s*:\s*[\'"]([^\'"]+)[\'"]'
    for match in re.finditer(route_obj_pattern, content, re.IGNORECASE):
        routes.append({
            'path': match.group(2),
            'method': match.group(1).upper(),
            'file': file_path,
            'framework': 'fastify'
        })

    return routes


def extract_hono_routes(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract routes from Hono code."""
    routes = []

    # app.get('/path', handler)
    pattern = r'(?:app|hono)\.(get|post|put|delete|patch|all)\s*\(\s*[\'"]([^\'"]+)[\'"]'

    for match in re.finditer(pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        path = match.group(2)

        if method == 'ALL':
            method = '*'

        routes.append({
            'path': path,
            'method': method,
            'file': file_path,
            'framework': 'hono'
        })

    return routes


def extract_nextjs_routes(root_path: Path) -> List[Dict[str, Any]]:
    """Extract routes from Next.js file structure."""
    routes = []

    # Check Pages Router API routes
    api_dir = root_path / 'pages' / 'api'
    if api_dir.is_dir():
        for file_path in api_dir.rglob('*.ts'):
            routes.extend(extract_nextjs_pages_api(file_path, root_path))
        for file_path in api_dir.rglob('*.js'):
            routes.extend(extract_nextjs_pages_api(file_path, root_path))

    # Check App Router
    app_dir = root_path / 'app'
    if app_dir.is_dir():
        for file_path in app_dir.rglob('route.ts'):
            routes.extend(extract_nextjs_app_route(file_path, root_path))
        for file_path in app_dir.rglob('route.js'):
            routes.extend(extract_nextjs_app_route(file_path, root_path))

    # Also check src/pages/api and src/app
    src_api_dir = root_path / 'src' / 'pages' / 'api'
    if src_api_dir.is_dir():
        for file_path in src_api_dir.rglob('*.ts'):
            routes.extend(extract_nextjs_pages_api(file_path, root_path))
        for file_path in src_api_dir.rglob('*.js'):
            routes.extend(extract_nextjs_pages_api(file_path, root_path))

    src_app_dir = root_path / 'src' / 'app'
    if src_app_dir.is_dir():
        for file_path in src_app_dir.rglob('route.ts'):
            routes.extend(extract_nextjs_app_route(file_path, root_path))
        for file_path in src_app_dir.rglob('route.js'):
            routes.extend(extract_nextjs_app_route(file_path, root_path))

    return routes


def extract_nextjs_pages_api(file_path: Path, root_path: Path) -> List[Dict[str, Any]]:
    """Extract API route from Next.js pages/api file."""
    routes = []
    rel_path = str(file_path.relative_to(root_path))

    # Convert file path to API route
    # pages/api/users/[id].ts -> /api/users/[id]
    api_path = rel_path
    for prefix in ['src/pages', 'pages']:
        if api_path.startswith(prefix):
            api_path = api_path[len(prefix):]
            break

    # Remove extension
    api_path = re.sub(r'\.[jt]sx?$', '', api_path)

    # Remove /index suffix
    if api_path.endswith('/index'):
        api_path = api_path[:-6] or '/'

    content = read_file_safe(file_path)
    methods = ['*']  # Default: handles all methods

    if content:
        # Check for specific method handlers
        specific_methods = []
        for method in HTTP_METHODS:
            if re.search(rf'req\.method\s*===?\s*[\'\"]{method}[\'\"]', content, re.IGNORECASE):
                specific_methods.append(method)
            if re.search(rf'case\s*[\'\"]{method}[\'\"]', content, re.IGNORECASE):
                specific_methods.append(method)

        if specific_methods:
            methods = specific_methods

    for method in methods:
        routes.append({
            'path': api_path,
            'method': method,
            'file': rel_path,
            'framework': 'next.js',
            'router': 'pages'
        })

    return routes


def extract_nextjs_app_route(file_path: Path, root_path: Path) -> List[Dict[str, Any]]:
    """Extract API route from Next.js App Router route.ts file."""
    routes = []
    rel_path = str(file_path.relative_to(root_path))

    # Convert file path to API route
    # app/api/users/[id]/route.ts -> /api/users/[id]
    api_path = str(file_path.parent.relative_to(root_path))
    for prefix in ['src/app', 'app']:
        if api_path.startswith(prefix):
            api_path = api_path[len(prefix):]
            break

    if not api_path.startswith('/'):
        api_path = '/' + api_path

    content = read_file_safe(file_path)
    methods = []

    if content:
        # App Router exports named functions for HTTP methods
        for method in HTTP_METHODS:
            if re.search(rf'export\s+(?:async\s+)?function\s+{method}\b', content):
                methods.append(method)
            if re.search(rf'export\s+const\s+{method}\s*=', content):
                methods.append(method)

    if not methods:
        methods = ['*']

    for method in methods:
        routes.append({
            'path': api_path,
            'method': method,
            'file': rel_path,
            'framework': 'next.js',
            'router': 'app'
        })

    return routes


def extract_nestjs_routes(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract routes from NestJS controllers."""
    routes = []

    # Find controller decorator
    controller_match = re.search(r'@Controller\s*\(\s*[\'"]([^\'"]*)[\'"]?\s*\)', content)
    base_path = controller_match.group(1) if controller_match else ''

    # Find method decorators
    method_pattern = r'@(Get|Post|Put|Delete|Patch|Head|Options|All)\s*\(\s*[\'"]?([^\'")\s]*)?[\'"]?\s*\)'

    for match in re.finditer(method_pattern, content):
        method = match.group(1).upper()
        path = match.group(2) or ''

        full_path = f"/{base_path}/{path}".replace('//', '/').rstrip('/')
        if not full_path:
            full_path = '/'

        routes.append({
            'path': full_path,
            'method': method if method != 'ALL' else '*',
            'file': file_path,
            'framework': 'nestjs'
        })

    return routes


def analyze_api_surface(root_dir: str) -> Dict[str, Any]:
    """Main analysis function."""
    root_path = Path(root_dir).resolve()

    if not root_path.is_dir():
        return {'error': f'Directory not found: {root_dir}'}

    framework = detect_framework(root_path)

    routes = []
    middleware_usage = defaultdict(int)
    files_processed = 0

    # For Next.js, extract from file structure
    if framework == 'next.js':
        routes.extend(extract_nextjs_routes(root_path))

    # Walk directory for code-based routes
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

            # Extract routes based on detected or inferred framework
            extracted = []

            if framework == 'express' or 'express' in content.lower():
                extracted.extend(extract_express_routes(content, rel_path))

            if framework == 'fastify' or 'fastify' in content.lower():
                extracted.extend(extract_fastify_routes(content, rel_path))

            if framework == 'hono' or 'Hono' in content:
                extracted.extend(extract_hono_routes(content, rel_path))

            if framework == 'nestjs' or '@Controller' in content:
                extracted.extend(extract_nestjs_routes(content, rel_path))

            routes.extend(extracted)

            # Track middleware
            for route in extracted:
                if 'middleware' in route:
                    middleware_usage[route['middleware']] += 1

        if files_processed >= MAX_FILES_TO_PROCESS:
            break

    # Deduplicate routes
    seen = set()
    unique_routes = []
    for route in routes:
        key = (route['path'], route['method'], route['file'])
        if key not in seen:
            seen.add(key)
            unique_routes.append(route)

    # Sort routes
    unique_routes.sort(key=lambda r: (r['path'], r['method']))

    # Group by path
    routes_by_path = defaultdict(list)
    for route in unique_routes:
        routes_by_path[route['path']].append(route['method'])

    return {
        'root': root_path.name,
        'framework': framework,
        'routes': unique_routes,
        'routes_by_path': dict(routes_by_path),
        'middleware_usage': dict(middleware_usage),
        'summary': {
            'total_routes': len(unique_routes),
            'total_paths': len(routes_by_path),
            'methods_used': list(set(r['method'] for r in unique_routes)),
            'framework_detected': framework,
            'files_analyzed': files_processed
        }
    }


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = analyze_api_surface(root_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
