#!/usr/bin/env python3
"""
Spec Import Script for Project Management Database

Automatically imports specifications from /job-queue/feature-*/docs/.

Usage:
    python3 skills/pm-db/scripts/import_specs.py
    python3 skills/pm-db/scripts/import_specs.py --project message-well

Features:
- Scans job-queue for feature folders
- Reads FRD, FRS, GS, TR, task-list files
- Captures project filesystem_path for Memory Bank exports
- Handles missing files gracefully
- Batch import with transactions
"""

import sys
from pathlib import Path
import json

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


def infer_project_path(feature_folder: Path) -> str:
    """
    Infer project filesystem path from feature folder name.

    Args:
        feature_folder: Path to feature folder (e.g., job-queue/feature-auth)

    Returns:
        Inferred project path
    """
    # Extract feature name (e.g., "feature-auth" -> "auth")
    feature_name = feature_folder.name.replace('feature-', '')

    # Common project location patterns
    home = Path.home()

    # Try common locations
    candidates = [
        home / "applications" / feature_name,
        home / "projects" / feature_name,
        home / "repos" / feature_name,
        home / feature_name
    ]

    for path in candidates:
        if path.exists():
            return str(path)

    # Default: assume applications folder
    return str(home / "applications" / feature_name)


def prompt_for_path(project_name: str, inferred_path: str) -> str:
    """
    Prompt user for project filesystem path.

    Args:
        project_name: Project name
        inferred_path: Inferred path

    Returns:
        Validated filesystem path
    """
    print(f"\n📍 Project Path Needed: {project_name}")
    print(f"   Inferred path: {inferred_path}")

    response = input(f"   Use this path? (Y/n) or enter custom path: ").strip()

    if not response or response.lower() == 'y':
        path = inferred_path
    else:
        path = response

    # Validate path
    path_obj = Path(path)
    if not path_obj.is_absolute():
        print(f"   ⚠️  Path must be absolute, converting...")
        path = str(path_obj.absolute())

    # Warn if path doesn't exist
    if not path_obj.exists():
        print(f"   ⚠️  Warning: Path does not exist yet: {path}")
        confirm = input(f"   Use anyway? (y/N): ").strip()
        if confirm.lower() != 'y':
            return prompt_for_path(project_name, inferred_path)

    return path


def import_spec(
    db: ProjectDatabase,
    feature_folder: Path,
    project_filter: str = None,
    auto_confirm: bool = False
) -> bool:
    """
    Import a single spec from feature folder.

    Args:
        db: Database instance
        feature_folder: Path to feature folder
        project_filter: Optional project name filter
        auto_confirm: If True, don't prompt for paths

    Returns:
        True if imported, False if skipped
    """
    docs_folder = feature_folder / "docs"

    if not docs_folder.exists():
        return False

    # Extract feature name
    feature_name = feature_folder.name

    # Filter by project if specified
    if project_filter and project_filter not in feature_name:
        return False

    print(f"\n📦 Processing: {feature_name}")

    # Read spec files
    spec_files = {
        'frd': docs_folder / "FRD.md",
        'frs': docs_folder / "FRS.md",
        'gs': docs_folder / "GS.md",
        'tr': docs_folder / "TR.md",
        'task_list': docs_folder / "task-list.md"
    }

    contents = {}
    found_files = 0

    for key, file_path in spec_files.items():
        if file_path.exists():
            with open(file_path, 'r') as f:
                contents[key] = f.read()
            found_files += 1
            print(f"   ✅ Found: {file_path.name}")
        else:
            contents[key] = None
            print(f"   ⚠️  Missing: {file_path.name}")

    if found_files == 0:
        print(f"   ❌ No spec files found, skipping")
        return False

    # Extract project name from feature name
    # e.g., "feature-auth" or "feature-sqlite-pm-db" -> extract meaningful name
    project_name = feature_name.replace('feature-', '')

    # Check if project exists
    existing_project = db.get_project_by_name(project_name)

    if existing_project:
        project_id = existing_project['id']
        print(f"   📁 Using existing project: {project_name} (ID: {project_id})")
        filesystem_path = existing_project.get('filesystem_path')
    else:
        # Need to create project - get filesystem_path
        inferred_path = infer_project_path(feature_folder)

        if auto_confirm:
            filesystem_path = inferred_path
        else:
            filesystem_path = prompt_for_path(project_name, inferred_path)

        print(f"   📁 Creating project: {project_name}")
        print(f"   📍 Filesystem path: {filesystem_path}")

        project_id = db.create_project(
            name=project_name,
            description=f"Auto-imported from {feature_name}",
            filesystem_path=filesystem_path
        )

    # Check if spec already exists
    specs = db.list_specs(project_id=project_id)
    existing_spec = next((s for s in specs if s['name'] == feature_name), None)

    if existing_spec:
        print(f"   ⚠️  Spec already exists (ID: {existing_spec['id']}), skipping")
        return False

    # Create spec
    spec_id = db.create_spec(
        project_id=project_id,
        name=feature_name,
        frd_content=contents['frd'],
        frs_content=contents['frs'],
        gs_content=contents['gs'],
        tr_content=contents['tr'],
        task_list_content=contents['task_list']
    )

    print(f"   ✅ Spec imported (ID: {spec_id})")

    return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Import specs from job-queue")
    parser.add_argument(
        "--project",
        help="Filter by project name (e.g., 'auth')"
    )
    parser.add_argument(
        "--job-queue-dir",
        default=str(Path.home() / ".claude" / "job-queue"),
        help="Path to job-queue directory"
    )
    parser.add_argument(
        "--auto-confirm",
        action="store_true",
        help="Auto-confirm inferred paths (no prompts)"
    )

    args = parser.parse_args()

    job_queue = Path(args.job_queue_dir)

    if not job_queue.exists():
        print(f"❌ Job queue directory not found: {job_queue}")
        sys.exit(1)

    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📥 Spec Import")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\nScanning: {job_queue}")

    # Find all feature-* folders
    feature_folders = sorted(job_queue.glob("feature-*"))

    if not feature_folders:
        print(f"\n⚠️  No feature folders found")
        sys.exit(0)

    print(f"Found {len(feature_folders)} feature folder(s)")

    # Import each spec
    imported = 0
    skipped = 0

    with ProjectDatabase() as db:
        for feature_folder in feature_folders:
            if import_spec(db, feature_folder, args.project, args.auto_confirm):
                imported += 1
            else:
                skipped += 1

    # Summary
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Import Complete")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\nImported: {imported}")
    print(f"Skipped: {skipped}")
    print(f"Total processed: {imported + skipped}")
    print()


if __name__ == "__main__":
    main()
