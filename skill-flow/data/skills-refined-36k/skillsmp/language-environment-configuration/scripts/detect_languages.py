#!/usr/bin/env python3
"""
Detect programming languages in a project directory.

Scans for language-specific configuration files and source code
to determine which languages are used.

Usage:
    python3 detect_languages.py /path/to/project

Output: JSON with detected languages and their indicator files
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set

# Language indicators
RUST_INDICATORS = {
    "Cargo.toml",
    "Cargo.lock",
    "rust-toolchain.toml",
    "rust-toolchain",
}

PYTHON_INDICATORS = {
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "Pipfile",
    "Pipfile.lock",
    ".python-version",
    "poetry.lock",
}

NODEJS_INDICATORS = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    ".nvmrc",
    ".node-version",
}

# Source file extensions
RUST_EXTENSIONS = {".rs"}
PYTHON_EXTENSIONS = {".py"}
NODEJS_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"}


def find_indicators(project_path: Path, indicators: Set[str]) -> List[str]:
    """Find indicator files in project directory."""
    found = []
    for indicator in indicators:
        file_path = project_path / indicator
        if file_path.exists():
            found.append(indicator)
    return found


def find_source_files(
    project_path: Path, extensions: Set[str], max_depth: int = 3
) -> List[str]:
    """Find source files with given extensions."""
    found = []

    for root, dirs, files in os.walk(project_path):
        # Calculate depth
        depth = len(Path(root).relative_to(project_path).parts)
        if depth > max_depth:
            continue

        # Skip common directories
        dirs[:] = [
            d
            for d in dirs
            if d
            not in {
                "node_modules",
                "target",
                ".git",
                "__pycache__",
                ".venv",
                "venv",
                "dist",
                "build",
            }
        ]

        for file in files:
            if Path(file).suffix in extensions:
                rel_path = Path(root).relative_to(project_path) / file
                found.append(str(rel_path))
                if len(found) >= 5:  # Limit to 5 examples
                    return found

    return found


def detect_languages(project_path: str) -> Dict:
    """
    Detect languages used in a project.

    Args:
        project_path: Path to project directory

    Returns:
        Dict with detection results for each language
    """
    path = Path(project_path).resolve()

    if not path.exists() or not path.is_dir():
        return {"error": f"Directory not found: {project_path}"}

    results = {}

    # Detect Rust
    rust_indicators = find_indicators(path, RUST_INDICATORS)
    rust_sources = find_source_files(path, RUST_EXTENSIONS) if not rust_indicators else []
    results["rust"] = {
        "detected": bool(rust_indicators or rust_sources),
        "indicators": rust_indicators,
        "source_files": rust_sources[:3],  # Include up to 3 examples
    }

    # Detect Python
    python_indicators = find_indicators(path, PYTHON_INDICATORS)
    python_sources = (
        find_source_files(path, PYTHON_EXTENSIONS) if not python_indicators else []
    )
    results["python"] = {
        "detected": bool(python_indicators or python_sources),
        "indicators": python_indicators,
        "source_files": python_sources[:3],
    }

    # Detect Node.js
    nodejs_indicators = find_indicators(path, NODEJS_INDICATORS)
    nodejs_sources = (
        find_source_files(path, NODEJS_EXTENSIONS) if not nodejs_indicators else []
    )
    results["nodejs"] = {
        "detected": bool(nodejs_indicators or nodejs_sources),
        "indicators": nodejs_indicators,
        "source_files": nodejs_sources[:3],
    }

    return results


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 detect_languages.py /path/to/project", file=sys.stderr)
        sys.exit(1)

    project_path = sys.argv[1]
    results = detect_languages(project_path)

    print(json.dumps(results, indent=2))

    # Exit with appropriate code
    detected = any(lang["detected"] for lang in results.values() if isinstance(lang, dict))
    sys.exit(0 if detected else 1)


if __name__ == "__main__":
    main()
