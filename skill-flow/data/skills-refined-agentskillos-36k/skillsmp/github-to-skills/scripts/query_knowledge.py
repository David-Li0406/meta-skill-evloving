#!/usr/bin/env python3
"""
Knowledge Query Tool

Query learned knowledge from GitHub repositories.
Supports progressive loading - only load knowledge relevant to current context.

Query modes:
- By framework: Get all knowledge about a specific framework
- By pattern: Get details about an architecture pattern
- By practice: Get details about a best practice
- By project: Auto-detect project tech stack and load relevant knowledge
- Search: Search across all knowledge
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional


def get_knowledge_dir() -> Path:
    """Get the knowledge directory path."""
    return Path(__file__).parent.parent / 'knowledge'


def load_index(knowledge_dir: Path) -> dict:
    """Load the knowledge index."""
    index_path = knowledge_dir / 'index.json'
    if not index_path.exists():
        return {
            'version': '1.0.0',
            'stats': {'total_repos_learned': 0, 'total_frameworks': 0},
            'index': {'frameworks': [], 'patterns': [], 'practices': []},
            'repos_learned': []
        }
    
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_name(name: str) -> str:
    """Normalize name for file lookup."""
    return name.lower().replace(' ', '-').replace('.', '-').replace('/', '-')


def load_framework_knowledge(knowledge_dir: Path, framework: str) -> Optional[dict]:
    """Load knowledge about a specific framework."""
    framework_key = normalize_name(framework)
    framework_file = knowledge_dir / 'frameworks' / f'{framework_key}.json'
    
    if not framework_file.exists():
        return None
    
    with open(framework_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_pattern_knowledge(knowledge_dir: Path, pattern: str) -> Optional[dict]:
    """Load knowledge about a specific pattern."""
    pattern_key = normalize_name(pattern)
    pattern_file = knowledge_dir / 'patterns' / f'{pattern_key}.json'
    
    if not pattern_file.exists():
        return None
    
    with open(pattern_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_practice_knowledge(knowledge_dir: Path, practice: str) -> Optional[dict]:
    """Load knowledge about a specific practice."""
    practice_key = normalize_name(practice)
    practice_file = knowledge_dir / 'practices' / f'{practice_key}.json'
    
    if not practice_file.exists():
        return None
    
    with open(practice_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_knowledge(knowledge_dir: Path, keyword: str) -> list:
    """Search knowledge by keyword across all categories."""
    results = []
    keyword_lower = keyword.lower()
    
    # Search frameworks
    frameworks_dir = knowledge_dir / 'frameworks'
    if frameworks_dir.exists():
        for f in frameworks_dir.glob('*.json'):
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Search in patterns and conventions
            for pattern in data.get('patterns', []):
                if keyword_lower in pattern.lower():
                    results.append({
                        'type': 'framework_pattern',
                        'framework': data.get('name', f.stem),
                        'content': pattern
                    })
            
            for conv in data.get('conventions', []):
                if keyword_lower in conv.lower():
                    results.append({
                        'type': 'framework_convention',
                        'framework': data.get('name', f.stem),
                        'content': conv
                    })
    
    # Search patterns
    patterns_dir = knowledge_dir / 'patterns'
    if patterns_dir.exists():
        for f in patterns_dir.glob('*.json'):
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if keyword_lower in data.get('name', '').lower():
                results.append({
                    'type': 'pattern',
                    'name': data.get('name'),
                    'description': data.get('description', '')
                })
    
    # Search practices
    practices_dir = knowledge_dir / 'practices'
    if practices_dir.exists():
        for f in practices_dir.glob('*.json'):
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if keyword_lower in data.get('name', '').lower():
                results.append({
                    'type': 'practice',
                    'name': data.get('name'),
                    'description': data.get('description', '')
                })
    
    return results


def query_by_project(knowledge_dir: Path, project_dir: str) -> dict:
    """
    Auto-detect project tech stack and load relevant knowledge.
    
    Args:
        knowledge_dir: Knowledge storage directory
        project_dir: Project directory to analyze
    
    Returns:
        dict with detected tech and relevant knowledge
    """
    # Import project detector
    prog_assist_scripts = Path(__file__).parent.parent.parent / 'programming-assistant' / 'scripts'
    sys.path.insert(0, str(prog_assist_scripts))
    
    try:
        from detect_project import detect_project
    except ImportError:
        return {'error': 'Project detector not available'}
    
    # Detect project tech stack
    detection = detect_project(project_dir)
    
    if 'error' in detection:
        return detection
    
    result = {
        'detected': detection,
        'knowledge': {
            'frameworks': {},
            'patterns': [],
            'practices': []
        }
    }
    
    # Load knowledge for each detected framework
    all_frameworks = detection.get('frameworks', [])
    
    for framework in all_frameworks:
        fw_knowledge = load_framework_knowledge(knowledge_dir, framework)
        if fw_knowledge:
            result['knowledge']['frameworks'][framework] = {
                'patterns': fw_knowledge.get('patterns', []),
                'conventions': fw_knowledge.get('conventions', []),
                'tips': fw_knowledge.get('tips', [])
            }
    
    # Load related patterns
    index = load_index(knowledge_dir)
    for pattern_key in index.get('index', {}).get('patterns', []):
        pattern_data = load_pattern_knowledge(knowledge_dir, pattern_key)
        if pattern_data:
            # Check if pattern is applicable to detected frameworks
            applicable = pattern_data.get('applicable_to', [])
            if not applicable or any(fw in applicable for fw in all_frameworks):
                result['knowledge']['patterns'].append({
                    'name': pattern_data.get('name'),
                    'description': pattern_data.get('description', '')
                })
    
    return result


def format_output(data, format_type: str = 'json') -> str:
    """Format output based on type."""
    if format_type == 'json':
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif format_type == 'markdown':
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, list):
                    lines.append(f"\n### {key.replace('_', ' ').title()}")
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(f"- **{item.get('name', 'Unknown')}**: {item.get('description', item.get('content', ''))}")
                        else:
                            lines.append(f"- {item}")
                elif isinstance(value, dict):
                    lines.append(f"\n### {key.replace('_', ' ').title()}")
                    for k, v in value.items():
                        lines.append(f"\n#### {k}")
                        if isinstance(v, dict):
                            for kk, vv in v.items():
                                if isinstance(vv, list) and vv:
                                    lines.append(f"**{kk}**:")
                                    for item in vv:
                                        lines.append(f"  - {item}")
                        elif isinstance(v, list):
                            for item in v:
                                lines.append(f"  - {item}")
                else:
                    lines.append(f"**{key}**: {value}")
            return '\n'.join(lines)
        elif isinstance(data, list):
            return '\n'.join(f"- {item}" for item in data)
    return str(data)


def main():
    parser = argparse.ArgumentParser(
        description='Query learned knowledge from GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query framework knowledge
  python query_knowledge.py --framework react
  python query_knowledge.py --framework gin
  python query_knowledge.py --framework spring-boot
  
  # Query by project (auto-detect)
  python query_knowledge.py --project /path/to/project
  
  # Search
  python query_knowledge.py --search "testing"
  
  # List all
  python query_knowledge.py --list-frameworks
  python query_knowledge.py --summary
        """
    )
    
    parser.add_argument(
        '--framework', '-f',
        help='Query knowledge for a specific framework'
    )
    parser.add_argument(
        '--pattern', '-p',
        help='Query a specific architecture pattern'
    )
    parser.add_argument(
        '--practice',
        help='Query a specific best practice'
    )
    parser.add_argument(
        '--project',
        help='Auto-detect project and load relevant knowledge'
    )
    parser.add_argument(
        '--search', '-s',
        help='Search knowledge by keyword'
    )
    parser.add_argument(
        '--list-frameworks',
        action='store_true',
        help='List all known frameworks'
    )
    parser.add_argument(
        '--list-patterns',
        action='store_true',
        help='List all known patterns'
    )
    parser.add_argument(
        '--list-repos',
        action='store_true',
        help='List all learned repositories'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show knowledge base summary'
    )
    parser.add_argument(
        '--knowledge-dir',
        default=str(get_knowledge_dir()),
        help='Knowledge directory path'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'markdown'],
        default='json',
        help='Output format'
    )
    
    args = parser.parse_args()
    knowledge_dir = Path(args.knowledge_dir)
    
    if not knowledge_dir.exists():
        print(f"Error: Knowledge directory not found: {knowledge_dir}", file=sys.stderr)
        print("Run extract_patterns.py --store first to build the knowledge base.", file=sys.stderr)
        sys.exit(1)
    
    index = load_index(knowledge_dir)
    
    if args.summary:
        summary = {
            'version': index.get('version', 'unknown'),
            'last_updated': index.get('last_updated'),
            'total_repos_learned': index.get('stats', {}).get('total_repos_learned', 0),
            'total_frameworks': index.get('stats', {}).get('total_frameworks', 0),
            'total_patterns': index.get('stats', {}).get('total_patterns', 0),
            'total_practices': index.get('stats', {}).get('total_practices', 0)
        }
        print(format_output(summary, args.format))
        return
    
    if args.list_frameworks:
        frameworks = index.get('index', {}).get('frameworks', [])
        print(format_output(frameworks, args.format))
        return
    
    if args.list_patterns:
        patterns = index.get('index', {}).get('patterns', [])
        print(format_output(patterns, args.format))
        return
    
    if args.list_repos:
        repos = index.get('repos_learned', [])
        print(format_output(repos, args.format))
        return
    
    if args.framework:
        result = load_framework_knowledge(knowledge_dir, args.framework)
        if result:
            print(format_output(result, args.format))
        else:
            print(f"No knowledge found for framework: {args.framework}", file=sys.stderr)
            sys.exit(1)
        return
    
    if args.pattern:
        result = load_pattern_knowledge(knowledge_dir, args.pattern)
        if result:
            print(format_output(result, args.format))
        else:
            print(f"No knowledge found for pattern: {args.pattern}", file=sys.stderr)
            sys.exit(1)
        return
    
    if args.practice:
        result = load_practice_knowledge(knowledge_dir, args.practice)
        if result:
            print(format_output(result, args.format))
        else:
            print(f"No knowledge found for practice: {args.practice}", file=sys.stderr)
            sys.exit(1)
        return
    
    if args.project:
        result = query_by_project(knowledge_dir, args.project)
        if 'error' in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(format_output(result, args.format))
        return
    
    if args.search:
        results = search_knowledge(knowledge_dir, args.search)
        if results:
            print(format_output(results, args.format))
        else:
            print(f"No results found for: {args.search}", file=sys.stderr)
        return
    
    # Default: show summary
    print(format_output({
        'frameworks': index.get('index', {}).get('frameworks', []),
        'patterns': index.get('index', {}).get('patterns', []),
        'practices': index.get('index', {}).get('practices', [])
    }, args.format))


if __name__ == '__main__':
    main()
