#!/usr/bin/env python3
"""
Parse language version requirements from project configuration files.

Extracts version specifications for Rust, Python, and Node.js from
their respective configuration files.

Usage:
    python3 parse_versions.py /path/to/project

Output: JSON with version requirements for each detected language
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional

try:
    import tomli as toml  # Python < 3.11
except ImportError:
    try:
        import tomllib as toml  # Python >= 3.11
    except ImportError:
        import toml  # Fallback to toml package


def parse_rust_version(project_path: Path) -> Optional[str]:
    """
    Parse Rust version from rust-toolchain.toml or rust-toolchain file.

    Args:
        project_path: Path to project directory

    Returns:
        Rust version string or None
    """
    # Try rust-toolchain.toml first
    toolchain_toml = project_path / "rust-toolchain.toml"
    if toolchain_toml.exists():
        try:
            with open(toolchain_toml, "rb") as f:
                data = toml.load(f)
                return data.get("toolchain", {}).get("channel")
        except Exception as e:
            print(f"Warning: Could not parse {toolchain_toml}: {e}", file=sys.stderr)

    # Try rust-toolchain (plain text)
    toolchain_txt = project_path / "rust-toolchain"
    if toolchain_txt.exists():
        try:
            with open(toolchain_txt) as f:
                return f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read {toolchain_txt}: {e}", file=sys.stderr)

    return None


def parse_python_version(project_path: Path) -> Optional[str]:
    """
    Parse Python version from pyproject.toml or .python-version.

    Args:
        project_path: Path to project directory

    Returns:
        Python version string or None
    """
    # Try pyproject.toml first
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            with open(pyproject, "rb") as f:
                data = toml.load(f)

                # Check project.requires-python
                requires_python = data.get("project", {}).get("requires-python")
                if requires_python:
                    # Extract version from spec like ">=3.14.2" or "^3.14"
                    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", requires_python)
                    if match:
                        return match.group(1)

                # Check tool.poetry.dependencies.python (Poetry projects)
                python_dep = (
                    data.get("tool", {}).get("poetry", {}).get("dependencies", {}).get("python")
                )
                if python_dep:
                    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", python_dep)
                    if match:
                        return match.group(1)

        except Exception as e:
            print(f"Warning: Could not parse {pyproject}: {e}", file=sys.stderr)

    # Try .python-version
    python_version_file = project_path / ".python-version"
    if python_version_file.exists():
        try:
            with open(python_version_file) as f:
                return f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read {python_version_file}: {e}", file=sys.stderr)

    return None


def parse_nodejs_version(project_path: Path) -> Optional[str]:
    """
    Parse Node.js version from .nvmrc, .node-version, or package.json.

    Args:
        project_path: Path to project directory

    Returns:
        Node.js version string or None
    """
    # Try .nvmrc first
    nvmrc = project_path / ".nvmrc"
    if nvmrc.exists():
        try:
            with open(nvmrc) as f:
                version = f.read().strip()
                # Return as-is (may be "lts/*", "node", "v18", etc.)
                return version
        except Exception as e:
            print(f"Warning: Could not read {nvmrc}: {e}", file=sys.stderr)

    # Try .node-version
    node_version_file = project_path / ".node-version"
    if node_version_file.exists():
        try:
            with open(node_version_file) as f:
                return f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read {node_version_file}: {e}", file=sys.stderr)

    # Try package.json engines field
    package_json = project_path / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                node_engine = data.get("engines", {}).get("node")
                if node_engine:
                    # Extract version from spec like ">=18.0.0"
                    match = re.search(r"(\d+(?:\.\d+)?(?:\.\d+)?)", node_engine)
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"Warning: Could not parse {package_json}: {e}", file=sys.stderr)

    return None


def parse_versions(project_path: str) -> Dict:
    """
    Parse version requirements for all languages.

    Args:
        project_path: Path to project directory

    Returns:
        Dict with version requirements for each language
    """
    path = Path(project_path).resolve()

    if not path.exists() or not path.is_dir():
        return {"error": f"Directory not found: {project_path}"}

    results = {
        "rust": parse_rust_version(path),
        "python": parse_python_version(path),
        "nodejs": parse_nodejs_version(path),
    }

    return results


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_versions.py /path/to/project", file=sys.stderr)
        sys.exit(1)

    project_path = sys.argv[1]
    results = parse_versions(project_path)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
