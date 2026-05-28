#!/usr/bin/env python3
"""
Knowledge Store Tool

Store learned knowledge from GitHub repositories into the progressive knowledge base.
Knowledge is organized by:
- frameworks/<framework-name>.json - Framework-specific patterns and practices
- patterns/<pattern-name>.json - Architecture patterns
- practices/<practice-name>.json - Best practices

This enables progressive loading - only load knowledge relevant to current project.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def get_knowledge_dir() -> Path:
    """Get the knowledge directory path."""
    return Path(__file__).parent.parent / 'knowledge'


def ensure_directories(knowledge_dir: Path):
    """Ensure knowledge directory structure exists."""
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / 'frameworks').mkdir(exist_ok=True)
    (knowledge_dir / 'patterns').mkdir(exist_ok=True)
    (knowledge_dir / 'practices').mkdir(exist_ok=True)


def load_index(knowledge_dir: Path) -> dict:
    """Load the knowledge index."""
    index_path = knowledge_dir / 'index.json'
    if not index_path.exists():
        return {
            'version': '1.0.0',
            'last_updated': None,
            'stats': {
                'total_repos_learned': 0,
                'total_frameworks': 0,
                'total_patterns': 0,
                'total_practices': 0
            },
            'index': {
                'frameworks': [],
                'patterns': [],
                'practices': []
            },
            'repos_learned': []
        }
    
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_index(knowledge_dir: Path, index: dict):
    """Save the knowledge index."""
    index['last_updated'] = datetime.now().isoformat()
    index_path = knowledge_dir / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def normalize_name(name: str) -> str:
    """Normalize name for file storage."""
    return name.lower().replace(' ', '-').replace('.', '-').replace('/', '-')


def store_framework_knowledge(
    knowledge_dir: Path,
    framework: str,
    source_repo: str,
    patterns: Optional[list] = None,
    conventions: Optional[list] = None,
    tips: Optional[list] = None
) -> bool:
    """
    Store knowledge about a specific framework.
    
    Args:
        knowledge_dir: Knowledge storage directory
        framework: Framework name (e.g., 'react', 'gin', 'spring-boot')
        source_repo: Source GitHub repository URL
        patterns: List of architecture/coding patterns
        conventions: List of code conventions
        tips: List of tips/tricks
    """
    framework_key = normalize_name(framework)
    framework_file = knowledge_dir / 'frameworks' / f'{framework_key}.json'
    
    # Load existing or create new
    if framework_file.exists():
        with open(framework_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            'name': framework,
            'sources': [],
            'patterns': [],
            'conventions': [],
            'tips': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': None
        }
    
    # Add source if not already present
    if source_repo and source_repo not in data['sources']:
        data['sources'].append(source_repo)
    
    # Merge patterns (deduplicate)
    if patterns:
        for p in patterns:
            if p not in data['patterns']:
                data['patterns'].append(p)
    
    # Merge conventions (deduplicate)
    if conventions:
        for c in conventions:
            if c not in data['conventions']:
                data['conventions'].append(c)
    
    # Merge tips (deduplicate)
    if tips:
        for t in tips:
            if t not in data['tips']:
                data['tips'].append(t)
    
    data['updated_at'] = datetime.now().isoformat()
    
    # Save
    with open(framework_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Update index
    index = load_index(knowledge_dir)
    if framework_key not in index['index']['frameworks']:
        index['index']['frameworks'].append(framework_key)
        index['stats']['total_frameworks'] = len(index['index']['frameworks'])
    save_index(knowledge_dir, index)
    
    print(f"Stored framework knowledge: {framework}")
    return True


def store_pattern_knowledge(
    knowledge_dir: Path,
    pattern: str,
    source_repo: str,
    description: Optional[str] = None,
    examples: Optional[list] = None,
    applicable_to: Optional[list] = None
) -> bool:
    """
    Store knowledge about an architecture/design pattern.
    
    Args:
        knowledge_dir: Knowledge storage directory
        pattern: Pattern name (e.g., 'feature-based-architecture')
        source_repo: Source GitHub repository URL
        description: Pattern description
        examples: List of example implementations
        applicable_to: List of frameworks/languages this applies to
    """
    pattern_key = normalize_name(pattern)
    pattern_file = knowledge_dir / 'patterns' / f'{pattern_key}.json'
    
    # Load existing or create new
    if pattern_file.exists():
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            'name': pattern,
            'sources': [],
            'description': description or '',
            'examples': [],
            'applicable_to': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': None
        }
    
    # Add source
    if source_repo and source_repo not in data['sources']:
        data['sources'].append(source_repo)
    
    # Update description if provided and current is empty
    if description and not data['description']:
        data['description'] = description
    
    # Merge examples
    if examples:
        for e in examples:
            if e not in data['examples']:
                data['examples'].append(e)
    
    # Merge applicable_to
    if applicable_to:
        for a in applicable_to:
            if a not in data['applicable_to']:
                data['applicable_to'].append(a)
    
    data['updated_at'] = datetime.now().isoformat()
    
    # Save
    with open(pattern_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Update index
    index = load_index(knowledge_dir)
    if pattern_key not in index['index']['patterns']:
        index['index']['patterns'].append(pattern_key)
        index['stats']['total_patterns'] = len(index['index']['patterns'])
    save_index(knowledge_dir, index)
    
    print(f"Stored pattern knowledge: {pattern}")
    return True


def store_practice_knowledge(
    knowledge_dir: Path,
    practice: str,
    source_repo: str,
    description: Optional[str] = None,
    how_to: Optional[list] = None,
    benefits: Optional[list] = None
) -> bool:
    """
    Store knowledge about a best practice.
    
    Args:
        knowledge_dir: Knowledge storage directory
        practice: Practice name (e.g., 'automated-testing')
        source_repo: Source GitHub repository URL
        description: Practice description
        how_to: List of how-to steps
        benefits: List of benefits
    """
    practice_key = normalize_name(practice)
    practice_file = knowledge_dir / 'practices' / f'{practice_key}.json'
    
    # Load existing or create new
    if practice_file.exists():
        with open(practice_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            'name': practice,
            'sources': [],
            'description': description or '',
            'how_to': [],
            'benefits': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': None
        }
    
    # Add source
    if source_repo and source_repo not in data['sources']:
        data['sources'].append(source_repo)
    
    # Update description
    if description and not data['description']:
        data['description'] = description
    
    # Merge how_to
    if how_to:
        for h in how_to:
            if h not in data['how_to']:
                data['how_to'].append(h)
    
    # Merge benefits
    if benefits:
        for b in benefits:
            if b not in data['benefits']:
                data['benefits'].append(b)
    
    data['updated_at'] = datetime.now().isoformat()
    
    # Save
    with open(practice_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Update index
    index = load_index(knowledge_dir)
    if practice_key not in index['index']['practices']:
        index['index']['practices'].append(practice_key)
        index['stats']['total_practices'] = len(index['index']['practices'])
    save_index(knowledge_dir, index)
    
    print(f"Stored practice knowledge: {practice}")
    return True


def record_repo_learned(knowledge_dir: Path, repo_url: str, repo_name: str):
    """Record that a repository has been learned."""
    index = load_index(knowledge_dir)
    
    repo_entry = {
        'url': repo_url,
        'name': repo_name,
        'learned_at': datetime.now().isoformat()
    }
    
    # Check if already learned
    for r in index['repos_learned']:
        if r['url'] == repo_url:
            r['learned_at'] = datetime.now().isoformat()
            save_index(knowledge_dir, index)
            return
    
    index['repos_learned'].append(repo_entry)
    index['stats']['total_repos_learned'] = len(index['repos_learned'])
    save_index(knowledge_dir, index)


def store_from_extracted(knowledge_dir: Path, extracted_data: dict, source_repo: str):
    """
    Store knowledge from extracted patterns data (output of extract_patterns.py).
    
    Args:
        knowledge_dir: Knowledge storage directory
        extracted_data: Dict with patterns, tech_stack, conventions, practices
        source_repo: Source GitHub repository URL
    """
    ensure_directories(knowledge_dir)
    
    repo_name = extracted_data.get('name', 'unknown')
    
    # Store framework-specific knowledge
    tech_stack = extracted_data.get('tech_stack', {})
    frameworks = tech_stack.get('frameworks', [])
    
    for framework in frameworks:
        store_framework_knowledge(
            knowledge_dir,
            framework=framework,
            source_repo=source_repo,
            patterns=extracted_data.get('architecture_patterns', []),
            conventions=extracted_data.get('conventions', []),
            tips=[]
        )
    
    # Store architecture patterns
    for pattern in extracted_data.get('architecture_patterns', []):
        store_pattern_knowledge(
            knowledge_dir,
            pattern=pattern,
            source_repo=source_repo,
            applicable_to=frameworks
        )
    
    # Store best practices
    for practice in extracted_data.get('practices', []):
        store_practice_knowledge(
            knowledge_dir,
            practice=practice,
            source_repo=source_repo
        )
    
    # Record repo as learned
    record_repo_learned(knowledge_dir, source_repo, repo_name)
    
    print(f"Successfully stored knowledge from {repo_name}")


def main():
    parser = argparse.ArgumentParser(
        description='Store learned knowledge into progressive knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Store framework knowledge
  python store_knowledge.py --framework react --source https://github.com/... --pattern "Use hooks"
  
  # Store from extracted data (pipe from extract_patterns.py)
  cat extracted.json | python store_knowledge.py --from-json --source https://github.com/...
  
  # Store pattern
  python store_knowledge.py --pattern "Feature-Based Architecture" --source https://github.com/...
        """
    )
    
    parser.add_argument(
        '--framework',
        help='Store knowledge for a specific framework'
    )
    parser.add_argument(
        '--pattern',
        help='Store an architecture/design pattern'
    )
    parser.add_argument(
        '--practice',
        help='Store a best practice'
    )
    parser.add_argument(
        '--source',
        help='Source repository URL'
    )
    parser.add_argument(
        '--content',
        help='Content to store (pattern, convention, or tip)'
    )
    parser.add_argument(
        '--from-json',
        action='store_true',
        help='Read extracted data from stdin (JSON format)'
    )
    parser.add_argument(
        '--knowledge-dir',
        default=str(get_knowledge_dir()),
        help='Knowledge directory path'
    )
    
    args = parser.parse_args()
    knowledge_dir = Path(args.knowledge_dir)
    ensure_directories(knowledge_dir)
    
    if args.from_json:
        # Read extracted data from stdin
        try:
            extracted_data = json.load(sys.stdin)
            if not args.source:
                print("Error: --source is required with --from-json", file=sys.stderr)
                sys.exit(1)
            store_from_extracted(knowledge_dir, extracted_data, args.source)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.framework:
        if not args.source:
            print("Error: --source is required", file=sys.stderr)
            sys.exit(1)
        patterns = [args.content] if args.content else []
        store_framework_knowledge(knowledge_dir, args.framework, args.source, patterns=patterns)
    elif args.pattern:
        if not args.source:
            print("Error: --source is required", file=sys.stderr)
            sys.exit(1)
        store_pattern_knowledge(knowledge_dir, args.pattern, args.source)
    elif args.practice:
        if not args.source:
            print("Error: --source is required", file=sys.stderr)
            sys.exit(1)
        store_practice_knowledge(knowledge_dir, args.practice, args.source)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
