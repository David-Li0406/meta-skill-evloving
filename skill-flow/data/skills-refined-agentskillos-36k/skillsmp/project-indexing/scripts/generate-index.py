#!/usr/bin/env python3
"""
Generate complete project index JSON from language detection and dependency scanning.

Usage:
    python generate-index.py /path/to/project
    python generate-index.py  # Uses current directory

This script orchestrates:
1. Language detection (detect-languages.py)
2. Dependency scanning (scan-dependencies.sh)
3. Key file identification
4. Structure analysis
5. Git metadata extraction
6. Final JSON generation
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone


def run_command(cmd, cwd=None):
    """Run command and return output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running {cmd[0]}: {e.stderr}", file=sys.stderr)
        return None


def detect_languages(project_root, script_dir):
    """Run language detection script."""
    script_path = script_dir / "detect-languages.py"
    output = run_command(["python3", str(script_path), project_root])

    if output:
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Error parsing language detection output: {e}", file=sys.stderr)
            return {}
    return {}


def scan_dependencies(project_root, script_dir):
    """Run dependency scanning script."""
    script_path = script_dir / "scan-dependencies.sh"
    output = run_command(["bash", str(script_path), project_root])

    if output:
        try:
            deps = json.loads(output)
            # Remove internal keys
            deps.pop("_generated", None)
            return deps
        except json.JSONDecodeError as e:
            print(f"Error parsing dependency scan output: {e}", file=sys.stderr)
            return {}
    return {}


def find_key_files(project_root):
    """Identify key project files."""
    project_path = Path(project_root).resolve()
    key_files = {
        "entry_points": [],
        "configs": [],
        "documentation": [],
        "tests": [],
        "build": []
    }

    # Entry points (language-specific patterns handled by detect-languages, add common ones here)
    entry_patterns = [
        "**/main.*", "**/app.*", "**/server.*", "**/index.*",
        "**/__main__.py", "**/manage.py"
    ]
    for pattern in entry_patterns:
        for file_path in project_path.glob(pattern):
            if file_path.is_file() and "test" not in str(file_path).lower():
                relative = file_path.relative_to(project_path)
                if str(relative) not in key_files["entry_points"]:
                    key_files["entry_points"].append(str(relative))

    # Configuration files
    config_patterns = [
        ".env.example", "config.yaml", "config/*.yaml", "*.config.js",
        "docker-compose*.yml", "Caddyfile", "nginx.conf"
    ]
    for pattern in config_patterns:
        for file_path in project_path.glob(pattern):
            if file_path.is_file():
                relative = file_path.relative_to(project_path)
                key_files["configs"].append(str(relative))

    # Documentation
    doc_patterns = [
        "README*", "CHANGELOG*", "CONTRIBUTING*", "LICENSE*",
        "CLAUDE.md", "docs/**/*.md"
    ]
    for pattern in doc_patterns:
        for file_path in project_path.glob(pattern):
            if file_path.is_file():
                relative = file_path.relative_to(project_path)
                key_files["documentation"].append(str(relative))

    # Test directories and files
    test_patterns = ["tests", "test", "**/tests", "**/*_test.*", "**/test_*.*"]
    for pattern in test_patterns:
        for path in project_path.glob(pattern):
            relative = path.relative_to(project_path)
            if path.is_dir():
                key_files["tests"].append(str(relative) + "/")
            elif path.is_file():
                key_files["tests"].append(str(relative))

    # Build files
    build_patterns = [
        "Dockerfile*", "Makefile", ".github/workflows/*.yml",
        ".gitlab-ci.yml", "build.sh", "deploy.sh"
    ]
    for pattern in build_patterns:
        for file_path in project_path.glob(pattern):
            if file_path.is_file():
                relative = file_path.relative_to(project_path)
                key_files["build"].append(str(relative))

    # Deduplicate and limit
    for category in key_files:
        key_files[category] = sorted(list(set(key_files[category])))[:20]

    return key_files


