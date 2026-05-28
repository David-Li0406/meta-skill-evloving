#!/usr/bin/env python3
"""
Analyze git changes since last documentation update.

This tool:
- Analyzes git history to identify changes
- Categorizes changes (architecture, modules, config, dependencies)
- Suggests which documentation files need updates
- Can scope updates to specific areas

Returns structured JSON with change analysis and update suggestions.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime


def run_git_command(project_path: Path, command: List[str]) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + command,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""


def is_git_repo(project_path: Path) -> bool:
    """Check if directory is a git repository."""
    git_dir = project_path / ".git"
    return git_dir.exists()


def get_last_doc_update_commit(project_path: Path) -> str:
    """Get the last commit that modified documentation hub."""
    docs_path = "cline-docs/"

    # Get last commit that touched cline-docs
    output = run_git_command(project_path, [
        'log', '-1', '--format=%H', '--', docs_path
    ])

    if output:
        return output
    else:
        # If no doc commits, use initial commit or fallback
        output = run_git_command(project_path, ['rev-list', '--max-parents=0', 'HEAD'])
        if output:
            return output.split('\n')[0]
        return 'HEAD~10'  # Fallback to last 10 commits


def get_changed_files(project_path: Path, since_commit: str) -> List[str]:
    """Get list of changed files since a commit."""
    output = run_git_command(project_path, [
        'diff', '--name-only', f'{since_commit}..HEAD'
    ])

    if output:
        return [f for f in output.split('\n') if f]
    return []


def categorize_changes(changed_files: List[str]) -> Dict:
    """Categorize changed files into meaningful groups."""
    categories = {
        "architecture": [],
        "modules": [],
        "config": [],
        "dependencies": [],
        "database": [],
        "api": [],
        "ui": [],
        "tests": [],
        "other": []
    }

    for file_path in changed_files:
        path_lower = file_path.lower()

        # Configuration files
        if any(config in path_lower for config in [
            'config.js', 'config.ts', 'config.json', '.env',
            'docker-compose', 'dockerfile', '.yml', '.yaml'
        ]):
            categories["config"].append(file_path)

        # Dependencies
        elif any(dep in path_lower for dep in [
            'package.json', 'package-lock.json', 'yarn.lock',
            'requirements.txt', 'pyproject.toml', 'poetry.lock'
        ]):
            categories["dependencies"].append(file_path)

        # Database
        elif any(db in path_lower for db in [
            'schema.prisma', 'migration', 'models', 'schema.sql'
        ]):
            categories["database"].append(file_path)

        # API/Routes
        elif any(api in path_lower for api in [
            '/api/', '/routes/', '/controllers/', '/endpoints/'
        ]):
            categories["api"].append(file_path)

        # UI Components
        elif any(ui in path_lower for ui in [
            '/components/', '/pages/', '/views/', '/app/'
        ]):
            categories["ui"].append(file_path)

        # Tests
        elif any(test in path_lower for test in [
            '.test.', '.spec.', '/tests/', '/__tests__/'
        ]):
            categories["tests"].append(file_path)

        # New modules (new directories in src/)
        elif 'src/' in path_lower:
            # Check if it's in a subdirectory of src
            parts = file_path.split('/')
            if len(parts) > 2 and parts[0] == 'src':
                module_name = parts[1]
                if module_name not in [f.split('/')[1] for f in categories["modules"] if '/' in f]:
                    categories["modules"].append(f"src/{module_name}")

        # Architecture changes (core system files)
        elif any(arch in path_lower for arch in [
            'main.', 'app.', 'index.', 'server.', 'client.'
        ]) and not any(test in path_lower for test in ['.test.', '.spec.']):
            categories["architecture"].append(file_path)

        else:
            categories["other"].append(file_path)

    return categories


def generate_change_descriptions(categories: Dict) -> List[str]:
    """Generate human-readable descriptions of changes."""
    descriptions = []

    if categories["dependencies"]:
        descriptions.append(f"Updated {len(categories['dependencies'])} dependency file(s)")

    if categories["config"]:
        config_files = [Path(f).name for f in categories["config"][:3]]
        descriptions.append(f"Modified configuration: {', '.join(config_files)}")

    if categories["database"]:
        descriptions.append("Database schema or models changed")

    if categories["api"]:
        api_count = len(categories["api"])
        descriptions.append(f"Modified {api_count} API/route file(s)")

    if categories["modules"]:
        unique_modules = list(set(categories["modules"]))
        if len(unique_modules) <= 3:
            descriptions.append(f"Changes in modules: {', '.join(unique_modules)}")
        else:
            descriptions.append(f"Changes in {len(unique_modules)} modules")

    if categories["architecture"]:
        descriptions.append("Core architecture files modified")

    if categories["ui"]:
        ui_count = len(categories["ui"])
        if ui_count > 5:
            descriptions.append(f"Significant UI changes ({ui_count} files)")

    return descriptions


def suggest_documentation_updates(categories: Dict, changed_files: List[str]) -> List[str]:
    """Suggest which documentation files need updates."""
    suggestions = []

    # systemArchitecture.md suggestions
    if categories["architecture"] or categories["database"] or categories["config"]:
        reasons = []
        if categories["architecture"]:
            reasons.append("core architecture files changed")
        if categories["database"]:
            reasons.append("database schema modified")
        if categories["config"]:
            reasons.append("configuration updated")

        suggestions.append({
            "file": "systemArchitecture.md",
            "reason": ", ".join(reasons),
            "priority": "high"
        })

    # keyPairResponsibility.md suggestions
    if categories["modules"] or categories["api"]:
        reasons = []
        if categories["modules"]:
            unique_modules = list(set(categories["modules"]))
            reasons.append(f"{len(unique_modules)} module(s) modified")
        if categories["api"]:
            reasons.append(f"{len(categories['api'])} API file(s) changed")

        suggestions.append({
            "file": "keyPairResponsibility.md",
            "reason": ", ".join(reasons),
            "priority": "high" if categories["modules"] else "medium"
        })

    # techStack.md suggestions
    if categories["dependencies"]:
        suggestions.append({
            "file": "techStack.md",
            "reason": "dependencies updated - verify technology stack",
            "priority": "medium"
        })

    # glossary.md suggestions
    if categories["modules"] or (len(changed_files) > 10):
        suggestions.append({
            "file": "glossary.md",
            "reason": "new code may introduce domain-specific terms",
            "priority": "low"
        })

    return suggestions


def get_commit_messages(project_path: Path, since_commit: str, limit: int = 10) -> List[str]:
    """Get recent commit messages."""
    output = run_git_command(project_path, [
        'log', f'{since_commit}..HEAD', f'--format=%s', f'-{limit}'
    ])

    if output:
        return output.split('\n')
    return []


def main():
    """Main change analysis function."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Project path required"}))
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(json.dumps({"error": f"Project path not found: {project_path}"}))
        sys.exit(1)

    # Check if git repo
    if not is_git_repo(project_path):
        print(json.dumps({
            "error": "Not a git repository. Change analysis requires git.",
            "changed_files": 0
        }))
        sys.exit(0)

    # Get since commit (optional arg)
    if len(sys.argv) >= 3:
        since_commit = sys.argv[2]
    else:
        since_commit = get_last_doc_update_commit(project_path)

    # Get changed files
    changed_files = get_changed_files(project_path, since_commit)

    if not changed_files:
        print(json.dumps({
            "changed_files": 0,
            "categories": {},
            "descriptions": ["No changes since last documentation update"],
            "suggestions": [],
            "commit_messages": []
        }))
        sys.exit(0)

    # Categorize changes
    categories = categorize_changes(changed_files)

    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}

    # Generate descriptions
    descriptions = generate_change_descriptions(categories)

    # Generate suggestions
    suggestions = suggest_documentation_updates(categories, changed_files)

    # Get recent commit messages
    commit_messages = get_commit_messages(project_path, since_commit)

    output = {
        "changed_files": len(changed_files),
        "since_commit": since_commit,
        "categories": {k: len(v) for k, v in categories.items()},
        "category_details": categories,
        "descriptions": descriptions,
        "suggestions": suggestions,
        "commit_messages": commit_messages,
        "project_path": str(project_path)
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
