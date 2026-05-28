#!/usr/bin/env python3
"""
Update project configuration in project.yml
"""
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def update_project_config(project_root: str, key: str, value: str):
    """Update a configuration value in project.yml"""
    project_yml_path = Path(project_root) / ".tmp" / ".serena-skills" / "project.yml"
    
    if not project_yml_path.exists():
        raise FileNotFoundError(
            f"Project configuration not found at {project_yml_path}. "
            "Run activate_project.py first."
        )
    
    # Load existing config
    with open(project_yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Parse value (handle lists and booleans)
    if value.lower() in ('true', 'false'):
        parsed_value = value.lower() == 'true'
    elif value.startswith('[') and value.endswith(']'):
        # Simple list parsing
        parsed_value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
    else:
        parsed_value = value
    
    # Update config
    config[key] = parsed_value
    
    # Save config
    with open(project_yml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    return f"Updated {key} = {parsed_value}"


def main():
    parser = argparse.ArgumentParser(description="Update project configuration")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--key", required=True, help="Configuration key to update")
    parser.add_argument("--value", required=True, help="New value (supports strings, booleans, lists)")
    
    args = parser.parse_args()
    
    try:
        result = update_project_config(args.project_root, args.key, args.value)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