def analyze_structure(project_root):
    """Analyze project directory structure."""
    project_path = Path(project_root).resolve()

    # Ignore patterns
    ignore_patterns = [
        ".git", "node_modules", "target", "venv", ".venv",
        "__pycache__", "dist", "build", ".next", ".nuxt",
        "vendor", "deps", "_build", "zig-cache", "zig-out"
    ]

    # Count files and calculate size
    total_files = 0
    total_size_bytes = 0
    max_depth = 0

    for root, dirs, files in os.walk(project_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_patterns]

        # Calculate depth
        depth = len(Path(root).relative_to(project_path).parts)
        max_depth = max(max_depth, depth)

        # Count files and size
        for file in files:
            file_path = Path(root) / file
            try:
                total_files += 1
                total_size_bytes += file_path.stat().st_size
            except (OSError, PermissionError):
                pass  # Skip files we can't access

    total_size_mb = round(total_size_bytes / (1024 * 1024), 1)

    # Get root directories
    root_dirs = [d.name for d in project_path.iterdir() if d.is_dir() and d.name not in ignore_patterns]

    # Determine architecture (simple heuristic)
    architecture = "monolith"
    if (project_path / "Cargo.toml").exists():
        with open(project_path / "Cargo.toml") as f:
            if "[workspace]" in f.read():
                architecture = "monorepo"
    elif (project_path / "go.work").exists():
        architecture = "monorepo"
    elif (project_path / "pnpm-workspace.yaml").exists():
        architecture = "monorepo"
    elif len([d for d in root_dirs if d == "services" or d == "packages"]) > 0:
        architecture = "monorepo"
    elif "src" in root_dirs and "tests" in root_dirs and ("lib" in root_dirs or (project_path / "Cargo.toml").exists()):
        architecture = "library"

    return {
        "architecture": architecture,
        "root_dirs": sorted(root_dirs),
        "depth": max_depth,
        "total_files": total_files,
        "total_size_mb": total_size_mb,
        "ignored_dirs": ignore_patterns
    }


def get_git_metadata(project_root):
    """Extract git repository metadata."""
    git_dir = Path(project_root) / ".git"
    if not git_dir.exists():
        return None

    metadata = {}

    # Current branch
    branch = run_command(["git", "branch", "--show-current"], cwd=project_root)
    if branch:
        metadata["branch"] = branch

    # Check for changes
    status = run_command(["git", "status", "--porcelain"], cwd=project_root)
    metadata["has_changes"] = bool(status)

    # Last commit
    commit = run_command(["git", "rev-parse", "--short", "HEAD"], cwd=project_root)
    if commit:
        metadata["last_commit"] = commit

    # Remote URL
    remote = run_command(["git", "remote", "get-url", "origin"], cwd=project_root)
    if remote:
        metadata["remote"] = remote

    # Recent tags
    tags = run_command(["git", "tag", "--sort=-creatordate"], cwd=project_root)
    if tags:
        metadata["tags"] = tags.split("\n")[:5]  # Last 5 tags

    return metadata


def generate_index(project_root):
    """Generate complete project index."""
    project_path = Path(project_root).resolve()
    script_dir = Path(__file__).parent

    # Gather all data
    print("Detecting languages...", file=sys.stderr)
    languages = detect_languages(str(project_path), script_dir)

    print("Scanning dependencies...", file=sys.stderr)
    dependencies = scan_dependencies(str(project_path), script_dir)

    print("Identifying key files...", file=sys.stderr)
    key_files = find_key_files(project_path)

    print("Analyzing structure...", file=sys.stderr)
    structure = analyze_structure(project_path)

    print("Extracting git metadata...", file=sys.stderr)
    git_metadata = get_git_metadata(project_path)

    # Build index
    index = {
        "schema_version": "1.0.0",
        "indexed_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_path),
        "languages": languages,
        "dependencies": dependencies,
        "key_files": key_files,
        "structure": structure
    }

    # Add git metadata if available
    if git_metadata:
        index["git"] = git_metadata

    return index


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

    # Generate index
    try:
        index = generate_index(project_root)

        # Output JSON
        print(json.dumps(index, indent=2))

        sys.exit(0)

    except Exception as e:
        print(f"Error generating index: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
