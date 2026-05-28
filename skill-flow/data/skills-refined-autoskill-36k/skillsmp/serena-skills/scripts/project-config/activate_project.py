#!/usr/bin/env python3
"""
Activate and register a project
"""
import argparse
import json
import os
import sys
from pathlib import Path


def create_project_yml_template(language: str) -> str:
    """Create project.yml template content"""
    return f"""# Serena Skills Project Configuration

# list of languages for language servers; choose from:
#   python, typescript, java, go, cpp, rust, csharp, ruby, php, etc.
# When using multiple languages, the first language server that supports a given file will be used.
languages: ["{language}"]

# the encoding used by text files in the project
encoding: "utf-8"

# whether to use the project's gitignore file to ignore files
ignore_all_files_in_gitignore: true

# list of additional paths to ignore (same syntax as gitignore)
ignored_paths: []

# whether the project is in read-only mode
# If set to true, all editing tools will be disabled
read_only: false

# list of tool names to exclude (not recommended)
excluded_tools: []

# initial prompt for the project
initial_prompt: ""
"""


def get_projects_file(project_root: str) -> Path:
    """Get path to project-local registry file"""
    serena_project_dir = Path(project_root) / ".tmp" / ".serena-skills"
    serena_project_dir.mkdir(parents=True, exist_ok=True)
    return serena_project_dir / "projects.json"


def load_projects(project_root: str):
    """Load registered projects"""
    projects_file = get_projects_file(project_root)
    if projects_file.exists():
        with open(projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_projects(project_root: str, projects):
    """Save registered projects"""
    projects_file = get_projects_file(project_root)
    with open(projects_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)


def activate_project(project_path: str, name: str | None = None):
    """Activate a project"""
    
    project_path = os.path.abspath(project_path)
    
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Project path does not exist: {project_path}")
    
    if not os.path.isdir(project_path):
        raise ValueError(f"Project path is not a directory: {project_path}")
    
    # Use directory name as default project name
    if name is None:
        name = os.path.basename(project_path)
    
    # Detect language
    language = "python"  # Default
    for root, dirs, files in os.walk(project_path):
        if any(f.endswith('.ts') or f.endswith('.tsx') for f in files):
            language = "typescript"
            break
        elif any(f.endswith('.java') for f in files):
            language = "java"
            break
        elif any(f.endswith('.go') for f in files):
            language = "go"
            break
    
    # Load and update projects (project-local registry)
    projects = load_projects(project_path)
    projects[name] = {
        "path": project_path,
        "language": language,
        "encoding": "utf-8"
    }
    save_projects(project_path, projects)
    
    # Create .tmp/.serena-skills directory in project
    serena_project_dir = Path(project_path) / ".tmp" / ".serena-skills"
    serena_project_dir.mkdir(parents=True, exist_ok=True)
    (serena_project_dir / "memories").mkdir(exist_ok=True)
    
    # Create project.yml if it doesn't exist
    project_yml_path = serena_project_dir / "project.yml"
    if not project_yml_path.exists():
        yml_content = create_project_yml_template(language)
        with open(project_yml_path, 'w', encoding='utf-8') as f:
            f.write(yml_content)
    
    return f"Project activated: {name} ({project_path})\nLanguage: {language}\nConfig: {project_yml_path}"


def main():
    parser = argparse.ArgumentParser(description="Activate a project")
    parser.add_argument("--project-path", required=True, help="Absolute path to project")
    parser.add_argument("--name", help="Project name (defaults to directory name)")
    
    args = parser.parse_args()
    
    try:
        result = activate_project(args.project_path, args.name)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
