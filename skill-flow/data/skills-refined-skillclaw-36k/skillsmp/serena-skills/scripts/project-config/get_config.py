#!/usr/bin/env python3
"""
Get current configuration
"""
import argparse
import json
import os
import sys
from pathlib import Path


def get_config(project_root: str):
    """Get current configuration"""

    cwd = os.getcwd()
    serena_project_dir = Path(project_root) / ".tmp" / ".serena-skills"
    projects_file = serena_project_dir / "projects.json"

    projects = {}
    if projects_file.exists():
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)

    active_project = None
    for name, info in projects.items():
        if info["path"] == cwd or cwd.startswith(info["path"]):
            active_project = name
            break

    config = {
        "active_project": active_project,
        "current_directory": cwd,
        "project_root": project_root,
        "registered_projects": list(projects.keys()),
        "projects": projects,
        "serena_project_dir": str(serena_project_dir)
    }

    return config


def main():
    parser = argparse.ArgumentParser(description="Get current configuration")
    parser.add_argument("--project-root", help="Absolute path to project root (defaults to cwd)")
    args = parser.parse_args()
    
    try:
        project_root = args.project_root or os.getcwd()
        config = get_config(project_root)
        print(json.dumps(config, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
