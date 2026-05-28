#!/usr/bin/env python3
"""
Unified Knowledge Integration

This module bridges the two knowledge bases:
- github-to-skills/knowledge: Learned patterns from GitHub repositories
- programming-assistant/experience: User-specific experiences and preferences

The unified query provides both sources of knowledge when working on a project.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List


def get_project_root() -> Path:
    """Get the evolving-programming-agent project root."""
    return Path(__file__).parent.parent.parent


def get_github_knowledge_dir() -> Path:
    """Get github-to-skills knowledge directory."""
    return get_project_root() / 'github-to-skills' / 'knowledge'


def get_experience_dir() -> Path:
    """Get programming-assistant experience directory."""
    return get_project_root() / 'programming-assistant' / 'experience'


def load_json_safe(file_path: Path) -> Dict[str, Any]:
    """Safely load JSON file."""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def detect_project(project_dir: str) -> Dict[str, Any]:
    """Detect project tech stack using the project detector."""
    detector_path = get_project_root() / 'programming-assistant' / 'scripts'
    sys.path.insert(0, str(detector_path))
    
    try:
        from detect_project import detect_project as dp
        return dp(project_dir)
    except ImportError:
        return {'error': 'Project detector not available'}


def query_github_knowledge(tech_list: List[str]) -> Dict[str, Any]:
    """
    Query github-to-skills knowledge for given tech stack.
    
    Returns:
        Dict with frameworks, patterns, and practices knowledge
    """
    knowledge_dir = get_github_knowledge_dir()
    result: Dict[str, Any] = {
        'frameworks': {},
        'patterns': [],
        'practices': []
    }
    
    if not knowledge_dir.exists():
        return result
    
    # Load framework knowledge
    for tech in tech_list:
        tech_key = tech.lower().replace(' ', '-').replace('.', '-')
        framework_file = knowledge_dir / 'frameworks' / f'{tech_key}.json'
        if framework_file.exists():
            data = load_json_safe(framework_file)
            result['frameworks'][tech] = {
                'patterns': data.get('patterns', []),
                'conventions': data.get('conventions', []),
                'tips': data.get('tips', []),
                'sources': data.get('sources', [])
            }
    
    # Load all patterns and filter by applicable tech
    patterns_dir = knowledge_dir / 'patterns'
    if patterns_dir.exists():
        for pattern_file in patterns_dir.glob('*.json'):
            data = load_json_safe(pattern_file)
            applicable = data.get('applicable_to', [])
            # Include if no restriction or matches detected tech
            if not applicable or any(t.lower() in [a.lower() for a in applicable] for t in tech_list):
                result['patterns'].append({
                    'name': data.get('name', pattern_file.stem),
                    'description': data.get('description', ''),
                    'examples': data.get('examples', [])[:3]  # Limit examples
                })
    
    # Load practices
    practices_dir = knowledge_dir / 'practices'
    if practices_dir.exists():
        for practice_file in practices_dir.glob('*.json'):
            data = load_json_safe(practice_file)
            result['practices'].append({
                'name': data.get('name', practice_file.stem),
                'description': data.get('description', ''),
                'how_to': data.get('how_to', [])[:3]  # Limit steps
            })
    
    return result


def query_experience(tech_list: List[str]) -> Dict[str, Any]:
    """
    Query programming-assistant experience for given tech stack.
    
    Returns:
        Dict with preferences, fixes, and tech-specific patterns
    """
    experience_dir = get_experience_dir()
    result: Dict[str, Any] = {
        'preferences': [],
        'fixes': [],
        'tech_patterns': {}
    }
    
    if not experience_dir.exists():
        return result
    
    # Load index
    index = load_json_safe(experience_dir / 'index.json')
    result['preferences'] = index.get('preferences', [])
    result['fixes'] = index.get('fixes', [])
    
    # Load tech-specific experiences
    tech_dir = experience_dir / 'tech'
    if tech_dir.exists():
        for tech in tech_list:
            tech_key = tech.lower()
            tech_file = tech_dir / f'{tech_key}.json'
            if tech_file.exists():
                data = load_json_safe(tech_file)
                result['tech_patterns'][tech] = data.get('patterns', [])
    
    return result


def unified_query(project_dir: Optional[str] = None, tech_list: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Unified query that combines both knowledge sources.
    
    Args:
        project_dir: Optional project directory to auto-detect tech stack
        tech_list: Optional explicit list of technologies to query
    
    Returns:
        Dict with:
        - detected: Auto-detected tech stack (if project_dir provided)
        - github_knowledge: Patterns learned from GitHub repositories
        - experience: User's experiences and preferences
        - combined_tips: Merged tips for quick reference
    """
    result: Dict[str, Any] = {
        'detected': None,
        'github_knowledge': {},
        'experience': {},
        'combined_tips': []
    }
    
    # Determine tech stack
    final_tech_list: List[str] = []
    
    if project_dir:
        detection = detect_project(project_dir)
        if 'error' not in detection:
            result['detected'] = detection
            final_tech_list = (
                detection.get('base_tech', []) +
                detection.get('frameworks', []) +
                detection.get('tools', [])
            )
    
    if tech_list:
        final_tech_list.extend(tech_list)
    
    # Remove duplicates while preserving order
    seen: set = set()
    unique_tech: List[str] = []
    for t in final_tech_list:
        if t.lower() not in seen:
            seen.add(t.lower())
            unique_tech.append(t)
    
    if not unique_tech:
        return result
    
    # Query both knowledge sources
    result['github_knowledge'] = query_github_knowledge(unique_tech)
    result['experience'] = query_experience(unique_tech)
    
    # Combine tips for quick reference
    combined: List[str] = []
    
    # Add preferences first (user's explicit preferences)
    combined.extend(result['experience'].get('preferences', []))
    
    # Add framework tips from GitHub learning
    for fw, fw_data in result['github_knowledge'].get('frameworks', {}).items():
        for tip in fw_data.get('tips', [])[:2]:  # Max 2 tips per framework
            combined.append(f"[{fw}] {tip}")
    
    # Add fixes
    combined.extend(result['experience'].get('fixes', []))
    
    result['combined_tips'] = combined
    
    return result


