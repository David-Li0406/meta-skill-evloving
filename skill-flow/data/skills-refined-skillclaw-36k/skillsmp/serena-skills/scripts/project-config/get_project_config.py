#!/usr/bin/env python3
"""
Get project configuration from project.yml
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def get_project_config(project_root: str):
    """Get project configuration"""
    project_yml_path = Path(project_root) / ".tmp" / ".serena-skills" / "project.yml"
    
    if not project_yml_path.exists():
        return {
            "error": f"Project configuration not found at {project_yml_path}",
            "suggestion": "Run activate_project.py first to create configuration"
        }
    
    with open(project_yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return {
        "config_path": str(project_yml_path),
        "project_root": project_root,
        "configuration": config
    }


def main():
    parser = argparse.ArgumentParser(description="Get project configuration")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    
    args = parser.parse_args()
    
    try:
        result = get_project_config(args.project_root)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
