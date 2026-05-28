#!/usr/bin/env python3
"""Detect Python project stack and generate commands."""

import json
import subprocess
import sys
from pathlib import Path


def detect_stack():
    """Detect project configuration and return commands."""

    try:
        repo_root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    except subprocess.CalledProcessError:
        print("Error: Not a git repository", file=sys.stderr)
        sys.exit(1)

    # Check for pyproject.toml
    pyproject_path = repo_root / "pyproject.toml"
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found - not a Python/uv project", file=sys.stderr)
        sys.exit(1)

    # Parse pyproject.toml
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("Error: tomllib/tomli not available. Install tomli: pip install tomli", file=sys.stderr)
            sys.exit(1)

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    project_name = pyproject.get("project", {}).get("name", "unknown")

    # Check for dependencies
    dependencies = pyproject.get("project", {}).get("dependencies", [])
    dev_dependencies = pyproject.get("project", {}).get("optional-dependencies", {}).get("dev", [])
    all_deps = dependencies + dev_dependencies

    # Convert to lowercase strings for easier checking
    all_deps_str = " ".join(str(dep).lower() for dep in all_deps)

    has_pytest = "pytest" in all_deps_str
    has_coverage = "pytest-cov" in all_deps_str or "coverage" in all_deps_str
    has_sqlalchemy = "sqlalchemy" in all_deps_str
    has_alembic = "alembic" in all_deps_str

    # Generate commands
    config = {
        "stack": "python",
        "package_manager": "uv",
        "project_name": project_name,
        "repo_root": str(repo_root),
        # Core commands
        "install_cmd": "uv sync",
        "test_cmd": "uv run pytest" if has_pytest else 'echo "No pytest configured"',
        "build_cmd": "uv build",
        # Coverage commands
        "coverage_cmd": "uv run pytest --cov=src --cov-report=term" if has_coverage else "uv run pytest",
        "coverage_check": "uv run pytest --cov=src --cov-report=term --cov-fail-under=80" if has_coverage else 'echo "No coverage tool"',
        # Database commands
        "database": "sqlite" if not has_sqlalchemy else "postgresql",
        "orm": "none" if not has_sqlalchemy else "sqlalchemy",
        "migrate_cmd": "uv run alembic upgrade head" if has_alembic else 'echo "No migrations"',
        # Container
        "container": "podman",
        "has_containerfile": (repo_root / "Containerfile").exists(),
        "has_compose": (repo_root / "podman-compose.yml").exists(),
        # Test framework details
        "test_framework": "pytest" if has_pytest else "none",
        "has_pytest_cov": has_coverage,
    }

    return config


if __name__ == "__main__":
    config = detect_stack()
    print(json.dumps(config, indent=2))
