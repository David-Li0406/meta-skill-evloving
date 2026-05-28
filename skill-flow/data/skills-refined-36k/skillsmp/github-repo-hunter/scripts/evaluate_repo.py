#!/usr/bin/env python3
"""
GitHub Repository Evaluator - Scoring Algorithm
Evaluates repositories based on tech stack, domain relevance, code quality, and community.
"""

import json
import re
from typing import Dict

def score_tech_stack(repo: Dict) -> int:
    """Score based on technology stack match (max 30 points)."""
    score = 0
    readme = (repo.get('readme') or '').lower()
    language = (repo.get('language') or '').lower()
    
    # Primary languages (10 pts)
    if language in ['python', 'rust', 'javascript', 'typescript']:
        score += 10
    
    # Supabase/PostgreSQL (5 pts)
    if 'supabase' in readme or 'postgresql' in readme or 'postgres' in readme:
        score += 5
    
    # LangGraph/LangChain (5 pts)
    if 'langgraph' in readme or 'langchain' in readme:
        score += 5
    
    # FastAPI/Flask (5 pts)
    if 'fastapi' in readme or 'flask' in readme:
        score += 5
    
    # GitHub Actions/CI (5 pts)
    if 'github actions' in readme or 'ci/cd' in readme or '.github/workflows' in readme:
        score += 5
    
    return min(score, 30)  # Cap at 30

def score_domain_relevance(repo: Dict, target: str = 'both') -> int:
    """Score based on domain relevance (max 40 points)."""
    score = 0
    readme = (repo.get('readme') or '').lower()
    description = (repo.get('description') or '').lower()
    combined = readme + ' ' + description
    
    # BidDeed.AI relevance
    if target in ['biddeed', 'both']:
        if 'foreclosure' in combined or 'auction' in combined:
            score += 40
        elif 'property' in combined and ('scraping' in combined or 'data' in combined):
            score += 30
        elif 'ocr' in combined or ('pdf' in combined and 'extract' in combined):
            score += 25
        elif 'lien' in combined or 'title search' in combined:
            score += 30
        elif 'real estate' in combined and 'ml' in combined:
            score += 25
    
    # Life OS relevance
    if target in ['life-os', 'both']:
        if 'adhd' in combined or 'productivity' in combined:
            score += 40
        elif 'swimming' in combined and 'analytics' in combined:
            score += 35
        elif 'task' in combined and 'tracking' in combined:
            score += 30
        elif 'calendar' in combined or 'timezone' in combined:
            score += 25
        elif 'learning' in combined or 'journal' in combined:
            score += 20
    
    # Multi-agent orchestration (universal)
    if 'multi-agent' in combined or 'agentic' in combined:
        score += 20
    
    return min(score, 40)  # Cap at 40

def score_code_quality(repo: Dict) -> int:
    """Score based on code quality indicators (max 20 points)."""
    score = 0
    readme = (repo.get('readme') or '').lower()
    
    # Has tests (10 pts)
    if 'test' in readme or 'pytest' in readme or 'jest' in readme or 'unittest' in readme:
        score += 10
    
    # Good documentation (5 pts)
    readme_length = len(readme) if readme else 0
    if readme_length > 2500:  # ~500 words
        score += 5
    
    # Active development (5 pts)
    # Check for recent activity indicators
    if 'roadmap' in readme or 'changelog' in readme or 'contributing' in readme:
        score += 5
    
    return min(score, 20)  # Cap at 20

def score_community(repo: Dict) -> int:
    """Score based on community engagement (max 10 points)."""
    score = 0
    
    stars = repo.get('stars', 0)
    forks = repo.get('forks', 0)
    
    # Stars (5 pts)
    if stars > 100:
        score += 5
    elif stars > 50:
        score += 3
    elif stars > 20:
        score += 2
    
    # Forks (3 pts)
    if forks > 20:
        score += 3
    elif forks > 10:
        score += 2
    elif forks > 5:
        score += 1
    
    # License (2 pts - prefer open licenses)
    license_spdx = repo.get('license', 'Unknown')
    if license_spdx in ['MIT', 'Apache-2.0', 'BSD-3-Clause', 'BSD-2-Clause']:
        score += 2
    
    return min(score, 10)  # Cap at 10

def evaluate(repo: Dict, target: str = 'both') -> Dict:
    """
    Main evaluation function.
    
    Returns dict with:
        - total_score: 0-100
        - breakdown: score components
        - recommendation: AUTO_ADD, REVIEW, or SKIP
    """
    tech_score = score_tech_stack(repo)
    domain_score = score_domain_relevance(repo, target)
    quality_score = score_code_quality(repo)
    community_score = score_community(repo)
    
    total = tech_score + domain_score + quality_score + community_score
    
    if total >= 70:
        recommendation = 'AUTO_ADD'
    elif total >= 50:
        recommendation = 'REVIEW'
    else:
        recommendation = 'SKIP'
    
    return {
        'total_score': total,
        'breakdown': {
            'tech_stack': tech_score,
            'domain_relevance': domain_score,
            'code_quality': quality_score,
            'community': community_score
        },
        'recommendation': recommendation,
        'repo_name': repo.get('full_name', 'Unknown'),
        'url': repo.get('url', ''),
        'stars': repo.get('stars', 0),
        'language': repo.get('language', 'Unknown')
    }

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python evaluate_repo.py <discovered_repos.json> [target]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else 'both'
    
    with open(input_file, 'r') as f:
        repos = json.load(f)
    
    results = []
    for repo in repos:
        eval_result = evaluate(repo, target)
        results.append(eval_result)
        
        print(f"\n📊 {eval_result['repo_name']}")
        print(f"   Score: {eval_result['total_score']}/100")
        print(f"   Breakdown: Tech:{eval_result['breakdown']['tech_stack']} | "
              f"Domain:{eval_result['breakdown']['domain_relevance']} | "
              f"Quality:{eval_result['breakdown']['code_quality']} | "
              f"Community:{eval_result['breakdown']['community']}")
        print(f"   Recommendation: {eval_result['recommendation']}")
    
    # Save evaluation results
    output_file = input_file.replace('.json', '_evaluated.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Evaluation complete: {output_file}")
    
    # Summary
    auto_add = sum(1 for r in results if r['recommendation'] == 'AUTO_ADD')
    review = sum(1 for r in results if r['recommendation'] == 'REVIEW')
    skip = sum(1 for r in results if r['recommendation'] == 'SKIP')
    
    print(f"\n📈 Summary:")
    print(f"   AUTO_ADD: {auto_add}")
    print(f"   REVIEW: {review}")
    print(f"   SKIP: {skip}")
