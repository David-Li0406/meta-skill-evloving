#!/usr/bin/env python3
"""
GitHub Repository Scorer

Scores repositories 0-100 based on:
- Stars (0-25): Logarithmic scale
- Recency (0-20): Days since last update
- Documentation (0-15): README quality
- Relevance (0-25): Manual input
- License (0-15): Permissiveness
"""

import json
import math
from datetime import datetime, timezone
from typing import Dict, Any

def score_repo(repo_data: Dict[str, Any], relevance_score: int = 15) -> Dict[str, Any]:
    """
    Score a GitHub repository.
    
    Args:
        repo_data: Dict with keys: stars, last_updated, has_readme, readme_length, license
        relevance_score: Manual relevance score (0-25)
    
    Returns:
        Dict with score breakdown and total
    """
    
    # Stars score (0-25): Logarithmic scale
    stars = repo_data.get('stars', 0)
    if stars == 0:
        stars_score = 0
    else:
        stars_score = min(25, (math.log10(stars + 1) / math.log10(10000)) * 25)
    
    # Recency score (0-20): Days since last update
    last_updated_str = repo_data.get('last_updated', '')
    if last_updated_str:
        try:
            last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
            days_since = (datetime.now(timezone.utc) - last_updated).days
            recency_score = max(0, 20 - (days_since / 15))
        except:
            recency_score = 0
    else:
        recency_score = 0
    
    # Documentation score (0-15)
    has_readme = repo_data.get('has_readme', False)
    readme_length = repo_data.get('readme_length', 0)
    
    if not has_readme:
        doc_score = 0
    elif readme_length < 500:
        doc_score = 5  # Minimal README
    elif readme_length < 2000:
        doc_score = 10  # Basic README
    else:
        doc_score = 15  # Comprehensive README
    
    # License score (0-15)
    license_name = repo_data.get('license', '').lower()
    if 'mit' in license_name or 'apache' in license_name or 'bsd' in license_name:
        license_score = 15
    elif 'gpl' in license_name or 'lgpl' in license_name:
        license_score = 10
    elif license_name == '' or license_name == 'other':
        license_score = 5
    else:
        license_score = 0
    
    # Total score
    total = min(100, round(stars_score + recency_score + doc_score + relevance_score + license_score))
    
    return {
        'total': total,
        'breakdown': {
            'stars': round(stars_score, 1),
            'recency': round(recency_score, 1),
            'documentation': round(doc_score, 1),
            'relevance': relevance_score,
            'license': license_score
        }
    }

def get_score_emoji(score: int) -> str:
    """Return emoji for score range."""
    if score >= 80:
        return '🟢'
    elif score >= 60:
        return '🟡'
    elif score >= 40:
        return '🟠'
    else:
        return '🔴'

if __name__ == '__main__':
    # Example usage
    example_repo = {
        'stars': 1234,
        'last_updated': '2025-12-20T10:30:00Z',
        'has_readme': True,
        'readme_length': 3500,
        'license': 'MIT'
    }
    
    result = score_repo(example_repo, relevance_score=20)
    print(json.dumps(result, indent=2))
    print(f"\nScore: {get_score_emoji(result['total'])} {result['total']}/100")
