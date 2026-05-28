#!/usr/bin/env python3
"""
Comprehensive language detection for polyglot projects.

Detects 8 programming languages:
- Python, Rust, Go, Julia, Elixir, C++, Zig, JavaScript/TypeScript

Usage:
    python detect-languages.py /path/to/project
    python detect-languages.py  # Uses current directory
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict

# Language definitions
LANGUAGES = {
    "Python": {
        "extensions": [".py", ".pyw", ".pyx", ".pyi"],
        "manifests": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "poetry.lock"],
        "entry_patterns": ["main.py", "__main__.py", "app.py", "manage.py"],
        "ignore_dirs": ["venv", ".venv", "env", "site-packages", "__pycache__"]
    },
    "Rust": {
        "extensions": [".rs"],
        "manifests": ["Cargo.toml", "Cargo.lock", "rust-toolchain.toml"],
        "entry_patterns": ["main.rs", "lib.rs"],
        "ignore_dirs": ["target"]
    },
    "Go": {
        "extensions": [".go"],
        "manifests": ["go.mod", "go.sum", "go.work"],
        "entry_patterns": ["main.go"],
        "ignore_dirs": ["vendor"]
    },
    "Julia": {
        "extensions": [".jl"],
        "manifests": ["Project.toml", "Manifest.toml", "JuliaProject.toml"],
        "entry_patterns": [],
        "ignore_dirs": []
    },
    "Elixir": {
        "extensions": [".ex", ".exs"],
        "manifests": ["mix.exs", "mix.lock"],
        "entry_patterns": ["application.ex"],
        "ignore_dirs": ["deps", "_build"]
    },
    "C++": {
        "extensions": [".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"],
        "manifests": ["CMakeLists.txt", "Makefile", "meson.build", "configure.ac"],
        "entry_patterns": ["main.cpp", "main.cc"],
        "ignore_dirs": ["build", "cmake-build-debug", "cmake-build-release"]
    },
    "Zig": {
        "extensions": [".zig"],
        "manifests": ["build.zig"],
        "entry_patterns": ["main.zig"],
        "ignore_dirs": ["zig-cache", "zig-out"]
    },
    "JavaScript": {
        "extensions": [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"],
        "manifests": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "tsconfig.json"],
        "entry_patterns": ["index.js", "server.js", "app.js", "main.js", "index.ts"],
        "ignore_dirs": ["node_modules", "dist", "build", ".next", ".nuxt"]
    }
}

# Global ignore patterns
GLOBAL_IGNORE = [".git", ".svn", ".hg", "__pycache__", ".pytest_cache", ".mypy_cache"]


def should_ignore(path, language_config):
    """Check if path should be ignored."""
    path_str = str(path)

    # Global ignores
    for ignore in GLOBAL_IGNORE:
        if f"/{ignore}/" in path_str or path_str.endswith(f"/{ignore}"):
            return True

    # Language-specific ignores
    for ignore in language_config["ignore_dirs"]:
        if f"/{ignore}/" in path_str or path_str.endswith(f"/{ignore}"):
            return True

    return False


def count_files_by_language(project_root):
    """Count source files for each language."""
    project_path = Path(project_root).resolve()
    counts = defaultdict(int)

    for lang_name, lang_config in LANGUAGES.items():
        for ext in lang_config["extensions"]:
            for file_path in project_path.rglob(f"*{ext}"):
                if not should_ignore(file_path, lang_config):
                    counts[lang_name] += 1

    return counts


def find_manifests(project_root):
    """Find package manager manifests for each language."""
    project_path = Path(project_root).resolve()
    manifests = defaultdict(list)

    for lang_name, lang_config in LANGUAGES.items():
        for manifest_name in lang_config["manifests"]:
            for manifest_path in project_path.rglob(manifest_name):
                # Only top-level or service-level manifests, not nested in deps
                if not should_ignore(manifest_path, lang_config):
                    relative_path = manifest_path.relative_to(project_path)
                    manifests[lang_name].append(str(relative_path))

    return manifests


def find_entry_points(project_root):
    """Find main entry point files for each language."""
    project_path = Path(project_root).resolve()
    entry_points = defaultdict(list)

    for lang_name, lang_config in LANGUAGES.items():
        for pattern in lang_config["entry_patterns"]:
            for entry_path in project_path.rglob(pattern):
                if not should_ignore(entry_path, lang_config):
                    relative_path = entry_path.relative_to(project_path)
                    entry_points[lang_name].append(str(relative_path))

    return entry_points


def calculate_percentages(counts):
    """Calculate percentage for each language."""
    total = sum(counts.values())
    if total == 0:
        return {}

    percentages = {}
    for lang, count in counts.items():
        percentages[lang] = round((count / total) * 100, 1)

    return percentages


def determine_primary_language(counts, manifests, entry_points):
    """Determine the primary language based on multiple factors."""
    if not counts:
        return None

    # Score each language
    scores = {}
    for lang in counts:
        score = counts[lang]  # Base score: file count

        # Bonus for having manifests
        if manifests.get(lang):
            score += 100

        # Bonus for having entry points
        if entry_points.get(lang):
            score += 50

        scores[lang] = score

    # Return language with highest score
    primary = max(scores, key=scores.get)
    return primary


def detect_languages(project_root):
    """Main language detection function."""
    counts = count_files_by_language(project_root)
    percentages = calculate_percentages(counts)
    manifests = find_manifests(project_root)
    entry_points = find_entry_points(project_root)
    primary = determine_primary_language(counts, manifests, entry_points)

    # Build result
    result = {}
    for lang in counts:
        result[lang] = {
            "file_count": counts[lang],
            "percentage": percentages.get(lang, 0.0),
            "primary": (lang == primary),
            "manifests": manifests.get(lang, []),
            "entry_points": entry_points.get(lang, [])
        }

    return result


def main():
    """CLI entry point."""
    # Get project root from args or use current directory
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()

    # Validate path
    if not os.path.isdir(project_root):
        print(f"Error: {project_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Detect languages
    try:
        languages = detect_languages(project_root)

        # Output JSON
        print(json.dumps(languages, indent=2))

        # Exit with 0 if languages found, 1 if none
        sys.exit(0 if languages else 1)

    except Exception as e:
        print(f"Error detecting languages: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
