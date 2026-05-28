#!/usr/bin/env python3
"""
Project structure initializer for task-starter skill.
Creates the standard folder structure for Web development projects.
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


def to_kebab_case(name: str) -> str:
    """Convert a string to kebab-case."""
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    # Insert hyphen before uppercase letters and convert to lowercase
    name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)
    # Remove non-alphanumeric characters except hyphens
    name = re.sub(r'[^a-zA-Z0-9-]', '', name)
    # Convert to lowercase and remove consecutive hyphens
    name = re.sub(r'-+', '-', name.lower())
    result = name.strip('-')
    if not result:
        raise ValueError(
            "Project name must contain at least one alphanumeric character."
        )
    return result


def create_readme(project_path: Path, project_name: str, description: str = "") -> None:
    """Create initial README.md."""
    content = f"""# {project_name}

## 概要

{description if description else "<!-- プロジェクトの概要を記載 -->"}

## 目的

<!-- プロジェクトの目的を記載 -->

## ステータス

- [ ] 計画中
- [ ] 開発中
- [ ] レビュー中
- [ ] 完了
"""
    (project_path / "README.md").write_text(content, encoding="utf-8")


def create_directories(project_path: Path) -> None:
    """Create the standard directory structure."""
    dirs = [
        "references",
        "files",
        "specs",
        "todos",
    ]
    for dir_name in dirs:
        (project_path / dir_name).mkdir(parents=True, exist_ok=True)
        # Ensure .gitkeep exists so the directory is tracked by git
        gitkeep = project_path / dir_name / ".gitkeep"
        gitkeep.touch()


def init_project(
    base_dir: str,
    project_name: str,
    description: str = "",
) -> Path:
    """
    Initialize a new project structure.

    Args:
        base_dir: Base directory where the project folder will be created
        project_name: Name of the project
        description: Optional project description

    Returns:
        Path to the created project directory
    """
    # Generate folder name with date prefix
    date_prefix = datetime.now().strftime("%Y%m%d")
    kebab_name = to_kebab_case(project_name)
    folder_name = f"{date_prefix}-{kebab_name}"

    project_path = Path(base_dir) / folder_name

    # Create project directory (race-safe)
    try:
        project_path.mkdir(parents=True)
    except FileExistsError:
        raise FileExistsError(f"Project directory already exists: {project_path}")

    # Create structure
    create_directories(project_path)
    create_readme(project_path, project_name, description)

    return project_path


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new project structure for Web development tasks"
    )
    parser.add_argument(
        "project_name",
        help="Name of the project"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Base directory where the project will be created (default: current directory)"
    )
    parser.add_argument(
        "--description",
        default="",
        help="Project description"
    )

    args = parser.parse_args()

    try:
        project_path = init_project(
            args.path,
            args.project_name,
            args.description,
        )
        print(f"✅ Project initialized at: {project_path}")
        print(f"\nCreated structure:")
        for item in sorted(project_path.rglob("*")):
            rel_path = item.relative_to(project_path)
            indent = "  " * (len(rel_path.parts) - 1)
            if item.is_dir():
                print(f"{indent}📁 {item.name}/")
            else:
                print(f"{indent}📄 {item.name}")
    except FileExistsError as e:
        print(f"❌ Error: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
