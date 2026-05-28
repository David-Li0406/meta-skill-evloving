#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Initialize FORGE in a project directory."""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def get_forge_dir(base_dir: Path | None = None) -> Path:
    """Get the .forge directory path."""
    base = base_dir or Path.cwd()
    return base / ".forge"


def create_config(forge_dir: Path, project_name: str) -> None:
    """Create the config.yaml file."""
    config = {
        "project": project_name,
        "version": "2.0.0",
        "created": datetime.now(timezone.utc).isoformat(),
        "phases": ["Focus", "Orchestrate", "Refine", "Generate", "Evaluate"],
    }
    config_path = forge_dir / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def create_context(forge_dir: Path, project_name: str) -> None:
    """Create the context.md file."""
    content = f"""# {project_name} - FORGE Context

## Project Overview

<!-- Describe the project purpose and scope -->

## Architecture Decisions

<!-- Document key architectural choices -->

## Vocabulary

<!-- Define project-specific terms -->

## Conventions

<!-- Document coding standards and patterns -->
"""
    context_path = forge_dir / "context.md"
    with open(context_path, "w") as f:
        f.write(content)


def create_learnings(forge_dir: Path) -> None:
    """Create the learnings.md file."""
    content = """# FORGE Learnings

Accumulated knowledge from development cycles.

## Patterns

<!-- Successful approaches to reuse -->

## Anti-Patterns

<!-- Approaches to avoid -->

## Decisions

<!-- Key decisions and their rationale -->

## Tools

<!-- Useful tools and techniques -->
"""
    learnings_path = forge_dir / "learnings.md"
    with open(learnings_path, "w") as f:
        f.write(content)


def initialize(base_dir: Path | None = None, project_name: str | None = None) -> bool:
    """Initialize FORGE in the specified directory."""
    base = base_dir or Path.cwd()
    forge_dir = get_forge_dir(base)

    if forge_dir.exists():
        print(f"FORGE already initialized at {forge_dir}")
        return False

    # Determine project name
    if not project_name:
        project_name = base.name

    # Create directory structure
    forge_dir.mkdir(parents=True)
    (forge_dir / "cycles" / "active").mkdir(parents=True)
    (forge_dir / "cycles" / "completed").mkdir(parents=True)

    # Create files
    create_config(forge_dir, project_name)
    create_context(forge_dir, project_name)
    create_learnings(forge_dir)

    print(f"FORGE initialized at {forge_dir}")
    print(f"  - config.yaml: Project configuration")
    print(f"  - context.md: AI assistant context")
    print(f"  - learnings.md: Knowledge base")
    print(f"  - cycles/: Development cycle storage")
    print()
    print("Next: Start a cycle with 'uv run forge_cycle.py new \"feature-name\"'")

    return True


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize FORGE in a project directory"
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="Directory to initialize (default: current directory)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Project name (default: directory name)",
    )

    args = parser.parse_args()

    success = initialize(base_dir=args.dir, project_name=args.name)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
