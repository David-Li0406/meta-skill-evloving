#!/usr/bin/env python3
"""
Archive GitHub discovery to Supabase insights table
"""

import json
import sys
from datetime import datetime

def generate_insert_sql(repo_data: dict) -> str:
    """
    Generate SQL INSERT statement for Supabase insights table.
    
    Args:
        repo_data: Dict containing:
            - repo_url: str
            - repo_name: str
            - score: int
            - stars: int
            - description: str
            - language: str
            - license: str
            - last_updated: str (ISO format)
            - integration_recommendation: str
            - relevant_to: list[str] (e.g., ["biddeed", "life-os"])
    
    Returns:
        SQL INSERT statement as string
    """
    
    content = {
        "repo_url": repo_data.get('repo_url'),
        "score": repo_data.get('score'),
        "stars": repo_data.get('stars'),
        "description": repo_data.get('description'),
        "language": repo_data.get('language'),
        "license": repo_data.get('license'),
        "last_updated": repo_data.get('last_updated'),
        "integration_recommendation": repo_data.get('integration_recommendation'),
        "relevant_to": repo_data.get('relevant_to', []),
        "integration_status": "pending",
        "discovered_at": datetime.now().isoformat()
    }
    
    # Escape single quotes in JSON
    content_json = json.dumps(content).replace("'", "''")
    
    sql = f"""
INSERT INTO insights (category, subcategory, title, content, created_at)
VALUES (
  'github_discovery',
  'auto_hunter',
  'GitHub Hunter: {repo_data.get('repo_name')}',
  '{content_json}'::jsonb,
  NOW()
);
"""
    
    return sql

def generate_workflow_dispatch(repo_data: dict) -> dict:
    """
    Generate GitHub Actions workflow dispatch payload.
    
    For use with insert_insight.yml workflow.
    """
    
    content = {
        "repo_url": repo_data.get('repo_url'),
        "score": repo_data.get('score'),
        "stars": repo_data.get('stars'),
        "description": repo_data.get('description'),
        "language": repo_data.get('language'),
        "license": repo_data.get('license'),
        "last_updated": repo_data.get('last_updated'),
        "integration_recommendation": repo_data.get('integration_recommendation'),
        "relevant_to": repo_data.get('relevant_to', []),
        "integration_status": "pending"
    }
    
    return {
        "ref": "main",
        "inputs": {
            "category": "github_discovery",
            "subcategory": "auto_hunter",
            "title": f"GitHub Hunter: {repo_data.get('repo_name')}",
            "content": json.dumps(content)
        }
    }

if __name__ == '__main__':
    # Example usage
    example_repo = {
        'repo_url': 'https://github.com/jsvine/pdfplumber',
        'repo_name': 'pdfplumber',
        'score': 82,
        'stars': 6100,
        'description': 'Plumb a PDF for detailed information about tables, text, images.',
        'language': 'Python',
        'license': 'MIT',
        'last_updated': '2025-12-15T10:30:00Z',
        'integration_recommendation': 'Replace manual PDF parsing in BECA scraper with pdfplumber for structured table extraction.',
        'relevant_to': ['biddeed']
    }
    
    print("=== SQL INSERT ===")
    print(generate_insert_sql(example_repo))
    
    print("\n=== WORKFLOW DISPATCH PAYLOAD ===")
    print(json.dumps(generate_workflow_dispatch(example_repo), indent=2))
