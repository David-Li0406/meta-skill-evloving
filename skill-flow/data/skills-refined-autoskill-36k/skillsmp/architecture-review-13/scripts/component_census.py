#!/usr/bin/env python3
"""
Component Census for Architecture Review

Maps React/React Native components including:
- Component definitions and their files
- Props extraction and typing
- Component usage tree
- Prop drilling detection
- Context providers and consumers
- Hooks usage catalog
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
MAX_FILES_TO_PROCESS = 400

# Built-in React hooks
BUILTIN_HOOKS = {
    'useState', 'useEffect', 'useContext', 'useReducer', 'useCallback',
    'useMemo', 'useRef', 'useImperativeHandle', 'useLayoutEffect',
    'useDebugValue', 'useDeferredValue', 'useTransition', 'useId',
    'useSyncExternalStore', 'useInsertionEffect'
}

# React Native specific hooks
RN_HOOKS = {
    'useColorScheme', 'useWindowDimensions', 'useAnimatedValue'
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


def is_react_project(root_path: Path) -> bool:
    """Check if this is a React/React Native project."""
    pkg_path = root_path / 'package.json'
    if not pkg_path.exists():
        return False

    try:
        content = read_file_safe(pkg_path)
        if content:
            pkg = json.loads(content)
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
            return 'react' in deps or 'react-native' in deps
    except Exception:
        pass

    return False


def extract_component_name(content: str, filename: str) -> List[Tuple[str, str]]:
    """Extract component names and their definition types from file."""
    components = []

    # Function component: function ComponentName or const ComponentName = (
    func_pattern = r'(?:export\s+)?(?:default\s+)?function\s+([A-Z][a-zA-Z0-9]*)\s*\('
    for match in re.finditer(func_pattern, content):
        components.append((match.group(1), 'function'))

    # Arrow function component: const ComponentName = ( or const ComponentName: FC =
    arrow_pattern = r'(?:export\s+)?const\s+([A-Z][a-zA-Z0-9]*)\s*(?::\s*(?:React\.)?(?:FC|FunctionComponent|ComponentType)[^=]*)?=\s*(?:\([^)]*\)|[a-z_][a-zA-Z0-9_]*)\s*=>'
    for match in re.finditer(arrow_pattern, content):
        name = match.group(1)
        if name not in [c[0] for c in components]:
            components.append((name, 'arrow'))

    # React.forwardRef
    forwardref_pattern = r'(?:export\s+)?const\s+([A-Z][a-zA-Z0-9]*)\s*=\s*(?:React\.)?forwardRef'
    for match in re.finditer(forwardref_pattern, content):
        name = match.group(1)
        if name not in [c[0] for c in components]:
            components.append((name, 'forwardRef'))

    # React.memo
    memo_pattern = r'(?:export\s+)?const\s+([A-Z][a-zA-Z0-9]*)\s*=\s*(?:React\.)?memo\s*\('
    for match in re.finditer(memo_pattern, content):
        name = match.group(1)
        if name not in [c[0] for c in components]:
            components.append((name, 'memo'))

    # If no components found, try to infer from filename for default export
    if not components and filename.endswith(('.tsx', '.jsx')):
        # Check for default export with JSX
        if re.search(r'export\s+default\s+', content) and re.search(r'<[A-Z][a-zA-Z]*|<div|<span|<View', content):
            name = Path(filename).stem
            if name[0].isupper() or name == 'index':
                # Convert kebab-case to PascalCase
                name = ''.join(word.capitalize() for word in name.replace('-', '_').split('_'))
                if name != 'Index':
                    components.append((name, 'inferred'))

    return components


def extract_props(content: str, component_name: str) -> List[Dict[str, Any]]:
    """Extract props for a component."""
    props = []

    # Look for Props type/interface
    props_type_pattern = rf'(?:type|interface)\s+{component_name}Props\s*(?:=\s*)?\{{([^}}]+)\}}'
    match = re.search(props_type_pattern, content, re.DOTALL)

    if match:
        props_body = match.group(1)
        # Extract individual props
        prop_pattern = r'(\w+)\s*(\?)?:\s*([^;,\n]+)'
        for prop_match in re.finditer(prop_pattern, props_body):
            props.append({
                'name': prop_match.group(1),
                'optional': bool(prop_match.group(2)),
                'type': prop_match.group(3).strip()[:50]
            })

    # Also check inline destructured props
    if not props:
        inline_pattern = rf'function\s+{component_name}\s*\(\s*\{{\s*([^}}]+)\s*\}}'
        match = re.search(inline_pattern, content)
        if match:
            props_str = match.group(1)
            for prop in props_str.split(','):
                prop = prop.strip()
                if prop and not prop.startswith('...'):
                    prop_name = prop.split('=')[0].split(':')[0].strip()
                    if prop_name:
                        props.append({
                            'name': prop_name,
                            'optional': '=' in prop,
                            'type': 'unknown'
                        })

    return props[:20]  # Limit props


def extract_hooks_usage(content: str) -> Dict[str, List[str]]:
    """Extract hooks usage from component."""
    hooks = {
        'builtin': [],
        'custom': []
    }

    # Find all hook calls
    hook_pattern = r'\b(use[A-Z][a-zA-Z0-9]*)\s*\('
    found_hooks = set()

    for match in re.finditer(hook_pattern, content):
        hook_name = match.group(1)
        if hook_name not in found_hooks:
            found_hooks.add(hook_name)
            if hook_name in BUILTIN_HOOKS or hook_name in RN_HOOKS:
                hooks['builtin'].append(hook_name)
            else:
                hooks['custom'].append(hook_name)

    return hooks


def extract_component_usage(content: str) -> List[str]:
    """Extract which components are used/rendered in this file."""
    used_components = []

    # JSX component usage: <ComponentName or <ComponentName.Sub
    jsx_pattern = r'<([A-Z][a-zA-Z0-9]*(?:\.[A-Z][a-zA-Z0-9]*)?)'
    found = set()

    for match in re.finditer(jsx_pattern, content):
        component = match.group(1)
        if component not in found:
            found.add(component)
            used_components.append(component)

    return used_components


def extract_context_info(content: str, file_path: str) -> Dict[str, Any]:
    """Extract Context provider and consumer information."""
    context_info = {
        'providers': [],
        'consumers': [],
        'creates_context': []
    }

    # Context creation
    create_pattern = r'(?:export\s+)?const\s+(\w+Context)\s*=\s*(?:React\.)?createContext'
    for match in re.finditer(create_pattern, content):
        context_info['creates_context'].append(match.group(1))

    # Provider usage
    provider_pattern = r'<(\w+)\.Provider|<(\w+Provider)'
    for match in re.finditer(provider_pattern, content):
        provider = match.group(1) or match.group(2)
        if provider:
            context_info['providers'].append(provider)

    # useContext usage
    use_context_pattern = r'useContext\s*\(\s*(\w+)\s*\)'
    for match in re.finditer(use_context_pattern, content):
        context_info['consumers'].append(match.group(1))

    return context_info


def detect_prop_drilling(components: Dict[str, Any], usage_graph: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """Detect potential prop drilling patterns."""
    drilling_paths = []

    # Track props that appear across multiple component levels
    prop_locations = defaultdict(list)

    for comp_name, comp_info in components.items():
        for prop in comp_info.get('props', []):
            prop_name = prop['name']
            if prop_name not in ['children', 'className', 'style', 'key', 'ref', 'id']:
                prop_locations[prop_name].append(comp_name)

    # Find props that appear in 3+ components (potential drilling)
    for prop_name, component_list in prop_locations.items():
        if len(component_list) >= 3:
            drilling_paths.append({
                'prop': prop_name,
                'components': component_list[:10],
                'depth': len(component_list)
            })

    # Sort by depth
    drilling_paths.sort(key=lambda x: -x['depth'])
    return drilling_paths[:10]


def analyze_components(root_dir: str) -> Dict[str, Any]:
    """Main analysis function."""
    root_path = Path(root_dir).resolve()

    if not root_path.is_dir():
        return {'error': f'Directory not found: {root_dir}'}

    if not is_react_project(root_path):
        return {
            'root': root_path.name,
            'is_react_project': False,
            'message': 'Not a React/React Native project',
            'components': [],
            'summary': {}
        }

    components = {}
    usage_graph = defaultdict(list)  # component -> [uses these components]
    hooks_summary = defaultdict(int)
    custom_hooks = defaultdict(int)
    context_summary = {
        'providers': [],
        'contexts_created': []
    }

    files_processed = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        for filename in filenames:
            if not filename.endswith(('.tsx', '.jsx')):
                continue

            if files_processed >= MAX_FILES_TO_PROCESS:
                break

            file_path = Path(dirpath) / filename
            rel_path = str(file_path.relative_to(root_path))

            content = read_file_safe(file_path)
            if not content:
                continue

            files_processed += 1

            # Extract components from this file
            found_components = extract_component_name(content, filename)

            for comp_name, comp_type in found_components:
                # Get props
                props = extract_props(content, comp_name)

                # Get hooks usage
                hooks = extract_hooks_usage(content)

                # Get used components
                used_components = extract_component_usage(content)

                # Store component info
                components[comp_name] = {
                    'name': comp_name,
                    'file': rel_path,
                    'type': comp_type,
                    'props': props,
                    'hooks_used': hooks,
                    'uses_components': used_components
                }

                # Update usage graph
                usage_graph[comp_name] = used_components

                # Update hooks summary
                for hook in hooks['builtin']:
                    hooks_summary[hook] += 1
                for hook in hooks['custom']:
                    custom_hooks[hook] += 1

            # Extract context info
            ctx_info = extract_context_info(content, rel_path)
            if ctx_info['creates_context']:
                for ctx in ctx_info['creates_context']:
                    context_summary['contexts_created'].append({
                        'name': ctx,
                        'file': rel_path
                    })
            if ctx_info['providers']:
                for provider in ctx_info['providers']:
                    context_summary['providers'].append({
                        'name': provider,
                        'file': rel_path
                    })

        if files_processed >= MAX_FILES_TO_PROCESS:
            break

    # Build component tree (used_by relationships)
    used_by = defaultdict(list)
    for comp_name, uses in usage_graph.items():
        for used_comp in uses:
            if used_comp in components:
                used_by[used_comp].append(comp_name)

    for comp_name in components:
        components[comp_name]['used_by'] = used_by.get(comp_name, [])

    # Detect prop drilling
    prop_drilling = detect_prop_drilling(components, dict(usage_graph))

    # Convert to list for output
    components_list = list(components.values())

    return {
        'root': root_path.name,
        'is_react_project': True,
        'components': components_list,
        'component_tree': dict(usage_graph),
        'prop_drilling_paths': prop_drilling,
        'context_providers': context_summary,
        'hooks_summary': {
            'builtin': dict(hooks_summary),
            'custom': dict(custom_hooks)
        },
        'summary': {
            'total_components': len(components_list),
            'total_hooks_usage': sum(hooks_summary.values()),
            'custom_hooks_count': len(custom_hooks),
            'contexts_count': len(context_summary['contexts_created']),
            'potential_prop_drilling': len(prop_drilling),
            'files_analyzed': files_processed
        }
    }


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = analyze_components(root_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
