#!/usr/bin/env python3
"""
Intelligent E2E Test Selector

Analyzes changed files and recommends appropriate test suite based on impact.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Set

# Test suite decision matrix
HIGH_IMPACT_PATTERNS = {
    'src/app/**/page.tsx': 'Page components - affects user journeys',
    'src/components/ui/*': 'UI components - may break interactions',
    'src/server/actions/*': 'Server actions - critical paths',
    'middleware.ts': 'Middleware - affects all routes',
    'src/lib/auth/*': 'Auth changes - high risk',
    'src/app/(auth)/**/*': 'Auth flow changes',
    'src/app/(app)/**/*': 'Main app changes',
}

MEDIUM_IMPACT_PATTERNS = {
    'src/lib/**/*': 'Library utilities',
    'src/server/db/*': 'Database layer',
    'src/components/**/*': 'Components',
}

LOW_IMPACT_PATTERNS = {
    '*.test.ts': 'Test files',
    '*.test.tsx': 'Test files',
    'docs/*': 'Documentation',
    '*.md': 'Documentation',
    'supabase/migrations/*': 'Migrations (tested in preflight)',
}


def get_changed_files() -> List[str]:
    """Get list of changed files from git."""
    try:
        # Get staged files
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def matches_pattern(filepath: str, pattern: str) -> bool:
    """Check if filepath matches a glob pattern."""
    return Path(filepath).match(pattern)


def analyze_impact(files: List[str]) -> dict:
    """Analyze the impact level of changed files."""
    high_impact = []
    medium_impact = []
    low_impact = []

    for filepath in files:
        file_path = Path(filepath)

        # Check high impact patterns
        for pattern, reason in HIGH_IMPACT_PATTERNS.items():
            if matches_pattern(str(file_path), pattern):
                high_impact.append((filepath, reason))
                break
        else:
            # Check medium impact patterns
            for pattern, reason in MEDIUM_IMPACT_PATTERNS.items():
                if matches_pattern(str(file_path), pattern):
                    medium_impact.append((filepath, reason))
                    break
            else:
                # Check low impact patterns
                for pattern, reason in LOW_IMPACT_PATTERNS.items():
                    if matches_pattern(str(file_path), pattern):
                        low_impact.append((filepath, reason))
                        break
                else:
                    # Unknown pattern - treat as medium impact
                    medium_impact.append((filepath, 'Unknown file type'))

    return {
        'high': high_impact,
        'medium': medium_impact,
        'low': low_impact,
    }


def recommend_test_suite(impact: dict) -> str:
    """Recommend test suite based on impact analysis."""
    if impact['high']:
        return 'e2e:full'
    elif impact['medium']:
        return 'smoke'
    else:
        return 'skip'


def main():
    """Main entry point."""
    files = get_changed_files()

    if not files:
        print('{"recommendation": "skip", "reason": "No files changed"}')
        return

    impact = analyze_impact(files)
    recommendation = recommend_test_suite(impact)

    # Output JSON for easy parsing
    import json
    output = {
        'recommendation': recommendation,
        'files_analyzed': len(files),
        'high_impact': len(impact['high']),
        'medium_impact': len(impact['medium']),
        'low_impact': len(impact['low']),
        'high_impact_files': [f[0] for f in impact['high']],
        'reasons': [f[1] for f in impact['high']] if impact['high'] else [f[1] for f in impact['medium']],
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
