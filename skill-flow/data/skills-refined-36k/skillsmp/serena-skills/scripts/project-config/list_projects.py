#!/usr/bin/env python3
"""
List all registered projects
"""
import argparse
import json
import os
import sys
from pathlib import Path


def get_projects_file(project_root: str) -> Path:
    """Get path to project-local registry file"""
    serena_project_dir = Path(project_root) / ".tmp" / ".serena-skills"
    return serena_project_dir / "projects.json"


def list_projects(project_root: str):
    """List all registered projects"""
    projects_file = get_projects_file(project_root)
    
    if not projects_file.exists():
        return {}
    
    with open(projects_file, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    
    return projects


def main():
    parser = argparse.ArgumentParser(description="List registered projects")
    parser.add_argument("--project-root", help="Absolute path to project root (defaults to cwd)")
    args = parser.parse_args()
    
    try:
        project_root = args.project_root or os.getcwd()
        projects = list_projects(project_root)
        print(json.dumps(projects, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
