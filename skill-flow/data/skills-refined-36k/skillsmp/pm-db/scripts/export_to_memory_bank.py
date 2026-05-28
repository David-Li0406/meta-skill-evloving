#!/usr/bin/env python3
"""
Memory Bank Export Script for Project Management Database

Exports project data to per-project Memory Banks.

CRITICAL: This uses PER-PROJECT Memory Banks, not global ~/.claude/memory-bank/
Each project has its own Memory Bank at {filesystem_path}/memory-bank/

Usage:
    python3 skills/pm-db/scripts/export_to_memory_bank.py
    python3 skills/pm-db/scripts/export_to_memory_bank.py --project my-app
    python3 skills/pm-db/scripts/export_to_memory_bank.py --dry-run
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
import json

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


def ensure_memory_bank_structure(memory_bank_path: Path) -> bool:
    """
    Ensure Memory Bank directory exists with minimal structure.

    Args:
        memory_bank_path: Path to Memory Bank directory

    Returns:
        True if structure created/verified, False on error
    """
    try:
        # Create memory-bank directory if needed
        memory_bank_path.mkdir(parents=True, exist_ok=True)

        # Create minimal files if they don't exist
        files_to_create = {
            'activeContext.md': """# Active Context

## Current Work

No active work tracked yet.

## Recent Updates

(Auto-updated by pm-db system)
""",
            'progress.md': """# Progress

## Recent Completions

(Auto-updated by pm-db system)

## Metrics

(Auto-updated by pm-db system)
""",
            'productContext.md': """# Product Context

## Product Overview

(To be filled in by team)
""",
            'codebaseSummary.md': """# Codebase Summary

## Architecture

(To be filled in by team)
""",
            'teamInfo.md': """# Team Information

## Team Members

(To be filled in by team)
""",
            'projectbrief.md': """# Project Brief

## Overview

