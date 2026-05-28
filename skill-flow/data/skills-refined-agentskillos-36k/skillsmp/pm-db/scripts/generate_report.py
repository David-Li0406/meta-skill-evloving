#!/usr/bin/env python3
"""
Dashboard Report Generator for Project Management Database

Generates formatted status dashboard with job metrics.

Usage:
    python3 skills/pm-db/scripts/generate_report.py
    python3 skills/pm-db/scripts/generate_report.py --format json
    python3 skills/pm-db/scripts/generate_report.py --project auth
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


def format_status_bar(completed: int, total: int, width: int = 20) -> str:
    """Create ASCII progress bar."""
    if total == 0:
        filled = 0
    else:
        filled = int((completed / total) * width)

    bar = "█" * filled + "░" * (width - filled)
    percent = int((completed / total) * 100) if total > 0 else 0
    return f"[{bar}] {completed}/{total} ({percent}%)"


def format_text_dashboard(data: dict) -> str:
    """Format dashboard as text."""
    lines = []

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📊 Project Management Dashboard")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    # Active jobs
    active = data['active_jobs']
    pending = data['pending_jobs']

    lines.append(f"🔥 Active Jobs: {len(active)}")
    for job in active[:5]:  # Show first 5
        lines.append(f"   • {job['name']} (ID: {job['id']})")
        lines.append(f"     Agent: {job['assigned_agent'] or 'N/A'}")
        lines.append(f"     Started: {job['started_at']}")

    if len(active) > 5:
        lines.append(f"   ... and {len(active) - 5} more")

    lines.append("")
    lines.append(f"⏳ Pending Jobs: {len(pending)}")
    for job in pending[:5]:
        lines.append(f"   • {job['name']} (ID: {job['id']})")
        lines.append(f"     Priority: {job['priority']}")

    if len(pending) > 5:
        lines.append(f"   ... and {len(pending) - 5} more")

    # Recent completions
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"✅ Recent Completions (Last 7 Days): {len(data['recent_completions'])}")
    lines.append("")

    for job in data['recent_completions'][:10]:
        status_icon = "✅" if job['status'] == 'completed' else "❌"
        lines.append(f"   {status_icon} {job['name']}")
        lines.append(f"      Completed: {job['completed_at']}")
        if job['duration_seconds']:
            duration = job['duration_seconds'] / 60
            lines.append(f"      Duration: {duration:.1f} minutes")

    # Velocity
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📈 Velocity Metrics")
    lines.append("")

    vel = data['velocity']
    lines.append(f"   This week: {vel['this_week']} jobs completed")
    lines.append(f"   Last week: {vel['last_week']} jobs completed")

    trend = vel['trend_percent']
    if trend > 0:
        lines.append(f"   Trend: ↗️  +{trend}% (improving)")
    elif trend < 0:
        lines.append(f"   Trend: ↘️  {trend}% (declining)")
    else:
        lines.append(f"   Trend: → 0% (stable)")

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


def format_markdown_dashboard(data: dict) -> str:
    """Format dashboard as Markdown."""
    lines = []

    lines.append("# Project Management Dashboard")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Active jobs
    lines.append("## 🔥 Active Jobs")
    lines.append("")

    if data['active_jobs']:
        lines.append("| Job | ID | Agent | Started |")
        lines.append("|-----|-------|--------|---------|")
        for job in data['active_jobs']:
            lines.append(f"| {job['name']} | {job['id']} | {job['assigned_agent'] or 'N/A'} | {job['started_at']} |")
    else:
        lines.append("*No active jobs*")

    lines.append("")

    # Pending jobs
    lines.append("## ⏳ Pending Jobs")
    lines.append("")

    if data['pending_jobs']:
        lines.append("| Job | ID | Priority |")
        lines.append("|-----|-------|----------|")
        for job in data['pending_jobs']:
            lines.append(f"| {job['name']} | {job['id']} | {job['priority']} |")
    else:
        lines.append("*No pending jobs*")

    lines.append("")

    # Recent completions
    lines.append("## ✅ Recent Completions (Last 7 Days)")
    lines.append("")

    if data['recent_completions']:
        lines.append("| Job | Status | Completed | Duration |")
        lines.append("|-----|--------|-----------|----------|")
        for job in data['recent_completions'][:10]:
            status = "✅" if job['status'] == 'completed' else "❌"
            duration = f"{job['duration_seconds'] / 60:.1f}m" if job['duration_seconds'] else "N/A"
            lines.append(f"| {job['name']} | {status} | {job['completed_at']} | {duration} |")
    else:
        lines.append("*No completions in the last 7 days*")

    lines.append("")

    # Velocity
    lines.append("## 📈 Velocity Metrics")
    lines.append("")

    vel = data['velocity']
    lines.append(f"- **This week:** {vel['this_week']} jobs completed")
    lines.append(f"- **Last week:** {vel['last_week']} jobs completed")

    trend = vel['trend_percent']
    if trend > 0:
        lines.append(f"- **Trend:** ↗️ +{trend}% (improving)")
    elif trend < 0:
        lines.append(f"- **Trend:** ↘️ {trend}% (declining)")
    else:
        lines.append(f"- **Trend:** → 0% (stable)")

    return "\n".join(lines)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate dashboard report")
    parser.add_argument(
        "--format",
        choices=['text', 'json', 'markdown'],
        default='text',
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--project",
        help="Filter by project name"
    )

    args = parser.parse_args()

    with ProjectDatabase() as db:
        # Generate dashboard data
        dashboard = db.generate_dashboard()

        # Format output
        if args.format == 'json':
            # Convert to JSON-serializable format
            print(json.dumps(dashboard, indent=2, default=str))

        elif args.format == 'markdown':
            print(format_markdown_dashboard(dashboard))

        else:  # text
            print(format_text_dashboard(dashboard))


if __name__ == "__main__":
    main()