def format_output(data: Dict[str, Any], format_type: str = 'json') -> str:
    """Format output based on type."""
    if format_type == 'json':
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif format_type == 'markdown':
        lines = []
        
        if data.get('detected'):
            det = data['detected']
            lines.append("## Detected Project")
            lines.append(f"- **Base**: {', '.join(det.get('base_tech', []))}")
            lines.append(f"- **Frameworks**: {', '.join(det.get('frameworks', []))}")
            lines.append(f"- **Tools**: {', '.join(det.get('tools', []))}")
            lines.append("")
        
        if data.get('combined_tips'):
            lines.append("## Quick Tips")
            for tip in data['combined_tips']:
                lines.append(f"- {tip}")
            lines.append("")
        
        gh = data.get('github_knowledge', {})
        if gh.get('frameworks'):
            lines.append("## Learned Patterns (from GitHub)")
            for fw, fw_data in gh['frameworks'].items():
                if fw_data.get('patterns'):
                    lines.append(f"\n### {fw}")
                    for p in fw_data['patterns'][:5]:
                        lines.append(f"- {p}")
        
        exp = data.get('experience', {})
        if exp.get('tech_patterns'):
            lines.append("\n## Experience Patterns")
            for tech, patterns in exp['tech_patterns'].items():
                lines.append(f"\n### {tech}")
                for p in patterns[:5]:
                    lines.append(f"- {p}")
        
        return '\n'.join(lines)
    
    return str(data)


def get_stats() -> Dict[str, Any]:
    """Get statistics from both knowledge bases."""
    gh_index = load_json_safe(get_github_knowledge_dir() / 'index.json')
    exp_index = load_json_safe(get_experience_dir() / 'index.json')
    
    return {
        'github_knowledge': {
            'repos_learned': gh_index.get('stats', {}).get('total_repos_learned', 0),
            'frameworks': gh_index.get('stats', {}).get('total_frameworks', 0),
            'patterns': gh_index.get('stats', {}).get('total_patterns', 0),
            'practices': gh_index.get('stats', {}).get('total_practices', 0)
        },
        'experience': {
            'version': exp_index.get('version', 'unknown'),
            'preferences': len(exp_index.get('preferences', [])),
            'fixes': len(exp_index.get('fixes', [])),
            'tech_stacks': len(exp_index.get('index', {}).get('tech_stacks', []))
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Unified knowledge query across github-to-skills and programming-assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query by project (auto-detect)
  python unified_knowledge.py --project /path/to/project
  
  # Query by explicit tech stack
  python unified_knowledge.py --tech react,typescript,jest
  
  # Get statistics
  python unified_knowledge.py --stats
  
  # Markdown output for embedding
  python unified_knowledge.py --project . --format markdown
        """
    )
    
    parser.add_argument(
        '--project', '-p',
        help='Project directory to auto-detect tech stack'
    )
    parser.add_argument(
        '--tech', '-t',
        help='Comma-separated list of technologies'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show knowledge base statistics'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'markdown'],
        default='json',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_stats()
        print(format_output(stats, args.format))
        return
    
    tech_list = None
    if args.tech:
        tech_list = [t.strip() for t in args.tech.split(',')]
    
    result = unified_query(project_dir=args.project, tech_list=tech_list)
    
    if not result.get('detected') and not result.get('github_knowledge') and not result.get('experience'):
        print("No knowledge found. Try:", file=sys.stderr)
        print("  - Specifying a project directory: --project /path/to/project", file=sys.stderr)
        print("  - Specifying technologies: --tech react,typescript", file=sys.stderr)
        sys.exit(1)
    
    print(format_output(result, args.format))


if __name__ == '__main__':
    main()