(To be filled in by team)
"""
        }

        for filename, default_content in files_to_create.items():
            file_path = memory_bank_path / filename
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    f.write(default_content)
                print(f"   ✅ Created: {filename}")
            else:
                print(f"   ✓ Exists: {filename}")

        return True

    except Exception as e:
        print(f"   ❌ Error creating structure: {e}")
        return False


def format_job_summary(job: Dict[str, Any], db: ProjectDatabase) -> str:
    """
    Format job as markdown summary.

    Args:
        job: Job dict
        db: Database instance

    Returns:
        Markdown formatted job summary
    """
    lines = []

    # Job header
    status_icon = {
        'pending': '⏳',
        'in-progress': '▶️',
        'completed': '✅',
        'failed': '❌'
    }.get(job['status'], '❓')

    lines.append(f"### {status_icon} {job['name']}")
    lines.append(f"**Status:** {job['status']}")

    if job['priority']:
        lines.append(f"**Priority:** {job['priority']}")

    if job['assigned_agent']:
        lines.append(f"**Agent:** {job['assigned_agent']}")

    # Timestamps
    if job['started_at']:
        lines.append(f"**Started:** {job['started_at']}")

    if job['completed_at']:
        lines.append(f"**Completed:** {job['completed_at']}")

    # Duration
    if job['duration_seconds']:
        duration_min = job['duration_seconds'] / 60
        lines.append(f"**Duration:** {duration_min:.1f} minutes")

    # Task summary
    tasks = db.get_tasks(job['id'])
    if tasks:
        completed = sum(1 for t in tasks if t['status'] == 'completed')
        total = len(tasks)
        lines.append(f"**Tasks:** {completed}/{total} completed")

    lines.append("")  # Empty line
    return "\n".join(lines)


def export_to_active_context(
    project: Dict[str, Any],
    db: ProjectDatabase,
    memory_bank_path: Path
) -> bool:
    """
    Update activeContext.md with current work.

    Args:
        project: Project dict
        db: Database instance
        memory_bank_path: Path to Memory Bank

    Returns:
        True on success, False on error
    """
    try:
        # Get active and pending jobs
        active_jobs = db.list_jobs(status='in-progress', limit=10)
        pending_jobs = db.list_jobs(status='pending', limit=10)

        # Build content
        lines = [
            f"# Active Context: {project['name']}",
            "",
            f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Current Work",
            ""
        ]

        if active_jobs:
            lines.append(f"### Active Jobs ({len(active_jobs)})")
            lines.append("")
            for job in active_jobs:
                lines.append(format_job_summary(job, db))
        else:
            lines.append("No active jobs.")
            lines.append("")

        if pending_jobs:
            lines.append(f"### Pending Jobs ({len(pending_jobs)})")
            lines.append("")
            for job in pending_jobs[:5]:  # Show first 5
                lines.append(f"- {job['name']} (Priority: {job['priority'] or 'normal'})")
            if len(pending_jobs) > 5:
                lines.append(f"- ... and {len(pending_jobs) - 5} more")
            lines.append("")

        # Recent updates section
        lines.append("## Recent Updates")
        lines.append("")

        # Get recent completions (last 7 days)
        recent = db.conn.execute(
            """
            SELECT * FROM jobs
            WHERE status IN ('completed', 'failed')
            AND completed_at >= datetime('now', '-7 days')
            ORDER BY completed_at DESC
            LIMIT 10
            """).fetchall()

        if recent:
            for job_row in recent:
                job = dict(job_row)
                lines.append(f"- {job['completed_at']}: {job['name']} ({job['status']})")
        else:
            lines.append("No recent completions.")

        lines.append("")
        lines.append("---")
        lines.append("*Auto-updated by pm-db export system*")

        # Write file
        active_context_file = memory_bank_path / "activeContext.md"
        with open(active_context_file, 'w') as f:
            f.write("\n".join(lines))

        return True

    except Exception as e:
        print(f"   ❌ Error updating activeContext.md: {e}")
        return False


def export_to_progress(
    project: Dict[str, Any],
    db: ProjectDatabase,
    memory_bank_path: Path
) -> bool:
    """
    Update progress.md with completion metrics.

    Args:
        project: Project dict
        db: Database instance
        memory_bank_path: Path to Memory Bank

    Returns:
        True on success, False on error
    """
    try:
        # Get dashboard metrics
        dashboard = db.generate_dashboard()

        # Build content
        lines = [
            f"# Progress: {project['name']}",
            "",
            f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Recent Completions (Last 7 Days)",
            ""
        ]

        if dashboard['recent_completions']:
            for job in dashboard['recent_completions'][:10]:
                status_icon = "✅" if job['status'] == 'completed' else "❌"
                duration = f" ({job['duration_seconds'] / 60:.1f}m)" if job['duration_seconds'] else ""
                lines.append(f"- {status_icon} {job['name']}{duration}")
                lines.append(f"  Completed: {job['completed_at']}")
        else:
            lines.append("No completions in the last 7 days.")

        lines.append("")
        lines.append("## Velocity Metrics")
        lines.append("")

        vel = dashboard['velocity']
        lines.append(f"- **This week:** {vel['this_week']} jobs completed")
        lines.append(f"- **Last week:** {vel['last_week']} jobs completed")

        trend = vel['trend_percent']
        if trend > 0:
            lines.append(f"- **Trend:** ↗️ +{trend}% (improving)")
        elif trend < 0:
            lines.append(f"- **Trend:** ↘️ {trend}% (declining)")
        else:
            lines.append(f"- **Trend:** → 0% (stable)")

        lines.append("")
        lines.append("## Overall Statistics")
        lines.append("")

        # Job counts
        total_jobs = db.conn.execute("SELECT COUNT(*) as count FROM jobs").fetchone()['count']
        completed = db.conn.execute(
            "SELECT COUNT(*) as count FROM jobs WHERE status = 'completed'"
        ).fetchone()['count']
        failed = db.conn.execute(
            "SELECT COUNT(*) as count FROM jobs WHERE status = 'failed'"
        ).fetchone()['count']

        lines.append(f"- **Total jobs:** {total_jobs}")
        lines.append(f"- **Completed:** {completed}")
        lines.append(f"- **Failed:** {failed}")

        if total_jobs > 0:
            success_rate = (completed / total_jobs) * 100
            lines.append(f"- **Success rate:** {success_rate:.1f}%")

        lines.append("")
        lines.append("---")
        lines.append("*Auto-updated by pm-db export system*")

        # Write file
        progress_file = memory_bank_path / "progress.md"
        with open(progress_file, 'w') as f:
            f.write("\n".join(lines))

        return True

    except Exception as e:
        print(f"   ❌ Error updating progress.md: {e}")
        return False


def export_project(
    project_id: int,
    db: ProjectDatabase,
    dry_run: bool = False
) -> bool:
    """
    Export single project to its Memory Bank.

    Args:
        project_id: Project ID
        db: Database instance
        dry_run: If True, only show what would happen

    Returns:
        True on success, False on error
    """
    # Get project
    project = db.get_project(project_id)
    if not project:
        print(f"❌ Project ID {project_id} not found")
        return False

    print(f"\n📦 Exporting: {project['name']}")

    # Get filesystem_path
    filesystem_path = project.get('filesystem_path')
    if not filesystem_path:
        print(f"   ⚠️  No filesystem_path set, skipping")
        return False

    # Build Memory Bank path
    memory_bank_path = Path(filesystem_path) / "memory-bank"

    print(f"   Target: {memory_bank_path}")

    if dry_run:
        print(f"   🔍 DRY RUN - Would export to {memory_bank_path}")
        return True

    # Ensure structure
    print(f"   📁 Ensuring Memory Bank structure...")
    if not ensure_memory_bank_structure(memory_bank_path):
        return False

    # Export activeContext.md
    print(f"   📝 Updating activeContext.md...")
    if not export_to_active_context(project, db, memory_bank_path):
        return False

    # Export progress.md
    print(f"   📊 Updating progress.md...")
    if not export_to_progress(project, db, memory_bank_path):
        return False

    print(f"   ✅ Export complete!")
    return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Export to Memory Banks")
    parser.add_argument(
        "--project",
        help="Export specific project (by name)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without making changes"
    )

    args = parser.parse_args()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📤 Memory Bank Export")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    with ProjectDatabase() as db:
        # Get projects to export
        if args.project:
            # Export specific project
            project = db.get_project_by_name(args.project)
            if not project:
                print(f"\n❌ Project '{args.project}' not found")
                sys.exit(1)

            projects = [project]
        else:
            # Export all projects
            projects = db.list_projects()

        if not projects:
            print("\n⚠️  No projects found")
            sys.exit(0)

        print(f"\nFound {len(projects)} project(s) to export")

        # Export each project
        success_count = 0
        skip_count = 0
        error_count = 0

        for project in projects:
            try:
                if export_project(project['id'], db, dry_run=args.dry_run):
                    if args.dry_run:
                        skip_count += 1
                    else:
                        success_count += 1
                else:
                    skip_count += 1
            except Exception as e:
                print(f"   ❌ Error: {e}")
                error_count += 1

        # Summary
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("✅ Export Complete")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print()
        if args.dry_run:
            print(f"DRY RUN - Would export: {skip_count}")
        else:
            print(f"Exported: {success_count}")
            print(f"Skipped: {skip_count}")
            if error_count:
                print(f"Errors: {error_count}")
        print()


if __name__ == "__main__":
    main()
