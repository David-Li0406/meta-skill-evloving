#!/usr/bin/env python3
"""
Semantic phase detection for automatic chunk creation.

Analyzes project structure, plan files, and git history to infer logical phases.

Usage:
    python create-phases.py [project_root]
    python create-phases.py  # Uses current directory
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone


def detect_from_plan_file(project_root):
    """Extract phases from plan file if exists."""
    plans_dir = Path("/root/.claude/plans")

    if not plans_dir.exists():
        return []

    # Find most recent plan file
    plan_files = sorted(plans_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not plan_files:
        return []

    plan_file = plan_files[0]
    phases = []

    with open(plan_file) as f:
        content = f.read()

    # Extract markdown headers (##)
    for line in content.split("\n"):
        if line.startswith("## "):
            phase_name = line[3:].strip()
            # Skip metadata sections
            if not any(skip in phase_name.lower() for skip in ["summary", "timeline", "overview", "scope"]):
                phases.append({
                    "name": phase_name,
                    "description": f"Phase extracted from plan: {plan_file.name}",
                    "source": "plan_file"
                })

    return phases


def detect_from_directory_structure(project_root):
    """Infer phases from directory structure."""
    project_path = Path(project_root).resolve()
    phases = []

    # Common phase indicators in directory names
    phase_indicators = {
        "setup": ("Setup & Configuration", "Initial project setup and dependencies"),
        "config": ("Configuration", "Project configuration files"),
        "core": ("Core Implementation", "Core functionality and business logic"),
        "api": ("API Integration", "REST API endpoints and integration"),
        "database": ("Database Setup", "Database schema and migrations"),
        "auth": ("Authentication", "User authentication and authorization"),
        "frontend": ("Frontend", "User interface implementation"),
        "ui": ("User Interface", "UI components and layouts"),
        "tests": ("Testing", "Test suite and quality assurance"),
        "docs": ("Documentation", "Project documentation"),
    }

    for indicator, (name, desc) in phase_indicators.items():
        # Check if directory exists (case-insensitive)
        for dir_path in project_path.iterdir():
            if dir_path.is_dir() and indicator in dir_path.name.lower():
                phases.append({
                    "name": name,
                    "description": desc,
                    "source": "directory_structure",
                    "directory": str(dir_path.relative_to(project_path))
                })
                break

    return phases


def infer_files_for_phase(project_root, phase):
    """Infer which files belong to a phase."""
    project_path = Path(project_root).resolve()
    files = []

    # Keywords to match in file paths
    keywords = []
    name = phase["name"].lower()

    if "setup" in name or "config" in name:
        keywords = ["setup", "config", "requirements", "cargo.toml", "go.mod", "package.json"]
    elif "database" in name:
        keywords = ["database", "models", "migrations", "schema", "db"]
    elif "api" in name:
        keywords = ["api", "routes", "endpoints", "controllers"]
    elif "auth" in name:
        keywords = ["auth", "login", "jwt", "token", "session"]
    elif "test" in name:
        keywords = ["test", "spec", "_test.", "test_"]
    elif "frontend" in name or "ui" in name:
        keywords = ["frontend", "ui", "components", "views", "templates"]
    elif "doc" in name:
        keywords = ["doc", "README", "guide", ".md"]

    # Scan project for matching files
    if keywords:
        for pattern in ["**/*.py", "**/*.rs", "**/*.go", "**/*.js", "**/*.md"]:
            for file_path in project_path.glob(pattern):
                # Skip common ignore patterns
                if any(ignore in str(file_path) for ignore in ["node_modules", "target", "venv", "__pycache__"]):
                    continue

                # Check if file matches any keyword
                file_str = str(file_path).lower()
                if any(keyword in file_str for keyword in keywords):
                    relative = file_path.relative_to(project_path)
                    files.append(str(relative))

    # Limit to 50 files per phase
    return files[:50]


def generate_chunks(project_root):
    """Generate complete chunks structure."""
    # Detect phases from multiple sources
    phases = []

    # Try plan file first
    plan_phases = detect_from_plan_file(project_root)
    if plan_phases:
        phases.extend(plan_phases)

    # Supplement with directory-based detection
    if not phases:
        dir_phases = detect_from_directory_structure(project_root)
        phases.extend(dir_phases)

    # If still no phases, create default structure
    if not phases:
        phases = [
            {"name": "Phase 1: Setup", "description": "Initial project setup", "source": "default"},
            {"name": "Phase 2: Core Implementation", "description": "Core functionality", "source": "default"},
            {"name": "Phase 3: Testing", "description": "Tests and QA", "source": "default"}
        ]

    # Build chunks
    chunks = []
    for i, phase in enumerate(phases, 1):
        chunk_id = f"chunk_phase_{i}_{phase['name'].lower().replace(' ', '_').replace(':', '')}"

        # Infer files for this phase
        files = infer_files_for_phase(project_root, phase)

        # Entry points (first 2 files)
        entry_points = files[:2]

        # Dependencies (each phase depends on previous)
        dependencies = []
        if i > 1:
            prev_chunk_id = f"chunk_phase_{i-1}_{phases[i-2]['name'].lower().replace(' ', '_').replace(':', '')}"
            dependencies.append(prev_chunk_id)

        chunks.append({
            "id": chunk_id,
            "name": phase["name"],
            "description": phase["description"],
            "files": files,
            "entry_points": entry_points,
            "dependencies": dependencies,
            "status": "pending",
            "completion": 0
        })

    # Build final structure
    result = {
        "strategy": "phase-based",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(Path(project_root).resolve()),
        "chunks": chunks,
        "current_chunk": chunks[0]["id"] if chunks else None,
        "metadata": {
            "total_chunks": len(chunks),
            "completed_chunks": 0,
            "overall_progress": 0
        }
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

    try:
        # Generate chunks
        chunks = generate_chunks(project_root)

        # Output JSON
        print(json.dumps(chunks, indent=2))

        sys.exit(0)

    except Exception as e:
        print(f"Error generating phases: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
